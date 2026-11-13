# STANDARD.md — Product Engineering Standard

A portable standard for building fast, secure, maintainable, visually intentional web products.
It is written to be copied into a new repository and read by both humans and coding agents.

---

## 1. Principles

1. **Clarity over decoration.** Every section has a job. If removing it loses nothing, remove it.
2. **Real over fake.** Real copy, real data, real states. No invented proof or filler.
3. **Fast by default.** Server-render what can be server-rendered; ship less JavaScript.
4. **Secure at the boundary.** Every external input is untrusted until validated.
5. **Mobile is not a smaller desktop.** Layout, touch targets and density are designed separately.
6. **Stable layout.** Content appearing must not make the page jump or move the footer.
7. **One source of truth.** Tokens, schema, validation and configuration live in one place.
8. **Explain the bug.** Diagnose before changing code; report the cause, not only the patch.
9. **No invisible work.** If it was not tested, say so. If it was not deployed, say so.
10. **Restraint.** No unsolicited features, pages, badges, animations or "nice to have" additions.

---

## 2. Default stack

| Layer | Default | Notes |
| --- | --- | --- |
| Framework | Next.js (App Router) | Server Components by default |
| Language | TypeScript strict | No implicit `any` |
| Styling | Tailwind CSS 4 + design tokens | One token source; no ad-hoc hex colors |
| Data | PostgreSQL + Prisma | Integer money, explicit relations |
| Mutations | Server Actions first | Route Handlers for webhooks/files only |
| Validation | Zod | At every server boundary |
| Auth | JWT in `httpOnly` cookie | `jose`, bcrypt/argon2 |
| Tests | Playwright + unit tests where valuable | Critical flows are covered |
| Hosting | Vercel + managed Postgres | Git-connected production deploys |
| Media | Local optimized assets or object storage | No runtime hotlinks |

A different stack is allowed only when the product needs it. Record the reason in
`docs/DECISIONS.md`, not in chat memory.

---

## 3. Repository shape

```
src/
  app/
    (marketing)/
    (shop)/
    (auth)/
    (admin)/
    api/
  components/
    ui/
    layout/
    <feature>/
  actions/
  lib/
  types/
prisma/
  schema.prisma
  migrations/
  seed.ts
public/
e2e/
docs/
```

Rules:

- Route groups describe **product areas**, not versions: `(shop)`, `(admin)`, `(auth)`.
  Never `(v3)`, `(old)`, `(new)`.
- A component used by one feature lives with that feature; a generic primitive lives in `ui/`.
- Server-only code stays in `lib/` with `server-only` where appropriate.
- No business logic in page files beyond data orchestration.
- No barrel files that hide dependency direction or bloat bundles.

---

## 4. Frontend model

- Server Components by default. Add `'use client'` only for state, effects, browser APIs or
  interactive libraries.
- Use the smallest client boundary possible. Do not turn a whole page into a client component
  to support one toggle.
- Design tokens are defined once and consumed everywhere: color, type, spacing, radius, motion.
- RTL is structural: logical properties (`padding-inline`, `inset-inline`), correct icon direction,
  correct flex/grid order, Persian numerals where the brand uses them.
- Every page has one clear `h1`, a meaningful title and a description.
- Images use `next/image`, explicit dimensions/aspect ratio and sensible `sizes`;
  no layout shift, no oversized source files.
- 3D is optional and lazy. Show a stable skeleton, respect reduced motion, cap the canvas height
  on tall screens and verify the full object stays inside the frame.
- Motion is short, purposeful and interruptible. Respect `prefers-reduced-motion`.
  Never animate layout in a way that moves the footer or traps scroll.
- Forms: visible labels, correct autocomplete, errors next to the field, disabled/loading state,
  preserved input on failure, no auto-filling of message fields unless requested.
- Empty, loading, error and success states are designed, not left as raw text.
- Do not hide essential navigation on mobile. Every account, cart and profile action has a
  visible entry point.

See `docs/FRONTEND.md` for the detailed checklist.

---

## 5. Backend model

- PostgreSQL is the source of truth. Prisma is the only normal data-access layer.
- Money is stored as integer minor units or integer Toman, never floating point.
- Dates are stored in UTC and formatted at the edge for the user's timezone.
- Every table has a stable primary key, `createdAt` and `updatedAt` where relevant.
- Use enums for finite states; use explicit foreign keys and indexes for query paths.
- Prefer soft availability flags (`isActive`) over deleting catalogue/history rows.
- Mutations validate with Zod, check authorization, then run in a transaction when they touch
  more than one row.
- Server actions return a small typed result: `{ ok: true, data }` or
  `{ ok: false, message, fieldErrors? }`. Never throw raw database errors at the UI.
