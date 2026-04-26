import json
import re


def load_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{filepath} not found.")
        return []


def normalize(text):
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s\-]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def build_abbreviation_map(papers):
    abbr_map = {}

    pattern = r"\b([A-Z][A-Za-z\s\-]+)\(([A-Z]{2,8})\)"

    for paper in papers:
        content = " ".join([
            paper.get("title", ""),
            paper.get("abstract", "")
        ])

        matches = re.findall(pattern, content)

        for full_form, short_form in matches:
            abbr_map.setdefault(short_form, set()).add(full_form.strip())

    return abbr_map


def score_paper(query_terms, paper):
    score = 0

    title = normalize(paper.get("title", ""))
    abstract = normalize(paper.get("abstract", ""))
    search_text = normalize(paper.get("search_text", ""))

    keywords = [
        normalize(x)
        for x in paper.get("cleaned_keywords", [])
    ]

    phrases = [
        normalize(x)
        for x in paper.get("important_phrases", [])
    ]

    authors = [
        normalize(x)
        for x in paper.get("authors", [])
    ]

    categories = [
        normalize(x)
        for x in paper.get("categories", [])
    ]

    for q in query_terms:
        if q == title:
            score += 100
        elif q in title:
            score += 50

        if q in abstract:
            score += 30

        if q in search_text:
            score += 25

        if any(q == k for k in keywords):
            score += 20

        if any(q in p for p in phrases):
            score += 15

        if any(q in a for a in authors):
            score += 15

        if any(q in c for c in categories):
            score += 10

    return score


def search_papers(query, papers, expanded_terms=None):
    query_terms = {normalize(query)}

    if expanded_terms:
        for term in expanded_terms:
            query_terms.add(normalize(term))

    results = []

    for paper in papers:
        score = score_paper(query_terms, paper)

        if score > 0:
            results.append({
                "score": score,
                "data": paper
            })

    results.sort(
        key=lambda x: (
            x["score"],
            x["data"].get("published", "")
        ),
        reverse=True
    )

    return results


def run_search_system():
    filename = "after_cleaning_final_research_data.json"

    papers = load_data(filename)

    if not papers:
        return

    abbr_map = build_abbreviation_map(papers)

    print(f"\nEngine Ready: {len(papers)} papers indexed")

    while True:
        user_input = input("\nSearch (or exit): ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        related_terms = []
        upper_input = user_input.upper()

        if upper_input in abbr_map:
            related_terms = list(abbr_map[upper_input])

        results = search_papers(
            user_input,
            papers,
            expanded_terms=related_terms
        )

        if not results:
            print("No results found.")
            continue

        print(f"\nFound {len(results)} results:\n")

        for i, item in enumerate(results[:10], 1):
            p = item["data"]

            print(f"[{i}] {p.get('title')}")
            print(f"Score: {item['score']}")
            print(f"Published: {p.get('published', '')[:10]}")
            print(f"Authors: {', '.join(p.get('authors', [])[:5])}")
            print(f"Categories: {', '.join(p.get('categories', [])[:5])}")
            print(f"URL: {p.get('url')}")
            print("-" * 80)


if __name__ == "__main__":
    run_search_system()