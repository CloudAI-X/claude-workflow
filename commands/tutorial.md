---
allowed-tools: Read, Glob, Grep
description: Interactive tutorial for learning the plugin. Walks through agents, skills, hooks, and commands with hands-on examples.
---

# Plugin Tutorial

Welcome the user and guide them through the plugin's features interactively. This is a read-only walkthrough -- no files are modified.

## Step 0: Detect Context

Before starting, silently gather context:

1. Use Glob to find `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or other project markers in the working directory
2. Identify the project's primary language and framework
3. Use Glob to list the plugin's available components:
   - `agents/*.md` for agents
   - `skills/*/SKILL.md` for skills
   - `hooks/hooks.json` for hooks
   - `commands/*.md` for commands

Then begin the tutorial.

## Step 1: Meet the Agents

Greet the user and introduce the agent system.

Read each file in `agents/*.md` and present a summary table:

```
Welcome to the Claude Workflow Plugin tutorial.

Let's explore what this plugin gives you. First up: Agents.

Agents are specialized assistants that activate automatically based on
your request. Here's what's available:

| Agent           | Triggers When You...                    | Model  |
|-----------------|----------------------------------------|--------|
| orchestrator    | Need multi-file coordinated changes    | opus   |
| code-reviewer   | Ask for a code review                  | sonnet |
| debugger        | Report a bug or error                  | sonnet |
| ...             | ...                                    | ...    |

Agents marked PROACTIVELY in their description will activate
automatically when your prompt matches their trigger keywords.
You don't need to invoke them explicitly.
```

Explain that the orchestrator can spawn subagents for parallel work, and how agent selection works based on prompt keywords.

**Try it**: Suggest the user try a prompt like "review the last commit for issues" to see the code-reviewer agent activate.

## Step 2: Commands at Your Fingertips

Read the list of command files from `commands/*.md` and present them:

```
Commands are slash-invocable workflows. Think of them as recipes
that combine multiple steps into one action.

Available commands:

| Command              | What It Does                              |
|---------------------|-------------------------------------------|
| /project-starter:commit         | Auto-generate conventional commit  |
| /project-starter:verify-changes | Multi-agent verification suite     |
| /project-starter:review         | Code review with structured output |
| ...                             | ...                               |

Commands can be simple (commit) or complex (verify-changes spawns
5+ parallel subagents).
```

Read the `commit.md` command file and walk through how it works:

```
Let's look at how /project-starter:commit works:

1. It gathers context: current branch, staged changes, recent commits
2. It analyzes the diff to understand what changed
3. It generates a conventional commit message (feat/fix/docs/...)
4. It executes the commit

Notice the frontmatter:
  allowed-tools: Bash(git status:*), Bash(git diff:*), ...

This restricts the command to only git operations -- it can't
accidentally modify your files.
```

**Try it**: Suggest staging a file and running `/project-starter:commit`.

## Step 3: Hooks That Protect Your Code

Read `hooks/hooks.json` and explain each hook:

```
Hooks run automatically before or after certain actions.
They protect your code without you thinking about it.

Active hooks:

| Hook                | Triggers On       | What It Does              |
|--------------------|-------------------|---------------------------|
| format-on-edit     | File save/edit    | Auto-formats changed files|
| ...                | ...               | ...                       |

Hooks use exit codes to control behavior:
  Exit 0 = allow the action to proceed
  Exit 2 = block the action and show a message

This means a hook can prevent you from committing secrets,
saving malformed config, or other mistakes.
```

Read one hook script to show the pattern:

```
Here's a simplified hook structure:

  1. Receive input as JSON from stdin
  2. Inspect the content or action
  3. Exit 0 (allow) or exit 2 (block with message)

Hooks fail silently on errors (exit 0) so they never block
your workflow unexpectedly.
```

**Try it**: Suggest the user edit a file and observe the format-on-edit hook in action (if applicable to their project).

## Step 4: Skills That Enhance Responses

Read `skills/*/SKILL.md` files and present the skill domains:

```
Skills inject domain knowledge into responses. When a skill's
trigger keywords match your prompt, its instructions are loaded
automatically.

Available skill domains:

| Skill Domain     | Enhances Responses About...             |
|-----------------|----------------------------------------|
| [skill-name]    | [description from SKILL.md]            |
| ...             | ...                                    |

Skills are passive -- they don't run commands. They shape how
the assistant thinks about your problem by providing specialized
knowledge, patterns, and best practices.
```

**Try it**: Suggest a prompt that would activate one of the skills relevant to their detected project type.

## Step 5: Your Personalized Next Steps

Based on the project context detected in Step 0, provide tailored recommendations:

```
Based on your project ([language/framework]), here's what I'd
recommend trying first:

1. **[Most relevant command]** -- [why it's useful for their stack]
   Run: /project-starter:[command-name]

2. **[Most relevant agent]** -- [scenario where it helps]
   Just describe your task and it will activate automatically.

3. **[Most relevant skill]** -- [how it will help]
   Ask about [topic] and see enhanced responses.

Quick reference card:

  /project-starter:commit          -- commit with auto-message
  /project-starter:verify-changes  -- verify before pushing
  /project-starter:review          -- get a code review
  /project-starter:bootstrap-repo  -- generate full codebase docs

All available commands: /project-starter:[tab] to see the list.
```

## Presentation Guidelines

- **Conversational tone**: Write as if explaining to a colleague, not writing documentation.
- **Concise**: Each step should take 30 seconds to read. No walls of text.
- **Concrete examples**: Every step ends with a "Try it" suggestion.
- **Adaptive**: Tailor language and examples to the detected project type.
- **Progressive**: Each step builds on the previous one. Don't reference concepts before introducing them.
- **No modifications**: This command is read-only. Do not create, edit, or delete any files.
