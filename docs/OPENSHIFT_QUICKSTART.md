# SAMMO Fight IQ - OpenShift Quick Start

## 🎯 Deploy in 5 Minutes

### Step 1: Prepare Credentials

Download your Google Cloud Firestore service account key:

```bash
# Save your credentials.json file to the project directory
export FIRESTORE_CREDENTIALS=./credentials.json
```

### Step 2: Login to OpenShift

```bash
oc login https://your-openshift-cluster.com
```

### Step 3: Deploy

```bash
cd openshift
chmod +x deploy.sh
./deploy.sh
```

### Step 4: Test

```bash
chmod +x test-api.sh
./test-api.sh
```

## 🎉 That's It!

Your application is now deployed and accessible via HTTPS.

## 📊 Access Your Application

```bash
# Get the URL
oc get route sammo-fight-iq -o jsonpath='{.spec.host}'

# Or visit
API_URL=$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')
echo "https://$API_URL"
```

## 🧪 Test Endpoints

```bash
API_URL=https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')

# Health check
curl $API_URL/health

# Log a round
curl -X POST $API_URL/api/log_round \
  -H "Content-Type: application/json" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great sparring session"
  }'

# Get statistics
curl $API_URL/api/dashboard_stats

# Get history
curl $API_URL/api/rounds_history?limit=10
```

## 📱 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/log_round` | Log boxing round |
| GET | `/api/dashboard_stats` | Get aggregated stats |
| GET | `/api/rounds_history` | Get round history |

## 📈 Monitor Your Application

```bash
# View logs
oc logs -f deployment/sammo-fight-iq

# Check status
oc get pods

# View resource usage
oc top pods
```

## 🔄 Update Application

```bash
# Rebuild and redeploy
oc start-build sammo-fight-iq --from-dir=.. --follow
oc rollout status deployment/sammo-fight-iq
```

## 🆘 Need Help?

- **Full Guide**: See [OPENSHIFT_DEPLOYMENT.md](OPENSHIFT_DEPLOYMENT.md)
- **View Logs**: `oc logs -f deployment/sammo-fight-iq`
- **Check Health**: `curl https://<your-route>/health`
- **OpenShift Docs**: https://docs.openshift.com/

## 🗑️ Clean Up

```bash
# Remove everything
oc delete all -l app=sammo-fight-iq
oc delete secret firestore-credentials
```

---

## 📦 What Was Deployed?

- **Flask Application** running with Gunicorn
- **2 Replicas** for high availability
- **Auto-scaling** (2-10 pods) based on CPU/memory
- **Health checks** for automatic recovery
- **HTTPS Route** with TLS termination
- **Firestore integration** for data persistence

## 🔒 Security Features

- Non-root container
- Security context with dropped capabilities
- Secrets mounted as volumes
- TLS/HTTPS enabled by default
- Network isolation

## ⚙️ Default Configuration

- **Port**: 8080
- **Min Replicas**: 2
- **Max Replicas**: 10
- **Memory Request**: 256Mi
- **Memory Limit**: 512Mi
- **CPU Request**: 100m
- **CPU Limit**: 500m

---

**Happy Boxing! 🥊**
