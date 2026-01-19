---
allowed-tools: Bash(git:*)
description: Sync current branch with main/master (fetch, rebase or merge)
argument-hint: [merge|rebase] (default: rebase)
---

## Context

- Current branch: !`git branch --show-current`
- Default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"`
- Uncommitted changes: !`git status --porcelain`
- Commits ahead/behind: !`git rev-list --left-right --count origin/$(git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main")...HEAD 2>/dev/null || echo "unknown"`
- Current remote: !`git remote -v | head -2`

## Task

Safely sync the current branch with **origin/main** (always use remote, never local):

### Pre-flight

1. **ALWAYS fetch first**: `git fetch origin` - This is mandatory to get latest remote state

### Main Workflow

1. Check for uncommitted changes - if any, stash them:
   ```bash
   git stash push -m "WIP before sync"
   ```

2. Fetch the latest from origin:
   ```bash
   git fetch origin
   ```

3. Based on argument (default: rebase):
   - **rebase** (recommended - keeps clean history):
     ```bash
     git rebase origin/main
     ```
   - **merge** (if rebase causes issues):
     ```bash
     git merge origin/main
     ```

4. Handle conflicts:
   - If conflicts occur, report them clearly with file list
   - Provide instructions: resolve conflicts, then `git rebase --continue` or `git merge --continue`
   - Do NOT automatically abort

5. If changes were stashed, pop them:
   ```bash
   git stash pop
   ```

6. Report sync status:
   - Number of new commits from main
   - Any conflicts that need resolution
   - Whether force-push is needed (after rebase)

### After Rebase

If rebase was performed and branch was already pushed:
```bash
git push --force-with-lease
```
This is safe because `--force-with-lease` prevents overwriting others' work.

### Why This Matters

- Using `origin/main` instead of local `main` ensures you always sync with the actual remote state
- Prevents "commits from other branches" appearing in PRs
- Reduces merge conflicts in PRs

Strategy: $ARGUMENTS
