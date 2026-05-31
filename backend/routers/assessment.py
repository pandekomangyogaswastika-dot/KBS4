"""Assessment module (Fase 4). Public token-based client flow + admin management.

Public (no login, UUID token in URL): load/answer/submit/export/attachments.
Admin/staff (require_role): templates, create/list sessions, stats, acknowledge, delete.
Attachments stored via the TD-008 storage abstraction (LocalStorageBackend).
"""
import io
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from assessment_engine import compute_progress, get_all_question_ids
from assessment_pdf import build_pdf
from core_utils import new_id, now_iso, serialize_doc, serialize_list, success_response
from db import get_db
from security import require_role
from storage import get_storage

router = APIRouter(prefix="/api/assessment")

ALLOWED_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".xlsx", ".docx"}
MAX_BYTES = 10 * 1024 * 1024
MAX_PER_QUESTION = 5


def _ext(filename: str) -> str:
    return ("." + filename.rsplit(".", 1)[1].lower()) if filename and "." in filename else ""


async def _session_by_token(token: str) -> dict:
    db = get_db()
    s = await db.assessment_sessions.find_one({"token": token, "voided": {"$ne": True}})
    if not s:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Sesi tidak ditemukan / link tidak valid"})
    return s


async def _template_for(session: dict) -> dict:
    db = get_db()
    t = await db.assessment_templates.find_one({"id": session.get("template_id"), "voided": {"$ne": True}})
    if not t:
        raise HTTPException(status_code=404, detail={"code": "TEMPLATE_NOT_FOUND", "message": "Template tidak ditemukan"})
    return t


async def _answers_and_progress(session_id: str, template: dict):
    db = get_db()
    answers = serialize_list(await db.assessment_answers.find({"session_id": session_id}).to_list(1000))
    answers_map = {a["question_id"]: a for a in answers}
    progress = compute_progress(template, answers)
    return answers_map, progress


async def _attachments_grouped(session_id: str):
    db = get_db()
    docs = await db.assessment_attachments.find({"session_id": session_id}).sort("uploaded_at", -1).to_list(500)
    grouped: dict[str, list] = {}
    for a in serialize_list(docs):
        a.pop("storage_key", None)
        grouped.setdefault(a.get("question_id"), []).append(a)
    return grouped


# --- PUBLIC (token) ---------------------------------------------------------
@router.get("/sessions/{token}")
async def get_session(token: str):
    session = await _session_by_token(token)
    template = await _template_for(session)
    answers_map, progress = await _answers_and_progress(session["id"], template)
    attachments = await _attachments_grouped(session["id"])
    return success_response({
        "session": serialize_doc(session),
        "template": serialize_doc(template),
        "answers": answers_map,
        "progress": progress,
        "attachments": attachments,
    })


class AnswerItem(BaseModel):
    question_id: str
    value: Any = None
    skipped: bool = False
    other_text: str | None = None
    note: str | None = None


class AnswersBatch(BaseModel):
    answers: list[AnswerItem]


@router.patch("/sessions/{token}/answers")
async def save_answers(token: str, payload: AnswersBatch):
    db = get_db()
    session = await _session_by_token(token)
    if session.get("status") in ("submitted", "archived"):
        raise HTTPException(status_code=403, detail={"code": "SESSION_LOCKED", "message": "Sesi sudah dikirim, tidak bisa diubah"})
    template = await _template_for(session)
    valid = set(get_all_question_ids(template))
    upserts = 0
    for a in payload.answers:
        if a.question_id not in valid:
            continue
        doc = {
            "session_id": session["id"], "question_id": a.question_id, "value": a.value,
            "skipped": bool(a.skipped), "other_text": (a.other_text or "").strip() or None,
            "note": (a.note or "").strip() or None, "updated_at": now_iso(),
        }
        await db.assessment_answers.update_one(
            {"session_id": session["id"], "question_id": a.question_id}, {"$set": doc}, upsert=True)
        upserts += 1
    await db.assessment_sessions.update_one({"id": session["id"]}, {"$set": {"updated_at": now_iso()}})
    _, progress = await _answers_and_progress(session["id"], template)
    return success_response({"upserted": upserts, "progress": progress})


@router.post("/sessions/{token}/submit")
async def submit_session(token: str):
    db = get_db()
    session = await _session_by_token(token)
    if session.get("status") != "draft":
        raise HTTPException(status_code=400, detail={"code": "NOT_DRAFT", "message": "Sesi bukan dalam status draft"})
    await db.assessment_sessions.update_one({"id": session["id"]}, {"$set": {
        "status": "submitted", "submitted_at": now_iso(), "updated_at": now_iso(), "acknowledged_at": None}})
    return success_response({"id": session["id"], "status": "submitted"})


