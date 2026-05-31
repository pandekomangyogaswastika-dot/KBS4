"""
Demo Session Router — manajemen sesi demo sandbox.
Endpoints:
  POST   /api/demo/sessions          buat sesi baru + seed data
  GET    /api/demo/sessions/:id       validate sesi
  DELETE /api/demo/sessions/:id       hapus sesi (cleanup)
  GET    /api/demo/sessions           list sesi aktif (admin only)
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
import os

from core_utils import now_iso
from demos.kn3.core_utils import safe_doc, new_id
from db import get_client as _get_mongo_client  # Shared Motor client dari KBS3
from demo_seed import seed_all

router = APIRouter(prefix="/api/demo")

# Main KBS3 database untuk menyimpan session registry
_db = _get_mongo_client()[os.environ.get("DB_NAME", "test_database")]

DEMO_SESSION_TTL_MINUTES = 90  # Session hidup 90 menit


class DemoSessionRequest(BaseModel):
    name: str
    email: str
    company: str = ""
    app_slug: str = "kn3"  # identifikasi demo app


def _short_id(session_id: str) -> str:
    """Ambil 16 char pertama UUID tanpa dash untuk nama DB."""
    return session_id.replace("-", "")[:16]


async def _get_demo_db(session_id: str):
    """Get Motor database object untuk session tertentu."""
    short_id = _short_id(session_id)
    return client[f"demo_kn3_{short_id}"]


async def get_active_session(session_id: str) -> Dict[str, Any]:
    """Validate session dan return session doc. Raise 404 jika expired/tidak ada."""
    session = safe_doc(
        await _db.demo_sessions.find_one({"id": session_id}, {"_id": 0})
    )
    if not session:
        raise HTTPException(status_code=404, detail="Demo session tidak ditemukan")
    expires_at = datetime.fromisoformat(session["expires_at"])
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(
            status_code=410,
            detail="Demo session sudah expired. Silakan mulai sesi baru."
        )
    return session


@router.post("/sessions", status_code=201)
async def create_demo_session(payload: DemoSessionRequest) -> Dict[str, Any]:
    """
    Buat demo session baru:
    1. Simpan gate form data ke crm_leads (lead generation)
    2. Buat session record di demo_sessions
    3. Seed data generic WMS ke isolated DB
    Return session token + redirect info
    """
    session_id = new_id("demo")
    now = now_iso()
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=DEMO_SESSION_TTL_MINUTES)).isoformat()
    short_id = _short_id(session_id)

    # 1. Simpan sebagai lead (lead generation dari demo gate)
    lead_id = new_id("lead")
    await _db.crm_leads.insert_one({
        "id": lead_id,
        "name": payload.name,
        "email": payload.email,
        "company": payload.company,
        "message": f"Demo request: {payload.app_slug} — via demo gate form",
        "source": "demo_gate",
        "demo_app": payload.app_slug,
        "status": "new",
        "created_at": now,
    })

    # 2. Buat session record
    session_doc = {
        "id": session_id,
        "short_id": short_id,
        "lead_id": lead_id,
        "name": payload.name,
        "email": payload.email,
        "company": payload.company,
        "app_slug": payload.app_slug,
        "db_name": f"demo_kn3_{short_id}",
        "expires_at": expires_at,
        "created_at": now,
        "seeded": False,
    }
    await _db.demo_sessions.insert_one(session_doc)

    # 3. Seed demo data ke isolated DB
    demo_db = _get_mongo_client()[f"demo_kn3_{short_id}"]
    seed_summary = await seed_all(demo_db)

    # Update session: seeded = True
    await _db.demo_sessions.update_one(
        {"id": session_id},
        {"$set": {"seeded": True, "seed_summary": seed_summary}}
    )

    return {
        "session_id": session_id,
        "token": session_id,  # token == session_id untuk simplicity
        "expires_at": expires_at,
        "ttl_minutes": DEMO_SESSION_TTL_MINUTES,
        "app_slug": payload.app_slug,
        "demo_url": f"/demo/kn3?session={session_id}",
        "seed_summary": seed_summary,
        "name": payload.name,
    }


@router.get("/sessions/{session_id}")
async def get_demo_session(session_id: str) -> Dict[str, Any]:
    """Validate dan return session info (dipakai frontend untuk cek expired)."""
    session = await get_active_session(session_id)
    # Hitung remaining minutes
    expires_at = datetime.fromisoformat(session["expires_at"])
    remaining_seconds = (expires_at - datetime.now(timezone.utc)).total_seconds()
    return {
        **session,
        "remaining_minutes": max(0, int(remaining_seconds / 60)),
        "remaining_seconds": max(0, int(remaining_seconds)),
    }


@router.delete("/sessions/{session_id}")
async def delete_demo_session(session_id: str) -> Dict[str, Any]:
    """Hapus session dan drop isolated DB (cleanup)."""
    session = safe_doc(
        await _db.demo_sessions.find_one({"id": session_id}, {"_id": 0})
    )
    if session:
        # Drop isolated demo database
        short_id = _short_id(session_id)
        demo_db_name = f"demo_kn3_{short_id}"
        await _get_mongo_client().drop_database(demo_db_name)
        await _db.demo_sessions.delete_one({"id": session_id})
    return {"deleted": True, "session_id": session_id}


@router.get("/sessions")
async def list_demo_sessions() -> Dict[str, Any]:
    """List semua active sessions (untuk admin monitoring)."""
    now = datetime.now(timezone.utc).isoformat()
    sessions = await _db.demo_sessions.find(
        {"expires_at": {"$gt": now}},
        {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    return {
        "active_count": len(sessions),
        "sessions": [safe_doc(s) for s in sessions]
    }
