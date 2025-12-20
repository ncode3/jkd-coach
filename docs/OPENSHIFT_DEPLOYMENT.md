# SAMMO Fight IQ - OpenShift Deployment Guide

## 📋 Overview

This guide walks you through deploying SAMMO Fight IQ to an on-premises OpenShift cluster using a containerized Flask application.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         OpenShift Cluster (On-Prem)         │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │      SAMMO Fight IQ Pod            │    │
│  │                                    │    │
│  │  ┌──────────────────────────┐     │    │
│  │  │   Flask App (Gunicorn)   │     │    │
│  │  │   Port: 8080             │     │    │
│  │  └──────────────────────────┘     │    │
│  │                                    │    │
│  └────────────────────────────────────┘    │
│               │                             │
│               ├─ Service (ClusterIP)        │
│               │                             │
│               └─ Route (HTTP/HTTPS)         │
│                                             │
└──────────────┬──────────────────────────────┘
               │
               ▼
   ┌─────────────────────────┐
   │  Google Cloud Firestore │
   │  (External Database)    │
   └─────────────────────────┘
```

## 📦 Prerequisites

1. **OpenShift CLI (oc)** installed and configured
2. **Docker** or **Podman** for building images
3. **OpenShift cluster access** with appropriate permissions
4. **Google Cloud Firestore** project and credentials
5. **Image registry** access (OpenShift internal registry or external like Quay.io)

## 🔧 Step 1: Prepare Google Cloud Credentials

### 1.1 Create Service Account Key

```bash
# In Google Cloud Console:
# 1. Go to IAM & Admin > Service Accounts
# 2. Create or select a service account
# 3. Create key (JSON format)
# 4. Download the key file
```

### 1.2 Create Kubernetes Secret

```bash
# Create secret from your service account JSON file
oc create secret generic firestore-credentials \
  --from-file=credentials.json=/path/to/your/service-account-key.json \
  -n sammo-fight-iq
```

## 🐳 Step 2: Build and Push Container Image

### Option A: Using OpenShift Internal Registry

```bash
# 1. Login to OpenShift
oc login https://your-openshift-cluster.com

# 2. Create project
oc new-project sammo-fight-iq

# 3. Get internal registry route
oc get route -n openshift-image-registry

# 4. Login to internal registry
docker login -u $(oc whoami) -p $(oc whoami -t) \
  default-route-openshift-image-registry.apps.your-cluster.com

# 5. Build image
docker build -t sammo-fight-iq:latest .

# 6. Tag for internal registry
docker tag sammo-fight-iq:latest \
  default-route-openshift-image-registry.apps.your-cluster.com/sammo-fight-iq/sammo-fight-iq:latest

# 7. Push to registry
docker push default-route-openshift-image-registry.apps.your-cluster.com/sammo-fight-iq/sammo-fight-iq:latest
```

### Option B: Using External Registry (Quay.io)

```bash
# 1. Build image
docker build -t sammo-fight-iq:latest .

# 2. Tag for Quay.io
docker tag sammo-fight-iq:latest quay.io/your-username/sammo-fight-iq:latest

# 3. Push to Quay.io
docker push quay.io/your-username/sammo-fight-iq:latest
```

### Option C: Using OpenShift BuildConfig (S2I)

```bash
# Create a BuildConfig from Dockerfile
oc new-build --name=sammo-fight-iq \
  --dockerfile="$(cat Dockerfile)" \
  --to=sammo-fight-iq:latest

