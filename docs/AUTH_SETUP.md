# SAMMO Fight IQ - Authentication Setup

## Overview

This document describes the JWT-based authentication system implemented for SAMMO Fight IQ. The system provides secure user registration, login, and protected API endpoints.

## Features

- **JWT Token-Based Authentication**: Secure stateless authentication using JSON Web Tokens
- **Password Hashing**: Bcrypt-based password hashing for security
- **User Management**: Registration, login, profile access, and account deactivation
- **Protected Endpoints**: All boxing round and analysis endpoints require authentication
- **User Isolation**: Users can only access their own boxing data
- **Firestore Integration**: User credentials stored securely in Google Cloud Firestore

## Architecture

```
src/auth/
├── __init__.py              # Auth module initialization
├── models.py                # Pydantic models for users and tokens
├── jwt_handler.py           # JWT token generation and validation
├── user_store.py            # Firestore user storage layer
├── dependencies.py          # FastAPI authentication dependencies
└── routes.py                # Authentication endpoints

api_server.py                # Main FastAPI application with protected routes
```

## Environment Variables

Set these environment variables for configuration:

```bash
# Required
JWT_SECRET_KEY=your-super-secret-key-min-32-chars

# Optional (with defaults)
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**IMPORTANT**: Generate a secure secret key for production:

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -hex 32
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
export JWT_SECRET_KEY="your-generated-secret-key"
```

3. Ensure Google Cloud credentials are configured:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

## Running the API Server

Start the FastAPI server:

```bash
# Development
python api_server.py

# Production with Uvicorn
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4

# With auto-reload for development
uvicorn api_server:app --reload
```

The API will be available at `http://localhost:8000`

Interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### Authentication Endpoints

#### Register a New User

```http
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "id": "uuid-string",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2025-12-09T10:00:00",
  "is_active": true,
  "is_verified": false
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Get Current User Info

```http
GET /auth/me
Authorization: Bearer <your-access-token>
```

Response:
```json
{
  "id": "uuid-string",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2025-12-09T10:00:00",
  "is_active": true,
  "is_verified": false
}
```

### Protected Boxing Endpoints

All boxing endpoints require authentication via `Authorization: Bearer <token>` header.

#### Log a Boxing Round

```http
POST /api/log_round
Authorization: Bearer <your-access-token>
Content-Type: application/json

{
  "pressure_score": 7.5,
  "ring_control_score": 6.0,
  "defense_score": 5.0,
  "clean_shots_taken": 3,
  "notes": "Good session, need to work on defense"
}
```

Response:
```json
{
  "status": "success",
  "id": "round-id",
  "danger_score": 0.52,
  "strategy": {
    "title": "RING_CUTTING",
    "text": "Smart pressure. Cut exits, feint to draw counters..."
  }
}
```

#### Get Dashboard Statistics

```http
GET /api/dashboard_stats
Authorization: Bearer <your-access-token>
```

Response:
```json
{
  "averages": {
    "pressure_score": 7.2,
    "ring_control_score": 6.5,
    "defense_score": 5.8,
    "clean_shots_taken": 2.5
  },
  "most_recent_round_date": "2025-12-09T10:00:00",
  "next_game_plan": {
    "title": "RING_CUTTING",
    "text": "Smart pressure. Cut exits..."
  },
  "total_rounds": 15
}
```

#### Get Round History

```http
GET /api/rounds_history?limit=50
Authorization: Bearer <your-access-token>
```

Response:
```json
{
  "rounds": [
    {
      "id": "round-id",
      "date": "2025-12-09T10:00:00",
      "pressure_score": 7.5,
      "ring_control_score": 6.0,
      "defense_score": 5.0,
      "clean_shots_taken": 3,
      "danger_score": 0.52,
      "notes": "Good session"
    }
  ],
  "total": 15
}
```

#### Delete a Round

```http
DELETE /api/rounds/{round_id}
Authorization: Bearer <your-access-token>
```

## Usage Examples

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Register
register_data = {
    "username": "fighter123",
    "email": "fighter@example.com",
    "password": "MySecurePass123!",
    "full_name": "Mike Tyson"
}
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(response.json())

# 2. Login
login_data = {
    "username": "fighter123",
    "password": "MySecurePass123!"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token_data = response.json()
access_token = token_data["access_token"]

# 3. Set up headers
headers = {
    "Authorization": f"Bearer {access_token}"
}

# 4. Log a round
round_data = {
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great sparring session"
}
response = requests.post(
    f"{BASE_URL}/api/log_round",
    json=round_data,
    headers=headers
)
print(response.json())

# 5. Get dashboard stats
response = requests.get(f"{BASE_URL}/api/dashboard_stats", headers=headers)
print(response.json())
```

### cURL Examples

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter123",
    "email": "fighter@example.com",
    "password": "MySecurePass123!",
    "full_name": "Mike Tyson"
  }'

# Login
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fighter123",
    "password": "MySecurePass123!"
  }' | jq -r '.access_token')

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
curl -X GET http://localhost:8000/api/dashboard_stats \
  -H "Authorization: Bearer $TOKEN"
```

## Security Best Practices

1. **Secret Key Management**
   - Never commit `JWT_SECRET_KEY` to version control
   - Use environment variables or secret management systems
   - Rotate keys periodically

2. **Password Requirements**
   - Minimum 8 characters (enforced in model)
   - Consider adding complexity requirements in production

3. **HTTPS in Production**
   - Always use HTTPS in production
   - JWT tokens in plain HTTP can be intercepted

4. **Token Expiration**
   - Default access token expires in 30 minutes
   - Implement refresh token flow for longer sessions

5. **Rate Limiting**
   - Consider adding rate limiting to auth endpoints
   - Prevent brute force attacks

## Firestore Data Structure

### Users Collection

```
users/
  {user_id}/
    - id: string
    - username: string (indexed)
    - email: string (indexed)
    - full_name: string
    - hashed_password: string
    - created_at: timestamp
    - is_active: boolean
    - is_verified: boolean
```

### Rounds Collection (with user association)

```
rounds/
  {round_id}/
    - user_id: string (indexed)
    - username: string
    - pressure_score: number
    - ring_control_score: number
    - defense_score: number
    - clean_shots_taken: number
    - danger_score: number
    - strategy_title: string
    - strategy_text: string
    - notes: string
    - date: timestamp
```

## Testing

The authentication system can be tested using the interactive API docs:

1. Start the server
2. Navigate to `http://localhost:8000/docs`
3. Use the "Authorize" button to set your bearer token
4. Test protected endpoints

## Troubleshooting

### "Could not validate credentials"
- Token may be expired (30 min default)
- Token format incorrect (should be `Bearer <token>`)
- Secret key mismatch between token generation and validation

### "Username already exists"
- Try a different username
- Check Firestore for existing user

### "User account is inactive"
- User has been deactivated
- Contact admin or reactivate account

## Future Enhancements

- [ ] Email verification flow
- [ ] Password reset functionality
- [ ] OAuth integration (Google, GitHub)
- [ ] Role-based access control (RBAC)
- [ ] Rate limiting on auth endpoints
- [ ] Refresh token rotation
- [ ] Session management and revocation
- [ ] Two-factor authentication (2FA)

## Support

For issues or questions, create an issue at:
https://github.com/ncode3/sammo-fight-iq/issues
