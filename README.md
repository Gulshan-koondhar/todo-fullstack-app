# Phase V - Cloud-Native Event-Driven Architecture

This repository contains the AI Todo Chatbot application with production-ready cloud-native deployment capabilities using DigitalOcean Kubernetes (DOKS), Dapr, Apache Kafka, and event-driven architecture.

## Features

- **Cloud-Native Deployment**: Optimized for DigitalOcean Kubernetes (DOKS) with production-ready configurations
- **Event-Driven Architecture**: Apache Kafka integration with Dapr for asynchronous task event processing
- **Horizontal Pod Autoscaling**: Automatic scaling based on CPU and memory metrics
- **Containerized Application**: Next.js frontend and FastAPI backend in Docker containers
- **Kubernetes Native**: Deployed with comprehensive Helm charts including Dapr and Kafka components
- **User Authentication**: Secure signup/signin with JWT tokens
- **Task Management**: Create, view, update, delete, and complete tasks
- **AI Chatbot**: Natural language interaction with AI assistant
- **Data Isolation**: Complete user data isolation - users can only see their own tasks
- **Stateless Architecture**: All persistent data stored in external Neon PostgreSQL
- **Secure Secrets Management**: Sensitive configuration stored in Kubernetes Secrets
- **AIOps Integration**: Designed for kubectl-ai and kagent for intelligent operations

## Tech Stack

### Application
- Next.js 16+ with App Router (Frontend)
- FastAPI with Python 3.11+ (Backend)
- SQLModel for ORM
- PostgreSQL (Neon) for database
- Better Auth for authentication
- OpenAI Agents SDK for AI interactions
- MCP (Model Context Protocol) for tool integration

### Deployment
- Docker for containerization
- Kubernetes for orchestration
- Minikube for local cluster
- Helm for package management
- kubectl for cluster management

## Cloud Deployment Instructions

### Prerequisites

- Docker Desktop or Docker Engine
- kubectl
- Helm 3.x
- Dapr CLI
- DigitalOcean CLI (doctl)
- Git
- Access to DigitalOcean Kubernetes (DOKS)

### 1. Configure DigitalOcean Kubernetes (DOKS)
```bash
# Authenticate with DigitalOcean
doctl auth init

# Connect to your DOKS cluster
doctl kubernetes cluster kubeconfig save <your-cluster-name>
```

### 2. Push Docker Images to Registry
```bash
# Tag images for your container registry (e.g., DigitalOcean Container Registry)
docker tag todo-frontend:latest registry.digitalocean.com/your-registry/todo-frontend:latest
docker tag todo-backend:latest registry.digitalocean.com/your-registry/todo-backend:latest

# Push images to registry
docker push registry.digitalocean.com/your-registry/todo-frontend:latest
docker push registry.digitalocean.com/your-registry/todo-backend:latest

# Update values.yaml with your image repository paths
# Or create a secrets-values.yaml file with your sensitive configuration:
```

### 3. Initialize Dapr on DOKS
```bash
# Initialize Dapr in the cluster
dapr init -k --runtime-version=1.11.0

# Verify Dapr installation
kubectl get pods -n dapr-system
```

### 4. Deploy Kafka for Event Streaming
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

### 5. Prepare Secret Values
Create a `secrets-values.yaml` file with your sensitive configuration:
```yaml
# secrets-values.yaml
secrets:
  neonDbUrl: "your-neon-db-url-here"
  openAiApiKey: "your-openai-api-key-here"
  jwtSecret: "your-jwt-secret-here"
  betterAuthSecret: "your-better-auth-secret-here"
```

### 6. Deploy with Helm
```bash
# Navigate to helm directory
cd helm/todo-app

# Install the application
helm install todo-app . -f secrets-values.yaml

# Or upgrade if already installed
helm upgrade todo-app . -f secrets-values.yaml
```

### 7. Access the Application
```bash
# Get the load balancer IP
kubectl get svc todo-frontend-service -n todo-app

# Or configure ingress for domain access
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/do/deploy.yaml
```

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods -A
# All pods should be in Running state (including dapr-system, kafka, and todo-app namespaces)
```

### 2. Check Services
```bash
kubectl get services -n todo-app
# Verify frontend and backend services are available
```

### 3. Test Event-Driven Functionality
```bash
# Check Dapr sidecars are injected
kubectl get pods -n todo-app -o yaml | grep dapr

# Test application functionality
- Access the frontend URL from load balancer
- Test user registration/login
- Create and manage tasks
- Use the AI chatbot functionality
- Verify conversation history persists
- Check Kafka topics for published events:
kubectl exec -it -n kafka $(kubectl get pods -n kafka -l app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}') -- kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 4. Test Horizontal Pod Autoscaling
```bash
# Check HPA status
kubectl get hpa -n todo-app
kubectl describe hpa -n todo-app

# Generate load to test scaling
hey -n 1000 -c 10 http://your-app-domain.com/api/v1/tasks?user_id=test-user
```

