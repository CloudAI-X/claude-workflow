---
name: analyzing-projects
description: Analyzes codebases to understand structure, tech stack, patterns, and conventions. Use when onboarding to a new project, exploring unfamiliar code, or when asked "how does this work?" or "what's the architecture?"
---

# Analyzing Projects

### When to Load

- **Trigger**: Onboarding to a new project, "how does this work" questions, codebase exploration, understanding unfamiliar code
- **Skip**: Already familiar with the project structure and patterns

## Project Analysis Workflow

Copy this checklist and track progress:

```
Project Analysis Progress:
- [ ] Step 1: Quick overview (README, root files)
- [ ] Step 2: Detect tech stack
- [ ] Step 3: Map project structure
- [ ] Step 4: Identify key patterns
- [ ] Step 5: Find development workflow
- [ ] Step 6: Generate summary report
```

## Step 1: Quick Overview

```bash
# Check for common project markers
ls -la
cat README.md 2>/dev/null | head -50
```

## Step 2: Tech Stack Detection

### Package Managers & Dependencies

- `package.json` → Node.js/JavaScript/TypeScript
- `requirements.txt` / `pyproject.toml` / `setup.py` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `pom.xml` / `build.gradle` → Java
- `Gemfile` → Ruby

### Frameworks (from dependencies)

- React, Vue, Angular, Next.js, Nuxt
- Express, FastAPI, Django, Flask, Rails
- Spring Boot, Gin, Echo

### Infrastructure

- `Dockerfile`, `docker-compose.yml` → Containerized
- `kubernetes/`, `k8s/` → Kubernetes
- `terraform/`, `.tf` files → IaC
- `serverless.yml` → Serverless Framework
- `.github/workflows/` → GitHub Actions

## Step 3: Project Structure Analysis

Present as a tree with annotations:

```
project/
├── src/              # Source code
│   ├── components/   # UI components (React/Vue)
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   └── utils/        # Shared utilities
├── tests/            # Test files
├── docs/             # Documentation
└── config/           # Configuration
```

## Step 4: Key Patterns Identification

Look for and report:

- **Architecture**: Monolith, Microservices, Serverless, Monorepo
- **API Style**: REST, GraphQL, gRPC, tRPC
- **State Management**: Redux, Zustand, MobX, Context
- **Database**: SQL, NoSQL, ORM used
- **Authentication**: JWT, OAuth, Sessions
- **Testing**: Jest, Pytest, Go test, etc.

## Step 5: Development Workflow

Check for:

- `.eslintrc`, `.prettierrc` → Linting/Formatting
- `.husky/` → Git hooks
- `Makefile` → Build commands
- `scripts/` in package.json → NPM scripts

## Step 6: Output Format

Generate a summary using this template:

```markdown
# Project: [Name]

## Overview

[1-2 sentence description]

## Tech Stack

| Category  | Technology |
| --------- | ---------- |
| Language  | TypeScript |
| Framework | Next.js 14 |
| Database  | PostgreSQL |
| ...       | ...        |

## Architecture

[Description with simple ASCII diagram if helpful]

## Key Directories

- `src/` - [purpose]
- `lib/` - [purpose]

## Entry Points

- Main: `src/index.ts`
- API: `src/api/`
- Tests: `npm test`

## Conventions

- [Naming conventions]
- [File organization patterns]
- [Code style preferences]

## Quick Commands

| Action  | Command         |
| ------- | --------------- |
| Install | `npm install`   |
| Dev     | `npm run dev`   |
| Test    | `npm test`      |
| Build   | `npm run build` |
```

## Analysis Validation

After completing analysis, verify:

```
Analysis Validation:
- [ ] All major directories explained
- [ ] Tech stack accurately identified
- [ ] Entry points documented
- [ ] Development commands verified working
- [ ] No assumptions made without evidence
```

If any items cannot be verified, note them as "needs clarification" in the report.
