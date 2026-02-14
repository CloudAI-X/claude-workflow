---
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(pip:*), Bash(uv:*), Bash(python:*), Bash(cargo:*), Bash(go:*), Read, Edit, WebFetch
description: Safe, one-at-a-time dependency upgrades with verification after each. Detects package manager automatically.
argument-hint: [specific package name, or blank for all outdated]
---

# Dependency Upgrade

Safely upgrade dependencies one at a time with testing between each upgrade.

## Context

- Package manager detection: !`ls package-lock.json 2>/dev/null && echo "npm" || ls yarn.lock 2>/dev/null && echo "yarn" || ls pnpm-lock.yaml 2>/dev/null && echo "pnpm" || ls bun.lockb 2>/dev/null && echo "bun" || ls Cargo.toml 2>/dev/null && echo "cargo" || ls go.mod 2>/dev/null && echo "go" || ls requirements.txt pyproject.toml 2>/dev/null && echo "pip/uv" || echo "Unknown"`
- Current branch: !`git branch --show-current`
- Working tree status: !`git status --short`
- Node version (if applicable): !`node --version 2>/dev/null || echo "N/A"`
- Python version (if applicable): !`python3 --version 2>/dev/null || echo "N/A"`

## Workflow

### Phase 1: Detect Environment

1. Identify the package manager from context above
2. Confirm a clean working tree (stash or commit uncommitted changes first)
3. Ensure tests pass BEFORE any upgrades — this is the baseline:
   - Node.js: `npm test` / `yarn test` / `pnpm test` / `bun test`
   - Python: `pytest` / `python -m pytest`
   - Rust: `cargo test`
   - Go: `go test ./...`
4. If baseline tests fail, STOP and report — do not upgrade on a broken baseline

### Phase 2: List Outdated Dependencies

Run the appropriate outdated command:

- npm: `npm outdated --json`
- yarn: `yarn outdated`
- pnpm: `pnpm outdated`
- bun: `bun outdated`
- pip/uv: `uv pip list --outdated` or `pip list --outdated --format=json`
- cargo: `cargo outdated` (if installed) or check Cargo.toml
- go: `go list -m -u all`

### Phase 3: Categorize Updates

Sort dependencies into risk categories:

```
## Outdated Dependencies

### Patch Updates (safe — bug fixes only)
| Package | Current | Latest | Notes |
|---------|---------|--------|-------|
| ...     | ...     | ...    | ...   |

### Minor Updates (review — new features, possible deprecations)
| Package | Current | Latest | Notes |
|---------|---------|--------|-------|
| ...     | ...     | ...    | ...   |

### Major Updates (careful — breaking changes expected)
| Package | Current | Latest | Notes |
|---------|---------|--------|-------|
| ...     | ...     | ...    | ...   |
```

If `$ARGUMENTS` specifies a package, focus only on that package.

### Phase 4: Upgrade One at a Time

Process in this order: patches first, then minors, then majors.

For EACH dependency:

1. **Announce** which package is being upgraded and from/to versions
2. **Check changelog/release notes** for breaking changes:
   - Look at the package's GitHub releases or CHANGELOG
   - For major upgrades, summarize breaking changes before proceeding
3. **Upgrade** the single package:
   - npm: `npm install package@latest`
   - yarn: `yarn upgrade package@latest`
   - pnpm: `pnpm update package@latest`
   - bun: `bun update package`
   - pip/uv: `uv add package@latest` or `uv pip install --upgrade package`
   - cargo: update version in Cargo.toml, then `cargo update -p package`
   - go: `go get package@latest && go mod tidy`
4. **Run tests** immediately
5. **If tests PASS:**
   - Commit: `chore(deps): upgrade [package] from [old] to [new]`
   - Continue to next package
6. **If tests FAIL:**
   - Revert: `git checkout -- .` and restore lockfile
   - Record the failure reason
   - If it is a minor/patch with failing tests, flag as unexpected
   - Move to the next package

### Phase 5: Summary Report

```
## Dependency Upgrade Report

### Successfully Upgraded
| Package | From | To | Type |
|---------|------|----|------|
| ...     | ...  | ...| patch/minor/major |

### Failed (Reverted)
| Package | From | To | Failure Reason |
|---------|------|----|----------------|
| ...     | ...  | ...| ...            |

### Skipped
| Package | From | To | Reason |
|---------|------|----|--------|
| ...     | ...  | ...| ...    |

### Test Results
- Baseline: [pass/fail]
- Final: [pass/fail]
- Total upgrades attempted: [count]
- Successful: [count]
- Reverted: [count]
```

## Target

$ARGUMENTS

If no target specified, process all outdated dependencies in order of risk (patches first).
