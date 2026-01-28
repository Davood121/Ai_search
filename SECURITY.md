# Security Guide

## Authentication Overview

The Nexus AI Search API uses **JWT (JSON Web Token)** authentication for secure access to protected endpoints. This prevents unauthorized access to your search API.

## How Authentication Works

### 1. **Login to Get Token** (First Time)

Send your API key to the `/login` endpoint to get a JWT token:

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "nexus-ai-search-default-key-change-in-production"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 2. **Use Token for Requests** (Every Search)

Include the token in the `Authorization` header for protected endpoints:

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{"query": "artificial intelligence"}'
```

**Python Example:**

```python
import requests

# 1. Get token
login_response = requests.post(
    "http://localhost:8000/login",
    json={"api_key": "nexus-ai-search-default-key-change-in-production"}
)
token = login_response.json()["access_token"]

# 2. Use token for search
search_response = requests.post(
    "http://localhost:8000/search",
    headers={"Authorization": f"Bearer {token}"},
    json={"query": "machine learning"}
)
results = search_response.json()
```

## Configuration

### Environment Variables

Edit `.env` in the `backend/` directory:

```env
# Security Configuration
SECRET_KEY=your-secret-key-change-in-production-change-me!
API_KEY=nexus-ai-search-default-key-change-in-production!
```

### Change Default API Key (Production)

1. Open `backend/.env`
2. Change `API_KEY` to a strong, unique key:
   ```env
   API_KEY=my-super-secure-key-12345!
   ```
3. Restart the backend:
   ```bash
   nexus-search
   # or
   python backend/main.py
   ```

### Change Secret Key (Production)

For production deployments, generate a new secret key:

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then update `.env`:
```env
SECRET_KEY=<paste-generated-key-here>
```

## Token Expiration

- **Token Lifetime:** 60 minutes
- **Action:** Get a new token by calling `/login` again when token expires
- **Error:** 401 Unauthorized means your token expired

## Protected Endpoints

The following endpoints require authentication:

- `POST /search` - Search across all engines
- `POST /search/specialized` - Specialized searches (News, Images, etc.)

## Unprotected Endpoints

These endpoints are publicly accessible (no token needed):

- `POST /login` - Obtain JWT token
- `GET /status` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `GET /redoc` - ReDoc documentation

## API Documentation with Authentication

### Swagger UI (http://localhost:8000/docs)

1. Click the **"Authorize"** button (top right)
2. Enter your JWT token (without "Bearer" prefix)
3. Click **"Authorize"**
4. Try endpoints from the UI

### Example Flow in Swagger:

```
1. Call POST /login with your API key
2. Copy the "access_token" from response
3. Click Authorize button
4. Paste token in "Value" field
5. Click Authorize
6. Now test /search endpoint
```

## Error Responses

### Invalid API Key
```json
{
  "detail": "Invalid API key"
}
```
**Solution:** Check API_KEY in .env matches what you're sending

### Invalid or Expired Token
```json
{
  "detail": "Invalid or expired token"
}
```
**Solution:** Call `/login` again to get a new token

### Missing Token
```json
{
  "detail": "Not authenticated"
}
```
**Solution:** Include Authorization header with Bearer token

## Best Practices

✅ **DO:**
- Change API_KEY and SECRET_KEY in production
- Use HTTPS in production (set up reverse proxy)
- Keep tokens private and never commit .env to version control
- Regenerate tokens periodically
- Store API keys securely (use environment variables)

❌ **DON'T:**
- Use default API key in production
- Expose API keys in client-side code
- Commit .env file to Git
- Share tokens via email or unencrypted channels
- Use HTTP in production (always use HTTPS)

## Troubleshooting

### "Invalid API key" error
- Check that API_KEY in `.env` matches what you're sending
- Make sure you're sending the API key, not the JWT token

### "Invalid or expired token" error
- Get a fresh token by calling `/login` again
- Token expires after 60 minutes of inactivity

### Can't access /docs
- The API documentation endpoint is public, no authentication needed
- Try accessing http://localhost:8000/docs directly in browser

## Environment Setup

### First Run

```bash
cd backend
cp .env.example .env  # Copy example config
# Edit .env and change SECRET_KEY and API_KEY if desired
pip install -r requirements.txt  # Install security libraries
nexus-search  # Start the application
```

### Using the API

```bash
# Terminal 1: Start the backend
nexus-search

# Terminal 2: Get a token
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "nexus-ai-search-default-key-change-in-production"}'

# Terminal 2: Search with token
curl -X POST "http://localhost:8000/search" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "python fastapi"}'
```

## Support

For security issues or questions, please refer to the main README.md or open an issue on GitHub.
