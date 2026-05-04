import json
import re
import spacy
from collections import Counter

try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("Run:")
    print("python -m spacy download en_core_web_lg")
    exit()


ACADEMIC_NOISE = {
    "study", "paper", "approach", "result",
    "author", "provide", "show", "discuss",
    "propose", "work", "method"
}

WEAK_WORDS = {
    "high", "low", "strong", "weak",
    "general", "main", "major", "specific",
    "possible", "different"
}

COMMON_CAPS_NOISE = {
    "USA", "ALL", "THE", "AND", "FOR"
}


def clean_text(text):
    text = re.sub(r"\$.*?\$", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def process_doc(doc):
    cleaned_keywords = []
    important_phrases = []

    for token in doc:
        if token.pos_ in ("NOUN", "PROPN", "ADJ"):
            if token.is_stop or token.is_punct or token.is_space:
                continue

            word = re.sub(r"[^a-zA-Z]", "", token.lemma_.lower())

            if len(word) <= 2:
                continue

            if word in ACADEMIC_NOISE:
                continue

            if word in WEAK_WORDS:
                continue

            cleaned_keywords.append(word)

    for chunk in doc.noun_chunks:
        phrase = chunk.text.lower().strip()
        phrase = re.sub(r"[^a-z\s\-]", "", phrase)

        words = phrase.split()

        filtered = [
            w for w in words
            if w not in nlp.Defaults.stop_words
            and w not in ACADEMIC_NOISE
            and w not in WEAK_WORDS
        ]

        if len(filtered) >= 2:
            important_phrases.append(" ".join(filtered))

    acronyms = [
        token.text
        for token in doc
        if token.text.isupper()
        and token.text.isalpha()
        and 1 < len(token.text) < 8
        and token.text not in COMMON_CAPS_NOISE
    ]

    important_phrases.extend(acronyms)

    cleaned_keywords = list(dict.fromkeys(cleaned_keywords))
    important_phrases = list(dict.fromkeys(important_phrases))

    return cleaned_keywords, important_phrases


def run_pipeline(
    input_file="arxiv_data.json",
    output_file="after_cleaning_final_research_data.json"
):
    print(f"Reading {input_file}...")

    with open(input_file, "r", encoding="utf-8") as f:
        papers = json.load(f)

    texts = []

    for p in papers:
        txt = " ".join([
            p.get("title", ""),
            p.get("abstract", ""),
            " ".join(p.get("categories", [])),
            p.get("comment", "")
        ])

        texts.append(clean_text(txt))

    print(f"Processing {len(texts)} papers...")

    docs = list(nlp.pipe(texts, batch_size=32))

    all_concepts = []

    for paper, doc in zip(papers, docs):
        keywords, phrases = process_doc(doc)

        paper["cleaned_keywords"] = keywords
        paper["important_phrases"] = phrases

        paper["search_text"] = " ".join([
            paper.get("title", ""),
            paper.get("abstract", ""),
            " ".join(keywords),
            " ".join(phrases),
            " ".join(paper.get("authors", [])),
            " ".join(paper.get("categories", []))
        ])

        all_concepts.extend(phrases)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            papers,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nSaved → {output_file}")

    print("\nTop concepts:")
    for concept, count in Counter(all_concepts).most_common(20):
        print(f"{concept} : {count}")


if __name__ == "__main__":
    run_pipeline()