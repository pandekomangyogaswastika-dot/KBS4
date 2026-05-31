"""
Phase 19F: Resources / Downloads Center
CRUD endpoints for downloadable resources (admin-only write, public read).
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from db import get_db
from core_utils import success_response
from security import require_role

router = APIRouter(prefix="/api/resources", tags=["Content"])

# Pydantic models
class BilingualField(BaseModel):
    id: str
    en: str

class ResourceCreate(BaseModel):
    slug: str = Field(..., min_length=1, pattern=r'^[a-z0-9-]+$')
    title: BilingualField
    type: str = Field(..., pattern=r'^(whitepaper|ebook|template|guide|case_study)$')
    cover: Optional[str] = None
    description: BilingualField
    file_url: str
    file_size: Optional[int] = None  # in bytes
    gated: bool = True
    download_count: int = 0
    tags: List[str] = []
    published_at: Optional[str] = None
    status: str = "published"

class ResourceUpdate(BaseModel):
    title: Optional[BilingualField] = None
    type: Optional[str] = None
    cover: Optional[str] = None
    description: Optional[BilingualField] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    gated: Optional[bool] = None
    tags: Optional[List[str]] = None
    published_at: Optional[str] = None
    status: Optional[str] = None

class ResourceResponse(BaseModel):
    id: str
    slug: str
    title: BilingualField
    type: str
    cover: Optional[str] = None
    description: BilingualField
    file_url: str
    file_size: Optional[int] = None
    gated: bool
    download_count: int
    tags: List[str]
    published_at: Optional[str] = None
    status: str
    created_at: str
    updated_at: Optional[str] = None

@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    type: Optional[str] = None,
    tag: Optional[str] = None,
    db=Depends(get_db)
):
    """
    Get all resources (public endpoint).
    Filter by type or tag if provided.
    """
    filter_query = {"status": "published"}
    if type:
        filter_query["type"] = type
    if tag:
        filter_query["tags"] = tag
    
    cursor = db.cms_resources.find(filter_query).sort("published_at", -1)
    items = await cursor.to_list(length=100)
    return [{"id": r["id"], **{k: v for k, v in r.items() if k != "_id"}} for r in items]

@router.get("/{slug}", response_model=ResourceResponse)
async def get_resource(slug: str, db=Depends(get_db)):
    """Get single resource by slug."""
    doc = await db.cms_resources.find_one({"slug": slug, "status": "published"})
    if not doc:
        raise HTTPException(404, "Resource not found")
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.post("/", response_model=ResourceResponse, dependencies=[Depends(require_role("admin"))])
async def create_resource(payload: ResourceCreate, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Create new resource (admin only)."""
    # Check slug uniqueness
    existing = await db.cms_resources.find_one({"slug": payload.slug})
    if existing:
        raise HTTPException(400, "Slug already exists")
    
    doc = {
        "id": str(uuid.uuid4()),
        **payload.dict(),
        "download_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": None
    }
    
    if not doc.get("published_at"):
        doc["published_at"] = doc["created_at"]
    
    await db.cms_resources.insert_one(doc)
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.patch("/{resource_id}", response_model=ResourceResponse, dependencies=[Depends(require_role("admin"))])
async def update_resource(
    resource_id: str,
    payload: ResourceUpdate,
    db=Depends(get_db),
    _user=Depends(require_role("admin"))
):
    """Update resource (admin only)."""
    existing = await db.cms_resources.find_one({"id": resource_id})
    if not existing:
        raise HTTPException(404, "Resource not found")
    
    update_data = {k: v for k, v in payload.dict(exclude_unset=True).items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.cms_resources.update_one({"id": resource_id}, {"$set": update_data})
    
    updated_doc = await db.cms_resources.find_one({"id": resource_id})
    return {"id": updated_doc["id"], **{k: v for k, v in updated_doc.items() if k != "_id"}}

@router.delete("/{resource_id}", dependencies=[Depends(require_role("admin"))])
async def delete_resource(resource_id: str, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Delete resource (admin only)."""
    result = await db.cms_resources.delete_one({"id": resource_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Resource not found")
    return success_response({"deleted": True})

@router.post("/{resource_id}/track-download", dependencies=[Depends(require_role("admin"))])
async def track_download(resource_id: str, db=Depends(get_db)):
    """
    Increment download counter.
    Public endpoint (no auth) untuk tracking.
    """
    result = await db.cms_resources.update_one(
        {"id": resource_id},
        {"$inc": {"download_count": 1}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Resource not found")
    return success_response({"tracked": True})
