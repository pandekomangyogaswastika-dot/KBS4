"""
Phase 19D: Pricing Packages
CRUD endpoints for service packages/pricing tiers (admin-only write, public read).
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from db import get_db
from core_utils import success_response
from security import require_role

router = APIRouter(prefix="/api/packages", tags=["Content"])

# Pydantic models
class BilingualField(BaseModel):
    id: str
    en: str

class PackageCreate(BaseModel):
    name: BilingualField
    tier: str = Field(..., pattern=r'^(starter|professional|enterprise)$')
    services_included: List[str] = []
    price_from: Optional[int] = None  # in IDR
    duration: Optional[str] = None  # e.g., "per month", "per project"
    features: List[BilingualField] = []
    popular: bool = False
    cta_label: Optional[BilingualField] = None
    order: int = 0
    status: str = "published"

class PackageUpdate(BaseModel):
    name: Optional[BilingualField] = None
    tier: Optional[str] = None
    services_included: Optional[List[str]] = None
    price_from: Optional[int] = None
    duration: Optional[str] = None
    features: Optional[List[BilingualField]] = None
    popular: Optional[bool] = None
    cta_label: Optional[BilingualField] = None
    order: Optional[int] = None
    status: Optional[str] = None

class PackageResponse(BaseModel):
    id: str
    name: BilingualField
    tier: str
    services_included: List[str]
    price_from: Optional[int]
    duration: Optional[str]
    features: List[BilingualField]
    popular: bool
    cta_label: Optional[BilingualField]
    order: int
    status: str
    created_at: str
    updated_at: Optional[str]

@router.get("/", response_model=List[PackageResponse])
async def get_packages(db=Depends(get_db)):
    """Get all packages (public endpoint)."""
    cursor = db.cms_packages.find({"status": "published"}).sort("order", 1)
    items = await cursor.to_list(length=50)
    return [{"id": p["id"], **{k: v for k, v in p.items() if k != "_id"}} for p in items]

@router.get("/{package_id}", response_model=PackageResponse)
async def get_package(package_id: str, db=Depends(get_db)):
    """Get single package by ID."""
    doc = await db.cms_packages.find_one({"id": package_id})
    if not doc:
        raise HTTPException(404, "Package not found")
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.post("/", response_model=PackageResponse, dependencies=[Depends(require_role("admin"))])
async def create_package(payload: PackageCreate, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Create new package (admin only)."""
    doc = {
        "id": str(uuid.uuid4()),
        **payload.dict(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": None
    }
    await db.cms_packages.insert_one(doc)
    return {"id": doc["id"], **{k: v for k, v in doc.items() if k != "_id"}}

@router.patch("/{package_id}", response_model=PackageResponse, dependencies=[Depends(require_role("admin"))])
async def update_package(
    package_id: str,
    payload: PackageUpdate,
    db=Depends(get_db),
    _user=Depends(require_role("admin"))
):
    """Update package (admin only)."""
    existing = await db.cms_packages.find_one({"id": package_id})
    if not existing:
        raise HTTPException(404, "Package not found")
    
    update_data = {k: v for k, v in payload.dict(exclude_unset=True).items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.cms_packages.update_one({"id": package_id}, {"$set": update_data})
    
    updated_doc = await db.cms_packages.find_one({"id": package_id})
    return {"id": updated_doc["id"], **{k: v for k, v in updated_doc.items() if k != "_id"}}

@router.delete("/{package_id}", dependencies=[Depends(require_role("admin"))])
async def delete_package(package_id: str, db=Depends(get_db), _user=Depends(require_role("admin"))):
    """Delete package (admin only)."""
    result = await db.cms_packages.delete_one({"id": package_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Package not found")
    return success_response({"deleted": True})