# Start the build
oc start-build sammo-fight-iq --from-dir=. --follow
```

## 🚀 Step 3: Deploy to OpenShift

### 3.1 Create Deployment YAML

Save as `openshift/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sammo-fight-iq
  labels:
    app: sammo-fight-iq
    app.kubernetes.io/name: sammo-fight-iq
    app.kubernetes.io/component: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sammo-fight-iq
  template:
    metadata:
      labels:
        app: sammo-fight-iq
    spec:
      containers:
      - name: sammo-fight-iq
        image: image-registry.openshift-image-registry.svc:5000/sammo-fight-iq/sammo-fight-iq:latest
        ports:
        - containerPort: 8080
          protocol: TCP
        env:
        - name: PORT
          value: "8080"
        - name: FLASK_ENV
          value: "production"
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: "/secrets/credentials.json"
        volumeMounts:
        - name: firestore-credentials
          mountPath: /secrets
          readOnly: true
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: firestore-credentials
        secret:
          secretName: firestore-credentials
```

### 3.2 Create Service YAML

Save as `openshift/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sammo-fight-iq
  labels:
    app: sammo-fight-iq
spec:
  selector:
    app: sammo-fight-iq
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  type: ClusterIP
```

### 3.3 Create Route YAML

Save as `openshift/route.yaml`:

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: sammo-fight-iq
  labels:
    app: sammo-fight-iq
spec:
  to:
    kind: Service
    name: sammo-fight-iq
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

### 3.4 Apply Configurations

```bash
# Create the openshift directory
mkdir -p openshift

# Apply all configurations
oc apply -f openshift/deployment.yaml
oc apply -f openshift/service.yaml
oc apply -f openshift/route.yaml
```

## 🔍 Step 4: Verify Deployment

```bash
# Check pod status
oc get pods -n sammo-fight-iq

# Check pod logs
oc logs -f deployment/sammo-fight-iq

# Get route URL
oc get route sammo-fight-iq -o jsonpath='{.spec.host}'

# Test health endpoint
curl https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')/health
```

## 🧪 Step 5: Test the API

### Test Health Endpoint

```bash
export API_URL=$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')

curl https://$API_URL/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-09T10:00:00",
  "firestore": "connected"
}
```

### Test Log Round Endpoint

```bash
curl -X POST https://$API_URL/api/log_round \
  -H "Content-Type: application/json" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great sparring session"
  }'
```

### Test Dashboard Stats

```bash
curl https://$API_URL/api/dashboard_stats
```

### Test Rounds History

```bash
curl https://$API_URL/api/rounds_history?limit=10
```

## 📊 Monitoring and Scaling

### View Logs

```bash
# Real-time logs
oc logs -f deployment/sammo-fight-iq

# Logs from specific pod
oc logs -f <pod-name>

# Logs from all replicas
oc logs -l app=sammo-fight-iq --all-containers=true
```

### Scale Deployment

```bash
# Scale up to 3 replicas
oc scale deployment/sammo-fight-iq --replicas=3

# Auto-scale based on CPU
oc autoscale deployment/sammo-fight-iq \
  --min=2 --max=10 --cpu-percent=80
```

### Resource Monitoring

```bash
# Check resource usage
oc top pods -l app=sammo-fight-iq

# Describe deployment
oc describe deployment sammo-fight-iq

# Check events
oc get events --sort-by='.lastTimestamp'
```

## 🔐 Security Best Practices

### 1. Use Secrets for Credentials

```bash
# Never hardcode credentials in Dockerfile or code
# Always use Kubernetes secrets

# Update secret if needed
oc create secret generic firestore-credentials \
  --from-file=credentials.json=/path/to/new-key.json \
  --dry-run=client -o yaml | oc apply -f -

# Restart deployment to pick up new secret
oc rollout restart deployment/sammo-fight-iq
```

### 2. Network Policies

```yaml
# openshift/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: sammo-fight-iq
spec:
  podSelector:
    matchLabels:
      app: sammo-fight-iq
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: openshift-ingress
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # For Firestore HTTPS
```

### 3. Service Account

```yaml
# openshift/service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sammo-fight-iq
```

Update deployment to use service account:
```yaml
spec:
  template:
    spec:
      serviceAccountName: sammo-fight-iq
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/openshift-deploy.yml
name: Deploy to OpenShift

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Login to OpenShift
      uses: redhat-actions/oc-login@v1
      with:
        openshift_server_url: ${{ secrets.OPENSHIFT_SERVER }}
        openshift_token: ${{ secrets.OPENSHIFT_TOKEN }}

    - name: Build and Push
      run: |
        oc start-build sammo-fight-iq --from-dir=. --follow

    - name: Rollout
      run: |
        oc rollout status deployment/sammo-fight-iq
