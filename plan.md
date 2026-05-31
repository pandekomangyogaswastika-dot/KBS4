# plan.md — Kubus Teknologi Indonesia Platform

## 1) Objectives
- Deliver an **award‑grade, space‑themed immersive** marketing site + a scalable **multi‑role platform**:
  - Advanced CMS + Media Library (admin/staff)
  - Assessment module (token-based, template-driven)
  - **Client Portal + Staff/Admin Portal extensions + Project Management (Phase 5–6)**
  - **AI advisor/assistant (Claude) grounded to KTI content (public + portal) + conversation logs (Phase 7)**
  - **Phase 9: E‑sign + audit trail untuk approvals (mandatory, auditable, RBAC-safe)**
  - **Phase 10: Analytics dashboard (lead funnel + portal usage) for admin/staff**
  - **Phase 11: AI Smart SEO Optimization (Claude) untuk seluruh halaman public**
    - **11.A Basic SEO Foundation** (meta/OG/Schema/sitemap/robots)
    - **11.B AI‑Powered SEO** (Claude: meta generator, analyzer/scoring, keywords, alt text)
    - **11.C SEO Dashboard Admin** (monitoring + bulk actions)
    - **11.D SEO Visual Enhancements** (SERP/OG previews, score trends, AI panel, PDF export)
  - **Phase 12 (Tier 1): Email Notifications (mock-first) + admin-configurable integrations (multi-integrasi)**
  - **Phase 13 (Tier 1): Performance Optimization (SEO + UX)**
  - **Phase 14 (Tier 1): Advanced Search (global search for usability)**
  - **Phase 15 (Tier 2): Real-time Notifications via WebSocket (toast + bell + persisted)**
  - **Phase 16 (Tier 2): Demo Sandbox Engine — Web Product Simulation/Prototype**
    - Studi kasus menampilkan **demo mini-app** yang bisa dicoba user
    - **Guided Tour** (walkthrough + hotspot) terintegrasi dalam demo
    - **Full sandbox** (create/edit/delete) dalam **session terisolasi**
    - **Gated demo** (nama+email) + **lead capture CTA** setelah demo
    - Konten demo dapat **dikonfigurasi admin** (routing/link, enable/disable, label)

- Build on the existing **governance foundation** (KTI_00–13, ENTITY_REGISTRY, scripts) to keep SSOT clear and prevent duplication/conflicts.
- Follow: **Test core in isolation → fix until works → build app → test incrementally**.

- Maintain production-readiness guardrails:
  - RBAC correctness, secure-by-default APIs (KTI_03/KTI_05)
  - Database SSOT + bilingual schema discipline (KTI_04, TD-002)
  - Performance + reduced-motion fallbacks for public UI (KTI_11)
  - Portal usability: projects/timeline/docs/approvals/invoices/messages must work end-to-end
  - AI safety + grounding + logging: refusal on out-of-scope, no cross-tenant leaks, auditable logs
  - Approval governance: approval decision + signature must be **append-only** (audit trail) and verifiable (certificate hash + PDF certificate)
  - **SEO governance:** no duplicate/contradicting metadata; canonical URLs; sitemap/robots consistent; prevent indexation of private portal routes; keep AI SEO outputs auditable.
  - **Integration governance (mandatory):**
    - **No hardcoded API keys / endpoints / DB name** in code.
    - All 3rd-party integrations must be **configurable via admin settings** (provider selection + credentials + enable/disable).
    - Support **mock providers** for development/testing without external accounts.

**Current status (overall):** Platform delivered through **Phase 15** ✅ ALL PHASES COMPLETE.
- ✅ Phase 9–15 selesai semuanya.
- ✅ **Phase 15: Real-time Notifications via WebSocket — COMPLETE** (2026-05-31)
  - Scope delivered: Toast + Bell + persisted MongoDB + multi-portal (admin/staff/client) + live updates
  - Triggers: lead.created, project.created/status_changed/assigned, approval.requested/signed, invoice.created/status_changed, document.uploaded, chat.message
  - Testing: Backend 93% (1 minor: GET /api/leads returns 405 by design), Frontend 100%, Overall 96%

