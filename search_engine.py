# # import json

# # def load_data(filepath):
# #     with open(filepath, "r", encoding="utf-8") as f:
# #         return json.load(f)

# # # --- PHASE 3: BUILD ABBREVIATION MAP ---
# # def build_abbreviation_map(papers):
# #     """
# #     Creates a dictionary where keys are acronyms (e.g., 'POP') 
# #     and values are sets of full phrases (e.g., {'persistent organic pollutants'}).
# #     """
# #     abbr_map = {}
# #     for paper in papers:
# #         # We check both extracted phrases and the acronyms we found earlier
# #         for phrase in paper.get("important_phrases", []):
# #             words = phrase.split()
# #             if len(words) >= 2:
# #                 # Create acronym from first letters: 'machine learning' -> 'ML'
# #                 abbr = "".join([w[0] for w in words if w[0].isalpha()]).upper()
# #                 if len(abbr) > 1:
# #                     if abbr not in abbr_map:
# #                         abbr_map[abbr] = set()
# #                     abbr_map[abbr].add(phrase)
# #     return abbr_map

# # # --- PHASE 2: SIMPLE SEARCH ---
# # def search_papers(query, papers):
# #     """
# #     Finds papers where the query matches keywords or phrases.
# #     """
# #     query = query.lower()
# #     results = []
# #     for paper in papers:
# #         # Check if query matches keywords or any part of the important phrases
# #         in_keywords = query in paper.get("cleaned_keywords", [])
# #         in_phrases = any(query in phrase for phrase in paper.get("important_phrases", []))
        
# #         if in_keywords or in_phrases:
# #             results.append(paper)
    
# #     # --- PHASE 4: SORT RESULTS (Newest to Oldest) ---
# #     # arXiv URLs look like: http://arxiv.org/abs/2401.12345
# #     # Sorting by URL reverse alphabetical order puts higher numbers (newer dates) first.
# #     return sorted(results, key=lambda x: x["url"], reverse=True)

# # # --- PHASE 5: COMBINE EVERYTHING (The Loop) ---
# # def run_search_system():
# #     # 1. Load the data you cleaned in Step 3
# #     print("Loading knowledge base...")
# #     papers = load_data("after_cleaning_final_research_data.json")
# #     abbr_map = build_abbreviation_map(papers)
    
# #     print(f"\nSystem Ready! Indexed {len(papers)} papers and {len(abbr_map)} abbreviations.")
    
# #     while True:
# #         query = input("\nSearch (or 'exit'): ").strip()
# #         if query.lower() == 'exit':
# #             break
# #         if not query:
# #             continue

# #         # DISAMBIGUATION LOGIC
# #         search_term = query
# #         upper_query = query.upper()

# #         if upper_query in abbr_map:
# #             meanings = list(abbr_map[upper_query])
# #             if len(meanings) > 1:
# #                 print(f"\n'{upper_query}' has multiple meanings in this library:")
# #                 for i, m in enumerate(meanings, 1):
# #                     print(f"  {i}. {m}")
                
# #                 choice = input("Select number (or Enter to search original): ")
# #                 if choice.isdigit() and 0 < int(choice) <= len(meanings):
# #                     search_term = meanings[int(choice)-1]
# #             else:
# #                 # If only one meaning exists, we can suggest it
# #                 print(f"(Assuming you mean: {meanings[0]})")
# #                 search_term = meanings[0]

# #         # PERFORM SEARCH
# #         results = search_papers(search_term, papers)

# #         # DISPLAY RESULTS
# #         if results:
# #             print(f"\nFound {len(results)} papers for '{search_term}':")
# #             for i, p in enumerate(results[:5], 1): # Show top 5
# #                 print(f"\n[{i}] {p['title']}")
# #                 print(f"    URL: {p['url']}")
# #                 # Show only first 2 phrases to keep it clean
# #                 tags = ", ".join(p['important_phrases'][:3])
# #                 print(f"    Tags: {tags}...")
            
# #             if len(results) > 5:
# #                 print(f"\n... and {len(results)-5} more results.")
# #         else:
# #             print(f"No papers found for '{search_term}'.")

# # if __name__ == "__main__":
# #     run_search_system()



# import json
# import re

# def load_data(filepath):
#     try:
#         with open(filepath, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception as e:
#         print(f"Error loading file: {e}")
#         return []

