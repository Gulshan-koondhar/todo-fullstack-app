<!--
Sync Impact Report
=================
Version: 1.2.0 → 1.3.0
Change: Updated constitution to emphasize event-driven architecture, cloud-native deployment, and AIOps-first operations for Phase V
Modified Principles: All principles updated to reflect Phase V requirements
Added Sections: Event-Driven Architecture Focus, Dapr Integration, Kafka Event Handling, AIOps-First Operations
Removed Sections: Phase IV specific local Kubernetes details
Templates Updated:
  ⚠️  plan-template.md - Needs update to reflect event-driven architecture requirements
  ⚠️  spec-template.md - Needs update to reflect event-driven requirements
  ⚠️  tasks-template.md - Needs update to reflect event-driven tasks
  ⚠️  phr-template.prompt.md - May need updates for event-driven context
Follow-up TODOs: None
-->

# Phase V – Cloud-Native Deployment with Event-Driven Architecture (Spec-Driven Development) Constitution

## Core Principles

### I. Spec-Driven Cloud Deployment Only Using Claude Code and Spec-Kit Plus
All deployment artifacts (Helm charts, Dapr components, Kafka manifests) MUST be generated exclusively by Claude Code from refined specs. No manual editing of YAML, Dockerfiles, or Helm files is permitted — only spec iteration is allowed. All deployment components MUST be generated from specifications through the Claude Code workflow.

**Rationale**: Ensures deterministic, traceable deployment configurations while maintaining separation of concerns between infrastructure definitions and manual intervention.

### II. Event-Driven Decoupling with Reusable Components for Pub/Sub and Service Invocation
All system components MUST be decoupled through event-driven architecture using reusable components for pub/sub and service invocation. Events MUST be published to Kafka topics and consumed by interested services via Dapr pub/sub. Service-to-service communication MUST utilize Dapr service invocation for loose coupling and resilience.

**Rationale**: Ensures scalable, resilient architecture with loose coupling between services and proper separation of concerns.

### III. Scalability and Resilience in Managed Kubernetes Environments
All application components MUST be designed for horizontal scalability and resilience in managed Kubernetes environments. Applications MUST gracefully handle scale-out and scale-in operations. Health checks and proper readiness/liveness probes MUST be implemented for all services. Horizontal Pod Autoscaler configurations MUST be defined where appropriate.

**Rationale**: Ensures the system can grow with demand and maintain availability during infrastructure changes in production environments.

### IV. Reusability of Intelligence Through Dapr Sidecars, Kafka Topics, and Cloud-Native Blueprints
Infrastructure intelligence MUST be reusable through Dapr sidecars, Kafka topics, and cloud-native deployment blueprints. Dapr components MUST be structured for reusability across different environments. All Kubernetes deployments MUST leverage Helm and Dapr for consistent, configurable deployment experiences.

**Rationale**: Enables rapid deployment across environments and promotes infrastructure-as-code best practices with enhanced service mesh capabilities.

### V. AIOps-First Operations for Generation, Troubleshooting, and Optimization
AIOps tools MUST be leveraged for manifest generation, troubleshooting, and scaling operations from the outset. Usage of kubectl-ai and kagent MUST be documented in specifications. All AIOps prompts and interactions MUST be recorded for reproducibility and learning. At least one deployment task MUST utilize AIOps tools.

**Rationale**: Accelerates operations and reduces manual intervention while building institutional knowledge and enabling intelligent automation.

### VI. Security-First Approach with Cloud-Native Secrets Management
Sensitive values (API keys, DB credentials, JWT secrets) MUST be managed exclusively via cloud-native tools like DOKS secrets and Dapr secrets. Secrets and environment variables MUST never be hardcoded in code or manifests. All sensitive configuration MUST be injected at runtime through cloud-native mechanisms. No plaintext secrets in source code or deployment files.

**Rationale**: Ensures secure handling of sensitive data and prevents accidental exposure of credentials in cloud environments.

## Technology Stack & Constraints

