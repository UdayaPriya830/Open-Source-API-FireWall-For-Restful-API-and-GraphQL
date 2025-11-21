#!/bin/bash
# AWS Deployment Script for API Firewall

set -e

echo "🚀 Deploying API Firewall to AWS..."

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME="api-firewall"
ECS_CLUSTER_NAME="api-firewall-cluster"
ECS_SERVICE_NAME="api-firewall-service"
TASK_DEFINITION_NAME="api-firewall-task"

# Build and push Docker image to ECR
echo "📦 Building Docker image..."
docker build -t $ECR_REPO_NAME .

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com

echo "📤 Creating ECR repository..."
aws ecr create-repository --repository-name $ECR_REPO_NAME --region $AWS_REGION || true

echo "🏷️ Tagging and pushing image..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME"
docker tag $ECR_REPO_NAME:latest $ECR_URI:latest
docker push $ECR_URI:latest

echo "✅ Deployment complete!"