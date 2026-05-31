# SESSION HANDOFF — Kubus Teknologi Indonesia

> State terkini untuk sesi/agent berikutnya. Baca setelah KTI_00.

## Status: Fase 4 (Assessment Module) SELESAI ✅ — Backend 100% (71/71) + Frontend ~98% teruji. Compliance 16/0/0. Fase 1–4 done. Lanjut Fase 5 (Portal Client/Staff penuh + Project Management).

## Yang sudah ada
- Governance docs: `/app/docs/KTI_00–13` + README.
- Memory: `/app/memory/PRD.md`, `TECH_DECISIONS.md`, `SESSION_LOG.md`, handoff ini, `test_credentials.md`.
- SSOT: `/app/ENTITY_REGISTRY.md`.
- Scripts: `/app/scripts/load_context.sh`, `validate_compliance.py`, `check_nav_map.py`.
- `plan.md` (roadmap).

## Baseline kode
- Backend: template FastAPI + Claude POC script (`scripts/poc_claude.py`). Belum ada router domain.
- Frontend: POC immersive di `/poc` (`poc/ImmersivePoc.jsx`, `lib/spaceScene.js`, `components/three/ImmersiveScene.jsx`, `lib/useDeviceCapability.js`). `App.js` punya route `/` + `/poc`.
- Terinstall: three, gsap, lenis, i18next, react-i18next (frontend); reportlab, emergentintegrations (backend). EMERGENT_LLM_KEY ada di backend/.env.
- @react-three/fiber & drei ter-install TAPI TIDAK DIPAKAI (lihat TD-007 — pakai Three.js imperatif).

## Keputusan kunci (lihat TECH_DECISIONS.md)
Bilingual {id,en} · JWT+RBAC no self-register · Claude grounded · assessment template-driven · balanced 3D + fallback · **3D = Three.js imperatif (TD-007)**.

## Next action
**Fase 5 (Portal Client/Staff penuh + Project Management)** — tentukan prioritas dgn user. Fase 1–4 sudah selesai (lihat di bawah). Fondasi auth/RBAC, Media Library (TD-008), Advanced CMS, dan Assessment Module sudah siap.

## Fase 4 — Assessment Module (SELESAI ✅, di-port/adaptasi dari KN3 Discovery)
**Backend** (`backend/`):
- `assessment_engine.py` — branching default-show (evaluate_show_if), progress value-aware (is_answer_filled), OTHER_SENTINEL.
- `assessment_questions.py` — seed template **bilingual** "IT Solution Discovery" (8 domain, ~28 pertanyaan, 7 tipe, 3 branching) — generalisasi dari struktur KN3 ke konteks IT.
- `assessment_pdf.py` — PDF bilingual (reportlab) brand KTI.
- `routers/assessment.py` — PUBLIC via UUID token (no login): GET/PATCH answers/submit/export.pdf/attachments(+download/delete). ADMIN (require_role): templates, sessions(list/create→token+share_url), stats, acknowledge, delete(cascade).
- `seed_assessment.py` (idempotent) + index (assessment_sessions.token unique, assessment_answers (session_id,question_id) unique).
- Lampiran via `storage.py` get_storage() (TD-008 local), ext pdf/png/jpg/jpeg/xlsx/docx, 10MB, maks 5/pertanyaan.

**Frontend** (`frontend/src/`):
- PUBLIC standalone `/assessment/:token` — `features/assessment/`: AssessmentClient (autosave 700ms, dashboard ring per-domain, branching mirror, locale ID/EN, summary+submit+PDF, invalid view), AssessmentQuestion (7 tipe + other + note + skip + attachments), ProgressRing, assessmentApi.
- ADMIN `/portal/admin/assessments` — `features/admin/pages/AdminAssessments.jsx` (stats, create+copy link, list+progress+NEW badge, acknowledge, PDF, delete). Nav item di sectionCrm.
- Media-driven public: CrewGrid (team avatar_url), CasesGrid (cover_image_url), BlogPage (cover_image_url) — fallback ke dekoratif bila kosong.
- i18n `assess.*` (ID+EN), testids `ASSESS` di constants/testIds/admin.js.

**Collection baru (registered):** assessment_templates, assessment_sessions, assessment_answers, assessment_attachments.
**Catatan:** Public assessment endpoint TANPA auth (token UUID = kredensial). Template editor visual (drag pertanyaan) = future. AssessmentQuestion hindari dynamic JSX tag (TD-007).

