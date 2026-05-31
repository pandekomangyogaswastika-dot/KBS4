# ENTITY REGISTRY — Kubus Teknologi Indonesia (SSOT)

> **Daftar otoritatif SEMUA MongoDB collection.** Sebelum membuat collection baru, cek di sini. Setiap collection baru WAJIB didaftarkan. Satu entity = satu collection (KTI_04).

**Konvensi:** `{domain}_{entity}` · `id` = UUID v4 · timestamp UTC ISO-8601 · soft delete (`voided`). Field konten user-facing = objek bilingual `{id, en}`.

---

## SYSTEM
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `system_users` | Akun admin/staff/client (dibuat admin/staff) | id, email(unique), password_hash, role, name, company?, phone?, locale, active |
| `system_settings` | Konfigurasi situs global (kontak, sosial, SEO, hero copy) | id, key(unique), value (bilingual bila perlu) |
| `audit_logs` | Jejak aksi sensitif | id, actor_id, action, entity, entity_id, meta, created_at |

## MEDIA (Media Library — Fase 3B, storage LOCAL via abstraksi TD-008)
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `media_folders` | Folder/kategori media | id, name, parent_id?, order, created_at |
| `media_assets` | Aset (image/video/document) | id, original_name, filename, mime_type, kind(image\|video\|document), size_bytes, width?, height?, storage_backend, storage_key, url, folder_id?, alt{}, title{}, tags[], created_by, voided |
| `media_usage` | Jejak pemakaian aset di CMS | id, asset_id, entity_type, entity_id, field, created_at |

## CMS (konten publik, bilingual)
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `cms_services` | Layanan (Constellations) | id, slug(unique), title{}, summary{}, body{}, icon, category, order, featured, status |
| `cms_home_blocks` | Section interaktif home (process/tiers/gauges/secure) | id, key(unique), kind, title{}, subtitle{}, items[], order, status |
| `cms_cases` | Studi kasus (Explored Worlds), bisa link project | id, slug(unique), title{}, client_name, industry, summary{}, body{}, cover, gallery[], results[], tech[], project_id?, status |
| `cms_team` | Anggota tim (The Crew) | id, name, role{}, bio{}, photo, socials, order, status |
| `cms_clients` | Klien (Star Map) | id, name, logo, url, order, status |
| `cms_tech` | Tech stack (The Engine) | id, name, category, logo, order |
| `cms_blog` | Artikel | id, slug(unique), title{}, excerpt{}, body{}, cover, tags[], author_id, published_at, status |
| `cms_careers` | Lowongan | id, slug(unique), title{}, location, type, level, description{}, requirements{}, status |
| `cms_pages` | Section editable (hero, about, dll) | id, key(unique), blocks[] (bilingual) |

## CRM
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `crm_leads` | Kontak form + lead dari assessment | id, source, name, email, company?, message, assessment_session_id?, status, created_at |

## ASSESSMENT (Discovery)
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `assessment_templates` | Template (domain+pertanyaan), bilingual | id, name{}, description{}, domains[], status |
| `assessment_sessions` | Instance terkirim ke klien | id, template_id, client_name, project_name, contact, token(uuid,unique), status, acknowledged_at, submitted_at |
| `assessment_answers` | Jawaban | id, session_id, question_id, value, other_text?, note?, (unique: session_id+question_id) |
| `assessment_attachments` | Lampiran | id, session_id, question_id, filename, size, path, content_type |

## PROJECT MANAGEMENT (portal)
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `pm_projects` | Project klien | id, code, name, client_id, staff_ids[], status, progress, start_date, due_date, summary |
| `pm_milestones` | Milestone/timeline | id, project_id, title, description, status(todo/in_progress/done), order, due_date, completed_at |
| `pm_documents` | Deliverable/dokumen | id, project_id, name, path, content_type, size, uploaded_by, created_at |
| `pm_approvals` | Approval/feedback milestone | id, project_id, milestone_id, status(pending/approved/changes_requested), feedback, decided_by, decided_at |

## BILLING
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `billing_invoices` | Invoice | id, number(unique), project_id, client_id, items[], amount, currency, status(unpaid/paid/overdue), issued_at, due_at, paid_at |

## COMMUNICATION / AI
| Collection | Deskripsi | Field kunci |
|------------|-----------|-------------|
| `chat_threads` | Thread klien<->staff | id, project_id?, client_id, staff_ids[], last_message_at |
| `chat_messages` | Pesan | id, thread_id, sender_id, body, attachments[], created_at |
| `ai_conversations` | Riwayat AI (advisor publik + portal) | id, surface(public/portal), user_id?, visitor_id?, messages[], created_at, updated_at |

---

## FORBIDDEN / RESERVED (jangan dipakai — melanggar SSOT)
`users`, `services`, `cases`, `projects`, `invoices`, `messages`, `leads`, `team`, `clients`, `blog`, `posts`, `sessions`, `templates`, `documents`, `files`, `content` (tanpa prefix domain). Gunakan versi ber-prefix di atas.

_Status: cms_services, cms_cases, cms_team, cms_clients, cms_tech, cms_blog, cms_careers, cms_pages, crm_leads, ai_conversations DIBUAT & ter-seed (Fase 2). system_users, media_folders, media_assets, media_usage, cms_home_blocks DIBUAT di Fase 3 (auth/RBAC + Media Library + Advanced CMS). assessment_templates, assessment_sessions, assessment_answers, assessment_attachments DIBUAT di Fase 4 (Assessment Module; template "it-solution-discovery" ter-seed). Sisanya dibuat saat fase masing-masing._
