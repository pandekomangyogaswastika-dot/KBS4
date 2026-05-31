import "@/i18n";
import "@/App.css";
import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import ScrollToTop from "@/components/ScrollToTop";
import PublicLayout from "@/components/PublicLayout";
import { AuthProvider } from "@/context/AuthContext";
import { NotificationProvider } from "@/context/NotificationContext";
import ProtectedRoute from "@/features/admin/ProtectedRoute";

const HomePage = lazy(() => import("@/features/public/HomePage"));
const ServicesPage = lazy(() => import("@/features/public/pages/ServicesPage"));
const ServiceDetailPage = lazy(() => import("@/features/public/pages/ServiceDetailPage"));
const CasesPage = lazy(() => import("@/features/public/pages/CasesPage"));
const CaseDetailPage = lazy(() => import("@/features/public/pages/CaseDetailPage"));
const TechPage = lazy(() => import("@/features/public/pages/TechPage"));
const TeamPage = lazy(() => import("@/features/public/pages/TeamPage"));
const BlogPage = lazy(() => import("@/features/public/pages/BlogPage"));
const BlogDetailPage = lazy(() => import("@/features/public/pages/BlogDetailPage"));
const CareerPage = lazy(() => import("@/features/public/pages/CareerPage"));
const CareerDetailPage = lazy(() => import("@/features/public/pages/CareerDetailPage"));
const ContactPage = lazy(() => import("@/features/public/pages/ContactPage"));
const PortalComingSoon = lazy(() => import("@/features/portal/PortalComingSoon"));

const LoginPage = lazy(() => import("@/features/portal/auth/LoginPage"));

// Admin / Staff portal
const AdminLayout = lazy(() => import("@/features/admin/AdminLayout"));
const AdminDashboard = lazy(() => import("@/features/admin/pages/AdminDashboard"));
const AdminUsers = lazy(() => import("@/features/admin/pages/AdminUsers"));
const AdminLeads = lazy(() => import("@/features/admin/pages/AdminLeads"));
const MediaLibrary = lazy(() => import("@/features/admin/pages/MediaLibrary"));
const CmsResourcePage = lazy(() => import("@/features/admin/pages/CmsResourcePage"));
const CmsSettings = lazy(() => import("@/features/admin/pages/CmsSettings"));
const AdminAssessments = lazy(() => import("@/features/admin/pages/AdminAssessments"));
const AdminProjects = lazy(() => import("@/features/admin/pages/AdminProjects"));
const StaffMessages = lazy(() => import("@/features/admin/pages/StaffMessages"));
const StaffClients = lazy(() => import("@/features/admin/pages/StaffClients"));
const AdminAiConversations = lazy(() => import("@/features/admin/pages/AdminAiConversations"));
const AdminAnalytics = lazy(() => import("@/features/admin/pages/AdminAnalytics"));
const AdminSeoDashboard = lazy(() => import("@/features/admin/pages/AdminSeoDashboard"));
const AdminIntegrations = lazy(() => import("@/features/admin/pages/AdminIntegrations"));
const AdminEmailOutbox = lazy(() => import("@/features/admin/pages/AdminEmailOutbox"));

// Client portal
const ClientLayout = lazy(() => import("@/features/portal/client/ClientLayout"));
const ClientDashboard = lazy(() => import("@/features/portal/client/ClientDashboard"));
const ClientProjects = lazy(() => import("@/features/portal/client/ClientProjects"));
const ClientProjectDetail = lazy(() => import("@/features/portal/client/ClientProjectDetail"));
const ClientInvoices = lazy(() => import("@/features/portal/client/ClientInvoices"));
const ClientMessages = lazy(() => import("@/features/portal/client/ClientMessages"));
const ClientAssistant = lazy(() => import("@/features/portal/client/ClientAssistant"));

const AssessmentClient = lazy(() => import("@/features/assessment/AssessmentClient"));

