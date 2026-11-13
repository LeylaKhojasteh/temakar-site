# FRONTEND.md — Interface Standard

The frontend is judged as a product, not as a collection of components.

---

## 1. Art direction before components

Use the installed design skills in this order:

1. **`design-taste-frontend`** — read its instructions, deal directions with
   `node <skill>/scripts/draw.mjs`, choose one, then build and inspect.
   Base directory on this machine: `C:\Users\Lenovo\.agents\skills\design-taste-frontend`.
   Useful scripts:
   - `scripts/draw.mjs` — deal directions, type, palette and hero/section blueprints.
   - `scripts/inspect.mjs` — real-browser house-style gate.
   - `scripts/scenes.mjs` — scroll scenes at desktop, phone and reduced motion.
   - `scripts/lint.mjs` — static gate.
   It needs Node 22+ and installed Chrome/Edge/Chromium and writes working files to `.taste-skill/`.
2. **`frontend-design`** — when the brief needs a distinctive direction rather than a known style.
3. **`ui-ux-pro-max`** — searchable styles, palettes, font pairings, UX rules and stack patterns.
4. **`web-design-guidelines`** — accessibility and interface audit before calling it finished.
5. **`vercel-react-best-practices`** — performance review of React/Next.js code.

Never claim a skill was used unless it was actually loaded and its output was considered.
The direction must come from the subject, not from a generic "premium dark landing page".

---

## 2. Tokens

One token source, consumed by CSS and components:

- `--ink`, `--ink-2`, `--ink-3` — surfaces
- `--bone`, `--bone-dim` — text
- `--copper` or brand accent — accent, used sparingly
- `--line` — hairlines and dividers
- type scale, spacing scale, radii, shadows, motion durations

Rules:

- No raw hex values scattered in components.
- No second palette for one page.
- Theme switching changes tokens, not component markup.
- Contrast must remain acceptable in every theme.
- Page background and text color are defined at the root; components inherit.

---

## 3. Typography

- Two families maximum: one display/wordmark, one text face (or a variable family used carefully).
- Self-host fonts, subset scripts, `font-display: swap`, preload only the first-screen face.
- Set a real type scale, not browser defaults:
  - display, h1, h2, h3, body, small, caption;
  - line heights tuned separately for headings and body;
  - tabular numbers for prices and quantities.
- Persian text: test real Persian shaping, line breaking, ZWNJ and mixed Latin/number runs.
- Thin serif hairlines at small sizes need a slight stroke or a heavier weight;
  verify in a real browser, not only in Figma.
- Do not use a display face for long paragraphs.
- Do not fake bold/italic if the font files do not include it.

---

## 4. Layout and responsive design

- Mobile-first CSS, but design the desktop composition intentionally.
- Breakpoints should be few and meaningful. Suggested: 640, 900/1024, 1440.
- Use logical properties: `padding-inline`, `margin-inline`, `inset-inline`.
- Content width is constrained; full-bleed is a deliberate choice, not a default.
- Cards and grids: no clipped media, no text overflow, no unclickable buttons.
- Stable layout:
  - reserve space for content that appears later (FAQ answers, banners, filters);
  - do not let opening/closing a panel move the footer;
  - do not use `height: 100vh` for content that must fit mobile browsers; use `svh` carefully.
- Fixed header: offset page content once, not with an arbitrary dead band.
- Touch targets: 44×44 px where practical; if a narrow header requires smaller icons,
  preserve the important account/menu action and keep spacing.
- Test at 320, 390, 768, 1024 and 1440 px; check 1920/2560/3840 for hero/3D framing.

---

## 5. Header, navigation and account

- Desktop nav is visible; mobile uses a real menu, not a hidden essential action.
- Every essential destination is reachable on mobile:
  home, catalogue, categories, cart, login/register, account/profile, contact.
- Signed-in state replaces "login" with "account" consistently.
- Menus close on navigation and outside click; they do not flicker when the pointer moves.
- Dropdowns need a small close delay and should remain open while the pointer is inside them.
- Account/profile links must not be hidden for space without an alternative visible entry point.
- Cart and search open as overlays with a shared, reference-counted scroll lock.
- Never leave the page scroll-locked after closing an overlay.

