# Installation Guide

This guide will walk you through setting up Nexus AI Search Engine on your system.

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended for optimal performance)
- **Disk Space:** 500MB for dependencies
- **Internet:** Required for search engines
- **OS:** Windows, macOS, or Linux

## Quick Installation (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Davood121/Ai_search.git
cd Ai_search
```

### 2. Run the Application

```bash
# Windows
python start_app.py

# macOS/Linux
python3 start_app.py
```

That's it! The application will:
- ✅ Check for available ports
- ✅ Start the backend server (http://localhost:8000)
- ✅ Start the frontend server (http://localhost:3000)
- ✅ Display connection information

## Manual Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/Davood121/Ai_search.git
cd Ai_search
```

### Step 2: Setup Backend

#### On Windows:

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Start backend
python main.py
```

#### On macOS/Linux:

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Start backend
python3 main.py
```

Backend will be available at: **http://localhost:8000**

### Step 3: Setup Frontend (New Terminal)

#### On Windows:

```bash
cd frontend
python -m http.server 3000
```

#### On macOS/Linux:

```bash
cd frontend
python3 -m http.server 3000
```

Frontend will be available at: **http://localhost:3000**

## Configuration

### Setting up .env File

1. Copy the template:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. Edit `backend/.env`:
   ```ini
   # Search Engine
   SEARXNG_INSTANCE=https://searx.work
   
   # Optional: Ollama integration
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3
   
   # Server
   BACKEND_PORT=8000
   FRONTEND_URL=http://localhost:3000
   
   # Search Settings
   SEARCH_TIMEOUT=15
   MAX_RESULTS_PER_ENGINE=10
   ```

### Optional: Enable Ollama AI Integration

For enhanced AI query processing:

1. **Download Ollama:** https://ollama.ai

2. **Install Ollama** for your OS

3. **Pull a model:**
   ```bash
   ollama pull llama3
   ```

4. **Ollama will auto-start** when you run the application

The system automatically detects Ollama if available.

## Testing Installation

### Verify Backend

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-28T12:34:56.789123"
}
```

### Check API Documentation

Visit: **http://localhost:8000/docs**

This shows the interactive Swagger UI with all available endpoints.

## Troubleshooting

### Issue: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process on port 8000
netstat -tulpn | grep 8000

# Kill the process (replace PID with actual process ID)
kill -9 PID
```

### Issue: Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
.\venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: WebSocket Connection Failed

**Error:** `WebSocket connection failed`

**Solution:**
- Ensure both backend and frontend are running
- Check that ports 8000 and 3000 are available
- Verify CORS is properly configured
- Check browser console (F12) for specific errors

### Issue: Slow Search Results

**Cause:** Network or instance overload

**Solution:**
- Check internet connection
- Try a different SearXNG instance in `.env`
- Increase `SEARCH_TIMEOUT` value
- Reduce `MAX_RESULTS_PER_ENGINE`

### Issue: Python Version Error

**Error:** `Python 3.8+ required`

**Solution:**
```bash
# Check Python version
python --version

# If not 3.8+, install newer version
# Download from https://www.python.org/downloads/
```

## Virtual Environment Troubleshooting

### Deactivate Virtual Environment

```bash
# Windows
.\venv\Scripts\deactivate

# macOS/Linux
deactivate
```

### Delete & Recreate Virtual Environment

```bash
# Windows
rmdir /s venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development Setup

If you want to contribute to the project:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black backend/

# Lint code
flake8 backend/
```

## Getting Help

- 📖 **Documentation:** Check [README.md](README.md)
- 🐛 **Issues:** GitHub Issues
- 💬 **Discussions:** GitHub Discussions
- 📧 **Email:** Contact the maintainers

## Next Steps

1. **Explore the UI** at http://localhost:3000
2. **Check API Docs** at http://localhost:8000/docs
3. **Read** [README.md](README.md) for features
4. **Contribute** by checking [CONTRIBUTING.md](CONTRIBUTING.md)

---

Happy searching! 🚀
