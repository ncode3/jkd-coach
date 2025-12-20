# SAMMO Fight IQ - Google Cloud Functions Deployment

## 📦 Overview

Serverless deployment of SAMMO Fight IQ using Google Cloud Functions.

## 📁 Files

- `main.py` - Cloud Functions entry point with Flask app

## 🚀 Quick Deployment

### Prerequisites

- Google Cloud SDK installed
- Google Cloud project with Firestore enabled
- Service account with Firestore permissions

### Deploy

```bash
# From this directory
gcloud functions deploy sammo \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --entry-point sammo
```

### With Environment Variables

```bash
gcloud functions deploy sammo \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --entry-point sammo \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project-id
```

## 🔗 Endpoints

After deployment, you'll get a URL like:
```
https://us-central1-your-project.cloudfunctions.net/sammo
```

Available endpoints:
- `POST /log_round` - Log a boxing round
- `GET /dashboard_stats` - Get aggregated statistics
- `GET /rounds_history` - Get round history

## 🧪 Testing

```bash
# Set your function URL
FUNCTION_URL="https://us-central1-your-project.cloudfunctions.net/sammo"

# Log a round
curl -X POST $FUNCTION_URL/log_round \
  -H "Content-Type: application/json" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great session"
  }'

# Get stats
curl $FUNCTION_URL/dashboard_stats

# Get history
curl $FUNCTION_URL/rounds_history
```

## 📊 Monitoring

View logs:
```bash
gcloud functions logs read sammo --limit 50
```

## 🔄 Update

```bash
gcloud functions deploy sammo \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated
```

## 🗑️ Delete

```bash
gcloud functions delete sammo
```

## 💰 Pricing

Google Cloud Functions pricing is based on:
- Number of invocations
- Compute time
- Network egress

See: https://cloud.google.com/functions/pricing

## 📚 Documentation

- [Full Deployment Guide](../../docs/DEPLOYMENT.md)
- [Deployment Options](../README.md)
- [Project Home](../../README.md)

## 🔗 Related

- [OpenShift Deployment](../openshift/) - For on-premises clusters
- [FastAPI with Auth](../fastapi-auth/) - For authenticated API
