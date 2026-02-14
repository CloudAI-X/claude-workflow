---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
description: Explore the repository with 10 parallel subagents to create comprehensive documentation. Creates CODEBASE.md with full architecture analysis.
---

# Bootstrap Repository

Perform a comprehensive exploration of the current repository using 10 parallel subagents, then synthesize findings into a single CODEBASE.md document.

## Phase 1: Initial Scan

Before spawning subagents, gather basic repo info:

```bash
git remote -v
git log --oneline -5
```

Use Glob to identify the project root and top-level structure:

- Check for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Dockerfile`, etc.
- Identify the primary language and framework

## Phase 2: Spawn 10 Exploration Subagents (Parallel)

**CRITICAL**: Launch ALL 10 Task calls in a SINGLE message for true parallelism. Each subagent uses `run_in_background: true`.

```
[Task 1]
description: "File Structure Explorer"
prompt: "Map the complete directory tree of this repository. Identify:
- Top-level directory purposes (src/, lib/, tests/, docs/, etc.)
- Entry points (main files, index files, app files)
- Configuration files and their roles
- Generated vs source directories
- File count and language breakdown by directory
Report a structured tree with annotations for each directory's purpose."
run_in_background: true

[Task 2]
description: "Dependency Analyzer"
prompt: "Analyze all dependency files in this repository:
- Package manifests (package.json, pyproject.toml, Cargo.toml, go.mod, etc.)
- Lock files and their state
- Direct vs transitive dependency count
- Key dependencies and what they provide (framework, ORM, HTTP client, etc.)
- Dev dependencies and their purposes
- Any outdated or pinned versions worth noting
Report a categorized dependency inventory."
run_in_background: true

[Task 3]
description: "Architecture Mapper"
prompt: "Determine the high-level architecture of this project:
- Architectural style (monolith, microservices, serverless, plugin system, CLI, library)
- Layer structure (presentation, business logic, data access)
- Module boundaries and how they communicate
- Key abstractions and interfaces
- Configuration management approach
- Error handling patterns
Create an ASCII architecture diagram showing component relationships."
run_in_background: true

[Task 4]
description: "Data Layer Analyst"
prompt: "Analyze the data layer of this repository:
- Database type and ORM/query builder used
- Schema definitions or migrations
- Models/entities and their relationships
- Data validation approach
- Caching strategy (if any)
- File-based storage or state management
If no database exists, analyze how state and data are managed (files, config, in-memory)."
run_in_background: true

[Task 5]
description: "API Surface Mapper"
prompt: "Map all external-facing interfaces:
- HTTP/REST/GraphQL endpoints with methods and paths
- CLI commands and their arguments
- Library exports and public API
- Event handlers or message consumers
- Webhook endpoints
- Plugin interfaces or extension points
For each interface, note its purpose and any authentication requirements."
run_in_background: true

[Task 6]
description: "Testing Analyst"
prompt: "Evaluate the testing setup:
- Test framework(s) used
- Test directory structure
- Types of tests present (unit, integration, e2e, snapshot)
- Test configuration files
- Coverage configuration and thresholds
- Test utilities, fixtures, and helpers
- How to run the tests (commands)
- Approximate test count and coverage level"
run_in_background: true

[Task 7]
description: "Deployment Analyst"
prompt: "Analyze deployment and CI/CD configuration:
- CI/CD pipeline files (.github/workflows, .gitlab-ci.yml, Jenkinsfile, etc.)
- Dockerfile and docker-compose configurations
- Infrastructure-as-code (Terraform, Pulumi, CloudFormation)
- Environment configuration (.env.example, config files)
- Build scripts and output
- Release/versioning strategy
- Deployment targets (cloud provider, platform)"
run_in_background: true

[Task 8]
description: "Security Reviewer"
prompt: "Perform a security-oriented scan:
- Authentication and authorization mechanisms
- Secret management approach (.env, vault, etc.)
- Input validation and sanitization patterns
- CORS, CSP, and other security headers
- Dependency vulnerability indicators
- File permission patterns
- Any security-related middleware or hooks
Note: Do NOT report actual secret values, only patterns."
run_in_background: true

