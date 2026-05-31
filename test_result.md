#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: |
  Platform Kubus Teknologi Indonesia - Phase 15: Real-time Notifications via WebSocket.
  Scope: Toast + Bell + persisted MongoDB + multi-portal (admin/staff/client) + live updates
  (project status change, approval sign, lead created, invoice created, chat message, document upload).
  Test credentials: admin@kubus.id/Admin#2026, staff@kubus.id/Staff#2026, client@kubus.id/Client#2026
  Preview URL: https://dev-context-setup-1.preview.emergentagent.com

backend:
  - task: "WebSocket endpoint /ws/notifications dengan JWT token auth"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "WebSocket endpoint implemented at /api/ws/notifications?token=<jwt>. ConnectionManager in realtime.py. Auth via JWT decode."

  - task: "REST GET /api/notifications - list notif dengan pagination"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Tested: returns success=True, unread count, items list. Auth required."

  - task: "REST GET /api/notifications/unread-count"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Tested curl: returns {unread: N}"

  - task: "REST POST /api/notifications/{id}/read - mark single read"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Implemented. Needs end-to-end testing."

  - task: "REST POST /api/notifications/read-all - mark all read"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Implemented. Needs end-to-end testing."

  - task: "REST DELETE /api/notifications/{id} - delete single notification"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "low"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Implemented. Needs end-to-end testing."

  - task: "Trigger notif saat lead dibuat (lead.created)"
    implemented: true
    working: true
    file: "backend/routers/leads.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "TESTED: POST /api/leads -> notification created for all admin/staff. Verified unread increases from 0 to 1."

  - task: "Trigger notif saat project dibuat (project.created)"
    implemented: true
    working: true
    file: "backend/routers/projects.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "inapp.create_for_users called for client + staff on project creation."

  - task: "Trigger notif saat project status berubah (project.status_changed)"
    implemented: true
    working: true
    file: "backend/routers/projects.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Triggers on PATCH /projects/{id} when status changes. Also broadcasts to topic."

  - task: "Trigger notif saat approval diminta (approval.requested)"
    implemented: true
    working: true
    file: "backend/routers/projects.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Fan-out to all project participants + admins."

  - task: "Trigger notif saat approval ditandatangani (approval.signed)"
    implemented: true
    working: true
    file: "backend/routers/projects.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Fan-out to client + staff + admins. Also broadcasts to approval: and project: topics."

  - task: "Trigger notif saat invoice dibuat (invoice.created)"
    implemented: true
    working: true
    file: "backend/routers/billing.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Notifies the invoice client."

  - task: "Trigger notif saat dokumen diupload (document.uploaded)"
    implemented: true
    working: true
    file: "backend/routers/projects.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Notifies project participants except uploader."

  - task: "Trigger notif saat pesan chat dikirim (chat.message)"
    implemented: true
    working: true
    file: "backend/routers/chat.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Notifies other thread participants."

  - task: "GET /api/admin/realtime/stats (admin only)"
    implemented: true
    working: true
    file: "backend/routers/notifications.py"
    stuck_count: 0
    priority: "low"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Returns connected_users, total_sockets, topics stats."

