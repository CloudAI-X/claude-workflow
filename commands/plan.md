---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*)
description: Create and maintain a structured PLAN.md for persistent task tracking. Supports phases, dependencies, and progress tracking.
argument-hint: [plan description, "status" to show current plan, or "complete" to mark done]
---

# Persistent Planning

Create, update, and track a structured project plan in PLAN.md.

## Context

- Existing plan: !`cat PLAN.md 2>/dev/null | head -50 || echo "No PLAN.md found"`
- Project structure: !`ls -la 2>/dev/null | head -20`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "No commits"`

## Behavior Based on Arguments

Interpret `$ARGUMENTS` to determine the action:

### If `$ARGUMENTS` is "status" or "show":

- Read PLAN.md and display current progress
- Show completion percentage for each phase
- Highlight the next actionable task
- List any open questions or blockers

### If `$ARGUMENTS` is "complete" or "done":

- Update the current phase to "done"
- If all phases are done, add a completion timestamp
- Summarize what was accomplished

### If PLAN.md already exists and `$ARGUMENTS` is a new task/description:

- Read the existing plan
- Add the new task(s) to the appropriate phase
- Preserve all existing progress (checked items stay checked)
- Update the plan status

### If PLAN.md does NOT exist:

- Create a new PLAN.md with the structure below
- Populate based on `$ARGUMENTS` description
- Set phase to "planning"

## PLAN.md Structure

When creating or updating PLAN.md, use this exact structure:

```markdown
# Project Plan

> Status: **[planning | implementing | verifying | done]**
> Created: [date]
> Last Updated: [date]

## Objective

[Clear, concise statement of what this plan achieves]

## Tasks

### Phase 1: [Phase Name]

- [ ] Task 1.1 — [description]
  - Depends on: [nothing | task X.Y]
- [ ] Task 1.2 — [description]
  - Depends on: Task 1.1
- [x] Task 1.3 — [completed task description]
  - Depends on: nothing
  - Completed: [date]

### Phase 2: [Phase Name]

- [ ] Task 2.1 — [description]
  - Depends on: Phase 1
- [ ] Task 2.2 — [description]
  - Depends on: Task 2.1

### Phase 3: Verification

- [ ] Run all tests
- [ ] Review changes
- [ ] Update documentation

## Architecture Decisions

| Decision   | Options Considered   | Chosen   | Rationale |
| ---------- | -------------------- | -------- | --------- |
| [decision] | [option A, option B] | [chosen] | [why]     |

## Open Questions

- [ ] [Question 1 — what needs to be answered]
- [x] [Question 2 — answered: [answer]]

## Progress Log

| Date   | Update          |
| ------ | --------------- |
| [date] | [what was done] |
```

## Rules for Plan Management

1. **Never delete completed tasks** — mark them with `[x]` and add completion date
2. **Respect dependencies** — do not mark a task complete if its dependencies are incomplete
3. **Add discovered tasks** — when implementation reveals new work, add it to the appropriate phase
4. **Update status** — move through phases: planning -> implementing -> verifying -> done
5. **Log progress** — every significant update gets a Progress Log entry
6. **Keep it current** — the plan should always reflect the true state of work
7. **Track decisions** — any architectural or design decisions go in the Architecture Decisions table
8. **Resolve questions** — when open questions are answered, mark them `[x]` with the answer

## Workflow

1. Check if PLAN.md exists in the project root
2. If it exists, read it fully to understand current state
3. Based on `$ARGUMENTS`, either show status, add tasks, or update progress
4. Write the updated PLAN.md back to disk
5. Display a summary of what changed and what is next

$ARGUMENTS
