"""
AI-powered query breakdown processor.
Analyzes user queries and generates focused sub-queries for targeted searches.
"""
import re
from typing import List
import asyncio


class QueryProcessor:
    """Breaks down complex queries into focused sub-queries."""
    
    def __init__(self):
        self.entity_patterns = {
            'person': r'\b(?:who|person|people|scientist|artist|leader)\b',
            'location': r'\b(?:where|place|city|country|location)\b',
            'time': r'\b(?:when|date|year|time|period|age|era)\b',
            'definition': r'\b(?:what is|define|meaning|definition)\b',
            'how': r'\b(?:how|process|method|way)\b',
            'why': r'\b(?:why|reason|cause|purpose)\b',
        }
    
    async def breakdown_query(self, query: str) -> List[str]:
        """
        Break down a query into focused sub-queries.
        
        Args:
            query: User's original search query
            
        Returns:
            List of 3-5 focused sub-queries
        """
        query_lower = query.lower()
        sub_queries = [query]  # Always include original
        
        # Detect query intent
        intent = self._detect_intent(query_lower)
        
        # Generate sub-queries based on intent
        keywords = self._extract_keywords(query)
        
        if intent == 'definition':
            # For "what is" queries
            main_term = self._extract_main_term(query)
            if main_term:
                sub_queries.append(f"{main_term} definition")
                sub_queries.append(f"{main_term} explanation")
                sub_queries.append(f"{main_term} examples")
        
        elif intent == 'how':
            # For "how to" queries
            sub_queries.append(f"{query} tutorial")
            sub_queries.append(f"{query} guide")
            sub_queries.append(f"{query} step by step")
        
        elif intent == 'factual':
            # For factual queries (who, when, where)
            if keywords:
                sub_queries.append(" ".join(keywords[:3]))
                sub_queries.append(f"{keywords[0]} facts")
        
        else:
            # General complex queries
            if len(keywords) > 2:
                # Split into concept combinations
                sub_queries.append(" ".join(keywords[:2]))
                sub_queries.append(" ".join(keywords[-2:]))
                
                # Add specific aspects
                for kw in keywords[:3]:
                    sub_queries.append(f"{kw} overview")
        
        # Remove duplicates and limit
        unique_queries = []
        seen = set()
        for q in sub_queries:
            q_normalized = q.lower().strip()
            if q_normalized not in seen and len(unique_queries) < 5:
                unique_queries.append(q)
                seen.add(q_normalized)
        
        return unique_queries[:5]
    
    def _detect_intent(self, query: str) -> str:
        """Detect the intent of the query."""
        for intent, pattern in self.entity_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return intent
        return 'general'
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query."""
        # Remove common stop words
        stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'what', 'which', 'who', 'when', 'where', 'why', 'how',
            'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'from', 'about', 'can', 'could', 'should', 'would'
        }
        
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _extract_main_term(self, query: str) -> str:
        """Extract the main term from 'what is X' queries."""
        patterns = [
            r'what is (?:a |an |the )?(.+?)(?:\?|$)',
            r'define (.+?)(?:\?|$)',
            r'explain (.+?)(?:\?|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""


# For Ollama integration (optional enhancement)
class OllamaQueryProcessor(QueryProcessor):
    """Enhanced query processor using local Ollama LLM."""
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        super().__init__()
        self.ollama_host = ollama_host
        self.use_ollama = self._check_ollama_available()
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            import httpx
            response = httpx.get(f"{self.ollama_host}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    async def breakdown_query(self, query: str) -> List[str]:
        """
        Use Ollama LLM for intelligent query breakdown if available,
        otherwise fall back to algorithmic approach.
        """
        if not self.use_ollama:
            return await super().breakdown_query(query)
        
        try:
            import httpx
            
            prompt = f"""Given this search query, generate 4 focused sub-queries that would help gather comprehensive information.
Each sub-query should target a specific aspect of the main query.

Query: {query}

Respond with only the sub-queries, one per line, no numbering or explanation."""

            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.post(
                    f"{self.ollama_host}/api/generate",
                    json={
                        "model": "llama3.2",
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    sub_queries = [query]  # Include original
                    
                    # Parse LLM response
                    lines = result.get("response", "").strip().split("\n")
                    for line in lines:
                        cleaned = line.strip().lstrip("0123456789.-) ")
                        if cleaned and len(sub_queries) < 5:
                            sub_queries.append(cleaned)
                    
                    return sub_queries[:5]
        
        except Exception as e:
            print(f"Ollama query breakdown failed, using fallback: {e}")
        
        # Fallback to algorithmic approach
        return await super().breakdown_query(query)
