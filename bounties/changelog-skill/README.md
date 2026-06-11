# CHANGELOG Generator Skill

💰 $50 Bounty — [Issue #1](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/1)

A Claude Code skill that generates structured, user-facing CHANGELOG files from git history.

## Installation

```bash
mkdir -p ~/.claude/skills/
cp changelog.md ~/.claude/skills/changelog.md
```

## Usage

In Claude Code:
```
/changelog                    # Since the last git tag
/changelog v1.0.0..main       # Between two refs
/changelog --since 14d        # Last 14 days
```

## Output Format

Generates Keep a Changelog-compliant changelogs with categories:
- **Added** — New features
- **Changed** — Modified behavior
- **Fixed** — Bug fixes
- **Deprecated** — Soon-to-remove
- **Removed** — Removed
- **Security** — Vulnerability fixes

Each entry is written for end users, links to relevant issues/PRs, and credits contributors.
