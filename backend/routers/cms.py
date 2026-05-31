"""Advanced CMS (Fase 3C). Generic schema-light CRUD for all cms_* collections.

The public site already reads these collections (routers/content.py), so admin
edits reflect on the public site once published. Bilingual fields ({id,en}) and
nested arrays are stored as-is from the client; base/system fields are enforced.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from core_utils import new_id, now_iso, serialize_doc, serialize_list, success_response
from db import get_db
from security import require_role
from routers.content import invalidate_public_cache

router = APIRouter(prefix="/api/admin/cms")

RESOURCES = {
    "services": "cms_services",
    "cases": "cms_cases",
    "team": "cms_team",
    "clients": "cms_clients",
    "tech": "cms_tech",
    "blog": "cms_blog",
    "careers": "cms_careers",
    "home-blocks": "cms_home_blocks",
}
PROTECTED = {"id", "created_at", "created_by", "voided", "voided_at", "_id"}


# Mapping from admin resource key → public collection name (for cache invalidation)
def _invalidate(resource: str, slug: str | None = None) -> None:
    col = RESOURCES.get(resource)
    if col:
        invalidate_public_cache(col, slug)


def _col(resource: str) -> str:
    col = RESOURCES.get(resource)
    if not col:
        raise HTTPException(status_code=404, detail={"code": "RESOURCE_NOT_FOUND", "message": f"Resource '{resource}' tidak dikenal"})
    return col


def _clean(body: dict) -> dict:
    return {k: v for k, v in (body or {}).items() if k not in PROTECTED}


# ---- Settings (declare before /{resource} to avoid capture) ----------------
@router.get("/settings")
async def get_settings(_user=Depends(require_role("admin", "staff"))):
    db = get_db()
    doc = await db.cms_pages.find_one({"key": "site", "voided": {"$ne": True}})
    return success_response(serialize_doc(doc) if doc else {})


class SettingsIn(BaseModel):
    data: dict


@router.put("/settings")
async def update_settings(payload: SettingsIn, user=Depends(require_role("admin", "staff"))):
    db = get_db()
    updates = _clean(payload.data)
    updates.pop("key", None)
    updates["updated_at"] = now_iso()
    existing = await db.cms_pages.find_one({"key": "site"})
    if existing:
        await db.cms_pages.update_one({"key": "site"}, {"$set": updates})
    else:
        now = now_iso()
        await db.cms_pages.insert_one({"id": new_id(), "key": "site", "created_at": now,
                                       "created_by": user["id"], "voided": False, **updates})
    fresh = await db.cms_pages.find_one({"key": "site"})
    # Phase 13: settings flush
    from routers.content import invalidate_public_cache as _flush
    _flush()  # full namespace flush — settings affects whole site
    return success_response(serialize_doc(fresh))


# ---- Generic collection CRUD ----------------------------------------------
@router.get("/{resource}")
async def list_items(resource: str, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    col = _col(resource)
    docs = await db[col].find({"voided": {"$ne": True}}).sort([("order", 1), ("created_at", 1)]).to_list(500)
    return success_response(serialize_list(docs))


@router.post("/{resource}", status_code=201)
async def create_item(resource: str, body: dict, user=Depends(require_role("admin", "staff"))):
    db = get_db()
    col = _col(resource)
    doc = _clean(body)
    now = now_iso()
    if "order" not in doc or not isinstance(doc.get("order"), int):
        last = await db[col].find_one({"voided": {"$ne": True}}, sort=[("order", -1)])
        doc["order"] = (last.get("order", 0) + 1) if last and isinstance(last.get("order"), int) else 1
    doc["status"] = doc.get("status") if doc.get("status") in {"draft", "published"} else "draft"
    doc.update({"id": new_id(), "created_at": now, "updated_at": now, "created_by": user["id"],
                "voided": False, "voided_at": None})
    try:
        await db[col].insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail={"code": "DUPLICATE_SLUG", "message": "Slug sudah dipakai"})
    _invalidate(resource, doc.get("slug"))
    return success_response(serialize_doc(doc))


@router.get("/{resource}/{item_id}")
async def get_item(resource: str, item_id: str, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    col = _col(resource)
    doc = await db[col].find_one({"id": item_id, "voided": {"$ne": True}})
    if not doc:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Item tidak ditemukan"})
    return success_response(serialize_doc(doc))


@router.patch("/{resource}/{item_id}")
async def update_item(resource: str, item_id: str, body: dict, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    col = _col(resource)
    existing = await db[col].find_one({"id": item_id, "voided": {"$ne": True}})
    if not existing:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Item tidak ditemukan"})
    updates = _clean(body)
    if "status" in updates and updates["status"] not in {"draft", "published"}:
        updates.pop("status")
    updates["updated_at"] = now_iso()
    try:
        await db[col].update_one({"id": item_id}, {"$set": updates})
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail={"code": "DUPLICATE_SLUG", "message": "Slug sudah dipakai"})
    fresh = await db[col].find_one({"id": item_id})
    # Invalidate both old slug + new slug to be safe
    _invalidate(resource, existing.get("slug"))
    if fresh and fresh.get("slug") and fresh.get("slug") != existing.get("slug"):
        _invalidate(resource, fresh.get("slug"))
    return success_response(serialize_doc(fresh))


@router.post("/{resource}/{item_id}/publish")
async def publish_item(resource: str, item_id: str, _user=Depends(require_role("admin", "staff"))):
    return await _set_status(resource, item_id, "published")


@router.post("/{resource}/{item_id}/unpublish")
async def unpublish_item(resource: str, item_id: str, _user=Depends(require_role("admin", "staff"))):
    return await _set_status(resource, item_id, "draft")


async def _set_status(resource: str, item_id: str, status: str):
    db = get_db()
    col = _col(resource)
    existing = await db[col].find_one({"id": item_id, "voided": {"$ne": True}}, {"_id": 0, "slug": 1})
    res = await db[col].update_one({"id": item_id, "voided": {"$ne": True}}, {"$set": {"status": status, "updated_at": now_iso()}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Item tidak ditemukan"})
    _invalidate(resource, existing.get("slug") if existing else None)
    return success_response({"id": item_id, "status": status})


@router.delete("/{resource}/{item_id}")
async def delete_item(resource: str, item_id: str, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    col = _col(resource)
    existing = await db[col].find_one({"id": item_id, "voided": {"$ne": True}}, {"_id": 0, "slug": 1})
    res = await db[col].update_one({"id": item_id, "voided": {"$ne": True}}, {"$set": {"voided": True, "voided_at": now_iso(), "updated_at": now_iso()}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Item tidak ditemukan"})
    _invalidate(resource, existing.get("slug") if existing else None)
    return success_response({"id": item_id})


class ReorderIn(BaseModel):
    ids: list[str]


@router.post("/{resource}/reorder")
async def reorder_items(resource: str, payload: ReorderIn, _user=Depends(require_role("admin", "staff"))):
    db = get_db()
    col = _col(resource)
    now = now_iso()
    for idx, item_id in enumerate(payload.ids):
        await db[col].update_one({"id": item_id}, {"$set": {"order": idx + 1, "updated_at": now}})
    _invalidate(resource)
    return success_response({"count": len(payload.ids)})
