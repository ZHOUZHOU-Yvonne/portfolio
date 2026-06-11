---
name: changelog
description: Generate structured CHANGELOG from git history between two refs
---

# CHANGELOG Generator

Generate a structured, user-facing CHANGELOG from git history.

## Usage

```
/changelog                    # Since last tag
/changelog v1.0.0..HEAD       # Specific range
/changelog --since 7d         # Last 7 days
```

## Process

1. Determine the git range:
   - No args: `git describe --tags --abbrev=0 HEAD^`..HEAD
   - `--since Nd`: `--since="N days ago"`
   - Otherwise: use provided range

2. Collect commits:
```bash
git log <range> --pretty=format:"%h %s (%an)" --no-merges
```

3. Collect closed issues/PRs if on GitHub:
```bash
gh pr list --state merged --search "merged:$(date -d '7 days ago' +%Y-%m-%d)..$(date +%Y-%m-%d)" --json number,title,author
```

4. Categorize changes into:
   - **Added** — New features (`feat:`, `feat(scope):`)
   - **Changed** — Modifications (`change:`, `refactor:`, `perf:`)
   - **Fixed** — Bug fixes (`fix:`, `fix(scope):`, `hotfix:`)
   - **Deprecated** — Soon-to-be-removed features
   - **Removed** — Removed features
   - **Security** — Security fixes (`security:`, `sec:`)

5. Generate the CHANGELOG in this format:

```markdown
# Changelog — vX.Y.Z (YYYY-MM-DD)

## Added
- **Feature name** — description (#PR_number)
- **Feature name** — description

## Changed
- **What changed** — description (#PR_number)

## Fixed
- **Bug fix description** — what was broken and how it was fixed (#issue_number)

## Contributors
@user1, @user2

---

[Full diff](https://github.com/owner/repo/compare/v1.0.0...v2.0.0)
```

6. Write to `CHANGELOG.md` (prepend to existing, after the header)

## Guidelines

- Write for end users, not developers. Explain what changed and why they should care.
- Group related changes together.
- Link to issues/PRs when available.
- If a change is from a community contributor, credit them.
- Skip internal refactors that have no user impact (unless they're significant).
- If there are no changes in a category, omit it.
- Always include the version number, date, and diff link.

## Example

```
> /changelog v2.1.0..v2.2.0

# Changelog — v2.2.0 (2026-06-12)

## Added
- **Dark mode support** — toggle in Settings > Appearance (#342)
- **CSV export** — download any table as CSV (#356)

## Fixed
- **Login timeout** — session now refreshes properly instead of kicking users out after 30min (#389)
- **Mobile nav overlap** — menu no longer covers the first page item on iOS (#401)

## Contributors
@alice, @bob, @charlie

---

[Full diff](https://github.com/acme/app/compare/v2.1.0...v2.2.0)
```
