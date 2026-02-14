# Contributing to project-starter

Thank you for your interest in contributing to the Claude Code workflow plugin! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/CloudAI-X/claude-workflow-v2/issues)
2. If not, create a new issue using the bug report template
3. Include:
   - Claude Code version (`claude --version`)
   - Operating system and version
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or error messages

### Suggesting Features

1. Check existing [Issues](https://github.com/CloudAI-X/claude-workflow-v2/issues) for similar suggestions
2. Create a new issue using the feature request template
3. Describe the use case and expected behavior

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes with Claude Code
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation changes
   - `refactor:` code refactoring
   - `test:` adding tests
   - `chore:` maintenance tasks
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Guidelines

### Adding Agents

Create a `.md` file in `agents/` with this structure:

```markdown
---
name: agent-name
description: What it does. Use PROACTIVELY when [triggers].
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

[Agent instructions here]
```

**Requirements:**

- Include "PROACTIVELY" in descriptions to enable auto-triggering
- Use valid tool names: Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch
- Choose appropriate model: `opus` (complex), `sonnet` (balanced), `haiku` (fast)

### Adding Skills

Create a subdirectory in `skills/` with a `SKILL.md` file:

```markdown
---
name: skill-name
description: Guides [domain]. Use when [triggers].
---

[Skill knowledge and patterns here]
```

**Requirements:**

- Keep skills under 500 lines for optimal context usage
- Include trigger keywords in descriptions
- Make content language-agnostic where possible

### Adding Output Styles (Commands)

Create a `.md` file in `commands/`:

```markdown
---
description: What this mode does
keep-coding-instructions: true
---

[Style instructions here]
```

### Adding Hooks

1. Add the hook script to `hooks/scripts/`
2. Register in `hooks/hooks.json`
3. Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
4. Exit codes: `0` = allow, `2` = block with message

**Example hook entry:**

```json
{
  "type": "PreToolUse",
  "matcher": "^Edit|Write$",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/my-hook.sh"
}
```

## Testing

Before submitting:

1. Install the plugin locally:

   ```bash
   claude --plugin-dir ./claude-workflow
   ```

2. Test relevant components:
   - Agents trigger on appropriate keywords
   - Skills activate correctly
   - Hooks execute as expected
   - Output styles switch properly

3. Verify cross-platform compatibility (if applicable)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Open a [Discussion](https://github.com/CloudAI-X/claude-workflow-v2/discussions) or reach out via Issues.
