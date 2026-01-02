# Claude Code Development Guidelines

> Team-maintained workflow document. Update frequently with new learnings.

## Quick Reference

- **Plugin validation**: `claude plugin validate`
- **Test locally**: `claude --plugin-dir ./`
- **Formatting**: Prettier for MD/JSON, Black for Python

## Development Workflow

### Making Changes

1. **Before editing any file**:
   - Run `claude plugin validate` to ensure current state is valid
   - Check existing patterns in similar files

2. **When adding agents** (`agents/*.md`):
   - Copy structure from `agents/orchestrator.md` as template
   - Include "PROACTIVELY" in description for auto-triggering
   - Specify tools, model (opus/sonnet/haiku), and skills
   - Test trigger keywords work as expected

3. **When adding skills** (`skills/*/SKILL.md`):
   - Keep under 500 lines for optimal context usage
   - Include trigger keywords in description
   - Make content language-agnostic where possible

4. **When adding hooks** (`hooks/scripts/*`):
   - Register in `hooks/hooks.json`
   - Use `${CLAUDE_PLUGIN_ROOT}` for paths
   - Exit codes: 0 = allow, 2 = block with message
   - Test with both success and failure cases

5. **After all changes**:
   - Run `claude plugin validate`
   - Test the specific feature with Claude Code

## Code Conventions

### Markdown Files
- Use YAML frontmatter for metadata
- Consistent heading hierarchy (# > ## > ###)
- Code blocks with language specifiers

### Python Hooks
- Use `#!/usr/bin/env python3` shebang
- Read input from stdin as JSON
- Handle all exceptions silently (don't block operations)
- Use subprocess.run with timeout

### JSON Files
- 2-space indentation
- No trailing commas
- Validate syntax before committing

## Git Workflow

### Commit Messages
Follow Conventional Commits:
```
feat: add new agent for X
fix: correct hook exit code handling
docs: update README with new feature
chore: bump version to X.Y.Z
```

### Branching
- `main` is always deployable
- Feature branches: `feature/description`
- Bug fixes: `fix/description`

## Available Agents (Use These!)

When working on this repo, leverage the plugin's own agents:

| Task | Agent to Use |
|------|--------------|
| Multi-file changes | `orchestrator` |
| Code quality check | `code-reviewer` |
| Bug investigation | `debugger` |
| Update docs | `docs-writer` |
| Security review | `security-auditor` |
| Clean up code | `refactorer` |
| Add tests | `test-architect` |

## Common Patterns

### Hook Script Template
```python
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
        # Process input_data
        # Exit 0 to allow, exit 2 to block
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Don't block on errors

if __name__ == '__main__':
    main()
```

### Agent Definition Template
```markdown
---
name: agent-name
description: What it does. Use PROACTIVELY when [triggers].
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

# Agent Name

[Instructions here]
```

## Testing Checklist

Before pushing:
- [ ] `claude plugin validate` passes
- [ ] Tested feature manually with Claude Code
- [ ] No hardcoded paths (use `${CLAUDE_PLUGIN_ROOT}`)
- [ ] Hook scripts handle errors gracefully
- [ ] CHANGELOG.md updated for user-facing changes

## Troubleshooting

### Hook not executing
- Check `hooks/hooks.json` matcher regex
- Verify script has executable permissions (`chmod +x`)
- Check Python path (`#!/usr/bin/env python3`)

### Agent not triggering
- Ensure "PROACTIVELY" is in description
- Check trigger keywords are in user's prompt
- Verify model name is valid (opus/sonnet/haiku)

### Validation failing
- Run `claude plugin validate` for specific errors
- Check JSON syntax in all config files
- Verify all referenced files exist

---

## Team Notes

<!-- Add learnings, gotchas, and tips here -->

- The format-on-edit hook silently fails if formatter not installed (by design)
- MCP permissions go in user's settings, not plugin
- Commands are accessed via `/project-starter:<command-name>`
- All commands (output styles, inner-loop, verification) go in `commands/` at root
