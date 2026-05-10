import time
import re
from typing import List, Dict, Optional
import streamlit as st

class SearchService:
    """
    Robust wrapper for the search engine with simulated async handling and retries.
    """
    
    def __init__(self, papers: List[Dict], abbr_map: Dict):
        self.papers = papers
        self.abbr_map = abbr_map

    @staticmethod
    def normalize(text: str) -> str:
        if text is None: return ""
        text = str(text).lower().strip()
        return re.sub(r's\b', '', text)
    @staticmethod
    def build_abbreviation_map(papers: List[Dict]) -> Dict:
        abbr_map = {}
        pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*\(([A-Z]{2,6})\)'
        for paper in papers:
            phrases = paper.get('important_phrases') or []
            content = f"{paper.get('title', '')} {' '.join(phrases)}"
            matches = re.findall(pattern, content)
            for full_form, short_form in matches:
                if short_form not in abbr_map:
                    abbr_map[short_form] = set()
                abbr_map[short_form].add(full_form)
        return abbr_map

    def search(self, query: str, expanded_terms: List[str] = None, retry_count: int = 3) -> List[Dict]:
        """
        Executes search with simulated latency and error handling.
        """
        if not query: return []
        
        for attempt in range(retry_count):
            try:
                # Simulated Backend Latency
                time.sleep(0.1) 
                
                query_norm = self.normalize(query)
                search_set = {query_norm}
                if expanded_terms:
                    for term in expanded_terms:
                        search_set.add(self.normalize(term))
                
                results_with_scores = []
                for paper in self.papers:
                    score = self._calculate_score(paper, search_set)
                    if score >= 10:
                        results_with_scores.append({"score": score, "data": paper})
                
                # Multi-level Sort: Score (DESC), Date (DESC)
                return sorted(
                    results_with_scores,
                    key=lambda x: (x["score"], x["data"].get("published", "")),
                    reverse=True
                )
            except Exception as e:
                if attempt == retry_count - 1:
                    st.error(f"Search Engine Error: {str(e)}")
                    return []
                time.sleep(0.5) # Wait before retry
        return []

    def _calculate_score(self, paper: Dict, search_set: set) -> int:
        score = 0
        title = self.normalize(paper.get("title", ""))
        phrases_raw = paper.get("important_phrases")
        phrases = [self.normalize(p) for p in phrases_raw] if isinstance(phrases_raw, list) else []
        
        keywords_raw = paper.get("cleaned_keywords")
        keywords = [self.normalize(k) for k in keywords_raw] if isinstance(keywords_raw, list) else []

        for q in search_set:
            if q == title: score += 60
            elif q in title: score += 30
            if any(q == k for k in keywords): score += 20
            if any(q == p for p in phrases): score += 15
            elif any(q in p for p in phrases): score += 5
        return score
