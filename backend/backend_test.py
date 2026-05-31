"""
Phase 16 Backend Testing: Demo Sandbox Engine
Tests demo session creation, KN3 WMS endpoints, and data seeding.

Tests:
- POST /api/demo/sessions (creates session with 11 products, 3 warehouses, 5 orders)
- GET /api/demo/sessions/{id} (validates active session, returns remaining_minutes)
- GET /api/demo/kn3/dashboard (returns metrics)
- GET /api/demo/kn3/products (returns list)
- GET /api/demo/kn3/sales-orders (returns orders)
- GET /api/demo/kn3/warehouses (returns 3 warehouses)
- GET /api/demo/kn3/document-templates (returns empty array, not 404)
- GET /api/demo/kn3/admin/permissions (returns matrix)
- DELETE /api/demo/sessions/{id} (cleanup)
"""
import requests
import sys
import time

BASE_URL = "https://dev-context-setup-1.preview.emergentagent.com/api"

class Phase16Tester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session_id = None
        
    def log(self, msg):
        print(f"  {msg}")
    
    def test(self, name, fn):
        """Run a test function and track results."""
        self.tests_run += 1
        print(f"\n🔍 Test {self.tests_run}: {name}")
        try:
            fn()
            self.tests_passed += 1
            print(f"✅ PASSED")
            return True
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            self.failed_tests.append({"name": name, "error": str(e)})
            return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            self.failed_tests.append({"name": name, "error": f"Exception: {e}"})
            return False
    
    def get(self, endpoint, token=None, expected_status=200):
        """GET request helper."""
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        r = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        if expected_status:
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}: {r.text}"
        return r
    
    def post(self, endpoint, data, expected_status=200):
        """POST request helper."""
        r = requests.post(f"{BASE_URL}{endpoint}", json=data)
        if expected_status:
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}: {r.text}"
        return r
    
    def delete(self, endpoint, expected_status=200):
        """DELETE request helper."""
        r = requests.delete(f"{BASE_URL}{endpoint}")
        if expected_status:
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}: {r.text}"
        return r
    
    # ========== PHASE 16: DEMO SESSION CREATION ==========
    
    def test_create_demo_session(self):
        """POST /api/demo/sessions creates session with seeded data."""
        session_data = {
            "name": "Test User",
            "email": "test@demo.com",
            "company": "Test Company",
            "app_slug": "kn3"
        }
        r = self.post("/demo/sessions", session_data, expected_status=201)
        data = r.json()
        
        # Validate response structure
        assert "session_id" in data, "Missing session_id"
        assert "token" in data, "Missing token"
        assert "expires_at" in data, "Missing expires_at"
        assert "ttl_minutes" in data, "Missing ttl_minutes"
        assert "app_slug" in data, "Missing app_slug"
        assert "demo_url" in data, "Missing demo_url"
        assert "seed_summary" in data, "Missing seed_summary"
        
        self.session_id = data["session_id"]
        self.log(f"✓ Session created: {self.session_id}")
        self.log(f"✓ TTL: {data['ttl_minutes']} minutes")
        self.log(f"✓ Demo URL: {data['demo_url']}")
        
        # Validate seed_summary
        seed = data["seed_summary"]
        assert "products" in seed, "Missing products in seed_summary"
        assert "warehouses" in seed, "Missing warehouses in seed_summary"
        assert "orders" in seed, "Missing orders in seed_summary"
        
        # Check expected counts
        assert seed["products"] == 11, f"Expected 11 products, got {seed['products']}"
        assert seed["warehouses"] == 3, f"Expected 3 warehouses, got {seed['warehouses']}"
        assert seed["orders"] == 5, f"Expected 5 orders, got {seed['orders']}"
        
        self.log(f"✓ Seed summary: {seed['products']} products, {seed['warehouses']} warehouses, {seed['orders']} orders")
    
    def test_get_demo_session(self):
        """GET /api/demo/sessions/{id} validates session and returns remaining_minutes."""
        if not self.session_id:
            raise AssertionError("No session_id available (create session first)")
        
        r = self.get(f"/demo/sessions/{self.session_id}", expected_status=200)
        data = r.json()
        
        # Validate response structure
        assert "id" in data, "Missing id"
        assert "name" in data, "Missing name"
        assert "email" in data, "Missing email"
        assert "expires_at" in data, "Missing expires_at"
        assert "remaining_minutes" in data, "Missing remaining_minutes"
        assert "remaining_seconds" in data, "Missing remaining_seconds"
        
        assert data["id"] == self.session_id, "Session ID mismatch"
        assert data["name"] == "Test User", "Name mismatch"
        assert data["email"] == "test@demo.com", "Email mismatch"
        assert isinstance(data["remaining_minutes"], int), "remaining_minutes should be integer"
        assert data["remaining_minutes"] > 0, "remaining_minutes should be positive"
        
        self.log(f"✓ Session validated: {data['id']}")
        self.log(f"✓ Remaining time: {data['remaining_minutes']} minutes ({data['remaining_seconds']} seconds)")
    
    # ========== PHASE 16: KN3 DEMO ENDPOINTS ==========
    
    def test_kn3_dashboard(self):
        """GET /api/demo/kn3/dashboard returns metrics."""
        if not self.session_id:
            raise AssertionError("No session_id available")
        
        r = self.get("/demo/kn3/dashboard", token=self.session_id, expected_status=200)
        data = r.json()
        
        # Dashboard returns nested structure with metrics
        assert "metrics" in data, "Missing metrics in response"
        metrics = data["metrics"]
        
        # Validate metrics structure
        assert "products" in metrics, "Missing products metric"
        assert "warehouses" in metrics, "Missing warehouses metric"
        assert "active_orders" in metrics, "Missing active_orders metric"
        assert "available_qty" in metrics, "Missing available_qty metric"
        assert "reserved_qty" in metrics, "Missing reserved_qty metric"
        
        # Check expected values
        assert metrics["products"] == 11, f"Expected 11 products, got {metrics['products']}"
        assert metrics["warehouses"] == 3, f"Expected 3 warehouses, got {metrics['warehouses']}"
        
        self.log(f"✓ Dashboard metrics: {metrics['products']} products, {metrics['warehouses']} warehouses, {metrics['active_orders']} active orders")
        self.log(f"✓ Inventory: {metrics['available_qty']} available, {metrics['reserved_qty']} reserved")
    
    def test_kn3_products(self):
        """GET /api/demo/kn3/products returns list of products."""
        if not self.session_id:
            raise AssertionError("No session_id available")
        
        r = self.get("/demo/kn3/products", token=self.session_id, expected_status=200)
        data = r.json()
        
        assert isinstance(data, list), "Expected list of products"
        assert len(data) == 11, f"Expected 11 products, got {len(data)}"
        
        # Validate product structure
        if data:
            product = data[0]
            assert "id" in product, "Product missing id"
            assert "name" in product, "Product missing name"
            assert "sku" in product, "Product missing sku"
            self.log(f"✓ Sample product: {product.get('name')} (SKU: {product.get('sku')})")
        
        self.log(f"✓ Got {len(data)} products")
    
    def test_kn3_sales_orders(self):
        """GET /api/demo/kn3/sales-orders returns list of orders."""
        if not self.session_id:
            raise AssertionError("No session_id available")
        
        r = self.get("/demo/kn3/sales-orders", token=self.session_id, expected_status=200)
        data = r.json()
        
        assert isinstance(data, list), "Expected list of orders"
        assert len(data) == 5, f"Expected 5 orders, got {len(data)}"
        
        # Validate order structure
        if data:
            order = data[0]
            assert "id" in order, "Order missing id"
            assert "status" in order, "Order missing status"
            self.log(f"✓ Sample order: {order.get('id')} (status: {order.get('status')})")
        
        self.log(f"✓ Got {len(data)} orders")
    
    def test_kn3_warehouses(self):
        """GET /api/demo/kn3/warehouses returns 3 warehouses."""
        if not self.session_id:
            raise AssertionError("No session_id available")
        
        r = self.get("/demo/kn3/warehouses", token=self.session_id, expected_status=200)
        data = r.json()
        
        assert isinstance(data, list), "Expected list of warehouses"
        assert len(data) == 3, f"Expected 3 warehouses, got {len(data)}"
        
        # Validate warehouse structure
        if data:
            warehouse = data[0]
            assert "id" in warehouse, "Warehouse missing id"
            assert "name" in warehouse, "Warehouse missing name"
            self.log(f"✓ Sample warehouse: {warehouse.get('name')}")
        
        self.log(f"✓ Got {len(data)} warehouses")
    
    def test_kn3_document_templates(self):
        """GET /api/demo/kn3/document-templates returns empty array (not 404)."""
        if not self.session_id:
            raise AssertionError("No session_id available")
        
        r = self.get("/demo/kn3/document-templates", token=self.session_id, expected_status=200)
        data = r.json()
        
        assert isinstance(data, list), "Expected list (array)"
        assert len(data) == 0, f"Expected empty array, got {len(data)} items"
        
        self.log(f"✓ Got empty array (not 404)")
    
    def test_kn3_admin_permissions(self):
        """GET /api/demo/kn3/admin/permissions returns matrix."""
        if not self.session_id:
            raise AssertionError("No session_id available")
        
        r = self.get("/demo/kn3/admin/permissions", token=self.session_id, expected_status=200)
        data = r.json()
        
        assert "matrix" in data, "Missing matrix"
        assert "actions" in data, "Missing actions"
        assert isinstance(data["matrix"], dict), "matrix should be dict"
        assert isinstance(data["actions"], list), "actions should be list"
        
        self.log(f"✓ Got permissions matrix with {len(data['actions'])} actions")
    
    # ========== CLEANUP ==========
    
    def test_delete_demo_session(self):
        """DELETE /api/demo/sessions/{id} cleans up session."""
        if not self.session_id:
            self.log("⚠ No session to delete")
            return
        
        r = self.delete(f"/demo/sessions/{self.session_id}", expected_status=200)
        data = r.json()
        
        assert "deleted" in data, "Missing deleted field"
        assert data["deleted"] == True, "Should return deleted=True"
        assert data["session_id"] == self.session_id, "Session ID mismatch"
        
        self.log(f"✓ Session {self.session_id} deleted")
    
    # ========== RUN ALL TESTS ==========
    
    def run_all(self):
        print("\n" + "="*80)
        print("PHASE 16 BACKEND TESTING: Demo Sandbox Engine")
        print("="*80)
        
        print("\n" + "="*80)
        print("DEMO SESSION MANAGEMENT")
        print("="*80)
        
        self.test("POST /api/demo/sessions (create session with seeded data)", self.test_create_demo_session)
        self.test("GET /api/demo/sessions/{id} (validate session)", self.test_get_demo_session)
        
        print("\n" + "="*80)
        print("KN3 DEMO ENDPOINTS")
        print("="*80)
        
        self.test("GET /api/demo/kn3/dashboard (metrics)", self.test_kn3_dashboard)
        self.test("GET /api/demo/kn3/products (11 products)", self.test_kn3_products)
        self.test("GET /api/demo/kn3/sales-orders (5 orders)", self.test_kn3_sales_orders)
        self.test("GET /api/demo/kn3/warehouses (3 warehouses)", self.test_kn3_warehouses)
        self.test("GET /api/demo/kn3/document-templates (empty array)", self.test_kn3_document_templates)
        self.test("GET /api/demo/kn3/admin/permissions (matrix)", self.test_kn3_admin_permissions)
        
        print("\n" + "="*80)
        print("CLEANUP")
        print("="*80)
        
        self.test("DELETE /api/demo/sessions/{id} (cleanup)", self.test_delete_demo_session)
        
        # Summary
        print("\n" + "="*80)
        print(f"📊 RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS ({len(self.failed_tests)}):")
            for ft in self.failed_tests:
                print(f"  - {ft['name']}")
                print(f"    {ft['error']}")
        print("="*80)
        
        return 0 if self.tests_passed == self.tests_run else 1

if __name__ == "__main__":
    tester = Phase16Tester()
    sys.exit(tester.run_all())
