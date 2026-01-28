"""
Search orchestrator - manages parallel searches across all engines.
"""
import asyncio
from typing import List, Dict, Any, AsyncGenerator, Tuple
from engines import SearchResult
from engines.duckduckgo import DuckDuckGoEngine
from engines.searxng import SearXNGEngine
from engines.google import GoogleEngine
from engines.wikipedia import WikipediaEngine
from engines.wikidata import WikidataEngine
from config import settings


class SearchOrchestrator:
    """Orchestrates parallel searches across 5 search engines."""
    
    def __init__(self):
        # Initialize all 5 search engines
        self.engines = {
            'SearXNG': SearXNGEngine(settings.searxng_instance),
            'DuckDuckGo': DuckDuckGoEngine(),
            'Google': GoogleEngine(),
            'Wikipedia': WikipediaEngine(),
            'Wikidata': WikidataEngine()
        }
    
    async def search_all(
        self,
        query: str,
        sub_queries: List[str],
        timeout: int = settings.search_timeout
    ) -> Dict[str, List[SearchResult]]:
        """
        Execute parallel searches across all engines.
        
        Args:
            query: Main query
            sub_queries: List of sub-queries (will distribute across engines)
            timeout: Timeout in seconds
            
        Returns:
            Dictionary mapping engine names to result lists
        """
        tasks = []
        
        # Create search tasks for each engine
        for engine_name, engine in self.engines.items():
            # Use different sub-queries for diversity
            query_idx = len(tasks) % len(sub_queries)
            search_query = sub_queries[query_idx]
            
            tasks.append(
                self._search_with_timeout(
                    engine_name,
                    engine,
                    search_query,
                    timeout
                )
            )
        
        # Execute all searches in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results by engine
        engine_results = {}
        for engine_name, result in zip(self.engines.keys(), results):
            if isinstance(result, Exception):
                print(f"[-] {engine_name} failed: {result}")
                engine_results[engine_name] = []
            else:
                engine_results[engine_name] = result
        
        return engine_results
    
    async def search_all_streaming(
        self,
        query: str,
        sub_queries: List[str]
    ) -> AsyncGenerator[Tuple[str, List[SearchResult]], None]:
        """
        Stream results as each engine completes.
        Useful for real-time UI updates.
        """
        tasks = {}
        
        # Create tasks
        for engine_name, engine in self.engines.items():
            query_idx = len(tasks) % len(sub_queries)
            search_query = sub_queries[query_idx]
            
            task = asyncio.create_task(
                self._search_with_timeout(engine_name, engine, search_query, 8)
            )
            tasks[task] = engine_name
        
        # Yield results as they complete
        while tasks:
            done, pending = await asyncio.wait(
                tasks.keys(),
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for task in done:
                engine_name = tasks.pop(task)
                try:
                    results = await task
                    yield engine_name, results
                except Exception as e:
                    print(f"{engine_name} streaming error: {e}")
                    yield engine_name, []
    
    async def _search_with_timeout(
        self,
        engine_name: str,
        engine: Any,
        query: str,
        timeout: int
    ) -> List[SearchResult]:
        """Execute a search with timeout."""
        try:
            return await asyncio.wait_for(
                engine.search(query, max_results=settings.max_results_per_engine),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            print(f"[-] {engine_name} timed out after {timeout}s")
            return []
        except Exception as e:
            print(f"[-] {engine_name} error: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
