# KTI_09 — NAVIGATION MAP (Master SSOT)

> Sebelum menambah halaman/menu APAPUN, update dokumen ini dulu (Navigation First Policy). Validasi dengan `python3 /app/scripts/check_nav_map.py`.

---

## PUBLIC (tanpa login) — bilingual, immersive
```
/                 Home (single-page immersive scroll):
                    #launch (Hero)  #origin (About)  #constellations (Services)
                    #engine (Tech Stack)  #worlds (Cases teaser)  #crew (Team)
                    #starmap (Clients)  #mission (Contact CTA)
/services         List services (Constellations)        testid: nav-services
/services/:slug   Service detail
/cases            Cases list (Explored Worlds)          testid: nav-cases
/cases/:slug      Case study detail (dive-in)
/tech             Tech Stack (The Engine)               testid: nav-tech
/team             Team (The Crew)                       testid: nav-team
/blog             Blog list                             testid: nav-blog
/blog/:slug       Blog post
/career           Career list                           testid: nav-career
/career/:slug     Job detail
/contact          Contact (Mission Control)             testid: nav-contact
/assessment       Assessment intro / start
/assessment/:token  Assessment fill (klien, no login)
+ AI Solution Advisor : floating widget (semua halaman publik)
+ Header: logo, nav links, language toggle (ID/EN), "Client Login" button
```

## PORTAL (login) — /portal
```
/portal/login                     Login (semua role)

CLIENT (role: client)
/portal/dashboard                 Ringkasan project
/portal/projects                  List project klien
/portal/projects/:id              Detail + timeline + milestone + dokumen + approval
/portal/cases                     Cases terkait klien
/portal/invoices                  Invoice & status bayar
/portal/messages                  Chat dengan tim
/portal/assistant                 AI assistant (grounded)

STAFF (role: staff)
/portal/staff/projects            Project yang dikelola
/portal/staff/projects/:id        Kelola milestone/dokumen/approval
/portal/staff/clients             Daftar klien
/portal/staff/assessments         Kelola assessment session
/portal/staff/messages            Chat dengan klien

ADMIN (role: admin & staff) — Advanced CMS + Media Library  [IMPLEMENTED Fase 3]
/portal/login                     Login (semua role)  testid: login-*
/portal/coming-soon               Placeholder portal klien (role client diarahkan ke sini; portal penuh = Fase 5)
/portal/admin                     Admin dashboard (stats)            testid: admin-nav-dashboard
/portal/admin/leads               Leads/CRM (admin+staff)            testid: admin-nav-leads
/portal/admin/media               Media Library (upload/folders)    testid: admin-nav-media
/portal/admin/cms/services        CRUD services (bilingual)         testid: admin-nav-cms-services
/portal/admin/cms/cases           CRUD cases                        testid: admin-nav-cms-cases
/portal/admin/cms/tech            CRUD tech stack                   testid: admin-nav-cms-tech
/portal/admin/cms/team            CRUD team                         testid: admin-nav-cms-team
/portal/admin/cms/clients         CRUD clients                      testid: admin-nav-cms-clients
/portal/admin/cms/blog            CRUD blog                         testid: admin-nav-cms-blog
/portal/admin/cms/careers         CRUD careers                      testid: admin-nav-cms-careers
/portal/admin/cms/home-blocks     Home sections (process/tiers/...) testid: admin-nav-cms-home
/portal/admin/settings            Site settings (hero/about/contact) testid: admin-nav-settings
/portal/admin/assessments         Assessment (Discovery) sessions    testid: admin-nav-assessments  [IMPLEMENTED Fase 4]
/portal/admin/users               User management (admin only)      testid: admin-nav-users

PUBLIC (tanpa login, akses via UUID token)  [IMPLEMENTED Fase 4]
/assessment/:token                Kuesioner 'IT Solution Discovery' untuk klien (autosave, lampiran, PDF)

CATATAN IMPLEMENTASI Fase 3:
- Route `/portal/admin/cms/:resource` menggantikan rencana awal `/portal/admin/content/*` (schema-driven, satu editor untuk semua cms_*).
- `/portal/admin/settings` menggantikan `/portal/admin/content/pages`.
- Akses: admin+staff = CMS/Media/Leads/Settings/Assessment; users = admin only.
- Belum diimplementasi (Fase 5+): /portal/admin/projects, portal CLIENT & STAFF penuh.

ADMIN/STAFF/CLIENT (Fase 5+) — RENCANA, belum dibangun
/portal/admin/projects            Project management (assign staff)
/portal/client                    Portal klien penuh (dashboard, proyek, pesan)
```

## Anti-Pattern Navigasi
- Maksimum kedalaman 4 level. Tidak ada label menu duplikat. Tiap nav item punya data-testid `nav-*`.
