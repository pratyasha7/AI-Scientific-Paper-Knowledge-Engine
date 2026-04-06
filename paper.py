# import requests
# import xml.etree.ElementTree as ET
# import time
# import json

# def fetch_arxiv_abstracts(total_records=5000):
#     # 1. Use HTTPS instead of HTTP
#     base_url = "https://export.arxiv.org/api/query"
    
#     # 2. Simplified query to ensure it works first
#     # We will let 'requests' handle the encoding
#     query = 'all:"machine learning" OR all:physics OR cat:cs.AI'
    
#     papers = []
#     chunk_size = 100

#     print(f"Starting to download {total_records} abstracts...")

#     for i in range(0, total_records, chunk_size):
#         params = {
#             "search_query": query,
#             "start": i,
#             "max_results": chunk_size,
#             "sortBy": "submittedDate",
#             "sortOrder": "descending"
#         }

#         # Adding a User-Agent header makes the request look more like a browser
#         headers = {
#             'User-Agent': 'MyResearchScript/1.0 (contact: your-email@example.com)'
#         }

#         response = requests.get(base_url, params=params, headers=headers)
        
#         # DEBUG: If it fails, show us why
#         if response.status_code != 200:
#             print(f"Error fetching data. Status Code: {response.status_code}")
#             print(f"Reason: {response.reason}")
#             # If you get a 403 or 503, you might be temporarily rate-limited.
#             break

#         root = ET.fromstring(response.content)
#         ns = {'atom': 'http://www.w3.org/2005/Atom'}
#         entries = root.findall('atom:entry', ns)

#         if not entries:
#             print("No entries found for this query.")
#             break

#         for entry in entries:
#             title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
#             summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
#             link = entry.find('atom:id', ns).text
            
#             papers.append({
#                 "title": title,
#                 "abstract": summary,
#                 "url": link
#             })

#         print(f"Downloaded {len(papers)} / {total_records}...")
        
#         # Wait 3 seconds instead of 2 to be extra safe
#         time.sleep(3)

#     with open("arxiv_data.json", "w", encoding="utf-8") as f:
#         json.dump(papers, f, indent=4)

#     print(f"Done! Saved {len(papers)} abstracts to 'arxiv_data.json'")

# if __name__ == "__main__":
#     fetch_arxiv_abstracts(5000)


import requests
import xml.etree.ElementTree as ET
import time
import json

def fetch_arxiv_abstracts(total_records=5000):
    base_url = "https://export.arxiv.org/api/query"
    
    # Your search query
    query = 'all:"machine learning" OR all:physics OR cat:cs.AI'
    
    papers = []
    chunk_size = 100

    print(f"Starting to download {total_records} abstracts...")

    for i in range(0, total_records, chunk_size):
        params = {
            "search_query": query,
            "start": i,
            "max_results": chunk_size,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        headers = {
            'User-Agent': 'MyResearchScript/1.0 (contact: your-email@example.com)'
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)
            if response.status_code != 200:
                print(f"Error fetching data. Status Code: {response.status_code}")
                break

            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)

            if not entries:
                print("No more entries found.")
                break

            for entry in entries:
                # Basic Metadata
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                link = entry.find('atom:id', ns).text
                
                # --- NEW: Extracting Date ---
                # 'published' is the original submission date
                published = entry.find('atom:published', ns).text
                # 'updated' is the latest version date
                updated = entry.find('atom:updated', ns).text

                papers.append({
                    "title": title,
                    "abstract": summary,
                    "url": link,
                    "published": published,
                    "updated": updated
                })

            print(f"Downloaded {len(papers)} / {total_records}...")
            
            # API Courtesy: Wait 3 seconds
            time.sleep(3)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    with open("arxiv_data.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=4)

    print(f"Done! Saved {len(papers)} abstracts to 'arxiv_data.json'")

if __name__ == "__main__":
    fetch_arxiv_abstracts(5000)