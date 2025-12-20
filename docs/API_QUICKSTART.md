# SAMMO Fight IQ - API Quick Start Guide

## 🚀 Getting Started with the Authenticated API

This guide will get you up and running with the SAMMO Fight IQ API in 5 minutes.

## Prerequisites

- Python 3.9+
- Google Cloud Firestore credentials
- pip installed

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set your JWT secret key:

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
JWT_SECRET_KEY=<your-generated-key>
```

Set up Google Cloud credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

## Step 3: Start the API Server

```bash
# Development mode with auto-reload
uvicorn api_server:app --reload

# Or simply
python api_server.py
```

The server will start at `http://localhost:8000`

## Step 4: Explore the API

Open your browser and go to:

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Step 5: Test with Example Client

Run the example client to see it in action:

```bash
python examples/auth_client.py
```

This will:
1. ✅ Register a new user
2. ✅ Login and get token
3. ✅ Get user profile
4. ✅ Log boxing rounds
5. ✅ Get dashboard stats
6. ✅ View round history
7. ✅ Delete a round

## Quick API Reference

### 1. Register

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

Save the `access_token` from the response.

### 3. Log a Round (Protected)

```bash
curl -X POST http://localhost:8000/api/log_round \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "pressure_score": 8.0,
    "ring_control_score": 7.5,
    "defense_score": 6.0,
    "clean_shots_taken": 2,
    "notes": "Great session"
  }'
```

### 4. Get Stats (Protected)

```bash
curl -X GET http://localhost:8000/api/dashboard_stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. View History (Protected)

```bash
curl -X GET "http://localhost:8000/api/rounds_history?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Using the Interactive Docs

1. Go to `http://localhost:8000/docs`
2. Click the "Authorize" button (lock icon)
3. After registering and logging in via the endpoints, paste your token
4. Format: `your.jwt.token` (without "Bearer ")
5. Click "Authorize"
6. Now all protected endpoints will include your token automatically

## Python Client Usage

```python
from examples.auth_client import SammoClient

# Initialize client
client = SammoClient("http://localhost:8000")

# Register and login
client.register("fighter1", "fighter@example.com", "SecurePass123!", "Fighter One")
client.login("fighter1", "SecurePass123!")

# Log a round
round_data = client.log_round(
    pressure_score=8.0,
    ring_control_score=7.5,
    defense_score=6.0,
    clean_shots_taken=2,
    notes="Excellent sparring"
)

print(f"Danger Score: {round_data['danger_score']}")
print(f"Strategy: {round_data['strategy']['title']}")

# Get stats
stats = client.get_dashboard_stats()
print(f"Total Rounds: {stats['total_rounds']}")
print(f"Average Defense: {stats['averages']['defense_score']}")
```

## API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | ❌ No | Register new user |
| POST | `/auth/login` | ❌ No | Login and get token |
| GET | `/auth/me` | ✅ Yes | Get current user profile |
| POST | `/api/log_round` | ✅ Yes | Log a boxing round |
| GET | `/api/dashboard_stats` | ✅ Yes | Get aggregated stats |
| GET | `/api/rounds_history` | ✅ Yes | Get round history |
| DELETE | `/api/rounds/{id}` | ✅ Yes | Delete a specific round |
| GET | `/api/health` | ❌ No | Health check |

## Understanding the Response

### Login Response
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Round Logging Response
```json
{
  "status": "success",
  "id": "round-uuid",
  "danger_score": 0.52,
  "strategy": {
    "title": "RING_CUTTING",
    "text": "Smart pressure. Cut exits, feint to draw counters..."
  }
}
```

### Dashboard Stats Response
```json
{
  "averages": {
    "pressure_score": 7.5,
    "ring_control_score": 6.8,
    "defense_score": 5.2,
    "clean_shots_taken": 2.5
  },
  "most_recent_round_date": "2025-12-09T10:00:00",
  "next_game_plan": {
    "title": "RING_CUTTING",
    "text": "Smart pressure..."
  },
  "total_rounds": 15
}
```

## Error Handling

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```
**Solution:** Check your token, it may be expired or invalid. Login again.

### 403 Forbidden
```json
{
  "detail": "Not authorized to delete this round"
}
```
**Solution:** You can only access/modify your own data.

### 400 Bad Request
```json
{
  "detail": "Username 'fighter1' already exists"
}
```
**Solution:** Choose a different username.

## Security Best Practices

1. **Never commit your `.env` file** - It's already in `.gitignore`
2. **Use HTTPS in production** - JWT tokens should never be sent over plain HTTP
3. **Rotate your JWT secret** - Change it periodically
4. **Store tokens securely** - Don't store in localStorage, use httpOnly cookies in production
5. **Implement rate limiting** - Protect against brute force attacks

## Next Steps

- 📖 Read the full [AUTH_SETUP.md](./AUTH_SETUP.md) for detailed documentation
- 🧪 Run tests: `pytest tests/test_auth.py -v`
- 📝 Check [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- 🐛 Report issues: [GitHub Issues](https://github.com/ncode3/sammo-fight-iq/issues)

## Troubleshooting

### "Could not connect to Firestore"
- Check your Google Cloud credentials are set correctly
- Verify `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### "Module not found"
- Run `pip install -r requirements.txt`
- Make sure you're in the correct virtual environment

### "Port already in use"
- Change the port: `uvicorn api_server:app --port 8001`
- Or kill the process using port 8000

### "Token expired"
- Tokens expire after 30 minutes by default
- Login again to get a new token
- Implement refresh token flow for longer sessions

## Support

Need help? Check these resources:

- 📚 API Documentation: `http://localhost:8000/docs`
- 📖 Full Auth Guide: [AUTH_SETUP.md](./AUTH_SETUP.md)
- 🐛 Issues: [GitHub Issues](https://github.com/ncode3/sammo-fight-iq/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ncode3/sammo-fight-iq/discussions)

---

**Built with 💪 by the SAMMO Fight IQ Team**
