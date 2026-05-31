/**
 * KN3DemoApp.jsx — Entry point untuk demo WMS Sandbox.
 * Props wired 1:1 seperti KN3 original App.js.
 */
import { useState, useEffect } from "react";
import "./App.css";
import { MetricCard, Sidebar, TopBar } from "./components/CoreWidgets";
import { formatQty } from "./utils/formatters";
import { SalesPortal } from "./features/sales/SalesPortal";
import OrdersView from "./features/orders/OrdersView";
import OperationsView from "./features/wms/OperationsView";
import AdminView from "./features/admin/AdminView";
import DetailDrawer from "./components/DetailDrawer";
import TourMenu from "./components/TourMenu";
import { PAGE_META, GUIDANCE_MAP, buildNavigation } from "./config/navigationConfig";
import { useKN3DemoActions } from "./hooks/useKN3DemoActions";
import ManagerDashboard from "./features/manager/ManagerDashboard";
import PurchaseOrderManagement from "./features/admin/PurchaseOrderManagement";
import EscalationManagement from "./features/manager/EscalationManagement";
import GuidedTour from "./components/GuidedTour";
import DemoBanner from "../../components/DemoBanner";
import {
  Archive, Boxes, Clock3, PackageCheck, Sparkles, Warehouse,
} from "lucide-react";

