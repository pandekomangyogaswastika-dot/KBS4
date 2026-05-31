import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { toast } from "sonner";
import { Plus, Copy, ExternalLink, FileText, Check, Trash2, Loader2, Inbox, Send, Sparkles } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { api, apiError } from "@/lib/apiClient";
import { LoadingView, ErrorView, EmptyView } from "@/components/StateViews";
import { pdfUrl, loc } from "@/features/assessment/assessmentApi";
import { ASSESS } from "@/constants/testIds";

const fieldCls = "kti-focus w-full rounded-xl border border-white/12 bg-white/[0.04] px-3.5 py-2.5 text-sm text-white placeholder:text-white/30";
const labelCls = "mb-1.5 block text-xs font-medium text-[color:var(--kti-text-dim)]";

export default function AdminAssessments() {
  const { t, i18n } = useTranslation();
  const [sessions, setSessions] = useState([]);
  const [stats, setStats] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [form, setForm] = useState({ template_id: "", client_name: "", project_name: "", contact_person: "", contact_email: "" });
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const [s, st] = await Promise.all([api.get("/assessment/sessions"), api.get("/assessment/stats")]);
      setSessions(s.data?.data || []);
      setStats(st.data?.data || null);
    } catch (err) { setError(apiError(err, t("admin.loadError"))); }
    finally { setLoading(false); }
  }, [t]);

  const loadTemplates = useCallback(async () => {
    try {
      const res = await api.get("/assessment/templates");
      const list = res.data?.data || [];
      setTemplates(list);
      if (list[0]) setForm((f) => ({ ...f, template_id: f.template_id || list[0].id }));
    } catch { /* ignore */ }
  }, []);

  useEffect(() => { load(); loadTemplates(); }, [load, loadTemplates]);

  const origin = window.location.origin;
  const copyLink = async (shareUrl) => {
    try { await navigator.clipboard.writeText(origin + shareUrl); toast.success(t("assess.linkCopied")); } catch { /* ignore */ }
  };

  const submitCreate = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      const res = await api.post("/assessment/sessions", form);
      const created = res.data?.data;
      toast.success(t("assess.linkCreated"));
      setCreateOpen(false);
      setForm({ template_id: templates[0]?.id || "", client_name: "", project_name: "", contact_person: "", contact_email: "" });
      load();
      if (created?.share_url) {
        try { await navigator.clipboard.writeText(origin + created.share_url); toast.success(t("assess.linkCopied")); } catch { /* ignore */ }
      }
    } catch (err) { toast.error(apiError(err)); }
    finally { setBusy(false); }
  };

  const acknowledge = async (id) => {
    try { await api.post(`/assessment/sessions/${id}/acknowledge`); load(); } catch (err) { toast.error(apiError(err)); }
  };
  const remove = async (id) => {
    try { await api.delete(`/assessment/sessions/${id}`); toast.success(t("assess.delete")); load(); } catch (err) { toast.error(apiError(err)); }
  };

  const statCards = [
    { label: t("assess.totalSessions"), value: stats?.total_sessions ?? 0, icon: Inbox },
    { label: t("assess.submittedCount"), value: stats?.submitted_sessions ?? 0, icon: Send },
    { label: t("assess.newCount"), value: stats?.new_submissions ?? 0, icon: Sparkles },
  ];

  return (
    <div data-testid={ASSESS.adminPage}>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-display text-2xl font-semibold text-white sm:text-3xl">{t("assess.title")}</h1>
        <Dialog open={createOpen} onOpenChange={setCreateOpen}>
          <DialogTrigger asChild>
            <button data-testid={ASSESS.createBtn} className="kti-focus inline-flex items-center gap-2 rounded-full border border-[rgba(124,104,225,0.45)] bg-[rgba(124,104,225,0.2)] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[rgba(124,104,225,0.3)]"><Plus className="size-4" /> {t("assess.create")}</button>
          </DialogTrigger>
          <DialogContent className="border-white/10" style={{ background: "#0B0D17", color: "#E8EAF2" }}>
            <DialogHeader><DialogTitle>{t("assess.create")}</DialogTitle></DialogHeader>
            <form onSubmit={submitCreate} className="flex flex-col gap-4">
              <div>
                <label className={labelCls}>{t("assess.template")}</label>
                <Select value={form.template_id} onValueChange={(v) => setForm({ ...form, template_id: v })}>
                  <SelectTrigger className="border-white/12 bg-white/[0.04]" data-testid={ASSESS.templateSelect}><SelectValue /></SelectTrigger>
                  <SelectContent>{templates.map((tp) => <SelectItem key={tp.id} value={tp.id}>{loc(tp.name, i18n.language)}</SelectItem>)}</SelectContent>
                </Select>
              </div>
              <div><label className={labelCls}>{t("assess.clientName")} *</label><input required value={form.client_name} onChange={(e) => setForm({ ...form, client_name: e.target.value })} className={fieldCls} data-testid={ASSESS.clientInput} /></div>
              <div className="grid gap-3 sm:grid-cols-2">
                <div><label className={labelCls}>{t("assess.projectName")}</label><input value={form.project_name} onChange={(e) => setForm({ ...form, project_name: e.target.value })} className={fieldCls} /></div>
                <div><label className={labelCls}>{t("assess.contactPerson")}</label><input value={form.contact_person} onChange={(e) => setForm({ ...form, contact_person: e.target.value })} className={fieldCls} /></div>
              </div>
              <div><label className={labelCls}>{t("assess.contactEmail")}</label><input type="email" value={form.contact_email} onChange={(e) => setForm({ ...form, contact_email: e.target.value })} className={fieldCls} /></div>
              <DialogFooter>
                <button type="submit" disabled={busy || !form.template_id} data-testid={ASSESS.createSubmit} className="kti-focus inline-flex items-center justify-center gap-2 rounded-full border border-white/14 bg-white/[0.08] px-5 py-2.5 text-sm font-semibold text-white hover:bg-white/[0.12] disabled:opacity-60">{busy && <Loader2 className="size-4 animate-spin" />} {t("assess.generate")}</button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="mb-6 grid grid-cols-3 gap-4">
        {statCards.map((s) => (
          <div key={s.label} className="rounded-[var(--kti-radius-card)] border border-white/10 bg-white/[0.05] p-4 backdrop-blur-xl">
            <div className="mb-2 flex items-center justify-between"><span className="grid size-8 place-items-center rounded-lg border border-white/12 bg-white/[0.04]"><s.icon className="size-4 text-[#73D1AD]" /></span></div>
            <p className="font-display text-2xl font-semibold text-white">{s.value}</p>
            <p className="text-xs text-[color:var(--kti-text-dim)]">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="overflow-hidden rounded-[var(--kti-radius-card)] border border-white/10 bg-white/[0.04]">
        {loading ? <LoadingView /> : error ? <ErrorView message={error} onRetry={load} /> : sessions.length === 0 ? <EmptyView message={t("assess.noSessions")} /> : (
          <Table>
            <TableHeader>
              <TableRow className="border-white/8 hover:bg-transparent">
                <TableHead className="text-white/70">{t("assess.clientName")}</TableHead>
                <TableHead className="text-white/70">{t("assess.statusDraft")}/{t("assess.statusSubmitted")}</TableHead>
                <TableHead className="text-white/70">Progress</TableHead>
                <TableHead className="text-right text-white/70">{t("admin.actions")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sessions.map((s) => (
                <TableRow key={s.id} className="border-white/8 hover:bg-white/[0.03]">
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-white">{s.client_name}</span>
                      {s.is_new_submission ? <span className="rounded-full border border-[rgba(115,209,173,0.5)] bg-[rgba(115,209,173,0.16)] px-2 py-0.5 text-[9px] font-bold tracking-wider text-[#a9ecd2]">{t("assess.newBadge")}</span> : null}
                    </div>
                    {s.project_name ? <p className="text-xs text-[color:var(--kti-text-dim)]">{s.project_name}</p> : null}
                  </TableCell>
                  <TableCell>
                    <span className={`inline-flex items-center gap-1.5 text-xs ${s.status === "submitted" ? "text-[#a9ecd2]" : "text-white/45"}`}>
                      <span className={`size-1.5 rounded-full ${s.status === "submitted" ? "bg-[#73D1AD]" : "bg-white/30"}`} />
                      {s.status === "submitted" ? t("assess.statusSubmitted") : t("assess.statusDraft")}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="h-1.5 w-24 overflow-hidden rounded-full bg-white/10"><div className="h-full rounded-full bg-gradient-to-r from-[#7C68E1] to-[#73D1AD]" style={{ width: `${s.progress?.percent || 0}%` }} /></div>
                      <span className="text-xs text-[color:var(--kti-text-dim)]">{s.progress?.percent || 0}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="inline-flex items-center gap-1">
                      <button onClick={() => copyLink(s.share_url)} data-testid={`${ASSESS.copyLink}-${s.id}`} title={t("assess.copyLink")} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-white/70 hover:bg-white/[0.06]"><Copy className="size-3.5" /></button>
                      <a href={origin + s.share_url} target="_blank" rel="noreferrer" title={t("assess.open")} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-white/70 hover:bg-white/[0.06]"><ExternalLink className="size-3.5" /></a>
                      <a href={pdfUrl(s.token, i18n.language.startsWith("en") ? "en" : "id")} target="_blank" rel="noreferrer" title={t("assess.exportPdf")} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-white/70 hover:bg-white/[0.06]"><FileText className="size-3.5" /></a>
                      {s.is_new_submission ? <button onClick={() => acknowledge(s.id)} data-testid={`${ASSESS.ackBtn}-${s.id}`} title={t("assess.acknowledge")} className="kti-focus grid size-8 place-items-center rounded-lg border border-[rgba(115,209,173,0.4)] text-[#a9ecd2] hover:bg-[rgba(115,209,173,0.1)]"><Check className="size-3.5" /></button> : null}
                      <AlertDialog>
                        <AlertDialogTrigger asChild>
                          <button data-testid={`${ASSESS.deleteBtn}-${s.id}`} className="kti-focus grid size-8 place-items-center rounded-lg border border-white/10 text-[#ff96aa] hover:bg-[rgba(255,92,122,0.1)]"><Trash2 className="size-3.5" /></button>
                        </AlertDialogTrigger>
                        <AlertDialogContent className="border-white/10" style={{ background: "#0B0D17", color: "#E8EAF2" }}>
                          <AlertDialogHeader><AlertDialogTitle>{t("assess.confirmDelete")}</AlertDialogTitle></AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel className="border-white/12 bg-transparent text-white hover:bg-white/[0.06]">{t("admin.cancel")}</AlertDialogCancel>
                            <AlertDialogAction onClick={() => remove(s.id)} data-testid={ASSESS.confirmDeleteBtn} className="border border-[rgba(255,92,122,0.4)] bg-[rgba(255,92,122,0.18)] text-white hover:bg-[rgba(255,92,122,0.28)]">{t("assess.delete")}</AlertDialogAction>
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
    </div>
  );
}