[Task 9]
description: "Documentation Auditor"
prompt: "Catalog existing documentation:
- README files and their completeness
- API documentation (Swagger, JSDoc, docstrings)
- Architecture decision records (ADRs)
- Contributing guides
- Changelog and versioning docs
- Inline code documentation quality
- Configuration documentation
Rate documentation completeness: None / Minimal / Moderate / Comprehensive"
run_in_background: true

[Task 10]
description: "Domain Model Analyst"
prompt: "Understand the business domain:
- Core domain concepts and entities
- Business rules encoded in the codebase
- Domain-specific terminology (build a glossary)
- Workflows and state machines
- Validation rules and constraints
- Key algorithms or business logic
Report a domain glossary and concept map."
run_in_background: true
```

## Phase 3: Collect Results

After all subagents complete, retrieve each result:

```
TaskOutput: task_1_id
TaskOutput: task_2_id
TaskOutput: task_3_id
TaskOutput: task_4_id
TaskOutput: task_5_id
TaskOutput: task_6_id
TaskOutput: task_7_id
TaskOutput: task_8_id
TaskOutput: task_9_id
TaskOutput: task_10_id
```

## Phase 4: Synthesize into CODEBASE.md

Combine all subagent findings into a single `CODEBASE.md` at the project root. Use this structure:

```markdown
# [Project Name] - Codebase Documentation

> Auto-generated by bootstrap-repo on YYYY-MM-DD

## Overview

[2-3 sentence summary: what the project is, its primary purpose, and tech stack]

## Architecture

[ASCII diagram of component relationships]
```

+-------------------+
| Component A |
+--------+----------+
|
v
+--------+----------+
| Component B |
+-------------------+

```

### Architectural Style
[Monolith / Microservices / Serverless / Library / CLI / Plugin / etc.]

### Key Design Decisions
- [Decision] -- [Rationale]

## Project Structure

```

repo-root/
src/ -- [purpose]
tests/ -- [purpose]
docs/ -- [purpose]
...

```

### Entry Points
- `path/to/main` -- [what it does]

## Dependencies

### Runtime
| Package | Purpose |
|---------|---------|
| pkg-a   | HTTP framework |

### Development
| Package | Purpose |
|---------|---------|
| pkg-b   | Test runner |

## Data Layer

[Database, ORM, schema summary, key models and relationships]

## API Surface

### [Interface Type: REST / CLI / Library / etc.]
| Endpoint/Command | Method | Purpose |
|-----------------|--------|---------|
| /api/foo        | GET    | Fetches foo |

## Testing

- **Framework**: [name]
- **Run command**: `[command]`
- **Coverage**: [level or percentage]
- **Test types**: [unit, integration, e2e]

## Deployment

- **CI/CD**: [platform]
- **Runtime**: [Docker, serverless, etc.]
- **Environments**: [dev, staging, prod]

## Security

- **Auth**: [mechanism]
- **Secrets**: [management approach]
- **Key patterns**: [validation, sanitization]

## Documentation Status

[None / Minimal / Moderate / Comprehensive] -- [summary of what exists]

## Domain Glossary

| Term | Definition |
|------|-----------|
| term | what it means in this project |

## Key Workflows

1. **[Workflow name]**: [step-by-step description]
```

### Rules for CODEBASE.md

- **Accuracy over completeness**: Only include what the subagents actually found. Do not speculate.
- **Concise entries**: Favor tables and bullet points over paragraphs.
- **ASCII diagrams**: Use box-drawing characters for architecture visualization. Keep diagrams under 30 lines.
- **Relative paths**: Use paths relative to repo root.
- **No secrets**: Never include actual credentials, tokens, or keys.

## Phase 5: Summary

After writing CODEBASE.md, print a summary:

```
## Bootstrap Complete

- **Project**: [name]
- **Language**: [primary language]
- **Architecture**: [style]
- **Files analyzed**: ~[count]
- **Documentation written**: CODEBASE.md ([line count] lines)
- **Subagents used**: 10 (parallel)

### Quick Stats
- Dependencies: X runtime, Y dev
- API endpoints: Z
- Test coverage: [level]
- Documentation status: [rating]
```

## When to Use

- Onboarding onto a new codebase
- Starting a major refactoring effort
- Preparing for an architecture review
- Creating documentation for a previously undocumented project
- Understanding an inherited or open-source project
