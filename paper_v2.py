import requests
import xml.etree.ElementTree as ET
import time
import json

BASE_URL = "https://export.arxiv.org/api/query"


def fetch_arxiv_abstracts(total_records=5000):
    query = 'all:"machine learning" OR all:physics OR cat:cs.AI'

    papers = []
    seen_ids = set()

    chunk_size = 100
    retries = 5

    print(f"Starting download of {total_records} papers...")

    for start in range(0, total_records, chunk_size):
        params = {
            "search_query": query,
            "start": start,
            "max_results": chunk_size,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        headers = {
            "User-Agent": "ScientificPaperEngine/1.0"
        }

        response = None

        for attempt in range(retries):
            try:
                response = requests.get(
                    BASE_URL,
                    params=params,
                    headers=headers,
                    timeout=60
                )

                if response.status_code == 200:
                    break

                print(
                    f"HTTP {response.status_code} "
                    f"(retry {attempt+1}/{retries})"
                )

            except Exception as e:
                print(
                    f"Network error: {e} "
                    f"(retry {attempt+1}/{retries})"
                )

            time.sleep(5)

        if response is None or response.status_code != 200:
            print("Skipping failed batch...")
            continue

        try:
            root = ET.fromstring(response.content)
        except Exception as e:
            print("XML parsing failed:", e)
            continue

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"
        }

        entries = root.findall("atom:entry", ns)

        if not entries:
            break

        for entry in entries:
            try:
                paper_id = entry.find("atom:id", ns)
                paper_id = paper_id.text.strip() if paper_id is not None else None

                if not paper_id:
                    continue

                if paper_id in seen_ids:
                    continue

                seen_ids.add(paper_id)

                title = entry.find("atom:title", ns)
                title = title.text.strip().replace("\n", " ") if title is not None else ""

                summary = entry.find("atom:summary", ns)
                summary = summary.text.strip().replace("\n", " ") if summary is not None else ""

                published = entry.find("atom:published", ns)
                published = published.text if published is not None else ""

                updated = entry.find("atom:updated", ns)
                updated = updated.text if updated is not None else ""

                authors = []
                for author in entry.findall("atom:author", ns):
                    name = author.find("atom:name", ns)
                    if name is not None:
                        authors.append(name.text.strip())

                categories = []
                for cat in entry.findall("atom:category", ns):
                    term = cat.attrib.get("term")
                    if term:
                        categories.append(term)

                primary_category = entry.find("arxiv:primary_category", ns)
                primary_category = (
                    primary_category.attrib.get("term")
                    if primary_category is not None
                    else ""
                )

                doi = entry.find("arxiv:doi", ns)
                doi = doi.text.strip() if doi is not None else ""

                journal_ref = entry.find("arxiv:journal_ref", ns)
                journal_ref = (
                    journal_ref.text.strip()
                    if journal_ref is not None
                    else ""
                )

                comment = entry.find("arxiv:comment", ns)
                comment = (
                    comment.text.strip()
                    if comment is not None
                    else ""
                )

                pdf_url = ""
                for link in entry.findall("atom:link", ns):
                    if link.attrib.get("title") == "pdf":
                        pdf_url = link.attrib.get("href")
                        break

                papers.append({
                    "id": paper_id,
                    "title": title,
                    "abstract": summary,
                    "authors": authors,
                    "author_count": len(authors),
                    "categories": categories,
                    "primary_category": primary_category,
                    "doi": doi,
                    "journal_reference": journal_ref,
                    "comment": comment,
                    "url": paper_id,
                    "pdf_url": pdf_url,
                    "published": published,
                    "updated": updated
                })

            except Exception as e:
                print("Skipping malformed paper:", e)

        print(f"Downloaded {len(papers)} / {total_records}")

        if len(papers) >= total_records:
            papers = papers[:total_records]
            break

        time.sleep(3)

    with open("arxiv_data.json", "w", encoding="utf-8") as f:
        json.dump(
            papers,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nDone! Saved {len(papers)} papers to arxiv_data.json")


if __name__ == "__main__":
    fetch_arxiv_abstracts(5000)