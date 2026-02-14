# Verification Guide

How to verify the comprehensive code review workflow works correctly.

## Quick Verification Checklist

After running the workflow, verify:

- [ ] Orchestrator agent activated (look for "orchestrator agent activated")
- [ ] Todo list was created with review steps
- [ ] At least 3 specialist agents were spawned
- [ ] Each agent produced a report
- [ ] Final summary synthesized all findings
- [ ] Exit code was 0 (no errors)

## Prerequisites Check

Before testing, ensure:

```bash
# Plugin is loaded
claude --plugin-dir /path/to/claude-workflow

# Check plugin status
/plugin
# Look for "project-starter" in the Installed tab
```

## Test Procedure

### 1. Simple Test (2 minutes)

Run this minimal prompt:

```
Review this file for quality issues: README.md
```

**Expected:**

- code-reviewer agent activates
- Provides feedback on the README

### 2. Full Workflow Test (10 minutes)

Run the full comprehensive review:

```
Review the hooks directory comprehensively.
Check code quality, security, and documentation.
```

**Expected:**

- Orchestrator creates a plan
- Multiple agents activate in sequence
- Final summary is provided

### 3. Verification Prompts

Ask these follow-up questions to verify agent delegation:

```
> Which agents did you use for this review?
```

Expected answer mentions: orchestrator, code-reviewer, and possibly security-auditor, docs-writer.

```
> Show me the todo list you created
```

Expected: A structured list of review tasks.

## Common Issues

### Agent Not Activating

**Symptom:** Orchestrator doesn't spawn specialist agents.

**Causes:**

- Task tool not available to orchestrator
- Agent files not in correct location
- Plugin not properly loaded

**Fix:**

```bash
# Verify plugin structure
ls agents/
# Should show: orchestrator.md, code-reviewer.md, etc.

# Reload plugin
/plugin reload
```

### No Output from Agent

**Symptom:** Agent activates but produces no output.

**Causes:**

- Model quota exceeded
- Network timeout
- Invalid agent configuration

**Fix:**

- Check Claude Code logs for errors
- Try a simpler prompt
- Verify agent .md file has valid frontmatter

### Workflow Incomplete

**Symptom:** Review stops partway through.

**Causes:**

- Context limit reached
- User interrupted
- Error in one agent

**Fix:**

- Ask: "Continue the review from where you left off"
- Or: "Complete the remaining review tasks"

## Sample Test Output

When working correctly, you should see output similar to:

```
[orchestrator agent activated]

I'll coordinate a comprehensive review of hooks.

Creating review plan...

Todo List:
1. [x] Understand the codebase structure
2. [ ] Run code quality review
3. [ ] Run security audit
4. [ ] Check documentation

Starting code quality review...

[code-reviewer agent activated]

Reviewing 4 Python files in hooks/...

## Code Review Findings

### verify-on-complete.py
✓ Good error handling with try/except
✓ Follows project conventions
⚠ Consider adding type hints to helper functions

### format-on-edit.py
✓ Clean implementation
⚠ Magic strings could be constants

[... more output ...]

[orchestrator]: Code review complete. Starting security audit...

[security-auditor agent activated]

[... continues ...]
```

## Reporting Issues

If the workflow doesn't work as expected:

1. Note the exact prompt used
2. Copy the full output
3. Check for error messages
4. Report at: https://github.com/CloudAI-X/claude-workflow-v2/issues
