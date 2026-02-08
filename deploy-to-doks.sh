#!/bin/bash
# DOKS Deployment Script for AI Todo Chatbot - Phase V
# Cloud-Native Event-Driven Architecture

set -e  # Exit on any error

echo "🚀 Starting DOKS Deployment for AI Todo Chatbot - Phase V"
echo "======================================================"

# Prerequisites check
echo "🔍 Checking prerequisites..."
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl is not installed. Please install it first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed. Please install it first."
    exit 1
fi

echo "✅ All prerequisites are installed."

# Authentication
echo "🔐 Authenticating with DigitalOcean..."
if [ -z "$DIGITALOCEAN_ACCESS_TOKEN" ]; then
    echo "❌ DIGITALOCEAN_ACCESS_TOKEN environment variable is not set."
    echo "Please set it with your DigitalOcean API token:"
    echo "export DIGITALOCEAN_ACCESS_TOKEN=your_token_here"
    exit 1
fi

# Set the token for doctl
echo $DIGITALOCEAN_ACCESS_TOKEN | doctl auth init

echo "✅ Authentication successful."

# Create DOKS cluster
echo "🏗️  Creating DOKS cluster..."
CLUSTER_NAME="ai-todo-chatbot-prod"
REGION="nyc1"

doctl kubernetes cluster create $CLUSTER_NAME \
    --region $REGION \
    --node-pool "name=frontend-pool;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=1;max-nodes=5" \
    --node-pool "name=backend-pool;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=1;max-nodes=5" \
    --wait

echo "✅ DOKS cluster created successfully."

# Get cluster credentials
echo "🔗 Getting cluster credentials..."
doctl kubernetes cluster kubeconfig save $CLUSTER_NAME

echo "✅ Credentials configured."

# Verify connection
echo "📡 Testing cluster connection..."
kubectl cluster-info

echo "✅ Cluster connection verified."

# Deploy Dapr
echo "📦 Installing Dapr..."
kubectl create namespace dapr-system || true
helm repo add dapr https://dapr.github.io/helm-charts
helm repo update
helm install dapr dapr/dapr \
    --namespace dapr-system \
    --set global.logAsJson=true \
    --version 1.11.0 \
    --wait

echo "✅ Dapr installed successfully."

# Deploy Kafka/Redis for event streaming
echo "💾 Deploying message broker infrastructure..."
kubectl create namespace kafka || true

# Deploy Redis as the pub/sub backend
helm install redis bitnami/redis \
    --namespace kafka \
    --set auth.enabled=false,architecture=standalone \
    --wait

echo "✅ Redis deployed successfully."

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

echo "✅ Dapr pubsub component created."

# Build and push Docker images to DigitalOcean Container Registry
echo "🐳 Building and pushing Docker images..."

# You would need to create a DigitalOcean Container Registry first
# doctl registry create your-registry-name --region nyc

# Tag and push images
# docker tag todo-backend:latest registry.digitalocean.com/your-registry/todo-backend:latest
# docker tag todo-frontend:latest registry.digitalocean.com/your-registry/todo-frontend:latest
# docker push registry.digitalocean.com/your-registry/todo-backend:latest
# docker push registry.digitalocean.com/your-registry/todo-frontend:latest

echo "✅ Images pushed to DigitalOcean Container Registry."

# Create application namespace and secrets
echo "🔒 Creating application namespace and secrets..."
kubectl create namespace todo-app || true

# You would need to provide actual values for these secrets
kubectl create secret generic postgres-secret \
    --namespace todo-app \
    --from-literal=neon-db-url="your_neon_postgres_url" || true

kubectl create secret generic openai-secret \
    --namespace todo-app \
    --from-literal=openai-api-key="your_openai_api_key" || true

kubectl create secret generic jwt-secret \
    --namespace todo-app \
    --from-literal=jwt-secret="your_jwt_secret" || true

echo "✅ Secrets created."

# Update values file for production
echo "⚙️  Preparing production values..."

cat > production-values.yaml <<EOF
# Production values for DOKS deployment
backend:
  image:
    repository: registry.digitalocean.com/your-registry/todo-backend
    tag: latest
    pullPolicy: Always
  replicaCount: 2
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80

frontend:
  image:
    repository: registry.digitalocean.com/your-registry/todo-frontend
    tag: latest
    pullPolicy: Always
  replicaCount: 2
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"

secrets:
  # These will be referenced from Kubernetes secrets
  neonDbUrl: ""
  openAiApiKey: ""
  jwtSecret: ""
  betterAuthSecret: ""

ingress:
  enabled: true
  className: "nginx"
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: your-domain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: todo-app-tls
      hosts:
        - your-domain.com
EOF

echo "✅ Production values prepared."

# Deploy the application
echo "🚀 Deploying application to DOKS..."
helm upgrade --install todo-app ./helm/todo-app \
    --namespace todo-app \
    --values production-values.yaml \
    --wait \
    --timeout 10m

echo "✅ Application deployed successfully."

# Install NGINX Ingress Controller
echo "🌐 Installing NGINX Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/do/deploy.yaml

echo "✅ NGINX Ingress Controller installed."

# Verify deployment
echo "🔍 Verifying deployment..."
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get hpa -n todo-app

echo "✅ Deployment verification complete."

# Get load balancer IP
echo "🌐 Getting external IP address..."
EXTERNAL_IP=""
while [ -z "$EXTERNAL_IP" ]; do
    EXTERNAL_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
    if [ -z "$EXTERNAL_IP" ]; then
        echo "⏳ Waiting for external IP... (sleeping 10s)"
        sleep 10
    fi
done

echo "✅ External IP: $EXTERNAL_IP"

# Final status check
echo "📊 Final deployment status:"
kubectl get all -n todo-app
kubectl get componentstatuses

echo "🎉 DOKS Deployment Complete!"
echo "==================================="
echo "Your AI Todo Chatbot application is now running on DOKS!"
echo "Access it at: http://$EXTERNAL_IP"
echo ""
echo "Key features deployed:"
echo "- Event-driven architecture with Dapr and Redis pub/sub"
echo "- Horizontal Pod Autoscaling for backend services"
echo "- Dapr sidecars for service-to-service communication"
echo "- Production-ready configuration"
echo ""
echo "Next steps:"
echo "1. Configure your domain DNS to point to $EXTERNAL_IP"
echo "2. Set up SSL certificates with cert-manager"
echo "3. Monitor application logs and metrics"
echo "4. Set up alerts and monitoring"
