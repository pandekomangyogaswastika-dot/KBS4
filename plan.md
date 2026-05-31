# plan.md — Kubus Teknologi Indonesia Platform

## 1) Objectives
- Deliver an **award‑grade, space‑themed immersive** marketing site (Compro) + a scalable **multi‑role platform**:
  - Advanced CMS + Media Library (admin/staff)
  - Assessment module (token-based, template-driven)
  - Client Portal + Staff/Admin Portal + Project Management (Phase 5–6)
  - AI advisor/assistant grounded to KTI content (public + portal) + conversation logs (Phase 7)
  - Phase 9: E‑sign + audit trail untuk approvals (append-only, auditable, RBAC-safe)
  - Phase 10: Analytics dashboard (lead funnel + portal usage) for admin/staff
  - Phase 11: AI Smart SEO Optimization untuk public pages + SEO dashboard
  - Phase 12: Integrations framework + Email Notifications (mock-first, admin-configurable)
  - Phase 13: Performance Optimization (SEO + UX)
  - Phase 14: Advanced Search (global search, RBAC-safe)
  - Phase 15: Real-time Notifications via WebSocket (toast + bell + persisted)
  - Phase 16: Demo Sandbox Engine — Web Product Simulation/Prototype (pilot: KN3)
  - Phase 17: API Documentation (OpenAPI/Swagger UI) — protected docs + JWT try-out
  - Phase 18: Compro UI/UX Improvements (Public Site Polish)
    - Modernisasi **font heading (H1/H2)** agar lebih modern/enterprise
    - Fix **loading states** (Services/Cases stuck loader) + timeout fallback
    - Improve perceived performance via skeleton loaders
  - **Phase 19: IT Solution Company Content Completion (Trust + Authority)**
    - Trust Triangle: **Testimonials**, **Privacy/Terms**, **FAQ**
    - Authority Stack: **Pricing/Packages**, **About page**, **Resources/Downloads**

- Build on existing governance foundation (KTI_00–13, ENTITY_REGISTRY, scripts) to keep SSOT clear and prevent duplication/conflicts.
- Process discipline: **Test core in isolation → fix until works → build app → test incrementally**.

- Maintain production-readiness guardrails:
  - RBAC correctness, secure-by-default APIs (KTI_03/KTI_05)
  - Database SSOT + bilingual schema discipline (KTI_04, TD-002)
  - Performance + reduced-motion fallbacks for public UI (KTI_11)
  - Portal usability: projects/timeline/docs/approvals/invoices/messages must work E2E
  - AI safety + grounding + logging: refusal on out-of-scope, no cross-tenant leaks, auditable logs
  - Approval governance: signature + audit trail **append-only** and verifiable (certificate hash + PDF certificate)
  - SEO governance: no duplicate/contradicting metadata; canonical URLs; sitemap/robots consistent; prevent indexation private routes; AI SEO outputs auditable
  - Integration governance (mandatory):
    - No hardcoded API keys/endpoints/DB name in code
    - All 3rd-party integrations configurable via admin settings
    - Support mock providers for development/testing

**Current status (overall):** Platform delivered through **Phase 17** ✅, with Phase 18 UI/UX changes implemented and ready for user testing.
- ✅ Phase 0–16 selesai (Phase 16 Demo Sandbox Engine: KN3) + E2E verified.
- ✅ Phase 17 API Documentation (OpenAPI/Swagger UI) — COMPLETE (2026-05-31)
  - `/api/docs`, `/api/redoc`, `/api/openapi.json` protected via **HTTP Basic Auth**
  - JWT Bearer scheme tersedia untuk “Try it out”
  - Tag grouping disediakan
  - Demo KN3 internal endpoints (`/api/demo/kn3/*`) disembunyikan dari schema
- ✅ Phase 18A/18B implemented:
  - Heading font: **Space Grotesk**
  - `useFetch` timeout protection
  - Skeleton loaders for `/services` and `/cases`

**Next major work:** **Phase 19 — Content Completion for IT Solution Company** (Trust Triangle → Authority Stack).

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
**Core (hardest / failure‑prone):** (A) LLM integration + (B) Immersive 3D+scroll stack viability.

