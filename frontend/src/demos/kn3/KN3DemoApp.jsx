/**
 * KN3DemoApp.jsx — Entry point untuk demo WMS.
 * - Membaca session_id dari URL param (?session=xxx)
 * - Auto-init demo session (no login screen)
 * - Wraps KN3 App with DemoBanner
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
  Archive, Boxes, Building2, Clock3, PackageCheck, Sparkles, Warehouse,
} from "lucide-react";

export default function KN3DemoApp({ sessionId, sessionData, onExit }) {
  const [activeView, setActiveView] = useState("sales");
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
  const [tourAutoStart, setTourAutoStart] = useState(false);
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

  const user = { id: "demo_admin_01", name: sessionData?.name || "Admin Demo", email: "admin@demo.wms", role: "admin" };

  const actions = useKN3DemoActions({
    sessionId,
    user, auditFilters, selectedCustomer, selectedAddress, cart, data,
    setActiveView, setNotice, setData, setTemplates, setUoms,
    setMovements, setTasks, setUsers, setPermissions, setAuditLogs,
    setSelectedCustomer, setSelectedAddress, setSelectedProduct, setBreakdown,
    setCart, setLastDocument, setLastLabel, setPreviewHtml,
    setActiveDetail, setLoading,
  });

  // Auto-init demo saat komponen mount
  useEffect(() => {
    if (sessionId && !initialized) {
      actions.initDemo().then(() => setInitialized(true));
    }
  }, [sessionId]); // eslint-disable-line

  // Auto-start guided tour setelah data loaded
  useEffect(() => {
    if (initialized && tourAutoStart) {
      setActiveTour("sales");
      setTourAutoStart(false);
    }
  }, [initialized, tourAutoStart]);

  const metrics = data.metrics || {};
  const navItems = buildNavigation(user.role) || [];

  const renderView = () => {
    const props = {
      data, products: data.products, customers: data.customers,
      orders: data.orders, warehouses: data.warehouses, movements,
      tasks, users, uoms, templates, permissions, auditLogs, auditFilters,
      user, loading,
      onUpdateAuditFilter: (k, v) => setAuditFilters(p => ({ ...p, [k]: v })),
      setActiveView, setNotice, setActiveDetail,
      onConfirmOrder: actions.confirmOrder,
      onApproveOrder: actions.approveOrder,
      onCancelOrder: actions.cancelOrder,
      onRejectOrder: actions.rejectOrder,
      onUpdateOrderStatus: actions.updateOrderStatus,
      onSaveOrder: actions.saveOrder,
      onDeliverOrder: actions.deliverOrder,
      onCreateProduct: actions.createProduct,
      onUpdateProduct: actions.updateProduct,
      onDeleteProduct: actions.deleteProduct,
      onCreateCustomer: actions.createCustomer,
      onUpdateCustomer: actions.updateCustomer,
      onDeleteCustomer: actions.deleteCustomer,
      onUpdateWarehouse: actions.updateWarehouse,
      onCreateWarehouse: actions.createWarehouse,
      onDeleteWarehouse: actions.deleteWarehouse,
      onScanTask: actions.scanTask,
      onCompleteTask: actions.completeTask,
      onReceiveInbound: actions.receiveInbound,
      onPickOutbound: actions.pickOutbound,
      onUpdatePermissions: actions.updatePermissions,
      onLoadAuditLogs: actions.loadAuditLogs,
      onUpdateUom: actions.updateUom,
      onCreateUom: actions.createUom,
      onAddToCart: actions.addToCart,
      onRemoveFromCart: actions.removeFromCart,
      onClearCart: actions.clearCart,
      onSelectCustomer: (c) => { setSelectedCustomer(c); setSelectedAddress(c?.addresses?.[0] || null); },
      onSelectAddress: setSelectedAddress,
      onSelectProduct: setSelectedProduct,
      onShowBreakdown: setBreakdown,
      onShowDocument: setLastDocument,
      selectedCustomer, selectedAddress, selectedProduct, cart, breakdown,
      lastDocument, lastLabel, previewHtml,
    };
    switch (activeView) {
      case "sales": return <SalesPortal {...props} />;
      case "orders": return <OrdersView {...props} />;
      case "operations": return <OperationsView {...props} />;
      case "admin": return <AdminView {...props} />;
      case "manager": return <ManagerDashboard {...props} />;
      case "po_management": return <PurchaseOrderManagement {...props} />;
      case "escalation": return <EscalationManagement {...props} />;
      default: return <SalesPortal {...props} />;
    }
  };

  return (
    <div className="flex flex-col h-screen bg-neutral-950 font-sans overflow-hidden">
      {/* Demo Banner */}
      <DemoBanner
        sessionId={sessionId}
        sessionData={sessionData}
        onExit={onExit}
      />

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
            pageMeta={PAGE_META}
            notice={notice}
            onClearNotice={() => setNotice("")}
            onLogout={onExit}
          />
          {/* Metric Bar */}
          <div className="flex gap-2 px-4 py-2 border-b border-neutral-800 flex-wrap">
            <MetricCard label="Produk" value={metrics.products ?? 0}
              icon={Boxes}
              onClick={() => actions.showMetricDetail("products")} />
            <MetricCard label="Available" value={formatQty(metrics.available_qty ?? 0)}
              icon={PackageCheck}
              onClick={() => actions.showMetricDetail("available")} />
            <MetricCard label="Reserved" value={formatQty(metrics.reserved_qty ?? 0)}
              icon={Clock3}
              onClick={() => actions.showMetricDetail("reserved")} />
            <MetricCard label="Orders Aktif" value={metrics.active_orders ?? 0}
              icon={Archive}
              onClick={() => actions.showMetricDetail("orders")} />
            <MetricCard label="Gudang" value={metrics.warehouses ?? 0}
              icon={Warehouse}
              onClick={() => actions.showMetricDetail("warehouses")} />
            {activeTour === null && initialized && (
              <button
                onClick={() => setActiveTour("sales")}
                className="ml-auto flex items-center gap-1 px-2 py-1 text-xs bg-indigo-900/60 hover:bg-indigo-800 text-indigo-300 rounded border border-indigo-700 transition-colors"
              >
                <Sparkles className="w-3 h-3" /> Mulai Guided Tour
              </button>
            )}
          </div>
          {/* Main content */}
          <div className="flex-1 overflow-auto">{renderView()}</div>
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
      <TourMenu
        user={user}
        onStartTour={(key) => { setActiveTour(key); }}
        activeTour={activeTour}
      />
    </div>
  );
}
