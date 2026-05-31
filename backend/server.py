import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()

from core_utils import success_response  # noqa: E402
from db import get_db  # noqa: E402
from routers import admin as admin_router  # noqa: E402
from routers import admin_users as admin_users_router  # noqa: E402
from routers import ai as ai_router  # noqa: E402
from routers import assessment as assessment_router  # noqa: E402
from routers import auth as auth_router  # noqa: E402
from routers import cms as cms_router  # noqa: E402
from routers import content as content_router  # noqa: E402
from routers import leads as leads_router  # noqa: E402
from routers import media as media_router  # noqa: E402
from seed_assessment import seed_assessment  # noqa: E402
from seed_data import seed_all  # noqa: E402
from seed_users import seed_users  # noqa: E402
from seed_pm import seed_pm  # noqa: E402
from routers import projects as projects_router  # noqa: E402
from routers import billing as billing_router  # noqa: E402
from routers import chat as chat_router  # noqa: E402
from routers import analytics as analytics_router  # noqa: E402
from routers import seo as seo_router  # noqa: E402
from routers import seo_ai as seo_ai_router  # noqa: E402
from routers import integrations as integrations_router  # noqa: E402
from routers import search as search_router  # noqa: E402
from routers import notifications as notifications_router  # noqa: E402
from routers import demo as demo_router  # noqa: E402
from demo_context import set_kn3_demo_db, reset_kn3_demo_db  # noqa: E402
from db import get_client as mongo_client  # noqa: E402
import re as _re  # noqa: E402

# Demo KN3 routers
from demos.kn3.routers import auth as kn3_auth_router  # noqa: E402
from demos.kn3.routers import dashboard as kn3_dashboard_router  # noqa: E402
from demos.kn3.routers import products as kn3_products_router  # noqa: E402
from demos.kn3.routers import inventory as kn3_inventory_router  # noqa: E402
from demos.kn3.routers import warehouses as kn3_warehouses_router  # noqa: E402
from demos.kn3.routers import customers as kn3_customers_router  # noqa: E402
from demos.kn3.routers import sales_orders as kn3_sales_orders_router  # noqa: E402
from demos.kn3.routers import uoms as kn3_uoms_router  # noqa: E402
from demos.kn3.routers import wms as kn3_wms_router  # noqa: E402
from demos.kn3.routers import inbound_receiving as kn3_inbound_router  # noqa: E402
from demos.kn3.routers import outbound_picking as kn3_outbound_router  # noqa: E402
from seed_email_templates import seed_email_templates  # noqa: E402
from security import require_role  # noqa: E402
from cache import cache_stats, clear_all  # noqa: E402
from fastapi import Depends  # noqa: E402

app = FastAPI(title="Kubus Teknologi Indonesia API")

# Phase 13: compress responses > 1KB for major bandwidth + LCP savings
app.add_middleware(GZipMiddleware, minimum_size=1024, compresslevel=6)

