# QueryMapper

## Overview

QueryMapper maps a logical job category into one or more search keywords before scraping.

It acts as a layer between the user's intent (e.g. "I want IT jobs") and the actual search queries sent to recruitment websites.

## Purpose

- Map a logical job category into one or more search keywords.
- Allow the scraper to search for multiple related keywords per category.
- Keep the mapping logic separate from scraping, parsing, and filtering.

## Usage

```python
from src.core.query_mapper import QueryMapper

mapper = QueryMapper()

# Known category
keywords = mapper.map("it")
# -> ["backend", "frontend", "fullstack", "software engineer", "devops"]

# Unknown category returns itself
keywords = mapper.map("data science")
# -> ["data science"]
```

## Built-in Mappings

| Category   | Keywords                                                        |
|------------|-----------------------------------------------------------------|
| `it`       | backend, frontend, fullstack, software engineer, devops         |
| `marketing`| marketing, digital marketing, content marketing                 |
| `sales`    | sales, kinh doanh, business development                         |

## Extensibility

New mappings can be added in two ways:

### 1. At initialization

```python
mapper = QueryMapper(mappings={"design": ["ui", "ux", "graphic design"]})
```

Custom mappings are merged over the defaults.

### 2. At runtime

```python
mapper = QueryMapper()
mapper.add_mapping("finance", ["accountant", "financial analyst"])
```

## Integration with Pipeline

The pipeline accepts a `category` and a `QueryMapper`. When both are provided
and the config has a `search_url` with a `{keyword}` placeholder, the pipeline:

1. Maps the category to keywords via QueryMapper.
2. Builds one search URL per keyword.
3. Scrapes each search URL as before.

Example config:

```yaml
name: topcv
start_url: https://www.topcv.vn/tim-viec-lam-moi-nhat
search_url: https://www.topcv.vn/tim-viec-lam-moi-nhat?keyword={keyword}
```

CLI usage:

```bash
python src/main.py --once --category it
```

## Constraints

- QueryMapper only maps categories to keywords.
- It does NOT perform scraping, parsing, pagination, networking, or filtering.
- Unknown categories return the category itself as a single keyword.