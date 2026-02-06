# Event-Driven Architecture Deployment Quickstart

## Prerequisites

- DigitalOcean account with API token
- `doctl` CLI tool installed and authenticated
- `kubectl` installed and configured
- `helm` 3.x installed
- `dapr` CLI installed

## Deployment Steps

### 1. Authenticate with DigitalOcean

```bash
doctl auth init
# Enter your DigitalOcean API token when prompted
```

### 2. Create or Connect to DOKS Cluster

```bash
# Option A: Create new cluster
doctl kubernetes cluster create todo-event-driven-cluster \
  --region nyc1 \
  --node-pool "name=default-pool;size=s-2vcpu-4gb;count=3"

# Option B: Connect to existing cluster
doctl kubernetes cluster kubeconfig save <cluster-name>
```

### 3. Install Dapr on the Cluster

```bash
dapr init -k
# Wait for Dapr to be ready
kubectl wait --for=condition=ready pod -l app=dapr-operator --namespace dapr-system
```

### 4. Deploy Kafka via Bitnami Helm Chart

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

helm install kafka bitnami/kafka \
  --set replicaCount=3 \
  --set zookeeper.enabled=true \
  --set persistence.enabled=true \
  --set persistence.size=10Gi
```

### 5. Deploy Dapr Components

```bash
# Apply Dapr pubsub component for Kafka
kubectl apply -f dapr/components/pubsub.yaml

# Apply Dapr state store component
kubectl apply -f dapr/components/statestore.yaml

# Apply Dapr configuration
kubectl apply -f dapr/config.yaml
```

### 6. Configure Secrets

Create a `secrets-values.yaml` file with your sensitive configuration:

```yaml
secrets:
  neonDbUrl: "your-neon-db-url-here"
  openAiApiKey: "your-openai-api-key-here"
  jwtSecret: "your-jwt-secret-here"
  betterAuthSecret: "your-better-auth-secret-here"
```

### 7. Deploy the Application

```bash
# Build and load Docker images to DOKS
# (This step depends on your specific build process)

# Install the application with Dapr annotations
helm install todo-app helm/todo-app/ \
  --set daprEnabled=true \
  --set backend.replicaCount=2 \
  --set frontend.replicaCount=1 \
  -f secrets-values.yaml
```

### 8. Verify Deployment

```bash
# Check all pods are running
kubectl get pods

# Check Dapr sidecars are injected
kubectl get pods -l dapr.io/enabled=true

# Check services are available
kubectl get svc

# Check HPA is configured
kubectl get hpa
```

## Testing Event Flow

### 1. Access the Application

```bash
# Get the frontend service URL
kubectl get svc todo-frontend-service
```

### 2. Create a Task

1. Access the application in your browser
2. Log in with your credentials
3. Create a new task

### 3. Verify Event Publication

```bash
# Check Kafka for events
kubectl exec -it $(kubectl get pods -l app=kafka -o jsonpath='{.items[0].metadata.name}') -- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic task-events --from-beginning

# Check application logs for event publishing
kubectl logs -l app=todo-backend | grep "Event published"
```

## Scaling Test

### Apply Load to Trigger HPA

```bash
# Monitor HPA status
kubectl get hpa -w

# Apply load (in another terminal)
# Use a load testing tool like hey or wrk
hey -z 5m -c 10 -H "Authorization: Bearer YOUR_TOKEN" -POST http://YOUR_APP_URL/api/v1/tasks -D '{"title":"Load test task", "description":"Created during load test"}'
```

## Cleanup

```bash
# Uninstall application
helm uninstall todo-app

# Uninstall Kafka
helm uninstall kafka

# Remove Dapr
dapr uninstall -k

# Delete cluster (if created for this demo)
doctl kubernetes cluster delete todo-event-driven-cluster
```

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**: Check resource quotas and node capacity
   ```bash
   kubectl describe nodes
   kubectl get quota
   ```

2. **Kafka connectivity issues**: Verify service names and ports
   ```bash
   kubectl get svc | grep kafka
   kubectl describe svc kafka
   ```

3. **Dapr sidecar not injected**: Check deployment annotations
   ```bash
   kubectl get deployment todo-backend -o yaml | grep -A 10 annotations
   ```

4. **HPA not scaling**: Verify metrics server and resource requests/limits
   ```bash
   kubectl top nodes
   kubectl top pods
   kubectl describe hpa
   ```

### Useful Commands

```bash
# Check Dapr sidecars
kubectl get pods -l dapr.io/enabled=true

# View Dapr logs
kubectl logs -l app=dapr -n dapr-system

# Check Dapr status
dapr status -k

# Get cluster events
kubectl get events --sort-by='.lastTimestamp'
```