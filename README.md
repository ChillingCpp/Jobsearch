# Job Aggregator

A configuration-driven job aggregation system.

It crawls job postings from multiple recruitment websites, parses them using per-website YAML configuration, normalizes the data into a unified format, and stores the results in a database.

## Architecture

The system is a pipeline of independent modules:

```
Website
   ↓
Crawler        → downloads HTML
   ↓
Parser         → extracts raw job data using config
   ↓
Normalizer     → converts raw values to unified format
   ↓
Job Model      → validated data structure
   ↓
Database       → stores normalized records
   ↓
API / CLI / Export
```

Each module has a single responsibility. Website-specific behavior is described through configuration files, not custom code.

## Project Structure

```
src/
├── core/          # Generic engine
├── crawler/       # HTML downloader
├── parser/        # HTML extraction
├── normalizer/    # Value standardization
├── storage/       # Save / load / query
├── database/      # Database layer
├── scheduler/     # Crawl timing
├── models/        # Data models
├── utils/         # Shared helpers
└── main.py        # Entry point
tests/             # Unit tests
configs/           # Website configurations
docs/              # Project documentation
tasks/             # Task tracking
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```

## Documentation

- `docs/vision.md` — project vision
- `docs/project_plan.md` — architecture
- `docs/execution.md` — execution plan