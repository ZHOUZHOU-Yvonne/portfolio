#!/usr/bin/env python3
"""
Claude Code PreToolUse Hook — Blocks destructive bash commands.
Reads tool input JSON from stdin, checks command against blocklist.
Outputs JSON with continue=false to block, or continue=true to allow.
"""

import sys, json, re, os

CONFIG_FILE = os.path.expanduser('~/.claude/hooks/destructive-config.json')

DEFAULT_CONFIG = {
    "protected_branches": ["main", "master", "production", "release"],
    "require_confirmation_for": ["rm", "git reset --hard", "DROP", "TRUNCATE"],
    "always_block": ["rm -rf /", "rm -rf /*", "rm -rf ~", "> /dev/"],
    "allowed_directories": ["/tmp", "./node_modules", "./dist", "./.cache", "./build"]
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            pass
    return DEFAULT_CONFIG

def check_destructive(command):
    """Check if a bash command is destructive. Returns (blocked, reason)."""
    config = load_config()
    cmd_lower = command.lower().strip()
    cmd_clean = ' '.join(cmd_lower.split())  # Normalize whitespace

    # Always blocked patterns — no override
    for pattern in config["always_block"]:
        if pattern.lower() in cmd_clean:
            return True, f"ALWAYS BLOCKED: Command matches forbidden pattern '{pattern}'"

    # Check for rm -rf (dangerous delete)
    rm_match = re.search(r'rm\s+(-[a-z]*r[a-z]*f[a-z]*|-rf|-fr)', cmd_lower)
    if rm_match:
        # Check if target is in allowed directories
        target = cmd_lower[rm_match.end():].strip()
        allowed = any(ad in target for ad in config["allowed_directories"])
        if not allowed:
            return True, (
                f"BLOCKED: 'rm -rf' outside safe directories.\n"
                f"  Target: {target}\n"
                f"  Allowed: {', '.join(config['allowed_directories'])}\n"
                f"  Safer: Use 'mv' to trash, or add path to allowed_directories"
            )

    # Check for force-push to protected branches
    fp_match = re.search(r'git\s+push\s+(-[a-z]*f|--force).*?(main|master|production|release)', cmd_lower)
    if fp_match:
        branch = fp_match.group(2)
        return True, (
            f"BLOCKED: Force-push to protected branch '{branch}'.\n"
            f"  Safer: Use 'git push --force-with-lease' or create a new branch"
        )

    # Check for git reset --hard
    if 'git reset --hard' in cmd_lower:
        return True, (
            f"BLOCKED: 'git reset --hard' discards uncommitted changes.\n"
            f"  Safer: Use 'git stash' to save work, then reset"
        )

    # Check for SQL DROP
    drop_match = re.search(r'\b(DROP\s+(TABLE|DATABASE|SCHEMA))\b', cmd_lower, re.IGNORECASE)
    if drop_match:
        return True, (
            f"BLOCKED: SQL {drop_match.group(1)} is irreversible.\n"
            f"  Safer: Create a backup or rename instead"
        )

    # Check for dd / raw device writes
    if re.search(r'\bdd\b.*\bof=/dev/', cmd_lower):
        return True, "BLOCKED: Writing to raw device via dd is dangerous"

    # Check for redirect overwrite to /dev
    if re.search(r'>\s*/dev/[a-z]+', cmd_lower):
        return True, "BLOCKED: Redirecting to /dev/ device"

    # Check for chmod 777 on system paths
    chmod_match = re.search(r'chmod\s+.*777\s+(/etc|/usr|/bin|/sbin|/var|/opt)', cmd_lower)
    if chmod_match:
        return True, f"BLOCKED: Setting 777 permissions on system path"

    return False, ""


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except:
        # If we can't parse input, let it through
        print(json.dumps({"continue": True}))
        return 0

    command = input_data.get('tool_input', {}).get('command', '') or ''

    if not command:
        print(json.dumps({"continue": True}))
        return 0

    blocked, reason = check_destructive(command)

    if blocked:
        print(json.dumps({
            "continue": False,
            "stopReason": f"🚨 Destructive command blocked:\n\n{reason}",
            "systemMessage": f"Destructive bash command was blocked by safety hook.\n\n{reason}\n\nTo override, prefix your command with: SAFE_OVERRIDE=1"
        }))
    else:
        print(json.dumps({"continue": True}))

    return 0

if __name__ == '__main__':
    sys.exit(main())
