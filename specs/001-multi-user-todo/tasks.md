---

description: "Task list template for feature implementation"
---

# Tasks: Secure Multi-User Full-Stack Todo Web Application with Polished Responsive UI

**Input**: Design documents from `/specs/001-multi-user-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual testing per specification - no automated unit/integration tests requested

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web application**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web application structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create frontend/ and backend/ directory structure per implementation plan
- [ ] T002 [P] Initialize Next.js 16+ project in frontend/ with App Router, TypeScript, Tailwind CSS
- [ ] T003 [P] Initialize FastAPI project in backend/ with Python 3.11+, SQLModel, Pydantic
- [ ] T004 [P] Install frontend dependencies: shadcn/ui, Sonner, next-themes, Lucide icons, Zod, Better Auth
- [ ] T005 [P] Install backend dependencies: python-jose, passlib, psycopg2-binary, python-dotenv
- [ ] T006 [P] Configure Tailwind CSS in frontend/ with dark mode support
- [ ] T007 [P] Initialize shadcn/ui components (button, card, checkbox, dialog, input, textarea, toast)
- [ ] T008 [P] Create .env.local template in frontend/ and .env template in backend/
- [ ] T009 [P] Configure Next.js for production (next.config.ts with headers, optimizations)
- [ ] T010 [P] Configure FastAPI CORS and security headers

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 Set up Neon PostgreSQL database connection with DATABASE_URL in backend/.env
- [ ] T012 Generate BETTER_AUTH_SECRET and configure in both frontend/.env.local and backend/.env
- [ ] T013 Create User SQLModel in backend/app/models/user.py with id, email, password_hash, created_at, updated_at
- [ ] T014 [P] Create Task SQLModel in backend/app/models/task.py with id, title, description, completed, user_id, created_at, updated_at
- [ ] T015 Create database initialization script backend/app/db/init_db.py with User and Task tables
- [ ] T016 Create database session management in backend/app/db/session.py with engine and session factory
- [ ] T017 Create FastAPI app configuration in backend/app/core/config.py for environment variables
- [ ] T018 Create JWT verification middleware in backend/app/core/security.py with python-jose
- [ ] T019 Create dependency injection system in backend/app/core/deps.py to extract user_id from JWT
- [ ] T020 Create Zod validation schemas in frontend/lib/validations.ts for User, Task, and API responses
- [ ] T021 Create API client in frontend/lib/api-client.ts with JWT injection and 401 redirect handling
- [ ] T022 [P] Initialize Better Auth in frontend/lib/auth.ts with email/password provider
- [ ] T023 Configure next-themes ThemeProvider in frontend/app/layout.tsx for system preference detection
- [ ] T024 Create global CSS in frontend/styles/globals.css with Tailwind directives and custom styles
- [ ] T025 Test database connection by running backend/app/db/init_db.py and verifying tables exist

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Account Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create secure accounts and sign in, ensuring data isolation foundation

**Independent Test**: Can be fully tested by attempting to create multiple user accounts, signing in as each user, and verifying that users cannot access each other's data. Delivers secure, private task management foundation.

### Implementation for User Story 1

- [ ] T026 [US1] Create frontend/app/(auth)/signup/page.tsx with email and password form
- [ ] T027 [US1] Create frontend/app/(auth)/signin/page.tsx with email and password form
- [ ] T028 [US1] Create frontend/components/auth/auth-forms.tsx with Better Auth integration
- [ ] T029 [US1] Create frontend/app/(auth)/layout.tsx with auth layout and redirect to tasks page if signed in
- [ ] T030 [US1] Create backend/app/api/v1/endpoints/auth.py with user creation endpoint (POST /users)
- [ ] T031 [US1] Implement password hashing in backend/app/models/user.py using passlib with bcrypt
- [ ] T032 [US1] Implement email validation and uniqueness check in user creation endpoint
- [ ] T033 [US1] Create frontend/app/(main)/tasks/page.tsx redirect to signin if not authenticated
- [ ] T034 [US1] Add sign out button and Better Auth signOut handler in frontend components
- [ ] T035 [US1] Configure Better Auth to issue JWT tokens with user_id in sub claim
- [ ] T036 [US1] Configure JWT verification to extract user_id from token in backend middleware
- [ ] T037 [US1] Test signup flow by creating user and verifying JWT is issued
- [ ] T038 [US1] Test signin flow by verifying credentials and JWT is returned
- [ ] T039 [US1] Test sign out flow by verifying session is terminated
- [ ] T040 [US1] Test unauthenticated access returns 401 by accessing /tasks page while signed out
- [ ] T041 [US1] Create user creation validation with email format and password strength requirements
- [ ] T042 [US1] Add error messages to auth forms for invalid email, weak password, existing email
- [ ] T043 [US1] Store JWT securely in frontend (localStorage or httpOnly cookie)
- [ ] T044 [US1] Configure automatic redirect from home page to tasks page if authenticated

**Checkpoint**: At this point, user accounts can be created and users can sign in/sign out securely. Foundation for data isolation is ready.

---

## Phase 4: User Story 2 - Basic Task CRUD Operations (Priority: P1)

**Goal**: Enable signed-in users to create, view, update, delete, and complete their tasks

**Independent Test**: Can be fully tested by creating tasks, viewing them in list, editing task details, marking tasks as complete, and deleting tasks. Delivers complete task management capability for single user.

### Implementation for User Story 2

- [ ] T045 [P] [US2] Create Task SQLModel in backend/app/models/task.py with id, title, description, completed, user_id, created_at, updated_at
- [ ] T046 [P] [US2] Create User SQLModel in backend/app/models/user.py with foreign key relationship to tasks
- [ ] T047 [US2] Create GET /api/v1/users/{user_id}/tasks endpoint in backend/app/api/v1/endpoints/tasks.py
- [ ] T048 [US2] Implement task listing query in GET /users/{user_id}/tasks endpoint with WHERE user_id = authenticated_user_id
- [ ] T049 [US2] Sort tasks by created_at DESC in GET /users/{user_id}/tasks endpoint
- [ ] T050 [US2] Add optional completed filter query parameter to GET /users/{user_id}/tasks endpoint
- [ ] T051 [US2] Create POST /api/v1/users/{user_id}/tasks endpoint in backend/app/api/v1/endpoints/tasks.py
- [ ] T052 [US2] Implement task creation with user_id extracted from JWT in POST /users/{user_id}/tasks endpoint
- [ ] T053 [US2] Validate task title (1-200 chars, required) and description (0-1000 chars, optional) in POST endpoint
- [ ] T054 [US2] Return 201 Created with full task object in POST /users/{user_id}/tasks endpoint
- [ ] T055 [US2] Create GET /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/app/api/v1/endpoints/tasks.py
- [ ] T056 [US2] Implement ownership verification in GET /users/{user_id}/tasks/{task_id} endpoint
- [ ] T057 [US2] Return 404 Not Found if task doesn't exist or user doesn't own it in GET endpoint
- [ ] T058 [US2] Create PUT /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/app/api/v1/endpoints/tasks.py
- [ ] T059 [US2] Implement partial updates in PUT /users/{user_id}/tasks/{task_id} endpoint
- [ ] T060 [US2] Verify user ownership before allowing task update in PUT endpoint
- [ ] T061 [US2] Return 404 Not Found if task doesn't exist or user doesn't own it in PUT endpoint
- [ ] T062 [US2] Create DELETE /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/app/api/v1/endpoints/tasks.py
- [ ] T063 [US2] Verify user ownership before allowing task deletion in DELETE endpoint
- [ ] T064 [US2] Return 404 Not Found if task doesn't exist or user doesn't own it in DELETE endpoint
- [ ] T065 [US2] Create frontend/app/(main)/tasks/page.tsx with task list fetch on component mount
- [ ] T066 [US2] Create useTasks hook in frontend/hooks/use-tasks.ts to fetch and manage task state
- [ ] T067 [US2] Create frontend/components/task/task-list.tsx to display all user's tasks
- [ ] T068 [US2] Create frontend/components/task/task-card.tsx to display individual task with title, description, status
- [ ] T069 [US2] Create frontend/components/task/task-form.tsx with title and description fields
- [ ] T070 [US2] Implement Zod validation in frontend/lib/validations.ts for CreateTaskRequest and UpdateTaskRequest schemas
- [ ] T071 [US2] Create frontend/components/task/add-task-button.tsx with prominent button (desktop) and FAB (mobile)
- [ ] T072 [US2] Implement task creation flow with API client POST to /users/{user_id}/tasks
- [ ] T073 [US2] Implement task list fetch with API client GET from /users/{user_id}/tasks
- [ ] T074 [US2] Implement task update flow with API client PUT to /users/{user_id}/tasks/{task_id}
- [ ] T075 [US2] Implement task deletion flow with API client DELETE to /users/{user_id}/tasks/{task_id}
- [ ] T076 [US2] Add optimistic updates for task completion and deletion for instant feedback
- [ ] T077 [US2] Create loading skeleton in frontend/app/(main)/tasks/loading.tsx
- [ ] T078 [US2] Test create task by adding task through form and verifying it appears in list
- [ ] T079 [US2] Test view tasks by verifying all tasks display in list
- [ ] T080 [US2] Test edit task by modifying title/description and verifying updates persist
- [ ] T081 [US2] Test complete task by toggling checkbox and verifying strikethrough and status change
- [ ] T082 [US2] Test incomplete task by unchecking and verifying it returns to active state
- [ ] T083 [US2] Test delete task by deleting and verifying task is removed from list
- [ ] T084 [US2] Test task list with 100 tasks to verify performance (<2s load time)
- [ ] T085 [US2] Verify all database queries filter by user_id in backend endpoints

**Checkpoint**: At this point, users can create, view, update, delete, and complete tasks. Basic CRUD functionality is fully operational.

---

## Phase 5: User Story 3 - Multi-User Data Isolation (Priority: P1)

**Goal**: Ensure 100% data isolation between users - no cross-user access possible

**Independent Test**: Can be fully tested by creating two different user accounts, adding tasks for each, signing in as each user, and verifying that users only ever see their own tasks. Delivers core security and privacy guarantee.

### Implementation for User Story 3

- [ ] T086 [US3] Verify JWT verification middleware runs on ALL protected endpoints (GET, POST, PUT, DELETE)
- [ ] T087 [US3] Test unauthenticated request to /api/v1/users/{user_id}/tasks returns 401
- [ ] T088 [US3] Test request with invalid JWT to /api/v1/users/{user_id}/tasks returns 401
- [ ] T089 [US3] Test request with expired JWT to /api/v1/users/{user_id}/tasks returns 401
- [ ] T090 [US3] Create User A (user_a@test.com) and sign in
- [ ] T091 [US3] Create 3 tasks as User A
- [ ] T092 [US3] Sign out User A, create User B (user_b@test.com), sign in
- [ ] T093 [US3] Verify User B sees 0 tasks initially (not User A's tasks)
- [ ] T094 [US3] Create 2 tasks as User B
- [ ] T095 [US3] Sign out User B, sign in as User A
- [ ] T096 [US3] Verify User A still sees only their 3 tasks (not User B's 2 tasks)
- [ ] T097 [US3] Use browser dev tools to capture User B's JWT token
- [ ] T098 [US3] Use cURL/Postman to attempt GET /users/{user_a_id}/tasks with User B's JWT
- [ ] T099 [US3] Verify request returns 403 Forbidden (user_id mismatch)
- [ ] T100 [US3] Use cURL/Postman to attempt POST task with User B's JWT to User A's account
- [ ] T101 [US3] Verify request returns 403 Forbidden
- [ ] T102 [US3] Use cURL/Postman to attempt PUT task with User B's JWT for User A's task
- [ ] T103 [US3] Verify request returns 404 Not Found (doesn't reveal if task exists)
- [ ] T104 [US3] Use cURL/Postman to attempt DELETE task with User B's JWT for User A's task
- [ ] T105 [US3] Verify request returns 404 Not Found
- [ ] T106 [US3] Verify backend endpoints reject cross-user access at middleware level or route handler level
- [ ] T107 [US3] Verify database queries include WHERE user_id = ? in all SELECT, UPDATE, DELETE queries
- [ ] T108 [US3] Test that task_id guessing doesn't reveal task existence for other users
- [ ] T109 [US3] Verify frontend cannot accidentally send other user's task IDs (JWT prevents this)
- [ ] T110 [US3] Document data isolation strategy in quickstart.md testing section

**Checkpoint**: At this point, 100% data isolation is verified. Users can only ever access their own tasks.

---

## Phase 6: User Story 4 - Premium Responsive User Interface (Priority: P2)

**Goal**: Provide beautiful, responsive, accessible UI with premium design, animations, and satisfying feedback

**Independent Test**: Can be fully tested by interacting with application on various screen sizes and devices, verifying that all actions provide visual feedback, interface is responsive, and interactions feel smooth and satisfying. Delivers enhanced, premium user experience.

### Implementation for User Story 4

- [ ] T111 [P] [US4] Create card-based task cards in frontend/components/task/task-card.tsx with shadow, rounded corners, hover states
- [ ] T112 [US4] Implement instant strikethrough and color change when task is completed
- [ ] T113 [US4] Add subtle animation for completion toggle (CSS transition or framer-motion)
- [ ] T114 [US4] Create frontend/components/task/empty-state.tsx with friendly message and illustration
- [ ] T115 [US4] Display empty-state component when task list is empty in frontend/app/(main)/tasks/page.tsx
- [ ] T116 [P] [US4] Install and configure Sonner for toast notifications in frontend/
- [ ] T117 [US4] Add toaster component in frontend/app/layout.tsx at top of app
- [ ] T118 [US4] Display toast notification after task creation with "Task created" message
- [ ] T119 [US4] Display toast notification after task update with "Task updated" message
- [ ] T120 [US4] Display toast notification after task deletion with "Task deleted" message
- [ ] T121 [US4] Display toast notification after task completion with "Task completed" message
- [ ] T122 [US4] Configure toast notifications to auto-dismiss after 3 seconds
- [ ] T123 [US4] Make toast notifications appear within 200ms of action completion
- [ ] T124 [P] [US4] Install and configure Lucide icons for UI elements (plus, trash, check, x)
- [ ] T125 [US4] Add icons to task cards (checkbox icon, delete button, edit button)
- [ ] T126 [US4] Add icons to add-task-button (plus icon)
- [ ] T127 [US4] Make frontend/components/task/add-task-button.tsx responsive with Tailwind breakpoints
- [ ] T128 [US4] Display fixed button on desktop (top or side of page) in add-task-button.tsx
- [ ] T129 [US4] Display floating action button (FAB) at bottom on mobile in add-task-button.tsx
- [ ] T130 [US4] Create task editing modal in frontend/components/task/task-form.tsx with dialog component
- [ ] T131 [US4] Implement smooth open/close transitions for task editing modal
- [ ] T132 [US4] Add modal trigger button on task card for editing tasks
- [ ] T133 [US4] Add ARIA labels to all interactive elements (buttons, checkboxes, forms)
- [ ] T134 [US4] Add keyboard navigation support (tab to all elements, enter to submit forms)
- [ ] T135 [US4] Implement focus management in modals (trap focus, escape to close)
- [ ] T136 [US4] Add skip links for keyboard users to bypass navigation
- [ ] T137 [US4] Verify text contrast ratios meet WCAG AA standards (4.5:1 for normal text)
- [ ] T138 [US4] Test dark mode by toggling system preference and verifying theme switches within 500ms
- [ ] T139 [US4] Test light mode by toggling system preference and verifying theme switches within 500ms
- [ ] T140 [US4] Configure next-themes ThemeProvider to respect system preference
- [ ] T141 [US4] Add light/dark mode toggle button in frontend/app/(main)/tasks/page.tsx (optional for user override)
- [ ] T142 [US4] Test loading skeleton appears immediately when fetching tasks
- [ ] T143 [US4] Configure loading skeleton to match task card structure
- [ ] T144 [US4] Test responsive layout at mobile viewport (375x667) using Chrome DevTools
- [ ] T145 [US4] Test responsive layout at tablet viewport (768x1024) using Chrome DevTools
- [ ] T146 [US4] Test responsive layout at desktop viewport (1440x900) using Chrome DevTools
- [ ] T147 [US4] Verify FAB appears on mobile and fixed button appears on desktop
- [ ] T148 [US4] Test on real mobile device (iPhone or Android) if available
- [ ] T149 [US4] Test keyboard navigation by navigating entire app with Tab and Enter keys only
- [ ] T150 [US4] Test with screen reader (NVDA or VoiceOver) to verify ARIA labels are announced
- [ ] T151 [US4] Add loading states for all API calls (creating, updating, deleting tasks)
- [ ] T152 [US4] Implement error handling with user-friendly messages for network errors
- [ ] T153 [US4] Test performance by timing task CRUD cycle (<30 seconds target)
- [ ] T154 [US4] Test signup/sign-in flow timing (<60 seconds target)
- [ ] T155 [US4] Add CSS animations for satisfying micro-interactions (hover, active states)
- [ ] T156 [US4] Apply Tailwind utility classes for spacing, typography, colors
- [ ] T157 [US4] Use Tailwind dark mode classes (dark:className) for theme-specific styling
- [ ] T158 [US4] Ensure fonts are readable on both light and dark backgrounds

**Checkpoint**: At this point, UI is polished, responsive, accessible, and provides premium user experience with animations and feedback.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T159 [P] Update README.md in repository root with project description and setup instructions
- [ ] T160 Add DEPLOYMENT.md to specs/001-multi-user-todo/ with Vercel and backend deployment steps
- [ ] T161 [P] Create comprehensive quickstart.md following quickstart.md template structure
- [ ] T162 Add troubleshooting section to quickstart.md for common issues
- [ ] T163 [P] Test end-to-end flow with two users and record <90-second demo video
- [ ] T164 [P] Demo video should show: signup → create tasks → sign out → sign in as other user → verify isolation
- [ ] T165 [P] Verify all security headers are present on backend responses (X-Content-Type-Options, X-Frame-Options, etc.)
- [ ] T166 Test API with Postman collection including all endpoints
- [ ] T167 [P] Verify CORS is configured correctly for frontend origin
- [ ] T168 [P] Add environment variable documentation to quickstart.md
- [ ] T169 [P] Document BETTER_AUTH_SECRET sharing between frontend and backend in quickstart.md
- [ ] T170 Verify Neon database indexes are created (idx_tasks_user_id, idx_tasks_created_at)
- [ ] T171 Test with 100 tasks to verify query performance with indexes
- [ ] T172 Clean up any temporary test data from database
- [ ] T173 Verify all console errors are resolved
- [ ] T174 Verify no console warnings in production build
- [ ] T175 Test application in production environment after deployment
- [ ] T176 [P] Deploy frontend to Vercel following deployment guide
- [ ] T177 [P] Deploy backend to Render or Railway following deployment guide
- [ ] T178 [P] Verify deployed application works end-to-end
- [ ] T179 [P] Create GitHub repository and push all code (public repository required for hackathon)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P1 → P2)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Uses task list page from US1
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Tests isolation of US2
- **User Story 4 (P2)**: Can start after User Stories 1, 2, 3 complete - enhances UI for all features

### Within Each User Story

- Models before services (US2)
- Services before endpoints (US2)
- Core implementation before integration (US2)
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (Phase 1) marked [P] can run in parallel
- All Foundational tasks (Phase 2) marked [P] can run in parallel
- Within US2: T045, T046 (models) can run in parallel
- Within US2: T090-T094 (user creation and task testing) can run in parallel with US4 UI tasks
- Within US4: T111, T116, T124 (component creation) can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch models for User Story 2 together:
Task: "Create Task SQLModel in backend/app/models/task.py with id, title, description, completed, user_id, created_at, updated_at"
Task: "Create User SQLModel in backend/app/models/user.py with foreign key relationship to tasks"

# Launch backend endpoint creation in parallel:
Task: "Create GET /api/v1/users/{user_id}/tasks endpoint in backend/app/api/v1/endpoints/tasks.py"
Task: "Create POST /api/v1/users/{user_id}/tasks endpoint in backend/app/api/v1/endpoints/tasks.py"
Task: "Create GET /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/app/api/v1/endpoints/tasks.py"
Task: "Create PUT /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/app/api/v1/endpoints/tasks.py"
Task: "Create DELETE /api/v1/users/{user_id}/tasks/{task_id} endpoint in backend/app/api/v1/endpoints/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (authentication foundation)
4. Complete Phase 4: User Story 2 (basic CRUD)
5. Complete Phase 5: User Story 3 (data isolation testing)
6. **STOP and VALIDATE**: Test stories 1, 2, 3 independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo (complete security guarantee)
5. Add User Story 4 → Test independently → Deploy/Demo (premium UI)
6. Complete Phase 7: Polish & Deployment → Final production-ready application

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (authentication)
   - Developer B: User Story 2 (CRUD endpoints)
   - Developer C: User Story 3 (isolation testing)
3. Once US1, US2, US3 complete:
   - Developer A: User Story 4 (UI polish)
4. Stories complete and integrate independently
5. Team completes Phase 7 together

---

## Summary

**Total Tasks**: 179
**Tasks per User Story**:
- Phase 1 (Setup): 10 tasks
- Phase 2 (Foundational): 15 tasks
- Phase 3 (US1 - User Account Management): 19 tasks
- Phase 4 (US2 - Basic Task CRUD): 41 tasks
- Phase 5 (US3 - Multi-User Data Isolation): 25 tasks
- Phase 6 (US4 - Premium Responsive UI): 48 tasks
- Phase 7 (Polish): 21 tasks

**Parallel Opportunities**:
- 21 tasks marked [P] can run in parallel
- Models, endpoints, and components can be created in parallel within stories
- User Stories 1, 2, 3 can be worked on in parallel after foundational phase

**Independent Test Criteria**:
- US1: Test signup, signin, signout, and 401 on unauthenticated access
- US2: Test create, view, update, delete, complete tasks with optimistic updates
- US3: Test two users, verify complete task isolation (100% separation)
- US4: Test responsiveness, dark mode, animations, toasts, accessibility

**MVP Scope**: Phases 1-5 (Setup + Foundational + User Stories 1, 2, 3) = 110 tasks

**Recommended Start**: Complete MVP (Phases 1-5), validate with demo video, then add US4 (premium UI)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All implementation follows spec-driven workflow with zero manual coding
