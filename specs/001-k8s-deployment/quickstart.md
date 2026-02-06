# Quickstart Guide: Phase IV – Local Kubernetes Deployment

**Date**: 2026-01-20
**Feature**: Phase IV – Local Kubernetes Deployment
**Branch**: 001-k8s-deployment

## Overview

This guide provides step-by-step instructions to deploy the AI Todo Chatbot application to a local Minikube cluster using Helm charts. The application consists of a Next.js frontend and a FastAPI backend with MCP server, all containerized and deployed following cloud-native best practices.

## Prerequisites

### System Requirements
- Docker Desktop or Docker Engine (v20+)
- Minikube (latest stable)
- kubectl (matching Minikube version)
- Helm 3.x
- Git
- Node.js 18+ (for local development)

### Installation Commands
```bash
# Install Docker (follow platform-specific instructions)
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/windows/amd64/kubectl.exe"  # Windows
# Install Helm
choco install kubernetes-helm  # Windows
# Install Minikube
choco install minikube  # Windows
```

### Required Environment Variables
Before deployment, ensure you have the following values ready:
- `NEON_DB_URL`: Your Neon PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `JWT_SECRET`: Secret for JWT token signing
- `BETTER_AUTH_SECRET`: Secret for Better Auth

## Deployment Steps

### 1. Start Minikube Cluster
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

### 2. Using kagent (if available)
```bash
# Get AI-assisted troubleshooting for pod issues
kagent diagnose pods
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

### Debug Commands
```bash
# Check pod logs
kubectl logs -l app=todo-backend

# Get detailed pod information
kubectl describe pod <pod-name>

# Check service endpoints
kubectl get endpoints <service-name>

# Port forward for direct access (temporary)
kubectl port-forward service/todo-frontend-service 8080:80
```

## Development Workflow

### Making Changes
1. Update application code in respective directories
2. Rebuild Docker images with new tags
3. Update image tags in Helm values
4. Upgrade Helm release: `helm upgrade todo-app . -f values.yaml`

### Local Development
- Use `skaffold` or similar tools for iterative development
- Consider using `telepresence` for intercepting traffic to local containers
- Implement hot-reload where possible for faster iteration

## Security Considerations

- Never commit secrets to version control
- Use Kubernetes Secrets for sensitive data
- Implement proper RBAC rules for production
- Regularly scan images for vulnerabilities
- Monitor network policies for inter-service communication