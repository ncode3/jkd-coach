# SAMMO Fight IQ - Complete Project Structure

## 📁 Directory Overview

```
sammo-fight-iq/
│
├── 📄 API & Authentication Documentation
│   ├── API_QUICKSTART.md              # Quick start guide for using the API
│   ├── AUTH_SETUP.md                  # Comprehensive authentication setup
│   ├── AUTHENTICATION_SUMMARY.md      # Implementation summary
│   ├── README.md                      # Main project README
│   └── DEPLOYMENT.md                  # Deployment instructions
│
├── 🔧 Configuration Files
│   ├── .env.example                   # Environment variables template
│   ├── .gitignore                     # Git ignore patterns
│   ├── pyproject.toml                 # Python project configuration
│   └── requirements.txt               # Python dependencies
│
├── 🌐 API Servers
│   ├── api_server.py                  # FastAPI server with JWT auth ⭐ NEW
│   └── main.py                        # Google Cloud Functions handler
│
├── 📂 Source Code (src/)
│   ├── __init__.py
│   ├── config.py                      # Configuration settings
│   ├── llm_client.py                  # LLM client for coaching
│   ├── logger.py                      # Logging utilities
│   ├── memory_layer.py                # Memory-backed LLM wrapper
│   ├── risk_model.py                  # Risk scoring model
│   ├── simple_memory.py               # JSONL-based conversation store
│   │
│   ├── 🤖 agents/                     # AI Coaching Agents
│   │   ├── __init__.py
│   │   ├── base_coach.py              # Base coach class
│   │   └── boxing_coach.py            # SAMMO coaching personality
│   │
│   └── 🔒 auth/                       # Authentication Module ⭐ NEW
│       ├── __init__.py
│       ├── models.py                  # Pydantic models for auth
│       ├── jwt_handler.py             # JWT token management
│       ├── user_store.py              # Firestore user storage
│       ├── dependencies.py            # FastAPI auth dependencies
│       └── routes.py                  # Authentication endpoints
│
├── 📊 Data & Storage
│   ├── data/                          # Round data and videos
│   │   ├── round1.json
│   │   ├── round1.mp4
│   │   └── video_round_stats.csv
│   │
│   ├── mem_data/                      # Conversation memory
│   │   ├── mem_store.jsonl
│   │   └── test.jsonl
│   │
│   └── models/                        # Trained ML models
│       ├── danger_predictor.joblib
│       ├── feature_columns.pkl
│       ├── focus_predictor.joblib
│       └── sammo_fight_iq_models.zip
│
├── 📓 Jupyter Notebooks (notebooks/)
│   ├── 01_pose_detection_test.ipynb   # Pose detection testing
│   ├── 02_video_processing.ipynb      # Video analysis pipeline
│   └── 03_model_inference_test.ipynb  # Model testing
│
├── 💡 Examples (examples/)            ⭐ NEW
│   └── auth_client.py                 # Python client example
│
├── 🧪 Tests (tests/)
│   ├── __init__.py
│   ├── test_auth.py                   # Auth unit tests ⭐ NEW
│   ├── test_api_integration.py        # API integration tests ⭐ NEW
│   ├── test_integration_function.py   # Function integration tests
│   └── test_risk_model.py             # Risk model tests
│
└── 📐 Documentation Assets (docs/)
    └── sammo_architecture.svg          # Architecture diagram
```

## 🔑 Key Components

### 1. Authentication System ⭐ NEW

**Location**: `src/auth/`

The complete JWT-based authentication implementation:

- **models.py**: User and token data models
- **jwt_handler.py**: Token creation, validation, password hashing
- **user_store.py**: Firestore CRUD operations for users
- **dependencies.py**: FastAPI dependency injection for auth
- **routes.py**: Registration, login, profile endpoints

**Purpose**: Secure user authentication and authorization for all API endpoints

### 2. API Server ⭐ UPDATED

**Location**: `api_server.py`

FastAPI application with:
- JWT authentication on all boxing endpoints
- User-specific data isolation
- CORS configuration
- Interactive documentation at `/docs`

