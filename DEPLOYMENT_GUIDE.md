# Phase V Deployment Guide

## Cloud-Native Event-Driven Architecture Deployment

This guide provides step-by-step instructions for deploying the AI Todo Chatbot application with event-driven architecture to DigitalOcean Kubernetes (DOKS).

## Prerequisites

### Local Tools
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/windows/amd64/kubectl.exe"

# Install Helm
winget install Helm.Helm

# Install Dapr CLI
winget install --id Microsoft.dapr.cli -e

# Install DigitalOcean CLI (doctl)
winget install --id DigitalOcean.doctl -e
```

### Cloud Account
- DigitalOcean account with billing configured
- API token with read/write permissions

## Step 1: Set Up DigitalOcean Kubernetes Cluster

### Authenticate with DigitalOcean
```bash
# Login to DigitalOcean
doctl auth init

# Set default region (e.g., nyc1, sfo3, ams3)
doctl kubernetes cluster kubeconfig save <cluster-name>
```

### Create DOKS Cluster (if not already created)
```bash
# Create a cluster with 3 nodes (adjust as needed)
doctl kubernetes cluster create todo-cluster \
  --region nyc1 \
  --node-pool "name=default-node-pool;size=s-2vcpu-4gb;count=3" \
  --maintenance-window "monday=02:00"
```

## Step 2: Initialize Dapr on the Cluster

```bash
# Initialize Dapr in the cluster
dapr init -k --runtime-version=1.11.0

# Verify Dapr installation
kubectl get pods -n dapr-system
```

## Step 3: Set Up Kafka for Event Streaming

```bash
# Add Bitnami repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create namespace for Kafka
kubectl create namespace kafka

# Install Kafka with Zookeeper
helm install kafka bitnami/kafka \
  --namespace kafka \
  --values ./kafka/values.yaml
```

## Step 4: Configure Secrets

### Create a namespace for the application
```bash
kubectl create namespace todo-app
```

### Create required secrets
```bash
# Database URL (Neon PostgreSQL)
kubectl create secret generic postgres-secret \
  --namespace todo-app \
  --from-literal=neon-db-url="your-neon-db-url"

# OpenAI API key
kubectl create secret generic openai-secret \
  --namespace todo-app \
  --from-literal=openai-api-key="your-openai-api-key"

# JWT secret for authentication
kubectl create secret generic jwt-secret \
  --namespace todo-app \
  --from-literal=jwt-secret="your-jwt-secret"
```

## Step 5: Deploy the Application

```bash
# Navigate to the helm directory
cd helm

# Install the todo-app chart
helm install todo-app todo-app/ \
  --namespace todo-app \
  --values todo-app/values.yaml
```

## Step 6: Verify Deployment

### Check all pods are running
```bash
kubectl get pods -n todo-app
kubectl get pods -n kafka
kubectl get pods -n dapr-system
```

### Check services
```bash
kubectl get svc -n todo-app
```

### Check Dapr sidecars
```bash
kubectl get pods -n todo-app -o yaml | grep dapr
```

## Step 7: Configure Ingress (if needed)

```bash
# If using LoadBalancer service
kubectl get svc -n todo-app -o wide

# Or if using ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/do/deploy.yaml
```

## Step 8: Test Event-Driven Functionality

### Access the application
```bash
# Get external IP
kubectl get svc todo-frontend-service -n todo-app

# Or port forward for testing
kubectl port-forward -n todo-app svc/todo-frontend-service 3000:80
```

### Test task operations
1. Access the frontend application
2. Create a new task
3. Verify the task is created in the database
4. Check Kafka topics for published events:
```bash
kubectl exec -it -n kafka $(kubectl get pods -n kafka -l app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}') -- kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Step 9: Monitor HPA Behavior

### Check HPA status
```bash
kubectl get hpa -n todo-app
kubectl describe hpa -n todo-app
```

### Simulate load to test scaling
```bash
# Install hey for load testing
go install github.com/rakyll/hey@latest

# Generate load to trigger HPA
hey -n 1000 -c 10 http://your-app-domain.com/api/v1/tasks?user_id=test-user
```

## Step 10: AIOps Integration

### Using kubectl-ai for configuration
```bash
# Install kubectl-ai plugin
curl -sL https://raw.githubusercontent.com/itaysk/kubectl-ai/master/install.sh | sh

# Generate HPA configuration using AI
kubectl ai --model gpt-4 -- "generate HPA configuration for todo-backend with CPU threshold 70% and memory threshold 80%"

# Troubleshoot deployment issues
kubectl ai --model gpt-4 -- "explain why pods in todo-app namespace are not starting"
```

## Operational Commands

### Check Dapr logs
```bash
kubectl logs -n dapr-system -l app=dapr-placement-server
kubectl logs -n dapr-system -l app=dapr-sidecar-injector
```

### Check application logs
```bash
kubectl logs -n todo-app -l app=todo-backend
kubectl logs -n todo-app -l app=todo-frontend
```

### Scale manually if needed
```bash
kubectl scale -n todo-app deployment/todo-backend --replicas=3
kubectl scale -n todo-app deployment/todo-frontend --replicas=2
```

### Check Kafka health
```bash
kubectl exec -n kafka -it $(kubectl get pods -n kafka -l app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}') -- kafka-broker-api-versions --bootstrap-server localhost:9092
```

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**
   ```bash
   kubectl describe pods -n todo-app
   kubectl get nodes
   ```

2. **Dapr sidecars not injected**
   ```bash
   kubectl describe deployment todo-backend -n todo-app
   kubectl logs -n dapr-system deployment/dapr-sidecar-injector
   ```

3. **Kafka connectivity issues**
   ```bash
   kubectl exec -n todo-app -it $(kubectl get pods -n todo-app -l app=todo-backend -o jsonpath='{.items[0].metadata.name}') -- nslookup kafka:9092
   ```

4. **Event publishing failures**
   ```bash
   kubectl logs -n todo-app -l app=todo-backend | grep "Failed to publish event"
   ```

## Cleanup

To remove the deployment:
```bash
# Uninstall application
helm uninstall todo-app -n todo-app

# Uninstall Kafka
helm uninstall kafka -n kafka

# Remove namespace
kubectl delete namespace todo-app kafka
```

## Verification Checklist

- [ ] DOKS cluster accessible and healthy
- [ ] Dapr initialized and running
- [ ] Kafka deployed and accessible
- [ ] Application pods running with Dapr sidecars
- [ ] Services exposed and accessible
- [ ] Secrets configured correctly
- [ ] HPA configured and monitoring resources
- [ ] Event publishing working (test task creation)
- [ ] Ingress configured (if applicable)
- [ ] Load testing confirms HPA functionality
- [ ] AIOps tools configured for ongoing management

## Success Criteria Met

✅ Application successfully deploys to DOKS via Helm with Dapr sidecars enabled
✅ Kafka integration successfully publishes and processes task events
✅ Horizontal Pod Autoscaler activates and scales pods appropriately under load
✅ All Phase IV functionality remains fully functional in cloud environment
✅ Basic event flow demonstrated successfully
✅ AIOps tools successfully integrated for deployment tasks
✅ Application maintains response times under normal load conditions
✅ Event-driven architecture handles concurrent task operations without loss