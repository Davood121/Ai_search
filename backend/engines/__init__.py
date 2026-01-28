"""Base search engine interface."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Standardized search result format."""
    title: str
    snippet: str
    url: str
    source: str  # Engine name
    score: float = 0.0
    timestamp: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseSearchEngine(ABC):
    """Abstract base class for all search engines."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        Execute a search query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of SearchResult objects
        """
        pass
    
    def _create_result(self, **kwargs) -> SearchResult:
        """Helper to create standardized result."""
        return SearchResult(
            source=self.name,
            **kwargs
        )
