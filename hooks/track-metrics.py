#!/usr/bin/env python3
"""
Agent telemetry hook.
Logs session metrics (duration, tools used, task outcome) on Stop event.
Writes to .claude/agent-metrics.jsonl. Informational only.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def run_command(cmd: list[str], timeout: int = 10) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""


def get_files_changed() -> int:
    """Count files changed from git diff --stat HEAD."""
    success, output = run_command(["git", "diff", "--stat", "HEAD"])
    if not success or not output:
        return 0
    # The last line of git diff --stat has the summary like:
    # " 3 files changed, 10 insertions(+), 2 deletions(-)"
    lines = output.strip().split("\n")
    if not lines:
        return 0
    summary_line = lines[-1]
    # Extract the number of files changed
    for part in summary_line.split(","):
        part = part.strip()
        if "file" in part and "changed" in part:
            try:
                return int(part.split()[0])
            except (ValueError, IndexError):
                return 0
    return 0


def get_latest_commit() -> str:
    """Get the latest commit message from git log --oneline -1."""
    success, output = run_command(["git", "log", "--oneline", "-1"])
    if success and output:
        return output
    return ""


def main():
    """Log session metrics on Stop event."""
    try:
        # Read stdin JSON (Stop event data)
        try:
            input_data = json.load(sys.stdin)
        except Exception:
            input_data = {}

        # Build the metrics entry
        timestamp = datetime.now(timezone.utc).isoformat()
        files_changed = get_files_changed()
        latest_commit = get_latest_commit()

        entry = {
            "timestamp": timestamp,
            "files_changed": files_changed,
            "commit": latest_commit if latest_commit else None,
            "duration_hint": "completed",
        }

        # Determine the metrics file path
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
        metrics_dir = os.path.join(project_dir, ".claude")
        metrics_file = os.path.join(metrics_dir, "agent-metrics.jsonl")

        # Ensure .claude/ directory exists
        os.makedirs(metrics_dir, exist_ok=True)

        # Append the JSON line to the metrics file
        with open(metrics_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception:
        pass  # Never block on errors

    sys.exit(0)


if __name__ == "__main__":
    main()