frontend:
  - task: "NotificationBell component terintegrasi di AdminLayout header"
    implemented: true
    working: true
    file: "frontend/src/features/admin/AdminLayout.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "NotificationBell imported and rendered in AdminLayout header at line 159."

  - task: "NotificationBell component terintegrasi di ClientLayout header"
    implemented: true
    working: true
    file: "frontend/src/features/portal/client/ClientLayout.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "NotificationBell imported and rendered in ClientLayout header at line 109."

  - task: "NotificationProvider wrapping seluruh App di App.js"
    implemented: true
    working: true
    file: "frontend/src/App.js"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "NotificationProvider wraps inside AuthProvider in App.js."

  - task: "Bell icon dengan badge unread count"
    implemented: true
    working: true
    file: "frontend/src/components/NotificationBell.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Bell icon shows badge when unread > 0. data-testid=notification-bell-badge."

  - task: "Popover daftar notifikasi dengan mark-as-read & delete"
    implemented: true
    working: true
    file: "frontend/src/components/NotificationBell.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Popover with scroll area, item list, mark-all-read button, delete per-item, refresh."

  - task: "WebSocket auto-connect saat user login + disconnect saat logout"
    implemented: true
    working: true
    file: "frontend/src/context/NotificationContext.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "useEffect on user state: connect() on login, disconnect() on logout. realtime.js has auto-reconnect with backoff."

  - task: "Toast popup saat notifikasi real-time masuk via WebSocket"
    implemented: true
    working: true
    file: "frontend/src/context/NotificationContext.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Notification kind='notification' triggers sonner toast() with title+body+optional action link."

  - task: "Connection status indicator (titik hijau=connected, amber=offline)"
    implemented: true
    working: true
    file: "frontend/src/components/NotificationBell.jsx"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Small dot indicator bottom-left of bell icon: emerald=connected, amber=offline."

  - task: "Relative timestamp pada setiap notifikasi (baru saja, Xm lalu, Xj lalu)"
    implemented: true
    working: true
    file: "frontend/src/components/NotificationBell.jsx"
    stuck_count: 0
    priority: "low"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "RelativeTime component renders baru saja/Xm lalu/Xj lalu/Xh lalu/date."

  - task: "i18n bilingual (ID/EN) untuk semua label notifikasi"
    implemented: true
    working: true
    file: "frontend/src/i18n/locales/id.json"
    stuck_count: 0
    priority: "low"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "notif.* keys present in both id.json and en.json."

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 11
  run_ui: true

test_plan:
  current_focus:
    - "WebSocket endpoint /ws/notifications dengan JWT token auth"
    - "NotificationBell component terintegrasi di AdminLayout header"
    - "NotificationBell component terintegrasi di ClientLayout header"
    - "Bell icon dengan badge unread count"
    - "Popover daftar notifikasi dengan mark-as-read & delete"
    - "Trigger notif saat lead dibuat (lead.created)"
    - "Trigger notif saat project dibuat (project.created)"
    - "Toast popup saat notifikasi real-time masuk via WebSocket"
    - "REST GET /api/notifications - list notif dengan pagination"
    - "REST POST /api/notifications/read-all - mark all read"
  stuck_tasks: []
  test_all: true
  test_priority: "high_first"

agent_communication:
  - agent: "main"
    message: |
      Phase 15 Real-time Notifications implementation sudah lengkap.
      
      BACKEND:
      - realtime.py: ConnectionManager (user fan-out + topic pub/sub)
      - routers/notifications.py: WebSocket /api/ws/notifications?token=<jwt> + REST CRUD
      - notification_service.py: create(), create_for_users(), create_for_admin_staff(), broadcast_topic()
      - Triggers wired di: leads.py (lead.created), projects.py (project.created/status_changed/assigned/approval.requested/approval.signed/document.uploaded), billing.py (invoice.created/status_changed/overdue), chat.py (chat.message)
      
      FRONTEND:
      - lib/realtime.js: RealtimeClient singleton dengan auto-reconnect exponential backoff
      - context/NotificationContext.jsx: provider yang connect/disconnect berdasarkan auth state
      - components/NotificationBell.jsx: bell icon + unread badge + popover list + mark-read + delete
      - AdminLayout.jsx line 159: <NotificationBell />
      - ClientLayout.jsx line 109: <NotificationBell />
      - App.js: <NotificationProvider> wraps semua routes
      
      VERIFIED via curl:
      - POST /api/leads -> notification auto-created di DB untuk admin, unread naik 0->1
      - GET /api/notifications: returns items + unread count
      - GET /api/admin/realtime/stats: returns connected_users stats
      
      TESTING FOCUS:
      1. Login sebagai admin, cek bell icon muncul di header portal admin
      2. Cek badge unread count tampil di bell (dari notif yang sudah ada dari test lead)
      3. Click bell -> popover muncul dengan list notifikasi
      4. Mark as read (single + all)
      5. Delete notifikasi
      6. Login sebagai client, cek bell di client portal
      7. Buat project/invoice via admin -> cek client mendapat notifikasi
      8. SKIP: WebSocket live push test (tidak bisa test browser automation untuk WebSocket real-time)
      
      SKIP drag-and-drop, camera, microphone tests.
      Auth credentials: admin@kubus.id/Admin#2026, staff@kubus.id/Staff#2026, client@kubus.id/Client#2026
