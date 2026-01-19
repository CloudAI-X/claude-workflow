---
allowed-tools: Bash(git:*), Bash(gh:*)
description: Commit staged changes, push to remote, and create a pull request
argument-hint: [optional PR title or description hint]
---

## Context

- Current branch: !`git branch --show-current`
- Default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5 || echo "main"`
- Git status: !`git status --short`
- Staged diff: !`git diff --cached`
- Unstaged diff: !`git diff`
- Commits ahead of origin: !`git log @{u}..HEAD --oneline 2>/dev/null || echo "No upstream branch"`
- Recent commits for style: !`git log --oneline -5`
- Local vs origin/main divergence: !`git fetch origin && git rev-list --left-right --count origin/main...HEAD 2>/dev/null || echo "unknown"`

## Task

Execute the full git workflow with **clean branch history**:

### Pre-flight Check

1. **Fetch latest**: Always run `git fetch origin` first to ensure we have the latest remote state

2. **Branch validation**: Check if current branch is already based on latest `origin/main`:
   - Run: `git merge-base --is-ancestor origin/main HEAD`
   - If this fails, the branch is NOT based on latest main → warn the user

### If on main/master branch (need to create new branch)

**CRITICAL: Always start from origin/main, never local main**

1. Stash any uncommitted changes: `git stash push -m "WIP before branch"`
2. Fetch latest: `git fetch origin`
3. Create branch from origin/main: `git checkout -b <branch-name> origin/main`
   - **For Linear tickets**: Use the Linear-generated branch name (found in ticket details under "Copy git branch name")
     - Example: `daweido/eng-123-add-user-authentication`
   - **Without Linear**: Use format `<type>/<ticket-id>-<description>`
   - Ask user for branch name or Linear ticket ID if not provided
4. Pop stash if needed: `git stash pop`

### If on feature branch

1. **Check branch base**: Verify branch started from main:
   ```bash
   git merge-base origin/main HEAD
   ```

2. **Check for divergence**: If branch has diverged significantly from main:
   - Count commits behind: `git rev-list --count HEAD..origin/main`
   - If >10 commits behind, recommend syncing first: `/sync-branch`

3. **Check for unmerged dependencies**:
   - If this branch depends on another unmerged branch, warn the user:
     - Option A: "The dependent branch should be merged to main first"
     - Option B: "Create this branch from the dependent branch (will inherit its commits)"
   - This causes the "commits from other branches in PR" problem

### Main Workflow

1. **Commit**: If there are staged changes, create a conventional commit
   - Follow conventional commits: `type(scope): description`
   - Types: feat, fix, docs, style, refactor, perf, test, chore

2. **Rebase on origin/main** (recommended before push):
   ```bash
   git fetch origin
   git rebase origin/main
   ```
   - If conflicts, report and stop

3. **Push**: Push the current branch to origin
   - For new branches: `git push -u origin HEAD`
   - For existing branches: `git push` (or `git push --force-with-lease` after rebase)

4. **PR**: Create a pull request using `gh pr create`
   - Base branch: always target the default branch (main/master)
   - Auto-generate title from commits
   - Include a summary of changes in the PR body
   - Link any related issues mentioned in commits

### Error Handling

- **Conflicts during rebase**: Stop and report. User must resolve manually.
- **Diverged from main**: Recommend `/sync-branch` before continuing.
- **Branch already has PR**: Just push (PR updates automatically).

If any step fails, stop and report the issue clearly.

$ARGUMENTS
