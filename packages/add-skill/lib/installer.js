const degit = require("degit");
const path = require("path");
const fs = require("fs");

const TIMEOUT_MS = 60000; // 60 second timeout for downloads

// Only these directories get installed to .claude/
const INSTALL_DIRS = ["agents", "commands", "hooks", "skills"];

/**
 * Validate GitHub repository format
 * @param {string} repo - Repository string to validate
 * @returns {boolean} True if valid format
 */
function isValidRepoFormat(repo) {
  // Must be "owner/repo" format with safe characters only
  // Allows: letters, numbers, hyphens, underscores, dots
  return /^[\w.-]+\/[\w.-]+$/.test(repo);
}

/**
 * Install a Claude Code plugin from GitHub (additive merge)
 * @param {string} repo - GitHub repo in format "owner/repo"
 * @param {string} name - Plugin name for display
 * @throws {Error} If plugin already installed or download fails
 */
async function install(repo, name) {
  // HIGH-1 FIX: Validate repository format to prevent path traversal
  if (!isValidRepoFormat(repo)) {
    throw new Error(
      `Invalid repository format: "${repo}". Expected: owner/repo`,
    );
  }

  const cwd = process.cwd();
  const target = path.join(cwd, ".claude");
  // MEDIUM-1 FIX: Use PID-based temp directory to prevent race conditions
  const tempTarget = path.join(cwd, `.claude-temp-install-${process.pid}`);

  const hasExisting = fs.existsSync(target);
  if (hasExisting) {
    console.log(`\n📁 Found existing .claude/ - will merge (nothing deleted)`);
  }

  console.log(`\n📦 Installing ${name}...`);

  // Clean up any previous failed install
  if (fs.existsSync(tempTarget)) {
    fs.rmSync(tempTarget, { recursive: true, force: true });
  }

  // Download to temp directory with timeout and error handling
  const emitter = degit(repo, {
    cache: false,
    force: true,
    verbose: false,
  });

  let timeoutId;
  try {
    const timeoutPromise = new Promise((_, reject) => {
      timeoutId = setTimeout(
        () => reject(new Error("Download timed out after 60 seconds")),
        TIMEOUT_MS,
      );
    });
    await Promise.race([emitter.clone(tempTarget), timeoutPromise]);
    clearTimeout(timeoutId);
  } catch (err) {
    clearTimeout(timeoutId);
    // Clean up temp on failure
    if (fs.existsSync(tempTarget)) {
      fs.rmSync(tempTarget, { recursive: true, force: true });
    }
    // MEDIUM-3 FIX: Enhanced error messages with actionable context
    if (err.code === "ENOTFOUND" || err.message.includes("getaddrinfo")) {
      throw new Error(
        `Network error accessing github.com/${repo}\n` +
          `   Check: internet connection, firewall, proxy settings`,
      );
    }
    if (err.message.includes("could not find commit")) {
      throw new Error(
        `Repository not found: github.com/${repo}\n` +
          `   Verify the repository exists and is public`,
      );
    }
    throw new Error(`Download failed for ${repo}: ${err.message}`);
  }

  // Create target if it doesn't exist
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
  }

  // Merge: copy only agents, commands, hooks, skills to target
  const stats = { added: 0, skipped: 0 };
  for (const dir of INSTALL_DIRS) {
    const srcDir = path.join(tempTarget, dir);
    const destDir = path.join(target, dir);
    if (fs.existsSync(srcDir)) {
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      mergeDirectories(srcDir, destDir, stats);
    }
  }

  // Clean up temp
  fs.rmSync(tempTarget, { recursive: true, force: true });

  // Count installed components
  const components = {
    agents: countFiles(path.join(target, "agents"), ".md"),
    skills: countDirs(path.join(target, "skills")),
    commands: countFiles(path.join(target, "commands"), ".md"),
    hooks:
      countFiles(path.join(target, "hooks"), ".py") +
      countFiles(path.join(target, "hooks"), ".sh"),
  };

  console.log(`\n✅ Installed to .claude/\n`);
  console.log(
    `   ${components.agents} agents | ${components.skills} skills | ${components.commands} commands | ${components.hooks} hooks`,
  );
  if (stats.skipped > 0) {
    console.log(`   (${stats.skipped} existing files preserved)`);
  }
  console.log(`\n   Run 'claude' to start.`);
}

/**
 * Recursively merge source directory into target, preserving existing files
 * Handles regular files, directories, and symlinks
 */
function mergeDirectories(src, dest, stats) {
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isSymbolicLink()) {
      // HIGH-2 FIX: Validate symlink targets to prevent path traversal attacks
      if (!fs.existsSync(destPath)) {
        const linkTarget = fs.readlinkSync(srcPath);
        const resolvedTarget = path.resolve(path.dirname(destPath), linkTarget);
        const resolvedDest = path.resolve(dest);

        // Only allow symlinks that point inside the .claude directory
        if (
          !resolvedTarget.startsWith(resolvedDest + path.sep) &&
          resolvedTarget !== resolvedDest
        ) {
          // Unsafe symlink - skip it with warning
          console.warn(
            `   ⚠️  Skipping unsafe symlink: ${entry.name} -> ${linkTarget}`,
          );
          stats.skipped++;
          continue;
        }

        fs.symlinkSync(linkTarget, destPath);
        stats.added++;
      } else {
        stats.skipped++;
      }
    } else if (entry.isDirectory()) {
      // Create directory if it doesn't exist
      if (!fs.existsSync(destPath)) {
        fs.mkdirSync(destPath, { recursive: true });
      }
      // Recursively merge
      mergeDirectories(srcPath, destPath, stats);
    } else if (entry.isFile()) {
      // Only copy file if it doesn't exist in destination
      if (!fs.existsSync(destPath)) {
        fs.copyFileSync(srcPath, destPath);
        stats.added++;
      } else {
        stats.skipped++;
      }
    }
    // Skip other types (sockets, fifos, etc.)
  }
}

/**
 * Count files with a specific extension in a directory
 */
function countFiles(dir, ext) {
  try {
    if (!fs.existsSync(dir)) return 0;
    return fs.readdirSync(dir).filter((f) => f.endsWith(ext)).length;
  } catch {
    return 0;
  }
}

/**
 * Count subdirectories in a directory
 */
function countDirs(dir) {
  try {
    if (!fs.existsSync(dir)) return 0;
    return fs
      .readdirSync(dir, { withFileTypes: true })
      .filter((d) => d.isDirectory()).length;
  } catch {
    return 0;
  }
}

module.exports = { install };
