# Phase IV - Local Kubernetes Deployment

This repository contains the AI Todo Chatbot application deployed to a local Kubernetes cluster using Minikube and Helm charts.

## Features

- **Containerized Application**: Next.js frontend and FastAPI backend in Docker containers
- **Kubernetes Native**: Deployed with Helm charts to Minikube cluster
- **User Authentication**: Secure signup/signin with JWT tokens
- **Task Management**: Create, view, update, delete, and complete tasks
- **AI Chatbot**: Natural language interaction with AI assistant
- **Data Isolation**: Complete user data isolation - users can only see their own tasks
- **Horizontal Scaling**: Backend services can scale to multiple replicas
- **Stateless Architecture**: All persistent data stored in external Neon PostgreSQL
- **Secure Secrets Management**: Sensitive configuration stored in Kubernetes Secrets

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

## Deployment Instructions

### Prerequisites

- Docker Desktop or Docker Engine
- Minikube
- kubectl
- Helm 3.x
- Git

### 1. Start Minikube
```bash
minikube start
minikube addons enable ingress  # Enable ingress for external access
```

### 2. Build Docker Images
```bash
# Navigate to project root
cd C:\Users\hp\Desktop\hackathon_phase_IV

# Build frontend image
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .

# Build backend image
docker build -f docker/backend.Dockerfile -t todo-backend:latest .

# Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 3. Prepare Secret Values
Create a `secrets-values.yaml` file with your sensitive configuration:
```yaml
# secrets-values.yaml
secrets:
  neonDbUrl: "your-neon-db-url-here"
  openAiApiKey: "your-openai-api-key-here"
  jwtSecret: "your-jwt-secret-here"
  betterAuthSecret: "your-better-auth-secret-here"
```

### 4. Deploy with Helm
```bash
# Navigate to helm directory
cd helm/todo-app

# Install the application
helm install todo-app . -f secrets-values.yaml

# Or upgrade if already installed
helm upgrade todo-app . -f secrets-values.yaml
```

### 5. Access the Application
```bash
# Get the service URL
minikube service todo-frontend-service --url

# Or use tunnel for direct access (in separate terminal)
minikube tunnel
```

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods
# All pods should be in Running state
```

### 2. Check Services
```bash
kubectl get services
# Verify frontend and backend services are available
```

### 3. Test Application Functionality
- Access the frontend URL from `minikube service` command
- Test user registration/login
- Create and manage tasks
- Use the AI chatbot functionality
- Verify conversation history persists

### 4. Test Scaling
```bash
# Scale backend to 3 replicas
kubectl scale deployment todo-backend --replicas=3

# Verify all replicas are running
kubectl get pods
```

### 5. Test Resilience
```bash
# Delete a backend pod to test statelessness
kubectl delete pod $(kubectl get pods -l app=todo-backend -o jsonpath='{.items[0].metadata.name}')

# Verify application continues to function
# Check that conversation history persists
```

## AIOps Integration

### 1. Using kubectl-ai
```bash
# Generate a sample deployment manifest using AI
kubectl ai create deployment todo-test --image=nginx --replicas=2

# Troubleshoot issues with AI assistance
kubectl ai explain "pods in CrashLoopBackOff"
```

## Uninstallation

```bash
# Uninstall the application
helm uninstall todo-app

# Optionally stop Minikube
minikube stop
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
│   └── todo-app/            # Main application chart
│       ├── Chart.yaml       # Chart metadata
│       ├── values.yaml      # Default configuration values
│       ├── templates/       # Kubernetes resource templates
│       └── README.md        # Chart documentation
├── k8s/raw/                 # Raw Kubernetes manifests (optional reference)
├── frontend/                # Next.js frontend source code
├── backend/                 # FastAPI backend source code
└── specs/                   # Feature specifications
    └── 001-k8s-deployment/  # Phase IV specifications
```

## API Documentation

See `specs/001-multi-user-todo/contracts/api-spec.md` for detailed API documentation.

## License

MIT
