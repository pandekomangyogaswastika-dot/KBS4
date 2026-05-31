import { useTranslation } from "react-i18next";
import { useFetch } from "@/lib/apiClient";
import PageHeader from "@/components/PageHeader";
import ServicesGrid from "@/features/public/blocks/ServicesGrid";
import { ErrorView, EmptyView } from "@/components/StateViews";
import { ServicesGridSkeleton } from "@/components/SkeletonLoaders";
import SEOHead from "@/components/SEOHead";

export default function ServicesPage() {
  const { t } = useTranslation();
  const { data, loading, error, reload } = useFetch("/services");
  
  return (
    <div data-testid="services-page">
      <SEOHead
        title={t("nav.services")}
        description="Layanan teknologi enterprise lengkap dari KTI: konsultasi IT, software development, cloud infrastructure, sistem integrasi, dan transformasi digital untuk bisnis Anda."
        type="website"
      />
      <PageHeader eyebrow={t("sections.constellations")} title={t("nav.services")} intro={t("pages.servicesIntro")} />
      <div className="kti-container pb-24">
        {loading && <ServicesGridSkeleton count={6} />}
        {error && <ErrorView message={error} onRetry={reload} />}
        {!loading && !error && (data?.length ? <ServicesGrid items={data} /> : <EmptyView />)}
      </div>
    </div>
  );
}
