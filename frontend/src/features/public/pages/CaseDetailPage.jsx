import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ArrowLeft, PlayCircle } from "lucide-react";
import { useFetch } from "@/lib/apiClient";
import { useContentLocale } from "@/lib/useContentLocale";
import { PlanetOrb } from "@/components/decor";
import PageHeader from "@/components/PageHeader";
import { LoadingView, ErrorView } from "@/components/StateViews";
import { GlassPillButton } from "@/components/kti/GlassPillButton";
import { TwoToneHeading } from "@/components/kti/TwoToneHeading";
import SEOHead from "@/components/SEOHead";
import DemoGateForm from "@/components/DemoGateForm";

const GLASS =
  "rounded-[var(--kti-radius-card)] border border-white/10 bg-white/[0.05] backdrop-blur-xl shadow-[0_18px_60px_rgba(0,0,0,0.55)]";

function Block({ label, text }) {
  if (!text) return null;
  return (
    <div className={`${GLASS} p-6 sm:p-7`}>
      <div className="kti-eyebrow mb-3">{label}</div>
      <p className="text-base leading-relaxed text-[color:var(--kti-text-strong)]">{text}</p>
    </div>
  );
}

export default function CaseDetailPage() {
  const { slug } = useParams();
  const { t } = useTranslation();
  const { L } = useContentLocale();
  const { data, loading, error, reload } = useFetch(`/cases/${slug}`, [slug]);
  const [showDemoGate, setShowDemoGate] = useState(false);

  if (loading) return <div className="pt-36"><LoadingView /></div>;
  if (error || !data) return <div className="pt-36"><ErrorView message={error} onRetry={reload} /></div>;

  return (
    <div data-testid="case-detail-page">
      <SEOHead
        title={`${L(data.title)} - ${data.client_name}`}
        description={L(data.summary) || L(data.challenge)?.substring(0, 160)}
        type="article"
      />
      <PageHeader eyebrow={L(data.industry)} title={L(data.title)} intro={L(data.summary)} />
      <div className="kti-container pb-24">
        <Link to="/cases" data-testid="case-back-link" className="kti-focus mb-8 inline-flex items-center gap-2 text-sm kti-text-dim transition-colors hover:text-white">
          <ArrowLeft className="h-4 w-4" /> {t("nav.cases")}
        </Link>

        <div className={`mb-10 flex flex-col items-center gap-6 ${GLASS} p-8 sm:flex-row`}>
          <PlanetOrb variant={data.cover || "planet-indigo"} size={120} />
          <div>
            <p className="font-hud text-xs uppercase tracking-[0.25em] kti-text-dim">{data.client_name}</p>
            <h2 className="mt-2 font-display text-2xl font-semibold">{L(data.title)}</h2>
          </div>
        </div>

        {data.results?.length > 0 && (
          <div className="mb-10 grid grid-cols-1 gap-4 sm:grid-cols-3" data-testid="case-results">
            {data.results.map((r, i) => (
              <div key={i} className={`${GLASS} p-6 text-center`}>
                <div className="font-display text-3xl font-semibold kti-gradient-text">{r.value}</div>
                <div className="mt-2 text-xs kti-text-dim">{L(r.label)}</div>
              </div>
            ))}
          </div>
        )}

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
          <Block label={t("pages.challenge")} text={L(data.challenge)} />
          <Block label={t("pages.approach")} text={L(data.approach)} />
          <Block label={t("pages.solution")} text={L(data.solution)} />
          <Block label={t("pages.impact")} text={L(data.impact)} />
        </div>

        {data.tech?.length > 0 && (
          <div className="mt-10">
            <div className="kti-eyebrow mb-3">{t("pages.techUsed")}</div>
            <div className="flex flex-wrap gap-2">
              {data.tech.map((tech) => (
                <span key={tech} className="rounded-lg border border-white/10 bg-white/[0.05] px-3 py-1.5 text-sm" style={{ color: "#cfd4ea" }}>{tech}</span>
              ))}
            </div>
          </div>
        )}

        <div className={`mt-12 flex flex-col items-center gap-5 ${GLASS} p-10 text-center kti-glow-mix`}>
          {/* Demo CTA — tampil jika case punya demo */}
          {data.demo_enabled && data.demo_slug && (
            <div className="mb-4 w-full flex flex-col items-center gap-3">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-900/60 border border-indigo-700/50 text-xs text-indigo-300 font-medium mb-1">
                <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                Demo Interaktif Tersedia
              </div>
              <p className="text-sm text-neutral-400 max-w-sm">
                Coba langsung simulasi{" "}
                <span className="text-white font-medium">{data.demo_label_id || L(data.title)}</span>{" "}
                — data sandbox terisolasi, 90 menit akses penuh.
              </p>
              <button
                data-testid="case-demo-cta"
                onClick={() => setShowDemoGate(true)}
                className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-colors shadow-lg shadow-indigo-900/40"
              >
                <PlayCircle className="w-5 h-5" />
                {data.demo_label_id || "Coba Demo Gratis"}
              </button>
            </div>
          )}

          <TwoToneHeading as="h3" className="text-2xl sm:text-3xl" strong={t("pages.relatedCta")} />
          <GlassPillButton as={Link} to="/contact" data-testid="case-contact-cta">
            {t("common.getStarted")}
          </GlassPillButton>
        </div>

        {/* Gate Form Modal */}
        {showDemoGate && (
          <DemoGateForm
            caseTitle={L(data.title)}
            appSlug={data.demo_slug || "kn3"}
            onClose={() => setShowDemoGate(false)}
          />
        )}
      </div>
    </div>
  );
}
