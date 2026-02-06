# Data Model: Phase IV – Local Kubernetes Deployment

**Date**: 2026-01-20
**Feature**: Phase IV – Local Kubernetes Deployment
**Branch**: 001-k8s-deployment

## Overview

This document describes the data model for the Kubernetes deployment artifacts and their relationships. The application data model remains unchanged from Phase III, but this document focuses on the deployment and infrastructure entities.

## Application Data Entities (Preserved from Phase III)

### User
- **Fields**: id, email, name, created_at, updated_at
- **Validation**: Email format, uniqueness
- **Relationships**: Owns multiple Tasks and Conversations

### Task
- **Fields**: id, title, description, status, user_id, created_at, updated_at
- **Validation**: Title required, status enum (todo, in_progress, done)
- **Relationships**: Belongs to User

### Conversation
- **Fields**: id, user_id, title, created_at, updated_at
- **Validation**: Title required
- **Relationships**: Belongs to User, contains multiple Messages

### Message
- **Fields**: id, conversation_id, role, content, timestamp
- **Validation**: Role enum (user, assistant), content required
- **Relationships**: Belongs to Conversation

## Deployment Infrastructure Entities

### DockerImage
- **Fields**: name, tag, registry, build_context, dockerfile_path, build_args
- **Validation**: Name follows Docker naming conventions, tag is valid semantic version
- **Relationships**: Referenced by Container in Deployment

### KubernetesDeployment
- **Fields**: name, namespace, replicas, selector_labels, template_spec
- **Validation**: Replicas within defined limits, valid Kubernetes resource names
- **Relationships**: Contains multiple Containers, references Services, ConfigMaps, Secrets

### KubernetesService
- **Fields**: name, namespace, service_type, ports, selector
- **Validation**: Port ranges valid, service type enum (ClusterIP, NodePort, LoadBalancer)
- **Relationships**: Maps to Deployment, exposes Ports

### KubernetesSecret
- **Fields**: name, namespace, data (key-value pairs), type
- **Validation**: Data properly encoded, follows Kubernetes naming conventions
- **Relationships**: Referenced by Deployment, stores sensitive configuration

### HelmChart
- **Fields**: name, version, description, dependencies, maintainers, kube_version
- **Validation**: Semantic versioning, valid chart structure
- **Relationships**: Contains multiple Templates, Values, Dependencies

### HelmValues
- **Fields**: image_tag, replica_count, resource_limits, resource_requests, environment_vars
- **Validation**: Values within acceptable ranges, proper format
- **Relationships**: Applied to HelmChart, overrides default parameters

## State Transitions

### Pod Lifecycle States
- Pending → Running → Terminating → Deleted
- Pending → Failed (error condition)
- Running → CrashLoopBackOff (restart policy handling)

### Deployment States
- Created → Progressing → Available → Ready
- Progressing → Failed (rollback trigger)

## Relationships

```
HelmChart --[contains]--> Templates
Templates --[define]--> KubernetesDeployment
Templates --[define]--> KubernetesService
Templates --[define]--> KubernetesSecret
KubernetesDeployment --[references]--> DockerImage
KubernetesDeployment --[exposes]--> KubernetesService
KubernetesDeployment --[uses]--> KubernetesSecret
KubernetesService --[selects]--> KubernetesDeployment
```

## Constraints

### Data Integrity
- All application data continues to be stored in Neon PostgreSQL
- No application state stored in Kubernetes volumes (stateless requirement)
- Database connections managed via environment variables

### Security
- Sensitive configuration stored only in Kubernetes Secrets
- No hardcoded credentials in any deployment files
- Proper RBAC configuration for all resources

### Scalability
- All application components must support horizontal scaling
- Database connection pooling implemented for multiple replicas
- Session data stored externally (Neon PostgreSQL)

## Validation Rules

### From Functional Requirements
- FR-005: Conversation state persists across pod restarts (validated via Neon PostgreSQL)
- FR-006: Horizontal scaling supported to at least 3 replicas (validated via Deployment configuration)
- FR-004: Sensitive configuration via Kubernetes Secrets (validated via Secret resources)

### Deployment Validation
- All resources must pass Kubernetes validation
- Helm chart must pass linting and dry-run tests
- Secrets must not be stored in plain text in repository