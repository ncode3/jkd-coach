# SAMMO Fight IQ - OpenShift Deployment Files

This directory contains all necessary files and scripts for deploying SAMMO Fight IQ to OpenShift.

## 📁 Contents

| File | Description |
|------|-------------|
| `deployment.yaml` | Kubernetes Deployment configuration |
| `service.yaml` | Kubernetes Service configuration |
| `route.yaml` | OpenShift Route configuration |
| `all-in-one.yaml` | Complete deployment (all resources in one file) |
| `deploy.sh` | Automated deployment script |
| `test-api.sh` | API testing script |
| `README.md` | This file |

## 🚀 Quick Start

### Prerequisites

1. OpenShift CLI (`oc`) installed
2. Access to an OpenShift cluster
3. Google Cloud Firestore credentials JSON file

### One-Command Deployment

```bash
# Set your credentials path
export FIRESTORE_CREDENTIALS=/path/to/credentials.json

# Run deployment script
cd openshift
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment

```bash
# 1. Login to OpenShift
oc login https://your-cluster.com

# 2. Create project
oc new-project sammo-fight-iq

# 3. Create secret for Firestore credentials
oc create secret generic firestore-credentials \
  --from-file=credentials.json=/path/to/credentials.json

# 4. Build image
oc new-build --name=sammo-fight-iq \
  --binary=true \
  --strategy=docker

oc start-build sammo-fight-iq --from-dir=.. --follow

# 5. Deploy application
oc apply -f all-in-one.yaml

# 6. Wait for rollout
oc rollout status deployment/sammo-fight-iq

# 7. Get route URL
oc get route sammo-fight-iq -o jsonpath='{.spec.host}'
```

## 🧪 Testing

After deployment, test the API:

```bash
chmod +x test-api.sh
./test-api.sh
```

Or test manually:

```bash
# Get URL
API_URL=$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')

# Test health
curl https://$API_URL/health

# Log a round
curl -X POST https://$API_URL/api/log_round \
  -H "Content-Type: application/json" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Test round"
  }'

# Get stats
curl https://$API_URL/api/dashboard_stats

# Get history
curl https://$API_URL/api/rounds_history
```

## 📊 Monitoring

### View Logs

```bash
# Real-time logs
oc logs -f deployment/sammo-fight-iq

# Logs from all pods
oc logs -l app=sammo-fight-iq --all-containers=true
```

### Check Status

```bash
# Pod status
oc get pods

# Deployment status
oc get deployment sammo-fight-iq

# Service status
oc get service sammo-fight-iq

# Route status
oc get route sammo-fight-iq
```

### Resource Usage

```bash
# CPU and memory usage
oc top pods -l app=sammo-fight-iq

# Describe deployment
oc describe deployment sammo-fight-iq
```

## ⚙️ Configuration

### Environment Variables

Edit `deployment.yaml` to customize:

```yaml
env:
- name: PORT
  value: "8080"
- name: FLASK_ENV
  value: "production"
```

### Resource Limits

Adjust based on your needs:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Replicas

Scale horizontally:

```bash
# Manual scaling
oc scale deployment/sammo-fight-iq --replicas=5

# Check HPA status
oc get hpa sammo-fight-iq
```

## 🔄 Updates

### Update Image

```bash
# Rebuild
oc start-build sammo-fight-iq --from-dir=.. --follow

# Restart deployment
oc rollout restart deployment/sammo-fight-iq

# Check status
oc rollout status deployment/sammo-fight-iq
```

### Rollback

```bash
# View history
oc rollout history deployment/sammo-fight-iq

# Rollback
oc rollout undo deployment/sammo-fight-iq
```

## 🗑️ Cleanup

```bash
# Delete all resources
oc delete all -l app=sammo-fight-iq

# Delete secrets
oc delete secret firestore-credentials

# Delete project (careful!)
oc delete project sammo-fight-iq
```

## 🔐 Security

### Update Credentials

```bash
# Update Firestore credentials
oc create secret generic firestore-credentials \
  --from-file=credentials.json=/path/to/new-credentials.json \
  --dry-run=client -o yaml | oc apply -f -

# Restart pods to pick up new secret
oc rollout restart deployment/sammo-fight-iq
```

### Network Policies

Apply network policies for additional security (create as needed).

## 🐛 Troubleshooting

### Pod Not Starting

```bash
# Check pod status
oc get pods

# Describe pod
oc describe pod <pod-name>

# View logs
oc logs <pod-name>
```

### Image Pull Errors

```bash
# Check build config
oc get bc

# View build logs
oc logs -f bc/sammo-fight-iq
```

### Firestore Connection Issues

```bash
# Verify secret exists
oc get secret firestore-credentials

# Check secret is mounted
oc describe pod <pod-name> | grep -A 5 volumes

# Test from inside pod
oc exec <pod-name> -- ls -la /secrets/
```

## 📝 Notes

- **Port**: Application runs on port 8080
- **Health Check**: Available at `/health`
- **TLS**: Route configured for edge termination
- **Auto-scaling**: HPA configured for 2-10 replicas based on CPU/memory
- **Rolling Updates**: Zero-downtime deployments with maxUnavailable: 0

## 🔗 Related Documentation

- [Full Deployment Guide](../OPENSHIFT_DEPLOYMENT.md)
- [Application Code](../app.py)
- [Dockerfile](../Dockerfile)
- [Main README](../README.md)

## 📞 Support

For issues or questions:
- Check [OPENSHIFT_DEPLOYMENT.md](../OPENSHIFT_DEPLOYMENT.md) for detailed troubleshooting
- Review OpenShift logs: `oc logs -f deployment/sammo-fight-iq`
- Check application health: `curl https://<route>/health`

---

**Quick Commands Reference**

```bash
# Deploy
./deploy.sh

# Test
./test-api.sh

# Logs
oc logs -f deployment/sammo-fight-iq

# Scale
oc scale deployment/sammo-fight-iq --replicas=3

# Update
oc start-build sammo-fight-iq --from-dir=.. --follow

# URL
echo "https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')"
```
