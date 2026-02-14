---
allowed-tools: Read, Bash, Glob
description: View agent performance metrics and session history. Shows usage patterns, files changed, and session summaries.
---

## Context

- Metrics file: !`cat .claude/agent-metrics.jsonl 2>/dev/null || echo "NO_METRICS_FILE"`

## Task

Analyze the agent performance metrics and present a summary.

**If the metrics file does not exist or the context above shows "NO_METRICS_FILE":**
Print exactly: "No metrics recorded yet. Metrics are automatically collected after each session."

**If metrics data exists**, parse each JSON line and present:

1. **Overview**
   - Total sessions logged
   - Sessions in the last 7 days (compare timestamps to now)
   - Average files changed per session

2. **Recent Sessions** (last 10)
   Format as a markdown table:

   | #   | Timestamp (UTC) | Files Changed | Commit | Status |
   | --- | --------------- | ------------- | ------ | ------ |
   - Show the most recent 10 sessions, newest first
   - For "Commit", show the short commit message or "—" if none
   - For "Status", show the duration_hint value

3. **Patterns**
   - Note any trends (e.g., sessions with many file changes, frequency of commits)
   - If there are sessions with 0 files changed, note how many were "no-op" sessions

Keep the output concise and well-formatted.