@router.get("/sessions/{token}/export.pdf")
async def export_pdf(token: str, locale: str = Query("id")):
    session = await _session_by_token(token)
    template = await _template_for(session)
    answers_map, progress = await _answers_and_progress(session["id"], template)
    attachments = await _attachments_grouped(session["id"])
    loc = locale if locale in ("id", "en") else (session.get("locale") or "id")
    pdf_bytes = build_pdf(serialize_doc(session), template, answers_map, progress, attachments, loc)
    fname = f"Discovery_{(session.get('client_name') or 'Client').replace(' ', '_')}.pdf"
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf",
                             headers={"Content-Disposition": f'attachment; filename="{fname}"'})


@router.get("/sessions/{token}/attachments")
async def list_attachments(token: str):
    session = await _session_by_token(token)
    grouped = await _attachments_grouped(session["id"])
    flat = [a for items in grouped.values() for a in items]
    return success_response(flat)


@router.post("/sessions/{token}/attachments", status_code=201)
async def upload_attachment(token: str, question_id: str = Form(...), file: UploadFile = File(...)):
    db = get_db()
    session = await _session_by_token(token)
    if session.get("status") in ("submitted", "archived"):
        raise HTTPException(status_code=403, detail={"code": "SESSION_LOCKED", "message": "Sesi sudah dikirim"})
    template = await _template_for(session)
    if question_id not in set(get_all_question_ids(template)):
        raise HTTPException(status_code=400, detail={"code": "INVALID_QUESTION", "message": "question_id tidak valid"})
    count = await db.assessment_attachments.count_documents({"session_id": session["id"], "question_id": question_id})
    if count >= MAX_PER_QUESTION:
        raise HTTPException(status_code=400, detail={"code": "ATTACH_LIMIT", "message": f"Maksimum {MAX_PER_QUESTION} file per pertanyaan"})
    ext = _ext(file.filename or "")
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail={"code": "ATTACH_TYPE", "message": f"Tipe {ext or '?'} tidak diizinkan"})
    raw = await file.read()
    if len(raw) == 0 or len(raw) > MAX_BYTES:
        raise HTTPException(status_code=400, detail={"code": "ATTACH_SIZE", "message": "Ukuran file 0 atau melebihi 10MB"})
    storage = get_storage()
    key = storage.save(raw, ext)
    att_id = new_id()
    doc = {
        "id": att_id, "session_id": session["id"], "question_id": question_id,
        "original_name": file.filename or "file", "storage_key": key, "storage_backend": storage.name,
        "mime_type": file.content_type or "application/octet-stream", "extension": ext,
        "size_bytes": len(raw), "uploaded_at": now_iso(),
    }
    await db.assessment_attachments.insert_one(doc)
    await db.assessment_sessions.update_one({"id": session["id"]}, {"$set": {"updated_at": now_iso()}})
    out = serialize_doc(dict(doc))
    out.pop("storage_key", None)
    return success_response(out)


@router.get("/sessions/{token}/attachments/{att_id}/download")
async def download_attachment(token: str, att_id: str):
    db = get_db()
    session = await _session_by_token(token)
    doc = await db.assessment_attachments.find_one({"id": att_id, "session_id": session["id"]})
    if not doc:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Lampiran tidak ditemukan"})
    p = get_storage().path(doc["storage_key"])
    if not p.exists():
        raise HTTPException(status_code=410, detail={"code": "FILE_GONE", "message": "File hilang di server"})
    return FileResponse(path=str(p), media_type=doc.get("mime_type") or "application/octet-stream",
                        filename=doc.get("original_name") or "download")


@router.delete("/sessions/{token}/attachments/{att_id}")
async def delete_attachment(token: str, att_id: str):
    db = get_db()
    session = await _session_by_token(token)
    if session.get("status") in ("submitted", "archived"):
        raise HTTPException(status_code=403, detail={"code": "SESSION_LOCKED", "message": "Sesi sudah dikirim"})
    doc = await db.assessment_attachments.find_one({"id": att_id, "session_id": session["id"]})
    if not doc:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Lampiran tidak ditemukan"})
    get_storage().delete(doc.get("storage_key", ""))
    await db.assessment_attachments.delete_one({"id": att_id})
    return success_response({"id": att_id})


# --- ADMIN (require_role admin/staff) ---------------------------------------
@router.get("/templates")
async def list_templates(_user=Depends(require_role("admin", "staff"))):
    db = get_db()
    docs = await db.assessment_templates.find({"voided": {"$ne": True}}).sort("created_at", -1).to_list(100)
    return success_response(serialize_list(docs))


