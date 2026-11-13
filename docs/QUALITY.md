# QUALITY.md — Definition of Done and Verification

A change is not done because it renders. It is done because it was verified.

---

## 1. Required gates

For every meaningful change, from the project root:

```bash
npm run build
npm run lint
npx tsc --noEmit
npx playwright test
```

If the project uses different script names, document them in `README.md` and use those.

Plus:

- `antislop` Delivery Gate passes: Hard Gate, Purpose-Gate, Liveliness and Craftsmanship.
- `design-taste-frontend` real-browser inspection for landing/marketing pages.
- production build, not only `next dev`
- fresh browser context for the main flow
- no console errors or hydration warnings
- no horizontal overflow
- no clipped or hidden essential control

---

## 2. Viewport matrix

| Width | Purpose |
| --- | --- |
| 320 | smallest supported phone |
| 390 | common phone |
| 768 | tablet |
| 1024 | small desktop |
| 1440 | standard desktop |
| 1920 / 2560 / 3840 | hero, 3D, large-monitor framing |

For each relevant page, check:

- header actions and menu entry points
- main heading and primary CTA
- forms and error states
- images/3D not cropped
- footer boundary not jumping
- no horizontal scroll
- theme light/dark, if supported

---

## 3. Interaction checklist

- [ ] menu opens, stays open when the pointer moves into it, closes on Escape/outside click
- [ ] login/register/profile entry visible on mobile
- [ ] overlays (menu, quick view, cart, dialog) release scroll lock
- [ ] forms preserve input on error and never auto-fill unexpected fields
- [ ] password show/hide does not overlap text
- [ ] FAQ/accordion answers appear under the correct question and do not move the footer
- [ ] 3D hero is fully in frame at large sizes
- [ ] loading, empty, error and success states exist
- [ ] keyboard focus is visible and trapped/restored in modals
- [ ] reduced motion still usable

---

## 4. Visual review

- Inspect the page in a real browser at the actual widths, not only from CSS reasoning.
- Compare the composition at mobile and desktop: hierarchy, spacing, density.
- Remove anything that does not earn its place.
- Check real Persian shaping, ZWNJ, numbers and mixed LTR strings.
- Check that thin type/logo strokes remain visible at the smallest size.
- Check that the design does not collapse into a generic template.

If a skill provides an inspector (for example `design-taste-frontend`'s
`scripts/inspect.mjs`), run it and address findings before declaring the design finished.

---

## 5. Test strategy

- **E2E (Playwright):** critical revenue/auth flows.
  - home → catalogue → product → cart → checkout;
  - register/login/logout;
  - profile/orders/addresses;
  - admin product/order/contact;
  - access control for protected routes;
  - mobile viewport overflow checks.
- **Unit:** pure pricing, validation, date/number formatting, state transitions.
- **Integration:** server actions with a test database when a bug justifies it.
- **Fixtures:** deterministic test users; reset passwords if a test changes them.
- **Artifacts:** screenshots/traces go to ignored `test-results/`, never committed.
- **Selectors:** prefer roles/labels; avoid brittle CSS chains.
- **Waits:** rely on web-first assertions, not arbitrary sleeps.
- **Flaky tests:** fix the cause; never add retries to hide it.

---

## 6. Performance verification

- Check the production build.
- Main thread: no unnecessary large client bundle on first load.
- Images: correct dimensions, no oversized downloads, no CLS.
- Fonts: subset/preload only critical faces.
- 3D/canvas: lazy, capped DPR, paused when hidden.
- Lists: paginated; database queries indexed and selected fields only.
- Record any measured budget in the project `README` or `docs/PERFORMANCE.md`.

There is no "perfect" backend. There is a backend whose failure modes are known, tested and
observable.

---

## 7. Report template

```md
# What changed
- ...

# Why
- ...

# Verified
- build:
- lint:
- tsc:
- tests:
- viewports:
- interactions:
- live URL:

# Open items
- ...
```

Be specific. "Everything works" is not a report.

---

## 8. Release gate

Before promotion:

- [ ] migrations applied with the direct database URL
- [ ] environment variables present for production/preview
- [ ] build uses the production command
- [ ] no demo credentials or sample data in production
- [ ] security headers active
- [ ] custom domain/canonical URL correct
- [ ] sitemap/robots correct
- [ ] error/404 pages use the real site design
- [ ] backup exists
- [ ] rollback path known
- [ ] live smoke test on the production URL