_origins = os.environ.get("CORS_ORIGINS", "*")
allow_origins = ["*"] if _origins.strip() == "*" else [o.strip() for o in _origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Demo Context Middleware -------------------------------------------------
# Set MongoDB database context untuk setiap request ke /api/demo/kn3/*
_DEMO_KN3_PATH_RE = _re.compile(r"^/api/demo/kn3/")

@app.middleware("http")
async def demo_kn3_context_middleware(request: Request, call_next):
    """
    Untuk setiap request ke /api/demo/kn3/*, ambil session_id dari
    Authorization header, validasi, dan set demo DB context.
    """
    if _DEMO_KN3_PATH_RE.match(str(request.url.path)):
        auth_header = request.headers.get("Authorization", "")
        session_id = None
        if auth_header.startswith("Bearer "):
            session_id = auth_header.replace("Bearer ", "").strip()

        if session_id and session_id != "demo-token":
            try:
                from datetime import datetime, timezone as _tz
                from demos.kn3.core_utils import safe_doc as _safe_doc
                db_name = os.environ.get("DB_NAME", "test_database")
                kbs3_db = mongo_client()[db_name]
                session = _safe_doc(
                    await kbs3_db.demo_sessions.find_one({"id": session_id}, {"_id": 0})
                )
                if session:
                    short_id = session_id.replace("-", "")[:16]
                    demo_db = mongo_client()[f"demo_kn3_{short_id}"]
                    token = set_kn3_demo_db(demo_db)
                    try:
                        response = await call_next(request)
                    finally:
                        reset_kn3_demo_db(token)
                    return response
            except Exception:
                pass
        # No valid session — still allow auth/login endpoint to pass through
        if "/auth/login" in str(request.url.path) or "/auth/me" in str(request.url.path):
            return await call_next(request)
        # For other demo routes without valid session, still try (will fail at db access)
        return await call_next(request)

    return await call_next(request)


# --- Consistent error envelope (KTI_05) ------------------------------------
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    if isinstance(detail, dict) and "code" in detail:
        error = {"code": detail.get("code"), "message": detail.get("message", ""), "details": detail.get("details", [])}
    else:
        error = {"code": "ERROR", "message": str(detail), "details": []}
    return JSONResponse(status_code=exc.status_code, content={"success": False, "error": error})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [{"loc": list(e.get("loc", [])), "msg": e.get("msg", ""), "type": e.get("type", "")} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Validasi gagal", "details": details}},
    )


# --- Routers ----------------------------------------------------------------
app.include_router(auth_router.router)
app.include_router(admin_users_router.router)
app.include_router(admin_router.router)
app.include_router(cms_router.router)
app.include_router(assessment_router.router)
app.include_router(media_router.router)
app.include_router(media_router.public_router)
app.include_router(content_router.router)
app.include_router(leads_router.router)
app.include_router(ai_router.router)
app.include_router(projects_router.router)
app.include_router(billing_router.router)
app.include_router(chat_router.router)
app.include_router(analytics_router.router)
app.include_router(seo_router.router, prefix="/api/seo", tags=["SEO"])
app.include_router(seo_ai_router.router, prefix="/api/seo", tags=["SEO AI"])
app.include_router(integrations_router.router)
app.include_router(search_router.router)
app.include_router(notifications_router.router)
app.include_router(demo_router.router)

# --- Demo KN3 Routers -------------------------------------------------------
app.include_router(kn3_auth_router.router)
app.include_router(kn3_dashboard_router.router)
app.include_router(kn3_products_router.router)
app.include_router(kn3_inventory_router.router)
app.include_router(kn3_warehouses_router.router)
app.include_router(kn3_customers_router.router)
app.include_router(kn3_sales_orders_router.router)
app.include_router(kn3_uoms_router.router)
app.include_router(kn3_wms_router.router)
app.include_router(kn3_inbound_router.router)
app.include_router(kn3_outbound_router.router)


@app.get("/api/")
async def root():
    return success_response({"service": "kti-api", "status": "ok"})


@app.get("/api/health")
async def health():
    return success_response({"status": "healthy"})


@app.get("/api/admin/cache/stats")
async def admin_cache_stats(_user=Depends(require_role("admin"))):
    """Admin-only: lightweight observability for the in-process cache (Phase 13)."""
    return success_response(cache_stats())


@app.post("/api/admin/cache/flush")
async def admin_cache_flush(_user=Depends(require_role("admin"))):
    """Admin-only: manual flush of the public content cache."""
    clear_all()
    return success_response({"flushed": True})


@app.on_event("startup")
async def on_startup():
    db = get_db()
    await db.cms_services.create_index("slug", unique=True)
    await db.cms_cases.create_index("slug", unique=True)
    await db.cms_blog.create_index("slug", unique=True)
    await db.cms_careers.create_index("slug", unique=True)
    await db.crm_leads.create_index([("created_at", -1)])
    await db.ai_conversations.create_index("session_id", unique=True)
    await db.system_users.create_index("email", unique=True)
    await db.media_assets.create_index([("created_at", -1)])
    await db.media_assets.create_index("kind")
    await db.media_assets.create_index("folder_id")
    await db.media_usage.create_index("asset_id")
    await db.cms_home_blocks.create_index("key", unique=True)
    await db.assessment_sessions.create_index("token", unique=True)
    await db.assessment_sessions.create_index([("created_at", -1)])
    await db.assessment_answers.create_index([("session_id", 1), ("question_id", 1)], unique=True)
    await db.assessment_attachments.create_index("session_id")
    # PM indexes
    await db.pm_projects.create_index([("created_at", -1)])
    await db.pm_projects.create_index("client_id")
    await db.pm_projects.create_index("staff_ids")
    await db.pm_milestones.create_index([("project_id", 1), ("order", 1)])
    await db.pm_documents.create_index("project_id")
    await db.pm_approvals.create_index([("project_id", 1), ("created_at", -1)])
    await db.billing_invoices.create_index([("created_at", -1)])
    await db.billing_invoices.create_index("client_id")
    await db.chat_threads.create_index([("last_message_at", -1)])
    await db.chat_threads.create_index("client_id")
    await db.chat_messages.create_index([("thread_id", 1), ("created_at", 1)])
    # AI conversations indexes
    await db.ai_conversations.create_index([("updated_at", -1)])
    await db.ai_conversations.create_index("user_id")
    await db.ai_conversations.create_index("surface")
    # Phase 9 - E-sign & audit indexes
    await db.approval_signatures.create_index("approval_id")
    await db.approval_signatures.create_index("signer_id")
    await db.approval_audit_logs.create_index([("approval_id", 1), ("timestamp", 1)])
    await db.approval_audit_logs.create_index("project_id")
    # Phase 12 - Integrations + Email Notifications
    await db.integration_settings.create_index("type", unique=True)
    await db.email_outbox.create_index([("created_at", -1)])
    await db.email_outbox.create_index("status")
    await db.email_outbox.create_index("template_id")
    await db.email_events.create_index([("outbox_id", 1), ("timestamp", 1)])
    await db.email_templates.create_index([("template_id", 1), ("locale", 1)], unique=True)
    await db.notification_preferences.create_index("user_id", unique=True)
    # Phase 13 - Performance indexes
    # Speed up the most common public read patterns: status+order, status+created_at
    for col in ("cms_services", "cms_cases", "cms_tech", "cms_team", "cms_clients",
                "cms_blog", "cms_careers", "cms_home_blocks"):
        await db[col].create_index([("status", 1), ("order", 1)])
        await db[col].create_index([("status", 1), ("created_at", -1)])
    # Lead status filter + search uses regex on name/email/company; index name/email/company
    await db.crm_leads.create_index("status")
    # Prep for Phase 14 advanced search: bilingual text indexes (best-effort; ignore errors)
    text_targets = [
        ("cms_services", [("title.id", "text"), ("title.en", "text"), ("summary.id", "text"), ("summary.en", "text")]),
        ("cms_cases", [("title.id", "text"), ("title.en", "text"), ("summary.id", "text"), ("summary.en", "text")]),
        ("cms_blog", [("title.id", "text"), ("title.en", "text"), ("body.id", "text"), ("body.en", "text")]),
        ("cms_careers", [("title.id", "text"), ("title.en", "text"), ("summary.id", "text"), ("summary.en", "text")]),
    ]
    for col_name, spec in text_targets:
        try:
            await db[col_name].create_index(spec, default_language="english")
        except Exception as exc:  # noqa: BLE001
            print(f"[startup] text index skip for {col_name}: {exc}")
    # Phase 15 - Notifications (in-app real-time)
    await db.notifications.create_index([("user_id", 1), ("created_at", -1)])
    await db.notifications.create_index([("user_id", 1), ("read", 1)])
    await db.notifications.create_index([("type", 1), ("created_at", -1)])
    await seed_all(db)
    await seed_users(db)
    await seed_assessment(db)
    await seed_pm(db)
    # Seed default email templates (idempotent)
    try:
        created = await seed_email_templates(db)
        if created:
            print(f"[startup] seeded {created} email templates")
    except Exception as exc:  # noqa: BLE001
        print(f"[startup] seed_email_templates failed: {exc}")
