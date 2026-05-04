# ***********************************************************Final code *****************************************************

import re
import spacy
from collections import Counter
from mongodb_config import get_cleaned_collection, get_raw_collection

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model not found. Run: python -m spacy download en_core_web_sm")
    exit()

def process_scientific_text(text):    
    text = re.sub(r'\$.*?\$', '', text)  # LaTeX     
    doc = nlp(text)
    #  FILTERS
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
    #  Negative Acronym Filter
    common_caps_noise = {
        "USA", "ALL", "SOME", "THE", "AND", "FOR", "ITS", "NEW", "ONE", "TWO"
    }
    corrections = {"datum": "data", "physic": "physics", "ai": "AI"}
    # CLEANED KEYWORDS (Unigrams) 
    cleaned_keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            if not token.is_stop and not token.is_punct and not token.is_space:
                word = re.sub(r'[^a-zA-Z]', '', token.lemma_.lower())
                word = corrections.get(word, word)
                
                if len(word) > 2 and word not in academic_noise and word not in weak_words:
                    cleaned_keywords.append(word)
    # IMPORTANT PHRASES
    important_phrases = []
    for chunk in doc.noun_chunks:
        phrase_raw = chunk.text.lower().strip().replace('\n', ' ')
        phrase_clean = re.sub(r'[^a-z\s\-]', '', phrase_raw).strip()
        
        # Removal of leading single-letter prefixes (k , d , x )
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

    acronyms = [
        token.text for token in doc
        if token.text.isupper() 
        and 1 < len(token.text) < 6 
        and token.is_alpha
        and token.text not in common_caps_noise
    ]
    important_phrases.extend(acronyms)
    unique_keywords = list(dict.fromkeys(cleaned_keywords))
    unique_phrases = list(dict.fromkeys(important_phrases))
    return unique_keywords, unique_phrases

def run_pipeline(input_file, output_file):
    print(f"Reading {input_file}...")
    raw_collection = get_raw_collection()
    papers = list(raw_collection.find({}, {"_id": 0}))
    if not papers:
        print("Error: No input data found in MongoDB.")
        return
    print(f"Processing {len(papers)} papers with order-preservation and noise-reduction...")
    
    all_summary = []
    for paper in papers:
        abstract = paper.get("abstract", "")
        keywords, phrases = process_scientific_text(abstract)
        paper["cleaned_keywords"] = keywords
        paper["important_phrases"] = phrases
        all_summary.extend(phrases)

    cleaned_collection = get_cleaned_collection()
    cleaned_collection.delete_many({})
    if papers:
        cleaned_collection.insert_many(papers)
    
    print(f"\nSUCCESS! High-fidelity data saved to MongoDB")
    
    print("\n--- TOP DISCOVERED CONCEPTS (Cleaned) ---")
    for concept, count in Counter(all_summary).most_common(10):
        print(f"{concept.upper()}: {count}")

if __name__ == "__main__":
    run_pipeline("arxiv_data.json", "after_cleaning_final_research_data.json")
