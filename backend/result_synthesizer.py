"""
Result synthesizer - AI algorithm for filtering and fusing search results.
Creates a "super output" from multiple search engines.
"""
from typing import List, Dict, Any
from collections import defaultdict
import re
from difflib import SequenceMatcher
from engines import SearchResult


class ResultSynthesizer:
    """Synthesizes results from multiple engines into a unified output."""
    
    def __init__(self):
        self.url_dedup_cache = set()
    
    async def synthesize(
        self,
        query: str,
        raw_results: Dict[str, List[SearchResult]],
        max_results: int = 15
    ) -> Dict[str, Any]:
        """
        Main synthesis algorithm.
        
        Steps:
        1. Flatten and normalize results
        2. Deduplicate
        3. Score and rank
        4. Generate summary
        
        Args:
            query: Original search query
            raw_results: Dictionary of engine_name -> results
            max_results: Maximum results in final output
            
        Returns:
            Dictionary with results, summary, and stats
        """
        # Step 1: Flatten all results
        all_results = []
        for engine_name, results in raw_results.items():
            all_results.extend(results)
        
        print(f"Total raw results: {len(all_results)}")
        
        # Step 2: Deduplicate
        unique_results = self._deduplicate(all_results)
        print(f"After deduplication: {len(unique_results)}")
        
        # Step 3: Score and rank
        scored_results = self._score_results(query, unique_results, raw_results)
        ranked_results = sorted(scored_results, key=lambda x: x['final_score'], reverse=True)
        
        # Step 4: Take top results
        top_results = ranked_results[:max_results]
        
        # Step 5: Generate summary
        summary = self._generate_summary(query, top_results, raw_results)
        
        # Engine statistics
        engine_stats = {
            engine: len(results)
            for engine, results in raw_results.items()
        }
        
        return {
            'results': top_results,
            'summary': summary,
            'engine_stats': engine_stats,
            'total_raw': len(all_results),
            'total_unique': len(unique_results)
        }
    
    def _deduplicate(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate results based on URL and content similarity."""
        seen_urls = {}
        unique = []
        
        for result in results:
            # Normalize URL
            url = self._normalize_url(result.url)
            
            # Check exact URL match
            if url in seen_urls:
                # Keep the one from higher-priority source
                existing = seen_urls[url]
                if self._get_source_priority(result.source) > self._get_source_priority(existing.source):
                    # Replace with higher priority
                    unique.remove(existing)
                    unique.append(result)
                    seen_urls[url] = result
                continue
            
            # Check content similarity with existing results
            is_duplicate = False
            for existing in unique:
                if self._is_content_similar(result.snippet, existing.snippet):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(result)
                seen_urls[url] = result
        
        return unique
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for comparison."""
        # Remove protocol, www, trailing slashes, query params
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.rstrip('/')
        url = url.split('?')[0]  # Remove query params
        url = url.split('#')[0]  # Remove anchors
        return url.lower()
    
    def _is_content_similar(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Check if two text snippets are similar."""
        if not text1 or not text2:
            return False
        
        # Use sequence matcher for similarity
        ratio = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        return ratio > threshold
    
    def _get_source_priority(self, source: str) -> int:
        """Get priority score for a source (higher is better)."""
        priorities = {
            'Wikipedia': 5,
            'Wikidata': 4,
            'SearXNG': 3,
            'DuckDuckGo': 2,
            'Brave': 2
        }
        return priorities.get(source, 1)
    
    def _score_results(
        self,
        query: str,
        results: List[SearchResult],
        raw_results: Dict[str, List[SearchResult]]
    ) -> List[Dict[str, Any]]:
        """
        Score results based on multiple factors.
        
        Scoring factors:
        - Relevance to query (keyword matching)
        - Source authority (Wikipedia > general web)
        - Cross-engine consensus (appears in multiple engines)
        - Content quality (snippet length, clarity)
        """
        query_keywords = set(query.lower().split())
        scored = []
        
        for result in results:
            scores = {
                'relevance': self._calculate_relevance(result, query_keywords),
                'authority': self._get_source_priority(result.source) / 5.0,
                'consensus': self._calculate_consensus(result, raw_results),
                'quality': self._calculate_quality(result)
            }
            
            # Weighted final score
            final_score = (
                scores['relevance'] * 0.4 +
                scores['authority'] * 0.3 +
                scores['consensus'] * 0.2 +
                scores['quality'] * 0.1
            )
            
            scored.append({
                'title': result.title,
                'snippet': result.snippet,
                'url': result.url,
                'source': result.source,
                'scores': scores,
                'final_score': final_score
            })
        
        return scored
    
    def _calculate_relevance(self, result: SearchResult, query_keywords: set) -> float:
        """Calculate relevance score based on keyword matching."""
        text = (result.title + ' ' + result.snippet).lower()
        words = set(text.split())
        
        # Jaccard similarity
        intersection = query_keywords.intersection(words)
        union = query_keywords.union(words)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _calculate_consensus(
        self,
        result: SearchResult,
        raw_results: Dict[str, List[SearchResult]]
    ) -> float:
        """
        Calculate consensus score - how many engines found similar content.
        """
        url = self._normalize_url(result.url)
        count = 0
        
        for engine_results in raw_results.values():
            for r in engine_results:
                if self._normalize_url(r.url) == url:
                    count += 1
                    break
        
        # Normalize to 0-1 (max 5 engines)
        return min(count / 5.0, 1.0)
    
    def _calculate_quality(self, result: SearchResult) -> float:
        """Calculate content quality score."""
        # Simple heuristic based on snippet length and completeness
        snippet_len = len(result.snippet)
        
        if snippet_len == 0:
            return 0.0
        elif snippet_len < 50:
            return 0.3
        elif snippet_len < 150:
            return 0.7
        else:
            return 1.0
    
    def _generate_summary(
        self,
        query: str,
        results: List[Dict[str, Any]],
        raw_results: Dict[str, List[SearchResult]]
    ) -> str:
        """
        Generate a summary of findings.
        """
        if not results:
            return "No results found."
        
        total_sources = sum(len(r) for r in raw_results.values())
        unique_count = len(results)
        
        # Extract key sources
        top_sources = [r['source'] for r in results[:3]]
        sources_str = ', '.join(set(top_sources))
        
        summary = (
            f"Found {unique_count} relevant results from {total_sources} total sources. "
            f"Top information from: {sources_str}. "
        )
        
        # Add snippet from best result
        if results:
            best_snippet = results[0]['snippet'][:150]
            summary += f"Key finding: {best_snippet}..."
        
        return summary
