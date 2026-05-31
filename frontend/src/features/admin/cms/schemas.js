// Declarative CMS schemas. One generic editor drives every cms_* collection.
// Field types: text | number | boolean | bilingual | bilingual-area | tags |
//              bilingual-list | object-list | media
// Labels carry {id,en}; rendered by current locale.

const L = (id, en) => ({ id, en });

const RESULTS_ITEM = [
  { name: "label", type: "bilingual", label: L("Label", "Label") },
  { name: "value", type: "text", label: L("Nilai", "Value") },
];

export const RESOURCE_SCHEMAS = {
  services: {
    label: L("Layanan", "Services"),
    primary: "title",
    hasSlug: true,
    fields: [
      { name: "slug", type: "text", label: L("Slug", "Slug"), required: true, half: true },
      { name: "icon", type: "text", label: L("Ikon (Lucide)", "Icon (Lucide)"), half: true },
      { name: "category", type: "text", label: L("Kategori", "Category"), half: true },
      { name: "featured", type: "boolean", label: L("Unggulan", "Featured"), half: true },
      { name: "title", type: "bilingual", label: L("Judul", "Title") },
      { name: "summary", type: "bilingual", label: L("Ringkasan", "Summary") },
      { name: "description", type: "bilingual-area", label: L("Deskripsi", "Description") },
      { name: "image_url", type: "media", label: L("Gambar", "Image") },
    ],
  },
  cases: {
    label: L("Studi Kasus", "Case Studies"),
    primary: "title",
    hasSlug: true,
    fields: [
      { name: "slug", type: "text", label: L("Slug", "Slug"), required: true, half: true },
      { name: "client_name", type: "text", label: L("Nama Klien", "Client Name"), half: true },
      { name: "cover", type: "text", label: L("Cover (key)", "Cover (key)"), half: true },
      { name: "industry", type: "bilingual", label: L("Industri", "Industry") },
      { name: "title", type: "bilingual", label: L("Judul", "Title") },
      { name: "summary", type: "bilingual", label: L("Ringkasan", "Summary") },
      { name: "challenge", type: "bilingual-area", label: L("Tantangan", "Challenge") },
      { name: "approach", type: "bilingual-area", label: L("Pendekatan", "Approach") },
      { name: "solution", type: "bilingual-area", label: L("Solusi", "Solution") },
      { name: "impact", type: "bilingual-area", label: L("Dampak", "Impact") },
      { name: "results", type: "object-list", label: L("Hasil", "Results"), itemFields: RESULTS_ITEM },
      { name: "tech", type: "tags", label: L("Teknologi", "Tech") },
      { name: "cover_image_url", type: "media", label: L("Gambar Cover", "Cover Image") },
      // ── Demo Sandbox Config ──────────────────────────────────────────────
      { name: "demo_enabled", type: "boolean", label: L("Aktifkan Demo", "Enable Demo"), half: true },
      { name: "demo_slug", type: "text", label: L("Demo App Slug", "Demo App Slug"), half: true,
        placeholder: "kn3", hint: L("Contoh: kn3 (nama app demo)", "e.g. kn3") },
      { name: "demo_label_id", type: "text", label: L("Label Tombol Demo (ID)", "Demo Button Label (ID)"), half: true,
        placeholder: "Coba Demo WMS" },
      { name: "demo_timeout_minutes", type: "number", label: L("Timeout Demo (menit)", "Demo Timeout (min)"), half: true,
        placeholder: "90" },
    ],
  },
  team: {
    label: L("Tim", "Team"),
    primary: "name",
    hasSlug: false,
    fields: [
      { name: "name", type: "text", label: L("Nama", "Name"), half: true },
      { name: "seed", type: "text", label: L("Seed Avatar", "Avatar Seed"), half: true },
      { name: "role", type: "bilingual", label: L("Jabatan", "Role") },
      { name: "bio", type: "bilingual-area", label: L("Bio", "Bio") },
      { name: "socials.linkedin", type: "text", label: L("LinkedIn", "LinkedIn"), half: true },
      { name: "avatar_url", type: "media", label: L("Foto", "Photo") },
    ],
  },
  clients: {
    label: L("Klien", "Clients"),
    primary: "name",
    hasSlug: false,
    fields: [
      { name: "name", type: "text", label: L("Nama", "Name") },
      { name: "logo_url", type: "media", label: L("Logo", "Logo") },
    ],
  },
  tech: {
    label: L("Teknologi", "Technology"),
    primary: "name",
    hasSlug: false,
    fields: [
      { name: "name", type: "text", label: L("Nama", "Name"), half: true },
      { name: "category", type: "text", label: L("Kategori", "Category"), half: true },
    ],
  },
  blog: {
    label: L("Artikel", "Blog"),
    primary: "title",
    hasSlug: true,
    fields: [
      { name: "slug", type: "text", label: L("Slug", "Slug"), required: true, half: true },
      { name: "author", type: "text", label: L("Penulis", "Author"), half: true },
      { name: "published_at", type: "text", label: L("Tanggal Terbit", "Published At"), half: true },
      { name: "cover", type: "text", label: L("Cover (key)", "Cover (key)"), half: true },
      { name: "title", type: "bilingual", label: L("Judul", "Title") },
      { name: "excerpt", type: "bilingual", label: L("Ringkasan", "Excerpt") },
      { name: "body", type: "bilingual-area", label: L("Isi", "Body") },
      { name: "tags", type: "tags", label: L("Tag", "Tags") },
      { name: "cover_image_url", type: "media", label: L("Gambar Cover", "Cover Image") },
    ],
  },
  careers: {
    label: L("Karier", "Careers"),
    primary: "title",
    hasSlug: true,
    fields: [
      { name: "slug", type: "text", label: L("Slug", "Slug"), required: true, half: true },
      { name: "location", type: "text", label: L("Lokasi", "Location"), half: true },
      { name: "type", type: "text", label: L("Tipe", "Type"), half: true },
      { name: "level", type: "text", label: L("Level", "Level"), half: true },
      { name: "title", type: "bilingual", label: L("Judul", "Title") },
      { name: "description", type: "bilingual-area", label: L("Deskripsi", "Description") },
      { name: "requirements", type: "bilingual-list", label: L("Persyaratan", "Requirements") },
    ],
  },
  "home-blocks": {
    label: L("Home Sections", "Home Sections"),
    primary: "title",
    hasSlug: false,
    fields: [
      { name: "key", type: "text", label: L("Key", "Key"), required: true, half: true },
      { name: "kind", type: "text", label: L("Jenis", "Kind"), half: true },
      { name: "title", type: "bilingual", label: L("Judul", "Title") },
      { name: "subtitle", type: "bilingual", label: L("Subjudul", "Subtitle") },
      {
        name: "items", type: "object-list", label: L("Item", "Items"),
        itemFields: [
          { name: "title", type: "bilingual", label: L("Judul", "Title") },
          { name: "text", type: "bilingual", label: L("Teks", "Text") },
        ],
      },
    ],
  },
};