### Locked Technology Stack
- **Orchestration**: DigitalOcean Kubernetes (DOKS) managed cluster
- **Event Streaming**: Kafka (via Bitnami Helm chart) for pub/sub messaging
- **Service Mesh**: Dapr for service invocation and pub/sub capabilities
- **Container Runtime**: Existing Phase IV Docker images (no rebuild required)
- **Package Manager**: Helm 3.x with Dapr and Kafka subcharts
- **Database**: Neon Serverless PostgreSQL (external persistence)
- **Development Tool**: Claude Code for all manifest and configuration generation

### Event-Driven Architecture Requirements
- All task operations MUST publish events to Kafka topics
- Event consumers MUST be implemented as Dapr pub/sub subscribers
- Event schemas MUST be defined and validated consistently
- Dead letter queues MUST be configured for failed event processing
- Event correlation IDs MUST be maintained across service boundaries
- Exactly-once or at-least-once delivery semantics MUST be configured appropriately

### Dapr Integration Requirements
- Dapr sidecars MUST be configured for all services requiring pub/sub or service invocation
- Dapr components MUST be defined for Kafka pub/sub and secret stores
- Service invocation MUST be used for synchronous communication between services
- Dapr state management MAY be used for transient state where appropriate
- Dapr configuration MUST be environment-specific with proper values overrides

### Kubernetes Deployment Requirements
- All Kubernetes manifests MUST be generated by Claude Code from specs
- Helm charts MUST support configurable values for different environments
- Deployments MUST include proper resource limits and requests for cloud environments
- Services MUST be configured for proper internal communication via Dapr
- Horizontal Pod Autoscalers MUST be configured for stateless services
- Network policies MUST be implemented for enhanced security in cloud environments

### Security Requirements
- All sensitive data MUST be stored in cloud-native secrets (DOKS secrets, Dapr secrets)
- No hardcoded credentials in any deployment files
- Proper RBAC configurations MUST be defined for all components
- Network policies MUST be implemented for enhanced security
- Pod security standards MUST be followed in managed environment
- Dapr security features (MTLS, component authentication) MUST be enabled

### Container Requirements
- Existing Phase IV Docker images MUST be reused (no rebuild required)
- Images MUST be compatible with managed Kubernetes environments
- Proper health checks MUST be implemented for all services
- Proper startup probes MUST be configured for all applications
- Resource constraints MUST be appropriate for cloud environments

### Event Handling Requirements
- Event publishing MUST be decoupled from business logic
- Event consumers MUST be idempotent and handle duplicate events gracefully
- Event schemas MUST be versioned and backward compatible
- Event processing MUST be monitored and logged appropriately
- Circuit breaker patterns MUST be implemented for resilience

### AIOps Integration Requirements
- AIOps tools usage MUST be documented in specs
- Prompts used with kubectl-ai/kagent MUST be recorded
- AIOps-generated resources MUST be validated before deployment
- At least one resource MUST be generated using AIOps tools
- Troubleshooting activities MUST leverage AIOps where applicable
- Deployment optimization MUST utilize AIOps recommendations

### Monorepo Organization
- Dapr configurations: `/dapr/` directory
- Kafka manifests: `/kafka/` directory
- Helm charts: `/helm/` directory
- Specs: `/specs/001-event-driven-architecture/` directory
- All changes MUST preserve Phase IV functionality

### Functional Constraints
- Cloud deployment only: DigitalOcean Kubernetes (managed service)
- No breaking changes to existing backend APIs or database schema
- All Phase IV functionality MUST remain preserved (multi-user, authentication, AI chatbot)
- Focus on Basic Level features with event-driven extensions
- Event-driven patterns limited to basic pub/sub (task events, notifications)

## Success Criteria

### Cloud Deployment Validation
- Full application (login, task CRUD, AI chatbot) runs reliably in DOKS
- Kubernetes manifests deploy without errors in managed environment
- All services are accessible within the cluster via Dapr
- External database connections are properly established
- Dapr sidecars initialize and communicate correctly

### Event-Driven Architecture Validation
- Event flow works correctly (e.g., add task → publish event → consume/log)
- Event consumers process messages reliably without duplicates or losses
- Pub/sub patterns function as expected with proper topic configuration
- Service invocation works correctly between services via Dapr
- Event-driven extensions enhance functionality without breaking existing features

