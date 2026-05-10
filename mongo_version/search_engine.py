import re
import spacy
from mongodb_config import get_cleaned_collection

try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Error: SpaCy model 'en_core_web_md' not found. Run: python -m spacy download en_core_web_md")

def load_data():
    papers = list(get_cleaned_collection().find({}, {"_id": 0}))
    if not papers:
        print("Error: No data found in MongoDB collection.")
        return []
    return papers

# ABBREVIATION MAP
def build_abbreviation_map(papers):
    abbr_map = {}
    # Pattern: Look for 'Phrase (ABBR)' standard research definitions
    pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*\(([A-Z]{2,6})\)'
    for paper in papers:
        content = f"{paper.get('title', '')} {' '.join(paper.get('important_phrases', []))}"
        matches = re.findall(pattern, content)
        for full_form, short_form in matches:
            if short_form not in abbr_map:
                abbr_map[short_form] = set()
            abbr_map[short_form].add(full_form)
    return abbr_map

# NORMALIZATION
def normalize(text):
    if not text: return ""
    text = text.lower().strip()
    return re.sub(r's\b', '', text)

# SEMANTIC SCORING
def get_semantic_score(query_doc, text):
    if not text: return 0
    target_doc = nlp(text)
    if not query_doc.vector_norm or not target_doc.vector_norm:
        return 0
    return query_doc.similarity(target_doc)

# SEARCH ENGINE (Lexical + Semantic + Recency)
def search_papers(query, papers, expanded_terms=None):
    query_doc = nlp(query)
    query_norm = normalize(query)
    
    search_set = {query_norm}
    if expanded_terms:
        for term in expanded_terms:
            search_set.add(normalize(term))           
    results_with_scores = []

    for paper in papers:
        lexical_score = 0
        title_raw = paper.get("title", "")
        title_norm = normalize(title_raw)
        phrases = [normalize(p) for p in paper.get("important_phrases", [])]
        keywords = [normalize(k) for k in paper.get("cleaned_keywords", [])]

        # LEXICAL SCORING 
        for q in search_set:
            if q == title_norm: lexical_score += 60
            elif q in title_norm: lexical_score += 30
            if any(q == k for k in keywords): lexical_score += 20
            if any(q == p for p in phrases): lexical_score += 15
            elif any(q in p for p in phrases): lexical_score += 5        
        # SEMANTIC SCORING 
        semantic_sim = get_semantic_score(query_doc, title_raw)
        semantic_score = 0
        if semantic_sim > 0.7:
            semantic_score = semantic_sim * 40

        total_score = lexical_score + semantic_score

        if total_score >= 15: 
            results_with_scores.append({
                "score": round(total_score, 2), 
                "lex_part": lexical_score,
                "sem_part": round(semantic_score, 2),
                "data": paper
            })    

    # MULTI-LEVEL SORT 
    sorted_results = sorted(
        results_with_scores, 
        key=lambda x: (x["score"], x["data"].get("published", "")), 
        reverse=True
    )   
    return sorted_results

def run_search_system():
    papers = load_data()
    if not papers: return    
    abbr_map = build_abbreviation_map(papers)
    print(f"--- Engine Ready: {len(papers)} papers indexed with Semantic Proximity ---")

    while True:
        user_input = input("\nSearch (or 'exit'): ").strip()
        if user_input.lower() == 'exit': break
        if not user_input: continue

        search_term = user_input
        related_terms = []
        upper_input = user_input.upper()
        if upper_input in abbr_map:
            options = sorted(list(abbr_map[upper_input]))
            print(f"\n'{upper_input}' identified as an abbreviation. Contexts:")
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            print(f"  {len(options)+1}. General search for '{user_input}'")
            choice = input(f"Select 1-{len(options)+1}: ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    search_term = options[idx]
                    related_terms = [upper_input]
                else:
                    related_terms = options

        print(f"Analyzing semantics for: '{search_term}'...")
        results = search_papers(search_term, papers, expanded_terms=related_terms)

        if results:
            print(f"Found {len(results)} matches (Latest first within score groups):")
            for i, res in enumerate(results[:5], 1):
                p = res['data']    
                date_str = p.get('published', 'Unknown Date')[:10]
                print(f" [{i}] {p['title']}")
                print(f"     Relevance: {res['score']} (Lex: {res['lex_part']}, Sem: {res['sem_part']}) | Date: {date_str}")
                print(f"     URL: {p.get('url', 'N/A')}")
        else:
            print("No high-relevance matches found.")

if __name__ == "__main__":
    run_search_system()