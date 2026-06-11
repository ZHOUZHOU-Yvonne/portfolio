# Claude Code PR Review Sub-Agent

💰 $150 Bounty — [Issue #4](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/4)

A Claude Code sub-agent that automatically reviews pull requests and posts findings as inline comments.

## Installation

```bash
mkdir -p ~/.claude/agents/
cp pr-review.md ~/.claude/agents/pr-review.md
```

## Usage

```
> @pr-review Review PR #42 in this repo
```

Or with specific focus:
```
> @pr-review Review PR #42 — focus on security vulnerabilities only
```

## Agent Prompt

See `pr-review.md` for the full agent configuration.

## Features

- Reviews PR diffs for bugs, security issues, and code quality
- Posts findings as GitHub PR review comments
- Supports configurable review depth (low/medium/high)
- Can focus on specific areas (security, performance, style)
- Respects .gitignore and existing project conventions

## Example Output

```
🔍 PR Review: #42 — Add user authentication

### Critical
- `auth.ts:45` — JWT secret from env var without fallback validation
  → Suggestion: Add runtime check + early return if secret is undefined

### Important  
- `login.ts:23` — Password comparison not constant-time
  → Suggestion: Use crypto.timingSafeEqual

### Style
- Consider extracting validation logic to shared middleware
```
