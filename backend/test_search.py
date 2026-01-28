import asyncio
import sys
import os

# Add the current directory to sys.path so we can import from backend
sys.path.append(os.getcwd())

from engines.google import GoogleEngine
from engines.duckduckgo import DuckDuckGoEngine
from engines.wikipedia import WikipediaEngine
from search_orchestrator import SearchOrchestrator

async def test_google():
    print("Testing Google Engine...")
    engine = GoogleEngine()
    results = await engine.search("Python programming")
    print(f"Google Results: {len(results)}")
    for r in results[:2]:
        print(f" - {r.title}: {r.url}")

async def test_orchestrator():
    print("\nTesting Orchestrator...")
    orch = SearchOrchestrator()
    # Mock settings if needed, or rely on defaults being loaded
    results = await orch.search_all("AI Agents", ["AI Agents", "Autonomous Agents"])
    for engine, res in results.items():
        print(f"Engine: {engine}, Results: {len(res)}")

async def main():
    try:
        await test_google()
        await test_orchestrator()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting test...", flush=True)
    asyncio.run(main())
