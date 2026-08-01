# Vision

## Project

This project aims to build a personal job aggregation platform that collects job postings from multiple recruitment websites and presents them in a unified format.

The system is intended for long-term personal use and continuous improvement.

---

## Goal

The project should be easy to extend, easy to maintain, and easy for AI to continue developing.

Adding support for a new recruitment website should require as little custom code as possible.

Whenever possible, reusable components and configuration should be preferred over website-specific implementations.

---

## Non-Goals

This project is not intended to become a distributed crawling platform.

It does not aim to support millions of jobs or enterprise-scale infrastructure.

The priority is maintainability, simplicity, and learning rather than maximum performance.

Features should only be added when they provide clear value.

--- 

## Design Philosophy

Keep the architecture simple.

Prefer reusable engines over duplicated logic.

Prefer configuration over custom implementation.

Avoid unnecessary abstractions.

The project should remain understandable even after months without maintenance.

---

## AI Philosophy

AI is a development assistant, not the owner of the project.

AI should follow existing documentation before making implementation decisions.

AI should complete one task at a time.

AI should avoid introducing unnecessary complexity.

If documentation is unclear, AI should ask for clarification instead of making assumptions.

---

## Success Criteria

The project is considered successful when:

- Multiple recruitment websites are supported.
- New websites can be added quickly.
- Most website-specific behavior is described through configuration.
- The codebase remains clean and maintainable.
- AI can continue extending the project without requiring a complete re-explanation of the system.