# # 1. ACCURATE DATE EXTRACTOR 
# def extract_arxiv_id(url):
#     """
#     Extracts the numeric date ID from an arXiv URL (e.g., 2401.12345).
#     Higher numbers = Newer papers.
#     """
#     match = re.search(r'(\d{4}\.\d+)', url)
#     return float(match.group(1)) if match else 0.0

# # 2. REFINED ABBREVIATION MAP
# def build_abbreviation_map(papers):
#     raw_map = {}
#     phrase_counts = {}

#     for paper in papers:
#         for phrase in paper.get("important_phrases", []):
#             phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

#     for paper in papers:
#         for phrase in paper.get("important_phrases", []):
#             # Only count phrases seen at least twice
#             if phrase_counts[phrase] < 2:
#                 continue

#             words = phrase.split()
#             if len(words) >= 2:
#                 # Build acronym: 'Machine Learning' -> 'ML'
#                 abbr = "".join([w[0] for w in words if w[0].isalpha()]).upper()
#                 if len(abbr) > 1 and abbr not in {"THE", "AND", "THAT", "FOR"}:
#                     if abbr not in raw_map:
#                         raw_map[abbr] = set()
#                     raw_map[abbr].add(phrase)
    
#     # ONLY keep abbreviations that are truly ambiguous (have more than 1 meaning)
#     # This removes noise like 'GMC' if it only means one thing.
#     ambiguous_map = {k: v for k, v in raw_map.items() if len(v) > 1}
#     return ambiguous_map

# # 3. SCORING & SEARCH LOGIC 
# def search_papers(query, papers):
#     """
#     Finds papers and ranks them by relevance and date.
#     """
#     query = query.lower().strip()
#     results_with_scores = []
    
#     for paper in papers:
#         score = 0
#         keywords = [k.lower() for k in paper.get("cleaned_keywords", [])]
#         phrases = [p.lower() for p in paper.get("important_phrases", [])]

#         # SCORE 2: Match found in cleaned keywords (Strong match)
#         if any(query in k or k in query for k in keywords):
#             score += 2
        
#         # SCORE 1: Match found in phrases (Contextual match)
#         if any(query in p or p in query for p in phrases):
#             score += 1
            
#         if score > 0:
#             # Get the numeric ID for date sorting
#             paper_id = extract_arxiv_id(paper.get("url", ""))
#             results_with_scores.append({
#                 "score": score,
#                 "id": paper_id,
#                 "data": paper
#             })
    
#     # SORT: First by Score (Highest relevance), then by ID (Newest date)
#     sorted_results = sorted(
#         results_with_scores, 
#         key=lambda x: (x["score"], x["id"]), 
#         reverse=True
#     )
    
#     return [item["data"] for item in sorted_results]

# #  4. THE INTERACTIVE INTERFACE 
# def run_search_system():
#     papers = load_data("after_cleaning_final_research_data.json")
#     if not papers:
#         print("Data file not found. Please run your cleaning script first.")
#         return
    
#     abbr_map = build_abbreviation_map(papers)
#     print(f"\n--- AI Scientific Knowledge Engine Live ---")
#     print(f"Index: {len(papers)} papers | {len(abbr_map)} ambiguous acronyms managed.")

#     while True:
#         user_input = input("\nEnter search term (or 'exit'): ").strip()
#         if user_input.lower() == 'exit': break
#         if not user_input: continue

#         final_term = user_input
#         upper_input = user_input.upper()

#         # DISAMBIGUATION CHECK
#         if upper_input in abbr_map:
#             meanings = sorted(list(abbr_map[upper_input]))
#             print(f"\nDisambiguation required for '{upper_input}':")
#             for i, m in enumerate(meanings, 1):
#                 print(f"  {i}. {m}")
            
#             choice = input(f"Select 1-{len(meanings)} (or Enter to search all): ")
#             if choice.isdigit():
#                 idx = int(choice) - 1
#                 if 0 <= idx < len(meanings):
#                     final_term = meanings[idx]

#         print(f"--- Searching for: '{final_term}' ---")
#         results = search_papers(final_term, papers)

#         if results:
#             print(f"Found {len(results)} matches. Showing top results by relevance and date:\n")
#             for i, p in enumerate(results[:5], 1):
#                 print(f"[{i}] {p['title']}")
#                 print(f"    URL:  {p['url']}")
                