---

## 6. Motion

- Motion explains a change: entrance, hierarchy, state transition, spatial relationship.
- Durations: micro 120–200 ms, UI 200–360 ms, reveal 500–800 ms. Avoid slow decorative motion.
- Easing: one or two curves, used consistently.
- Animate opacity/transform, not layout where possible.
- Every overlay/route uses a stable transition; no flash between old and new snapshots.
- `prefers-reduced-motion`: disable non-essential animation, keep the interface usable.
- A splash/preload screen is optional, must respect the theme, must have a hard time cap and
  must never trap the page if hydration is slow.

---

## 7. 3D and media

- 3D only if it serves the product (showcase, configurator), never as decoration for its own sake.
- Lazy-load the 3D bundle; show a stable skeleton; provide a non-3D fallback.
- Cap DPR (`[1, 1.8]`), pause off-screen, and respect reduced motion.
- Camera framing must be responsive:
  - cap canvas height on very tall screens;
  - pull the composition back as the canvas aspect narrows;
  - verify the outermost object has margin at 1440/1920/2560/3840.
- Do not put essential text inside a `<canvas>`.
- Images: `next/image`, explicit aspect ratio, responsive `sizes`, no upscaled thumbnails,
  no runtime hotlinks, no generated placeholder imagery in production.
- Product/gallery lightbox must not crop the subject; use `contain` for full-view.

---

## 8. Forms

- Visible labels; placeholders are examples, not labels.
- Correct `autocomplete`, `inputMode`, `dir` and `type`.
- Validate on submit and on blur, not on every keystroke (unless the field benefits).
- Errors appear next to the field, announced with `role="alert"`.
- Preserve values after a failed submit.
- Loading state disables double submit and says what is happening.
- No auto-filling of a message body when a topic chip is selected.
- Password fields: show/hide control has its own space and never overlaps the placeholder/text.
- Success state states the reference/next step; no false claim of payment/email delivery.
- Honeypot/time-trap for public forms; server-side rate limit.

---

## 9. Content and states

- Empty states explain what to do, not just "no items".
- Loading states are skeletons or clear text, never a blank white area.
- Error states are human, specific and leave a way forward.
- Success states confirm what happened and what happens next.
- No fake testimonials, ratings, customer counts, urgency timers or "only 1 left" unless true.
- No legal/returns/privacy pages unless the brief asks; do not invent policies.
- Every page has a title, description, canonical URL and sensible Open Graph data.

---

## 10. Accessibility

- Keyboard reachable; visible focus ring.
- Semantic landmarks: header, nav, main, footer.
- One `h1` per page; heading order meaningful.
- Buttons are buttons; links are links.
- Images have useful alt text; decorative images empty alt.
- Modals trap focus and restore it on close.
- Color is not the only signal.
- Reduced motion respected.
- Form errors linked with `aria-describedby` and `aria-invalid`.

---

## 11. Frontend performance

- Server Components by default; small client islands.
- Avoid shipping large UI libraries for a single icon; import icons individually.
- Dynamic-import heavy canvas/editor/chart code.
- Preload only critical fonts; avoid layout shift.
- Do not render a huge list without pagination/virtualization.
- Defer non-critical third-party scripts; ideally none.
- Check the production build, not only dev.
- Target: first screen interactive quickly on a mid-range phone; no main-thread long tasks from
  unnecessary hydration.

---

## 12. Frontend review gate

Before declaring done:

- [ ] 320 / 390 / 768 / 1440 checked
- [ ] no horizontal overflow or clipped media
- [ ] 3D framing checked at 1440 / 1920 / 2560 / 3840
- [ ] header account and menu entry points visible on mobile
- [ ] overlays release scroll lock
- [ ] forms preserve values and never auto-fill unexpectedly
- [ ] FAQ/panels do not move the footer
- [ ] theme light/dark checked
- [ ] reduced motion checked
- [ ] keyboard/focus checked
- [ ] no console errors
- [ ] images optimized and no broken references
