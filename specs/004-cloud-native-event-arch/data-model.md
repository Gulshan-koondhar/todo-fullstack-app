# Data Model: Cloud-Native Event-Driven Architecture

## Event Structures

### Task Event
Represents a task-related action that is published to Kafka and processed asynchronously.

**Fields**:
- `eventId`: Unique identifier for the event (UUID)
- `eventType`: Type of event (CREATE_TASK, UPDATE_TASK, COMPLETE_TASK, DELETE_TASK)
- `taskId`: Identifier of the affected task (UUID)
- `userId`: Identifier of the user who triggered the event (UUID)
- `timestamp`: When the event was created (ISO 8601)
- `payload`: Event-specific data (object)
- `correlationId`: For tracking related events (UUID)
- `version`: Schema version (string)

**Validation rules**:
- `eventId` must be a valid UUID
- `eventType` must be one of the allowed values
- `timestamp` must be in ISO 8601 format
- `payload` structure varies by event type

**State transitions**:
- Event created → Published to Kafka → Processed by consumers → Acknowledged

### Task Event Payload
Structure of the payload field in Task Event based on event type.

**CREATE_TASK payload**:
- `title`: Task title (string, max 200 chars)
- `description`: Task description (string, max 1000 chars)
- `createdAt`: Task creation time (ISO 8601)

**UPDATE_TASK payload**:
- `title`: Updated task title (string, max 200 chars)
- `description`: Updated task description (string, max 1000 chars)
- `updatedAt`: Task update time (ISO 8601)

**COMPLETE_TASK payload**:
- `completedAt`: Task completion time (ISO 8601)
- `completedBy`: User who completed the task (UUID)

**DELETE_TASK payload**:
- `deletedAt`: Task deletion time (ISO 8601)

## User Session
Represents an authenticated user's interaction with the system, maintained across the cloud-native infrastructure.

**Fields**:
- `sessionId`: Unique session identifier (UUID)
- `userId`: Associated user identifier (UUID)
- `token`: JWT token for authentication (string)
- `createdAt`: Session creation time (ISO 8601)
- `expiresAt`: Session expiration time (ISO 8601)
- `lastActivity`: Last activity timestamp (ISO 8601)
- `clientInfo`: Information about the client device (object)

**Validation rules**:
- `sessionId` must be a valid UUID
- `token` must be a valid JWT
- `expiresAt` must be after `createdAt`

## Cloud Deployment Configuration
Represents the Kubernetes, Dapr, and Kafka configurations that enable the event-driven architecture.

**Fields**:
- `deploymentId`: Unique identifier for the deployment (string)
- `environment`: Deployment environment (dev/staging/prod)
- `daprComponents`: List of configured Dapr components (array of objects)
- `kafkaTopics`: List of configured Kafka topics (array of strings)
- `scalingConfig`: HPA configuration parameters (object)
- `securityConfig`: Security-related configurations (object)
- `createdBy`: User who initiated the deployment (UUID)

**Validation rules**:
- `deploymentId` must be unique
- `environment` must be one of the allowed values
- `daprComponents` must have valid Dapr component configurations
- `kafkaTopics` must follow naming conventions

## Kafka Topic Schema
Definition of Kafka topics used in the system.

**Task Events Topic**:
- Name: `task-events`
- Partitions: Configurable based on expected load
- Replication factor: 3 for durability
- Message retention: 7 days
- Key: userId for partitioning
- Value: Task Event JSON structure

**Processing Events Topic**:
- Name: `processing-events`
- Partitions: Configurable based on expected load
- Replication factor: 3 for durability
- Message retention: 3 days
- Key: taskId for partitioning
- Value: Processing Event JSON structure

## Dapr Component Configuration
Structure of Dapr component configurations.

**Pub/Sub Component**:
- `name`: Component name (string)
- `type`: Component type (pubsub.kafka, pubsub.rabbitmq, etc.)
- `version`: Component version (string)
- `metadata`: Component-specific metadata (object)

**State Store Component**:
- `name`: Component name (string)
- `type`: Component type (state.redis, state.mongodb, etc.)
- `version`: Component version (string)
- `metadata`: Component-specific metadata (object)

**Secret Store Component**:
- `name`: Component name (string)
- `type`: Component type (secretstores.kubernetes, secretstores.hashicorp.vault, etc.)
- `version`: Component version (string)
- `metadata`: Component-specific metadata (object)