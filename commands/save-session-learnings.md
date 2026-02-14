---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*)
description: Document session learnings to CLAUDE.md and AGENTS.md. Use after completing significant tasks, debugging sessions, or discovering project patterns.
---

# Save Session Learnings

Capture and persist significant discoveries from this session into project documentation so knowledge survives across sessions and agents.

## Phase 1: Gather Session Context

Collect evidence of what was learned during this session:

```bash
git diff HEAD~5 --stat
git log --oneline -10
git diff --name-only HEAD~5
```

Also review the conversation history for:

- Bugs that were debugged (root cause + fix)
- Architecture decisions made
- Configuration or environment discoveries
- Patterns established or followed
- Commands that worked (or failed)
- Gotchas and edge cases encountered

## Phase 2: Categorize Learnings

Sort each finding into one of these categories:

### Architecture

- Key files, folders, data flow, component relationships
- Service boundaries, module dependencies

### Patterns

- Naming conventions, code style, recurring design patterns
- File structure conventions, import ordering

### Gotchas

- Things that break, common errors, non-obvious behavior
- Workarounds for known issues

### Commands

- Build, test, deploy, dev server commands that work
- Tool-specific invocations with correct flags

### Decisions

- Why something was done a certain way
- Trade-offs considered, alternatives rejected

## Phase 3: Check Existing Documentation

Before writing, read both files to avoid duplicating entries:

1. Use Glob to check if `CLAUDE.md` and `AGENTS.md` exist in the project root
2. If they exist, Read them fully
3. Compare gathered learnings against existing entries
4. Skip anything already documented
5. If existing entries are outdated, update them instead of adding duplicates

## Phase 4: Write Learnings

Update both `CLAUDE.md` and `AGENTS.md` in the project root (create if missing).

### Format for New Entries

Append to the `## Session Log` section (create it if absent). Use this format:

```markdown
## Session Log

- YYYY-MM-DD: [Category] Brief, actionable description of what was learned
```

For structured learnings, append to the relevant section (`### Gotchas`, `### Patterns`, etc.) or create the section if it does not exist:

```markdown
### Gotchas

- `short description` -- explanation of the issue and the workaround

### Patterns

- Pattern name -- where it applies and why

### Commands

- `command here` -- what it does, when to use it
```

### Rules

- **Concise**: Each entry should be 1-2 lines max. Favor telegraphic style.
- **Actionable**: Write entries that help a future developer take action, not just understand history.
- **No duplicates**: If the learning is already documented, skip it or update the existing entry.
- **Date stamp**: Always include today's date in Session Log entries.
- **Both files**: CLAUDE.md and AGENTS.md must contain the same learnings. Keep them in sync.
- **Preserve existing content**: Never overwrite or remove existing entries. Only append or update.

## Phase 5: Confirm

After writing, summarize what was added:

```
## Learnings Saved

- **New entries added**: X
- **Existing entries updated**: Y
- **Skipped (already documented)**: Z

### Added
1. [Category] Description
2. [Category] Description

### Updated
1. [What changed and why]
```

## When to Use

- After completing a significant feature or bug fix
- After a long debugging session
- After discovering non-obvious project behavior
- After setting up a new tool or integration
- Before ending a session where important context was built up
- When you realize "a future me would want to know this"
