"""Wikidata SPARQL search engine integration."""
from typing import List
import httpx
from engines import BaseSearchEngine, SearchResult


class WikidataEngine(BaseSearchEngine):
    """Wikidata structured knowledge base using SPARQL queries."""
    
    def __init__(self):
        super().__init__("Wikidata")
        self.endpoint = "https://query.wikidata.org/sparql"
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search Wikidata using SPARQL."""
        try:
            # Generate SPARQL query for the search term
            sparql_query = self._generate_sparql(query, max_results)
            
            async with httpx.AsyncClient(timeout=8) as client:
                response = await client.get(
                    self.endpoint,
                    params={
                        'query': sparql_query,
                        'format': 'json'
                    },
                    headers={
                        'User-Agent': 'AiEngine/1.0 (http://localhost:8000; contact@localhost)'
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_results(data, query)
                else:
                    print(f"Wikidata returned status {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Wikidata search error: {e}")
            return []
    
    def _generate_sparql(self, query: str, limit: int) -> str:
        """Generate SPARQL query to find relevant entities."""
        # Simple full-text search query
        return f"""
        SELECT ?item ?itemLabel ?itemDescription WHERE {{
          SERVICE wikibase:mwapi {{
            bd:serviceParam wikibase:endpoint "www.wikidata.org";
                            wikibase:api "EntitySearch";
                            mwapi:search "{query}";
                            mwapi:language "en".
            ?item wikibase:apiOutputItem mwapi:item.
          }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        """
    
    def _parse_results(self, data: dict, query: str) -> List[SearchResult]:
        """Parse Wikidata SPARQL results."""
        results = []
        
        bindings = data.get('results', {}).get('bindings', [])
        
        for item in bindings:
            item_id = item.get('item', {}).get('value', '').split('/')[-1]
            label = item.get('itemLabel', {}).get('value', 'No label')
            description = item.get('itemDescription', {}).get('value', '')
            
            url = f"https://www.wikidata.org/wiki/{item_id}"
            
            results.append(self._create_result(
                title=label,
                snippet=description if description else f"Wikidata entity: {label}",
                url=url,
                metadata={
                    'entity_id': item_id,
                    'type': 'structured_data'
                }
            ))
        
        return results
