---
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(pytest:*), Bash(python:*), Bash(go:*), Bash(cargo:*), Read, Write, Edit, Glob, Grep
description: Systematic, safety-first refactoring with verification at each step. Never refactors and adds features simultaneously.
argument-hint: [target file, directory, or refactoring description]
---

# Guided Refactoring

Perform safe, incremental refactoring with test verification at every step.

## Context

- Recent changes: !`git diff --name-only HEAD~3 2>/dev/null | head -10 || echo "No recent changes"`
- Current branch: !`git branch --show-current`
- Working tree status: !`git status --short`
- Test framework: !`cat package.json 2>/dev/null | grep -E '"(jest|vitest|mocha)"' | head -1 || ls pytest.ini pyproject.toml 2>/dev/null | head -1 || ls Cargo.toml go.mod 2>/dev/null | head -1 || echo "Unknown"`
- Existing tests: !`find . -name "*test*" -o -name "*spec*" 2>/dev/null | grep -E '\.(ts|tsx|js|jsx|py|go|rs)$' | head -10 || echo "No test files found"`

## Safety Rules (NON-NEGOTIABLE)

1. **NEVER refactor AND add features simultaneously.** Each change is purely structural.
2. **NEVER proceed without passing tests.** If tests fail after a refactoring, revert immediately.
3. **ONE refactoring at a time.** Each commit is a single, atomic refactoring step.
4. **Preserve external behavior.** Inputs and outputs must remain identical.
5. **Ensure clean working tree before starting.** Stash or commit uncommitted changes first.

## Workflow

### Phase 1: Analyze Scope

1. Identify the target file(s) or directory from `$ARGUMENTS`
2. Map all dependencies — files that import/use the target
3. Map all dependents — files that the target imports/uses
4. Assess blast radius: how many files could be affected?
5. Report scope summary before proceeding:
   ```
   ## Refactoring Scope
   - Target: [file/directory]
   - Files affected: [count]
   - Dependencies: [list]
   - Dependents: [list]
   - Risk level: [low/medium/high]
   ```

### Phase 2: Ensure Test Coverage

1. Check if tests exist for the current behavior of the target
2. Run existing tests to confirm they pass (this is your safety net)
3. If test coverage is insufficient:
   - Write tests that capture the current behavior BEFORE refactoring
   - Run them to confirm they pass
   - Commit these tests separately: `test: add coverage for [target] before refactoring`
4. Record baseline test results (pass count, time)

### Phase 3: Refactor Incrementally

For each refactoring step:

1. **Describe** the specific refactoring about to be applied (e.g., "Extract method X from class Y", "Rename variable A to B", "Move function to separate module")
2. **Apply** the single refactoring change
3. **Run tests** immediately after applying
4. **If tests PASS:**
   - Commit with message: `refactor: [specific change description]`
   - Move to next refactoring step
5. **If tests FAIL:**
   - Revert the change: `git checkout -- .`
   - Analyze why it failed
   - Try a different approach or break it into smaller steps
   - Document what went wrong

Common refactoring types (apply as appropriate):

- Extract function/method
- Rename for clarity
- Remove duplication (DRY)
- Simplify conditionals
- Split large files/functions
- Improve type signatures
- Replace magic values with constants
- Consolidate imports

### Phase 4: Summary Report

After all refactoring steps are complete, provide:

```
## Refactoring Summary

### Before
- Files: [count and names]
- Lines of code: [approximate]
- Complexity: [observations]

### After
- Files: [count and names]
- Lines of code: [approximate]
- Complexity: [observations]

### Changes Applied
1. [refactoring 1] - [commit hash]
2. [refactoring 2] - [commit hash]
...

### Reverted Attempts
1. [what was tried] - [why it failed]

### Test Results
- All tests passing: [yes/no]
- Tests added: [count]
- Total test runs: [count]
```

## Target

$ARGUMENTS

If no target specified, analyze the most recently modified files and suggest refactoring opportunities.
