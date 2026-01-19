---
name: managing-git
description: Manages Git workflows including branching, commits, and pull requests. Use when working with Git, creating commits, opening PRs, managing branches, resolving conflicts, or when asked about version control best practices.
---

# Managing Git

## Feature Development Workflow

Copy this checklist and track progress:

```
Feature Development Progress:
- [ ] Step 1: Create feature branch from main
- [ ] Step 2: Make changes with atomic commits
- [ ] Step 3: Rebase on latest main
- [ ] Step 4: Push and create PR
- [ ] Step 5: Address review feedback
- [ ] Step 6: Merge after approval
```

## Branching Strategies

### GitHub Flow (Recommended for most projects)
```
main ──●────●────●────●────●── (always deployable)
        \          /
feature  └──●──●──┘
```
- `main` is always deployable
- Feature branches from main
- PR + review + merge
- Deploy after merge

### Git Flow (For release-based projects)
```
main     ──●─────────────●────── (releases only)
            \           /
release      └────●────┘
                 /
develop  ──●──●────●──●──●──
            \     /
feature      └──●┘
```

## Commit Conventions

### Conventional Commits Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Build process, dependencies |
| `ci` | CI configuration |

### Examples
```bash
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth providers.
Closes #123

BREAKING CHANGE: Session tokens now expire after 24h
```

```bash
fix(api): handle null response from payment gateway

Previously caused 500 error when gateway returned null.
Now returns appropriate error message to user.
```

## Branch Naming
```
<type>/<ticket-id>-<short-description>

# Examples
feature/AUTH-123-oauth-login
fix/BUG-456-null-pointer
chore/TECH-789-upgrade-deps
```

## Pull Request Workflow

Copy this checklist when creating PRs:

```
PR Checklist:
- [ ] Code follows project conventions
- [ ] Tests added/updated for changes
- [ ] All tests pass locally
- [ ] No merge conflicts with main
- [ ] Documentation updated if needed
- [ ] No security vulnerabilities introduced
- [ ] PR description explains the "why"
```

### PR Template
```markdown
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] E2E tests pass

## Screenshots (if UI changes)
[Before/After screenshots]
```

### PR Size Guidelines
| Size | Lines Changed | Review Guidance |
|------|---------------|-----------------|
| XS | < 50 | Quick review |
| S | 50-200 | Standard review |
| M | 200-500 | Thorough review |
| L | 500+ | Split if possible |

## Common Git Commands

### Daily Workflow

**CRITICAL: Always start branches from `origin/main`, not local `main`**

This prevents:
- PRs containing commits from other branches
- Merge conflicts due to stale local main
- Messy PR history

```bash
# ================================================================
# START NEW FEATURE (Always from origin/main!)
# ================================================================

# Step 1: Fetch latest from origin (REQUIRED)
git fetch origin

# Step 2: Create branch directly from origin/main
# Use the Linear-generated branch name from the ticket
git checkout -b daweido/eng-123-add-feature origin/main

# WRONG ✗ - Don't do this! Local main may be stale
# git checkout main && git pull && git checkout -b branch-name

# ================================================================
# IF YOU HAVE UNCOMMITTED CHANGES
# ================================================================
git stash push -m "WIP"
git fetch origin
git checkout -b daweido/eng-123-add-feature origin/main
git stash pop

# ================================================================
# COMMIT CHANGES
# ================================================================
git add -p  # Stage interactively
git commit -m "feat(scope): description"

# ================================================================
# BEFORE PUSHING: Sync with main to avoid conflicts
# ================================================================
git fetch origin
git rebase origin/main
# If conflicts: resolve, then `git rebase --continue`

# ================================================================
# PUSH AND CREATE PR
# ================================================================
git push -u origin HEAD
gh pr create --fill
```

### Branch Dependencies (When Feature B Depends on Feature A)

**Option 1: Wait for merge (Recommended)**
```bash
# Wait for feature-a to be merged, then start fresh
git fetch origin
git checkout -b daweido/eng-456-feature-b origin/main
```

**Option 2: Branch from unmerged branch (Creates messy history)**
```bash
# This WILL include feature-a commits in feature-b PR
# After feature-a merges, you MUST rebase feature-b:
git fetch origin
git rebase origin/main
git push --force-with-lease
```

### Fixing Mistakes
```bash
# Amend last commit (before push)
git commit --amend

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a pushed commit
git revert <commit-hash>

# Interactive rebase to clean up
git rebase -i HEAD~3
```

### Advanced Operations
```bash
# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Find which commit broke something
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>

# Stash with message
git stash push -m "WIP: feature description"
git stash list
git stash pop
```

## Commit Validation

Before pushing, validate commits:

```
Commit Validation:
- [ ] Each commit has a clear, descriptive message
- [ ] Commit type matches the change (feat, fix, etc.)
- [ ] No WIP or temporary commits
- [ ] No secrets or credentials committed
- [ ] Changes are atomic (one logical change per commit)
```

If validation fails, use `git rebase -i` to clean up commit history before pushing.