**Endpoints**:
- Public: `/auth/register`, `/auth/login`, `/api/health`
- Protected: `/api/log_round`, `/api/dashboard_stats`, `/api/rounds_history`

### 3. AI Coaching Agents

**Location**: `src/agents/`

- **base_coach.py**: Abstract base class for coaches
- **boxing_coach.py**: SAMMO personality with boxing expertise

**Purpose**: Provide personalized coaching feedback using LLM

### 4. ML Models

**Location**: `models/`

- **danger_predictor.joblib**: Predicts danger score from metrics
- **focus_predictor.joblib**: Recommends training focus areas
- **feature_columns.pkl**: Feature definitions

**Purpose**: Risk scoring and strategic recommendations

### 5. Video Processing

**Location**: `notebooks/`

Jupyter notebooks for:
- Pose detection with MediaPipe
- Video analysis and metric extraction
- Model training and inference

**Purpose**: Extract boxing metrics from video footage

## 📚 Documentation Files

### User Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview and motivation | Everyone |
| `API_QUICKSTART.md` | Quick start guide | Developers |
| `AUTH_SETUP.md` | Authentication setup details | Developers |
| `AUTHENTICATION_SUMMARY.md` | Implementation summary | Developers/Reviewers |
| `DEPLOYMENT.md` | Deployment instructions | DevOps |

### Technical Documentation

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment configuration template |
| `pyproject.toml` | Project metadata |
| `/docs` endpoint | Interactive API documentation |

## 🧪 Testing Strategy

### Unit Tests
**Location**: `tests/test_auth.py`

Tests for:
- Password hashing and verification
- JWT token creation and validation
- Token expiration
- Model validation

**Run**: `pytest tests/test_auth.py -v`

### Integration Tests
**Location**: `tests/test_api_integration.py`

Tests for:
- Complete authentication flow
- Protected endpoint access
- User data isolation
- Round logging and retrieval

**Run**: `pytest tests/test_api_integration.py -v` (requires running server)

### ML Model Tests
**Location**: `tests/test_risk_model.py`

Tests for risk scoring and predictions

## 💡 Example Code

### Python Client
**Location**: `examples/auth_client.py`

Complete example showing:
- User registration
- Login and token management
- Logging rounds
- Retrieving statistics
- Deleting rounds

**Run**: `python examples/auth_client.py`

## 🗄️ Data Storage

### Firestore Collections

#### users/ ⭐ NEW
```
users/{user_id}/
├── id: string
├── username: string (indexed)
├── email: string (indexed)
├── full_name: string
├── hashed_password: string
├── created_at: timestamp
├── is_active: boolean
└── is_verified: boolean
```

#### rounds/ (updated)
```
rounds/{round_id}/
├── user_id: string (indexed) ⭐ NEW
├── username: string ⭐ NEW
├── pressure_score: number
├── ring_control_score: number
├── defense_score: number
├── clean_shots_taken: number
├── danger_score: number
├── strategy_title: string
├── strategy_text: string
├── notes: string
└── date: timestamp
```

### Local Storage

