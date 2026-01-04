# project-starter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-v1.0.33+-blue.svg)](https://code.claude.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/CloudAI-X/claude-workflow/pulls)

A universal Claude Code workflow plugin with specialized agents, skills, hooks, and output styles for any software project.

---

## Quick Start

### Option 1: CLI (Per-Session)

```bash
# Clone the plugin
git clone https://github.com/CloudAI-X/claude-workflow.git

# Run Claude Code with the plugin
claude --plugin-dir ./claude-workflow
```

### Option 2: Agent SDK

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Hello",
  options: {
    plugins: [{ type: "local", path: "./claude-workflow" }],
  },
})) {
  // Plugin commands, agents, and skills are now available
}
```

### Option 3: Install Permanently

```bash
# Install from marketplace (when available)
claude plugin install project-starter

# Or install from local directory
claude plugin install ./claude-workflow
```

### Verify Installation

After loading the plugin, verify it's working:

```
> /plugin
```

Tab to **Installed** - you should see `project-starter` listed.
Tab to **Errors** - should be empty (no errors).

These commands become available:

```
/project-starter:architect    # Architecture-first mode
/project-starter:rapid        # Ship fast mode
/project-starter:commit       # Auto-generate commit message
/project-starter:verify-changes  # Multi-agent verification
```

---

## What's Included

| Component    | Count | Description                                                              |
| ------------ | ----- | ------------------------------------------------------------------------ |
| **Agents**   | 7     | Specialized subagents for code review, debugging, security, etc.         |
| **Commands** | 17    | Slash commands for workflows and output styles                           |
| **Skills**   | 6     | Knowledge domains Claude uses autonomously                               |
| **Hooks**    | 9     | Automation scripts for formatting, security, verification, notifications |

---

## Usage Examples

### Commands in Action

**Auto-commit your changes:**

```
> /project-starter:commit

Looking at staged changes...
✓ Created commit: feat(auth): add JWT refresh token endpoint
```

**Full git workflow:**

```
> /project-starter:commit-push-pr

✓ Committed: feat: add user dashboard
✓ Pushed to origin/feature/dashboard
✓ Created PR #42: https://github.com/you/repo/pull/42
```

**Verify before shipping:**

```
> /project-starter:verify-changes

Spawning verification agents...
├─ build-validator: ✓ Build passes
├─ test-runner: ✓ 42 tests pass
├─ lint-checker: ⚠ 2 warnings (non-blocking)
└─ security-scanner: ✓ No vulnerabilities

Ready to ship!
```

### Agents in Action

Agents spawn automatically based on your request:

**You say:** "The login is broken, users get 401 errors"

```
[debugger agent activated]
→ Checking auth middleware... found issue
→ Token validation uses wrong secret in production
→ Fix: Update AUTH_SECRET in .env.production
```

**You say:** "Review my changes"

```
[code-reviewer agent activated]
→ Analyzing 3 files changed...
✓ Logic is correct
⚠ Missing null check on line 42
⚠ Consider adding rate limiting to this endpoint
```

**You say:** "Add authentication to the API"

```
[orchestrator agent activated]
→ Breaking down into subtasks:
  1. Design auth schema (spawning architect)
  2. Implement JWT middleware
  3. Add login/register endpoints
  4. Write tests (spawning test-architect)
  5. Update API docs (spawning docs-writer)
```

### Skills in Action

Skills provide domain knowledge automatically:

**You ask:** "How should I structure the payment service?"

```
[designing-architecture skill applied]
→ Recommending hexagonal architecture
→ Payment providers as adapters
→ Core domain isolated from infrastructure
```

**You ask:** "Make this endpoint faster"

```
[optimizing-performance skill applied]
→ Adding database indexes
→ Implementing response caching
→ Using pagination for large results
```

### Hooks in Action

Hooks run automatically on events:

**Security block (pre-edit):**

```
⛔ BLOCKED: Potential secret detected
   File: src/config.ts, Line 5
   Pattern: API key (sk-...)

   Remove the secret and use environment variables.
