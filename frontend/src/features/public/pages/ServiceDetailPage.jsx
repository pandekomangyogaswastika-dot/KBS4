import { Link, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ArrowLeft } from "lucide-react";
import { useFetch } from "@/lib/apiClient";
import { useContentLocale } from "@/lib/useContentLocale";
import PageHeader from "@/components/PageHeader";
import { LoadingView, ErrorView } from "@/components/StateViews";
import { GlassPillButton } from "@/components/kti/GlassPillButton";
import { TwoToneHeading } from "@/components/kti/TwoToneHeading";
import SEOHead, { createServiceSchema } from "@/components/SEOHead";

const GLASS =
  "rounded-[var(--kti-radius-card)] border border-white/10 bg-white/[0.05] backdrop-blur-xl shadow-[0_18px_60px_rgba(0,0,0,0.55)]";

export default function ServiceDetailPage() {
  const { slug } = useParams();
  const { t } = useTranslation();
  const { L } = useContentLocale();
  const { data, loading, error, reload } = useFetch(`/services/${slug}`, [slug]);

  if (loading) return <div className="pt-36"><LoadingView /></div>;
  if (error || !data) return <div className="pt-36"><ErrorView message={error} onRetry={reload} /></div>;

  const schema = createServiceSchema(data);

  return (
    <div data-testid="service-detail-page">
      <SEOHead
        title={L(data.title)}
        description={L(data.summary) || L(data.description)?.substring(0, 160)}
        type="website"
        schema={schema}
      />
      <PageHeader eyebrow={t("sections.constellations")} title={L(data.title)} intro={L(data.summary)} />
      <div className="kti-container pb-24">
        <Link to="/services" data-testid="service-back-link" className="kti-focus mb-8 inline-flex items-center gap-2 text-sm kti-text-dim transition-colors hover:text-white">
          <ArrowLeft className="h-4 w-4" /> {t("nav.services")}
        </Link>
        <div className={`${GLASS} p-6 sm:p-10`}>
          <p className="text-base leading-relaxed text-[color:var(--kti-text-strong)] sm:text-lg">{L(data.description)}</p>
        </div>
        <div className={`mt-10 flex flex-col items-center gap-5 ${GLASS} p-10 text-center kti-glow-mix`}>
          <TwoToneHeading as="h3" className="text-2xl sm:text-3xl" strong={t("pages.relatedCta")} />
          <GlassPillButton as={Link} to="/contact" data-testid="service-contact-cta">
            {t("common.getStarted")}
          </GlassPillButton>
        </div>
      </div>
    </div>
  );
}