**Next major work:** **Phase 16 Demo Sandbox Engine** (pilot: **KN3 Smart WMS**).

---

## 2) Implementation Steps (Phased)

### Phase 0 — Foundation ✅ DONE
**User stories**
1. As a maintainer, I want SSOT collections documented so I don’t create duplicates.
2. As a maintainer, I want STOP&ASK gates so risky changes require confirmation.
3. As a maintainer, I want automated compliance checks so regressions are caught early.
4. As a maintainer, I want a navigation SSOT so routes don’t drift.
5. As a maintainer, I want a memory layer so context survives across sessions.

**Steps**
- Completed: `/app/docs/KTI_00–13`, `/app/ENTITY_REGISTRY.md`, `/app/memory/*`, `/app/scripts/*`, `/app/plan.md`.

---

### Phase 1 — Core POC (Isolation) ✅ COMPLETE
**Core (hardest / failure‑prone):** (A) Claude integration + (B) Immersive 3D+scroll stack viability.

**Result (verified):**
- (A) Claude POC `/app/scripts/poc_claude.py` → 3/3 PASS (grounded answer, multi-turn CTA, out-of-scope guardrail). Model `anthropic/claude-sonnet-4-6` via `EMERGENT_LLM_KEY`.
- (B) Immersive POC `/poc` → renders hex-crystal + starfield, GSAP ScrollTrigger reveals + camera dolly, 0 page errors. Reduced-motion fallback verified.
- KEY DECISION TD-007: visual-edits babel plugin breaks R3F → use imperative Three.js (`lib/spaceScene.js`).

---

### Phase 2 — V1 Public Immersive Website (MVP) ✅ DONE
**Outcome:** bilingual public site, content endpoints, leads, AI advisor; replaced by cinematic redesign in Phase 2.5.

---

## PHASE 2.5 — COMPRO CINEMATIC REDESIGN (V2) ✅ COMPLETED
Fokus: public website (compro) sinematik (scroll-driven).
- Hero = scroll-scrubbed video + Kubus Core (imperative Three.js)
- Sticky services, HUD gauges, horizontal cases rail, secure transmission demo, engagement tiers
- Bilingual ID/EN, mobile + reduced-motion fallback
- testing_agent_v3: 29/29 PASS; compliance 16/0/0

---

### Phase 3 — Auth + RBAC + Advanced CMS + Media Library (Admin) ✅ SELESAI
**Outcome:**
- JWT access+refresh, RBAC admin/staff/client (no self-register)
- Admin panel `/portal/admin/*`
- Media Library local-first (TD-008) + Range support
- Advanced CMS schema-driven CRUD untuk semua `cms_*` + `cms_home_blocks` + settings
- Public content filter `status=published`
- testing_agent_v3: backend 97.8% / frontend 100%; compliance 16/0/0

---

### Phase 4 — Assessment Module (template-driven, CMS-managed) ✅ SELESAI
**Outcome:**
- Template bilingual “IT Solution Discovery” (8 domain, ~28 Q) + branching
- Public token-based `/assessment/:token` (autosave, attachments via TD-008, submit lock)
- Admin `/portal/admin/assessments` (create link/list/stats/acknowledge/delete) + PDF export (reportlab)
- testing_agent_v3: backend 100% (71/71), frontend ~98%; compliance 16/0/0

---

### Phase 5 + Phase 6 (MERGED) — Client Portal + Staff/Admin Extensions + Project Management ✅ COMPLETE
> Decision: Phase 5 (Client Portal) dan Phase 6 (Staff + Project Management) dikerjakan bersamaan karena entity dan flow saling terkait.

