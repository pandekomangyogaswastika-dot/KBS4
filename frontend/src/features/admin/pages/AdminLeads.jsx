import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { toast } from "sonner";
import { Search } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { api, apiError } from "@/lib/apiClient";
import { LoadingView, ErrorView, EmptyView } from "@/components/StateViews";
import { LEADS } from "@/constants/testIds";

const STATUSES = ["new", "contacted", "qualified", "won", "lost", "archived"];
const statusTone = {
  new: "text-[#a9ecd2]", contacted: "text-[#cfc4ff]", qualified: "text-[#9fd0ff]",
  won: "text-[#a9ecd2]", lost: "text-[#ff96aa]", archived: "text-white/45",
};
const fieldCls = "kti-focus w-full rounded-xl border border-white/12 bg-white/[0.04] px-3.5 py-2.5 text-sm text-white placeholder:text-white/30";

export default function AdminLeads() {
  const { t } = useTranslation();
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const res = await api.get(`/admin/leads?limit=100&search=${encodeURIComponent(search)}`);
      setLeads(res.data?.data || []);
    } catch (err) {
      setError(apiError(err, t("admin.loadError")));
    } finally { setLoading(false); }
  }, [search, t]);

  useEffect(() => { load(); }, [load]);

  const updateStatus = async (lead, status) => {
    const prev = leads;
    setLeads((ls) => ls.map((l) => (l.id === lead.id ? { ...l, status } : l)));
    try {
      await api.patch(`/admin/leads/${lead.id}`, { status });
      toast.success(t("admin.saved"));
    } catch (err) {
      setLeads(prev);
      toast.error(apiError(err));
    }
  };

  const fmtDate = (iso) => { try { return new Date(iso).toLocaleDateString(); } catch { return iso; } };

  return (
    <div>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-semibold text-white sm:text-3xl">{t("admin.leads")}</h1>
      </div>

      <div className="mb-4 relative max-w-xs">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-white/40" />
        <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder={t("admin.search")} data-testid={LEADS.searchInput} className={`${fieldCls} pl-9`} />
      </div>

      <div className="overflow-hidden rounded-[var(--kti-radius-card)] border border-white/10 bg-white/[0.04]">
        {loading ? <LoadingView /> : error ? <ErrorView message={error} onRetry={load} /> : leads.length === 0 ? <EmptyView message={t("admin.noLeads")} /> : (
          <Table data-testid={LEADS.table}>
            <TableHeader>
              <TableRow className="border-white/8 hover:bg-transparent">
                <TableHead className="text-white/70">{t("admin.leadName")}</TableHead>
                <TableHead className="text-white/70">{t("admin.email")}</TableHead>
                <TableHead className="text-white/70">{t("admin.company")}</TableHead>
                <TableHead className="text-white/70">{t("admin.leadDate")}</TableHead>
                <TableHead className="text-white/70">{t("admin.leadStatus")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {leads.map((l) => (
                <TableRow key={l.id} className="border-white/8 align-top hover:bg-white/[0.03]">
                  <TableCell>
                    <p className="font-medium text-white">{l.name}</p>
                    {l.message && <p className="mt-0.5 max-w-xs truncate text-xs text-[color:var(--kti-text-dim)]">{l.message}</p>}
                  </TableCell>
                  <TableCell className="text-[color:var(--kti-text-dim)]">{l.email}</TableCell>
                  <TableCell className="text-[color:var(--kti-text-dim)]">{l.company || "—"}</TableCell>
                  <TableCell className="whitespace-nowrap text-xs text-[color:var(--kti-text-dim)]">{fmtDate(l.created_at)}</TableCell>
                  <TableCell>
                    <Select value={l.status} onValueChange={(v) => updateStatus(l, v)}>
                      <SelectTrigger data-testid={`${LEADS.statusSelect}-${l.id}`} className={`h-9 w-36 border-white/12 bg-white/[0.04] ${statusTone[l.status] || ""}`}><SelectValue /></SelectTrigger>
                      <SelectContent>
                        {STATUSES.map((s) => (<SelectItem key={s} value={s}>{t(`admin.status${s.charAt(0).toUpperCase() + s.slice(1)}`)}</SelectItem>))}
                      </SelectContent>
                    </Select>
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
