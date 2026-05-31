"""Admin dashboard stats + Leads (CRM) management. Admin/staff only."""
import re

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from core_utils import new_id, now_iso, paginate_response, serialize_list, success_response  # noqa: F401
from db import get_db
from security import require_role

router = APIRouter(prefix="/api/admin")

_CONTENT_COLLECTIONS = [
    "cms_services", "cms_cases", "cms_team", "cms_clients",
    "cms_tech", "cms_blog", "cms_careers", "cms_home_blocks",
]


@router.get("/stats")
async def stats(_user=Depends(require_role("admin", "staff"))):
    db = get_db()
    counts = {}
    for col in _CONTENT_COLLECTIONS + ["crm_leads", "system_users", "media_assets"]:
        counts[col] = await db[col].count_documents({"voided": {"$ne": True}})
    new_leads = await db.crm_leads.count_documents({"voided": {"$ne": True}, "status": "new"})
    recent_cursor = db.crm_leads.find({"voided": {"$ne": True}}).sort("created_at", -1).limit(5)
    recent = serialize_list(await recent_cursor.to_list(5))
    return success_response({"counts": counts, "new_leads": new_leads, "recent_leads": recent})


@router.get("/leads")
async def list_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
    source: str | None = None,
    search: str | None = None,
    _user=Depends(require_role("admin", "staff")),
):
    db = get_db()
    flt = {"voided": {"$ne": True}}
    if status:
        flt["status"] = status
    if source:
        flt["source"] = source
    if search:
        flt["$or"] = [
            {"name": {"$regex": re.escape(search), "$options": "i"}},
            {"email": {"$regex": re.escape(search), "$options": "i"}},
            {"company": {"$regex": re.escape(search), "$options": "i"}},
        ]
    total = await db.crm_leads.count_documents(flt)
    cursor = db.crm_leads.find(flt).sort("created_at", -1).skip((page - 1) * limit).limit(limit)
    docs = serialize_list(await cursor.to_list(limit))
    return paginate_response(docs, total, page, limit)


class LeadStatusIn(BaseModel):
    status: str = Field(min_length=1, max_length=40)


@router.patch("/leads/{lead_id}")
async def update_lead(lead_id: str, payload: LeadStatusIn, _user=Depends(require_role("admin", "staff"))):
    if payload.status not in {"new", "contacted", "qualified", "won", "lost", "archived"}:
        raise HTTPException(status_code=422, detail={"code": "VALIDATION_ERROR", "message": "Status tidak valid"})
    db = get_db()
    res = await db.crm_leads.update_one(
        {"id": lead_id, "voided": {"$ne": True}},
        {"$set": {"status": payload.status, "updated_at": now_iso()}},
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Lead tidak ditemukan"})
    return success_response({"id": lead_id, "status": payload.status})
