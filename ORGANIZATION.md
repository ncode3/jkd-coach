# SAMMO Fight IQ - Project Organization

## 📋 Organization Summary

The project has been reorganized for maximum efficiency and clarity. All files are now logically grouped by purpose, deployment type, and functionality.

## 🎯 Key Changes

### ✅ What Was Done

1. **Created `deployments/` directory** - All deployment configurations organized by type
2. **Created `docs/` directory** - All documentation in one place
3. **Organized by deployment type** - Each deployment has its own isolated directory
4. **Added navigation READMEs** - Every directory has a README with clear navigation
5. **Cleaned root directory** - Only essential files remain at the root
6. **Updated all references** - Links and paths updated throughout

## 📁 New Directory Structure

```
sammo-fight-iq/
│
├── 📄 Essential Files (Root)
│   ├── README.md                # Main project README with navigation
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   ├── .gitignore              # Git ignore patterns
│   └── pyproject.toml          # Python project config
│
├── 📂 deployments/              # All deployment configurations
│   ├── README.md               # Deployment comparison & guide
│   │
│   ├── openshift/              # OpenShift/Kubernetes deployment
│   │   ├── README.md           # OpenShift-specific guide
│   │   ├── app.py              # Flask application
│   │   ├── Dockerfile          # Container definition
│   │   ├── requirements-openshift.txt
│   │   ├── .dockerignore
│   │   ├── deployment.yaml     # Kubernetes manifests
│   │   ├── service.yaml
│   │   ├── route.yaml
│   │   ├── all-in-one.yaml     # Complete deployment
│   │   ├── deploy.sh           # Automated deployment
│   │   └── test-api.sh         # API testing script
│   │
│   ├── cloud-functions/        # Google Cloud Functions deployment
│   │   ├── README.md           # Cloud Functions guide
│   │   └── main.py             # Cloud Functions entry point
│   │
│   └── fastapi-auth/           # FastAPI with JWT authentication
│       ├── README.md           # FastAPI auth guide
│       ├── api_server.py       # FastAPI application
│       ├── auth/               # Authentication module
│       │   ├── models.py
│       │   ├── jwt_handler.py
│       │   ├── user_store.py
│       │   ├── dependencies.py
│       │   └── routes.py
│       └── examples/           # Client examples
│           └── auth_client.py
│
├── 📂 docs/                    # All documentation
│   ├── README.md               # Documentation index
│   ├── OPENSHIFT_DEPLOYMENT.md # Complete OpenShift guide
│   ├── OPENSHIFT_QUICKSTART.md # Quick OpenShift start
│   ├── DEPLOYMENT_COMMANDS.md  # Command reference
│   ├── CONTAINERIZATION_SUMMARY.md
│   ├── AUTH_SETUP.md           # Authentication guide
│   ├── API_QUICKSTART.md       # Quick API start
│   ├── AUTHENTICATION_SUMMARY.md
│   ├── PROJECT_STRUCTURE.md    # Project overview
│   ├── DEPLOYMENT.md           # Cloud Functions guide
│   └── sammo_architecture.svg  # Architecture diagram
│
├── 📂 src/                     # Core source code
│   ├── __init__.py
│   ├── agents/                 # AI coaching agents
│   │   ├── base_coach.py
│   │   └── boxing_coach.py
│   ├── auth/                   # Authentication module (shared)
│   ├── config.py
│   ├── llm_client.py
│   ├── logger.py
│   ├── memory_layer.py
│   ├── risk_model.py
│   └── simple_memory.py
│
├── 📂 notebooks/               # Jupyter notebooks
│   ├── 01_pose_detection_test.ipynb
│   ├── 02_video_processing.ipynb
│   └── 03_model_inference_test.ipynb
│
├── 📂 tests/                   # Test suites
│   ├── test_auth.py           # Authentication tests
│   ├── test_api_integration.py # API integration tests
│   ├── test_risk_model.py
│   └── test_integration_function.py
│
├── 📂 data/                    # Training data and videos
├── 📂 models/                  # Trained ML models
└── 📂 mem_data/                # Conversation history
```

## 🔄 What Moved Where

### Documentation Files

| Old Location (Root) | New Location |
|---------------------|--------------|
| `API_QUICKSTART.md` | `docs/API_QUICKSTART.md` |
| `AUTH_SETUP.md` | `docs/AUTH_SETUP.md` |
| `AUTHENTICATION_SUMMARY.md` | `docs/AUTHENTICATION_SUMMARY.md` |
| `PROJECT_STRUCTURE.md` | `docs/PROJECT_STRUCTURE.md` |
| `OPENSHIFT_DEPLOYMENT.md` | `docs/OPENSHIFT_DEPLOYMENT.md` |
| `OPENSHIFT_QUICKSTART.md` | `docs/OPENSHIFT_QUICKSTART.md` |
| `CONTAINERIZATION_SUMMARY.md` | `docs/CONTAINERIZATION_SUMMARY.md` |
| `DEPLOYMENT_COMMANDS.md` | `docs/DEPLOYMENT_COMMANDS.md` |
| `DEPLOYMENT.md` | `docs/DEPLOYMENT.md` |
| `sammo_architecture.svg` | `docs/sammo_architecture.svg` |

### Deployment Files

