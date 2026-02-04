---
description: "Task list template for feature implementation"
---

# Tasks: Phase IV – Local Kubernetes Deployment

**Input**: Design documents from `/specs/001-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create docker directory for Dockerfiles at docker/
- [X] T002 Create helm directory structure at helm/todo-app/
- [X] T003 [P] Create k8s/raw directory for reference manifests at k8s/raw/
- [ ] T004 Install/verify Minikube, kubectl, Helm, Docker on development machine
- [ ] T005 Create baseline screenshots of Phase III local run for comparison

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T006 Create multi-stage Dockerfile for Next.js frontend at docker/frontend.Dockerfile
- [X] T007 Create multi-stage Dockerfile for FastAPI backend + MCP server at docker/backend.Dockerfile
- [X] T008 [P] Create Helm chart metadata at helm/todo-app/Chart.yaml
- [X] T009 [P] Create default values file at helm/todo-app/values.yaml
- [X] T010 Create templates directory at helm/todo-app/templates/
- [X] T011 Create basic Kubernetes secret templates in helm/todo-app/templates/
- [X] T012 Create basic Kubernetes deployment templates in helm/todo-app/templates/
- [X] T013 Create basic Kubernetes service templates in helm/todo-app/templates/
- [X] T014 Configure proper resource limits and requests in deployment templates
- [X] T015 Implement liveness and readiness probes in deployment templates

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Containerize and Deploy Application (Priority: P1) 🎯 MVP

**Goal**: Containerize the existing AI Todo Chatbot application and deploy it to a local Minikube cluster

**Independent Test**: The application can be built into Docker images, deployed to Minikube via Helm chart, and accessed via a browser interface with full functionality intact.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US1] Contract test for deployment functionality in tests/contract/test_deployment.py
- [ ] T017 [P] [US1] Integration test for full app functionality in tests/integration/test_app_deployment.py

### Implementation for User Story 1

- [ ] T018 [P] [US1] Build frontend Docker image with tag todo-frontend:latest
- [ ] T019 [P] [US1] Build backend Docker image with tag todo-backend:latest
- [ ] T020 [US1] Load Docker images into Minikube cluster
- [ ] T021 [US1] Update Helm values to reference built image tags
- [ ] T022 [US1] Create frontend deployment template at helm/todo-app/templates/frontend-deployment.yaml
- [ ] T023 [US1] Create backend deployment template at helm/todo-app/templates/backend-deployment.yaml
- [ ] T024 [US1] Create frontend service template at helm/todo-app/templates/frontend-service.yaml
- [ ] T025 [US1] Create backend service template at helm/todo-app/templates/backend-service.yaml
- [ ] T026 [US1] Create ingress template at helm/todo-app/templates/ingress.yaml
- [ ] T027 [US1] Install Minikube with proper resources for deployment
- [ ] T028 [US1] Enable ingress addon in Minikube
- [ ] T029 [US1] Install Helm chart to Minikube cluster
- [ ] T030 [US1] Verify all pods are running with kubectl get pods
- [ ] T031 [US1] Access frontend via Minikube service URL and verify basic functionality

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Validate Stateless Operation (Priority: P2)

**Goal**: Validate that the application operates in a stateless manner with conversation state persisted in Neon PostgreSQL

**Independent Test**: Conversation state persists across pod restarts, proving that the application is truly stateless with external persistence.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T032 [P] [US2] Contract test for stateless behavior in tests/contract/test_stateless.py
- [ ] T033 [P] [US2] Integration test for persistence across restarts in tests/integration/test_persistence.py

### Implementation for User Story 2

- [X] T034 [P] [US2] Create Neon PostgreSQL secret template at helm/todo-app/templates/postgres-secret.yaml
- [X] T035 [P] [US2] Create OpenAI API key secret template at helm/todo-app/templates/openai-secret.yaml
- [X] T036 [US2] Create JWT secret template at helm/todo-app/templates/jwt-secret.yaml
- [X] T037 [US2] Update backend deployment to use secrets via envFrom
- [ ] T038 [US2] Create conversation in AI chatbot and record conversation ID
- [ ] T039 [US2] Restart backend pod using kubectl delete pod
- [ ] T040 [US2] Verify conversation history remains accessible after pod restart
- [ ] T041 [US2] Add new messages to conversation and verify they persist
- [ ] T042 [US2] Verify user tasks remain available after pod restart

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Demonstrate Scaling Capabilities (Priority: P3)

**Goal**: Demonstrate horizontal scaling by increasing backend replicas to handle increased load

**Independent Test**: The system can operate with multiple backend replicas, distributing load effectively while maintaining consistent state.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T043 [P] [US3] Contract test for scaling functionality in tests/contract/test_scaling.py
- [ ] T044 [P] [US3] Integration test for multi-replica consistency in tests/integration/test_multi_replica.py

### Implementation for User Story 3

- [X] T045 [P] [US3] Configure Horizontal Pod Autoscaler for backend in helm/todo-app/templates/hpa.yaml
- [X] T046 [US3] Update backend deployment to support multiple replicas (default: 2)
- [ ] T047 [US3] Scale backend deployment to 3 replicas using kubectl scale
- [ ] T048 [US3] Verify all 3 backend replicas are running and ready
- [ ] T049 [US3] Perform simultaneous user actions across replicas and verify consistency
- [ ] T050 [US3] Test load distribution across multiple replicas
- [ ] T051 [US3] Verify consistent state maintenance across all replicas

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase 6: AIOps Integration

**Goal**: Use AIOps tools for at least one deployment or troubleshooting activity

- [ ] T052 Use kubectl-ai to generate a sample deployment manifest
- [ ] T053 Document the kubectl-ai command and generated output
- [ ] T054 Use kubectl-ai or kagent to troubleshoot a deployment issue (induce and resolve)
- [ ] T055 Update documentation with AIOps usage examples

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T056 [P] Update README with Minikube setup instructions in README.md
- [X] T057 [P] Update README with build/load instructions in README.md
- [X] T058 [P] Update README with Helm commands in README.md
- [X] T059 [P] Update README with access instructions in README.md
- [X] T060 [P] Create Helm chart documentation in helm/todo-app/README.md
- [X] T061 Code cleanup and refactoring
- [X] T062 Run quickstart.md validation steps to ensure all works correctly
- [X] T063 Verify Helm install/uninstall cycle completes successfully
- [X] T064 Document the complete spec → generation → commit history

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **AIOps Integration (Phase 6)**: Depends on basic deployment working (Phase 3+)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all Dockerfile creation tasks together:
Task: "Create multi-stage Dockerfile for Next.js frontend at docker/frontend.Dockerfile"
Task: "Create multi-stage Dockerfile for FastAPI backend + MCP server at docker/backend.Dockerfile"

# Launch all Helm chart creation tasks together:
Task: "Create Helm chart metadata at helm/todo-app/Chart.yaml"
Task: "Create default values file at helm/todo-app/values.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence