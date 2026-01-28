# Nexus AI Search Engine 🚀

A powerful **AI-powered multi-engine search system** that orchestrates parallel searches across 5 different search engines with intelligent result synthesis using AI.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-brightgreen?style=flat-square&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

## ✨ Features

- 🔍 **Multi-Engine Search** - Searches across 5 different engines simultaneously:
  - 🦆 DuckDuckGo
  - 🔎 Google
  - 🌐 SearXNG
  - 📚 Wikipedia
  - 🏷️ Wikidata

- 🤖 **AI-Powered Query Breakdown** - Analyzes user queries and generates focused sub-queries
- 💡 **Intelligent Result Synthesis** - Combines and ranks results across all engines
- ⚡ **Real-time WebSocket Support** - Live streaming of results
- 🎨 **Modern UI** - Beautiful, futuristic dark theme interface
- 🔓 **No API Keys Required** - All search engines work for free
- 🚀 **Fast & Async** - Built with FastAPI for high performance

## 📋 System Architecture

```
┌─────────────────────────────────────────────┐
│          Frontend (HTML/CSS/JS)             │
│     Beautiful UI with Real-time Updates     │
└────────────────┬────────────────────────────┘
                 │ WebSocket
┌────────────────▼────────────────────────────┐
│        FastAPI Backend Server               │
│  ┌──────────────────────────────────────┐   │
│  │  Query Processor (Intent Detection)  │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │ Search Orchestrator (Parallel)       │   │
│  │  ├─ DuckDuckGo Engine                │   │
│  │  ├─ Google Engine                    │   │
│  │  ├─ SearXNG Engine                   │   │
│  │  ├─ Wikipedia Engine                 │   │
│  │  └─ Wikidata Engine                  │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │ Result Synthesizer (AI Ranking)      │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Modern web browser

### Installation

#### Option 1: Automated Setup (Recommended)

```bash
# Windows
python start_app.py

# Linux/Mac
python3 start_app.py
```

This will automatically start both backend and frontend servers.

#### Option 2: Manual Setup

**Backend Setup:**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
python main.py
```

Backend runs on: **http://localhost:8000**

**Frontend Setup (in a new terminal):**

```bash
# Navigate to frontend directory
cd frontend

# Start HTTP server
python -m http.server 3000
```

Frontend runs on: **http://localhost:3000**

### 3. Open in Browser

Navigate to: **[http://localhost:3000](http://localhost:3000)**

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure as needed:

```bash
# Backend Configuration
SEARXNG_INSTANCE=https://searx.work
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# Server Settings
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000

# Search Settings
SEARCH_TIMEOUT=15
MAX_RESULTS_PER_ENGINE=10
```

### Search Engines - All FREE!

All 5 search engines work without any API keys or authentication:

1. **SearXNG** - Metasearch (246+ engines)
2. **DuckDuckGo** - Privacy-focused
3. **Qwant** - European privacy search
4. **Wikipedia** - Knowledge base
5. **Wikidata** - Structured data

**No configuration needed!** All engines are free forever with no rate limits.

### Optional: Ollama LLM Integration

For enhanced AI query breakdown and synthesis:

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3.2`
3. Make sure Ollama is running (it will auto-start)

The system will automatically detect and use Ollama if available.

---

## 📖 Usage Guide

### Search Examples

Try these queries to see the AI in action:

- **Simple factual**: "What is quantum computing?"
- **Complex analysis**: "Latest breakthroughs in fusion energy and their implications"
- **Technical**: "How does neural network backpropagation work?"
- **Current events**: "Climate change solutions 2026"

### Key Features

✅ **5 FREE Search Engines** - SearXNG, DuckDuckGo, Qwant, Wikipedia, Wikidata  
✅ **AI Query Breakdown** - Automatically generates focused sub-queries  
✅ **Parallel Search** - All engines search simultaneously  
✅ **Intelligent Synthesis** - Deduplicates and ranks results by relevance  
✅ **Real-time Updates** - Live progress for each engine  
✅ **Beautiful UI** - Modern, responsive dark theme interface  

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + K` | Focus search input |
| `Enter` | Search |
| `Escape` | Clear search and reset UI |

---

## 🏗️ Project Structure

```
Ai_search/
├── backend/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Configuration management
│   ├── query_processor.py           # AI query breakdown
│   ├── search_orchestrator.py       # Parallel search coordination
│   ├── result_synthesizer.py        # AI result ranking
│   ├── engines/
│   │   ├── brave.py
│   │   ├── duckduckgo.py
│   │   ├── google.py
│   │   ├── qwant.py
│   │   ├── searxng.py
│   │   ├── wikipedia.py
│   │   └── wikidata.py
│   └── requirements.txt
├── frontend/
│   ├── index.html                   # Main HTML
│   ├── styles.css                   # Beautiful UI styling
│   ├── script.js                    # Frontend logic
│   └── hologram.js                  # Visualization effects
├── start_app.py                     # One-command startup
├── README.md                        # This file
└── .env.example                     # Configuration template
```

---

## 🔧 Development

### Backend Structure

- **main.py** - FastAPI server with WebSocket support
- **query_processor.py** - Analyzes queries and generates sub-queries
- **search_orchestrator.py** - Manages parallel searches across all engines
- **result_synthesizer.py** - Ranks and deduplicates results
- **config.py** - Centralized configuration

### Frontend Structure

- **index.html** - Semantic HTML structure
- **styles.css** - CSS variables and responsive design
- **script.js** - Main frontend logic
- **hologram.js** - Real-time visualization

### API Endpoints

```
POST /search           - Execute a search
GET  /health          - Health check
WS   /ws/search       - WebSocket for live results
```

---

## 🚀 Performance

- **Concurrent Searches**: All 5 engines search in parallel
- **Average Response Time**: 3-8 seconds (depending on query complexity)
- **Result Deduplication**: Automatic removal of duplicate results
- **Smart Ranking**: Results ranked by relevance, authority, and consensus

---

## 📦 Dependencies

### Backend
- FastAPI - Modern web framework
- Uvicorn - ASGI server
- HTTPX - HTTP client
- Aiohttp - Async HTTP requests
- BeautifulSoup4 - HTML parsing
- SPARQLWrapper - Wikidata queries
- DuckDuckGo Search - DuckDuckGo API

### Frontend
- Vanilla HTML/CSS/JavaScript (no build tools needed!)
- CSS Grid & Flexbox for responsive design
- WebSocket API for real-time updates

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

To contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open-source and available under the MIT License - see the LICENSE file for details.

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -tulpn | grep 8000

# Kill process on port 8000 and try again
```

### Frontend can't connect to backend
- Ensure backend is running on http://localhost:8000
- Check browser console (F12) for CORS errors
- Verify both services are running

### Slow search results
- Check internet connection
- SearXNG instance might be overloaded, try another instance
- Increase SEARCH_TIMEOUT in .env

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ by Davood**

---

## Troubleshooting

### Backend won't start

**Error**: Module not found
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate

# Reinstall dependencies
pip install -r requirements.txt
```

### No results from SearXNG or Qwant

**Issue**: Public SearXNG instances may be slow or rate-limited

**Solution**: Try a different SearXNG instance in `.env`:
```
SEARXNG_INSTANCE=https://searx.fmac.xyz
# or
SEARXNG_INSTANCE=https://searx.tiekoetter.com
```

**Qwant Issue**: If Qwant API changes, other engines still provide results

### WebSocket connection failed

**Issue**: Frontend can't connect to backend

**Check**:
1. Backend is running on port 8000
2. No firewall blocking localhost connections
3. Browser console for specific errors (F12)

### Results are slow

**Normal**: First search takes 5-8 seconds (5 engines in parallel)
**If very slow**: Some engines may be timing out, check backend console logs

---

## API Documentation

Backend API docs: **http://localhost:8000/docs** (Swagger UI)

### Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /search` - Execute search (REST)
- `WS /ws/process` - Real-time search updates (WebSocket)

---

## System Requirements

- **Python**: 3.8+
- **Browser**: Modern browser with WebSocket support
- **RAM**: 500MB minimum
- **Internet**: Required for search engines

---

## Next Steps

### Enhancements You Can Add

1. **User Authentication**: Track search history
2. **Search History**: Save and revisit past searches
3. **Export Results**: Download as PDF or JSON
4. **Filter by Source**: Checkbox to include/exclude engines
5. **Advanced Settings**: Timeout, max results per engine
6. **Dark/Light Mode**: Theme switcher
7. **Voice Search**: Web Speech API integration

---

## Credits

**Search Engines Used** (All 100% Free):
- SearXNG (Privacy-focused metasearch - 246+ engines)
- DuckDuckGo (Privacy-first search)
- Qwant (European privacy search)
- Wikipedia (Knowledge base)
- Wikidata (Structured data)

**Built with**: FastAPI, Vanilla JavaScript, Canvas API, WebSockets
