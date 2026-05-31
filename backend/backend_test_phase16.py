"""
Phase 16 Backend Testing: Demo Sandbox Engine
Tests demo session creation, validation, KN3 WMS demo endpoints, and regression.

Tests:
- NEW: POST /api/demo/sessions (create session with seed data)
- NEW: GET /api/demo/sessions/{id} (validate session)
- NEW: GET /api/demo/kn3/dashboard (WMS metrics with session auth)
- NEW: GET /api/demo/kn3/products (products list)
- NEW: GET /api/demo/kn3/sales-orders (orders list)
- NEW: GET /api/demo/kn3/warehouses (warehouses list)
- NEW: GET /api/demo/sessions (list active sessions - admin only)
- NEW: DELETE /api/demo/sessions/{id} (cleanup)
- REGRESSION: Admin login, public cases still working
"""
import requests
import sys
import time

BASE_URL = "https://dev-context-setup-1.preview.emergentagent.com/api"

class Phase16Tester:
    def __init__(self):
        self.admin_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session_id = None
        self.session_token = None
        
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
    
    def login(self, email, password):
        """Login and return token."""
        r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        assert r.status_code == 200, f"Login failed: {r.status_code} {r.text}"
        data = r.json().get("data", {})
        token = data.get("access_token")
        assert token, "No access_token in response"
        return token
    
    def get(self, endpoint, token=None, expected_status=200):
        """GET request helper."""
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        if expected_status:
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}: {r.text}"
        return r
    
    def post(self, endpoint, data, token=None, expected_status=200):
        """POST request helper."""
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
        if expected_status:
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}: {r.text}"
        return r
    
    def delete(self, endpoint, token=None, expected_status=200):
        """DELETE request helper."""
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        if expected_status:
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}: {r.text}"
        return r
    
    # ========== AUTH SETUP ==========
    
    def test_auth_setup(self):
        """Login as admin."""
        self.log("Logging in as admin...")
        self.admin_token = self.login("admin@kubus.id", "Admin#2026")
        self.log(f"✓ Admin token: {self.admin_token[:20]}...")
    
    # ========== DEMO SESSION TESTS ==========
    
    def test_create_demo_session(self):
        """POST /api/demo/sessions - Create demo session with seed data."""
        self.log("Creating demo session...")
        payload = {
            "name": "Test User Demo",
            "email": "testdemo@example.com",
            "company": "Test Company",
            "app_slug": "kn3"
        }
        r = self.post("/demo/sessions", payload, expected_status=201)
        data = r.json()
        
        # Validate response structure
        assert "session_id" in data, "Missing session_id in response"
        assert "token" in data, "Missing token in response"
        assert "expires_at" in data, "Missing expires_at in response"
        assert "demo_url" in data, "Missing demo_url in response"
        assert "seed_summary" in data, "Missing seed_summary in response"
        
        # Store session info for later tests
        self.session_id = data["session_id"]
        self.session_token = data["token"]
        
        # Validate seed summary
        seed = data["seed_summary"]
        assert seed.get("warehouses") == 3, f"Expected 3 warehouses, got {seed.get('warehouses')}"
        assert seed.get("products") == 11, f"Expected 11 products, got {seed.get('products')}"
        assert seed.get("customers") == 5, f"Expected 5 customers, got {seed.get('customers')}"
        assert seed.get("orders") == 5, f"Expected 5 orders, got {seed.get('orders')}"
        
        self.log(f"✓ Session created: {self.session_id}")
        self.log(f"✓ Seed summary: {seed}")
    
    def test_validate_demo_session(self):
        """GET /api/demo/sessions/{id} - Validate active session."""
        assert self.session_id, "No session_id from previous test"
        self.log(f"Validating session {self.session_id}...")
        
        r = self.get(f"/demo/sessions/{self.session_id}")
        data = r.json()
        
        assert data.get("id") == self.session_id, "Session ID mismatch"
        assert data.get("app_slug") == "kn3", "App slug mismatch"
        assert "remaining_minutes" in data, "Missing remaining_minutes"
        assert "remaining_seconds" in data, "Missing remaining_seconds"
        assert data.get("seeded") == True, "Session not seeded"
        
        self.log(f"✓ Session valid, remaining: {data['remaining_minutes']} minutes")
    
    def test_kn3_dashboard(self):
        """GET /api/demo/kn3/dashboard - Get WMS metrics with session auth."""
        assert self.session_token, "No session token from previous test"
        self.log("Fetching KN3 dashboard...")
        
        r = self.get("/demo/kn3/dashboard", token=self.session_token)
        data = r.json()
        
        # Validate response structure
        assert "metrics" in data, "Missing metrics in response"
        assert "products" in data, "Missing products list"
        assert "orders" in data, "Missing orders list"
        assert "warehouses" in data, "Missing warehouses list"
        assert "customers" in data, "Missing customers list"
        
        metrics = data["metrics"]
        assert metrics.get("products") == 11, f"Expected 11 products, got {metrics.get('products')}"
        assert metrics.get("warehouses") == 3, f"Expected 3 warehouses, got {metrics.get('warehouses')}"
        assert metrics.get("customers") == 5, f"Expected 5 customers, got {metrics.get('customers')}"
        assert "available_qty" in metrics, "Missing available_qty"
        assert "reserved_qty" in metrics, "Missing reserved_qty"
        
        self.log(f"✓ Dashboard metrics: {metrics}")
    
    def test_kn3_products(self):
        """GET /api/demo/kn3/products - Get products list."""
        assert self.session_token, "No session token"
        self.log("Fetching KN3 products...")
        
        r = self.get("/demo/kn3/products", token=self.session_token)
        products = r.json()
        
        assert isinstance(products, list), f"Expected list, got {type(products)}"
        assert len(products) == 11, f"Expected 11 products, got {len(products)}"
        
        # Validate product structure
        product = products[0]
        assert "id" in product, "Product missing id"
        assert "sku" in product, "Product missing sku"
        assert "name" in product, "Product missing name"
        assert "category" in product, "Product missing category"
        
        self.log(f"✓ Found {len(products)} products")
    
    def test_kn3_sales_orders(self):
        """GET /api/demo/kn3/sales-orders - Get orders list."""
        assert self.session_token, "No session token"
        self.log("Fetching KN3 sales orders...")
        
        r = self.get("/demo/kn3/sales-orders", token=self.session_token)
        orders = r.json()
        
        assert isinstance(orders, list), f"Expected list, got {type(orders)}"
        assert len(orders) == 5, f"Expected 5 orders, got {len(orders)}"
        
        # Validate order structure
        order = orders[0]
        assert "id" in order, "Order missing id"
        assert "number" in order, "Order missing number"
        assert "status" in order, "Order missing status"
        assert "customer_name" in order, "Order missing customer_name"
        assert "items" in order, "Order missing items"
        
        self.log(f"✓ Found {len(orders)} orders")
    
    def test_kn3_warehouses(self):
        """GET /api/demo/kn3/warehouses - Get warehouses list."""
        assert self.session_token, "No session token"
        self.log("Fetching KN3 warehouses...")
        
        r = self.get("/demo/kn3/warehouses", token=self.session_token)
        warehouses = r.json()
        
        assert isinstance(warehouses, list), f"Expected list, got {type(warehouses)}"
        assert len(warehouses) == 3, f"Expected 3 warehouses, got {len(warehouses)}"
        
        # Validate warehouse structure
        wh = warehouses[0]
        assert "id" in wh, "Warehouse missing id"
        assert "name" in wh, "Warehouse missing name"
        assert "code" in wh, "Warehouse missing code"
        assert "city" in wh, "Warehouse missing city"
        
        self.log(f"✓ Found {len(warehouses)} warehouses")
    
    def test_list_active_sessions_admin(self):
        """GET /api/demo/sessions - List active sessions (admin only)."""
        assert self.admin_token, "No admin token"
        self.log("Listing active demo sessions (admin)...")
        
        r = self.get("/demo/sessions", token=self.admin_token)
        data = r.json()
        
        assert "active_count" in data, "Missing active_count"
        assert "sessions" in data, "Missing sessions list"
        assert data["active_count"] > 0, "No active sessions found"
        
        self.log(f"✓ Found {data['active_count']} active sessions")
    
    def test_delete_demo_session(self):
        """DELETE /api/demo/sessions/{id} - Cleanup session."""
        assert self.session_id, "No session_id"
        self.log(f"Deleting session {self.session_id}...")
        
        r = self.delete(f"/demo/sessions/{self.session_id}")
        data = r.json()
        
        assert data.get("deleted") == True, "Session not deleted"
        assert data.get("session_id") == self.session_id, "Session ID mismatch"
        
        self.log("✓ Session deleted successfully")
        
        # Verify session is gone
        self.log("Verifying session is deleted...")
        r = requests.get(f"{BASE_URL}/demo/sessions/{self.session_id}")
        assert r.status_code == 404, f"Session still exists: {r.status_code}"
        self.log("✓ Session no longer accessible")
    
    # ========== REGRESSION TESTS ==========
    
    def test_regression_api_health(self):
        """Regression: GET /api/health - API health check still works."""
        self.log("Testing API health endpoint...")
        r = self.get("/health")
        data = r.json()
        
        assert "success" in data, "Missing success field"
        assert data["success"] == True, "Request not successful"
        assert "data" in data, "Missing data field"
        assert data["data"]["status"] == "healthy", "API not healthy"
        
        self.log("✓ API health endpoint working")
    
    def test_regression_api_root(self):
        """Regression: GET /api/ - API root endpoint still works."""
        self.log("Testing API root endpoint...")
        
        r = self.get("/")
        data = r.json()
        
        assert "success" in data, "Missing success field"
        assert data["success"] == True, "Request not successful"
        assert data["data"]["service"] == "kti-api", "Wrong service name"
        
        self.log("✓ API root endpoint working")
    
    # ========== RUN ALL TESTS ==========
    
    def run_all(self):
        """Run all Phase 16 tests."""
        print("\n" + "="*70)
        print("Phase 16 Backend Testing: Demo Sandbox Engine")
        print("="*70)
        
        # Auth setup
        self.test("Auth Setup", self.test_auth_setup)
        
        # Demo session tests
        self.test("Create Demo Session", self.test_create_demo_session)
        self.test("Validate Demo Session", self.test_validate_demo_session)
        self.test("KN3 Dashboard", self.test_kn3_dashboard)
        self.test("KN3 Products", self.test_kn3_products)
        self.test("KN3 Sales Orders", self.test_kn3_sales_orders)
        self.test("KN3 Warehouses", self.test_kn3_warehouses)
        self.test("List Active Sessions (Admin)", self.test_list_active_sessions_admin)
        self.test("Delete Demo Session", self.test_delete_demo_session)
        
        # Regression tests
        self.test("Regression: API Health", self.test_regression_api_health)
        self.test("Regression: API Root", self.test_regression_api_root)
        
        # Summary
        print("\n" + "="*70)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        print("="*70)
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for ft in self.failed_tests:
                print(f"  - {ft['name']}: {ft['error']}")
            return 1
        else:
            print("\n✅ All tests passed!")
            return 0

if __name__ == "__main__":
    tester = Phase16Tester()
    sys.exit(tester.run_all())
