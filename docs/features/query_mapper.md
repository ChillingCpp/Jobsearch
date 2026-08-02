# QueryMapper

## Overview

QueryMapper maps a logical job category into one or more search keywords before scraping.

It acts as a layer between the user's intent (e.g. "I want IT jobs") and the actual search queries sent to recruitment websites.

## Purpose

- Map a logical job category into one or more search keywords.
- Allow the scraper to search for multiple related keywords per category.
- Keep the mapping logic separate from scraping, parsing, and filtering.

## Configuration

Category-to-keyword mappings are defined in each website's YAML config under `category_mappings`.

This follows the project's **Configuration First** principle — no mappings are hardcoded in Python.

Example (`configs/topcv.yaml`):

```yaml
name: topcv
start_url: https://www.topcv.vn/tim-viec-lam-moi-nhat
search_url: https://www.topcv.vn/tim-viec-lam-moi-nhat?keyword={keyword}
category_mappings:
  it:
    - backend
    - frontend
    - fullstack
    - software engineer
    - devops
  marketing:
    - marketing
    - digital marketing
    - content marketing
  sales:
    - sales
    - kinh doanh
    - business development
```

## Usage

### In Python

```python
from src.core.query_mapper import QueryMapper

mapper = QueryMapper({"it": ["backend", "frontend"]})

# Known category
keywords = mapper.map("it")
# -> ["backend", "frontend"]

# Unknown category returns itself
keywords = mapper.map("data science")
# -> ["data science"]
```

### Via CLI

```bash
python src/main.py --once --category it
```

## How It Works in the Pipeline

1. The pipeline receives a `category` (from CLI `--category`).
2. For each config:
   - If the config has `category_mappings`, a QueryMapper is created from those mappings.
   - Otherwise, the global QueryMapper (if provided) is used as fallback.
3. If the config has a `search_url` with `{keyword}` placeholder:
   - The category is mapped to keywords.
   - One search URL is built per keyword (URL-encoded).
   - Each URL is scraped with pagination as normal.
4. If no category or no `search_url`, the config's `start_url` is used as-is.

## Extensibility

New mappings can be added in two ways:

### 1. In config (recommended)

Add a new category under `category_mappings` in the YAML file.

### 2. At runtime

```python
mapper = QueryMapper()
mapper.add_mapping("finance", ["accountant", "financial analyst"])
```

## Constraints

- QueryMapper only maps categories to keywords.
- It does NOT perform scraping, parsing, pagination, networking, or filtering.
- Unknown categories return the category itself as a single keyword.
- Mappings are config-driven, not hardcoded.