### 5. Test Resilience
```bash
# Delete a backend pod to test statelessness
kubectl delete pod -n todo-app $(kubectl get pods -n todo-app -l app=todo-backend -o jsonpath='{.items[0].metadata.name}')

# Verify application continues to function
# Check that conversation history persists in Neon PostgreSQL
# Verify Dapr sidecar automatically reconnects
```

## AIOps Integration

### 1. Phase V: Cloud-Native Event-Driven Architecture

Phase V successfully implements a production-ready, cloud-native event-driven architecture for the AI Todo Chatbot application. Key features include:

- **DigitalOcean Kubernetes (DOKS) Deployment**: Full Helm chart support for production deployment
- **Event-Driven Architecture**: Apache Kafka integration with Dapr for task event processing
- **Horizontal Pod Autoscaling**: Automatic scaling based on CPU and memory metrics
- **AIOps Integration**: Support for kubectl-ai and kagent for intelligent operations
- **Production-Ready**: All components optimized for cloud deployment with resilience

### Using kubectl-ai
```bash
# Generate HPA configuration using AI
kubectl ai create hpa todo-backend-hpa --namespace todo-app --from=deployment/todo-backend --cpu-percent=70 --min=2 --max=5

# Troubleshoot deployment issues with AI assistance
kubectl ai explain "pods in CrashLoopBackOff" --namespace todo-app

# Generate Dapr component configuration
kubectl ai create component kafka-pubsub --apiVersion=dapr.io/v1alpha1
```

## Uninstallation

```bash
# Uninstall the application
helm uninstall todo-app -n todo-app

# Uninstall Kafka
helm uninstall kafka -n kafka

# Remove namespaces
kubectl delete namespace todo-app kafka

# Optionally remove Dapr from cluster
dapr uninstall -k
```

## Troubleshooting

### Common Issues

#### Pods in Pending State
- Check if Minikube has sufficient resources
- Verify Docker images are loaded: `minikube image ls`

#### Service Not Accessible
- Ensure Minikube tunnel is running: `minikube tunnel`
- Check service configuration: `kubectl describe service todo-frontend-service`

#### Database Connection Errors
- Verify NEON_DB_URL is correctly configured in secrets
- Check if database allows connections from Kubernetes cluster

#### Scaling Issues
- Ensure resource limits are appropriate for Minikube
- Check if Minikube has sufficient CPU/memory for multiple replicas

## Project Structure

```
├── docker/                   # Dockerfiles for containerization
│   ├── frontend.Dockerfile  # Multi-stage build for Next.js frontend
│   └── backend.Dockerfile   # Multi-stage build for FastAPI backend + MCP server
├── helm/                     # Helm charts for deployment
│   ├── todo-app/            # Main application chart with Dapr annotations
│   │   ├── Chart.yaml       # Chart metadata
│   │   ├── values.yaml      # Default configuration values
│   │   ├── templates/       # Kubernetes resource templates with Dapr annotations
│   │   └── README.md        # Chart documentation
│   └── dapr-components/     # Dapr components Helm subchart
│       ├── Chart.yaml       # Chart metadata
│       ├── values.yaml      # Configuration values
│       └── templates/       # Dapr component templates
├── dapr/                     # Dapr component configurations
│   ├── components/          # Individual Dapr component definitions
│   ├── templates/           # Reusable Dapr component templates
│   └── config.yaml          # Dapr configuration
├── kafka/                    # Kafka configuration files optimized for DOKS
├── k8s/raw/                 # Raw Kubernetes manifests (optional reference)
├── frontend/                # Next.js frontend source code
├── backend/                 # FastAPI backend source code with Dapr event publisher
│   └── src/mcp_tools/       # MCP tools including event_publisher.py
├── docs/                     # Documentation
│   ├── event-driven-architecture.md  # Event-driven architecture documentation
│   └── deployment-quickstart.md      # Deployment quickstart guide
├── specs/                    # Feature specifications
│   └── 004-cloud-native-event-arch/ # Phase V specifications
├── history/                  # Development history records
│   └── prompts/             # Prompt History Records
├── PHASE_V_SUMMARY.md       # Phase V implementation summary
├── DEPLOYMENT_GUIDE.md      # Cloud deployment guide
└── README.md                # This file
```

## Event-Driven Architecture

This application implements an event-driven architecture using Dapr and Apache Kafka for cloud-native deployment. Key features include:

### Event Types
- **CREATE_TASK**: Published when a new task is created
- **UPDATE_TASK**: Published when an existing task is updated
- **COMPLETE_TASK**: Published when a task is marked as completed
- **DELETE_TASK**: Published when a task is deleted

### Architecture Components
- **Dapr**: Distributed Application Runtime for service mesh capabilities
- **Apache Kafka**: Message broker for event streaming
- **Helm Charts**: For deployment of Dapr components and main application
- **Horizontal Pod Autoscaling**: For scaling based on load

### Event Flow
1. User performs action in frontend
2. Backend API processes request and updates database
3. Backend publishes event to Kafka via Dapr pub/sub
4. Event consumers can process events asynchronously (future enhancement)

## API Documentation

See `specs/001-multi-user-todo/contracts/api-spec.md` for detailed API documentation.

## License

MIT