#### 5/6.1 Scope — Navigation (KTI_09)
**Client (role: client)**
- `/portal/dashboard` — ringkasan project
- `/portal/projects` — daftar project
- `/portal/projects/:id` — detail project + timeline/milestones + dokumen + approvals
- `/portal/invoices` — invoice & status bayar
- `/portal/messages` — chat thread dengan tim
- `/portal/assistant` — AI assistant

**Staff/Admin (role: staff | admin)**
- `/portal/admin` — dashboard
- `/portal/admin/projects` — project management
- `/portal/admin/messages` — komunikasi dengan klien
- `/portal/admin/clients` — daftar klien
- `/portal/admin/analytics` — analytics dashboard (Phase 10)
- `/portal/admin/seo` — SEO dashboard (Phase 11)
- `/portal/admin/settings/integrations` — integrations settings (Phase 12)
- `/portal/admin/settings/email-outbox` — email outbox viewer (Phase 12)

> Note: `docs/KTI_09_NAVIGATION_MAP.md` harus merefleksikan rute final di atas.

#### 5/6.2 Collections (SSOT — ENTITY_REGISTRY)
Added collections (Phase 5–6):
- `pm_projects`, `pm_milestones`, `pm_documents`, `pm_approvals`
- `billing_invoices`
- `chat_threads`, `chat_messages`

#### 5/6.3 Backend — API design (prefix `/api`, follow KTI_05)
Implemented routers:
- `routers/projects.py` (pm_*)
- `routers/billing.py` (billing_invoices)
- `routers/chat.py` (chat_threads, chat_messages)

#### 5/6.4 Seeding & Demo Data
- `seed_pm.py` idempotent: projects, milestones, docs, approvals, invoices, chat.

#### 5/6.5 Frontend — Portal UI build
- Client UI lengkap (dashboard/projects/detail/invoices/messages/assistant)
- Admin/staff UI lengkap (projects/messages/clients/analytics/seo)

#### 5/6.6 Security & RBAC (KTI_03)
- Enforced role gates via ProtectedRoute + backend require_role.

#### 5/6.7 Testing & Governance
- Backend: 93/93 tests passed (100%)
- Frontend: key workflows verified (~95%)

---

### Phase 7 — AI Discussion (Claude) public + portal (grounded) ✅ COMPLETE
**Implemented:**
- Backend: `/api/ai/advisor`, `/api/ai/portal`, admin logs
- Frontend: Public widget + portal assistant + admin AI conversation logs

---

### Phase 9 — E‑Sign + Audit Trail untuk Approvals ✅ COMPLETE
**Goal:** approvals keputusan dapat ditandatangani secara digital, disertai audit trail append-only dan PDF certificate.

**Backend (implemented):**
- Indexes: `approval_signatures`, `approval_audit_logs` (created at startup)
- PDF generator: `backend/approval_cert.py` (reportlab)
- Endpoints (routers/projects.py):
  - `POST /api/projects/{project_id}/approvals/{approval_id}/sign`
  - `GET /api/projects/{project_id}/approvals/{approval_id}/signatures`
  - `GET /api/projects/{project_id}/approvals/{approval_id}/history`
  - `GET /api/projects/{project_id}/approvals/{approval_id}/certificate`

**Frontend (implemented):**
- `SignatureModal` (typed + drawn canvas)
- ClientProjectDetail: sign button + certificate download
- AdminProjects: signature status + certificate download + audit modal

---

### Phase 10 — Analytics Dashboard (Lead Funnel + Portal Usage) ✅ COMPLETE
**Backend (implemented):**
- `backend/routers/analytics.py` endpoints:
  - `/api/analytics/overview`, `/funnel`, `/leads-trend`, `/ai-trend`, `/revenue-trend`
- RBAC: only admin/staff.

**Frontend (implemented):**
- AdminAnalytics page (recharts)
- Route `/portal/admin/analytics` added
- Menu item `admin.analytics` added

---

