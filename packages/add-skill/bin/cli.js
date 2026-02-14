#!/usr/bin/env node

const { install } = require("../lib/installer");

const REPO = "CloudAI-X/claude-workflow-v2";
const NAME = "claude-workflow-v2";

// Parse command line arguments
const args = process.argv.slice(2);

// Show help
if (args.includes("--help") || args.includes("-h")) {
  console.log(`
install-claude-workflow-v2 - Install Claude Code workflow plugin

Usage:
  npx install-claude-workflow-v2

Installs agents, skills, commands, and hooks to .claude/ in current directory.

After install, run 'claude' to start.

Repository: https://github.com/CloudAI-X/claude-workflow-v2
`);
  process.exit(0);
}

// Run the installer
install(REPO, NAME)
  .then(() => process.exit(0))
  .catch((err) => {
    console.error(`\n❌ ${err.message}`);
    process.exit(1);
  });