export default function KN3DemoApp({ sessionId, sessionData, onExit }) {
  const [activeView, setActiveView] = useState("sales");
  const [search, setSearch] = useState("");
  const [data, setData] = useState({ products: [], customers: [], orders: [], warehouses: [], metrics: {} });
  const [movements, setMovements] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [users, setUsers] = useState([]);
  const [uoms, setUoms] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [permissions, setPermissions] = useState({ matrix: {}, actions: [] });
  const [auditLogs, setAuditLogs] = useState([]);
  const [auditFilters, setAuditFilters] = useState({ actor: "", module: "", action: "", date_from: "", date_to: "" });
  const [activeTour, setActiveTour] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [cart, setCart] = useState([]);
  const [breakdown, setBreakdown] = useState(null);
  const [lastDocument, setLastDocument] = useState(null);
  const [lastLabel, setLastLabel] = useState(null);
  const [previewHtml, setPreviewHtml] = useState("");
  const [activeDetail, setActiveDetail] = useState(null);
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);

  const user = {
    id: "demo_admin_01",
    name: sessionData?.name || "Admin Demo",
    email: "admin@demo.wms",
    role: "admin",
  };

  const actions = useKN3DemoActions({
    sessionId, user, auditFilters, selectedCustomer, selectedAddress, cart, data,
    setActiveView, setNotice, setData, setTemplates, setUoms,
    setMovements, setTasks, setUsers, setPermissions, setAuditLogs,
    setSelectedCustomer, setSelectedAddress, setSelectedProduct, setBreakdown,
    setCart, setLastDocument, setLastLabel, setPreviewHtml,
    setActiveDetail, setLoading,
  });

  // Auto-init saat mount
  useEffect(() => {
    if (sessionId && !initialized) {
      actions.initDemo().then(() => setInitialized(true));
    }
  }, [sessionId]); // eslint-disable-line

  const metrics = data.metrics || {};
  const navItems = buildNavigation(user.role);
  const pageMeta = PAGE_META[activeView] || { kicker: "Workspace", title: "Smart WMS Demo" };

  const renderView = () => {
    switch (activeView) {
      case "sales":
        return (
          <SalesPortal
            data={data}
            selectedProduct={selectedProduct}
            breakdown={breakdown}
            onInspect={setSelectedProduct}
            onAdd={actions.addToCart}
            cart={cart}
            setCart={setCart}
            selectedCustomer={selectedCustomer}
            setSelectedCustomer={(c) => {
              setSelectedCustomer(c);
              setSelectedAddress(c?.addresses?.[0] || null);
            }}
            selectedAddress={selectedAddress}
            setSelectedAddress={setSelectedAddress}
            onCreateCustomer={actions.createCustomer}
            onSubmitOrder={actions.saveOrder}
            search={search}
            setSearch={setSearch}
            onShowDetail={setActiveDetail}
          />
        );
      case "orders":
        return (
          <OrdersView
            orders={data.orders || []}
            onShowDetail={setActiveDetail}
            onApprove={actions.approveOrder}
            onConfirm={actions.confirmOrder}
            onCancel={actions.cancelOrder}
            onPay={() => setNotice("Simulasi pembayaran diproses.")}
            onGenerateDocument={() => setNotice("Dokumen dibuat.")}
            onReleaseReservation={() => setNotice("Reservasi dirilis.")}
          />
        );
      case "operations":
        return (
          <OperationsView
            data={data}
            movements={movements}
            tasks={tasks}
            onGenerateLabel={() => setNotice("Label digenerate.")}
            onCreateInboundTask={actions.receiveInbound}
            onCreateOutboundTasks={actions.pickOutbound}
            onScanTask={actions.scanTask}
            onAdvanceTask={actions.completeTask}
            onShowDetail={setActiveDetail}
            token={sessionId}
            user={user}
          />
        );
      case "admin":
        return (
          <AdminView
            data={data}
            users={users}
            uoms={uoms}
            templates={templates}
            permissions={permissions}
            previewHtml={previewHtml}
            auditLogs={auditLogs}
            auditFilters={auditFilters}
            setAuditFilters={setAuditFilters}
            onAdminCreate={() => setNotice("Item dibuat.")}
            onAdminPatch={() => setNotice("Item diperbarui.")}
            onAdminDelete={() => setNotice("Item dihapus.")}
            onImportMaster={() => {}}
            onExportMaster={() => {}}
            onUpdatePermissions={actions.updatePermissions}
            onPreviewTemplate={() => {}}
            onRefreshAudit={actions.loadAuditLogs}
            onShowDetail={setActiveDetail}
            onSeedDemo={actions.initDemo}
          />
        );
      case "manager":
        return <ManagerDashboard token={sessionId} />;
      case "po_management":
        return <PurchaseOrderManagement user={user} />;
      case "escalation":
        return <EscalationManagement user={user} />;
      default:
        return (
          <SalesPortal
            data={data}
            selectedProduct={selectedProduct}
            breakdown={breakdown}
            onInspect={setSelectedProduct}
            onAdd={actions.addToCart}
            cart={cart}
            setCart={setCart}
            selectedCustomer={selectedCustomer}
            setSelectedCustomer={setSelectedCustomer}
            selectedAddress={selectedAddress}
            setSelectedAddress={setSelectedAddress}
            onCreateCustomer={actions.createCustomer}
            onSubmitOrder={actions.saveOrder}
            search={search}
            setSearch={setSearch}
            onShowDetail={setActiveDetail}
          />
        );
    }
  };

  return (
    <div className="flex flex-col h-screen bg-neutral-950 font-sans overflow-hidden">
      {/* Demo Banner */}
      <DemoBanner sessionId={sessionId} sessionData={sessionData} onExit={onExit} />

      {/* KN3 App Shell */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          navItems={navItems}
          activeView={activeView}
          onNav={setActiveView}
          user={user}
          onLogout={onExit}
        />
        <div className="flex-1 flex flex-col min-w-0">
          <TopBar
            user={user}
            activeView={activeView}
            pageMeta={pageMeta}
            notice={notice}
            onClearNotice={() => setNotice("")}
            onLogout={onExit}
          />
          {/* Metric Bar */}
          <div className="flex gap-2 px-4 py-2 border-b border-neutral-800 flex-wrap items-center">
            <MetricCard label="Produk" value={metrics.products ?? 0}
              icon={Boxes}
              onClick={() => setActiveView("sales")} />
            <MetricCard label="Available" value={formatQty(metrics.available_qty ?? 0)}
              icon={PackageCheck}
              onClick={() => setActiveView("sales")} />
            <MetricCard label="Reserved" value={formatQty(metrics.reserved_qty ?? 0)}
              icon={Clock3}
              onClick={() => setActiveView("orders")} />
            <MetricCard label="Orders Aktif" value={metrics.active_orders ?? 0}
              icon={Archive}
              onClick={() => setActiveView("orders")} />
            <MetricCard label="Gudang" value={metrics.warehouses ?? 0}
              icon={Warehouse}
              onClick={() => setActiveView("operations")} />
            {activeTour === null && initialized && (
              <button
                data-testid="demo-start-tour"
                onClick={() => setActiveTour("sales")}
                className="ml-auto flex items-center gap-1 px-2 py-1 text-xs bg-indigo-900/60 hover:bg-indigo-800 text-indigo-300 rounded border border-indigo-700 transition-colors"
              >
                <Sparkles className="w-3 h-3" /> Mulai Guided Tour
              </button>
            )}
          </div>
          {/* Main content */}
          <div className="flex-1 overflow-auto">
            {initialized ? renderView() : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
                  <p className="text-neutral-400 text-sm">Menyiapkan demo sandbox...</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Detail Drawer */}
      {activeDetail && (
        <DetailDrawer detail={activeDetail} onClose={() => setActiveDetail(null)} />
      )}

      {/* Guided Tour */}
      {activeTour && (
        <GuidedTour
          tourKey={activeTour}
          onClose={() => setActiveTour(null)}
          onNavigate={setActiveView}
        />
      )}

      {/* Tour Menu */}
      <TourMenu user={user} onStartTour={(key) => setActiveTour(key)} activeTour={activeTour} />
    </div>
  );
}