## Phase 11 — AI Smart SEO Optimization (Claude) ✅ COMPLETE

### Phase 11.A — Basic SEO Foundation ✅ COMPLETE
- `SEOHead` + react-helmet-async integrated
- OG/Twitter tags + Schema.org JSON-LD
- Backend sitemap.xml + robots.txt endpoints
- All public pages integrated

### Phase 11.B — AI‑Powered SEO (Claude) ✅ COMPLETE
- `/api/seo/ai/generate-meta`, `/ai/analyze`, `/ai/keywords`, `/ai/alt-text`
- Collections: `seo_pages`, `seo_ai_logs`
- RBAC: admin/staff

### Phase 11.C — SEO Dashboard (Admin Portal) ✅ COMPLETE
- `/portal/admin/seo` dashboard (KPI + list/filter + bulk actions + detail modal)

### Phase 11.D — SEO Visual Enhancements ✅ COMPLETE
- Google SERP preview component
- Social OG/Twitter preview component
- Score history chart (recharts)
- Score history persistence:
  - `POST /api/seo/pages/{page_id}/score-snapshot`
  - `GET /api/seo/pages/{page_id}/score-history`
- New collection: `seo_score_history`
- PDF export:
  - `GET /api/seo/report/pdf/{page_id}` (reportlab)

---

## Phase 12 (Tier 1) — Integrations (Admin-configurable) + Email Notifications (Mock-first) ✅ COMPLETED
**Goal:** meningkatkan engagement portal dengan notifikasi email untuk event penting, dengan **kerangka multi-integrasi** yang dapat diatur dari admin settings (tanpa hardcode).

### 12.0 Decisions (confirmed by user)
- **A. Triggers:** gunakan **semua** event (lead, approval request, approval signed, invoice created/due/overdue, project created/assigned)
- **B. Admin settings:** siapkan **semua** kerangka multi-integrasi: **Email + Payment Gateway placeholder + Object Storage placeholder**
- **C. Next:** setelah Phase 12 selesai & testing lulus → **lanjut langsung Phase 13**
- **D. Testing:** pakai **testing_agent_v3** → lulus (lihat `/app/test_reports/iteration_8.json`)

### 12.1 Final result (testing_agent_v3 iteration 8)
- ✅ Backend: 20/20 PASS (100%)
- ✅ Frontend: 95% (semua flow utama lulus, tab Payment/Storage struktur sesuai)
- ✅ 0 hardcoded API keys
- ✅ Secret masking round-trip verified
- ✅ 6 trigger event terkirim ke outbox (lead/project/approval-req/approval-sign/invoice-created/invoice-overdue)
- ✅ 12 template seeded (6 events × 2 locales id/en)

### 12.2 Delivered artifacts
**Backend**
- `email_service.py` (async motor, provider abstraction: Mock + SMTP + placeholders)
- `notifications.py` (recipient discovery + dispatcher)
- `routers/integrations.py` (multi-integration CRUD, masking, test email, outbox, templates)
- `seed_email_templates.py` (idempotent template seed)
- Wired triggers di `routers/leads.py`, `routers/projects.py`, `routers/billing.py`
- Indexes: `integration_settings`, `email_outbox`, `email_events`, `email_templates`, `notification_preferences`

**Frontend**
- `/portal/admin/settings/integrations` (Tabs: Email | Payment | Storage)
- `/portal/admin/settings/email-outbox` (table + filter + pagination + detail dialog)
- Sidebar nav items + bilingual i18n (id/en)

### 12.3 Requirements compliance (mandatory)
- ✅ **No hardcoded** API keys / endpoints / DB name — semua dari `integration_settings` MongoDB
- ✅ Mock provider default → siap deploy tanpa kredensial eksternal
- ✅ Masking secret di response API & input UI
- ✅ Round-trip safe (kirim `********` tidak menimpa nilai asli)

---

