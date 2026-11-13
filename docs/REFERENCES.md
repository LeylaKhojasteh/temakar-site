# REFERENCES.md — Approved Design and Motion Resources

A curated set of the resources the owner trusts. They are **research and implementation references**, not a
license to copy a brand, a page, or an entire library.

---

## Tier A — Installed skills and filters

These are loaded/available in the agent environment. Use them before and during design.

| Skill | Use it for | Status |
| --- | --- | --- |
| `design-taste-frontend` | Direction, composition, type, anti-slop house style, browser inspector | Installed at `C:\Users\Lenovo\.agents\skills\design-taste-frontend` |
| `antislop` | Mandatory filter: 40 rules, liveliness dials, Delivery Gate | Installed as DSH bundle `antislop-ai@3.2.28` |
| `antislop-ui` | Layout, color, components, decoration, motion, performance | Installed with antislop |
| `antislop-layoutmobile` | Reflow, breakpoints, grids, overflow, tap targets | Installed with antislop |
| `antislop-human` | Contrast, keyboard, focus, states | Installed with antislop |
| `antislop-copywriting` | Headlines, CTAs, fake-stat removal, tone | Installed with antislop |
| `animate-ui` | Motion primitives, springs, reduced motion, animated icons | Installed at `C:\Users\Lenovo\.agents\skills\animate-ui` |
| `frontend-design` | Distinctive direction, type, mood | Installed |
| `ui-ux-pro-max` | Styles, palettes, pairings, UX rules, stack patterns | Installed |
| `web-design-guidelines` | Accessibility and interface audit | Installed |
| `vercel-react-best-practices` | React/Next.js performance review | Installed |

**Order of use:** direction (`design-taste-frontend` / `frontend-design`) → pattern search
(`ui-ux-pro-max`) → build → `antislop` Delivery Gate → `web-design-guidelines` →
`vercel-react-best-practices` for perf-sensitive work.

`antislop` has two modes. For new projects use **DURING**; for an existing project use **AFTER**.
If the mode is not saved, ask once at the start. Announce the mode and its source.

---

## Tier B — Component, block and layout catalogues

Use these to study composition or to use a small piece. Do not add a whole library for one
component, and do not let a catalogue dictate the brand.

| Resource | What it is | Use it for | Cautions |
| --- | --- | --- | --- |
| [useLayouts](https://uselayouts.com/) | 69 free animated React/Motion/Tailwind components; copy-paste | Layout, navigation, interactions, cards | Adapt tokens; avoid copy-paste of the demo look |
| [AIMRAN Library](https://library.aimran.es/) | 814 animated HTML/CSS/React blocks; many categories | Loaders, inputs, navigation, cards, backgrounds | Huge catalogue; pick one, not a theme |
| [Watermelon UI](https://ui.watermelon.sh/home) | Open-source React components, blocks, dashboards, templates; MCP tooling | Dashboards, page sections, templates | Template look is generic; use structure, not skin |
| [Animata](https://animata.design/components) | 2.8k-star copy-paste animated components | Text motion, backgrounds, cards, preloaders | Motion can be decorative; purpose test required |
| [Aceternity UI](https://ui.aceternity.com/) | 118+ free, 200+ paid React/Tailwind/Motion components | Hero/background inspiration, occasional component | High slop risk: glows, beams, aurora, bento; use only with purpose; paid license |
| [Lumenite UI](https://lumeniteui.com/) | 182 animated components, 131 free, MIT-style free tier | Tactile cards, buttons, glass, commerce | High "premium AI" risk: spotlight, aurora, shimmer, meteors; use sparingly; Pro license |
| [Animate UI](https://animate-ui.com/) | Animated primitives for Radix/Base UI/React Aria; CLI; official skill | Accessible motion for shadcn-style primitives | Package adds Motion; verify version; don't mix with existing CSS animations |
| [MotionIn](https://motionin.design/) | Premium interactive sections with detailed motion specs | Motion study, scroll choreography | Very heavy GSAP/rAF; direct copy will hurt performance; study, don't transplant wholesale |

### Catalogue rules

1. No second component library with its own theme layer unless the project explicitly chooses it.
2. Strip the demo's brand-specific copy, fake testimonials, fake metrics and decorative gimmicks.
3. Verify accessibility, keyboard behavior and `prefers-reduced-motion` yourself; a catalogue demo is not QA.
4. Run the `antislop` rules: a glass/aurora/spotlight/bento pattern must serve identity or hierarchy, with a
   one-line reason, or it is rejected.
5. Do not copy a whole landing-page template; use it as a composition study.

---

## Tier C — Inspiration galleries

Use these to study rhythm, type, footers and CTAs. They are **not** component sources and must not be cloned.

| Resource | Focus |
| --- | --- |
| [Land-book](https://land-book.com/) | Landing-page composition and section rhythm |
| [Recent.design](https://recent.design/?ref=godly) | Contemporary visual direction |
| [CTA.gallery](https://www.cta.gallery/) | Calls to action and conversion copy |
| [Footer.design](https://www.footer.design/) | Footer structures and typographic treatments |
| [MotionIn](https://motionin.design/) | Motion language and scroll choreography (study only) |

### Gallery rules

- Pick **one** reference per page and name what you are taking: type scale, asymmetry, footer model, CTA placement.
- Never copy a site's layout, copy or brand assets. The result must survive the logo-swap test.
- Check mobile: the gallery screenshot is usually desktop; the mobile composition is your job.
- Do not reproduce a gallery's fake social proof, metrics, or "trusted by" rows.

---

## Tier D — Background and texture assets

| Resource | Use |
| --- | --- |
| [Grainient.supply](https://grainient.supply/) | Grain/gradient backgrounds as reference or licensed assets |
| [Backgrounds.supply](https://backgrounds.supply/) | Background packs as reference or licensed assets |

Rules:

- Check the license for commercial use and attribution.
- Download and optimize locally; never hotlink a third-party asset at runtime.
- A background must serve depth, brand or readability. A full-page gradient/orb because "it looks AI" is slop.
- Test contrast of text over the texture in both themes; no text over a moving/light-variable area.
- Prefer CSS gradients/noise generated in-house when that is lighter and sufficient.

---

## Brainstorming reference

The owner also referenced the **Brainstorming** skill on `aitmpl.com`. The page was not reachable during this
audit, so it is **not installed** and no unverified skill content is copied here.

Use a structured brainstorming step anyway, before any design:

1. State the product, audience and one concrete outcome.
2. Produce three distinct directions, not three color variants.
3. For each: idea, composition, type, palette, motion, risk.
4. Pick one with a one-line reason.
5. Write a Design Read: `page kind / audience / visual language / ENERGY RHYTHM MOTION`.

If the owner later provides the skill, review its license and content before installing it.

---

## Recommended combination per project

| Project type | Primary | Motion | Catalogue |
| --- | --- | --- | --- |
| Editorial brand site | `design-taste-frontend` + `frontend-design` | `animate-ui` or hand-written Motion | Animata / useLayouts |
| Product/app UI | `ui-ux-pro-max` + `web-design-guidelines` | `animate-ui` | Watermelon UI structure |
| Marketplace | `design-taste-frontend` | subtle Motion | useLayouts |
| Dashboard | `ui-ux-pro-max` | minimal | Watermelon UI dashboards |
| Experimental portfolio | `frontend-design` + MotionIn study | custom | Animata / Aceternity |

Whatever the combination, the final gate is `antislop` plus the project quality gate.
