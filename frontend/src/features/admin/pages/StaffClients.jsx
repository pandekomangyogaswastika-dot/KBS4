import { useTranslation } from "react-i18next";
import { Loader2, AlertCircle, Building2 } from "lucide-react";
import { useFetch } from "@/lib/apiClient";

export default function StaffClients() {
  const { t } = useTranslation();
  const { data: users, loading, error } = useFetch("/admin/users", []);

  const clients = (users || []).filter((u) => u.role === "client");

  if (loading) return <div className="flex min-h-[60vh] items-center justify-center"><Loader2 className="size-8 animate-spin" style={{ color: "var(--kti-indigo)" }} /></div>;
  if (error) return <div className="flex min-h-[40vh] items-center justify-center gap-3"><AlertCircle className="size-8" style={{ color: "#E05555" }} /><p>{error}</p></div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-2xl font-semibold text-white">Daftar Klien</h1>
        <p className="mt-1 text-sm text-[color:var(--kti-text-dim)]">{clients.length} klien terdaftar</p>
      </div>

      {clients.length === 0 ? (
        <div className="flex flex-col items-center gap-4 rounded-2xl border border-white/8 bg-white/[0.03] py-20">
          <Building2 className="size-12" style={{ color: "var(--kti-text-faint)" }} />
          <p className="text-sm text-[color:var(--kti-text-dim)]">{t("portal.noClients")}</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {clients.map((c) => (
            <div key={c.id} className="rounded-2xl border border-white/8 bg-white/[0.04] p-5">
              <div className="mb-3 flex items-center gap-3">
                <div className="grid size-10 place-items-center rounded-full border border-white/15 bg-[rgba(124,104,225,0.18)] text-sm font-bold text-white">{c.name[0]}</div>
                <div>
                  <p className="font-semibold text-white">{c.name}</p>
                  <p className="text-xs text-[color:var(--kti-text-dim)]">{c.email}</p>
                </div>
              </div>
              <div className="space-y-1 text-xs">
                {c.company && <p className="text-[color:var(--kti-text-dim)]"><span className="text-[color:var(--kti-text-faint)]">Perusahaan:</span> {c.company}</p>}
                {c.phone && <p className="text-[color:var(--kti-text-dim)]"><span className="text-[color:var(--kti-text-faint)]">Telepon:</span> {c.phone}</p>}
                <p>
                  <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium ${ c.status === "active" ? "bg-[rgba(78,203,175,0.15)] text-[#4ECBAF]" : "bg-white/8 text-[color:var(--kti-text-dim)]" }`}>
                    {c.status === "active" ? "Aktif" : "Nonaktif"}
                  </span>
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
