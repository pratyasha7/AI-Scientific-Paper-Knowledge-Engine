import json
import re

def load_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return []
#  ABBREVIATION MAP 
def build_abbreviation_map(papers):
    abbr_map = {}
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
# SEARCH ENGINE (Multi-Level Sort)
def search_papers(query, papers, expanded_terms=None):
    query_norm = normalize(query)
    search_set = {query_norm}
    if expanded_terms:
        for term in expanded_terms:
            search_set.add(normalize(term))
    results_with_scores = []

    for paper in papers:
        score = 0
        title = normalize(paper.get("title", ""))
        phrases = [normalize(p) for p in paper.get("important_phrases", [])]
        keywords = [normalize(k) for k in paper.get("cleaned_keywords", [])]

        for q in search_set:
            if q == title: score += 60
            elif q in title: score += 30
            if any(q == k for k in keywords): score += 20
            if any(q == p for p in phrases): score += 15
            elif any(q in p for p in phrases): score += 5
        
        if score >= 10: 
            results_with_scores.append({"score": score, "data": paper})    
    sorted_results = sorted(
        results_with_scores, 
        key=lambda x: (x["score"], x["data"].get("published", "")), 
        reverse=True
    )   
    return sorted_results
def run_search_system():
    filename = "after_cleaning_final_research_data.json"
    papers = load_data(filename)
    if not papers: return    
    abbr_map = build_abbreviation_map(papers)
    print(f"--- Engine Ready: {len(papers)} papers indexed ---")

    while True:
        user_input = input("\nSearch (or 'exit'): ").strip()
        if user_input.lower() == 'exit': break
        if not user_input: continue
        search_term = user_input
        related_terms = []
        upper_input = user_input.upper()
        
        if upper_input in abbr_map:
            options = sorted(list(abbr_map[upper_input]))
            print(f"\n'{upper_input}' found. Choose context:")
            
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            print(f"  {len(options)+1}. General search")
            choice = input(f"Select 1-{len(options)+1}: ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    search_term = options[idx]
                    related_terms = [upper_input]
                else:
                    related_terms = options
        print(f"Searching for: '{search_term}'...")
        results = search_papers(search_term, papers, expanded_terms=related_terms)

        if results:
            print(f"Found {len(results)} relevant results (Latest first within score groups):")
            for i, res in enumerate(results[:5], 1):
                p = res['data']    
                date_str = p.get('published', 'Unknown Date')[:10]
                print(f" [{i}] {p['title']}")
                print(f"     Score: {res['score']} | Published: {date_str}")
                print(f"     URL: {p.get('url', 'N/A')}")
        else:
            print("No high-relevance matches found.")

if __name__ == "__main__":
    run_search_system()
