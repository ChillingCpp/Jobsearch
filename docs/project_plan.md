# Overview

The project is a configuration-driven job aggregation system.

A generic engine is responsible for crawling, parsing, normalizing and storing job information.

Each recruitment website should provide only configuration whenever possible.

The core engine should remain independent of individual websites.
# Description

- The crawler is responsible for downloading web pages.
- The parser extracts raw information from HTML.
- The normalizer converts raw values into a unified format.
- The database stores normalized job records.
- Every stage should perform only one responsibility.

# Project Architecture

The project consists of four major parts.

- Generic Engine
- Website Configurations
- Data Models
- Task Automation

The generic engine should never contain website-specific logic.

Website-specific behavior belongs inside configuration files.

# Folder Structure

job_aggregator/

├── src/
│   │
│   ├── core/
│   │
│   ├── crawler/
│   │
│   ├── parser/
│   │
│   ├── normalizer/
│   │
│   ├── storage/
│   │
│   ├── database/
│   │
│   ├── scheduler/
│   │
│   ├── models/
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── tests/
│   Unit test 
|
├── requirements.txt
│
├── README.md
│
├── configs/
|   contains website configuration
|
├── docs/
|   What AI read and execute
|   
├── tasks/
|   What AI need to do, AI create this folder

# Data Flow

The system processes job data through a simple pipeline.

Website
↓
Crawler
↓
Raw HTML
↓
Parser
↓
Raw Job Data
↓
Normalizer
↓
Job Model
↓
Database
↓
API / CLI / Export
# Modules

## Crawler

Responsible for retrieving web pages.

Responsibilities:

- Download HTML
- Handle browser automation when necessary
- Manage retries and delays
- Return raw HTML

The crawler should never parse HTML or write to the database.

---

## Parser

Responsible for extracting information from HTML.

Responsibilities:

- Read HTML
- Apply website configuration
- Produce raw job data

The parser should never perform normalization or database operations.

---

## Normalizer

Responsible for transforming raw values into standardized values.

Examples:

- Salary
- Location
- Employment type
- Experience level
- Dates

Normalization should be independent from website implementations.

---

## Storage

Responsible for saving and loading data.

Responsibilities:

- Store jobs
- Update existing records
- Query data

The storage layer should hide database implementation details.

---

## Scheduler

Responsible for deciding when crawling should happen.

Examples:

- Manual crawl
- Daily crawl
- Hourly crawl

---

## Configuration

Responsible for loading website configurations.

Configuration defines:

- Selectors
- Pagination
- Browser actions
- Extraction rules

The configuration layer should not contain business logic.

# Config Driven

The project follows a configuration-driven architecture.

Whenever possible, website-specific behavior should be described using configuration instead of Python code.

Each supported website owns its own configuration.

Configuration may describe:

- CSS selectors
- XPath selectors
- Pagination rules
- Browser actions
- Wait conditions
- Data transformations
- Request headers

The generic engine reads configuration and performs the work.

Adding support for a new website should require little or no modification to the core engine.

# Technology

Current technology choices.

Language

- Python 3

Crawler

- Playwright
- Requests (when browser automation is unnecessary)

HTML Parsing

- BeautifulSoup
- lxml (optional)

Data Validation

- Pydantic

Database

- PostgreSQL

ORM

- SQLAlchemy

Configuration

- YAML

Testing

- pytest

Logging

- Python logging module

The technology stack may evolve as the project grows, but simplicity and maintainability should remain the priority.

# Coding Principles

The project values maintainability over complexity.

## Keep It Simple

Prefer straightforward solutions.

Avoid unnecessary abstractions.

---

## Single Responsibility

Each module should perform one primary responsibility.

---

## Reusability

Prefer reusable components over duplicated logic.

---

## Configuration First

Whenever possible, solve website differences through configuration instead of creating custom code.

---

## Readability

Code should be easy to understand.

Prefer explicit code over clever code.

---

## Small Functions

Functions should have one clear purpose.

Large functions should be split into smaller units.

---

## Loose Coupling

Modules should communicate through well-defined interfaces.

Avoid tight dependencies between components.

---

## Extensibility

The architecture should allow future expansion without major refactoring.

Adding support for a new website should not require modifying unrelated modules.

# Future Expansion
The architecture should allow

- adding new websites without rewrite code
- supporting new extractors
- supporting browser automation 

without major changes to the core engine.

# Project Constraints

The project is intended to remain a personal application.

Avoid introducing enterprise patterns unless they solve a real problem.

Optimize for maintainability before optimization.

Prefer one good generic solution over multiple specialized implementations.

Avoid premature optimization.

Do not add complexity for hypothetical future requirements.