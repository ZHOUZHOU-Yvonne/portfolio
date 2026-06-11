# CLAUDE.md Template — Next.js + SQLite SaaS

💰 $75 Bounty — [Issue #2](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/2)

A production-ready CLAUDE.md for Next.js 14 + SQLite SaaS projects. Drop it into any Next.js project for instant Claude Code productivity.

## Usage

```bash
cp CLAUDE.md /path/to/your-nextjs-project/CLAUDE.md
```

## What's Covered

- **Commands**: dev, build, test, lint, database operations
- **Architecture**: App Router directory structure and conventions
- **Database**: Drizzle ORM patterns, migration workflow, soft deletes
- **Server Actions**: Type-safe server mutations (preferred over API routes)
- **Data Fetching**: Server Components with direct DB access
- **Error Handling**: Structured error responses, never expose raw errors
- **Testing**: Vitest, Playwright, in-memory SQLite configuration
- **Code Rules**: TypeScript strictness, Tailwind-only styling, security constraints

## Customization

Edit the CLAUDE.md to match your specific stack:
- Replace package manager (`npm` → `pnpm`/`yarn`/`bun`)
- Update auth provider if not using NextAuth.js
- Adjust Drizzle config if using PostgreSQL/MySQL instead of SQLite
