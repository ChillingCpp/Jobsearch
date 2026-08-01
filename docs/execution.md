# Execution Plan

## Overview

This document translates the project vision and architecture into an actionable execution plan for AI and human developers.

It defines how the project will be built, in what order, and what each step must accomplish.

---

## Project Summary

A configuration-driven job aggregation system in Python.

A generic engine crawls, parses, normalizes and stores job postings from multiple recruitment websites.

Website-specific behavior is described through YAML configuration files, not custom code.

---

## Architecture Recap

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

Each module has a single responsibility and communicates through well-defined interfaces.

---

## Module Responsibilities

| Module       | Responsibility                                        | Must NOT do                    |
|--------------|-------------------------------------------------------|--------------------------------|
| Crawler      | Download HTML, handle browser automation, retries     | Parse HTML, write to DB        |
| Parser       | Extract raw data from HTML using config               | Normalize, write to DB         |
| Normalizer   | Standardize salary, location, dates, etc.             | Depend on website specifics    |
| Storage      | Save, update, query jobs                              | Contain business logic         |
| Scheduler    | Decide when crawling happens                         | Crawl or parse itself          |
| Configuration| Load website configs (selectors, pagination, etc.)   | Contain business logic         |

---

## Folder Structure

```
job_aggregator/
├── src/
│   ├── core/
│   ├── crawler/
│   ├── parser/
│   ├── normalizer/
│   ├── storage/
│   ├── database/
│   ├── scheduler/
│   ├── models/
│   ├── utils/
│   └── main.py
├── tests/
├── requirements.txt
├── README.md
├── configs/
├── docs/
└── tasks/
    ├── todo/
    └── done/
```

---

## Technology Stack

- Python 3
- Playwright (browser automation)
- Requests (simple HTTP)
- BeautifulSoup / lxml (HTML parsing)
- Pydantic (data validation)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- YAML (configuration)
- pytest (testing)
- Python logging module

---

## Execution Order

The project will be built in phases. Each phase produces a working, testable increment.

### Phase 1 — Project Skeleton

- Create folder structure
- Create `requirements.txt`
- Create `README.md`
- Create empty module stubs
- Set up pytest

### Phase 2 — Data Models

- Define Job model with Pydantic
- Define normalized fields (title, company, salary, location, etc.)

### Phase 3 — Configuration Layer

- Load YAML website configs
- Define config schema (selectors, pagination, browser actions)

### Phase 4 — Crawler

- Implement HTML downloader
- Implement browser automation wrapper
- Retries and delays

### Phase 5 — Parser

- Apply config selectors to HTML
- Produce raw job data

### Phase 6 — Normalizer

- Standardize salary, location, employment type, dates

### Phase 7 — Storage / Database

- SQLAlchemy models
- Save, update, query operations

### Phase 8 — Scheduler

- Manual, daily, hourly crawl triggers

### Phase 9 — CLI / Entry Point

- `main.py` to run the pipeline

### Phase 10 — First Website Configuration

- Add a real recruitment website config
- End-to-end test

---

## Coding Principles

- Keep functions small and focused.
- Keep modules single-responsibility.
- Prefer configuration over custom code.
- Prefer reusable components over duplication.
- Write readable, explicit code.
- Avoid unnecessary abstractions and over-engineering.
- Do not add complexity for hypothetical future needs.

---

## Definition of Done

A task is complete only when:

- Implementation works.
- No obvious bugs.
- Follows project architecture.
- Passes tests (if available).
- Documentation is updated if necessary.
- Committed to Git with a short, descriptive message.