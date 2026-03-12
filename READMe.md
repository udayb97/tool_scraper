## Tool Scraper

`Tool Scraper` is a small Python CLI that ingests job descriptions, detects tool and technology names from a maintained dictionary, and stores the results in SQLite for later analysis.

The project currently supports:

- Loading a single job description from a local text file
- Fetching a single job posting from a URL
- Processing a batch of job-posting URLs from a file
- Persisting raw job text plus detected tools into `data/jobs.db`
- Reporting tool frequencies across all stored jobs

## How It Works

The project is organized around a simple pipeline:

1. `ingestion.py` loads raw job text from a file or downloads and cleans HTML from a URL.
2. `extractor.py` reads `skills_dictionary.txt`, builds a regular expression, and matches known tool names in the job text.
3. `database.py` initializes and writes to a SQLite database at `data/jobs.db`.
4. `main.py` coordinates ingestion, extraction, and persistence.
5. `analysis.py` queries the stored results and prints tool frequencies.

## Project Structure

```text
.
|-- main.py                 # CLI entry point for ingestion and extraction
|-- ingestion.py            # Load job text from files or URLs
|-- extractor.py            # Dictionary-backed regex extractor
|-- database.py             # SQLite schema and insert helpers
|-- analysis.py             # Frequency report for stored tools
|-- skills_dictionary.txt   # Canonical list of detectable tools/skills
|-- jobs0312.txt            # Example batch file of job URLs
|-- sample_job1.txt         # Example local input file (currently empty)
|-- data/
|   `-- jobs.db             # SQLite database, created on first run
`-- scraper.py              # Placeholder file, currently unused
```

## Requirements

- Python 3.10+ is a safe baseline for this codebase
- Packages listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

Current dependencies:

- `beautifulsoup4`
- `requests`

## Usage

### 1. Process a local text file

```bash
python main.py --text sample_job1.txt
```

### 2. Process a single job URL

```bash
python main.py --url "https://example.com/job-posting"
```

### 3. Process a batch of job URLs

```bash
python main.py --batch jobs0312.txt
```

For a single job, the script prints the inserted `job_id` and the detected tools.  
For batch mode, it prints one processed `job_id` per URL.

## Output and Storage

The application stores data in `data/jobs.db` using three tables:

- `jobs`: source URL or file path, raw extracted text, timestamp
- `tools`: unique tool names
- `job_tools`: many-to-many mapping between jobs and tools

To inspect aggregate results:

```bash
python analysis.py
```

This prints output in the form:

```text
Python: 4
SQL: 3
AWS: 2
```

## Tool Dictionary

Detection is driven entirely by `skills_dictionary.txt`.  
Each non-empty line is treated as a valid tool or skill label.

Examples already included:

- Languages: `Python`, `Java`, `Scala`, `Go`
- Data platforms: `Spark`, `Databricks`, `Snowflake`, `BigQuery`
- Cloud tools: `AWS`, `GCP`, `Azure`
- Orchestration and ETL: `Airflow`, `dbt`, `Fivetran`, `Informatica`
- DevOps and observability: `Docker`, `Kubernetes`, `Terraform`, `Grafana`

To expand coverage, add one item per line to `skills_dictionary.txt`.

## Notes on Extraction Behavior

The extractor is intentionally simple:

- Matching is case-insensitive
- Matching is dictionary-based, not ML-based
- Results are de-duplicated per job before insertion into the `tools` table
- The returned detected tools are sorted alphabetically

Because extraction is regex-based, expect some limitations:

- Multi-word tools depend on exact dictionary phrasing
- Broad terms such as `SQL`, `Streaming`, or `Machine Learning` can create false positives
- Synonyms are only detected if each variant is listed in `skills_dictionary.txt`
- The scraper captures general page text, not job-site-specific structured fields

## Current Repository State

The current checked-in project has a few practical details worth knowing:

- `sample_job1.txt` exists but is empty
- `data/jobs.db` currently has no stored jobs, tools, or links
- `scraper.py` exists but has no implementation and is not used by the CLI
- `data/.gitgnore` appears to be intended as a local ignore file for database artifacts

## Suggested Next Improvements

If you want to evolve the project, the next high-value changes are:

- Add tests for text ingestion, extraction, and database writes
- Normalize duplicate job URLs before inserting batch results
- Prevent duplicate rows in `job_tools`
- Add job-site-specific parsers for cleaner text extraction
- Support exporting results to CSV or JSON
- Rename `READMe.md` to the conventional `README.md`

## Quick Start

```bash
pip install -r requirements.txt
python main.py --text sample_job1.txt
python analysis.py
```
