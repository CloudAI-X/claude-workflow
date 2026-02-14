# MCP Server Configuration Guide

This file documents common MCP servers you might want to add to your project.

## Quick Add Commands

### Development Tools

```bash
# GitHub - PR management, issues, code review
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Sentry - Error monitoring and debugging
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Vercel - Deployment management
claude mcp add --transport http vercel https://mcp.vercel.com

# Netlify - Static site deployment
claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp
```

### Documentation & Knowledge

```bash
# Context7 - Up-to-date library documentation
claude mcp add --transport stdio context7 -- npx -y @context7/mcp-server

# Scholar Gateway - Academic research
claude mcp add --transport http scholar-gateway https://connector.scholargateway.ai/mcp
```

### Project Management

```bash
# Linear - Issue tracking
claude mcp add --transport http linear https://mcp.linear.app/mcp

# Notion - Docs and wikis
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Asana - Task management
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Monday.com - Project boards
claude mcp add --transport http monday https://mcp.monday.com/mcp

# Jira & Confluence (Atlassian)
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
```

### Database & Data

```bash
# PostgreSQL via DBHub
claude mcp add --transport stdio postgres -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@host:5432/database"

# Airtable
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

### Communication

```bash
# Intercom - Customer support
claude mcp add --transport http intercom https://mcp.intercom.com/mcp
```

### Payments & Commerce

```bash
# Stripe - Payment processing
claude mcp add --transport http stripe https://mcp.stripe.com

# PayPal - Payment platform
claude mcp add --transport http paypal https://mcp.paypal.com/mcp

# Square - POS and payments
claude mcp add --transport sse square https://mcp.squareup.com/sse
```

## Configuration Template

Add servers to `.mcp.json` for project-wide sharing:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"],
      "env": {}
    }
  }
}
```

## Authentication

After adding a server that requires OAuth:
1. Run `/mcp` in Claude Code
2. Select the server
3. Click "Authenticate"
4. Complete the OAuth flow in your browser

## Scopes

- `--scope local` (default): Only you, only this project
- `--scope project`: Shared with team (adds to `.mcp.json`)
- `--scope user`: Available to you across all projects
