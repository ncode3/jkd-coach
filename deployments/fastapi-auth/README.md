# SAMMO Fight IQ - FastAPI with JWT Authentication

## 📦 Overview

Full-featured API server with JWT-based user authentication for SAMMO Fight IQ.

## 📁 Files

```
fastapi-auth/
├── api_server.py          # FastAPI application
├── auth/                  # Authentication module
│   ├── models.py         # User and token models
│   ├── jwt_handler.py    # JWT utilities
│   ├── user_store.py     # Firestore user storage
│   ├── dependencies.py   # FastAPI dependencies
│   └── routes.py         # Auth endpoints
└── examples/             # Usage examples
    └── auth_client.py    # Python client example
```

## ✨ Features

- ✅ User registration and login
- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ User data isolation
- ✅ Protected endpoints
- ✅ Interactive API documentation (Swagger)
- ✅ Firestore integration

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ../..  # Go to project root
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file
cp .env.example .env

# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
echo "JWT_SECRET_KEY=<your-generated-key>" >> .env
```

### 3. Set Firestore Credentials

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 4. Start Server

```bash
cd deployments/fastapi-auth
python api_server.py
```

Server will start at: http://localhost:8000

## 📚 API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## 🔐 Authentication Flow

### 1. Register a User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter1",
    "email": "fighter@example.com",
    "password": "SecurePass123!",
    "full_name": "Fighter One"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter1",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Use Protected Endpoints

```bash
TOKEN="<your-access-token>"

# Log a round
curl -X POST http://localhost:8000/api/log_round \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great session"
  }'

# Get stats
curl http://localhost:8000/api/dashboard_stats \
  -H "Authorization: Bearer $TOKEN"

# Get profile
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## 💻 Python Client Example

```python
from examples.auth_client import SammoClient

# Initialize client
client = SammoClient("http://localhost:8000")

# Register and login
client.register("fighter1", "fighter@example.com", "SecurePass123!", "Fighter One")
client.login("fighter1", "SecurePass123!")

# Use the API
round_data = client.log_round(
    pressure_score=8.0,
    ring_control_score=7.5,
    defense_score=6.0,
    clean_shots_taken=2,
    notes="Great session"
)

# Get stats
stats = client.get_dashboard_stats()
print(f"Total Rounds: {stats['total_rounds']}")
```

Run the example:
```bash
python examples/auth_client.py
```

## 📊 API Endpoints

### Public Endpoints (No Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/health` | Health check |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get token |

### Protected Endpoints (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/me` | Get current user |
| POST | `/api/log_round` | Log boxing round |
| GET | `/api/dashboard_stats` | Get user stats |
| GET | `/api/rounds_history` | Get user's rounds |
| DELETE | `/api/rounds/{id}` | Delete a round |

## 🔐 Security

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET_KEY` | Yes | - | Secret key for JWT signing |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 30 | Token expiration time |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | - | Path to Firestore credentials |

### Best Practices

- ✅ Use strong JWT secret (32+ characters)
- ✅ Never commit `.env` file
- ✅ Use HTTPS in production
- ✅ Rotate JWT secrets periodically
- ✅ Implement rate limiting (production)

## 🧪 Testing

Run the example client:
```bash
python examples/auth_client.py
```

Run unit tests:
```bash
cd ../..  # Go to project root
pytest tests/test_auth.py -v
```

Run integration tests (server must be running):
```bash
pytest tests/test_api_integration.py -v
```

## 🚀 Production Deployment

### With Uvicorn

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn

```bash
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### With Docker

```bash
# Build
docker build -t sammo-fastapi-auth .

# Run
docker run -p 8000:8000 \
  -e JWT_SECRET_KEY=<your-secret> \
  -v /path/to/credentials.json:/secrets/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/credentials.json \
  sammo-fastapi-auth
```

## 📚 Documentation

- [Authentication Setup](../../docs/AUTH_SETUP.md) - Complete auth guide
- [API Quick Start](../../docs/API_QUICKSTART.md) - Quick start guide
- [Authentication Summary](../../docs/AUTHENTICATION_SUMMARY.md) - Implementation details
- [Deployment Options](../README.md) - Compare deployments

## 🔗 Related

- [OpenShift Deployment](../openshift/) - For containerized deployment
- [Cloud Functions](../cloud-functions/) - For serverless deployment
- [Project Home](../../README.md) - Main README

## 🆘 Troubleshooting

### "Could not validate credentials"
- Token expired (30 min default)
- Wrong token format
- JWT secret mismatch

**Solution:** Login again to get new token

### "Username already exists"
**Solution:** Choose different username or login with existing account

### "Firestore connection failed"
**Solution:** Check `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### "Module not found"
**Solution:** Run `pip install -r ../../requirements.txt`

## 📞 Support

- Review [AUTH_SETUP.md](../../docs/AUTH_SETUP.md) for detailed documentation
- Check [examples/auth_client.py](examples/auth_client.py) for usage examples
- Visit http://localhost:8000/docs for interactive API documentation
