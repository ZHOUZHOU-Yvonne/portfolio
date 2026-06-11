# n8n + Claude API — Automated Weekly Dev Summary

💰 **$200 Bounty Submission** — [Issue #5](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/5)

## What This Does

Every Friday at 5PM, this n8n workflow:
1. Fetches this week's commits, closed issues, and merged PRs from GitHub
2. Sends the data to Claude API (Sonnet 4) to generate a professional narrative summary
3. Delivers the summary via email and/or Slack/Discord webhook

## Setup (5 Steps)

### 1. Import the Workflow
- Open n8n → Workflows → Import from File
- Select `Weekly_Dev_Summary.json`

### 2. Configure Variables
Edit the **Configuration** node:
| Variable | Description | Example |
|----------|-------------|---------|
| `repo_name` | GitHub repo | `owner/repo` |
| `repo_url` | GitHub API URL | `https://api.github.com/repos/owner/repo` |
| `github_token` | GitHub Personal Access Token | `ghp_xxx` |
| `claude_api_key` | Anthropic API Key | `sk-ant-xxx` |
| `from_email` | Sender email | `bot@company.com` |
| `to_email` | Recipient email | `team@company.com` |
| `webhook_url` | Slack/Discord webhook URL | `https://hooks.slack.com/...` |
| `language` | Summary language | `English` or `French` |

### 3. Configure Email (if using email delivery)
- Edit the **Send Email Report** node
- Set up SMTP credentials in n8n Credentials

### 4. Activate the Workflow
- Toggle the **Active** switch (top right)
- The cron trigger will fire every Friday at 5PM

### 5. Test
- Click **Test Workflow** to run immediately
- Check your email/Slack for the summary

## Requirements Checklist

- [x] Exportable n8n workflow (.json file)
- [x] Trigger: weekly cron (Friday 5PM)
- [x] Fetches GitHub: commits, closed issues, merged PRs
- [x] Calls Claude API (claude-sonnet-4-20250514)
- [x] Delivers via email + Slack/Discord webhook
- [x] Configurable: repo, destination, language (EN/FR)
- [x] README with setup in 5 steps or fewer

## Workflow Architecture

```
[Cron Trigger (Fri 5PM)]
         │
    ┌────┼────┐
    ▼    ▼    ▼
[Commits][Issues][PRs]
    │    │    │
    └────┼────┘
         ▼
  [Format Data]
         │
         ▼
  [Claude API]
         │
    ┌────┴────┐
    ▼         ▼
[Email]  [Slack/Discord]
```

## Example Output

> ## Weekly Summary: owner/repo (June 6-12, 2026)
>
> ### Key Accomplishments
> This week the team landed 23 commits across 4 contributors. The authentication refactor was completed and deployed to staging...
>
> ### Notable Changes
> - **Auth module rewrite** — migrated from JWT to session-based auth, reducing token size by 60%
> - **Performance fix** — query optimization reduced homepage load time from 2.1s to 0.8s
>
> ### Areas Needing Attention
> - Test coverage dropped 3% this week — consider adding tests for the new auth module
> - 2 high-priority bugs remain open in the backlog
>
> ### Next Week Recommendations
> - Prioritize the payment integration PR (#342) — it's blocking the release
> - Schedule a review session for the new onboarding flow

## License

MIT — Built for the Claude Builders Bounty program.
