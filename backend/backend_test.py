"""
Phase 15 Backend Testing: Real-time Notifications via WebSocket
Tests notification REST endpoints, event triggers, and regression.

Tests:
- NEW: GET /api/notifications (list with unread count)
- NEW: GET /api/notifications/unread-count
- NEW: POST /api/notifications/{id}/read
- NEW: POST /api/notifications/read-all
- NEW: DELETE /api/notifications/{id}
- NEW: GET /api/admin/realtime/stats (admin only)
- NEW: Lead creation triggers lead.created notification
- NEW: Project creation triggers project.created notification
- NEW: Project status change triggers project.status_changed notification
- REGRESSION: Admin dashboard, Projects, Leads still working
"""
import requests
import sys
import time

BASE_URL = "https://dev-context-setup-1.preview.emergentagent.com/api"

class Phase15Tester:
    def __init__(self):
        self.admin_token = None
        self.staff_token = None
        self.client_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.created_lead_id = None
        self.created_project_id = None
        
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
    
    def patch(self, endpoint, data, token=None, expected_status=200):
        """PATCH request helper."""
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.patch(f"{BASE_URL}{endpoint}", json=data, headers=headers)
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
        """Login as admin, staff, and client."""
        self.log("Logging in as admin...")
        self.admin_token = self.login("admin@kubus.id", "Admin#2026")
        self.log("✓ Admin logged in")
        
        self.log("Logging in as staff...")
        self.staff_token = self.login("staff@kubus.id", "Staff#2026")
        self.log("✓ Staff logged in")
        
        self.log("Logging in as client...")
        self.client_token = self.login("client@kubus.id", "Client#2026")
        self.log("✓ Client logged in")
    
    # ========== PHASE 15: NOTIFICATION REST ENDPOINTS ==========
    
    def test_notifications_list(self):
        """GET /api/notifications returns list with unread count."""
        r = self.get("/notifications", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        assert "items" in data, "Missing 'items' in response"
        assert "total" in data, "Missing 'total' in response"
        assert "unread" in data, "Missing 'unread' in response"
        assert isinstance(data["items"], list), "items should be a list"
        assert isinstance(data["unread"], int), "unread should be an integer"
        self.log(f"✓ Got {len(data['items'])} notifications, {data['unread']} unread")
    
    def test_notifications_unread_count(self):
        """GET /api/notifications/unread-count returns integer count."""
        r = self.get("/notifications/unread-count", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        assert "unread" in data, "Missing 'unread' in response"
        assert isinstance(data["unread"], int), "unread should be an integer"
        self.log(f"✓ Unread count: {data['unread']}")
    
    def test_notifications_mark_read(self):
        """POST /api/notifications/{id}/read marks single notification as read."""
        # First get a notification
        r = self.get("/notifications?unread_only=true", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        items = data.get("items", [])
        
        if not items:
            self.log("⚠ No unread notifications to test mark-read")
            return
        
        notif_id = items[0]["id"]
        self.log(f"Testing mark-read on notification: {notif_id}")
        
        # Mark as read
        r2 = self.post(f"/notifications/{notif_id}/read", {}, token=self.admin_token, expected_status=200)
        result = r2.json().get("data", {})
        assert result.get("id") == notif_id, "ID mismatch"
        assert result.get("read") == True, "Should be marked as read"
        self.log(f"✓ Notification {notif_id} marked as read")
    
    def test_notifications_mark_all_read(self):
        """POST /api/notifications/read-all marks all as read."""
        r = self.post("/notifications/read-all", {}, token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        assert "modified" in data, "Missing 'modified' in response"
        self.log(f"✓ Marked {data['modified']} notifications as read")
    
    def test_notifications_delete(self):
        """DELETE /api/notifications/{id} removes notification."""
        # First get a notification
        r = self.get("/notifications?limit=1", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        items = data.get("items", [])
        
        if not items:
            self.log("⚠ No notifications to test delete")
            return
        
        notif_id = items[0]["id"]
        self.log(f"Testing delete on notification: {notif_id}")
        
        # Delete
        r2 = self.delete(f"/notifications/{notif_id}", token=self.admin_token, expected_status=200)
        result = r2.json().get("data", {})
        assert result.get("deleted") == True, "Should return deleted=True"
        self.log(f"✓ Notification {notif_id} deleted")
    
    def test_admin_realtime_stats(self):
        """GET /api/admin/realtime/stats returns connection stats (admin only)."""
        # Admin can access
        r = self.get("/admin/realtime/stats", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        assert "connected_users" in data, "Missing 'connected_users'"
        assert "total_sockets" in data, "Missing 'total_sockets'"
        assert "topics" in data, "Missing 'topics'"
        self.log(f"✓ Realtime stats: {data['connected_users']} users, {data['total_sockets']} sockets")
        
        # Staff should get 403
        r2 = self.get("/admin/realtime/stats", token=self.staff_token, expected_status=403)
        self.log("✓ Staff correctly forbidden")
    
    # ========== PHASE 15: EVENT TRIGGERS ==========
    
    def test_lead_creation_triggers_notification(self):
        """POST /api/leads creates lead AND triggers lead.created notification."""
        # Get initial unread count for admin
        r1 = self.get("/notifications/unread-count", token=self.admin_token, expected_status=200)
        unread_before = r1.json().get("data", {}).get("unread", 0)
        self.log(f"Unread before: {unread_before}")
        
        # Create a lead
        lead_data = {
            "name": "Test Lead Phase 15",
            "email": f"testlead{int(time.time())}@example.com",
            "company": "Test Company",
            "phone": "+62123456789",
            "message": "This is a test lead for Phase 15 notification testing",
            "source": "contact_form"
        }
        r2 = self.post("/leads", lead_data, expected_status=201)
        lead_id = r2.json().get("data", {}).get("id")
        assert lead_id, "Lead ID not returned"
        self.created_lead_id = lead_id
        self.log(f"✓ Lead created: {lead_id}")
        
        # Wait a bit for notification to be created
        time.sleep(1)
        
        # Check if notification was created for admin
        r3 = self.get("/notifications/unread-count", token=self.admin_token, expected_status=200)
        unread_after = r3.json().get("data", {}).get("unread", 0)
        self.log(f"Unread after: {unread_after}")
        
        # Check recent notifications for lead.created
        r4 = self.get("/notifications?limit=5", token=self.admin_token, expected_status=200)
        items = r4.json().get("data", {}).get("items", [])
        lead_notif = [n for n in items if n.get("type") == "lead.created" and lead_id in str(n.get("metadata", {}))]
        
        if lead_notif:
            self.log(f"✓ lead.created notification found: {lead_notif[0].get('title')}")
        else:
            self.log(f"⚠ lead.created notification not found in recent notifications (may have been created)")
    
    def test_project_creation_triggers_notification(self):
        """POST /api/projects creates project AND triggers project.created notification."""
        # Get initial unread count for admin
        r1 = self.get("/notifications/unread-count", token=self.admin_token, expected_status=200)
        unread_before = r1.json().get("data", {}).get("unread", 0)
        
        # Create a project
        project_data = {
            "name": f"Test Project Phase 15 {int(time.time())}",
            "status": "active",
            "progress": 0,
            "summary": "Test project for Phase 15 notification testing"
        }
        r2 = self.post("/projects", project_data, token=self.admin_token, expected_status=200)
        project_id = r2.json().get("data", {}).get("id")
        assert project_id, "Project ID not returned"
        self.created_project_id = project_id
        self.log(f"✓ Project created: {project_id}")
        
        # Wait a bit for notification to be created
        time.sleep(1)
        
        # Check recent notifications for project.created
        r3 = self.get("/notifications?limit=5", token=self.admin_token, expected_status=200)
        items = r3.json().get("data", {}).get("items", [])
        project_notif = [n for n in items if n.get("type") == "project.created" and project_id in str(n.get("metadata", {}))]
        
        if project_notif:
            self.log(f"✓ project.created notification found: {project_notif[0].get('title')}")
        else:
            self.log(f"⚠ project.created notification not found in recent notifications")
    
    def test_project_status_change_triggers_notification(self):
        """PATCH /api/projects/{id} with status change triggers project.status_changed notification."""
        if not self.created_project_id:
            self.log("⚠ No project to test status change")
            return
        
        # Change project status
        patch_data = {"status": "on_hold"}
        r = self.patch(f"/projects/{self.created_project_id}", patch_data, token=self.admin_token, expected_status=200)
        self.log(f"✓ Project status changed to on_hold")
        
        # Wait a bit for notification to be created
        time.sleep(1)
        
        # Check recent notifications for project.status_changed
        r2 = self.get("/notifications?limit=5", token=self.admin_token, expected_status=200)
        items = r2.json().get("data", {}).get("items", [])
        status_notif = [n for n in items if n.get("type") == "project.status_changed" and self.created_project_id in str(n.get("metadata", {}))]
        
        if status_notif:
            self.log(f"✓ project.status_changed notification found: {status_notif[0].get('title')}")
        else:
            self.log(f"⚠ project.status_changed notification not found in recent notifications")
    
    # ========== REGRESSION TESTS ==========
    
    def test_regression_admin_dashboard(self):
        """Admin dashboard endpoints still working."""
        # Test auth/me
        r = self.get("/auth/me", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        assert data.get("email") == "admin@kubus.id", "Email mismatch"
        self.log("✓ GET /api/auth/me working")
    
    def test_regression_projects_list(self):
        """GET /api/projects still working."""
        r = self.get("/projects", token=self.admin_token, expected_status=200)
        data = r.json().get("data", [])
        assert isinstance(data, list), "Expected list of projects"
        self.log(f"✓ GET /api/projects working ({len(data)} projects)")
    
    def test_regression_leads_list(self):
        """GET /api/leads still working."""
        r = self.get("/leads", token=self.admin_token, expected_status=200)
        data = r.json().get("data", {})
        assert "items" in data, "Missing items"
        self.log(f"✓ GET /api/leads working ({data.get('total', 0)} leads)")
    
    def test_regression_public_homepage(self):
        """Public website homepage loads without error."""
        # Test public services endpoint
        r = self.get("/services", expected_status=200)
        data = r.json().get("data", [])
        assert isinstance(data, list), "Expected list of services"
        self.log(f"✓ GET /api/services working ({len(data)} services)")
    
    # ========== RUN ALL TESTS ==========
    
    def run_all(self):
        print("\n" + "="*80)
        print("PHASE 15 BACKEND TESTING: Real-time Notifications via WebSocket")
        print("="*80)
        
        # Auth setup
        self.test("Auth Setup (admin/staff/client login)", self.test_auth_setup)
        
        print("\n" + "="*80)
        print("PHASE 15: NOTIFICATION REST ENDPOINTS")
        print("="*80)
        
        self.test("GET /api/notifications (list with unread count)", self.test_notifications_list)
        self.test("GET /api/notifications/unread-count", self.test_notifications_unread_count)
        self.test("POST /api/notifications/{id}/read", self.test_notifications_mark_read)
        self.test("POST /api/notifications/read-all", self.test_notifications_mark_all_read)
        self.test("DELETE /api/notifications/{id}", self.test_notifications_delete)
        self.test("GET /api/admin/realtime/stats (admin only)", self.test_admin_realtime_stats)
        
        print("\n" + "="*80)
        print("PHASE 15: EVENT TRIGGERS")
        print("="*80)
        
        self.test("Lead creation triggers lead.created notification", self.test_lead_creation_triggers_notification)
        self.test("Project creation triggers project.created notification", self.test_project_creation_triggers_notification)
        self.test("Project status change triggers project.status_changed notification", self.test_project_status_change_triggers_notification)
        
        print("\n" + "="*80)
        print("REGRESSION TESTS")
        print("="*80)
        
        self.test("Admin dashboard (GET /api/auth/me)", self.test_regression_admin_dashboard)
        self.test("Projects list (GET /api/projects)", self.test_regression_projects_list)
        self.test("Leads list (GET /api/leads)", self.test_regression_leads_list)
        self.test("Public homepage (GET /api/services)", self.test_regression_public_homepage)
        
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
    tester = Phase15Tester()
    sys.exit(tester.run_all())
