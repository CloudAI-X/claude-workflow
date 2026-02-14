#!/usr/bin/env python3
"""
Pre-commit quality check hook.
Detects debug statements, temporary markers, and large file content.
Runs on PreToolUse for Edit|Write operations.
"""
import json
import re
import sys
import os


DEBUG_PATTERNS = [
    (r'\bconsole\.log\s*\(', "console.log", "Remove before commit, or use a proper logger (e.g., winston, pino)"),
    (r'\bconsole\.debug\s*\(', "console.debug", "Remove before commit, or use a proper logger (e.g., winston, pino)"),
    (r'\bdebugger\b', "debugger statement", "Remove before commit — debugger statements pause execution in production"),
    (r'\bbreakpoint\s*\(', "breakpoint()", "Remove before commit — use a conditional breakpoint or logging instead"),
    (r'\bpdb\.set_trace\s*\(', "pdb.set_trace()", "Remove before commit, or use a proper logger (e.g., logging module)"),
]

TEMP_MARKERS = [
    (r'\bFIXME\b', "FIXME", "Address the issue or convert to a tracked GitHub issue"),
    (r'\bHACK\b', "HACK", "Refactor the workaround or document why it is necessary in a comment"),
    (r'\bXXX\b', "XXX", "Resolve the concern or convert to a tracked GitHub issue"),
]

MAX_CONTENT_SIZE = 500 * 1024
SKIP_EXTENSIONS = {'.md', '.markdown', '.txt', '.rst', '.json', '.yml', '.yaml'}


def should_skip(file_path):
    basename = os.path.basename(file_path).lower()
    ext = os.path.splitext(file_path)[1].lower()

    if ext in SKIP_EXTENSIONS:
        return True

    if 'test' in basename or 'spec' in basename:
        return True

    path_lower = file_path.lower()
    if '/tests/' in path_lower or '/test/' in path_lower or '/__tests__/' in path_lower:
        return True
    if 'example' in path_lower or '/examples/' in path_lower:
        return True

    return False


def check_content(content):
    issues = []
    for pattern, name, suggestion in DEBUG_PATTERNS:
        if re.search(pattern, content):
            issues.append(f"Debug statement found: {name} → {suggestion}")

    for pattern, name, suggestion in TEMP_MARKERS:
        if re.search(pattern, content):
            issues.append(f"Temporary marker found: {name} → {suggestion}")

    content_size = len(content.encode('utf-8', errors='replace'))
    if content_size > MAX_CONTENT_SIZE:
        size_kb = content_size // 1024
        issues.append(f"Large file content: {size_kb}KB (limit: {MAX_CONTENT_SIZE // 1024}KB) → Consider splitting into smaller modules or extracting data")

    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        file_path = tool_input.get('file_path', '')
        content = tool_input.get('content', '') or tool_input.get('new_string', '')

        if not content:
            sys.exit(0)

        if file_path and should_skip(file_path):
            sys.exit(0)

        issues = check_content(content)

        if issues:
            print("Quality check - issues detected:")
            for issue in issues:
                print(f"  - {issue}")
            print("\nConsider resolving before committing.")
            # Exit 0 - warn but don't block edits
            sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
