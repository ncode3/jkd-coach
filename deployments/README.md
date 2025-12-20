# SAMMO Fight IQ - Deployment Options

This directory contains different deployment configurations for SAMMO Fight IQ.

## 📦 Available Deployments

### 1. [OpenShift / Kubernetes](./openshift/)
**Recommended for: On-premises clusters, enterprise deployments**

Containerized Flask application for OpenShift/Kubernetes deployment.

**Features:**
- Docker containerization
- Auto-scaling (2-10 pods)
- Health checks
- HTTPS/TLS
- Firestore integration
- Production-ready with Gunicorn

**Files:**
- `app.py` - Flask application
- `Dockerfile` - Container definition
- Deployment manifests (YAML)
- Automated deployment scripts

**Quick Start:**
```bash
cd openshift
./deploy.sh
```

📖 [Full Documentation](./openshift/README.md)

---

### 2. [Google Cloud Functions](./cloud-functions/)
**Recommended for: Serverless deployment, pay-per-use**

Serverless deployment using Google Cloud Functions with Flask.

**Features:**
- Serverless (no infrastructure management)
- Automatic scaling
- Pay-per-invocation pricing
- Direct Firestore integration
- CORS enabled

**Files:**
- `main.py` - Cloud Functions entry point

**Quick Start:**
```bash
cd cloud-functions
gcloud functions deploy sammo --runtime python39 --trigger-http --allow-unauthenticated
```

📖 [Full Documentation](../docs/DEPLOYMENT.md)

---

### 3. [FastAPI with JWT Authentication](./fastapi-auth/)
**Recommended for: API-first applications, user authentication needed**

Full-featured API server with JWT-based user authentication.

**Features:**
- User registration and login
- JWT token authentication
- Password hashing (bcrypt)
- User data isolation
- Protected endpoints
- Swagger/OpenAPI documentation
- Firestore user storage

**Files:**
- `api_server.py` - FastAPI application
- `auth/` - Authentication module
- `examples/` - Client examples

**Quick Start:**
```bash
cd fastapi-auth
pip install -r ../../requirements.txt
python api_server.py
# Visit http://localhost:8000/docs
```

📖 [Full Documentation](../docs/AUTH_SETUP.md)

---

## 🔄 Comparison

| Feature | OpenShift | Cloud Functions | FastAPI Auth |
|---------|-----------|-----------------|--------------|
| **Deployment** | Container | Serverless | Container/Local |
| **Scaling** | Auto (2-10) | Automatic | Manual/HPA |
| **Authentication** | ❌ No | ❌ No | ✅ Yes (JWT) |
| **Cost Model** | Fixed | Pay-per-use | Fixed |
| **TLS/HTTPS** | ✅ Yes | ✅ Yes | Manual setup |
| **Infrastructure** | Kubernetes | Managed | Self-managed |
| **Best For** | Enterprise | Serverless | API products |

## 🎯 Which Deployment Should I Use?

### Choose **OpenShift** if you:
- Have an on-premises Kubernetes/OpenShift cluster
- Need enterprise-grade deployment
- Want containerized applications
- Need auto-scaling and high availability
- Prefer infrastructure control

### Choose **Cloud Functions** if you:
- Want serverless deployment
- Prefer pay-per-use pricing
- Don't want to manage infrastructure
- Have variable/unpredictable traffic
- Need quick deployment

### Choose **FastAPI Auth** if you:
- Need user authentication
- Building a user-facing application
- Want JWT-based security
- Need user data isolation
- Prefer API-first architecture
- Want interactive API documentation

## 📚 Documentation

- [OpenShift Deployment Guide](../docs/OPENSHIFT_DEPLOYMENT.md)
- [Cloud Functions Guide](../docs/DEPLOYMENT.md)
- [Authentication Setup](../docs/AUTH_SETUP.md)
- [API Quick Start](../docs/API_QUICKSTART.md)

## 🔗 Common Files

All deployments share:
- `src/` - Core source code (agents, models, utilities)
- `notebooks/` - Jupyter notebooks for analysis
- `tests/` - Test suites
- `data/` - Training data
- `models/` - ML models

## 🆘 Need Help?

1. Check the specific deployment's README
2. Review the documentation in `docs/`
3. Check the main [project README](../README.md)
4. Create an issue on GitHub

---

**Quick Links:**
- [Project Home](../README.md)
- [Documentation](../docs/)
- [Source Code](../src/)
- [Tests](../tests/)
