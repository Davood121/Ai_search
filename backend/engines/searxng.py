"""SearXNG metasearch engine integration."""
from typing import List
import httpx
from engines import BaseSearchEngine, SearchResult


import random

class SearXNGEngine(BaseSearchEngine):
    """SearXNG metasearch engine (aggregates 246+ engines)."""
    
    INSTANCES = [
        "https://searx.work",
        "https://search.ononoki.org",
        "https://searx.be",
        "https://searx.aicamp.cn",
        "https://searx.thegpm.org",
        "https://search.mdosch.de",
        "https://opensearch.vnet.solutions"
    ]
    
    def __init__(self, instance_url: str = None):
        super().__init__("SearXNG")
        self.instance_url = instance_url or self.INSTANCES[0]
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using SearXNG instance (with rotation)."""
        # Try up to 3 instances
        for _ in range(3):
            instance = random.choice(self.INSTANCES)
            print(f"[*] SearXNG trying instance: {instance}")
            
            try:
                async with httpx.AsyncClient(timeout=8) as client:
                    response = await client.get(
                        f"{instance}/search",
                        params={
                            'q': query,
                            'format': 'json',
                            'pageno': 1
                        },
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                            'Accept': 'application/json'
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        results = self._parse_results(data, max_results)
                        if results:
                            print(f"[+] SearXNG found {len(results)} results on {instance}")
                            return results
                    else:
                        print(f"[-] SearXNG {instance} returned status {response.status_code}")
                        
            except Exception as e:
                print(f"[-] SearXNG {instance} error: {e}")
        
        return []
    
    def _parse_results(self, data: dict, max_results: int) -> List[SearchResult]:
        """Parse SearXNG JSON response."""
        results = []
        
        for item in data.get('results', [])[:max_results]:
            results.append(self._create_result(
                title=item.get('title', 'No title'),
                snippet=item.get('content', ''),
                url=item.get('url', ''),
                metadata={
                    'engine': item.get('engine', 'unknown'),
                    'category': item.get('category', '')
                }
            ))
        
        return results
