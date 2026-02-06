# Quickstart Guide: Cloud-Native Event-Driven Todo Application

## Prerequisites

- DigitalOcean account with API token
- `doctl` CLI tool installed and authenticated
- `kubectl` installed and configured
- `helm` 3.x installed
- `dapr` CLI installed
- Docker installed for local image building (if needed)

## Setup and Deployment

### 1. Authenticate with DigitalOcean

```bash
doctl auth init
# Enter your DigitalOcean API token when prompted
```

### 2. Create or Connect to DOKS Cluster

```bash
# Option A: Create new cluster
doctl kubernetes cluster create my-todo-cluster \
  --region nyc1 \
  --node-pool "name=default-node-pool;size=s-2vcpu-4gb;count=3"

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

### 5. Configure Dapr Components

Create the Kafka pub/sub component:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: authRequired
    value: "false"
EOF
```

### 6. Deploy the Application

```bash
# Add your application Helm repository
helm repo add todo-app https://your-repo/charts
helm repo update

# Install the application with Dapr annotation
helm install todo-app todo-app/todo-app \
  --set daprEnabled=true \
  --set kafka.broker=kafka:9092 \
  --set hpa.enabled=true \
  --set hpa.minReplicas=1 \
  --set hpa.maxReplicas=10 \
  --set hpa.targetCPUUtilizationPercentage=70
```

## Using AIOps Tools

### Generate HPA Configuration with kubectl-ai

```bash
kubectl ai create hpa todo-backend \
  --from-deployment todo-backend \
  --cpu-percent 70 \
  --min 1 \
  --max 10
```

### Troubleshoot with kubectl-ai

```bash
kubectl ai explain "pods in CrashLoopBackOff"
kubectl ai generate "network policy to isolate kafka from frontend"
```

## Verification Steps

### 1. Check All Resources Are Running

```bash
kubectl get pods
kubectl get svc
kubectl get hpa
dapr status -k
```

### 2. Verify Event Flow

```bash
# Check Kafka topics
kubectl exec -it $(kubectl get pods -l app=kafka -o jsonpath='{.items[0].metadata.name}') -- kafka-topics.sh --list --bootstrap-server localhost:9092

# Check application logs for event processing
kubectl logs -l app=todo-backend --since=10m
```

### 3. Test Application Functionality

1. Access the application via the frontend service
2. Log in with your credentials
3. Create a task and observe the event in Kafka
4. Verify that the task appears in your task list

## Scaling Test

### Simulate Load and Observe HPA

```bash
# Monitor HPA status
kubectl get hpa -w

# Apply load to trigger scaling (in another terminal)
while true; do
  curl -H "Authorization: Bearer YOUR_TOKEN" \
       -X POST https://your-app-url/api/tasks \
       -d '{"title":"Load test task", "description":"Created during load test"}'
  sleep 0.1
done
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
doctl kubernetes cluster delete my-todo-cluster
```

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**: Check resource quotas and node capacity
2. **Kafka connectivity issues**: Verify service names and ports
3. **Dapr sidecar not injected**: Check deployment annotations
4. **HPA not scaling**: Verify metrics server and resource requests/limits

### Useful Commands

```bash
# Check Dapr sidecars
kubectl get pods -l dapr.io/enabled=true

# View Dapr logs
kubectl logs -l app=dapr -n dapr-system

# Check Kafka connectivity from application
dapr logs todo-backend

# Get cluster events
kubectl get events --sort-by='.lastTimestamp'
```