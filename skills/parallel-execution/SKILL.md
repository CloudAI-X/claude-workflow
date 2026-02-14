---
name: parallel-execution
description: Patterns for parallel subagent execution using Task tool with run_in_background. Use when coordinating multiple independent tasks, spawning dynamic subagents, or implementing features that can be parallelized.
---

# Parallel Execution Patterns

### When to Load

- **Trigger**: Multi-agent tasks, concurrent operations, spawning subagents, parallelizing independent work
- **Skip**: Single-step tasks or sequential workflows with no parallelization opportunity

## Core Concept

Parallel execution spawns multiple subagents simultaneously using the Task tool with `run_in_background: true`. This enables N tasks to run concurrently, dramatically reducing total execution time.

**Critical Rule**: ALL Task calls MUST be in a SINGLE assistant message for true parallelism. If Task calls are in separate messages, they run sequentially.

## Execution Protocol

### Step 1: Identify Parallelizable Tasks

Before spawning, verify tasks are independent:

- No task depends on another's output
- Tasks target different files or concerns
- Can run simultaneously without conflicts

### Step 2: Prepare Dynamic Subagent Prompts

Each subagent receives a custom prompt defining its role:

```
You are a [ROLE] specialist for this specific task.

Task: [CLEAR DESCRIPTION]

Context:
[RELEVANT CONTEXT ABOUT THE CODEBASE/PROJECT]

Files to work with:
[SPECIFIC FILES OR PATTERNS]

Output format:
[EXPECTED OUTPUT STRUCTURE]

Focus areas:
- [PRIORITY 1]
- [PRIORITY 2]
```

### Step 3: Launch All Tasks in ONE Message

**CRITICAL**: Make ALL Task calls in the SAME assistant message:

```
I'm launching N parallel subagents:

[Task 1]
description: "Subagent A - [brief purpose]"
prompt: "[detailed instructions for subagent A]"
run_in_background: true

[Task 2]
description: "Subagent B - [brief purpose]"
prompt: "[detailed instructions for subagent B]"
run_in_background: true

[Task 3]
description: "Subagent C - [brief purpose]"
prompt: "[detailed instructions for subagent C]"
run_in_background: true
```

### Step 4: Retrieve Results with TaskOutput

After launching, retrieve each result:

```
[Wait for completion, then retrieve]

TaskOutput: task_1_id
TaskOutput: task_2_id
TaskOutput: task_3_id
```

### Step 5: Synthesize Results

Combine all subagent outputs into unified result:

- Merge related findings
- Resolve conflicts between recommendations
- Prioritize by severity/importance
- Create actionable summary

## Dynamic Subagent Patterns

### Pattern 1: Task-Based Parallelization

When you have N tasks to implement, spawn N subagents:

```
Plan:
1. Implement auth module
2. Create API endpoints
3. Add database schema
4. Write unit tests
5. Update documentation

Spawn 5 subagents (one per task):
- Subagent 1: Implements auth module
- Subagent 2: Creates API endpoints
- Subagent 3: Adds database schema
- Subagent 4: Writes unit tests
- Subagent 5: Updates documentation
```

### Pattern 2: Directory-Based Parallelization

Analyze multiple directories simultaneously:

```
Directories: src/auth, src/api, src/db

Spawn 3 subagents:
- Subagent 1: Analyzes src/auth
- Subagent 2: Analyzes src/api
- Subagent 3: Analyzes src/db
```

### Pattern 3: Perspective-Based Parallelization

Review from multiple angles simultaneously:

```
Perspectives: Security, Performance, Testing, Architecture

Spawn 4 subagents:
- Subagent 1: Security review
- Subagent 2: Performance analysis
- Subagent 3: Test coverage review
- Subagent 4: Architecture assessment
```

## TodoWrite Integration

When using parallel execution, TodoWrite behavior differs:

**Sequential execution**: Only ONE task `in_progress` at a time
**Parallel execution**: MULTIPLE tasks can be `in_progress` simultaneously

```
# Before launching parallel tasks
todos = [
  { content: "Task A", status: "in_progress" },
  { content: "Task B", status: "in_progress" },
  { content: "Task C", status: "in_progress" },
  { content: "Synthesize results", status: "pending" }
]

# After each TaskOutput retrieval, mark as completed
todos = [
  { content: "Task A", status: "completed" },
  { content: "Task B", status: "completed" },
  { content: "Task C", status: "completed" },
  { content: "Synthesize results", status: "in_progress" }
]
```

## When to Use Parallel Execution

**Good candidates:**

- Multiple independent analyses (code review, security, tests)
- Multi-file processing where files are independent
- Exploratory tasks with different perspectives
- Verification tasks with different checks
- Feature implementation with independent components

**Avoid parallelization when:**

- Tasks have dependencies (Task B needs Task A's output)
- Sequential workflows are required (commit -> push -> PR)
- Tasks modify the same files (risk of conflicts)
- Order matters for correctness

## Performance Benefits

| Approach   | 5 Tasks @ 30s each          | Total Time |
| ---------- | --------------------------- | ---------- |
| Sequential | 30s + 30s + 30s + 30s + 30s | ~150s      |
| Parallel   | All 5 run simultaneously    | ~30s       |

Parallel execution is approximately Nx faster where N is the number of independent tasks.

## Example: Feature Implementation

**User request**: "Implement user authentication with login, registration, and password reset"

**Orchestrator creates plan**:

1. Implement login endpoint
2. Implement registration endpoint
3. Implement password reset endpoint
4. Add authentication middleware
5. Write integration tests

**Parallel execution**:

```
Launching 5 subagents in parallel:

[Task 1] Login endpoint implementation
[Task 2] Registration endpoint implementation
[Task 3] Password reset endpoint implementation
[Task 4] Auth middleware implementation
[Task 5] Integration test writing

All tasks run simultaneously...

[Collect results via TaskOutput]

[Synthesize into cohesive implementation]
```

## Troubleshooting

**Tasks running sequentially?**

- Verify ALL Task calls are in SINGLE message
- Check `run_in_background: true` is set for each

**Results not available?**

- Use TaskOutput with correct task IDs
- Wait for tasks to complete before retrieving

**Conflicts in output?**

- Ensure tasks don't modify same files
- Add conflict resolution in synthesis step
