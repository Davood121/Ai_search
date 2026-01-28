import httpx
import asyncio

instances = [
    "https://searx.be",
    "https://searx.work",
    "https://search.ononoki.org",
    "https://searx.aicamp.cn",
    "https://searx.thegpm.org",
    "https://search.mdosch.de",
    "https://opensearch.vnet.solutions",
    "https://searx.webheberg.info"
]

async def check_instance(url):
    print(f"Checking {url}...")
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{url}/search", params={"q": "test", "format": "json"})
            if resp.status_code == 200:
                print(f"[SUCCESS] {url}")
                return url
            else:
                print(f"[FAIL] {url} status {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
    return None

async def main():
    tasks = [check_instance(url) for url in instances]
    results = await asyncio.gather(*tasks)
    working = [u for u in results if u]
    print("\nWorking instances:")
    for w in working:
        print(w)

if __name__ == "__main__":
    asyncio.run(main())