## Phase 13 (Tier 1) — Performance Optimization (SEO + UX) ✅ COMPLETED
**Goal:** mempercepat public site dan backend tanpa merusak cinematic visuals atau behavior existing.

### 13.0 Final result (testing_agent_v3 iteration 9)
- ✅ Backend (Phase 13 features): **7/7 = 100% PASS**
- ✅ Backend regression: **23/27 = 85%** (4 "failures" adalah issue di skrip test pakai path salah — bukan bug aplikasi)
- ✅ Frontend: **100% PASS** — homepage, services, cases, blog, admin portal semua render
- ✅ **Zero regression** untuk Phase 9-12

### 13.1 Delivered — Backend Performance
- **In-memory TTL cache** (`backend/cache.py`): asyncio-safe dict-based, namespace + per-key invalidation, deepcopy on store to prevent caller mutation, stats counters
- **Public content caching** (`routers/content.py`): all 12 public read endpoints cached 60s + `Cache-Control: public, max-age=60, stale-while-revalidate=30`
- **Cache invalidation** wired in `routers/cms.py`
- **GZipMiddleware** at minimum_size=1024
- **Admin observability**:
  - `GET /api/admin/cache/stats`
  - `POST /api/admin/cache/flush`

### 13.2 Delivered — MongoDB Indexes
- Compound indexes on `cms_*` collections for `(status, order)` and `(status, created_at -1)`
- `crm_leads` status index
- Bilingual text indexes on `cms_services` / `cms_cases` / `cms_blog` / `cms_careers`

### 13.3 Delivered — Frontend Performance
- LCP image priorities and `decoding="async"` on below-the-fold images
- Admin pages already use `React.lazy` route splitting

---

## Phase 14 (Tier 1) — Advanced Search (Global, RBAC-safe) ✅ COMPLETED
**Goal:** menyatukan pencarian seluruh konten (CMS + Portal) dalam satu UX, dengan RBAC ketat.

### 14.0 Final result (testing_agent_v3 iteration 10)
- ✅ Backend: **20/20 PASS (100%)**
- ✅ Frontend: **100%**

### 14.1 Delivered — Backend
- `routers/search.py` public + portal search endpoints
- MongoDB `$text` primary + regex fallback
- RBAC strict scoping
- Public search cached 30s

### 14.2 Delivered — Frontend
- `components/GlobalSearch.jsx` command palette
- Integrated in public navbar + admin/client headers
- i18n `search.*`

---

## Phase 15 (Tier 2) — Real-time Notifications WebSocket ✅ COMPLETED
**Goal:** meningkatkan UX portal dengan notifikasi real-time (bell + toast) yang persisted.

**Delivered:**
- WebSocket `/api/ws/notifications?token=...`
- REST CRUD notifications
- Triggers across lead/project/approval/invoice/document/chat

**Testing (iteration_11):** Backend 93% (1 by design), Frontend 100%.

---

## Phase 16 (Tier 2) — Demo Sandbox Engine (Web Product Simulation/Prototype) 🟡 PLANNED

### Phase 16.0 Scope (confirmed)
- **Type:** Sandboxed Mini‑App (fully functional, limited scope) + Guided Tour
- **Interaction:** Full sandbox (create/edit/delete) dalam session terisolasi
- **Content:** Admin‑configurable via CMS (enable, label, route/link)
- **Lead gen:**
  - **Gated demo** (nama + email) sebelum akses
  - **Lead capture CTA** setelah user mencoba demo