#                 matches = [t for t in p['important_phrases'] if final_term.lower() in t.lower()]
#                 if matches:
#                     print(f"    Tags: {', '.join(matches[:3])}")
            
#             if len(results) > 5:
#                 print(f"\n... plus {len(results)-5} more relevant papers.")
#         else:
#             print(f"No results found for '{final_term}'. Try a different keyword.")

# if __name__ == "__main__":
#     run_search_system()



# import json
# import re

# def load_data(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         return json.load(f)

# # --- 1. ABBREVIATION MAP (PHASE 3) ---
# def build_abbreviation_map(papers):
#     abbr_map = {}
#     for paper in papers:
#         for phrase in paper.get("important_phrases", []):
#             words = phrase.split()
#             if len(words) >= 2:
#                 # Create acronym: 'Polar Optical Phonons' -> 'POP'
#                 abbr = "".join([w[0] for w in words if w[0].isalpha()]).upper()
#                 if 1 < len(abbr) < 6:
#                     if abbr not in abbr_map:
#                         abbr_map[abbr] = set()
#                     abbr_map[abbr].add(phrase)
#     # We keep ALL abbreviations now, even if they only have 1 meaning
#     return abbr_map

# # --- 2. THE SMART SEARCH ENGINE (PHASE 2 & 4) ---
# def search_papers(query, papers):
#     """
#     State-Aware Search:
#     - Acronyms (POP): Exact match only.
#     - Phrases/Words: Flexible match.
#     """
#     is_acronym = query.isupper() and 1 < len(query) < 6
#     results_with_scores = []

#     for paper in papers:
#         score = 0
#         # Get data once
#         keywords = paper.get("cleaned_keywords", [])
#         phrases = paper.get("important_phrases", [])

#         if is_acronym:
#             # FIX: BLOCK SUBSTRING MATCH (No 'pop' in 'popular')
#             # Check for EXACT match in keywords or phrases
#             if query in keywords or query in phrases:
#                 score = 10  # Highest priority
#         else:
#             # FLEXIBLE SEARCH for words/phrases
#             query_low = query.lower()
#             is_phrase = len(query_low.split()) > 1
            
#             if is_phrase:
#                 if any(query_low in p.lower() for p in phrases):
#                     score = 5
#             else:
#                 if any(query_low in k.lower() for k in keywords):
#                     score = 3
#                 elif any(query_low in p.lower() for p in phrases):
#                     score = 1

#         if score > 0:
#             results_with_scores.append({"score": score, "data": paper})

#     # Sort by score (highest relevance first)
#     sorted_results = sorted(results_with_scores, key=lambda x: x["score"], reverse=True)
#     return [item["data"] for item in sorted_results]

# # --- 3. THE INTERACTIVE LOOP (PHASE 5) ---
# def run_search_system():
#     papers = load_data("after_cleaning_final_research_data.json")
#     abbr_map = build_abbreviation_map(papers)
#     print(f"--- Engine Ready: {len(papers)} papers, {len(abbr_map)} acronyms ---")

#     while True:
#         user_input = input("\nSearch: ").strip()
#         if user_input.lower() == 'exit': break
#         if not user_input: continue
        
#         # FIX: BLOCK ACCIDENTAL NUMBER SEARCH
#         if user_input.isdigit():
#             print("(!) Please enter a keyword, not just a number.")
#             continue

#         # DISAMBIGUATION LOGIC
#         final_term = user_input
#         upper_input = user_input.upper()

#         if upper_input in abbr_map:
#             meanings = sorted(list(abbr_map[upper_input]))
#             print(f"\n'{upper_input}' found. Select the correct context:")
#             for i, m in enumerate(meanings, 1):
#                 print(f"  {i}. {m}")
            
#             choice = input(f"Select 1-{len(meanings)} (or Enter for general search): ")
#             if choice.isdigit():
#                 idx = int(choice) - 1
#                 if 0 <= idx < len(meanings):
#                     # SUCCESS: final_term is now the full phrase
#                     final_term = meanings[idx]

#         # EXECUTION
#         print(f"Searching for: '{final_term}'...")
#         results = search_papers(final_term, papers)

