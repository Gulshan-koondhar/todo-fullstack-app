# Event-Driven Architecture Documentation

## Overview

This document describes the event-driven architecture implemented in the AI Todo Chatbot application using Dapr and Kafka for cloud-native deployment on DigitalOcean Kubernetes (DOKS).

## Architecture Components

### 1. Event Publishers
- **Location**: Backend API endpoints in `tasks.py`
- **Function**: Publish task-related events to Kafka via Dapr pub/sub
- **Events Published**:
  - `CREATE_TASK`: When a new task is created
  - `UPDATE_TASK`: When an existing task is updated
  - `COMPLETE_TASK`: When a task is marked as completed
  - `DELETE_TASK`: When a task is deleted

### 2. Event Consumers
- **Location**: `src/mcp_tools/event_consumer.py`
- **Function**: Handle incoming events from Kafka topics
- **Current Handlers**:
  - `handle_task_created_event`: Processes task creation events
  - `handle_task_updated_event`: Processes task update events
  - `handle_task_completed_event`: Processes task completion events
  - `handle_task_deleted_event`: Processes task deletion events

### 3. Message Broker
- **Technology**: Apache Kafka (via Bitnami Helm chart)
- **Topic**: `task-events`
- **Partitions**: 3 for scalability
- **Replication Factor**: 3 for durability

### 4. Service Mesh
- **Technology**: Dapr (Distributed Application Runtime)
- **Components**:
  - Pub/Sub component connecting to Kafka
  - Service invocation for inter-service communication
  - Configuration for tracing and metrics

## Event Structure

### TaskEvent Schema
```json
{
  "event_id": "uuid",
  "event_type": "CREATE_TASK | UPDATE_TASK | COMPLETE_TASK | DELETE_TASK",
  "task_id": "string",
  "user_id": "string",
  "timestamp": "ISO 8601 datetime",
  "payload": {
    // Event-specific data
  },
  "correlation_id": "uuid",
  "version": "string"
}
```

### Payload Structures

#### CREATE_TASK Payload
```json
{
  "title": "string",
  "description": "string | null",
  "created_at": "ISO 8601 datetime"
}
```

#### UPDATE_TASK Payload
```json
{
  "title": "string | null",
  "description": "string | null",
  "updated_at": "ISO 8601 datetime"
}
```

#### COMPLETE_TASK Payload
```json
{
  "completed_at": "ISO 8601 datetime",
  "completed_by": "string"
}
```

#### DELETE_TASK Payload
```json
{
  "deleted_at": "ISO 8601 datetime"
}
```

## Implementation Details

### Event Publishing
Events are published synchronously after successful database operations in the backend API. If event publishing fails, a warning is logged but the main operation continues to ensure application availability.

### Dapr Configuration
Dapr sidecars are injected into both frontend and backend deployments with the following annotations:
- `dapr.io/enabled: "true"`
- `dapr.io/app-id: "todo-backend"` or `"todo-frontend"`
- `dapr.io/app-port: "8000"` or `"3000"`
- `dapr.io/config: "dapr-config"`

### Horizontal Pod Autoscaling
HPA is configured for both frontend and backend services based on CPU and memory utilization:
- Min replicas: 2
- Max replicas: 5
- Target CPU utilization: 80%
- Target memory utilization: 80%

## Deployment Structure

### Helm Charts
- Main application: `helm/todo-app/`
- Dapr components: `helm/dapr-components/`
- Kafka: Deployed via Bitnami Kafka Helm chart

### Dapr Components
Located in `dapr/` directory:
- `components/pubsub.yaml`: Kafka pub/sub configuration
- `components/statestore.yaml`: State store configuration
- `config.yaml`: Dapr configuration for tracing and secrets

## Operational Considerations

### Monitoring
- Dapr logs provide insights into component health and event processing
- Application logs track event publishing success/failure
- Kafka logs show message throughput and broker health

### Scaling
- The event-driven architecture supports horizontal scaling of application services
- Kafka partitioning allows for parallel event processing
- HPA ensures adequate resources during high event throughput

### Resilience
- Event publishing failures are logged but don't block primary operations
- Kafka's replication ensures message durability
- Dapr's retry mechanisms handle transient failures

## Future Enhancements

- Add dead letter queues for failed event processing
- Implement event sourcing patterns for audit trails
- Add event schema validation
- Implement event replay capabilities for debugging