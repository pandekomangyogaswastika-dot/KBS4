"""
Phase 19C: FAQ
CRUD endpoints for frequently asked questions (admin-only write, public read).
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from db import get_db
from util import success_response
from security import require_role

router = APIRouter(prefix="/faq", tags=["Content"])

# Pydantic models
class BilingualField(BaseModel):
    id: str
    en: str

class FaqCreate(BaseModel):
    category: str = Field(..., min_length=1)  # general/pricing/technical/process
    question: BilingualField
    answer: BilingualField
    related_service_id: Optional[str] = None
    order: int = 0
    status: str = "published"

class FaqUpdate(BaseModel):
    category: Optional[str] = None
    question: Optional[BilingualField] = None
    answer: Optional[BilingualField] = None
    related_service_id: Optional[str] = None
    order: Optional[int] = None
    status: Optional[str] = None

class FaqResponse(BaseModel):
    id: str
    category: str
    question: BilingualField
    answer: BilingualField
    related_service_id: Optional[str]
    order: int
    status: str
    created_at: str
    updated_at: Optional[str]

@router.get("/", response_model=List[FaqResponse])
async def get_faqs(
    category: Optional[str] = None,
    db=Depends(get_db)
):
    """
    Get all FAQs (public endpoint).
    Filter by category if provided.
    """
    filter_query = {"status": "published"}
    if category:
        filter_query["category"] = category
    
    cursor = db.cms_faq.find(filter_query).sort([("category", 1), ("order", 1)])
    items = await cursor.to_list(length=200)
    return [{"id": f["id"], **{k: v for k, v in f.items() if k != "_id"}} for f in items]

@router.get("/{faq_id}", response_model=FaqResponse)
async def get_faq(faq_id: str, db=Depends(get_db)):
    """Get single FAQ by ID."""
    doc = await db.cms_faq.find_one({"id": faq_id})
    if not doc:
        raise HTTPException(404, "FAQ not found")
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.post("/", response_model=FaqResponse, dependencies=[Depends(require_role("admin"))])
async def create_faq(payload: FaqCreate, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Create new FAQ (admin only)."""
    doc = {
        "id": str(uuid.uuid4()),
        **payload.dict(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": None
    }
    await db.cms_faq.insert_one(doc)
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.patch("/{faq_id}", response_model=FaqResponse, dependencies=[Depends(require_role("admin"))])
async def update_faq(
    faq_id: str,
    payload: FaqUpdate,
    db=Depends(get_db),
    _user=Depends(require_role("admin"))
):
    """Update FAQ (admin only)."""
    existing = await db.cms_faq.find_one({"id": faq_id})
    if not existing:
        raise HTTPException(404, "FAQ not found")
    
    update_data = {k: v for k, v in payload.dict(exclude_unset=True).items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.cms_faq.update_one({"id": faq_id}, {"$set": update_data})
    
    updated_doc = await db.cms_faq.find_one({"id": faq_id})
    return {"id": updated_doc["id"], **{k: v for k, v in updated_doc.items() if k != "_id"}}

@router.delete("/{faq_id}", dependencies=[Depends(require_role("admin"))])
async def delete_faq(faq_id: str, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Delete FAQ (admin only)."""
    result = await db.cms_faq.delete_one({"id": faq_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "FAQ not found")
    return success_response({"deleted": True})