@router.get("/templates/{template_id}")
async def get_template(template_id: str, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    doc = await db.assessment_templates.find_one({"id": template_id, "voided": {"$ne": True}})
    if not doc:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Template tidak ditemukan"})
    return success_response(serialize_doc(doc))


class SessionCreate(BaseModel):
    template_id: str
    client_name: str = Field(min_length=2, max_length=200)
    project_name: str | None = None
    contact_person: str | None = None
    contact_email: str | None = None
    notes: str | None = None
    locale: str = "id"


@router.post("/sessions", status_code=201)
async def create_session(payload: SessionCreate, user=Depends(require_role("admin", "staff"))):
    db = get_db()
    template = await db.assessment_templates.find_one({"id": payload.template_id, "voided": {"$ne": True}})
    if not template:
        raise HTTPException(status_code=404, detail={"code": "TEMPLATE_NOT_FOUND", "message": "Template tidak ditemukan"})
    now = now_iso()
    token = new_id()
    session = {
        "id": new_id(), "token": token, "template_id": payload.template_id,
        "client_name": payload.client_name.strip(),
        "project_name": (payload.project_name or "").strip() or None,
        "contact_person": (payload.contact_person or "").strip() or None,
        "contact_email": (payload.contact_email or "").strip() or None,
        "notes": (payload.notes or "").strip() or None,
        "locale": payload.locale if payload.locale in ("id", "en") else "id",
        "status": "draft", "created_at": now, "updated_at": now, "created_by": user["id"],
        "submitted_at": None, "acknowledged_at": None, "voided": False, "voided_at": None,
    }
    await db.assessment_sessions.insert_one(session)
    out = serialize_doc(dict(session))
    out["share_url"] = f"/assessment/{token}"
    return success_response(out)


@router.get("/sessions")
async def list_sessions(limit: int = Query(100, ge=1, le=300), _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    sessions = await db.assessment_sessions.find({"voided": {"$ne": True}}).sort("created_at", -1).to_list(limit)
    templates = {t["id"]: t for t in await db.assessment_templates.find({}).to_list(100)}
    out = []
    for s in sessions:
        tpl = templates.get(s.get("template_id"))
        answers = serialize_list(await db.assessment_answers.find({"session_id": s["id"]}).to_list(1000))
        progress = compute_progress(tpl, answers) if tpl else {"answered": 0, "total": 0, "percent": 0, "domains": []}
        row = serialize_doc(s)
        row["progress"] = progress
        row["share_url"] = f"/assessment/{s.get('token')}"
        row["is_new_submission"] = s.get("status") == "submitted" and not s.get("acknowledged_at")
        out.append(row)
    return success_response(out)


@router.get("/stats")
async def assessment_stats(_user=Depends(require_role("admin", "staff"))):
    db = get_db()
    flt = {"voided": {"$ne": True}}
    total = await db.assessment_sessions.count_documents(flt)
    submitted = await db.assessment_sessions.count_documents({**flt, "status": "submitted"})
    new_subs = await db.assessment_sessions.count_documents({**flt, "status": "submitted", "acknowledged_at": None})
    latest = await db.assessment_sessions.find({**flt, "status": "submitted"}).sort("submitted_at", -1).limit(1).to_list(1)
    return success_response({
        "total_sessions": total, "submitted_sessions": submitted, "draft_sessions": total - submitted,
        "new_submissions": new_subs,
        "latest_submission": serialize_doc(latest[0]) if latest else None,
    })


@router.post("/sessions/{session_id}/acknowledge")
async def acknowledge_session(session_id: str, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    res = await db.assessment_sessions.update_one({"id": session_id, "voided": {"$ne": True}}, {"$set": {"acknowledged_at": now_iso()}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Sesi tidak ditemukan"})
    return success_response({"id": session_id, "acknowledged_at": now_iso()})


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    session = await db.assessment_sessions.find_one({"id": session_id, "voided": {"$ne": True}})
    if not session:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Sesi tidak ditemukan"})
    storage = get_storage()
    atts = await db.assessment_attachments.find({"session_id": session_id}).to_list(500)
    for a in atts:
        storage.delete(a.get("storage_key", ""))
    await db.assessment_attachments.delete_many({"session_id": session_id})
    await db.assessment_answers.delete_many({"session_id": session_id})
    await db.assessment_sessions.update_one({"id": session_id}, {"$set": {"voided": True, "voided_at": now_iso(), "updated_at": now_iso()}})
    return success_response({"id": session_id})
