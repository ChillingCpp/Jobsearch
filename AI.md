# AI Operating Guide

## Purpose

You are an AI software engineer responsible for helping develop this project.

Your goal is to produce maintainable, simple and reusable code while following the project documentation.

Do not make assumptions when documentation already exists.

---

# Startup

Before writing any code, always perform the following steps.

1. Read:

./docs/vision.md
s
Understand the project's long-term goal.

2. Read:

./docs/project_plan.md

Understand the architecture.

3. Create

./docs/execution.md
After Understand project plan and vision

4. Read the current task inside

./tasks/todo/

Only work on ONE task at a time.

---

# Workflow

For every task:

Understand the task

↓

Plan the solution

↓

Implement

↓

Test

↓

Review

↓

Move task to done

Never work on multiple tasks simultaneously.

---

# Project Rules

Always prefer

- reusable code
- simple code
- readable code

Avoid

- duplicated logic
- hardcoded values
- unnecessary abstractions
- over-engineering

---

# Configuration First

Whenever possible

Prefer configuration

instead of

writing custom logic.

If a reusable solution exists,

use it.

---

# Code Quality

Keep functions small.

Keep modules focused.

Write meaningful names.

Do not create complexity unless necessary.

---

# If Documentation Is Wrong

Do not silently change it.

Instead

- explain the problem
- propose improvements in the file as comments
- wait for approval if the change affects architecture

---

# If You Are Unsure

Never invent project requirements.

Instead

leave a TODO

or

ask for clarification.

---

# Definition of Done

A task is complete only if

- implementation works
- no obvious bugs
- follows project architecture
- passes tests (if available)
- documentation is updated if necessary

---

# Git Workflow

Every completed task should be committed to Git.

Before creating a commit, verify that:

- The task has been fully completed.
- The project still builds successfully.
- Existing tests pass (if available).
- New tests are added when appropriate.
- Only files related to the current task are included.

Create one commit per completed task.

Commit messages should be short and descriptive.

Examples:

feat: add generic parser

feat: support TopCV configuration

fix: normalize salary values

refactor: simplify parser pipeline

docs: update project plan

After committing successfully, push the current branch to GitHub.

Do not commit unfinished work unless explicitly requested.

# Goal

The objective is not only to finish the project.

The objective is to keep the project easy to maintain for both humans and future AI.