- **mem_data/**: JSONL files for conversation history
- **data/**: Training data and video files
- **models/**: Serialized ML models

## 🔄 Data Flow

### 1. User Authentication Flow
```
Client
  → POST /auth/register → UserStore → Firestore (users/)
  → POST /auth/login → JWT Token
  → Headers: Authorization: Bearer <token>
```

### 2. Round Logging Flow
```
Client (with token)
  → POST /api/log_round
  → Validate JWT
  → Calculate danger_score
  → Get strategy
  → Store in Firestore (rounds/)
  → Return response
```

### 3. Stats Retrieval Flow
```
Client (with token)
  → GET /api/dashboard_stats
  → Validate JWT
  → Query Firestore (filter by user_id)
  → Calculate averages
  → Return aggregated stats
```

## 🚀 Deployment Options

### 1. Local Development
```bash
uvicorn api_server:app --reload
```

### 2. Production with Uvicorn
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Google Cloud Run
Use the existing `DEPLOYMENT.md` guide

### 4. Docker (Future)
Containerized deployment

## 🔐 Security Layers

### 1. Password Security
- Bcrypt hashing with automatic salting
- Minimum 8 character requirement
- Never stored in plain text

### 2. Token Security
- JWT with HS256 algorithm
- 30-minute expiration
- Signature validation on every request

### 3. API Security
- Authentication required for sensitive endpoints
- User data isolation at query level
- CORS configuration
- HTTPS recommended for production

### 4. Environment Security
- Secrets in environment variables
- `.env` excluded from git
- Service account credentials protected

## 📊 Metrics & Monitoring

### Application Metrics
- User registrations
- Login attempts (success/failure)
- API request rates
- Token validation failures
- Round logging frequency

### Boxing Metrics
- Danger scores over time
- Average metrics per user
- Training focus trends
- Round count per user

## 🛠️ Development Workflow

### 1. Setup
```bash
git clone <repo>
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

### 2. Development
```bash
# Start API server
python api_server.py

# Run tests
pytest tests/ -v

# Try example client
python examples/auth_client.py
```

### 3. Testing
```bash
# Unit tests
pytest tests/test_auth.py -v

# Integration tests (server must be running)
pytest tests/test_api_integration.py -v
```

### 4. Documentation
```bash
# Interactive docs
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc
```

## 🎯 Integration Points

### Current Integrations
1. **Firestore**: User and round data storage
2. **FastAPI**: REST API framework
3. **JWT**: Token-based authentication
4. **MediaPipe**: Pose detection (in notebooks)
5. **scikit-learn**: ML models for predictions

### Future Integrations
1. **Ollama**: Local LLM for coaching
2. **Streamlit/Gradio**: Web UI
3. **OAuth**: Third-party authentication
4. **Redis**: Caching and rate limiting
5. **SendGrid**: Email verification

## 📈 Roadmap Alignment

| Feature | Status | Location |
|---------|--------|----------|
| Video pose detection | ✅ Complete | notebooks/ |
| Risk scoring model | ✅ Complete | models/ |
| Agentic coach | ✅ Complete | src/agents/ |
| JWT Authentication | ✅ Complete | src/auth/ ⭐ NEW |
| FastAPI server | ✅ Complete | api_server.py ⭐ UPDATED |
| Production LLM | 🔄 In Progress | - |
| Web UI | 📋 Planned | - |
| OAuth integration | 📋 Planned | - |

## 🐛 Troubleshooting Guide

### Import Errors
**Issue**: `ModuleNotFoundError`
**Solution**: `pip install -r requirements.txt`

### Authentication Errors
**Issue**: "Could not validate credentials"
**Solution**: Check token expiration, format, and secret key

### Firestore Connection
**Issue**: "Failed to connect to Firestore"
**Solution**: Verify GOOGLE_APPLICATION_CREDENTIALS path

### Port Already in Use
**Issue**: "Address already in use"
**Solution**: Change port with `--port 8001` or kill existing process

## 📞 Getting Help

1. **Documentation**: Start with API_QUICKSTART.md
2. **API Docs**: http://localhost:8000/docs
3. **Examples**: See examples/auth_client.py
4. **Tests**: Run tests to verify setup
5. **Issues**: Create GitHub issue with details

## ⚡ Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python api_server.py

# Run all tests
pytest tests/ -v

# Run example client
python examples/auth_client.py

# View API docs
open http://localhost:8000/docs

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🎓 Learning Path

### For New Developers
1. Read README.md for project context
2. Follow API_QUICKSTART.md to set up
3. Run examples/auth_client.py to see it work
4. Explore /docs for API reference
5. Review src/auth/ to understand implementation

### For API Users
1. API_QUICKSTART.md - Get started fast
2. AUTH_SETUP.md - Detailed API reference
3. /docs endpoint - Interactive testing
4. examples/auth_client.py - Code examples

### For Contributors
1. AUTHENTICATION_SUMMARY.md - Implementation overview
2. tests/ - Test examples
3. src/auth/ - Core implementation
4. DEPLOYMENT.md - Deployment guide

---

**Last Updated**: 2025-12-09
**Authentication System**: ✅ Fully Implemented
**API Status**: 🟢 Operational