### Scalability Validation
- Horizontal scaling demonstrated with multiple replicas of stateless services
- Load distribution works correctly across replicas with Dapr service invocation
- Event processing scales appropriately with consumer groups
- Resource utilization remains stable during scaling operations
- Horizontal Pod Autoscaler configured and functioning in DOKS

### Security Validation
- Cloud-native secrets properly injected and used (DB connection, OpenAI key, JWT)
- No plaintext secrets visible in Kubernetes resources or Dapr configurations
- Proper access controls implemented in managed environment
- Security scanning passes without high/critical vulnerabilities
- Dapr security features properly configured and operational

### AIOps Integration Validation
- AIOps tools used to generate or debug at least one resource
- kubectl-ai or kagent commands successfully executed for deployment tasks
- AIOps-generated configurations are functional in cloud environment
- Documentation of AIOps usage included in specs
- AIOps-assisted troubleshooting demonstrated

### Demo Validation
- Demo shows: DOKS cluster setup, Helm install with Dapr/Kafka, app access, event flow demonstration
- Complete spec → generation → commit history proving iterative, non-manual development
- All Phase IV functionality remains operational with event-driven enhancements
- No manual edits to generated files
- Event-driven features demonstrated working correctly

## Agentic Dev Stack Workflow

### Workflow Stages
1. **Spec Creation**: User provides feature description → Claude generates spec.md with user stories, requirements, and success criteria
2. **Planning**: Claude generates plan.md with architecture, data models, API contracts, and implementation strategy
3. **Task Generation**: Claude generates tasks.md with testable, ordered tasks grouped by user story
4. **Implementation**: Claude executes tasks.md sequentially, implementing all code

### Documentation Requirements
- Every feature gets its own spec.md before implementation
- Public GitHub repository MUST contain:
  - Constitution (this file)
  - Full specs history in `specs/` directory
  - All generated code
  - CLAUDE.md files for agent guidance
- CLAUDE.md MUST follow the SpecKit Plus structure
- AIOps usage MUST be documented with prompts and outcomes
- Event-driven architecture decisions MUST be recorded

### Success Criteria Tracking
- Application deploys successfully to DOKS using Helm charts with Dapr and Kafka
- Kubernetes manifests generated exclusively through Claude Code
- Event-driven architecture validated through pub/sub testing
- Cloud-native secrets properly managed through DOKS and Dapr
- Horizontal scaling demonstrated with multiple replicas in managed environment
- AIOps tools utilized for at least one resource generation or deployment task
- All Phase IV features remain fully functional in cloud deployment
- No manual edits to generated Kubernetes manifests, Dapr configs, or Kafka manifests
- Working multi-user web application with full CRUD for tasks in cloud environment
- Event-driven extensions (task events, notifications) functioning correctly
- Users can only view, create, update, and delete their own tasks
- Backend API secured with JWT verification and user filtering in DOKS
- Successful demonstration showing cloud deployment, event flow, and scalability

## Governance

### Constitution Authority
This constitution supersedes all other practices and guidelines in the project. All development decisions MUST be evaluated against these principles. Any ambiguity MUST be resolved by prioritizing security, event-driven architecture, and spec-driven workflow.

### Amendment Process
1. Propose amendment with clear justification and impact analysis
2. Document the change rationale, affected artifacts, and migration strategy
3. Verify that changes do not violate core security and event-driven principles
4. Update constitution version following semantic versioning:
   - MAJOR: Backward-incompatible principle removals or redefinitions
   - MINOR: New principle added or material expansion of guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements
5. Propagate changes to dependent templates (plan, spec, tasks)
6. Maintain full amendment history in governance section

### Compliance Verification
- All PRs MUST verify compliance with constitution principles
- Complexity or deviations from principles MUST be explicitly justified
- Constitution Check in plan.md MUST be completed before implementation
- Any bypass of spec-driven workflow MUST be documented and approved
- Event-driven architecture best practices MUST be verified before deployment
- Cloud-native security practices MUST be validated before production deployment

### Runtime Development Guidance
Use CLAUDE.md in the repository root for agent-specific runtime guidance. Constitution provides the principles; CLAUDE.md provides operational context for cloud-native, event-driven deployment.

**Version**: 1.3.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-02-02