# SAMMO Fight IQ - Quick Deployment Commands

## 🚀 One-Line Deployment

```bash
export FIRESTORE_CREDENTIALS=/path/to/credentials.json && cd openshift && chmod +x deploy.sh test-api.sh && ./deploy.sh && ./test-api.sh
```

## 📋 Step-by-Step Commands

### 1. Setup
```bash
# Login to OpenShift
oc login https://your-cluster.com

# Set credentials path
export FIRESTORE_CREDENTIALS=/path/to/credentials.json
```

### 2. Deploy
```bash
cd openshift
chmod +x deploy.sh test-api.sh
./deploy.sh
```

### 3. Test
```bash
./test-api.sh
```

## 🔍 Useful Commands

### Get Application URL
```bash
echo "https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')"
```

### View Logs (Real-time)
```bash
oc logs -f deployment/sammo-fight-iq
```

### Check Pod Status
```bash
oc get pods -l app=sammo-fight-iq
```

### Scale Application
```bash
oc scale deployment/sammo-fight-iq --replicas=5
```

### Restart Application
```bash
oc rollout restart deployment/sammo-fight-iq
```

### Delete Everything
```bash
oc delete all -l app=sammo-fight-iq
oc delete secret firestore-credentials
```

## 🧪 Test Endpoints

### Set API URL
```bash
API_URL=https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')
```

### Health Check
```bash
curl $API_URL/health | jq
```

### Log Round
```bash
curl -X POST $API_URL/api/log_round \
  -H "Content-Type: application/json" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Test"
  }' | jq
```

### Get Stats
```bash
curl $API_URL/api/dashboard_stats | jq
```

### Get History
```bash
curl $API_URL/api/rounds_history?limit=5 | jq
```

## 🔄 Update Workflow

```bash
# 1. Make code changes to app.py

# 2. Rebuild image
oc start-build sammo-fight-iq --from-dir=.. --follow

# 3. Deployment auto-updates (or force restart)
oc rollout restart deployment/sammo-fight-iq

# 4. Check rollout
oc rollout status deployment/sammo-fight-iq

# 5. Test
curl $API_URL/health
```

## 🐛 Debug Commands

### Pod Logs
```bash
# List pods
oc get pods

# Tail logs
oc logs -f <pod-name>

# Previous logs (if crashed)
oc logs <pod-name> --previous
```

### Pod Shell
```bash
# Access pod shell
oc rsh <pod-name>

# Or execute command
oc exec <pod-name> -- curl http://localhost:8080/health
```

### Describe Resources
```bash
# Describe pod
oc describe pod <pod-name>

# Describe deployment
oc describe deployment sammo-fight-iq

# Get events
oc get events --sort-by='.lastTimestamp'
```

## 🔐 Secret Management

### Update Firestore Credentials
```bash
oc create secret generic firestore-credentials \
  --from-file=credentials.json=/path/to/new-credentials.json \
  --dry-run=client -o yaml | oc apply -f -

oc rollout restart deployment/sammo-fight-iq
```

### View Secret (be careful!)
```bash
oc get secret firestore-credentials -o yaml
```

## 📊 Monitoring

### Resource Usage
```bash
oc top pods -l app=sammo-fight-iq
```

### HPA Status
```bash
oc get hpa sammo-fight-iq
```

### Watch Pods
```bash
watch oc get pods
```

## 🔄 Rollback

### View History
```bash
oc rollout history deployment/sammo-fight-iq
```

### Rollback
```bash
# To previous version
oc rollout undo deployment/sammo-fight-iq

# To specific revision
oc rollout undo deployment/sammo-fight-iq --to-revision=2
```

## 📦 Build Commands

### View BuildConfigs
```bash
oc get bc
```

### View Builds
```bash
oc get builds
```

### Build Logs
```bash
oc logs -f bc/sammo-fight-iq
```

### Start New Build
```bash
oc start-build sammo-fight-iq --from-dir=.. --follow
```

## 🌐 Network Commands

### Port Forward
```bash
oc port-forward deployment/sammo-fight-iq 8080:8080
# Then access: http://localhost:8080
```

### Get Route
```bash
oc get route sammo-fight-iq
```

### Route Details
```bash
oc describe route sammo-fight-iq
```

## 🧹 Cleanup Commands

### Delete Application
```bash
oc delete all -l app=sammo-fight-iq
```

### Delete Secret
```bash
oc delete secret firestore-credentials
```

### Delete Project
```bash
oc delete project sammo-fight-iq
```

---

## 💡 Pro Tips

1. **Save API URL as variable:**
   ```bash
   export API_URL=https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')
   ```

2. **Create alias for logs:**
   ```bash
   alias sammo-logs='oc logs -f deployment/sammo-fight-iq'
   ```

3. **Quick health check:**
   ```bash
   curl -s $(oc get route sammo-fight-iq -o jsonpath='https://{.spec.host}')/health | jq
   ```

4. **Watch deployment:**
   ```bash
   watch oc get pods,deployment,hpa
   ```

5. **Export resources:**
   ```bash
   oc get all -l app=sammo-fight-iq -o yaml > backup.yaml
   ```

---

**Quick Links:**
- [Quick Start](OPENSHIFT_QUICKSTART.md)
- [Full Guide](OPENSHIFT_DEPLOYMENT.md)
- [Summary](CONTAINERIZATION_SUMMARY.md)
