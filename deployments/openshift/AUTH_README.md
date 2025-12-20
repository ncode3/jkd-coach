# SAMMO Fight IQ - OpenShift Authentication

## 🔐 Overview

The OpenShift deployment now includes JWT-based authentication with user registration, login, and protected endpoints. All boxing data endpoints require authentication, and users can only access their own data.

## ✨ Features

- ✅ User registration and login
- ✅ JWT token authentication (same tokens as FastAPI deployment)
- ✅ Password hashing with bcrypt
- ✅ User data isolation (users only see their own rounds)
- ✅ Protected endpoints with `@require_auth` decorator
- ✅ Firestore user storage (shared with FastAPI deployment)

## 📁 Files

| File | Purpose |
|------|---------|
| `auth_flask.py` | Flask authentication module (JWT handlers, decorators) |
| `app.py` | Main Flask application with protected endpoints |
| `requirements-openshift.txt` | Updated with auth dependencies |

## 🔑 Environment Variables

Add to your OpenShift deployment:

```bash
# Required for JWT authentication
JWT_SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30  # Optional, default is 30

# Required for Firestore
GOOGLE_APPLICATION_CREDENTIALS=/secrets/credentials.json
```

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Quick Start

### 1. Set JWT Secret in OpenShift

```bash
# Create secret for JWT key
oc create secret generic jwt-secret \
  --from-literal=JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Update deployment to use the secret
oc set env deployment/sammo-fight-iq --from=secret/jwt-secret
```

### 2. Deploy

```bash
cd deployments/openshift
./deploy.sh
```

The deployment script will automatically build and deploy the authenticated version.

### 3. Test Authentication

```bash
API_URL=https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')

# Register a user
curl -X POST $API_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter1",
    "email": "fighter@example.com",
    "password": "SecurePass123!",
    "full_name": "Fighter One"
  }'

# Login
TOKEN=$(curl -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter1",
    "password": "SecurePass123!"
  }' | jq -r '.access_token')

# Use protected endpoint
curl -X POST $API_URL/api/log_round \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great session"
  }'
```

## 📊 API Endpoints

### Public Endpoints (No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get token |

### Protected Endpoints (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/me` | Get current user profile |
| POST | `/api/log_round` | Log boxing round |
| GET | `/api/dashboard_stats` | Get user's statistics |
| GET | `/api/rounds_history` | Get user's round history |
| DELETE | `/api/rounds/{id}` | Delete user's round |

## 🔐 Authentication Flow

### 1. Register

```bash
curl -X POST https://your-api.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter1",
    "email": "fighter@example.com",
    "password": "SecurePass123!",
    "full_name": "Fighter One"
  }'
```

Response:
```json
{
  "status": "success",
  "user": {
    "id": "uuid",
    "username": "fighter1",
    "email": "fighter@example.com",
    "full_name": "Fighter One",
    "is_active": true,
    "is_verified": false
  }
}
```

### 2. Login

```bash
curl -X POST https://your-api.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter1",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Use Protected Endpoints

```bash
curl -X GET https://your-api.com/api/dashboard_stats \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## 🔒 Security Features

### Password Security
- Bcrypt hashing with automatic salting
- Minimum 8 character requirement
- Passwords never stored in plain text

### Token Security
- JWT with HS256 algorithm
- 30-minute expiration (configurable)
- Signature validation on every request
- Token contains user ID and username

### Data Isolation
- All rounds queries filtered by `user_id`
- Users can only access their own data
- Authorization checks on delete operations

### API Security
- Bearer token authentication
- Invalid token returns 401
- Missing token returns 401
- Expired token returns 401

## 📝 Code Example

### Flask Authentication Decorator

The `@require_auth` decorator protects endpoints:

```python
from auth_flask import require_auth, get_current_user

@app.route('/api/log_round', methods=['POST'])
@require_auth
def log_round():
    user = get_current_user()  # Get authenticated user
    # ... endpoint logic with user context
```

### Manual Token Verification

```python
from auth_flask import decode_token

token = "eyJhbGciOiJIUzI1NiIs..."
payload = decode_token(token)

if payload:
    user_id = payload.get('sub')
    username = payload.get('username')
```

## 🗄️ Database Schema

### Users Collection (Firestore)

```
users/{user_id}
├── id: string
├── username: string (indexed)
├── email: string (indexed)
├── full_name: string
├── hashed_password: string
├── created_at: timestamp
├── is_active: boolean
└── is_verified: boolean
```

### Rounds Collection (Updated)

```
rounds/{round_id}
├── user_id: string (indexed) ← NEW
├── username: string ← NEW
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

## 🔄 Token Compatibility

The JWT tokens are **100% compatible** between:
- OpenShift Flask deployment (`deployments/openshift/app.py`)
- FastAPI deployment (`deployments/fastapi-auth/api_server.py`)

Both use the same:
- Secret key
- Algorithm (HS256)
- Token structure
- User store (Firestore)

**You can use a token from one deployment in the other!**

## 🧪 Testing

### Test Script

Create `test_auth.sh`:

```bash
#!/bin/bash
API_URL=https://$(oc get route sammo-fight-iq -o jsonpath='{.spec.host}')

echo "1. Register user"
curl -X POST $API_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","email":"test1@test.com","password":"TestPass123!"}'

echo -e "\n\n2. Login"
TOKEN=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","password":"TestPass123!"}' | jq -r '.access_token')

echo "Token: $TOKEN"

echo -e "\n\n3. Get profile"
curl $API_URL/auth/me \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\n4. Log round"
curl -X POST $API_URL/api/log_round \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2
  }'

echo -e "\n\n5. Get stats"
curl $API_URL/api/dashboard_stats \
  -H "Authorization: Bearer $TOKEN"
```

## 🐛 Troubleshooting

### "Authentication required"
- Missing Authorization header
- Token not in format `Bearer <token>`

**Solution:** Include header: `Authorization: Bearer your-token-here`

### "Could not validate credentials"
- Token expired (30 min default)
- Invalid token
- Wrong secret key

**Solution:** Login again to get new token

### "Username already exists"
**Solution:** Choose different username or login with existing account

### "Password must be at least 8 characters"
**Solution:** Use longer password

### Authentication not working after deployment
- Check JWT_SECRET_KEY environment variable is set
- Verify Firestore credentials are mounted
- Check pod logs: `oc logs deployment/sammo-fight-iq`

## 📦 Deployment Checklist

- [ ] Set JWT_SECRET_KEY environment variable
- [ ] Firestore credentials secret exists
- [ ] Deploy with updated app.py and auth_flask.py
- [ ] Test registration endpoint
- [ ] Test login endpoint
- [ ] Test protected endpoints with token
- [ ] Verify user data isolation

## 🔗 Related Documentation

- [OpenShift Deployment Guide](../../docs/OPENSHIFT_DEPLOYMENT.md)
- [Authentication Setup (FastAPI)](../../docs/AUTH_SETUP.md)
- [Deployment Commands](../../docs/DEPLOYMENT_COMMANDS.md)

## 💡 Tips

1. **Tokens work across deployments** - Same secret = same tokens work everywhere
2. **Use environment variables** - Never hardcode JWT_SECRET_KEY
3. **Test without auth first** - Verify Firestore connection before adding auth
4. **Monitor token expiration** - Default 30 min, adjust as needed
5. **Secure the secret** - Use OpenShift secrets, not ConfigMaps

---

**Authentication Type**: JWT Bearer Token
**Token Expiration**: 30 minutes (configurable)
**Password Hashing**: Bcrypt
**User Storage**: Firestore
**Compatibility**: Works with FastAPI deployment tokens