**Result (verified):**
- LLM POC passed (grounded, multi-turn, guardrails).
- Immersive POC stable with reduced-motion fallback.

---

### Phase 2 — V1 Public Website ✅ DONE
Outcome delivered, later superseded by cinematic redesign.

---

### Phase 2.5 — Compro Cinematic Redesign (V2) ✅ COMPLETED
- Scroll-driven hero, 3D Kubus Core, sticky services, cases rail, secure transmission, engagement tiers
- Bilingual ID/EN, mobile + reduced-motion fallback

---

### Phase 3 — Auth + RBAC + Advanced CMS + Media Library ✅ COMPLETE

---

### Phase 4 — Assessment Module ✅ COMPLETE

---

### Phase 5 + 6 (Merged) — Portal + Project Management ✅ COMPLETE

---

### Phase 7 — AI Advisor/Assistant ✅ COMPLETE

---

### Phase 9 — E‑Sign + Audit Trail ✅ COMPLETE

---

### Phase 10 — Analytics Dashboard ✅ COMPLETE

---

### Phase 11 — AI Smart SEO ✅ COMPLETE

---

### Phase 12 — Integrations + Email Notifications ✅ COMPLETE

---

### Phase 13 — Performance Optimization ✅ COMPLETE

---

### Phase 14 — Advanced Search ✅ COMPLETE

---

### Phase 15 — Real-time Notifications WebSocket ✅ COMPLETE

---

### Phase 16 — Demo Sandbox Engine (Pilot: KN3 Smart WMS) ✅ COMPLETE
- Case CTA → Gate form lead capture → session created → `/demo/kn3?session=...` lazy loads
- Per-session isolated MongoDB database `demo_kn3_{short_id}`

---

### Phase 17 — API Documentation (OpenAPI/Swagger UI) ✅ COMPLETE
**Scope:** Public API + Portal endpoints (exclude demo KN3 internal)

**Delivered:**
- `/api/docs` Swagger UI (protected Basic Auth)
- `/api/redoc` ReDoc (protected Basic Auth)
- `/api/openapi.json` OpenAPI schema (protected Basic Auth)
- JWT Bearer security scheme available for “Try it out”
- Tags grouping + endpoint filtering for `/api/demo/kn3/*`

---

## Phase 18 — Compro UI/UX Improvements (Public Site Polish) ✅ IMPLEMENTED (Pending User Acceptance)

### Phase 18.0 Scope (confirmed by discussion)
Fokus pada UI/UX public marketing site:
- ✅ Modernisasi font untuk H1 (dan heading lain yang relevan) agar lebih modern
- ✅ Fix masalah **loader** yang berpotensi “stuck” pada halaman Services/Cases
- ✅ Improve perceived performance via skeleton loaders

### Phase 18A — Typography Modernization (H1/H2) ✅ DONE
- Replaced display font to **Space Grotesk**
- Updated `index.css` + Tailwind font config

### Phase 18B — Loading Reliability (Services/Cases) ✅ DONE
- Added request timeout protection in `useFetch` (default 10s)
- Added skeleton loaders for `/services` and `/cases`

### Phase 18 Testing
- **Pending:** User manual testing (desktop + mobile)

---

## Phase 19 — IT Solution Company Content Completion (Trust + Authority) ✅ BACKEND STABILIZED — Awaiting User Review

### Phase 19 Backend Stabilization (2026-05-31) ✅
**Issue resolved:** Phase 19 endpoints (`/api/testimonials`, `/api/faq`, `/api/packages`, `/api/legal`, `/api/resources`) sebelumnya gagal karena:
1. Pydantic `ResponseValidationError` (missing `services_included` field) — RESOLVED
2. Response shape tidak konsisten dengan `apiClient.useFetch` (raw array vs `{success, data}` wrapper) — RESOLVED
3. FastAPI 307 trailing-slash redirect ke `http://` (Mixed Content blocked oleh browser HTTPS) — RESOLVED