```

**Auto-format (post-edit):**

```
✓ Formatted with prettier: src/components/Button.tsx
✓ Formatted with black: scripts/deploy.py
```

**Desktop notifications:**

```
🔔 "Claude needs input" - when waiting for your response
🔔 "Task complete" - when finished
```

---

## Commands Reference

All commands use the format `/project-starter:<command>`.

### Output Styles

| Command                      | Mode                                          |
| ---------------------------- | --------------------------------------------- |
| `/project-starter:architect` | System design mode - architecture before code |
| `/project-starter:rapid`     | Fast development - ship quickly, iterate      |
| `/project-starter:mentor`    | Teaching mode - explain the "why"             |
| `/project-starter:review`    | Code review mode - strict quality             |

### Git Workflow (Inner-Loop)

| Command                              | Purpose                                   |
| ------------------------------------ | ----------------------------------------- |
| `/project-starter:commit`            | Auto-generate conventional commit message |
| `/project-starter:commit-push-pr`    | Commit → Push → Create PR (full workflow) |
| `/project-starter:quick-fix`         | Fast fix for lint/type errors             |
| `/project-starter:add-tests`         | Generate tests for recent changes         |
| `/project-starter:lint-fix`          | Auto-fix all linting issues               |
| `/project-starter:sync-branch`       | Sync with main (rebase or merge)          |
| `/project-starter:summarize-changes` | Generate standup/PR summaries             |

### Verification

| Command                            | Purpose                                 |
| ---------------------------------- | --------------------------------------- |
| `/project-starter:verify-changes`  | Multi-subagent adversarial verification |
| `/project-starter:validate-build`  | Build process validation                |
| `/project-starter:run-tests`       | Tiered test execution                   |
| `/project-starter:lint-check`      | Code quality checks                     |
| `/project-starter:security-scan`   | Security vulnerability detection        |
| `/project-starter:code-simplifier` | Post-implementation cleanup             |

---

## Agents

Agents are specialized subagents that Claude spawns automatically based on your task.

| Agent              | Purpose                          | Auto-Triggers                               |
| ------------------ | -------------------------------- | ------------------------------------------- |
| `orchestrator`     | Coordinate multi-step tasks      | "improve", "refactor", multi-module changes |
| `code-reviewer`    | Review code quality              | After code changes, before commits          |
| `debugger`         | Systematic bug investigation     | Errors, test failures, crashes              |
| `docs-writer`      | Technical documentation          | README, API docs, guides                    |
| `security-auditor` | Security vulnerability detection | Auth, user input, sensitive data            |
| `refactorer`       | Code structure improvements      | Technical debt, cleanup                     |
| `test-architect`   | Design test strategies           | Adding/improving tests                      |

---

## Skills

Skills are knowledge domains that Claude uses autonomously when relevant.

| Skill                    | Domain                                      |
| ------------------------ | ------------------------------------------- |
| `analyzing-projects`     | Understand codebase structure and patterns  |
| `designing-tests`        | Unit, integration, E2E test approaches      |
| `designing-architecture` | Clean Architecture, Hexagonal, etc.         |
| `optimizing-performance` | Speed up applications, identify bottlenecks |
| `managing-git`           | Version control, conventional commits       |
| `designing-apis`         | REST/GraphQL patterns and best practices    |

---

## Hooks

Hooks run automatically on specific events.

| Hook                  | Trigger       | Action                                 |
| --------------------- | ------------- | -------------------------------------- |
| Security scan         | Edit/Write    | Blocks commits with potential secrets  |
| File protection       | Edit/Write    | Blocks edits to lock files, .env, .git |
| Auto-format           | Edit/Write    | Runs prettier/black/gofmt by file type |
| Command logging       | Bash          | Logs to `.claude/command-history.log`  |
| Environment check     | Session start | Validates Node.js, Python, Git         |
| Prompt analysis       | User prompt   | Suggests appropriate agents            |
| Auto-verify           | Task complete | Runs tests/lint, reports results       |
| Input notification    | Input needed  | Desktop notification                   |
| Complete notification | Task complete | Desktop notification                   |

---

## Configuration

### Add Permissions to Your Project

Copy the permissions template to your project:

```bash
mkdir -p /path/to/your/project/.claude
cp templates/settings.local.json.template /path/to/your/project/.claude/settings.local.json
```

This pre-allows common safe commands so you don't get prompted every time.

### Add Team Conventions

Copy the CLAUDE.md template to your project root:

```bash
cp templates/CLAUDE.md.template /path/to/your/project/CLAUDE.md
```

Then customize with your:

- Package manager commands
- Test/build/lint commands
- Code conventions
- Architecture decisions

### MCP Servers

Copy the MCP template to enable integrations like Slack, GitHub, Sentry:

```bash
cp templates/mcp.json.template /path/to/your/project/.mcp.json
```

Then configure the environment variables for the servers you want to use.

### GitHub Action (@.claude in PRs)

Enable Claude to respond to PR comments by installing the GitHub Action:

```bash
# In your repository
claude /install-github-action
```

This enables:

- Tag `@claude` in PR comments to get code suggestions
- Auto-update `CLAUDE.md` during code review
- Claude responds to review feedback automatically

**Example PR comment:**

```
@claude please add input validation to the email field
```

**Team workflow tip:** Use `@claude` to update your `CLAUDE.md` with learnings from code review:

```
@claude add a note to CLAUDE.md that we should always validate email format before API calls
```

---

## Extending the Plugin

### Add Custom Commands

Create `.md` files in `commands/`:

```markdown
---
allowed-tools: Bash(git:*), Read, Write
description: What this command does
argument-hint: [optional arguments]
---

