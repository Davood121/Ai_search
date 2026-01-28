"""Google search engine integration (Scraped)."""
from typing import List
import httpx
from bs4 import BeautifulSoup
from engines import BaseSearchEngine, SearchResult

class GoogleEngine(BaseSearchEngine):
    """Google search engine scraper."""
    
    def __init__(self):
        super().__init__("Google")
        self.base_url = "https://www.google.com/search"
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search Google."""
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9"
                }
                # 'num' parameter controls number of results
                params = {
                    "q": query,
                    "num": max_results + 2, # Request a few more to filter
                    "hl": "en"
                }
                
                cookies = {
                    "CONSENT": "YES+cb.20230531-11-p0.en+FX+119",
                    "SOCS": "CAECHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzEaAmVuIAEaBgiBo_CmBg"
                }
                
                response = await client.get(self.base_url, params=params, headers=headers, cookies=cookies)
                
                if response.status_code == 200:
                    return self._parse_results(response.text, max_results)
                elif response.status_code == 429:
                    print("[-] Google returned 429 (Rate Limit)")
                    return []
                else:
                    print(f"[-] Google returned {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"[-] Google search error: {e}")
            return []
    
    def _parse_results(self, html: str, max_results: int) -> List[SearchResult]:
        """Parse Google HTML results."""
        results = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # Debug: check for consent or captcha
            text_content = soup.get_text()
            if "Before you continue to Google" in text_content:
                print("[-] Google consent page detected")
            if "unusual traffic" in text_content:
                print("[-] Google captcha/traffic check detected")

            # Find result containers
            # Try multiple selectors
            elements = soup.select("div.g") or soup.select("div.tF2Cxc") or soup.select("div.Ee3tId")
            
            for g in elements[:max_results]:
                title_elem = g.select_one("h3")
                link_elem = g.select_one("a")
                snippet_elem = g.select_one("div.VwiC3b") or g.select_one("div.IsZvec") or g.select_one("div.aCOpRe")
                
                if title_elem and link_elem and link_elem.get("href"):
                    url = link_elem["href"]
                    if url.startswith("/"):
                        continue
                        
                    results.append(self._create_result(
                        title=title_elem.get_text(),
                        url=url,
                        snippet=snippet_elem.get_text() if snippet_elem else ""
                    ))
            
            print(f"[+] Google found {len(results)} results")
        except Exception as e:
            print(f"[-] Google parse error: {e}")
            
        return results
