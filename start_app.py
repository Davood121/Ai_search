"""
Nexus AI Search Engine - Application Starter
Runs both backend and frontend servers in parallel.
"""
import multiprocessing
import uvicorn
import os
import sys
import time
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser


def check_port_available(port: int) -> bool:
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
        return True
    except OSError:
        return False


def run_backend():
    """Start FastAPI backend server."""
    print("\n" + "="*60)
    print("Starting Backend Server...")
    print("="*60)
    
    # Change into backend dir for imports
    os.chdir('backend')
    sys.path.insert(0, os.getcwd())
    
    try:
        from main import app
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Backend failed to start: {e}")
        import traceback
        traceback.print_exc()


def run_frontend():
    """Start Frontend HTTP server."""
    print("\n" + "="*60)
    print("Starting Frontend Server...")
    print("="*60)
    
    os.chdir('frontend')
    
    class CORSRequestHandler(SimpleHTTPRequestHandler):
        """HTTP Request handler with CORS support."""
        
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            return super().end_headers()
        
        def log_message(self, format, *args):
            """Suppress default logging."""
            pass

    try:
        httpd = HTTPServer(('0.0.0.0', 3000), CORSRequestHandler)
        print("✅ Frontend listening on http://localhost:3000")
        httpd.serve_forever()
    except OSError as e:
        print(f"❌ Frontend failed to start: {e}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "🚀 NEXUS AI SEARCH ENGINE LAUNCHER" + " "*14 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check ports
    if not check_port_available(8000):
        print("⚠️  Port 8000 is already in use. Please free it and try again.")
        sys.exit(1)
    
    if not check_port_available(3000):
        print("⚠️  Port 3000 is already in use. Please free it and try again.")
        sys.exit(1)
    
    # Create and start processes
    backend_process = multiprocessing.Process(target=run_backend, daemon=True)
    frontend_process = multiprocessing.Process(target=run_frontend, daemon=True)
    
    backend_process.start()
    frontend_process.start()
    
    # Give servers time to start
    time.sleep(3)
    
    # Print startup info
    print("\n" + "="*60)
    print("✅ ALL SERVERS STARTED SUCCESSFULLY")
    print("="*60)
    print("\n📍 Access the application:")
    print("   Frontend:  http://localhost:3000")
    print("   Backend:   http://localhost:8000")
    print("   API Docs:  http://localhost:8000/docs")
    print("\n⚙️  Engines:")
    print("   • SearXNG")
    print("   • DuckDuckGo")
    print("   • Qwant")
    print("   • Wikipedia")
    print("   • Wikidata")
    print("\n💡 Tip: Press Ctrl+C to stop all servers")
    print("="*60 + "\n")
    
    try:
        # Keep processes running
        backend_process.join()
    except KeyboardInterrupt:
        print("\n\n⛔ Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join(timeout=5)
        frontend_process.join(timeout=5)
        print("✅ All servers stopped. Goodbye!")

