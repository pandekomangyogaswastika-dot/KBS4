import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";
import { useFetch } from "@/lib/apiClient";
import { ErrorView } from "@/components/StateViews";
import SEOHead from "@/components/SEOHead";

export default function LegalPage() {
  const { i18n } = useTranslation();
  const lang = i18n.language;
  const location = useLocation();
  
  // Extract slug from pathname
  const slug = location.pathname.replace('/', '');
  
  const { data: page, loading, error } = useFetch(`/legal/${slug}`);

  if (loading) {
    return (
      <div className="kti-container py-24">
        <div className="max-w-4xl mx-auto space-y-6 animate-pulse">
          <div className="h-12 bg-white/5 rounded w-2/3" />
          <div className="h-4 bg-white/5 rounded w-1/4" />
          <div className="space-y-3">
            {[1,2,3,4,5,6,7,8].map(i => <div key={i} className="h-4 bg-white/5 rounded" />)}
          </div>
        </div>
      </div>
    );
  }

  if (error || !page) {
    return (
      <div className="kti-container py-24">
        <ErrorView message={error || "Page not found"} />
      </div>
    );
  }

  return (
    <div data-testid="legal-page">
      <SEOHead
        title={lang.startsWith("en") ? page.title.en : page.title.id}
        description={lang.startsWith("en") ? page.title.en : page.title.id}
        type="article"
      />
      
      <div className="kti-container py-24">
        <div className="max-w-4xl mx-auto">
          <h1 className="kti-heading-1 mb-4">
            {lang.startsWith("en") ? page.title.en : page.title.id}
          </h1>
          
          <div className="flex items-center gap-4 text-sm text-white/50 mb-12">
            <span>Version {page.version}</span>
            <span>•</span>
            <span>
              Last updated: {new Date(page.last_updated).toLocaleDateString()}
            </span>
          </div>

          <div
            className="prose prose-invert prose-lg max-w-none"
            dangerouslySetInnerHTML={{
              __html: lang.startsWith("en") ? page.content.en : page.content.id
            }}
          />
        </div>
      </div>
    </div>
  );
}