#         if results:
#             print(f"Found {len(results)} results.")
#             for i, p in enumerate(results[:5], 1):
#                 print(f" [{i}] {p['title']} ({p['url']})")
#         else:
#             print("No results found.")

# if __name__ == "__main__":
#     run_search_system()


import json
import re

def load_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return []

# --- 1. ABBREVIATION MAP ---
def build_abbreviation_map(papers):
    abbr_map = {}
    for paper in papers:
        for phrase in paper.get("important_phrases", []):
            words = phrase.split()
            if len(words) >= 2:
                abbr = "".join([w[0] for w in words if w[0].isalpha()]).upper()
                if 1 < len(abbr) < 6:
                    if abbr not in abbr_map:
                        abbr_map[abbr] = set()
                    abbr_map[abbr].add(phrase)
    return abbr_map

# --- 2. HIERARCHICAL SEARCH ENGINE (The Final Fix) ---
def search_papers(query, papers):
    """
    Balanced Search:
    - Acronym (POP): Strict Exact Match (Score 20)
    - Exact Phrase Match: Highest priority (Score 15)
    - Partial Phrase Match: Medium priority (Score 10)
    - Word Fallback: Low priority (Score 1-3)
    """
    query_raw = query.strip()
    query_low = query_raw.lower()
    query_words = query_low.split()
    
    # Identify acronym (Must be uppercase, e.g., "POP")
    is_acronym = query_raw.isupper() and 1 < len(query_raw) < 6
    
    results_with_scores = []

    for paper in papers:
        score = 0
        keywords = [k.lower() for k in paper.get("cleaned_keywords", [])]
        phrases = [p.lower() for p in paper.get("important_phrases", [])]

        # MODE A: ACRONYM SEARCH (Strict)
        if is_acronym:
            # Look for exact match in important phrases or keywords
            if query_raw in paper.get("important_phrases", []) or query_raw in paper.get("cleaned_keywords", []):
                score = 20 

        # MODE B: TEXT SEARCH (The "Sweet Spot" Logic)
        else:
            # 1. EXACT PHRASE MATCH (Priority 1)
            # User typed: "context-aware reasoning" -> Paper has: "context-aware reasoning"
            if any(query_low == p for p in phrases):
                score = 15
            
            # 2. PARTIAL PHRASE MATCH (Priority 2)
            # User typed: "black hole" -> Paper has: "supermassive black hole"
            elif any(query_low in p for p in phrases):
                score = 10
            
            # 3. INDIVIDUAL WORD FALLBACK (Priority 3)
            # If no phrase matches, check if the words exist at all
            else:
                for word in query_words:
                    if word in keywords:
                        score += 3
                    elif any(word in p for p in phrases):
                        score += 1

        if score > 0:
            results_with_scores.append({"score": score, "data": paper})

    # SORTING: Highest Score first
    sorted_results = sorted(results_with_scores, key=lambda x: x["score"], reverse=True)
    return [item["data"] for item in sorted_results]

# --- 3. THE INTERACTIVE LOOP ---
def run_search_system():
    # Make sure this filename matches your cleaned data file
    filename = "after_cleaning_final_research_data.json"
    papers = load_data(filename)
    if not papers: return
    
    abbr_map = build_abbreviation_map(papers)
    print(f"--- Engine Ready: {len(papers)} papers indexed ---")

    while True:
        user_input = input("\nSearch: ").strip()
        if user_input.lower() == 'exit': break
        if not user_input: continue
        
        if user_input.isdigit():
            print("(!) Please enter a keyword, not just a number.")
            continue

        final_term = user_input
        upper_input = user_input.upper()

        # Handle Abbreviations
        if upper_input in abbr_map:
            meanings = sorted(list(abbr_map[upper_input]))
            print(f"\n'{upper_input}' found. Select context:")
            for i, m in enumerate(meanings, 1):
                print(f"  {i}. {m}")
            
            choice = input(f"Select 1-{len(meanings)} (or Enter for general search): ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(meanings):
                    final_term = meanings[idx]

        print(f"Searching for: '{final_term}'...")
        results = search_papers(final_term, papers)

        if results:
            print(f"Found {len(results)} matches.")
            # Show top 5
            for i, p in enumerate(results[:5], 1):
                print(f" [{i}] {p['title']}")
                print(f"     URL: {p['url']}")
        else:
            print("No results found.")

if __name__ == "__main__":
    run_search_system()