# DESIGN.md — Design Direction and Taste

This is the taste layer: what the work should feel like, and what to refuse.

---

## 1. What the user values

- **Premium and intentional.** The site should look designed for this brand, not generated from
  a template.
- **Editorial restraint.** Strong type, generous spacing, one clear accent, no visual noise.
- **Real content.** Exact copy, real photos, real product facts. No lorem, demo labels or invented
  claims.
- **Mobile is equal.** Not a compressed desktop. Navigation, account, forms and 3D must be usable.
- **No clutter.** If a badge, tag, paragraph, animation or section does not add meaning, remove it.
- **Stable interfaces.** No jumping footers, no hidden primary actions, no overlays that trap scroll,
  no cropped product imagery.
- **Purposeful motion.** Fast, quiet, never decorative for its own sake.
- **Honest reporting.** Explain the cause of a bug and what was verified, not only the patch.

These preferences are part of the standard, not a one-project style.

---

## 2. Direction before decoration

Use the installed skills:

- **`design-taste-frontend`** — deal three directions with `scripts/draw.mjs`, choose the one that
  carries the product's idea, then build and inspect. Base directory on this machine:
  `C:\Users\Lenovo\.agents\skills\design-taste-frontend`.
  - `scripts/inspect.mjs` checks the house style in a real browser.
  - `scripts/scenes.mjs` checks scroll scenes at desktop, phone and reduced motion.
  - `scripts/lint.mjs` is the static gate.
  - It requires Node 22+ and installed Chrome/Edge/Chromium.
- **`antislop`** — mandatory filter on every UI task: 40 rules, liveliness dials and the Delivery Gate.
  Use DURING for new work, AFTER for audits. Load the relevant companion skills:
  `antislop-ui`, `antislop-layoutmobile`, `antislop-human`, `antislop-copywriting`.
- **`animate-ui`** — when the project needs accessible animated primitives, springs, tokens, reduced
  motion or animated icons. Installed at `C:\Users\Lenovo\.agents\skills\animate-ui`.
- **`frontend-design`** — when the brief needs a distinctive direction rather than a known style.
- **`ui-ux-pro-max`** — searchable styles, palettes, font pairings, UX guidelines and stack patterns.
- **`web-design-guidelines`** — accessibility and interface audit.
- **`vercel-react-best-practices`** — React/Next.js performance review.

The approved component catalogues, motion libraries, inspiration galleries and background suppliers are
listed in `REFERENCES.md`. Use them as references, adapt what you take to the project tokens, and still
run the anti-slop gate.

Do not skip straight to components. Choose the idea, type, palette and composition first.

---

## 3. House rules

- No generic "AI landing page": centered eyebrow + three feature cards + gradient blob + icon soup.
- No three equal cards by reflex; composition follows content.
- No decorative labels ("تجربهٔ متفاوت") without a concrete meaning.
- No fake social proof, counters, ratings or urgency.
- No glassmorphism/neon/glow unless the subject genuinely calls for it.
- No second accent color introduced casually.
- No font pair chosen only because it is popular.
- No tiny type for essential information; no uppercase Persian as a style trick.
- No animation on every element; motion should mark a state change.
- No desktop-only hover interactions; provide touch equivalents.
- No hidden account/login path on mobile.
- No layout that shifts when an answer/panel opens; reserve space.
- No auto-filled form messages or "smart" behavior that overrides the user.
- No 3D that is cropped, too small, too heavy or blocks the first screen.

---

## 4. Composition

- A page is a sequence of clearly different zones, not repeated cards.
- The first screen establishes the idea: one headline, one supporting line, one action,
  one visual world.
- Use full-width bands, asymmetric grids or editorial columns where the subject supports it.
- Keep a consistent vertical rhythm and content width.
- Use whitespace as structure; do not fill every gap.
- Every section has one job and one primary action at most.

---

## 5. Typography and color

- One display face and one text face, or one versatile variable family.
- Strong scale contrast: display / h1 / h2 / body / small.
- Body line length 55–70 characters for Latin; tune for Persian.
- Prices and quantities use tabular numerals.
- Palette: one dominant surface, one text color, one accent, one line color.
  Themes change values, not structure.
- Verify contrast and thin strokes at the smallest rendered size.
- Persian text must be shaped, kerned and spaced by a native reader's eye.

---

## 6. Imagery and 3D

- Use owner-supplied imagery where possible; if unavailable, say so instead of inventing.
- One visual language: crop ratio, color grade, background treatment consistent.
- No stock-photo clichés; no AI-generated product shots presented as real.
- 3D: purposeful, lazy-loaded, stable skeleton, capped DPR, responsive framing.
- Verify the outermost object is fully inside the canvas at wide/large monitors.
- Full-view image lightboxes use `contain`, not `cover`.

---

## 7. Mobile art direction

- Recompose, do not shrink. Headline size, spacing, image crop and section order may change.
- Keep primary actions above the fold where possible.
- Header: logo, essential actions and a visible account/menu path.
- Filters, category rails and product grids adapt without horizontal page overflow.
- Forms are single-column, with labels and 44px targets.
- 3D scales without clipping and does not push the main content below the first viewport.
- Preload/splash screens are short, themed and never block indefinitely.

---

## 8. Motion language

- Entrance: short fade/translate, 300–700 ms.
- State change: 150–350 ms.
- Page/overlay: one consistent curve.
- No long decorative intros; no animation that delays reading.
- Respect `prefers-reduced-motion`.
- Verify no flash/skew when deployments change assets.

---

## 9. Design review

- Look at screenshots at 390 and 1440, plus the 3D at 3840.
- Ask: does it look like this subject, or like a generic premium template?
- Remove one thing; if nothing is lost, it was decoration.
- Check the smallest text/hairline is visible.
- Check the footer does not move when panels open.
- Check the primary action is visible without hunting.
- Run the accessibility/interface audit before calling it done.

---

## 10. Design anti-patterns

- Version-named route groups that leak into the product structure.
- A hidden account icon on mobile to save 44 px.
- Auto-filling a contact message from a topic chip.
- FAQ answers in a separate panel below all questions with a fixed min-height.
- A 3D hero that is cropped on tall monitors.
- A preloader that waits on hydration without a hard timeout.
- Reserving space by leaving an unexplained blank area without telling the user why.
- "Demo" copy in a portfolio piece that is meant to look real.