- Idempotency is required for checkout, order creation, payment and any external side effect.
- Uploads validate MIME, extension, size and ownership. Store outside the source tree or in
  Postgres/object storage. Never trust a client filename.
- Email is a side effect, not a transaction. Password-reset tokens are hashed, single-use, expiring
  and never logged in production.
- Rate-limit authentication, contact and mutation endpoints. The limiter must be shared across
  instances for production scale.

See `docs/BACKEND.md` for schemas, actions and failure handling.

---

## 6. Security baseline

Non-negotiable:

- Validate environment variables at boot; fail fast if a required secret is missing.
- Passwords hashed with bcrypt (cost ≥ 12) or argon2; never reversible.
- Session cookie: `httpOnly`, `Secure` in production, `SameSite=Lax`, bounded lifetime.
- Authorization on the server for every admin/customer action, not only in the UI.
- CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, frame restrictions, COOP/CORP.
- No secrets in the client bundle, repository, logs or error messages.
- No demo accounts with public passwords in production. Rotate or remove them.
- Dependency audit and a plan for security updates.
- Backups and restore procedure for the production database.

See `docs/SECURITY.md` for the full checklist.

---

## 7. Performance budgets

- First load should feel instant on a normal connection; the hero must not wait for the whole
  application bundle.
- JavaScript sent to the client is a budget, not a default. Keep client components small.
- Fonts: self-hosted, subset, `font-display: swap`, preload only what the first screen needs.
- Images: correct dimensions, modern formats, responsive `sizes`, lazy below the fold.
- 3D: lazy-load, cap DPR, pause when off-screen/hidden, provide a static fallback.
- Database: index every filter/sort path; avoid N+1; paginate lists; select only needed fields.
- Cache deliberately. Use revalidation for catalogue data and `no-store` for personalized pages.
- Measure before optimizing. Record target metrics in `docs/QUALITY.md` for the project.

---

## 8. Testing and quality gates

Every meaningful change:

```bash
npm run build
npm run lint
npx tsc --noEmit
npx playwright test
```

Plus:

- manual or scripted checks at 320, 390, 768 and 1440 px;
- no horizontal overflow, no clipped 3D, no hidden primary action;
- no console errors or hydration warnings;
- keyboard navigation and focus states for interactive UI;
- empty/loading/error/unauthorized paths;
- real browser verification before claiming success.

See `docs/QUALITY.md` for the full gate and report template.

---

## 9. Git and deployment

- One logical change per commit; imperative, specific message.
- Never commit `.env`, secrets, `node_modules`, `.next`, local databases, test artifacts or
  generated screenshots.
- Keep `.vercelignore` (or equivalent) explicit; deploy sources, not the local workspace.
- Connect the repository to the host so pushes deploy; avoid manual uploads of large folders.
- Apply migrations before promoting a production deployment.
- Seed idempotently. Seed must not overwrite real user passwords on every run.
- Keep `README.md` for humans and `AGENTS.md` for agents up to date.
- Do not tag releases, force-push or rewrite history without explicit permission.

---

## 10. Design process

1. Read the brief and the real content.
2. Use the design skills (see `docs/DESIGN.md` and `docs/REFERENCES.md`) to choose a direction,
   not to decorate a default. Load `antislop` before UI work.
3. Set the Design Read and dials (ENERGY / RHYTHM / MOTION).
4. Define tokens and type before building pages.
5. Build the page as a composition with a clear hierarchy; check it in a real browser.
6. Review at mobile and desktop; remove anything that does not earn its place.
7. Run the anti-slop Delivery Gate and the accessibility/layout gate; fix; look again.

No "AI default" look: no generic gradient hero, no three equal feature cards by reflex, no
meaningless labels, no icon soup, no unearned glassmorphism.

---

## 11. Anti-patterns

- Version names in routes or folders.
- A hidden mobile login/profile entry point.
- Auto-filling a contact message when a topic changes.
- Fixed-height FAQ answer panels that move the footer, or inline answers that do too.
- Client-side data fetching for data the server can render.
- A server action that trusts the client's price, stock or role.
- Catching errors and replacing them with "Something went wrong" without logging context.
- Copying a demo catalogue and prices into production as if they were real.
- Shipping a splash screen that waits on hydration without a time cap.
- "Temporary" `unsafe-inline` CSP without a documented reason.
- Commit messages like "fix", "update", "changes".

---

## 12. Definition of done

A change is complete when it is:

- correct on desktop and mobile;
- accessible by keyboard and screen-reader labels;
- tested at the agreed widths and states;
- secure at the boundary;
- committed with a clear message;
- deployed (when authorized) and verified live;
- reported honestly, including what remains.
