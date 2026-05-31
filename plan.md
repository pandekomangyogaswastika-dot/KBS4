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
  - **Phase 18: Compro UI/UX Improvements (Public Site Polish)**
    - Modernisasi **font heading (H1/H2)** agar lebih modern/enterprise
    - Fix **loading states** (Services/Cases stuck loader) + timeout fallback
    - Simplify hero (reduce cognitive load, improve clarity & CTA hierarchy)
    - Improve content clarity (balance metaphor vs. value proposition)
    - Mobile-first checks: responsive hero, CTAs, 3D fallback
    - Performance polish for animation/3D: lazy-load + prefers-reduced-motion

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

**Current status (overall):** Platform delivered through **Phase 17** ✅
- ✅ Phase 0–16 selesai (Phase 16 Demo Sandbox Engine: KN3) + E2E verified.
- ✅ Phase 17 API Documentation (OpenAPI/Swagger UI) — COMPLETE (2026-05-31)
  - `/api/docs`, `/api/redoc`, `/api/openapi.json` protected via **HTTP Basic Auth**
  - JWT Bearer scheme tersedia untuk “Try it out”
  - Tag grouping disediakan
  - Demo KN3 internal endpoints (`/api/demo/kn3/*`) disembunyikan dari schema

**Next major work:** **Phase 18 — Compro UI/UX Improvements** (public marketing site polish).

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

## Phase 18 — Compro UI/UX Improvements (Public Site Polish) 🟡 PLANNED

### Phase 18.0 Scope (confirmed by discussion)
Fokus pada UI/UX public marketing site:
- Modernisasi font untuk H1 (dan heading lain yang relevan) agar lebih modern
- Fix masalah **loader** yang berpotensi “stuck” pada halaman Services/Cases
- Perbaikan hirarki CTA dan kejelasan value proposition di hero
- Mobile-first responsivity & ergonomics
- Performance polish untuk animasi/3D (prefers-reduced-motion + lazy-load)

### Phase 18A — Typography Modernization (H1/H2)
**Goal:** Heading terasa lebih modern, premium, dan enterprise.

**Steps**
- Audit font yang digunakan (saat ini `Clash Display` untuk display)
- Pilih font display baru (opsi aman: `Space Grotesk`, `General Sans`, atau `Plus Jakarta Sans` sebagai display)
- Terapkan konsisten di seluruh public pages:
  - Home hero H1
  - Page headers (services/cases/blog/team/contact)
- Pastikan fallback dan loading font tidak mengganggu CLS.

### Phase 18B — Loading Reliability (Services/Cases)
**Goal:** Tidak ada halaman public yang stuck di loading.

**Steps**
- Audit komponen loader dan data fetching.
- Tambahkan:
  - timeout fallback (mis. 5 detik) → tampilkan error + retry
  - skeleton loader untuk list pages
  - guard untuk “loading 100% tapi tidak redirect”
- Pastikan behavior sama untuk desktop & mobile.

### Phase 18C — Hero Simplification + CTA Hierarchy
**Goal:** Kurangi cognitive load, tingkatkan conversion.

**Steps**
- Evaluasi elemen hero yang saling bersaing (H1, 3D, telemetry panel, multi CTA)
- Define CTA hierarchy:
  - Primary: Konsultasi (lebih eksplisit)
  - Secondary: Lihat Portfolio/Case Studies
- Rapikan spacing/white space & focus point.

### Phase 18D — Content Clarity (Copy)
**Goal:** Lebih jelas dan cepat dipahami tanpa kehilangan nuansa space theme.

**Steps**
- Pendekkan subheading value proposition
- Kurangi jargon/metafora di CTA
- Pastikan user “langsung paham” layanan utama di 5 detik pertama.

### Phase 18E — Mobile-first UX 
**Goal:** Experience setara/lebih baik di layar kecil.

**Steps**
- Audit hero layout di 320/375/414 px
- Pastikan CTA tidak cramped
- Pastikan 3D/telemetry panel punya fallback sederhana di mobile

### Phase 18F — Motion/3D Performance Polish
**Goal:** Animasi tetap cinematic tapi tidak mengorbankan performa.

**Steps**
- Perkuat `prefers-reduced-motion` behavior
- Lazy-load 3D scene hanya saat diperlukan
- Batasi heavy effects untuk low-end devices (optional device heuristics)

### Phase 18 Testing (mandatory)
- Manual UX testing (desktop + mobile)
- Periksa:
  - Tidak ada stuck loading
  - Hero copy & CTA jelas
  - Font heading terlihat modern dan konsisten
  - Reduced-motion fallback bekerja
- Regression: portal/admin/demos tidak terdampak.

---

## 3) Next Actions (Immediate)
1. ✅ Phase 16: Demo Sandbox Engine (KN3) (DONE — iteration_13 100% PASS)
2. ✅ Phase 17: API Documentation (DONE)
3. 🟡 **Phase 18: Compro UI/UX Improvements** (mulai dari: fix loading + modernisasi H1 font)

**Tier 2 remaining (after Phase 18 — menunggu konfirmasi user):**
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
- **Phase 18:**
  - H1 font terasa modern/premium dan konsisten
  - Tidak ada loading screen stuck di Services/Cases
  - CTA hierarchy jelas; conversion path lebih kuat
  - Mobile UX solid
  - Animasi/3D tetap halus; reduced-motion fallback benar
  - Tidak ada regression di portal/admin/demos