**Fixes applied:**
- Refactor semua 5 router Phase 19 (testimonials, faq, packages, legal, resources):
  - Hapus `response_model=...` pada GET list/single endpoints (untuk wrapping fleksibel)
  - Tambahkan helper `_shape()` per router yang fill default `Optional` field secara defensif
  - Wrap semua response dengan `success_response()` untuk format konsisten `{success, data}`
  - Ubah route path dari `"/"` ke `""` (sejalan dengan pattern `content.py`) untuk hindari 307 redirect
- Pydantic `Create`/`Update` models tetap dipakai untuk input validation (admin POST/PATCH)

**Verifikasi (E2E):**
| Endpoint | HTTP | Items | UI Verified |
|---|---|---|---|
| GET /api/testimonials?featured=true | 200 | 4 | ✅ Home carousel |
| GET /api/faq | 200 | 8 | ✅ /faq page (accordions) |
| GET /api/packages | 200 | 3 | ✅ /pricing page (3 tier cards) |
| GET /api/legal | 200 | 2 | ✅ list |
| GET /api/legal/privacy-policy | 200 | 1 | ✅ /privacy-policy page |
| GET /api/resources | 200 | 3 | ✅ /resources page (3 cards) |

**Files modified:**
- `/app/backend/routers/testimonials.py`
- `/app/backend/routers/faq.py`
- `/app/backend/routers/packages.py`
- `/app/backend/routers/legal.py`
- `/app/backend/routers/resources.py`

### Phase 19 Remaining Items (next iterations)
- [ ] i18n: Add Phase 19 translation keys (id/en) di `frontend/src/i18n/`
- [ ] Polish: Fix `tierOrder["starter"]=0` falsy bug in `PricingPage.jsx` (`||` should be `??`)
- [ ] Polish: Legal page typography (enable `@tailwindcss/typography` plugin)
- [ ] Footer links untuk legal pages
- [ ] Privacy disclaimer pada contact/demo gate forms
- [ ] Run comprehensive `testing_agent` (backend + frontend)
- [ ] Update `KTI_09_NAVIGATION_MAP.md`

---

## Phase 19 — Original Scope (Reference) 🟡 PLANNED

### Phase 19.0 Scope
Melengkapi konten marketing website agar memenuhi standar **IT Solution Company** dan meningkatkan trust + conversion.

**Trust Triangle (P0):**
1. Testimonials
2. Privacy Policy + Terms of Service
3. FAQ

**Authority Stack (P1):**
4. Pricing/Packages
5. About page (dedicated)
6. Resources/Downloads center


### Phase 19A — Testimonials (CMS + Public Components)
**Goal:** Tambahkan social proof yang kuat untuk meningkatkan conversion.

**Steps**
- Add entity `cms_testimonials` (bilingual fields) + register in `ENTITY_REGISTRY.md`
- Build admin CMS CRUD for testimonials (`/portal/admin/cms/testimonials`)
- Add public components:
  - Homepage testimonial carousel/rail
  - Optional: show related testimonials on case detail pages
- Seed initial testimonials (min 5)

**Acceptance Criteria**
- Testimonials tampil di homepage (responsive)
- Admin bisa CRUD testimonials
- Bilingual rendering sesuai locale


### Phase 19B — Legal Pages: Privacy Policy + Terms
**Goal:** Compliance + trust + readiness untuk iklan/enterprise.

**Steps**
- Add entity `cms_legal_pages` (bilingual title/content, slug, version)
- Build admin CMS CRUD (`/portal/admin/cms/legal`)
- Add public pages:
  - `/privacy-policy`
  - `/terms-of-service`
  - (optional) `/cookie-policy`
- Add footer links ke legal pages
- Add consent note pada forms (contact + demo gate + assessment start) linking to privacy policy

**Acceptance Criteria**
- Legal pages accessible dan SEO-safe
- Footer links tersedia
- Forms menampilkan disclaimer/link


### Phase 19C — FAQ (CMS + Public Page)
**Goal:** Menjawab objections dan mengurangi friction.

**Steps**
- Add entity `cms_faq` (category, Q/A bilingual, ordering)
- Build admin CMS CRUD (`/portal/admin/cms/faq`)
- Build public `/faq` page:
  - Category filters
  - Accordion UI
