# PRD — Kubus Teknologi Indonesia Platform

**Produk:** Immersive space-themed company website + multi-role application portal untuk **Kubus Teknologi Indonesia** (perusahaan IT solutions).

**Status:** Fase 4 (Assessment Module) SELESAI ✅. Platform: public site sinematik + AI Advisor, admin (auth/RBAC, Media Library, Advanced CMS bilingual), dan Assessment Module (Discovery klien token-based + PDF). Lanjut Fase 5 (Portal Client/Staff + Project Management).

---

## Visi
Website award-grade (referensi UX: oryzo.ai) dengan tema **Space**: bukan sekadar sumber informasi, tapi pengalaman menjelajahi "Kubus Universe". Sekaligus platform: CMS canggih, portal klien & staff, assessment intake, dan AI advisor (Claude).

## Pengguna & Roles
- **Visitor** — jelajah website, isi assessment (via token), chat AI advisor.
- **Client** — portal: dashboard, timeline project, dokumen, cases, approval, invoice, chat, AI assistant. (Akun dibuat staff/admin.)
- **Staff** — kelola project/milestone/dokumen, klien, assessment.
- **Admin** — advanced CMS, user management, project management, leads, settings.

## Keputusan Produk (dari diskusi user)
- Bahasa: **Bilingual ID/EN** (toggle, default ID).
- 3D/animasi: **Balanced** (3D di hero/section kunci + partikel ringan + CSS), wajib fallback & reduced-motion.
- Konten awal: **placeholder profesional** (diganti user nanti).
- Auth: **email+password**, RBAC; client/staff dibuat oleh admin/staff (no self-register).
- Assessment: **template-driven** dikelola CMS; seed 1 template "IT Solution Discovery" (adopsi gaya pertanyaan dari referensi).
- AI: **Claude** (Emergent LLM), **grounded** ke konten Kubus; dua permukaan (publik + portal).
- Service categories: Custom Software/ERP/WMS, Web & Mobile, Cloud/DevOps, AI/Data/Automation, IoT/RFID, UI/UX & Product Design, IT Consulting & System Integration.

## Roadmap (SSOT operasional = /app/plan.md)
Fase 0 Foundation → 1 Core POC (Claude + immersive 3D) → 2 Public Website → 3 Auth+CMS → 4 Assessment → 5 Client Portal → 6 Staff/PM → 7 AI. (Blog & Career: list publik di Fase 2, editor CMS di Fase 3.)

---

## Feature Log
| Tanggal | Fase | Fitur | Status |
|---------|------|-------|--------|
| - | 0 | Governance docs (KTI_00–13), memory layer, ENTITY_REGISTRY, scripts | done |
| - | 1 | Core POC: Claude (grounded, 3/3) + immersive Three.js (imperatif) + GSAP/Lenis + fallback | done ✅ |
| - | 2 | Public Immersive Website: hero 3D, semua section, bilingual ID/EN, 10 halaman, contact→crm_leads, AI Advisor (Claude), seed konten placeholder | done ✅ |
| - | 2.5 | Cinematic redesign V2 (scroll-scrub hero + Kubus Core, sticky services, gauges, cases rail) | done ✅ |
| - | 3 | Auth & RBAC (JWT access+refresh, admin/staff/client), Media Library (storage LOCAL TD-008, upload/serve Range, folders, picker), Advanced CMS (schema-driven CRUD semua cms_* + home-blocks, draft/publish, reorder, site settings), public filter status=published | done ✅ |
| - | 4 | Assessment Module (port/adaptasi KN3 Discovery): template-driven bilingual "IT Solution Discovery" (8 domain), public token-based client flow (autosave, branching, lampiran via TD-008, submit), admin (create link/list/stats/acknowledge/delete), export PDF (reportlab). + media-driven public (avatar tim, cover case/blog) | done ✅ |

## Backlog / Ide (P3)
- Email/WhatsApp notifikasi (assessment submitted, invoice).
- Analytics dashboard admin.
- Multi-PIC collaborate per assessment session.
- Retrieval (RAG) untuk AI advisor bila konten besar.
- Sound design ambient + toggle (opsional, dikonfirmasi user nanti).
