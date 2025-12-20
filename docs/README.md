# SAMMO Fight IQ - Documentation

Complete documentation for the SAMMO Fight IQ project.

## 📚 Documentation Index

### 🚀 Getting Started

1. **[Project Overview](../README.md)**
   - What is SAMMO Fight IQ
   - The legacy behind it
   - Core features and capabilities

### 📦 Deployment Guides

2. **[Deployment Options](../deployments/README.md)**
   - Comparison of deployment methods
   - Which deployment to choose

3. **[OpenShift Deployment](./OPENSHIFT_DEPLOYMENT.md)**
   - Complete guide for OpenShift/Kubernetes
   - Container configuration
   - Monitoring and scaling
   - Troubleshooting

4. **[OpenShift Quick Start](./OPENSHIFT_QUICKSTART.md)**
   - 5-minute deployment guide
   - Essential commands
   - Quick testing

5. **[Deployment Commands](./DEPLOYMENT_COMMANDS.md)**
   - Quick command reference
   - Common operations
   - Debug commands

6. **[Containerization Summary](./CONTAINERIZATION_SUMMARY.md)**
   - Implementation overview
   - Architecture details
   - File-by-file breakdown

7. **[Cloud Functions Deployment](./DEPLOYMENT.md)**
   - Google Cloud Functions setup
   - Serverless deployment
   - Configuration

### 🔐 Authentication & API

8. **[Authentication Setup](./AUTH_SETUP.md)**
   - Complete JWT authentication guide
   - Security features
   - API endpoints
   - Usage examples

9. **[API Quick Start](./API_QUICKSTART.md)**
   - 5-minute API setup
   - Quick commands
   - Testing guide

10. **[Authentication Summary](./AUTHENTICATION_SUMMARY.md)**
    - Implementation details
    - Design decisions
    - Security practices

### 📊 Project Structure

11. **[Project Structure](./PROJECT_STRUCTURE.md)**
    - Complete file organization
    - Component descriptions
    - Data flow diagrams

## 🎯 Quick Navigation

### By Use Case

**I want to deploy to OpenShift:**
1. [OpenShift Quick Start](./OPENSHIFT_QUICKSTART.md)
2. [Deployment Commands](./DEPLOYMENT_COMMANDS.md)
3. [Full OpenShift Guide](./OPENSHIFT_DEPLOYMENT.md)

**I want to add user authentication:**
1. [API Quick Start](./API_QUICKSTART.md)
2. [Authentication Setup](./AUTH_SETUP.md)
3. [FastAPI Auth Deployment](../deployments/fastapi-auth/)

**I want serverless deployment:**
1. [Cloud Functions Guide](./DEPLOYMENT.md)
2. [Cloud Functions Deployment](../deployments/cloud-functions/)

**I want to understand the project:**
1. [Project Overview](../README.md)
2. [Project Structure](./PROJECT_STRUCTURE.md)
3. [Architecture Diagram](./sammo_architecture.svg)

## 📁 Documentation by Topic

### Deployment
- [Deployment Options](../deployments/README.md)
- [OpenShift Deployment](./OPENSHIFT_DEPLOYMENT.md)
- [Cloud Functions](./DEPLOYMENT.md)
- [Containerization](./CONTAINERIZATION_SUMMARY.md)

### API & Authentication
- [Authentication Setup](./AUTH_SETUP.md)
- [API Quick Start](./API_QUICKSTART.md)
- [Authentication Implementation](./AUTHENTICATION_SUMMARY.md)

### Reference
- [Project Structure](./PROJECT_STRUCTURE.md)
- [Deployment Commands](./DEPLOYMENT_COMMANDS.md)
- [OpenShift Quick Start](./OPENSHIFT_QUICKSTART.md)

## 🔍 Search Documentation

Looking for something specific?

| Topic | Document |
|-------|----------|
| Docker, Containers | [Containerization Summary](./CONTAINERIZATION_SUMMARY.md) |
| JWT, Authentication | [Authentication Setup](./AUTH_SETUP.md) |
| OpenShift, Kubernetes | [OpenShift Deployment](./OPENSHIFT_DEPLOYMENT.md) |
| API Endpoints | [API Quick Start](./API_QUICKSTART.md) |
| Commands, CLI | [Deployment Commands](./DEPLOYMENT_COMMANDS.md) |
| Quick Deploy | [OpenShift Quick Start](./OPENSHIFT_QUICKSTART.md) |
| Serverless | [Cloud Functions](./DEPLOYMENT.md) |
| File Organization | [Project Structure](./PROJECT_STRUCTURE.md) |

## 📖 Reading Order

### For New Users
1. [Project Overview](../README.md)
2. [Deployment Options](../deployments/README.md)
3. Choose your deployment guide

### For Developers
1. [Project Structure](./PROJECT_STRUCTURE.md)
2. [Authentication Implementation](./AUTHENTICATION_SUMMARY.md)
3. [API Quick Start](./API_QUICKSTART.md)

### For DevOps
1. [OpenShift Deployment](./OPENSHIFT_DEPLOYMENT.md)
2. [Deployment Commands](./DEPLOYMENT_COMMANDS.md)
3. [Containerization Summary](./CONTAINERIZATION_SUMMARY.md)

## 🔗 External Resources

- **OpenShift Documentation**: https://docs.openshift.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **JWT Information**: https://jwt.io/
- **Firestore Documentation**: https://cloud.google.com/firestore/docs
- **Flask Documentation**: https://flask.palletsprojects.com/

## 📞 Getting Help

1. **Start here:** Check the relevant documentation above
2. **Quick reference:** [Deployment Commands](./DEPLOYMENT_COMMANDS.md)
3. **Deployment issues:** [OpenShift Troubleshooting](./OPENSHIFT_DEPLOYMENT.md#troubleshooting)
4. **Auth issues:** [Authentication Setup](./AUTH_SETUP.md#troubleshooting)
5. **Still stuck?** Create an issue on GitHub

## 🎓 Tutorials

- **Deploy to OpenShift in 5 minutes:** [Quick Start](./OPENSHIFT_QUICKSTART.md)
- **Add authentication in 5 minutes:** [API Quick Start](./API_QUICKSTART.md)
- **Run the example client:** [FastAPI Auth Examples](../deployments/fastapi-auth/examples/)

---

**Documentation Structure:**
```
docs/
├── README.md                       # This file - documentation index
├── OPENSHIFT_DEPLOYMENT.md         # Complete OpenShift guide
├── OPENSHIFT_QUICKSTART.md         # Quick OpenShift deployment
├── DEPLOYMENT_COMMANDS.md          # Command reference
├── CONTAINERIZATION_SUMMARY.md     # Container implementation
├── AUTH_SETUP.md                   # Authentication guide
├── API_QUICKSTART.md               # Quick API setup
├── AUTHENTICATION_SUMMARY.md       # Auth implementation
├── PROJECT_STRUCTURE.md            # Project organization
├── DEPLOYMENT.md                   # Cloud Functions guide
└── sammo_architecture.svg          # Architecture diagram
```

**Quick Links:**
- [Back to Project Home](../README.md)
- [Deployment Options](../deployments/README.md)
- [Source Code](../src/)
- [Tests](../tests/)
