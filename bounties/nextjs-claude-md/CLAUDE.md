# CLAUDE.md — Next.js + SQLite SaaS Template

## Project Overview
Next.js 14 App Router + SQLite (libsql/serverless) + Tailwind CSS + NextAuth.js SaaS starter.

## Commands
```bash
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build
npm run start        # Start production server
npm run lint         # ESLint check
npm run test         # Run Vitest tests
npm run test:e2e     # Run Playwright E2E tests
npm run db:migrate   # Run database migrations
npm run db:seed      # Seed database with sample data
npm run db:studio    # Open Drizzle Studio (DB GUI)
```

## Architecture
```
src/
├── app/             # Next.js App Router pages & API routes
│   ├── (auth)/      # Auth pages (login, register)
│   ├── (dashboard)/ # Authenticated dashboard pages
│   └── api/         # API route handlers
├── components/      # Shared React components
│   ├── ui/          # Shadcn/ui components
│   └── forms/       # Form components
├── lib/             # Core utilities
│   ├── db/          # Database (Drizzle ORM + SQLite)
│   │   ├── schema.ts    # Table definitions
│   │   ├── index.ts     # DB connection
│   │   └── migrations/  # SQL migration files
│   ├── auth/        # NextAuth configuration
│   └── utils.ts     # Shared helpers
├── server/          # Server-only logic
│   └── actions.ts   # Server actions
└── styles/          # Global styles
```

## Database
- **ORM**: Drizzle ORM with `better-sqlite3` (dev) / `@libsql/client` (prod)
- **Migrations**: `drizzle-kit migrate`
- **Schema location**: `src/lib/db/schema.ts`
- **Conventions**:
  - Use `cuid2()` for primary keys, not auto-increment
  - All tables get `createdAt` and `updatedAt` timestamps
  - Soft deletes: add `deletedAt` column, never hard-delete user data
  - Foreign keys: always define `onDelete` and `onUpdate` explicitly

## Patterns

### Server Actions (Preferred over API routes)
```typescript
// src/server/actions.ts
'use server'
import { auth } from '@/lib/auth'
import { db } from '@/lib/db'
import { revalidatePath } from 'next/cache'

export async function createWidget(formData: FormData) {
  const session = await auth()
  if (!session?.user?.id) throw new Error('Unauthorized')
  
  const widget = await db.widget.create({
    data: { name: formData.get('name') as string, userId: session.user.id }
  })
  
  revalidatePath('/dashboard')
  return widget
}
```

### Data Fetching
```typescript
// Server Component — direct DB access
async function WidgetList() {
  const widgets = await db.widget.findMany({ orderBy: { createdAt: 'desc' } })
  return widgets.map(w => <WidgetCard key={w.id} widget={w} />)
}
```

### Error Handling
- Server actions: return `{ error: string }` or `{ success: data }`, never throw
- API routes: use NextResponse with status codes
- Edge: wrap in try/catch, log to console.error, return generic error to client

## Testing
- **Unit**: Vitest with React Testing Library
- **E2E**: Playwright
- **DB tests**: Use in-memory SQLite (`:memory:`)
- Test files: co-located `*.test.ts` or `__tests__/`

## Rules
1. Always use Server Components by default; add `'use client'` only when needed
2. Prefer Server Actions over API routes for mutations
3. All user input must be validated with Zod before touching the database
4. Never expose raw SQL errors to the client
5. Use `next/image` for all images; never raw `<img>` tags
6. Tailwind classes only; no custom CSS files
7. No `any` types — use `unknown` and type guards if truly uncertain
8. Environment variables: prefix with `NEXT_PUBLIC_` only if used client-side
