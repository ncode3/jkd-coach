#!/bin/bash
# SAMMO Fight IQ - OpenShift Deployment Script
# This script automates the deployment process to OpenShift

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="${OPENSHIFT_PROJECT:-sammo-fight-iq}"
IMAGE_NAME="sammo-fight-iq"
CREDENTIALS_FILE="${FIRESTORE_CREDENTIALS:-./credentials.json}"

echo -e "${GREEN}🥊 SAMMO Fight IQ - OpenShift Deployment${NC}"
echo "============================================"
echo ""

# Check if oc is installed
if ! command -v oc &> /dev/null; then
    echo -e "${RED}❌ OpenShift CLI (oc) not found. Please install it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ OpenShift CLI found${NC}"

# Check if logged in
if ! oc whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to OpenShift.${NC}"
    echo "Please login first with: oc login <your-cluster-url>"
    exit 1
fi

echo -e "${GREEN}✅ Logged in as: $(oc whoami)${NC}"
echo ""

# Create or switch to project
echo "📦 Setting up project: $PROJECT_NAME"
if oc get project $PROJECT_NAME &> /dev/null; then
    echo -e "${YELLOW}Project already exists, switching to it...${NC}"
    oc project $PROJECT_NAME
else
    echo "Creating new project..."
    oc new-project $PROJECT_NAME --display-name="SAMMO Fight IQ" --description="AI-Powered Boxing Coach"
fi
echo ""

# Check for Firestore credentials
echo "🔐 Checking Firestore credentials..."
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo -e "${RED}❌ Credentials file not found: $CREDENTIALS_FILE${NC}"
    echo "Please provide the path to your Google Cloud service account key:"
    echo "  export FIRESTORE_CREDENTIALS=/path/to/credentials.json"
    exit 1
fi

# Create or update secret
echo "Creating/updating Firestore credentials secret..."
oc create secret generic firestore-credentials \
    --from-file=credentials.json=$CREDENTIALS_FILE \
    --dry-run=client -o yaml | oc apply -f -

echo -e "${GREEN}✅ Firestore credentials configured${NC}"
echo ""

# Build image
echo "🐳 Building container image..."
if oc get bc $IMAGE_NAME &> /dev/null; then
    echo "BuildConfig exists, starting new build..."
    oc start-build $IMAGE_NAME --from-dir=.. --follow
else
    echo "Creating BuildConfig..."
    oc new-build --name=$IMAGE_NAME \
        --binary=true \
        --strategy=docker \
        --to=$IMAGE_NAME:latest

    echo "Starting first build..."
    oc start-build $IMAGE_NAME --from-dir=.. --follow
fi

echo -e "${GREEN}✅ Image built successfully${NC}"
echo ""

# Deploy application
echo "🚀 Deploying application..."
oc apply -f all-in-one.yaml

echo ""
echo "⏳ Waiting for deployment to be ready..."
oc rollout status deployment/$IMAGE_NAME --timeout=5m

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo ""

# Get route URL
echo "🌐 Application URL:"
ROUTE_URL=$(oc get route $IMAGE_NAME -o jsonpath='{.spec.host}' 2>/dev/null || echo "Route not found")
if [ "$ROUTE_URL" != "Route not found" ]; then
    echo -e "${GREEN}https://$ROUTE_URL${NC}"
    echo ""

    # Test health endpoint
    echo "🧪 Testing health endpoint..."
    sleep 5  # Give it a moment to be fully ready

    if curl -sf "https://$ROUTE_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed!${NC}"
        curl -s "https://$ROUTE_URL/health" | jq . || curl -s "https://$ROUTE_URL/health"
    else
        echo -e "${YELLOW}⚠️  Health check failed. The app might still be starting up.${NC}"
        echo "Try: curl https://$ROUTE_URL/health"
    fi
else
    echo -e "${YELLOW}⚠️  Route not found. Creating route manually may be needed.${NC}"
fi

echo ""
echo "============================================"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo "Useful commands:"
echo "  oc get pods -n $PROJECT_NAME"
echo "  oc logs -f deployment/$IMAGE_NAME"
echo "  oc get route $IMAGE_NAME"
echo "  oc delete all -l app=$IMAGE_NAME"
echo ""
echo "API Endpoints:"
echo "  GET  /health"
echo "  POST /api/log_round"
echo "  GET  /api/dashboard_stats"
echo "  GET  /api/rounds_history"
echo ""
