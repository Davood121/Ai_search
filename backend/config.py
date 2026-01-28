"""
Configuration Management for Nexus AI Search Engine

This module handles all application settings loaded from environment variables.
Settings are loaded from .env file if present, otherwise defaults are used.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings and configuration.
    
    All settings are loaded from environment variables with sensible defaults.
    Create a .env file in the backend directory to override defaults.
    """
    
    # Search Engine Configuration
    searxng_instance: str = "https://searx.work"
    """URL of the SearXNG instance to use for metasearch"""
    
    # Ollama LLM Configuration (Optional)
    ollama_host: str = "http://localhost:11434"
    """Ollama server address for AI query processing"""
    
    ollama_model: str = "llama3"
    """Ollama model to use for query synthesis"""
    
    # Server Configuration
    backend_port: int = 8000
    """Port for FastAPI backend server"""
    
    frontend_url: str = "http://localhost:3000"
    """Frontend URL for CORS configuration"""
    
    # Search Configuration
    search_timeout: int = 15
    """Timeout for individual search engine requests (seconds)"""
    
    max_results_per_engine: int = 10
    """Maximum results to fetch from each search engine"""
    
    max_total_results: int = 50
    """Maximum total results after deduplication"""
    
    # Logging Configuration
    log_level: str = "INFO"
    """Logging level (DEBUG, INFO, WARNING, ERROR)"""
    
    # Feature Flags
    enable_ollama: bool = True
    """Enable Ollama integration for AI processing"""
    
    enable_websocket: bool = True
    """Enable WebSocket for real-time updates"""
    
    class Config:
        """Pydantic configuration for Settings class."""
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = 'utf-8'


# Global settings instance
settings = Settings()


# Configure logging
def configure_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


# Initialize logging on import
configure_logging()

