"""Wikipedia search engine integration."""
from typing import List
import httpx
import asyncio
from engines import BaseSearchEngine, SearchResult


class WikipediaEngine(BaseSearchEngine):
    """Wikipedia knowledge base search (Async API)."""
    
    def __init__(self):
        super().__init__("Wikipedia")
        self.api_url = "https://en.wikipedia.org/w/api.php"
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search Wikipedia using direct API."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                # 1. Search for titles
                search_params = {
                    "action": "opensearch",
                    "search": query,
                    "limit": max_results,
                    "namespace": 0,
                    "format": "json"
                }
                
                response = await client.get(
                    self.api_url, 
                    params=search_params,
                    headers={'User-Agent': 'AiEngine/1.0 (http://localhost:8000; contact@localhost)'}
                )
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                # opensearch returns [query, [titles], [descriptions], [urls]]
                if not data or len(data) < 4:
                    return []
                    
                titles = data[1]
                descriptions = data[2]
                urls = data[3]
                
                results = []
                for i in range(len(titles)):
                    results.append(self._create_result(
                        title=titles[i],
                        snippet=descriptions[i] if descriptions[i] else f"Wikipedia article for {titles[i]}",
                        url=urls[i],
                        metadata={'type': 'article'}
                    ))
                    
                print(f"[+] Wikipedia found {len(results)} results")
                return results
                
        except Exception as e:
            print(f"[-] Wikipedia search error: {e}")
            return []
