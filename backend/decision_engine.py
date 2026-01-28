"""
AI Decision Engine.
Responsible for high-level reasoning, planning, and self-reflection.
"""
from typing import List, Dict, Any
import httpx
import json
from config import settings

class DecisionEngine:
    """The 'Brain' of the AI agent."""
    
    def __init__(self):
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        
    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze the user's query to determine intent and strategy.
        Returns a plan JSON.
        """
        prompt = f"""Query: "{query}"
Classify intent: FACTUAL, TUTORIAL, OPINION, CREATIVE.
Real-time data needed? YES/NO.
Strategy: SHORT REASONING.

JSON:
{{
    "intent": "...",
    "needs_realtime_data": true/false,
    "complexity": "low/medium/high",
    "reasoning": "..."
}}"""
        return await self._call_llm_json(prompt, fast=True)

    async def evaluate_results(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Critique the search results to decide if they are sufficient.
        """
        # Create a compact representation of results for the LLM
        context = ""
        for i, r in enumerate(results[:5]):
            context += f"[{i+1}] {r.get('title')}: {r.get('snippet')[:150]}...\n"
            
        prompt = f"""I am answering the query: "{query}"
        
I have found these search results:
{context}

Evaluate if these results are sufficient to answer the query accurately and comprehensively.
Respond in JSON:
{{
    "sufficient": true/false,
    "missing_info": "What key information is missing (if any)?",
    "suggested_action": "answer|search_more",
    "refinement_query": "Better search query if needed (or null)"
}}"""
        return await self._call_llm_json(prompt)

    async def _call_llm_json(self, prompt: str, fast: bool = False) -> Dict[str, Any]:
        """Helper to call Ollama and parse JSON response."""
        try:
            options = {
                "num_predict": 100 if fast else 200,
                "temperature": 0.1,
                "num_ctx": 1024
            }
            
            async with httpx.AsyncClient(timeout=10 if fast else 20) as client:
                response = await client.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt + "\n\nRespond ONLY with valid JSON.",
                        "format": "json",
                        "stream": False,
                        "options": options
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data.get("response", "{}")
                    try:
                        return json.loads(text)
                    except:
                        print(f"[-] Failed to parse JSON from LLM: {text}")
                        return {}
                else:
                    print(f"[-] Ollama error: {response.status_code}")
                    return {}
        except Exception as e:
            print(f"[-] Decision Engine error: {e}")
            return {}