export const SETTINGS_SCHEMA = {
  fields: [
    { name: "hero_title", type: "bilingual", label: L("Judul Hero", "Hero Title") },
    { name: "hero_subtitle", type: "bilingual-area", label: L("Subjudul Hero", "Hero Subtitle") },
    { name: "tagline", type: "bilingual", label: L("Tagline", "Tagline") },
    { name: "about_title", type: "bilingual", label: L("Judul Tentang", "About Title") },
    { name: "about_body", type: "bilingual-area", label: L("Isi Tentang", "About Body") },
    {
      name: "stats", type: "object-list", label: L("Statistik", "Stats"),
      itemFields: RESULTS_ITEM,
    },
    { name: "contact.email", type: "text", label: L("Email", "Email"), half: true },
    { name: "contact.phone", type: "text", label: L("Telepon", "Phone"), half: true },
    { name: "contact.address", type: "bilingual", label: L("Alamat", "Address") },
    { name: "contact.social.linkedin", type: "text", label: L("LinkedIn", "LinkedIn"), half: true },
    { name: "contact.social.instagram", type: "text", label: L("Instagram", "Instagram"), half: true },
    { name: "contact.social.twitter", type: "text", label: L("Twitter/X", "Twitter/X"), half: true },
    { name: "contact.social.github", type: "text", label: L("GitHub", "GitHub"), half: true },
  ],
};

export function fieldLabel(field, lang) {
  const l = field.label || {};
  return (lang && lang.startsWith("en")) ? (l.en || l.id) : (l.id || l.en);
}