[Command instructions here]
```

### Add Custom Agents

Create `.md` files in `agents/`:

```markdown
---
name: my-agent
description: What it does. Use PROACTIVELY when [triggers].
tools: Read, Write, Edit, Bash
model: sonnet
---

[Agent instructions here]
```

### Add Custom Skills

Create subdirectories in `skills/` with a `SKILL.md` file:

```markdown
---
name: my-skill
description: Guides [domain]. Use when [triggers].
---

[Skill knowledge and patterns here]
```

---

## Plugin Structure

```
claude-workflow/
├── .claude-plugin/
│   ├── plugin.json           # Required: Plugin manifest
│   └── marketplace.json      # Optional: Marketplace metadata
├── agents/                   # 7 specialized agents
│   ├── orchestrator.md
│   ├── code-reviewer.md
│   ├── debugger.md
│   ├── docs-writer.md
│   ├── security-auditor.md
│   ├── refactorer.md
│   └── test-architect.md
├── commands/                 # 17 slash commands
│   ├── architect.md          # Output styles
│   ├── rapid.md
│   ├── mentor.md
│   ├── review.md
│   ├── commit.md             # Git workflow
│   ├── commit-push-pr.md
│   ├── quick-fix.md
│   ├── add-tests.md
│   ├── lint-fix.md
│   ├── sync-branch.md
│   ├── summarize-changes.md
│   ├── verify-changes.md     # Verification
│   ├── validate-build.md
│   ├── run-tests.md
│   ├── lint-check.md
│   ├── security-scan.md
│   └── code-simplifier.md
├── skills/                   # 6 knowledge domains
│   ├── analyzing-projects/
│   ├── designing-tests/
│   ├── designing-architecture/
│   ├── designing-apis/
│   ├── managing-git/
│   └── optimizing-performance/
├── hooks/
│   ├── hooks.json            # Hook configuration
│   └── scripts/              # 9 automation scripts
├── templates/                # User-copyable templates
│   ├── CLAUDE.md.template
│   ├── settings.json.template
│   ├── settings.local.json.template
│   └── mcp.json.template
├── CLAUDE.md                 # Plugin development guidelines
└── README.md
```

---

## Requirements

- **Claude Code** v1.0.33 or later
- **Python 3** (for hook scripts)
- **Node.js** (optional, for npm commands)
- **Git** (for version control features)

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CloudAI-X/claude-workflow-v2&type=date&legend=top-left)](https://www.star-history.com/#CloudAI-X/claude-workflow-v2&type=date&legend=top-left)

## Credits

- Plugin created by [@cloudxdev](https://x.com/cloudxdev)
- Workflow patterns inspired by [Boris Cherny](https://x.com/bcherny) (creator of Claude Code)

## License

MIT - see [LICENSE](./LICENSE) for details.
