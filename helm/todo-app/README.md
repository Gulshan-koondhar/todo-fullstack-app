# Todo App Helm Chart

A Helm chart for deploying the AI Todo Chatbot application to Kubernetes.

## Chart Details

This chart deploys a full-stack application consisting of:
- Next.js frontend
- FastAPI backend with MCP server
- Required secrets for database and API keys

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Minikube or a Kubernetes cluster

## Installing the Chart

To install the chart with the release name `todo-app`:

```bash
# First, ensure you have the required secrets in your values file
# Create a secrets-values.yaml file with your sensitive information:

cat <<EOF > secrets-values.yaml
secrets:
  neonDbUrl: "your-neon-db-url-here"
  openAiApiKey: "your-openai-api-key-here"
  jwtSecret: "your-jwt-secret-here"
  betterAuthSecret: "your-better-auth-secret-here"
EOF

# Install the chart
helm install todo-app . -f secrets-values.yaml
```

## Uninstalling the Chart

To uninstall/delete the `todo-app` deployment:

```bash
helm delete todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

| Parameter                       | Description                                            | Default                          |
|-------------------------------|--------------------------------------------------------|----------------------------------|
| `frontend.image.repository`   | Frontend image repository                              | `todo-frontend`                 |
| `frontend.image.tag`          | Frontend image tag                                     | `latest`                        |
| `frontend.replicaCount`       | Number of frontend replicas                            | `1`                             |
| `frontend.service.type`       | Frontend service type                                  | `ClusterIP`                     |
| `frontend.service.port`       | Frontend service port                                  | `80`                            |
| `backend.image.repository`    | Backend image repository                               | `todo-backend`                  |
| `backend.image.tag`           | Backend image tag                                      | `latest`                        |
| `backend.replicaCount`        | Number of backend replicas                             | `2`                             |
| `backend.service.type`        | Backend service type                                   | `ClusterIP`                     |
| `backend.service.port`        | Backend service port                                   | `8000`                          |
| `backend.autoscaling.enabled` | Enable Horizontal Pod Autoscaler for backend          | `true`                          |
| `backend.autoscaling.minReplicas` | Minimum number of backend replicas                 | `2`                             |
| `backend.autoscaling.maxReplicas` | Maximum number of backend replicas                 | `5`                             |
| `ingress.enabled`             | Enable ingress resource                                | `true`                          |
| `ingress.hosts[0].host`       | Hostname for ingress                                  | `todo.local`                    |

## Secrets Configuration

The chart expects the following secrets to be provided:

- `neonDbUrl`: Neon PostgreSQL database connection string
- `openAiApiKey`: OpenAI API key
- `jwtSecret`: JWT secret for authentication
- `betterAuthSecret`: Better Auth secret

These should be provided in a values file during installation to avoid exposing sensitive information.

## Scaling

The backend deployment is configured with Horizontal Pod Autoscaler by default. You can adjust the scaling parameters in the values file:

```yaml
backend:
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilizationPercentage: 80
```

## Health Checks

Both frontend and backend deployments include liveness and readiness probes to ensure application health and proper traffic routing.