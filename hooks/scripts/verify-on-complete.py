#!/usr/bin/env python3
"""
Stop hook - Auto-verification when Claude completes a task.
Runs quick validation checks and reports results.
Triggered by: Stop event

This hook checks:
1. If there are uncommitted changes
2. If tests pass (if test command is available)
3. If lint passes (if lint command is available)

Exit codes:
- 0: Allow (verification passed or skipped)
- Non-zero exits are caught and logged, never block
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], timeout: int = 30) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "Command not found"
    except Exception as e:
        return False, str(e)


def detect_package_manager() -> str | None:
    """Detect which package manager is used in the project."""
    cwd = Path(os.getcwd())

    if (cwd / "bun.lockb").exists():
        return "bun"
    if (cwd / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (cwd / "yarn.lock").exists():
        return "yarn"
    if (cwd / "package-lock.json").exists():
        return "npm"
    if (cwd / "package.json").exists():
        return "npm"
    return None


def get_test_command() -> list[str] | None:
    """Get the test command for this project."""
    cwd = Path(os.getcwd())

    # Check package.json for test script
    package_json = cwd / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                pkg = json.load(f)
            if pkg.get("scripts", {}).get("test"):
                pm = detect_package_manager() or "npm"
                return [pm, "test"]
        except Exception:
            pass

    # Python projects
    if (cwd / "pytest.ini").exists() or (cwd / "pyproject.toml").exists():
        return ["pytest", "--tb=no", "-q"]

    # Go projects
    if (cwd / "go.mod").exists():
        return ["go", "test", "./..."]

    # Rust projects
    if (cwd / "Cargo.toml").exists():
        return ["cargo", "test", "--quiet"]

    return None


def get_lint_command() -> list[str] | None:
    """Get the lint command for this project."""
    cwd = Path(os.getcwd())

    # Check package.json for lint script
    package_json = cwd / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                pkg = json.load(f)
            if pkg.get("scripts", {}).get("lint"):
                pm = detect_package_manager() or "npm"
                return [pm, "run", "lint"]
        except Exception:
            pass

    # Python - check for ruff or flake8
    if (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists():
        success, _ = run_command(["which", "ruff"])
        if success:
            return ["ruff", "check", "."]

    return None


def check_git_status() -> tuple[bool, str]:
    """Check if there are uncommitted changes."""
    success, output = run_command(["git", "status", "--porcelain"])
    if not success:
        return True, "Not a git repository"

    if output.strip():
        lines = output.strip().split("\n")
        return False, f"{len(lines)} uncommitted change(s)"
    return True, "Working tree clean"


def send_notification(title: str, message: str, is_error: bool = False):
    """Send a desktop notification with verification results."""
    sound = "Basso" if is_error else "Ping"

    # macOS
    if sys.platform == "darwin":
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)
    # Linux - only if notify-send is available (not present in WSL/headless)
    elif sys.platform.startswith("linux"):
        if shutil.which("notify-send"):
            urgency = "critical" if is_error else "normal"
            subprocess.run(
                ["notify-send", title, message, f"--urgency={urgency}"],
                capture_output=True,
            )


def main():
    """Run verification checks on task completion."""
    results = []
    has_failures = False

    # 1. Check git status
    git_ok, git_msg = check_git_status()
    results.append(f"{'✓' if git_ok else '!'} Git: {git_msg}")

    # 2. Run tests if available (with short timeout)
    test_cmd = get_test_command()
    if test_cmd:
        test_ok, test_output = run_command(test_cmd, timeout=60)
        if test_ok:
            results.append("✓ Tests: passed")
        else:
            results.append("✗ Tests: failed")
            has_failures = True

    # 3. Run lint if available (quick check)
    lint_cmd = get_lint_command()
    if lint_cmd:
        lint_ok, lint_output = run_command(lint_cmd, timeout=30)
        if lint_ok:
            results.append("✓ Lint: passed")
        else:
            results.append("⚠ Lint: issues found")
            # Lint warnings don't count as failures

    # Send notification with results
    if results:
        summary = "\n".join(results)
        title = "Claude Code - Verification"
        if has_failures:
            send_notification(title, "⚠️ Some checks failed", is_error=True)
        else:
            send_notification(title, "✓ All checks passed", is_error=False)

        # Also print to stderr for logging (won't affect tool output)
        print(f"\n[Verification Results]\n{summary}\n", file=sys.stderr)

    # Always exit 0 - verification should never block
    sys.exit(0)


if __name__ == "__main__":
    main()
