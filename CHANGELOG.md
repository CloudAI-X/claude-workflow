# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-07

### Added

- **Parallel Execution Support**
  - Orchestrator can now spawn N subagents simultaneously for N independent tasks
  - Uses `run_in_background: true` with Task tool for concurrent execution
  - Results collected via TaskOutput after all agents complete
  - Roughly Nx faster than sequential execution

- **New Commands**
  - `/project-starter:parallel-review` - Review multiple directories in parallel
  - `/project-starter:parallel-analyze` - Analyze code from architecture, security, performance, and testing perspectives simultaneously

- **New Skill**
  - `parallel-execution` - Patterns for spawning dynamic subagents, best practices for parallelization, and TodoWrite integration

### Changed

- Updated orchestrator agent with Parallel Execution Protocol section
- Enhanced verify-changes command with explicit parallel syntax
- Added parallel execution examples and diagrams to documentation

---

## [1.0.0] - 2025-01-01

### Added

- **7 Specialized Agents**
  - `orchestrator` - Coordinate complex multi-step tasks
  - `code-reviewer` - Review code quality and best practices
  - `debugger` - Systematic bug investigation and fixing
  - `docs-writer` - Create technical documentation
  - `security-auditor` - Security vulnerability detection
  - `refactorer` - Code structure improvements
  - `test-architect` - Design comprehensive test strategies

- **6 Knowledge Skills**
  - `project-analysis` - Understand any codebase structure and patterns
  - `testing-strategy` - Design test approaches (unit, integration, E2E)
  - `architecture-patterns` - System design guidance
  - `performance-optimization` - Speed up applications, identify bottlenecks
  - `git-workflow` - Version control best practices
  - `api-design` - REST/GraphQL API patterns

- **4 Output Styles**
  - `/project-starter:architect` - System design mode
  - `/project-starter:rapid` - Fast development mode
  - `/project-starter:mentor` - Learning/teaching mode
  - `/project-starter:review` - Code review mode

- **8 Automation Hooks**
  - Security scan (blocks commits with potential secrets)
  - File protection (blocks edits to lock files, .env, .git)
  - Auto-format (runs prettier/black/gofmt based on file type)
  - Command logging (logs to `.claude/command-history.log`)
  - Environment check (validates Node.js, Python, Git)
  - Prompt analysis (suggests appropriate agents)
  - Input notification (desktop notification when input needed)
  - Complete notification (desktop notification when task finishes)

- Cross-platform notification support (macOS, Linux, Windows)
- Comprehensive documentation (README, PERMISSIONS, MCP servers guide)
- MIT License

[1.0.0]: https://github.com/CloudAI-X/claude-workflow/releases/tag/v1.0.0
