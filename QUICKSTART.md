# Quick Start Reference

## 🚀 One-Command Startup

```bash
python start_app.py
```

Then open: **http://localhost:3000**

## 📍 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web UI |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API Redoc | http://localhost:8000/redoc | ReDoc UI |

## 🔧 Manual Startup

### Backend
```bash
cd backend
python -m venv venv
# Activate venv (Windows: .\venv\Scripts\activate OR macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python main.py
```

### Frontend (New Terminal)
```bash
cd frontend
python -m http.server 3000
```

## ⚙️ Configuration

Copy and edit `backend/.env.example` to `backend/.env`:

```ini
SEARXNG_INSTANCE=https://searx.work
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
SEARCH_TIMEOUT=15
MAX_RESULTS_PER_ENGINE=10
```

## 🔍 Search Features

- **5 Free Search Engines**
  - SearXNG (metasearch)
  - DuckDuckGo (privacy)
  - Qwant (European)
  - Wikipedia (knowledge)
  - Wikidata (structured data)

- **AI Powered**
  - Automatic query breakdown
  - Intelligent result synthesis
  - Smart deduplication
  - Real-time WebSocket updates

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl/Cmd + K` | Focus search |
| `Enter` | Search |
| `Escape` | Clear |

## 🛠️ Development

```bash
# Install dev tools
pip install pytest pytest-asyncio black flake8

# Format code
black backend/

# Lint
flake8 backend/

# Test
cd backend && pytest
```

## 📦 Deploy to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/Davood121/Ai_search.git
git push -u origin main
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port in use | Kill process on port or change .env |
| Import error | Activate virtual environment |
| No results | Check internet, try different SearXNG |
| WebSocket error | Check both servers running |

## 📚 Documentation

- **README.md** - Project overview and features
- **INSTALL.md** - Detailed installation guide
- **CONTRIBUTING.md** - How to contribute
- **IMPROVEMENTS.md** - Changes made
- **.env.example** - Configuration template

## 🎯 Key Endpoints

### Search Endpoint
```bash
POST /search
Content-Type: application/json

{
  "query": "your search query",
  "max_results": 15
}
```

### WebSocket Endpoint
```
WS /ws/process
```

### Health Check
```bash
GET /health
```

## 🚢 Production Ready

✅ Docker support (add Dockerfile)
✅ Environment variables
✅ Error handling
✅ Logging configured
✅ CORS enabled
✅ Static file serving

## 📊 Performance

- **Concurrent searches** across 5 engines
- **Average response time**: 3-8 seconds
- **No API keys required**
- **Unlimited requests** (rate limited by SearXNG)

## 📞 Support

- 📖 GitHub: https://github.com/Davood121/Ai_search
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

Happy searching! 🎉