| Old Location (Root) | New Location |
|---------------------|--------------|
| `main.py` | `deployments/cloud-functions/main.py` |
| `app.py` | `deployments/openshift/app.py` |
| `Dockerfile` | `deployments/openshift/Dockerfile` |
| `requirements-openshift.txt` | `deployments/openshift/requirements-openshift.txt` |
| `.dockerignore` | `deployments/openshift/.dockerignore` |
| `openshift/*` | `deployments/openshift/*` |
| `api_server.py` | `deployments/fastapi-auth/api_server.py` |
| `src/auth/` | `deployments/fastapi-auth/auth/` (copy) |
| `examples/` | `deployments/fastapi-auth/examples/` |

## 📖 Navigation Guide

### For New Users

1. **Start here**: [README.md](README.md)
2. **Choose deployment**: [deployments/README.md](deployments/README.md)
3. **Follow quick start**:
   - OpenShift: [docs/OPENSHIFT_QUICKSTART.md](docs/OPENSHIFT_QUICKSTART.md)
   - FastAPI Auth: [docs/API_QUICKSTART.md](docs/API_QUICKSTART.md)
   - Cloud Functions: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### For Developers

1. **Project structure**: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
2. **Source code**: [src/](src/)
3. **Tests**: [tests/](tests/)
4. **Notebooks**: [notebooks/](notebooks/)

### For DevOps

1. **Deployment options**: [deployments/README.md](deployments/README.md)
2. **OpenShift deployment**: [deployments/openshift/](deployments/openshift/)
3. **Quick commands**: [docs/DEPLOYMENT_COMMANDS.md](docs/DEPLOYMENT_COMMANDS.md)

### For Documentation

1. **Documentation index**: [docs/README.md](docs/README.md)
2. **All guides organized by topic**
3. **Cross-referenced for easy navigation**

## 🎯 Benefits of New Organization

### 1. Clearer Deployment Options

Each deployment type is completely isolated:
- **OpenShift**: `deployments/openshift/`
- **Cloud Functions**: `deployments/cloud-functions/`
- **FastAPI Auth**: `deployments/fastapi-auth/`

No confusion about which files belong to which deployment.

### 2. Centralized Documentation

All documentation in `docs/`:
- Easy to find
- Organized by topic
- Index with navigation
- No clutter in root

### 3. Clean Root Directory

Only 5 essential files at root:
- `README.md` - Project overview
- `requirements.txt` - Dependencies
- `.env.example` - Configuration template
- `.gitignore` - Git patterns
- `pyproject.toml` - Python config

### 4. Better Navigation

Every directory has a `README.md`:
- Clear purpose
- Quick start instructions
- Links to related files
- Back to parent directory

### 5. Logical Grouping

Files grouped by:
- **Purpose**: Deployment vs docs vs source
- **Type**: OpenShift vs Cloud Functions vs FastAPI
- **Functionality**: Auth vs agents vs utilities

## 🔗 Quick Links

### Most Used Files

| What | Where |
|------|-------|
| Project README | [README.md](README.md) |
| Deploy to OpenShift | [deployments/openshift/deploy.sh](deployments/openshift/deploy.sh) |
| API with Auth | [deployments/fastapi-auth/api_server.py](deployments/fastapi-auth/api_server.py) |
| All Documentation | [docs/README.md](docs/README.md) |
| Deployment Comparison | [deployments/README.md](deployments/README.md) |

### Quick Start Commands

```bash
# OpenShift deployment
cd deployments/openshift && ./deploy.sh

# FastAPI with auth
cd deployments/fastapi-auth && python api_server.py

# Cloud Functions
cd deployments/cloud-functions
gcloud functions deploy sammo --runtime python39 --trigger-http

# View all documentation
ls docs/

# Run tests
pytest tests/ -v
```

## 💡 Tips for Navigation

1. **Start with main README** - Always begin at [README.md](README.md)
2. **Use directory READMEs** - Each directory explains its contents
3. **Follow the links** - Documentation is cross-referenced
4. **Check deployment comparison** - [deployments/README.md](deployments/README.md)
5. **Bookmark docs index** - [docs/README.md](docs/README.md)

## 🔍 Finding Things

### Looking for deployment info?
→ [deployments/README.md](deployments/README.md)

### Looking for documentation?
→ [docs/README.md](docs/README.md)

### Looking for source code?
→ [src/](src/)

### Looking for examples?
→ [deployments/fastapi-auth/examples/](deployments/fastapi-auth/examples/)

### Looking for tests?
→ [tests/](tests/)

## ✅ Organization Checklist

- [x] Deployments organized by type
- [x] Documentation centralized in `docs/`
- [x] Root directory cleaned (5 files only)
- [x] Every directory has README
- [x] All links updated
- [x] Navigation clear and logical
- [x] Files grouped by purpose
- [x] Quick starts accessible
- [x] Cross-references working
- [x] Structure documented

## 🎉 Result

A clean, organized project structure where:
- ✅ Everything has its place
- ✅ Navigation is intuitive
- ✅ Documentation is centralized
- ✅ Deployments are isolated
- ✅ Root is uncluttered
- ✅ Paths are logical

---

**Organization Date**: 2025-12-09
**Structure**: Production-ready and maintainable
**Navigation**: Clear and comprehensive
