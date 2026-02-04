# Research Findings: Phase IV – Local Kubernetes Deployment

**Date**: 2026-01-20
**Feature**: Phase IV – Local Kubernetes Deployment
**Branch**: 001-k8s-deployment

## Overview

This document captures research findings and decisions made during the planning phase for containerizing and deploying the AI Todo Chatbot application to a local Minikube cluster.

## Key Decisions

### 1. Dockerfile Architecture
**Decision**: Implement multi-stage Dockerfiles for both frontend and backend with optimized builds
**Rationale**: Multi-stage builds reduce attack surface, optimize image size, and follow security best practices
**Alternatives considered**:
- Single-stage builds (rejected - larger images, more vulnerabilities)
- Pre-built images from third-party sources (rejected - trust and security concerns)

### 2. Kubernetes Service Configuration
**Decision**: Use ClusterIP for internal services and NodePort/LoadBalancer for external access
**Rationale**: ClusterIP provides secure internal communication while NodePort enables external access in Minikube
**Alternatives considered**:
- Direct LoadBalancer (rejected - not suitable for local Minikube)
- ExternalIP services (rejected - unnecessary complexity)

### 3. Secret Management Strategy
**Decision**: Use Kubernetes Secrets with envFrom to inject sensitive configuration
**Rationale**: Best practice for managing sensitive data in Kubernetes, aligns with security-first principle
**Alternatives considered**:
- ConfigMaps for secrets (rejected - not secure)
- Hardcoded values (rejected - violates security principle)

### 4. Health Checks Implementation
**Decision**: Implement liveness and readiness probes for all deployments
**Rationale**: Essential for Kubernetes to manage pod lifecycle and ensure application reliability
**Alternatives considered**:
- No health checks (rejected - poor resilience)
- Startup probes only (rejected - insufficient monitoring)

### 5. Ingress Strategy
**Decision**: Use basic Ingress with Minikube ingress addon for external access
**Rationale**: Provides clean URL structure and supports future expansion
**Alternatives considered**:
- NodePort services only (rejected - less flexible)
- Port forwarding (rejected - not suitable for demo)

## Technical Specifications

### Frontend Dockerfile Strategy
- Use node:18-alpine as base image for smaller footprint
- Implement build stage with dependency installation and build
- Copy only built assets to production stage
- Run as non-root user for security

### Backend Dockerfile Strategy
- Use python:3.11-slim as base image
- Multi-stage build with requirements installation in intermediate layer
- Copy application code and dependencies separately for caching
- Expose port 8000 for FastAPI
- Include MCP server in same container or separate (to be determined)

### Helm Chart Structure
- Parameterize image tags, replica counts, and resource limits
- Use conditional templates for optional components
- Include default values that work for local development
- Support overrides for different environments

## Architecture Considerations

### Statelessness Validation
- Ensure no session state stored in pod filesystem
- Verify Neon PostgreSQL handles all persistent data
- Test conversation persistence across pod restarts

### Scaling Strategy
- Configure Horizontal Pod Autoscaler (HPA) for backend
- Set appropriate resource requests and limits
- Ensure stateless design supports multiple replicas
- Validate shared database connection handling

### AIOps Integration Points
- Use kubectl-ai for generating initial manifests
- Leverage kagent for troubleshooting deployment issues
- Document prompts and responses for reproducibility

## Risks and Mitigations

### Risk: Database Connection Issues
**Mitigation**: Implement proper connection pooling and retry logic
**Impact**: Medium - could affect application availability

### Risk: Resource Constraints in Minikube
**Mitigation**: Configure appropriate resource limits and requests
**Impact**: Medium - could prevent deployment

### Risk: Secret Management Failures
**Mitigation**: Validate secret injection before deployment
**Impact**: High - could expose sensitive data

## Dependencies

### Required Tools
- Docker (version 20+)
- Minikube (latest stable)
- kubectl (matching Minikube version)
- Helm 3.x
- kubectl-ai plugin (for AIOps integration)

### External Services
- Neon PostgreSQL (existing from Phase III)
- OpenAI API (existing from Phase III)
- Minikube cluster (local)

## Next Steps

1. Generate Dockerfiles based on research findings
2. Create Kubernetes manifests for deployments and services
3. Develop Helm chart with configurable parameters
4. Implement secret management strategy
5. Test local deployment workflow