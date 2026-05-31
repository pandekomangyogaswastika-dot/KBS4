"""
Phase 19A: Testimonials
CRUD endpoints for client testimonials (admin-only write, public read).
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from db import get_db
from core_utils import success_response
from security import require_role

router = APIRouter(prefix="/api/testimonials", tags=["Content"])

# Pydantic models
class BilingualField(BaseModel):
    id: str
    en: str

class TestimonialCreate(BaseModel):
    client_id: Optional[str] = None
    person_name: str = Field(..., min_length=1)
    person_role: BilingualField
    company: str = Field(..., min_length=1)
    quote: BilingualField
    rating: Optional[int] = Field(None, ge=1, le=5)
    video_url: Optional[str] = None
    case_id: Optional[str] = None
    photo_url: Optional[str] = None
    featured: bool = False
    order: int = 0
    status: str = "published"

class TestimonialUpdate(BaseModel):
    person_name: Optional[str] = None
    person_role: Optional[BilingualField] = None
    company: Optional[str] = None
    quote: Optional[BilingualField] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    video_url: Optional[str] = None
    case_id: Optional[str] = None
    photo_url: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = None
    status: Optional[str] = None

class TestimonialResponse(BaseModel):
    id: str
    client_id: Optional[str]
    person_name: str
    person_role: BilingualField
    company: str
    quote: BilingualField
    rating: Optional[int]
    video_url: Optional[str]
    case_id: Optional[str]
    photo_url: Optional[str]
    featured: bool
    order: int
    status: str
    created_at: str
    updated_at: Optional[str]

@router.get("/", response_model=List[TestimonialResponse])
async def get_testimonials(
    status: Optional[str] = "published",
    featured: Optional[bool] = None,
    db=Depends(get_db)
):
    """
    Get all testimonials (public endpoint).
    Filters: status (default: published), featured.
    """
    filter_query = {}
    if status:
        filter_query["status"] = status
    if featured is not None:
        filter_query["featured"] = featured
    
    cursor = db.cms_testimonials.find(filter_query).sort("order", 1)
    items = await cursor.to_list(length=100)
    return [{"id": t["id"], **{k: v for k, v in t.items() if k != "_id"}} for t in items]

@router.get("/{testimonial_id}", response_model=TestimonialResponse)
async def get_testimonial(testimonial_id: str, db=Depends(get_db)):
    """Get single testimonial by ID."""
    doc = await db.cms_testimonials.find_one({"id": testimonial_id})
    if not doc:
        raise HTTPException(404, "Testimonial not found")
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.post("/", response_model=TestimonialResponse, dependencies=[Depends(require_role("admin"))])
async def create_testimonial(payload: TestimonialCreate, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Create new testimonial (admin only)."""
    doc = {
        "id": str(uuid.uuid4()),
        **payload.dict(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": None
    }
    await db.cms_testimonials.insert_one(doc)
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.patch("/{testimonial_id}", response_model=TestimonialResponse, dependencies=[Depends(require_role("admin"))])
async def update_testimonial(
    testimonial_id: str,
    payload: TestimonialUpdate,
    db=Depends(get_db),
    _user=Depends(require_role("admin"))
):
    """Update testimonial (admin only)."""
    existing = await db.cms_testimonials.find_one({"id": testimonial_id})
    if not existing:
        raise HTTPException(404, "Testimonial not found")
    
    update_data = {k: v for k, v in payload.dict(exclude_unset=True).items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.cms_testimonials.update_one({"id": testimonial_id}, {"$set": update_data})
    
    updated_doc = await db.cms_testimonials.find_one({"id": testimonial_id})
    return {"id": updated_doc["id"], **{k: v for k, v in updated_doc.items() if k != "_id"}}

@router.delete("/{testimonial_id}", dependencies=[Depends(require_role("admin"))])
async def delete_testimonial(testimonial_id: str, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Delete testimonial (admin only)."""
    result = await db.cms_testimonials.delete_one({"id": testimonial_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Testimonial not found")
    return success_response({"deleted": True})
