# import json
# import re
# import spacy
# from collections import Counter

# # Load SpaCy model
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     print("SpaCy model not found. Run: python -m spacy download en_core_web_sm")
#     exit()

# def process_scientific_text(text):
#     # 1. PRE-CLEANING: Remove LaTeX math and leading fragments
#     text = re.sub(r'\$.*?\$', '', text)
    
#     doc = nlp(text)

#     # 2. DEFINE FILTERS
#     academic_noise = {
#         "revisit", "result", "find", "give", "determine", "completely", "choice", 
#         "live", "example", "assign", "case", "hand", "number", "various", 
#         "study", "paper", "approach", "provide", "show", "discuss", "conclusion", 
#         "author", "present", "propose", "work", "base", "new", "describe", 
#         "different", "furthermore", "step-wise", "identify"
#     }
    
#     weak_words = {
#          "original", "new", "general", "different","consistent", "possible", "various", "particular",
#          "nearby", "unique", "previous"
#     }

#     corrections = {"datum": "data", "physic": "physics", "ai": "AI"}

#     # --- STEP A: CLEANED KEYWORDS (Unigrams) ---
#     cleaned_keywords = []
#     for token in doc:
#         if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
#             if not token.is_stop and not token.is_punct and not token.is_space:
#                 word = re.sub(r'[^a-zA-Z]', '', token.lemma_.lower())
#                 word = corrections.get(word, word)
                
#                 # FIX 1: Filter out academic noise AND weak words
#                 if len(word) > 2 and word not in academic_noise and word not in weak_words:
#                     cleaned_keywords.append(word)

#     # --- STEP B: IMPORTANT PHRASES ---
#     important_phrases = []
#     for chunk in doc.noun_chunks:
#         phrase_raw = chunk.text.lower().strip().replace('\n', ' ')
        
#         # Keep letters and hyphens, but clean up the rest
#         phrase_clean = re.sub(r'[^a-z\s\-]', '', phrase_raw).strip()
        
#         # FIX 2: Remove leading single-letter prefixes (k , d , x )
#         # This fixes "k real-world" -> "real-world" or "d gauged" -> "gauged"
#         phrase_clean = re.sub(r'^[a-z]\s+', '', phrase_clean)
        
#         # FIX 3: Remove trailing or leading hyphens (fixes "low- plasma")
#         phrase_clean = phrase_clean.strip('-').strip()

#         words = phrase_clean.split()
        
#         # FILTERING LOGIC
#         if len(phrase_clean) > 5: # FIX 4: Phrase must be a decent length
#             # Filter words in the phrase
#             filtered_words = [
#                 w for w in words 
#                 if w not in nlp.Defaults.stop_words 
#                 and w not in academic_noise 
#                 and w not in weak_words
#             ]

#             if len(filtered_words) >= 2:
#                 # Ensure the phrase doesn't start with a messy fragment
#                 final_phrase = " ".join(filtered_words)
                
#                 # Final check: Don't allow phrases starting with messy fragments
#                 bad_prefixes = ("k-", "d-", "x-", "low-", "multi-")
#                 if not final_phrase.startswith(bad_prefixes):
#                     final_phrase = final_phrase.replace("datum", "data")
#                     important_phrases.append(final_phrase)

#     # --- STEP C: ACRONYMS ---
#     acronyms = [
#         token.text for token in doc
#         if token.text.isupper() 
#         and 1 < len(token.text) < 6 # Restored to 1 < len to keep AI, ML, GR
#         and token.is_alpha
#     ]
#     important_phrases.extend(acronyms)

#     return list(set(cleaned_keywords)), list(set(important_phrases))

# def run_pipeline(input_file, output_file):
#     print(f"Reading {input_file}...")
#     try:
#         with open(input_file, "r", encoding="utf-8") as f:
#             papers = json.load(f)
#     except FileNotFoundError:
#         print("Error: Input file not found.")
#         return

#     print(f"Processing {len(papers)} papers with advanced structural filtering...")
    
#     all_summary = []
#     for paper in papers:
#         abstract = paper.get("abstract", "")
#         keywords, phrases = process_scientific_text(abstract)
#         paper["cleaned_keywords"] = keywords
#         paper["important_phrases"] = phrases
#         all_summary.extend(phrases)

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(papers, f, indent=4)
    
#     # Final check of the top results
#     print("\n--- CLEANED TOP CONCEPTS ---")
#     for concept, count in Counter(all_summary).most_common(15):
#         print(f"{concept.upper()}: {count}")

