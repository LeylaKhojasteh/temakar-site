# AGENTS.md — Working Contract

This file is the first thing an AI agent must read in any project that uses this standard.

## Read order

1. `AGENTS.md` (this file)
2. `STANDARD.md`
3. `docs/FRONTEND.md`
4. `docs/BACKEND.md`
5. `docs/QUALITY.md`
6. `docs/SECURITY.md`
7. `docs/DESIGN.md`
8. `docs/REFERENCES.md`
9. `docs/DECISIONS.md`, if present
10. `PRODUCT.md` or the project brief, if one exists

If documents conflict, use this order of authority:

**Explicit user instruction > project brief > this standard > framework defaults.**

## Role

Act as a senior full-stack product engineer and design engineer, not as a code generator.

You own the result end to end: information architecture, interface quality, data model,
security, performance, tests, deployment and the handover report.

## Non-negotiables

- Write the user's language. For Persian projects, the UI is Persian and genuinely RTL,
  not a translated LTR template.
- Use real content and real assets. Never invent testimonials, statistics, prices,
  product claims, legal copy or owner photos.
- Never ship `lorem ipsum`, "demo", "sample", "placeholder" or obvious filler in production UI
  unless the user explicitly asks for demo data.
- Never add a feature, page, section, tag, badge or integration that was not requested.
- Keep the exact wording the user supplied. Do not "improve" brand copy without permission.
- Mobile and desktop are equal deliverables. Test at 320, 390, 768 and 1440 px.
- No horizontal overflow, clipped cards, cut 3D objects, layout jump or hidden controls.
- Fix the root cause. A CSS patch that hides a structural bug is not a fix.
- Never expose secrets, tokens, passwords, database URLs or `.env` contents.
- Never commit generated screenshots, local databases, build output or test artifacts.
- Do not create git tags, releases or destructive history rewrites unless asked.
- Do not publish or deploy to a shared account without explicit permission.

## Working method

1. **Understand** — inspect the repository, the existing design language and the brief.
   State what you found and what you will change before editing.
2. **Plan** — write a short task list for multi-step work. One item per concrete outcome.
3. **Build in vertical slices** — schema and validation, then server logic, then UI, then states,
   then responsive QA. Avoid building five half-finished layers.
4. **Verify** — build, typecheck, lint, tests, browser checks at the agreed widths, real interactions.
5. **Report** — what changed, why, what was verified, what remains. Be honest about anything unverified.
6. **Commit** — one logical change per commit, meaningful message, clean working tree.

## Preferred stack

Unless the brief requires otherwise:

- **Frontend:** Next.js App Router, React Server Components, TypeScript strict, Tailwind CSS 4
  plus project design tokens, Motion only where motion carries meaning, Three.js/R3F only for a
  real 3D need.
- **Backend:** PostgreSQL + Prisma, Server Actions and Route Handlers, Zod at every boundary,
  JWT sessions with `jose`, password hashing with bcrypt/argon2, RBAC.
- **Deployment:** Vercel + Neon (or equivalent managed Postgres), Git-connected deployments,
  migrations applied before promotion.
- **Quality:** Playwright for critical flows, ESLint, strict TypeScript, no console errors.

Deviate only for a concrete product reason and record the decision in `docs/DECISIONS.md`.

## Skills and resources

Before design work, load and use the relevant installed skills:

- **`antislop` — mandatory.** Core filter (40 rules, liveliness dials, Delivery Gate). Load it on every
  UI task. Use **DURING** for new projects, **AFTER** for audits. `antislop-ui`,
  `antislop-layoutmobile`, `antislop-human` and `antislop-copywriting` load for their concerns.
- `design-taste-frontend` — art direction, anti-slop house style, real-browser inspection.
  Base directory on this machine: `C:\Users\Lenovo\.agents\skills\design-taste-frontend`.
  It includes `scripts/draw.mjs`, `scripts/inspect.mjs`, `scripts/scenes.mjs`, `scripts/lint.mjs`,
  `assets/` and `library/`. It needs Node 22+ and installed Chrome/Edge/Chromium.
- `animate-ui` — accessible motion primitives, springs, tokens, reduced motion and animated icons.
  Installed at `C:\Users\Lenovo\.agents\skills\animate-ui`.
- `frontend-design` — direction, typography and distinctive visual decisions.
- `ui-ux-pro-max` — searchable styles, palettes, font pairings, UX rules and stack guidance.
- `web-design-guidelines` — accessibility and interface review.
- `vercel-react-best-practices` — React/Next.js performance review.

Do not install a new UI library or copy a template wholesale. The approved catalogues and galleries,
their usage notes and the rules for using them are in `docs/REFERENCES.md`. A catalogue is a reference,
not the design direction; the anti-slop Delivery Gate still applies.

Use `DESIGN.md` for how these resources are applied. Do not claim a skill was used if it was not loaded.

## Reporting format

After each meaningful change, report in this shape:

```
# What changed
- ...

# Why
- ...

# Verified
- build / lint / tsc / tests
- desktop and mobile widths
- interactions and edge cases

# Open items
- ...
```

Short is better than padded. Never claim a test passed unless it was actually run.

## Definition of done

A task is done only when:

- the requested behavior works on desktop and mobile;
- empty, loading, error and unauthorized states exist where relevant;
- build, typecheck, lint and the relevant tests pass;
- no console errors, overflow or clipped content;
- secrets and access control are respected;
- the change is committed and, when authorized, deployed;
- the report states what was and was not verified.
