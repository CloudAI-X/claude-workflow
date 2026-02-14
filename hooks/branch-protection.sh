#!/usr/bin/env bash
# Warn when git operations target protected branches.
# Informational only - never blocks operations.

INPUT=$(cat)

if command -v jq &> /dev/null; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
else
    COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
fi

if [[ -z "$COMMAND" ]]; then
    exit 0
fi

if ! echo "$COMMAND" | grep -qE 'git (commit|push)'; then
    exit 0
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [[ -z "$CURRENT_BRANCH" ]]; then
    exit 0
fi

PROTECTED_BRANCHES=("main" "master" "production")

for BRANCH in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$CURRENT_BRANCH" == "$BRANCH" ]]; then
        echo "WARNING: You are on protected branch '$CURRENT_BRANCH'."
        echo "  Create a feature branch: git checkout -b feature/your-change"
        echo "  Or use: /project-starter:sync-branch to manage branches"
        exit 0
    fi
done

exit 0
