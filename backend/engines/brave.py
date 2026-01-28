"""Brave Search API integration."""
from typing import List, Optional
import httpx
from engines import BaseSearchEngine, SearchResult


class BraveEngine(BaseSearchEngine):
    """Brave Search API (privacy-focused, independent index)."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("Brave")
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using Brave Search API."""
        if not self.api_key:
            print("Brave API key not configured, skipping")
            return []
        
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        'q': query,
                        'count': min(max_results, 20)
                    },
                    headers={
                        'Accept': 'application/json',
                        'Accept-Encoding': 'gzip',
                        'X-Subscription-Token': self.api_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_results(data, max_results)
                else:
                    print(f"Brave API returned status {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Brave search error: {e}")
            return []
    
    def _parse_results(self, data: dict, max_results: int) -> List[SearchResult]:
        """Parse Brave API response."""
        results = []
        
        web_results = data.get('web', {}).get('results', [])
        
        for item in web_results[:max_results]:
            results.append(self._create_result(
                title=item.get('title', 'No title'),
                snippet=item.get('description', ''),
                url=item.get('url', ''),
                metadata={
                    'age': item.get('age', ''),
                    'language': item.get('language', '')
                }
            ))
        
        return results