# if __name__ == "__main__":
#     run_pipeline("arxiv_data.json", "after_cleaning_final_research_data.json")

# Final code *********************************************************************************

import json
import re
import spacy
from collections import Counter

# Load SpaCy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model not found. Run: python -m spacy download en_core_web_sm")
    exit()

def process_scientific_text(text):
    # 1. PRE-CLEANING: Remove LaTeX math
    text = re.sub(r'\$.*?\$', '', text)
    
    doc = nlp(text)

    # 2. DEFINE FILTERS
    academic_noise = {
        "revisit", "result", "find", "give", "determine", "completely", "choice", 
        "live", "example", "assign", "case", "hand", "number", "various", 
        "study", "paper", "approach", "provide", "show", "discuss", "conclusion", 
        "author", "present", "propose", "work", "base", "new", "describe", 
        "different", "furthermore", "step-wise", "identify"
    }
    
    weak_words = {
        "high", "low", "strong", "weak", "general", "current", "simple", "likely", "main", "major", "specific",  "original", "new", "different","consistent", "possible", "various", "particular", "nearby", "unique", "previous"
    }

    # FIX 1: Negative Acronym Filter (exclude non-scientific all-caps words)
    common_caps_noise = {
        "USA", "ALL", "SOME", "THE", "AND", "FOR", "ITS", "NEW", "ONE", "TWO"
    }

    corrections = {"datum": "data", "physic": "physics", "ai": "AI"}

    # --- STEP A: CLEANED KEYWORDS (Unigrams) ---
    cleaned_keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            if not token.is_stop and not token.is_punct and not token.is_space:
                word = re.sub(r'[^a-zA-Z]', '', token.lemma_.lower())
                word = corrections.get(word, word)
                
                if len(word) > 2 and word not in academic_noise and word not in weak_words:
                    cleaned_keywords.append(word)

    # --- STEP B: IMPORTANT PHRASES ---
    important_phrases = []
    for chunk in doc.noun_chunks:
        phrase_raw = chunk.text.lower().strip().replace('\n', ' ')
        phrase_clean = re.sub(r'[^a-z\s\-]', '', phrase_raw).strip()
        
        # Remove leading single-letter prefixes (k , d , x )
        phrase_clean = re.sub(r'^[a-z]\s+', '', phrase_clean)
        phrase_clean = phrase_clean.strip('-').strip()

        words = phrase_clean.split()
        
        if len(phrase_clean) > 5:
            filtered_words = [
                w for w in words 
                if w not in nlp.Defaults.stop_words 
                and w not in academic_noise 
                and w not in weak_words
            ]

            if len(filtered_words) >= 2:
                final_phrase = " ".join(filtered_words)
                bad_prefixes = ("k-", "d-", "x-", "low-", "multi-")
                if not final_phrase.startswith(bad_prefixes):
                    final_phrase = final_phrase.replace("datum", "data")
                    important_phrases.append(final_phrase)

    # --- STEP C: ACRONYM UPGRADE ---
    # FIX 2: Added 'token.text not in common_caps_noise'
    acronyms = [
        token.text for token in doc
        if token.text.isupper() 
        and 1 < len(token.text) < 6 
        and token.is_alpha
        and token.text not in common_caps_noise
    ]
    important_phrases.extend(acronyms)

    # --- STEP D: ORDER PRESERVATION ---
    # FIX 3: Using dict.fromkeys() instead of set()
    # This removes duplicates but keeps the words in the order they appeared!
    unique_keywords = list(dict.fromkeys(cleaned_keywords))
    unique_phrases = list(dict.fromkeys(important_phrases))

    return unique_keywords, unique_phrases

def run_pipeline(input_file, output_file):
    print(f"Reading {input_file}...")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            papers = json.load(f)
    except FileNotFoundError:
        print("Error: Input file not found.")
        return

    print(f"Processing {len(papers)} papers with order-preservation and noise-reduction...")
    
    all_summary = []
    for paper in papers:
        abstract = paper.get("abstract", "")
        keywords, phrases = process_scientific_text(abstract)
        paper["cleaned_keywords"] = keywords
        paper["important_phrases"] = phrases
        all_summary.extend(phrases)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=4)
    
    print(f"\nSUCCESS! High-fidelity data saved to {output_file}")
    
    print("\n--- TOP DISCOVERED CONCEPTS (Cleaned) ---")
    for concept, count in Counter(all_summary).most_common(10):
        print(f"{concept.upper()}: {count}")

if __name__ == "__main__":
    run_pipeline("arxiv_data.json", "after_cleaning_final_research_data.json")