import { Link, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ArrowLeft } from "lucide-react";
import { useFetch } from "@/lib/apiClient";
import { useContentLocale } from "@/lib/useContentLocale";
import { PlanetOrb } from "@/components/decor";
import PageHeader from "@/components/PageHeader";
import { LoadingView, ErrorView } from "@/components/StateViews";
import { GlassPillButton } from "@/components/kti/GlassPillButton";
import { TwoToneHeading } from "@/components/kti/TwoToneHeading";
import SEOHead from "@/components/SEOHead";

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
          <TwoToneHeading as="h3" className="text-2xl sm:text-3xl" strong={t("pages.relatedCta")} />
          <GlassPillButton as={Link} to="/contact" data-testid="case-contact-cta">
            {t("common.getStarted")}
          </GlassPillButton>
        </div>
      </div>
    </div>
  );
}
