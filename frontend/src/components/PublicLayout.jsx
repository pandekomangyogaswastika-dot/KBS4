import { Outlet } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { useDeviceCapability } from "@/lib/useDeviceCapability";
import { SmoothScrollProvider } from "@/context/SmoothScroll";
import CustomCursor from "@/components/CustomCursor";
import Preloader from "@/components/Preloader";
import { FloatingPillNavbar } from "@/components/kti/FloatingPillNavbar";
import SiteFooter from "@/components/SiteFooter";
import AIAdvisorWidget from "@/components/AIAdvisorWidget";
import { useFetch } from "@/lib/apiClient";

export default function PublicLayout() {
  const caps = useDeviceCapability();
  const { data: settings } = useFetch("/settings");
  const smooth = caps.ready && !caps.reducedMotion;

  return (
    <SmoothScrollProvider enabled={smooth}>
      <div className="kti-noise relative min-h-screen">
        <Preloader />
        <CustomCursor />
        <FloatingPillNavbar />
        <main>
          <Outlet context={{ settings }} />
        </main>
        <SiteFooter settings={settings} />
        <AIAdvisorWidget />
        <Toaster position="top-center" theme="dark" richColors />
      </div>
    </SmoothScrollProvider>
  );
}
