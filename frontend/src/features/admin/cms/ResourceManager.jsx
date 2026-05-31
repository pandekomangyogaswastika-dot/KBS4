import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { toast } from "sonner";
import { Plus, Pencil, Trash2, ArrowUp, ArrowDown, Eye, EyeOff } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { api, apiError } from "@/lib/apiClient";
import { LoadingView, ErrorView, EmptyView } from "@/components/StateViews";
import ResourceForm from "@/features/admin/cms/ResourceForm";
import { RESOURCE_SCHEMAS, fieldLabel } from "@/features/admin/cms/schemas";
import { getPath } from "@/features/admin/cms/objectPath";
import { CMS } from "@/constants/testIds";

function displayPrimary(item, schema, lang) {
  const v = getPath(item, schema.primary);
  if (v && typeof v === "object") return (lang.startsWith("en") ? v.en : v.id) || v.id || v.en || "(untitled)";
  return v || item.name || item.slug || item.key || "(untitled)";
}

export default function ResourceManager({ resource }) {
  const { t, i18n } = useTranslation();
  const schema = RESOURCE_SCHEMAS[resource];
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editing, setEditing] = useState(null); // item object or {} (new)
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const res = await api.get(`/admin/cms/${resource}`);
      setItems(res.data?.data || []);
    } catch (err) {
      setError(apiError(err, t("cms.loadError")));
    } finally { setLoading(false); }
  }, [resource, t]);

  useEffect(() => { load(); }, [load]);

  const save = async (form) => {
    setBusy(true);
    try {
      if (editing && editing.id) {
        await api.patch(`/admin/cms/${resource}/${editing.id}`, form);
        toast.success(t("cms.saved"));
      } else {
        await api.post(`/admin/cms/${resource}`, form);
        toast.success(t("cms.created"));
      }
      setEditing(null);
      load();
    } catch (err) {
      toast.error(apiError(err));
    } finally { setBusy(false); }
  };

  const togglePublish = async (item) => {
    const action = item.status === "published" ? "unpublish" : "publish";
    try {
      await api.post(`/admin/cms/${resource}/${item.id}/${action}`);
      load();
    } catch (err) { toast.error(apiError(err)); }
  };

  const remove = async (item) => {
    try {
      await api.delete(`/admin/cms/${resource}/${item.id}`);
      toast.success(t("cms.deleted"));
      load();
    } catch (err) { toast.error(apiError(err)); }
  };

  const move = async (index, dir) => {
    const target = index + dir;
    if (target < 0 || target >= items.length) return;
    const next = [...items];
    [next[index], next[target]] = [next[target], next[index]];
    setItems(next);
    try {
      await api.post(`/admin/cms/${resource}/reorder`, { ids: next.map((x) => x.id) });
    } catch (err) { toast.error(apiError(err)); load(); }
  };

  if (!schema) return <ErrorView message={`Unknown resource: ${resource}`} />;

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-display text-2xl font-semibold text-white sm:text-3xl">{fieldLabel({ label: schema.label }, i18n.language)}</h1>
        <button onClick={() => setEditing({})} data-testid={CMS.addButton} className="kti-focus inline-flex items-center gap-2 rounded-full border border-[rgba(124,104,225,0.45)] bg-[rgba(124,104,225,0.2)] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[rgba(124,104,225,0.3)]">
          <Plus className="size-4" /> {t("cms.add")}
        </button>
      </div>

      <div className="overflow-hidden rounded-[var(--kti-radius-card)] border border-white/10 bg-white/[0.04]">
        {loading ? <LoadingView /> : error ? <ErrorView message={error} onRetry={load} /> : items.length === 0 ? <EmptyView message={t("cms.empty")} /> : (
          <Table data-testid={CMS.table}>
            <TableHeader>
              <TableRow className="border-white/8 hover:bg-transparent">
                <TableHead className="w-20 text-white/70">{t("cms.order")}</TableHead>
                <TableHead className="text-white/70">{fieldLabel({ label: schema.label }, i18n.language)}</TableHead>
                <TableHead className="text-white/70">{t("cms.status")}</TableHead>
                <TableHead className="text-right text-white/70">{t("cms.actions")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((item, idx) => (
                <TableRow key={item.id} className="border-white/8 hover:bg-white/[0.03]">
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <button onClick={() => move(idx, -1)} disabled={idx === 0} data-testid={`${CMS.moveUp}-${idx}`} className="kti-focus grid size-6 place-items-center rounded border border-white/10 text-white/60 disabled:opacity-30 hover:bg-white/[0.06]"><ArrowUp className="size-3" /></button>
                      <button onClick={() => move(idx, 1)} disabled={idx === items.length - 1} data-testid={`${CMS.moveDown}-${idx}`} className="kti-focus grid size-6 place-items-center rounded border border-white/10 text-white/60 disabled:opacity-30 hover:bg-white/[0.06]"><ArrowDown className="size-3" /></button>
                    </div>
                  </TableCell>
                  <TableCell className="font-medium text-white">{displayPrimary(item, schema, i18n.language)}</TableCell>
                  <TableCell>
                    <span className={`inline-flex items-center gap-1.5 text-xs ${item.status === "published" ? "text-[#a9ecd2]" : "text-white/45"}`}>
                      <span className={`size-1.5 rounded-full ${item.status === "published" ? "bg-[#73D1AD]" : "bg-white/30"}`} />
                      {item.status === "published" ? t("cms.published") : t("cms.draft")}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="inline-flex items-center gap-1">
                      <button onClick={() => togglePublish(item)} data-testid={`${CMS.publishToggle}-${item.id}`} title={item.status === "published" ? t("cms.unpublish") : t("cms.publish")} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-white/70 hover:bg-white/[0.06]">{item.status === "published" ? <EyeOff className="size-3.5" /> : <Eye className="size-3.5" />}</button>
                      <button onClick={() => setEditing(item)} data-testid={`${CMS.editButton}-${item.id}`} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-white/70 hover:bg-white/[0.06]"><Pencil className="size-3.5" /></button>
                      <AlertDialog>
                        <AlertDialogTrigger asChild>
                          <button data-testid={`${CMS.deleteButton}-${item.id}`} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-[#ff96aa] hover:bg-[rgba(255,92,122,0.1)]"><Trash2 className="size-3.5" /></button>
                        </AlertDialogTrigger>
                        <AlertDialogContent className="border-white/10" style={{ background: "#0B0D17", color: "#E8EAF2" }}>
                          <AlertDialogHeader><AlertDialogTitle>{t("cms.confirmDelete")}</AlertDialogTitle></AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel className="border-white/12 bg-transparent text-white hover:bg-white/[0.06]">{t("admin.cancel")}</AlertDialogCancel>
                            <AlertDialogAction onClick={() => remove(item)} data-testid={CMS.confirmDeleteButton} className="border border-[rgba(255,92,122,0.4)] bg-[rgba(255,92,122,0.18)] text-white hover:bg-[rgba(255,92,122,0.28)]">{t("cms.delete")}</AlertDialogAction>
                          </AlertDialogFooter>
                        </AlertDialogContent>
                      </AlertDialog>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      <Dialog open={!!editing} onOpenChange={(o) => !o && setEditing(null)}>
        <DialogContent className="max-h-[90vh] max-w-3xl overflow-y-auto border-white/10" style={{ background: "#0B0D17", color: "#E8EAF2" }} data-testid={CMS.formDialog}>
          <DialogHeader><DialogTitle>{editing && editing.id ? t("cms.edit") : `${fieldLabel({ label: schema.label }, i18n.language)} · ${t("cms.new")}`}</DialogTitle></DialogHeader>
          {editing && (
            <ResourceForm
              key={editing.id || "new"}
              fields={schema.fields}
              initial={editing.id ? editing : { status: "draft" }}
              onSubmit={save}
              busy={busy}
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
