#!/usr/bin/env python3
"""
Protect sensitive files from modification.
Blocks edits to production configs, lock files, and sensitive directories.
"""
import json
import sys
import os
import fnmatch

# Files/patterns to protect (exit code 2 = block)
# Each entry is (pattern, reason) for actionable messages
PROTECTED_PATTERNS_WITH_REASONS = [
    # Lock files (usually shouldn't be manually edited)
    ('package-lock.json', "Lock files should be updated via package manager (npm install), not edited directly"),
    ('yarn.lock', "Lock files should be updated via package manager (yarn install), not edited directly"),
    ('pnpm-lock.yaml', "Lock files should be updated via package manager (pnpm install), not edited directly"),
    ('Gemfile.lock', "Lock files should be updated via package manager (bundle install), not edited directly"),
    ('poetry.lock', "Lock files should be updated via package manager (poetry lock), not edited directly"),
    ('Cargo.lock', "Lock files should be updated via package manager (cargo update), not edited directly"),

    # Sensitive files
    ('.env', ".env files contain secrets — edit manually outside of Claude Code"),
    ('.env.local', ".env files contain secrets — edit manually outside of Claude Code"),
    ('.env.production', ".env files contain secrets — edit manually outside of Claude Code"),
    ('**/secrets/*', "Secrets directory contains sensitive data — manage outside of Claude Code"),
    ('**/credentials/*', "Credentials directory contains sensitive data — manage outside of Claude Code"),

    # Git internals
    ('.git/*', ".git directory is managed by Git — never edit directly"),

    # CI/CD (warn but don't block)
    # '.github/workflows/*',
]

# Flat list for backward-compatible matching
PROTECTED_PATTERNS = [p for p, _ in PROTECTED_PATTERNS_WITH_REASONS]

# Map pattern to reason for lookup
PROTECTED_REASONS = {p: r for p, r in PROTECTED_PATTERNS_WITH_REASONS}

# Files that should warn but not block
WARN_PATTERNS = [
    '.github/workflows/*',
    'docker-compose.yml',
    'Dockerfile',
    '**/production/*',
]

def matches_pattern(file_path, patterns):
    """Check if file matches any protected pattern."""
    file_path = file_path.lstrip('./')
    for pattern in patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return pattern
        if fnmatch.fnmatch(os.path.basename(file_path), pattern):
            return pattern
    return None

def main():
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        if not file_path:
            sys.exit(0)
        
        # Check for blocked patterns
        blocked = matches_pattern(file_path, PROTECTED_PATTERNS)
        if blocked:
            reason = PROTECTED_REASONS.get(blocked, "This file is protected from edits")
            print(f"BLOCKED: {file_path}")
            print(f"   Matches protected pattern: {blocked}")
            print(f"   Reason: {reason}")
            print("   Use --force if this is intentional")
            sys.exit(2)  # Block the operation
        
        # Check for warning patterns
        warned = matches_pattern(file_path, WARN_PATTERNS)
        if warned:
            print(f"⚠️ WARNING: Editing sensitive file: {file_path}")
            print(f"   Matches pattern: {warned}")
            # Don't block, just warn
            sys.exit(0)
            
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
