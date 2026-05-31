import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Plus, Trash2, Image as ImageIcon } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import MediaPicker from "@/components/admin/MediaPicker";
import { fieldLabel } from "@/features/admin/cms/schemas";

const inputCls = "kti-focus w-full rounded-lg border border-white/12 bg-white/[0.04] px-3 py-2 text-sm text-white placeholder:text-white/30";
const tagCls = "font-mono-kti text-[10px] uppercase tracking-wider text-[color:var(--kti-text-faint)]";

function Bilingual({ value, onChange, area }) {
  const v = value || { id: "", en: "" };
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      <div>
        <span className={tagCls}>ID</span>
        {area ? (
          <textarea rows={3} value={v.id || ""} onChange={(e) => onChange({ ...v, id: e.target.value })} className={`${inputCls} mt-1`} />
        ) : (
          <input value={v.id || ""} onChange={(e) => onChange({ ...v, id: e.target.value })} className={`${inputCls} mt-1`} />
        )}
      </div>
      <div>
        <span className={tagCls}>EN</span>
        {area ? (
          <textarea rows={3} value={v.en || ""} onChange={(e) => onChange({ ...v, en: e.target.value })} className={`${inputCls} mt-1`} />
        ) : (
          <input value={v.en || ""} onChange={(e) => onChange({ ...v, en: e.target.value })} className={`${inputCls} mt-1`} />
        )}
      </div>
    </div>
  );
}

function TagsField({ value, onChange }) {
  const [str, setStr] = useState((value || []).join(", "));
  const handle = (e) => {
    setStr(e.target.value);
    onChange(e.target.value.split(",").map((s) => s.trim()).filter(Boolean));
  };
  return <input value={str} onChange={handle} placeholder="a, b, c" className={inputCls} />;
}

function MediaField({ value, onChange }) {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  return (
    <div className="flex items-center gap-3">
      {value ? (
        <div className="size-16 overflow-hidden rounded-lg border border-white/12"><img src={value} alt="" className="h-full w-full object-cover" /></div>
      ) : (
        <div className="grid size-16 place-items-center rounded-lg border border-dashed border-white/15"><ImageIcon className="size-5 text-white/40" /></div>
      )}
      <button type="button" onClick={() => setOpen(true)} className="kti-focus rounded-lg border border-white/12 px-3 py-2 text-xs text-white hover:bg-white/[0.06]">{t("media.pick")}</button>
      {value ? (
        <button type="button" onClick={() => onChange("")} className="kti-focus rounded-lg border border-white/12 px-3 py-2 text-xs text-[color:var(--kti-text-dim)] hover:bg-white/[0.06]">{t("media.delete")}</button>
      ) : null}
      <MediaPicker open={open} onOpenChange={setOpen} onSelect={(a) => onChange(a.url)} kind="image" />
    </div>
  );
}

function BilingualList({ value, onChange }) {
  const items = Array.isArray(value) ? value : [];
  const setItem = (i, val) => onChange(items.map((it, idx) => (idx === i ? val : it)));
  const removeItem = (i) => onChange(items.filter((_, idx) => idx !== i));
  return (
    <div className="space-y-2">
      {items.map((it, i) => (
        <div key={i} className="flex items-start gap-2">
          <div className="flex-1"><Bilingual value={it} onChange={(v) => setItem(i, v)} /></div>
          <button type="button" onClick={() => removeItem(i)} className="kti-focus mt-5 grid size-8 place-items-center rounded-lg border border-white/12 text-[#ff96aa] hover:bg-[rgba(255,92,122,0.1)]"><Trash2 className="size-3.5" /></button>
        </div>
      ))}
      <button type="button" onClick={() => onChange([...items, { id: "", en: "" }])} className="kti-focus inline-flex items-center gap-1.5 rounded-lg border border-white/12 px-3 py-1.5 text-xs text-white hover:bg-white/[0.06]"><Plus className="size-3.5" /> Add</button>
    </div>
  );
}

// Renders one sub-field inside an object-list item. Only "bilingual" and "text"
// are used by itemFields, so no recursion into the main switch is needed.
function ItemField({ type, value, onChange }) {
  if (type === "bilingual") return <Bilingual value={value} onChange={onChange} />;
  return <input value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={inputCls} data-testid="cms-item-field" />;
}

function ObjectList({ value, onChange, itemFields, lang }) {
  const items = Array.isArray(value) ? value : [];
  const setField = (i, key, val) => onChange(items.map((it, idx) => (idx === i ? { ...it, [key]: val } : it)));
  const removeItem = (i) => onChange(items.filter((_, idx) => idx !== i));
  const makeEmpty = () => itemFields.reduce((acc, f) => ({ ...acc, [f.name]: f.type === "bilingual" ? { id: "", en: "" } : "" }), {});
  return (
    <div className="space-y-3">
      {items.map((it, i) => (
        <div key={i} className="rounded-xl border border-white/10 bg-white/[0.02] p-3">
          <div className="mb-2 flex items-center justify-between">
            <span className={tagCls}>#{i + 1}</span>
            <button type="button" onClick={() => removeItem(i)} className="kti-focus grid size-7 place-items-center rounded-lg border border-white/12 text-[#ff96aa] hover:bg-[rgba(255,92,122,0.1)]"><Trash2 className="size-3.5" /></button>
          </div>
          <div className="space-y-2">
            {itemFields.map((f) => (
              <div key={f.name}>
                <span className={tagCls}>{fieldLabel(f, lang)}</span>
                <div className="mt-1"><ItemField type={f.type} value={it[f.name]} onChange={(v) => setField(i, f.name, v)} /></div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <button type="button" onClick={() => onChange([...items, makeEmpty()])} className="kti-focus inline-flex items-center gap-1.5 rounded-lg border border-white/12 px-3 py-1.5 text-xs text-white hover:bg-white/[0.06]"><Plus className="size-3.5" /> Add</button>
    </div>
  );
}

export default function FieldInput({ field, value, onChange }) {
  const { i18n } = useTranslation();
  const type = field.type;

  if (type === "bilingual") return <Bilingual value={value} onChange={onChange} />;
  if (type === "bilingual-area") return <Bilingual value={value} onChange={onChange} area />;
  if (type === "number") return <input type="number" value={value ?? ""} onChange={(e) => onChange(e.target.value === "" ? null : Number(e.target.value))} className={inputCls} />;
  if (type === "boolean") return <Switch checked={!!value} onCheckedChange={onChange} />;
  if (type === "tags") return <TagsField value={value} onChange={onChange} />;
  if (type === "media") return <MediaField value={value} onChange={onChange} />;
  if (type === "bilingual-list") return <BilingualList value={value} onChange={onChange} />;
  if (type === "object-list") return <ObjectList value={value} onChange={onChange} itemFields={field.itemFields} lang={i18n.language} />;
  return <input value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={inputCls} />;
}
