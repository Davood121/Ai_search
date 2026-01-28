"""Qwant search engine integration - European privacy-focused search."""
from typing import List
import httpx
from engines import BaseSearchEngine, SearchResult


class QwantEngine(BaseSearchEngine):
    """Qwant search engine - Free, privacy-focused, no API key needed."""
    
    def __init__(self):
        super().__init__("Qwant")
        self.base_url = "https://api.qwant.com/v3/search/web"
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using Qwant API (completely free, no auth needed)."""
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        'q': query,
                        'count': max_results,
                        't': 'web',
                        'locale': 'en_US',
                        'safesearch': '1'
                    },
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Referer': 'https://www.qwant.com/',
                        'Origin': 'https://www.qwant.com'
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = self._parse_results(data, max_results)
                    print(f"[+] Qwant found {len(results)} results")
                    return results
                else:
                    print(f"[-] Qwant returned status {response.status_code}: {response.text}")
                    return []
                    
        except Exception as e:
            print(f"[-] Qwant search error: {e}")
            return []
    
    def _parse_results(self, data: dict, max_results: int) -> List[SearchResult]:
        """Parse Qwant API response."""
        results = []
        
        try:
            items = data.get('data', {}).get('result', {}).get('items', [])
            
            for item in items[:max_results]:
                results.append(self._create_result(
                    title=item.get('title', 'No title'),
                    snippet=item.get('desc', ''),
                    url=item.get('url', ''),
                    metadata={
                        'source': item.get('source', ''),
                        'favicon': item.get('favicon', '')
                    }
                ))
        except Exception as e:
            print(f"Qwant parse error: {e}")
        
        return results
