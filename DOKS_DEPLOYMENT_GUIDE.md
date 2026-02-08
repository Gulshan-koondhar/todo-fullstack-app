# DOKS Deployment Guide for AI Todo Chatbot - Phase V

## Cloud-Native Event-Driven Architecture Deployment

This guide provides instructions for deploying the AI Todo Chatbot application to DigitalOcean Kubernetes (DOKS) with event-driven architecture.

## Prerequisites

1. DigitalOcean account with billing configured
2. DigitalOcean API token with read/write permissions
3. `doctl`, `kubectl`, and `helm` installed locally
4. Docker images built and pushed to a container registry

## Step 1: Authenticate with DigitalOcean

```bash
# Set your DigitalOcean API token as an environment variable
export DIGITALOCEAN_ACCESS_TOKEN=your_token_here

# Or use doctl to authenticate
doctl auth init
```

## Step 2: Create DOKS Cluster

```bash
# Create a Kubernetes cluster with auto-scaling node pools
doctl kubernetes cluster create ai-todo-chatbot-prod \
    --region nyc1 \
    --node-pool "name=frontend-pool;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=1;max-nodes=5" \
    --node-pool "name=backend-pool;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=1;max-nodes=5" \
    --wait
```

## Step 3: Configure kubectl

```bash
# Get the cluster credentials
doctl kubernetes cluster kubeconfig save ai-todo-chatbot-prod

# Verify the connection
kubectl cluster-info
```

## Step 4: Deploy Dapr Runtime

```bash
# Create Dapr namespace
kubectl create namespace dapr-system

# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts
helm repo update

# Install Dapr
helm install dapr dapr/dapr \
    --namespace dapr-system \
    --set global.logAsJson=true \
    --version 1.11.0 \
    --wait
```

## Step 5: Deploy Message Broker Infrastructure

```bash
# Create kafka namespace (for consistency with our naming)
kubectl create namespace kafka

# Deploy Redis for pub/sub functionality
helm install redis bitnami/redis \
    --namespace kafka \
    --set auth.enabled=false,architecture=standalone \
    --wait

# Create Dapr pubsub component
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.kafka.svc.cluster.local:6379
  - name: redisPassword
    value: ""
EOF
```

## Step 6: Prepare Application Images

```bash
# Create DigitalOcean Container Registry (if not already created)
doctl registry create your-registry-name --region nyc

# Tag and push your built images
docker tag todo-backend:latest registry.digitalocean.com/your-registry/todo-backend:latest
docker tag todo-frontend:latest registry.digitalocean.com/your-registry/todo-frontend:latest

docker push registry.digitalocean.com/your-registry/todo-backend:latest
docker push registry.digitalocean.com/your-registry/todo-frontend:latest
```

## Step 7: Create Application Secrets

```bash
# Create application namespace
kubectl create namespace todo-app

# Create secrets for the application
kubectl create secret generic postgres-secret \
    --namespace todo-app \
    --from-literal=neon-db-url="your_neon_postgres_connection_string"

kubectl create secret generic openai-secret \
    --namespace todo-app \
    --from-literal=openai-api-key="your_openai_api_key"

kubectl create secret generic jwt-secret \
    --namespace todo-app \
    --from-literal=jwt-secret="your_jwt_secret"
```

## Step 8: Deploy the Application

```bash
# Deploy using Helm charts
helm upgrade --install todo-app ./helm/todo-app \
    --namespace todo-app \
    --set backend.image.repository=registry.digitalocean.com/your-registry/todo-backend \
    --set backend.image.tag=latest \
    --set frontend.image.repository=registry.digitalocean.com/your-registry/todo-frontend \
    --set frontend.image.tag=latest \
    --wait \
    --timeout 10m
```

## Step 9: Install Ingress Controller

```bash
# Install NGINX Ingress Controller for DOKS
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/do/deploy.yaml
```

## Step 10: Verify Deployment

```bash
# Check all resources
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get hpa -n todo-app

# Check Dapr sidecars
kubectl get pods -n todo-app -o yaml | grep dapr
```

## Architecture Verification

After deployment, verify that:

1. **Dapr Sidecars**: Are injected with annotations:
   - `dapr.io/enabled: "true"`
   - `dapr.io/app-id: todo-backend/todo-frontend`
   - `dapr.io/app-port: "8000"/"3000"`

2. **HPA**: Is configured and monitoring resources

3. **Event System**: Is ready for event publishing (as implemented in code)

4. **Services**: Are accessible and properly load balanced

## Production Considerations

- Set up SSL certificates with cert-manager and Let's Encrypt
- Configure proper domain DNS records
- Set up monitoring and alerting
- Implement proper backup strategies
- Configure security policies and network restrictions

## Expected Outcomes

Upon successful deployment:

✅ Application running on DOKS with Dapr sidecars
✅ Event-driven architecture with pub/sub infrastructure
✅ Horizontal Pod Autoscaling configured
✅ Production-ready security and configuration
✅ All Phase IV functionality preserved
✅ AIOps integration readiness

## Troubleshooting

Common issues and solutions:

- **ImagePullBackOff**: Verify image names and registry access
- **CrashLoopBackOff**: Check environment variables and secrets
- **Dapr sidecars not starting**: Verify Dapr installation
- **HPA not working**: Check metrics server availability

This deployment completes Phase V - Cloud-Native Event-Driven Architecture, ready for production use on DigitalOcean Kubernetes.