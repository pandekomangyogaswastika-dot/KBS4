import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Loader2 } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import FieldInput from "@/features/admin/cms/FieldInput";
import { fieldLabel } from "@/features/admin/cms/schemas";
import { getPath, setPath } from "@/features/admin/cms/objectPath";

const tag = "mb-1 block text-xs font-medium text-[color:var(--kti-text-dim)]";

export default function ResourceForm({ fields, initial, onSubmit, busy, showStatus = true, submitLabel }) {
  const { t, i18n } = useTranslation();
  const [form, setForm] = useState(() => initial || {});
  const update = (path, val) => setForm((f) => setPath(f, path, val));

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        {fields.map((f) => (
          <div key={f.name} className={f.half ? "sm:col-span-1" : "sm:col-span-2"}>
            <label className={tag}>{fieldLabel(f, i18n.language)}{f.required ? " *" : ""}</label>
            <FieldInput field={f} value={getPath(form, f.name)} onChange={(v) => update(f.name, v)} />
          </div>
        ))}
      </div>

      {showStatus && (
        <div className="flex items-center justify-between rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3">
          <span className="text-sm text-white">{t("cms.published")}</span>
          <Switch checked={form.status === "published"} onCheckedChange={(v) => update("status", v ? "published" : "draft")} data-testid="cms-status-switch" />
        </div>
      )}

      <div className="flex justify-end pt-1">
        <button type="submit" disabled={busy} data-testid="cms-save-button" className="kti-focus inline-flex items-center justify-center gap-2 rounded-full border border-[rgba(124,104,225,0.45)] bg-[rgba(124,104,225,0.2)] px-6 py-2.5 text-sm font-semibold text-white hover:bg-[rgba(124,104,225,0.3)] disabled:opacity-60">
          {busy && <Loader2 className="size-4 animate-spin" />} {submitLabel || t("cms.save")}
        </button>
      </div>
    </form>
  );
}