- **Pilot demo:** KN3 (Smart WMS)
- **Demo role:** Admin (full access)
- **Demo data:** dibuat **generic** (hindari nama/identitas PT. Kain Nusantara)
- **Language:** Indonesian only (v1)
- **Architecture:** Copy KN3 code into KBS3, lalu adapt:
  - auth → demo session token (bukan login)
  - API prefix → /api/demo/wms/*
  - MongoDB session isolation → per-session namespace + TTL cleanup

### Phase 16A — Demo Session Engine (Backend Infra)
**Goal:** membuat engine session demo yang aman, terisolasi, dan auto-clean.

**User stories**
1. Sebagai visitor, saya bisa mengakses demo setelah mengisi nama+email.
2. Sebagai sistem, demo data harus terisolasi per session agar visitor tidak saling mengganggu.
3. Sebagai sistem, demo harus auto-expire agar database tidak menumpuk.

**Steps**
- Data model (SSOT): `demo_sessions`:
  - `id`, `case_slug`, `demo_key` (mis: `kn3_wms`), `created_at`, `expires_at`, `status`
  - `lead_id` (optional), `ip_hash` (optional), `ua_hash` (optional)
  - Index TTL di `expires_at`
- Endpoint inti:
  - `POST /api/demo/sessions` (anonymous): create session + (optional) create lead
  - `GET /api/demo/sessions/{id}`: validate active
  - `POST /api/demo/sessions/{id}/renew` (optional): extend TTL (rate-limited)
- Namespace isolation:
  - Semua query KN3 router membaca `X-Demo-Session: <id>` dan menggunakan collection prefix `demo_<id>__<collection>` atau `demo_db.get_collection(name)` wrapper.
- Seeding:
  - Port `seed_realistic.py` logic dan ubah jadi **generic seed** (nama perusahaan, warehouse, customers, products) via parameter.

**Security**
- Session ID random UUIDv4 (unpredictable)
- Rate limit create session per IP
- No admin JWT needed (demo uses session token)

### Phase 16B — KN3 Backend Router Mounting (API prefix + session aware)
**Goal:** copy router KN3 tapi tidak bentrok dengan KBS3 `/api/*`.

**Steps**
- Mount KN3 routers di prefix khusus: `/api/demo/wms/*`
- Adapt dependencies:
  - Replace `get_db()` calls dengan `get_demo_db(session_id)` wrapper
  - Ensure all writes go to namespaced collections
- Add "demo admin" identity (virtual user) untuk audit fields:
  - `actor_id="demo_admin"`, `actor_role="admin"`

### Phase 16C — KN3 Frontend Integration (React, code-splitting)
**Goal:** demo tidak membebani initial load public site.

**Steps**
- Copy KN3 frontend ke folder baru:
  - `frontend/src/demos/kn3/*`
- Implement entrypoint `KN3DemoApp`:
  - Read `session` dari query param
  - Setup axios base URL to KBS3 backend
  - Add header `X-Demo-Session`
  - Replace login screen dengan `DemoSessionGuard`
- Code splitting:
  - Routing demo via `React.lazy(() => import('@/demos/kn3/KN3DemoApp'))`
  - Demo assets only load when user enters `/demo/kn3`
- Guided Tour:
  - Reuse `tourDefinitions.js` dari KN3
  - Auto-start tour ketika demo pertama kali dibuka
- Bahasa:
  - Indonesian only (no i18n work in v1 demo)

### Phase 16D — KBS3 Case Study Integration (Gating + Admin Config)
**Goal:** admin bisa mengaktifkan demo per studi kasus + mengatur routing/link.

**Steps**
- Extend `cms_cases` schema:
  - `demo_enabled: bool`
  - `demo_route: string` (mis. `/demo/kn3` atau `/demo/wms`)
  - `demo_label: string` (button label)
  - `demo_timeout_minutes: number`
  - `demo_key: string` (maps to backend demo implementation)
- Update Admin CMS UI:
  - form fields untuk demo
  - validation: route must start with `/demo/`
- Public CaseDetailPage:
  - If `demo_enabled` show button “Coba Demo”
  - Click → open GateForm (nama+email)
  - On submit → `POST /api/demo/sessions` → redirect ke `demo_route?session=<id>`

### Phase 16E — Polish (Lead capture + UX)
- Lead capture banner/modal setelah:
  - (A) 2 menit in-demo, atau
  - (B) user menyelesaikan guided tour
- CTA: “Minta konsultasi / Minta proposal”
- Optional: add analytics event tracking (Phase 10 pipeline)

### Phase 16 Testing (mandatory)
- Backend:
  - Create demo session → TTL created
  - Namespaced write/read works
  - Expired session returns 410/401
- Frontend:
  - Gated access flow works
  - Demo loads via lazy route only
  - Guided tour runs
- Regression: public pages + portals unaffected

---

## 3) Next Actions (Immediate)
**Tier 1 COMPLETE** ✅ **Tier 2 Phase 15 COMPLETE** ✅
1. ✅ Phase 12: Integrations Settings + Email Notifications (DONE — iteration_8 PASS)
2. ✅ Phase 13: Performance Optimization (DONE — iteration_9 PASS)
3. ✅ Phase 14: Advanced Search (DONE — iteration_10 100% PASS)
4. ✅ Phase 15: Real-time Notifications WebSocket (DONE — iteration_11 96% PASS, 100% frontend)

**Next build target:**
5. 🟡 **Phase 16 (Pilot): Demo Sandbox Engine for KN3 Smart WMS**

**Tier 2 remaining (after Phase 16 — menunggu konfirmasi user):**
- Dark/Light theme toggle (ambient + persistent user preference)
- Multi-tenant support / Custom branding per-client (sub-domain whitelabel)
- Advanced analytics (funnels/cohort/retention)
- Mobile PWA
- Payment gateway aktivasi (Midtrans/Xendit) — skema config sudah disiapkan di Phase 12
- Optional: object storage migration ke S3/R2 (config sudah disiapkan di Phase 12)

**SSOT docs to update (mandatory)**
- Update `ENTITY_REGISTRY.md`:
  - add `demo_sessions` (+ possible `demo_events` if tracking interactions)
  - ensure `notification_preferences`, `integration_settings`, `email_outbox`, `email_events`, `email_templates`
- Update `docs/KTI_09_NAVIGATION_MAP.md`:
  - include `/demo/*` routes
  - include admin CMS demo fields location

**Catatan dependency / environment:**
- Container Node.js = `20.20.2`.
- Hindari package frontend yang butuh Node >=22.
- Semua API integration config harus lewat admin settings (no hardcode).

---

## 4) Success Criteria
- Governance: compliance scripts pass (0 FAIL) at phase ends; SSOT maintained.
- Public: cinematic experience remains stable, reduced-motion supported.
- Admin: CMS/Media/Assessment/PM remain stable, RBAC correct.
- Portal (Phase 5–6): client+staff workflows usable end-to-end with strict scoping.
- Phase 7: AI groundedness + RBAC-safe portal context; logs available.
- Phase 9: approvals e-sign + audit trail verifiable; certificate PDF downloadable; strict RBAC.
- Phase 10: analytics visible for admin/staff; charts stable; client blocked.
- Phase 11: SEO foundation + AI automation + dashboard + visual enhancements + PDF exports all RBAC-safe.
- Phase 12: integrations framework + email notifications (mock) end-to-end.
- Phase 13: measurable performance improvements without breaking visuals.
- Phase 14: global search works with correct RBAC scoping; no data leakage.
- Phase 15: real-time notifications stable (WS + REST + persisted).
- **Phase 16 (Demo Sandbox Engine):**
  - User dapat membuka demo dari studi kasus dengan gating name+email
  - Demo **tidak membebani initial load** (lazy route + code splitting)
  - Session sandbox **terisolasi** (create/edit/delete aman)
  - Session auto-expire (TTL) dan tidak menumpuk DB
  - Admin bisa mengaktifkan/menonaktifkan demo per studi kasus dan mengatur route/link
  - Guided tour berjalan dan membantu user menyelesaikan flow demo
  - Lead capture CTA muncul dan leads tercatat
- Every phase ends with `testing_agent_v3` and all reported bugs fixed (or explicitly accepted as tech debt).
