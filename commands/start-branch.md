---
allowed-tools: Bash(git:*), mcp__linear__get_issue
description: Start a new branch from origin/main for a Linear ticket or custom name
argument-hint: <LINEAR-ISSUE-ID or branch-name>
---

## Context

- Current branch: !`git branch --show-current`
- Uncommitted changes: !`git status --porcelain`
- Current remote: !`git remote -v | head -2`
- Local branches: !`git branch --list | head -10`

## Task

Create a new branch with a **clean history** starting from `origin/main`.

**CRITICAL RULES:**
1. ALWAYS start from `origin/main`, never local main
2. ALWAYS fetch before creating the branch
3. For Linear tickets, use the Linear-generated branch name

### Workflow

1. **Stash uncommitted changes** (if any):
   ```bash
   git stash push -m "WIP before starting new branch"
   ```

2. **Fetch latest from origin** (MANDATORY):
   ```bash
   git fetch origin
   ```

3. **Determine branch name**:
   - If argument is a Linear issue ID (e.g., `ENG-123`, `DAT-456`):
     - Fetch the issue from Linear using `mcp__linear__get_issue`
     - Use the `branchName` field from the issue (e.g., `daweido/eng-123-add-feature`)
   - If argument is a custom branch name:
     - Use it directly
   - If no argument provided:
     - Ask user for Linear issue ID or branch name

4. **Check if branch already exists**:
   ```bash
   git branch --list <branch-name>
   git ls-remote --heads origin <branch-name>
   ```
   - If exists locally: ask to switch or create new
   - If exists on remote: checkout and track it

5. **Create branch from origin/main**:
   ```bash
   git checkout -b <branch-name> origin/main
   ```

6. **Pop stashed changes** (if any):
   ```bash
   git stash pop
   ```

7. **Report success**:
   - Branch name created
   - Starting point (commit hash of origin/main)
   - Any stashed changes restored

### Handling Dependencies

If user mentions this work depends on another unmerged branch:

**Warn them:**
> ⚠️ Starting from another unmerged branch will include its commits in your PR.
>
> **Recommended:** Wait for the dependent branch to be merged to main first.
>
> **If you must proceed:** After the dependent branch merges, run `/sync-branch` to rebase onto main.

Then ask:
1. Wait and start from origin/main (recommended)
2. Start from the dependent branch (will need rebase later)

### Why origin/main?

- Local `main` may be stale (not pulled recently)
- Starting from stale main causes:
  - PR conflicts with main
  - Extra commits appearing in PR
  - Messy git history
- `origin/main` is always the source of truth

$ARGUMENTS
