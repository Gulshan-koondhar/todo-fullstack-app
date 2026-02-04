#!/bin/bash

# Simple validation script for the Helm chart structure

CHART_DIR="helm/todo-app"

echo "Validating Helm chart structure at $CHART_DIR..."

# Check required files
if [ ! -f "$CHART_DIR/Chart.yaml" ]; then
    echo "❌ Chart.yaml not found"
    exit 1
else
    echo "✅ Chart.yaml found"
fi

if [ ! -f "$CHART_DIR/values.yaml" ]; then
    echo "❌ values.yaml not found"
    exit 1
else
    echo "✅ values.yaml found"
fi

if [ ! -d "$CHART_DIR/templates" ]; then
    echo "❌ templates directory not found"
    exit 1
else
    echo "✅ templates directory found"

    # Check template files
    templates=(frontend-deployment.yaml backend-deployment.yaml frontend-service.yaml backend-service.yaml postgres-secret.yaml openai-secret.yaml jwt-secret.yaml ingress.yaml hpa.yaml _helpers.tpl)

    for template in "${templates[@]}"; do
        if [ -f "$CHART_DIR/templates/$template" ]; then
            echo "✅ $template found"
        else
            echo "❌ $template not found"
        fi
    done
fi

echo "Helm chart validation completed!"