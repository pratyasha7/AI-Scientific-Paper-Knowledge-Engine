# MongoDB Version

This folder contains the MongoDB-backed copy of the original JSON-based project.

The original project files are unchanged. Only the storage layer is replaced:

- `paper_v2.py` fetches raw arXiv papers and saves them into MongoDB.
- `nountotokenclean.py` reads raw papers from MongoDB, applies the same SpaCy cleaning logic, and writes cleaned documents back to MongoDB.
- `search_engine.py` reads cleaned documents from MongoDB and uses the same search, abbreviation, normalization, scoring, sorting, and output behavior as the original.

## Files

| File | Purpose |
| --- | --- |
| `paper_v2.py` | MongoDB version of the arXiv fetching script. |
| `nountotokenclean.py` | MongoDB version of the cleaning pipeline. |
| `search_engine.py` | MongoDB version of the CLI search program. |
| `mongodb_config.py` | Central MongoDB connection/configuration helper. |
| `.env` | Local environment variables such as MongoDB URI and collection names. |
| `requirements.txt` | Extra dependencies needed for MongoDB and `.env` loading. |

## Environment Variables

All MongoDB settings are stored in `.env`.

Default `.env`:

```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=scientific_paper_engine
MONGO_RAW_COLLECTION=arxiv_data
MONGO_CLEANED_COLLECTION=after_cleaning_final_research_data
```

### Variable Meaning

| Variable | Meaning |
| --- | --- |
| `MONGO_URI` | MongoDB connection string. Use a local MongoDB URI or MongoDB Atlas URI. |
| `MONGO_DB_NAME` | Database name used by this project. |
| `MONGO_RAW_COLLECTION` | Collection where raw arXiv papers are stored. |
| `MONGO_CLEANED_COLLECTION` | Collection where cleaned/searchable papers are stored. |

For MongoDB Atlas, replace `MONGO_URI` with your Atlas connection string:

```env
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER_HOST/?retryWrites=true&w=majority
```

Keep the database and collection names the same if you want the exact same flow described below.

## Setup

Run all commands from this folder:

```powershell
cd "C:\INTERNSHIP_TASK\AI_SCIENTIFIC_PAPER\WITHOUT_ MONGODB\AI-Scientific-Paper-Knowledge-Engine\mongo_version"
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

The cleaning script also needs the same SpaCy model as the original project:

```powershell
python -m spacy download en_core_web_sm
```

Make sure MongoDB is running before executing the scripts.

For local MongoDB, the default URI is:

```env
mongodb://localhost:27017/
```

For MongoDB Atlas, update `MONGO_URI` in `.env`.

## Execution Flow

The intended full pipeline is:

```text
paper_v2.py
  -> MongoDB raw collection
  -> nountotokenclean.py
  -> MongoDB cleaned collection
  -> search_engine.py
```

This matches the original JSON pipeline:

```text
paper.py
  -> arxiv_data.json
  -> nountotokenclean.py
  -> after_cleaning_final_research_data.json
  -> search_engine.py
```

Only the storage backend changes from JSON files to MongoDB collections.

## Run Option 1: Full Pipeline

Use this when starting from no MongoDB data.

Step 1: Fetch raw arXiv papers into MongoDB:

```powershell
python paper_v2.py
```

What it does:

- Calls the arXiv API.
- Uses the same query as the original script.
- Fetches papers in chunks of 100.
- Preserves the same fields:
  - `title`
  - `abstract`
  - `url`
  - `published`
  - `updated`
- Clears the raw MongoDB collection.
- Inserts the newly fetched raw papers.

Step 2: Clean raw papers and save cleaned documents:

```powershell
python nountotokenclean.py
```

What it does:

- Reads raw papers from `MONGO_RAW_COLLECTION`.
- Runs the same SpaCy NLP pipeline.
- Preserves the same regex cleaning, filters, corrections, noun chunk extraction, acronym extraction, and ordering.
- Adds:
  - `cleaned_keywords`
  - `important_phrases`
- Clears the cleaned MongoDB collection.
- Inserts the cleaned papers.

Step 3: Start the search engine:

```powershell
python search_engine.py
```

What it does:

- Reads cleaned papers from `MONGO_CLEANED_COLLECTION`.
- Builds the same abbreviation map.
- Starts the same terminal search loop.
- Uses the same scoring:
  - exact title match: `+60`
  - partial title match: `+30`
  - exact keyword match: `+20`
  - exact phrase match: `+15`
  - partial phrase match: `+5`
- Shows the top 5 results.

To exit:

```text
exit
```

## Run Option 2: Fetch Only

Use this if you only want to populate the raw MongoDB collection:

```powershell
python paper_v2.py
```

After this, data exists only in the raw collection. Search will not work until the cleaning script has been run.

## Run Option 3: Clean Existing Raw MongoDB Data

Use this if raw papers already exist in MongoDB:

```powershell
python nountotokenclean.py
```

This reads from the raw collection and refreshes the cleaned collection.

## Run Option 4: Search Existing Cleaned Data

Use this if cleaned documents already exist in MongoDB:

```powershell
python search_engine.py
```

This does not fetch or clean data. It only loads the cleaned collection and starts the CLI search loop.

## MongoDB Data Schema

Raw collection document shape:

```json
{
  "title": "Paper title",
  "abstract": "Paper abstract",
  "url": "http://arxiv.org/abs/...",
  "published": "2026-04-03T17:59:39Z",
  "updated": "2026-04-03T17:59:39Z"
}
```

Cleaned collection document shape:

```json
{
  "title": "Paper title",
  "abstract": "Paper abstract",
  "url": "http://arxiv.org/abs/...",
  "published": "2026-04-03T17:59:39Z",
  "updated": "2026-04-03T17:59:39Z",
  "cleaned_keywords": ["keyword"],
  "important_phrases": ["important phrase"]
}
```

MongoDB automatically adds `_id` to stored documents. The search and cleaning scripts exclude `_id` while reading so the application data shape remains the same as the original JSON records.