function NotFound() {
  return (
    <div className="grid min-h-[70vh] place-items-center px-6 pt-24 text-center">
      <div>
        <div className="font-display text-6xl font-semibold kti-gradient-text">404</div>
        <p className="mt-4 kti-text-dim">Lost in space. Halaman tidak ditemukan.</p>
        <Link to="/" data-testid="notfound-home" className="kti-focus mt-6 inline-block rounded-xl border border-white/15 px-5 py-3 text-sm hover:bg-white/5">Kembali ke Beranda</Link>
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <NotificationProvider>
          <ScrollToTop />
          <Suspense fallback={<div style={{ background: "#05060A", minHeight: "100vh" }} />}>
            <Routes>
              {/* Public site */}
              <Route element={<PublicLayout />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/services" element={<ServicesPage />} />
                <Route path="/services/:slug" element={<ServiceDetailPage />} />
                <Route path="/cases" element={<CasesPage />} />
                <Route path="/cases/:slug" element={<CaseDetailPage />} />
                <Route path="/tech" element={<TechPage />} />
                <Route path="/team" element={<TeamPage />} />
                <Route path="/blog" element={<BlogPage />} />
                <Route path="/blog/:slug" element={<BlogDetailPage />} />
                <Route path="/career" element={<CareerPage />} />
                <Route path="/career/:slug" element={<CareerDetailPage />} />
                <Route path="/contact" element={<ContactPage />} />
                <Route path="*" element={<NotFound />} />
              </Route>

              {/* Auth */}
              <Route path="/portal/login" element={<LoginPage />} />
              <Route path="/portal/coming-soon" element={<PortalComingSoon />} />
              <Route path="/assessment/:token" element={<AssessmentClient />} />

              {/* Admin + Staff portal */}
              <Route
                path="/portal/admin"
                element={(
                  <ProtectedRoute roles={["admin", "staff"]}>
                    <AdminLayout />
                  </ProtectedRoute>
                )}
              >
                <Route index element={<AdminDashboard />} />
                <Route path="leads" element={<AdminLeads />} />
                <Route path="media" element={<MediaLibrary />} />
                <Route path="cms/:resource" element={<CmsResourcePage />} />
                <Route path="settings" element={<CmsSettings />} />
                <Route path="assessments" element={<AdminAssessments />} />
                <Route path="projects" element={<AdminProjects />} />
                <Route path="messages" element={<StaffMessages />} />
                <Route path="clients" element={<StaffClients />} />
                <Route path="ai-conversations" element={<AdminAiConversations />} />
                <Route path="analytics" element={<AdminAnalytics />} />
                <Route path="seo" element={<AdminSeoDashboard />} />
                <Route
                  path="settings/integrations"
                  element={(
                    <ProtectedRoute roles={["admin"]}>
                      <AdminIntegrations />
                    </ProtectedRoute>
                  )}
                />
                <Route path="settings/email-outbox" element={<AdminEmailOutbox />} />
                <Route
                  path="users"
                  element={(
                    <ProtectedRoute roles={["admin"]}>
                      <AdminUsers />
                    </ProtectedRoute>
                  )}
                />
              </Route>

              {/* Client portal */}
              <Route
                path="/portal"
                element={(
                  <ProtectedRoute roles={["client"]}>
                    <ClientLayout />
                  </ProtectedRoute>
                )}
              >
                <Route index element={<Navigate to="/portal/dashboard" replace />} />
                <Route path="dashboard" element={<ClientDashboard />} />
                <Route path="projects" element={<ClientProjects />} />
                <Route path="projects/:id" element={<ClientProjectDetail />} />
                <Route path="invoices" element={<ClientInvoices />} />
                <Route path="messages" element={<ClientMessages />} />
                <Route path="assistant" element={<ClientAssistant />} />
              </Route>
            </Routes>
          </Suspense>
          </NotificationProvider>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
