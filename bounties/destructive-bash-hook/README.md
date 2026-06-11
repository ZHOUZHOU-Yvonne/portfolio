# Destructive Bash Command Blocker Hook

💰 $100 Bounty — [Issue #3](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/3)

A Claude Code PreToolUse hook that intercepts and blocks destructive bash commands before execution.

## Installation

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/destructive-check.py"
      }]
    }]
  }
}
```

Then copy the script:
```bash
mkdir -p ~/.claude/hooks/
cp destructive-check.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/destructive-check.py
```

## What It Blocks

| Pattern | Example | Reason |
|---------|---------|--------|
| `rm -rf /` or `rm -rf /*` | System wipe | Irreversible filesystem destruction |
| `rm -rf ~` | Home directory deletion | Data loss |
| `git push --force` to main/master | Force push to protected branch | Team workflow disruption |
| `git reset --hard` | Discard uncommitted work | Data loss |
| `DROP TABLE` / `DROP DATABASE` | SQL destruction | Database loss |
| `chmod 777` on system dirs | Permission escalation | Security risk |
| `> /dev/sda` or `dd` to raw devices | Disk overwrite | Hardware damage |

## Behavior

- Blocks the command and shows a warning
- Explains WHY it's dangerous
- Suggests safer alternatives
- Allows override with explicit confirmation

## Configuration

Edit `~/.claude/hooks/destructive-config.json`:
```json
{
  "protected_branches": ["main", "master", "production", "release"],
  "require_confirmation_for": ["rm", "git reset --hard", "DROP"],
  "always_block": ["rm -rf /", "rm -rf /*", "> /dev/"],
  "allowed_directories": ["/tmp", "./node_modules", "./.cache"]
}
```