- Optional: embed FAQ blocks on services detail pages

**Acceptance Criteria**
- `/faq` live, cepat, mobile friendly
- Admin bisa manage FAQ
- Bilingual Q/A


### Phase 19D — Pricing/Packages
**Goal:** Transparansi dan guidance untuk calon klien + meningkatkan conversion.

**Steps**
- Add entity `cms_packages` (tier, price_from, features bilingual, CTA label)
- Build admin CMS CRUD (`/portal/admin/cms/packages`)
- Add public `/pricing` page dengan tier cards + comparison table
- Integrate CTA to contact form with prefilled package interest

**Acceptance Criteria**
- `/pricing` live dan mudah dipahami
- Packages dapat dikelola di CMS


### Phase 19E — About Page (Dedicated)
**Goal:** Brand story dan trust (enterprise buyers sering cek about page).

**Steps**
- Add route `/about`
- Source content dari `system_settings` atau `cms_pages` (prefer `cms_pages` blocks agar fleksibel)
- Add sections:
  - Story, Mission, Values
  - Timeline/milestones
  - Link ke `/team` dan `/career`

**Acceptance Criteria**
- `/about` live, bilingual, CTA ke contact


### Phase 19F — Resources / Downloads Center
**Goal:** Thought leadership + lead magnet.

**Steps**
- Add entity `cms_resources` (type, description bilingual, file url, gated flag)
- Build admin CMS CRUD (`/portal/admin/cms/resources`)
- Build public `/resources` list + detail
- Lead capture gating (optional P1): require email before download → store into `crm_leads` with source `resource_download`

**Acceptance Criteria**
- `/resources` live, filterable
- Admin bisa upload/manage resources
- Optional gating flow teruji


### Phase 19 Testing (mandatory)
- Manual UX testing (desktop + mobile)
- Content QA:
  - Bilingual fields render correctly
  - Links/CTA correct
  - SEO meta generated/consistent
- Regression: portal/admin/demos tidak terdampak
- Update `KTI_09_NAVIGATION_MAP.md` + validate with `check_nav_map.py`

---

## 3) Next Actions (Immediate)
1. ✅ Phase 16: Demo Sandbox Engine (KN3) (DONE — iteration_13 100% PASS)
2. ✅ Phase 17: API Documentation (DONE)
3. ✅ Phase 18: Compro UI/UX Improvements (IMPLEMENTED — waiting user testing)
4. 🟡 **Phase 19: Content Completion** (start with Trust Triangle: Testimonials + Legal + FAQ)

**Tier 2 remaining (after Phase 19 — menunggu konfirmasi user):**
- Dark/Light theme toggle
- Multi-tenant support / whitelabel
- Advanced analytics (funnels/cohort/retention)
- Mobile PWA
- Payment gateway activation (Midtrans/Xendit)
- Object storage migration S3/R2
- Scaling Demo Sandbox: tambah demo mini-app lain

---

## 4) Success Criteria
- Governance: compliance scripts pass (0 FAIL) at phase ends; SSOT maintained.
- Public: cinematic experience remains stable; reduced-motion supported.
- Admin/Portal: workflows tetap stabil; RBAC correct.
- Phase 16: demo sandbox stable, isolated, lead capture works.
- Phase 17: docs protected Basic Auth + JWT try-it-out works.
- Phase 18:
  - H1 font terasa modern/premium dan konsisten
  - Tidak ada loading screen stuck di Services/Cases
  - Skeleton loaders improve perceived performance
  - Tidak ada regression di portal/admin/demos
- **Phase 19:**
  - Testimonials tersedia dan dapat dikelola via CMS
  - Legal pages (privacy/terms) live + footer links + form disclaimers
  - FAQ page live (bilingual, categorized)
  - Pricing/packages live dan manageable via CMS
  - About page live dan jelas (story/mission/values)
  - Resources center live (optional gated downloads) + lead tracking
  - SEO metadata konsisten dan tidak ada broken links
  - Navigation SSOT (`KTI_09_NAVIGATION_MAP.md`) updated + validation pass
