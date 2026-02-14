---
name: managing-git
description: Manages Git workflows including branching, commits, and pull requests. Use when working with Git, creating commits, opening PRs, managing branches, resolving conflicts, or when asked about version control best practices.
---

# Managing Git

### When to Load

- **Trigger**: Branching strategies, commit workflows, pull requests, merge conflicts, version control questions
- **Skip**: Tasks that do not involve git operations

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

| Type       | Description                                         |
| ---------- | --------------------------------------------------- |
| `feat`     | New feature                                         |
| `fix`      | Bug fix                                             |
| `docs`     | Documentation only                                  |
| `style`    | Formatting, no logic change                         |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `perf`     | Performance improvement                             |
| `test`     | Adding/updating tests                               |
| `chore`    | Build process, dependencies                         |
| `ci`       | CI configuration                                    |

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

| Size | Lines Changed | Review Guidance   |
| ---- | ------------- | ----------------- |
| XS   | < 50          | Quick review      |
| S    | 50-200        | Standard review   |
| M    | 200-500       | Thorough review   |
| L    | 500+          | Split if possible |

## Common Git Commands

### Daily Workflow

```bash
# Start new feature
git checkout main
git pull
git checkout -b feature/TICKET-123-description

# Commit changes
git add -p  # Stage interactively
git commit -m "feat: description"

# Keep up with main
git fetch origin main
git rebase origin/main

# Push and create PR
git push -u origin HEAD
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