```

## 🐛 Troubleshooting

### Pod Not Starting

```bash
# Check pod status
oc get pods

# Describe pod for events
oc describe pod <pod-name>

# Check logs
oc logs <pod-name>

# Common issues:
# 1. Image pull errors - check image name and registry access
# 2. Secret mounting - verify firestore-credentials secret exists
# 3. Resource limits - check if cluster has enough resources
```

### Firestore Connection Issues

```bash
# Verify secret exists
oc get secret firestore-credentials

# Check secret content (be careful with sensitive data)
oc get secret firestore-credentials -o yaml

# Verify environment variable in pod
oc exec <pod-name> -- env | grep GOOGLE

# Test Firestore connection from pod
oc exec <pod-name> -- python -c "from google.cloud import firestore; client = firestore.Client(); print('Connected')"
```

### Application Errors

```bash
# Check application logs
oc logs -f deployment/sammo-fight-iq

# Access pod shell
oc rsh <pod-name>

# Check health endpoint from inside pod
oc exec <pod-name> -- curl http://localhost:8080/health
```

## 📈 Performance Tuning

### Gunicorn Workers

Adjust workers in Dockerfile CMD:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "8", ...]
```

Or use environment variable:
```yaml
env:
- name: GUNICORN_WORKERS
  value: "8"
```

### Resource Limits

Adjust based on load testing:
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

## 🔄 Updates and Rollbacks

### Update Application

```bash
# Rebuild image
oc start-build sammo-fight-iq --from-dir=. --follow

# Or update image tag
oc set image deployment/sammo-fight-iq \
  sammo-fight-iq=sammo-fight-iq:v2.0

# Check rollout status
oc rollout status deployment/sammo-fight-iq
```

### Rollback

```bash
# Check rollout history
oc rollout history deployment/sammo-fight-iq

# Rollback to previous version
oc rollout undo deployment/sammo-fight-iq

# Rollback to specific revision
oc rollout undo deployment/sammo-fight-iq --to-revision=2
```

## 📝 Quick Reference

### Essential Commands

```bash
# Get all resources
oc get all -l app=sammo-fight-iq

# Delete everything
oc delete all -l app=sammo-fight-iq

# Get route URL
echo "https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')"

# Port forward for local testing
oc port-forward deployment/sammo-fight-iq 8080:8080
```

### Health Checks

```bash
# Liveness probe
curl http://localhost:8080/health

# Readiness probe
curl http://localhost:8080/health

# Full functionality test
curl -X POST http://localhost:8080/api/log_round \
  -H "Content-Type: application/json" \
  -d '{"pressure_score": 8.0, "ring_control_score": 7.5, "defense_score": 6.0, "clean_shots_taken": 2}'
```

## 🎯 Production Checklist

- [ ] Firestore credentials secret created
- [ ] Container image built and pushed
- [ ] Deployment, Service, and Route applied
- [ ] Health checks passing
- [ ] Resource limits configured
- [ ] Horizontal Pod Autoscaler configured
- [ ] Network policies applied
- [ ] Monitoring and alerting set up
- [ ] Backup strategy for Firestore
- [ ] SSL/TLS certificate configured (if using custom domain)
- [ ] Load testing completed
- [ ] Disaster recovery plan documented

## 📞 Support

- **OpenShift Documentation**: https://docs.openshift.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Firestore Documentation**: https://cloud.google.com/firestore/docs
- **Project Issues**: https://github.com/ncode3/sammo-fight-iq/issues

---

**Container Image**: `sammo-fight-iq:latest`
**Base Image**: `python:3.9-slim`
**Port**: `8080`
**Protocol**: `HTTP/HTTPS`