## Fase 3 — yang sudah dibangun (SELESAI ✅)
**Backend** (`backend/`):
- `security.py` — JWT HS256 (access 8j + refresh 7h stateless) + passlib bcrypt + `get_current_user`/`require_role`.
- `routers/auth.py` — login/refresh/logout/me. `routers/admin_users.py` — CRUD user (admin only).
- `routers/admin.py` — `/api/admin/stats` + `/api/admin/leads` (admin+staff).
- `storage.py` — `StorageBackend` ABC + `LocalStorageBackend` + `get_storage()` (env `STORAGE_BACKEND=local`, `UPLOAD_DIR`).
- `routers/media.py` — upload (img/video/pdf, limit 10/50/20MB, dim via Pillow) + serve Range 206 (`/api/media/file/{id}`) + folders + usage; admin router + public_router.
- `routers/cms.py` — generic schema-light CRUD untuk semua `cms_*` (+home-blocks) + publish/unpublish + reorder + settings (cms_pages "site").
- `content.py` public sekarang filter `status=published`.
- `server.py` — exception handler envelope {success,error}, register router baru, index baru, `seed_users` (idempotent).
- `.env` tambah: `EMERGENT_LLM_KEY`, `JWT_SECRET`, `STORAGE_BACKEND`, `UPLOAD_DIR`.

**Frontend** (`frontend/src/`):
- `context/AuthContext.jsx` + `lib/apiClient.js` (interceptor token + auto-refresh 401).
- `features/portal/auth/LoginPage.jsx`, `features/admin/ProtectedRoute.jsx`, `AdminLayout.jsx` (sidebar+topbar, role-aware nav, ID/EN, logout).
- Pages: `AdminDashboard`, `AdminUsers`, `AdminLeads`, `MediaLibrary` (+`components/admin/MediaPicker.jsx`), CMS schema-driven (`features/admin/cms/*`: schemas, FieldInput, ResourceForm, ResourceManager) + `CmsResourcePage`, `CmsSettings`.
- i18n keys `auth.*`, `admin.*`, `cms.*`, `media.*` (ID+EN). testids di `constants/testIds/admin.js`.

**Seed login** (`memory/test_credentials.md`): admin@kubus.id/Admin#2026 · staff@kubus.id/Staff#2026 · client@kubus.id/Client#2026. **Hapus/ganti sebelum production.**

## Catatan penting Fase 3
- ⚠️ FieldInput.jsx: HINDARI dynamic JSX tag (`<Cmp>`) — plugin visual-edits babel crash (RangeError). Pakai if/else literal (TD-007 family).
- Collection baru ter-register di ENTITY_REGISTRY: `system_users`, `media_folders`, `media_assets`, `media_usage`, `cms_home_blocks`.
- `validate_compliance.py` di-upgrade: duplicate-endpoint check kini PREFIX-AWARE (hindari false positive antar router beda prefix).
- Media field di schema CMS (image_url/cover_image_url/avatar_url) DISIMPAN tapi belum dirender di public site (opsional wiring lanjutan).
- AI Advisor pakai EMERGENT_LLM_KEY (universal) — bila 502 "budget exceeded", user top-up via Profile → Universal Key.

## Catatan
- **Fase 2.5 (V2 redesign) SELESAI:** UI public dibangun ulang sinematik (scroll-driven). Sistem komponen baru di `src/components/kti/*` (TwoToneHeading, GlassCard, GlassPillButton, MediaSection, ScrollScrubHero, StickyStackServices, IdeaToLaunchSlider, GaugeDataViz, HorizontalCasesRail, SecureTransmissionDemo, EngagementTiers, KubusCore). Nav = `FloatingPillNavbar`. Section interaktif baru pakai placeholder di `src/content/home.js` (CMS-ready, untuk di-wire Fase 3).
- Fonts: Clash Display + Sora + Chakra Petch (CDN, tanpa install dependency).
- Scroll engine: Lenis + GSAP ScrollTrigger terintegrasi via `context/SmoothScroll.jsx` + `lib/gsap.js`. Hero & Cases rail = pinned; mobile/reduced-motion = poster fallback (tanpa pin/scrub/WebGL).
- Dead code dihapus: `blocks/HeroLaunch.jsx`, `components/ImmersiveHeader.jsx`. `MagneticButton.jsx` & `poc/*` masih ada tapi tak dipakai (boleh dihapus nanti).
- Konten Fase 2 tetap live dari MongoDB (cms_* + cms_pages). CMS Fase 3 meng-edit collection yang sama + tambah section baru.
- AI Advisor (Claude) berfungsi (floating bottom-LEFT agar tidak bentrok badge preview Emergent).
- @react-three/fiber & drei TIDAK dipakai (TD-007 — Three.js imperatif).

## STOP & ASK aktif
Install dependency baru, ubah auth, tambah menu di luar KTI_09 -> konfirmasi user dulu.
