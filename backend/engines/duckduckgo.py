"""DuckDuckGo search engine integration."""
from typing import List
import asyncio
from engines import BaseSearchEngine, SearchResult


class DuckDuckGoEngine(BaseSearchEngine):
    """DuckDuckGo search engine using duckduckgo_search library."""
    
    def __init__(self):
        super().__init__("DuckDuckGo")
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using DuckDuckGo."""
        try:
            from ddgs import DDGS
            
            # Run in thread pool since DDGS is synchronous
            print(f"[*] Starting DuckDuckGo search for: {query}")
            results = await asyncio.to_thread(self._sync_search, query, max_results)
            print(f"[+] DuckDuckGo found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"[-] DuckDuckGo search error: {e}")
            return []
    
    def _sync_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Synchronous search implementation."""
        from ddgs import DDGS
        
        results = []
        
        try:
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                
                for item in search_results:
                    if len(results) >= max_results:
                        break
                    
                    results.append(self._create_result(
                        title=item.get('title', 'No title'),
                        snippet=item.get('body', ''),
                        url=item.get('href', ''),
                        timestamp=item.get('date', '')
                    ))
        
        except Exception as e:
            print(f"DuckDuckGo sync search error: {e}")
        
        return results
