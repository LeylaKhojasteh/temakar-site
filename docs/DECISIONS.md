# DECISIONS.md — Decision Log

Record decisions that would otherwise be re-litigated in chat. One short entry per decision.

Use this format:

```md
## YYYY-MM-DD — Decision title

**Context:** why a decision was needed.

**Decision:** what we chose.

**Alternatives:** what we rejected and why.

**Consequences:** trade-offs, follow-up work, review date.
```

Examples of decisions that belong here:

- choosing a stack or database;
- a non-obvious data model or order state machine;
- accepting a third-party service;
- a deliberate exception to this standard;
- a security trade-off with a documented reason and owner.

Do not use this file for task lists or progress updates.

---

## 2026-11-11: Django instead of the standard Next.js/Prisma stack

**Context:** `STANDARD.md` prefers Next.js + Prisma. `PRODUCT.md` requires Django 5 +
PostgreSQL + Django templates + Tailwind + a little HTMX, one service, one deploy.

**Decision:** Django, per the brief. Authority order: explicit user instruction > project
brief > standard.

**Alternatives:** Next.js was rejected because the brief forbids React/Next and a separate
frontend.

**Consequences:** the standard's `npm run build / tsc` gate is replaced by
`manage.py check --deploy`, `ruff`, and `pytest`. Documented in `README.md`.

## 2026-11-11: A small i18n dictionary instead of gettext `.po` files

**Context:** neither `xgettext` nor `msgfmt` is installed on the Windows development machine,
and the site has two complete languages plus DB-backed bilingual content.

**Decision:** UI strings live in `apps/core/i18n.py` as an explicit dict with a `tr` template
tag. Django i18n (`LocaleMiddleware`, `i18n_patterns`) still handles the URL prefix and the
active language. Content stays in `_en` / `_fa` model fields.

**Alternatives:** hand-written `.po` files compiled by a custom script (fragile, another build
step, silent English fallback when a msgid is missing); installing gettext system-wide
(unrequested machine change, not reproducible for the owner).

**Consequences:** no pluralization support (not needed here); a test asserts every key has
both languages. Revisit if the project adds a third language or real plural forms.

## 2026-11-11: One Latin slug per entity, shared by both languages

**Context:** the brief lists one `نامک` field per model, and routes show
`/fa/our-services/<دسته>`. Two slugs per entity would double the maintenance and risk
broken links between languages.

**Decision:** a single ASCII slug, used under both `/` and `/fa/`.

**Alternatives:** translated Persian slugs (need `allow_unicode` and duplicate fields, and
copy-pasted URLs become unreadable).

**Consequences:** the language switcher can map a page to its counterpart by only changing
the prefix, and `sitemap.xml` alternates stay trivial.

## 2026-11-11: SQLite is a local-only switch

**Context:** the owner must create the PostgreSQL database and provide credentials; meanwhile
the templates and tests need to be verifiable.

**Decision:** `USE_SQLITE=1` in `dev.py` switches to a local SQLite file. Production settings
never read it. Tests use `config.settings.test` with in-memory SQLite.

**Consequences:** SQLite is not the product database; the Postgres migration still has to run
once credentials exist. Remove the switch when the local Postgres is ready.

## 2026-11-11: Rate limiting lives in the database, keyed by hashed IP

**Context:** a single service on Render/Railway has no Redis. The standard allows an
in-memory limiter only when documented.

**Decision:** count `ContactMessage` rows per `ip_hash` inside a time window. The raw IP is
never stored.

**Alternatives:** in-memory limiter (resets on restart, not shared across workers); adding
Redis (a second service for one form).

**Consequences:** best-effort protection only; a real WAF or proxy rate limit is still the
stronger control. `X-Forwarded-For` is trusted, so the proxy must overwrite it.

## 2026-11-11: Quill for rich text with server-side sanitization

**Context:** the owner asked for a rich text editor (bold, lists, links) for service bodies.

**Decision:** self-hosted Quill 2 in the admin only; HTML is sanitized with `nh3` on save,
and the template renders it with `|safe`.

**Alternatives:** CKEditor/TinyMCE packages (extra dependency, CDN or API keys); plain
paragraphs (rejected by the owner).

**Consequences:** admin JS needs a small CSP exception; allowed tags are fixed in
`apps/core/richtext.py` and must be extended deliberately.

## 2026-11-11: Strict CSP without a nonce, admin-only exception

**Context:** public pages load only local CSS/JS, so no inline script is needed. Django admin
and Quill do use inline styles/scripts.

**Decision:** public CSP has no `unsafe-inline`; `/admin/` gets a documented looser policy.
HTMX's injected indicator style is disabled with a `htmx-config` meta tag.

**Consequences:** any future inline style on a public page will fail loudly, which is the
point. Add a nonce mechanism only if a real inline script becomes necessary.

## 2026-11-11: Fixed light theme, no dark toggle

**Context:** `PRODUCT.md` explicitly excludes dark mode and a theme switch. The antislop
R-21 heuristic would prefer a toggle when no strong reason exists.

**Decision:** one warm light theme, documented as an explicit owner instruction, which wins
over the heuristic.

**Consequences:** the color tokens are theme-ready (`data-theme` could be added later) but no
toggle ships.

## 2026-11-11: Fonts: Estedad for Persian, Libre Franklin + Source Serif 4 for English

**Context:** the dealt direction (`type-only-statement`) supplied a Latin pair that has no
Persian glyphs. The brief requires genuinely Persian typography.

**Decision:** English uses the dealt pair; Persian uses Estedad (OFL, variable). All fonts are
self-hosted and preloaded per language.

**Consequences:** the inspector's "font not dealt" warning appears on Persian pages by design;
this is a documented adaptation, not a fallback to a default face.

## 2026-11-11: Demo content is explicit placeholder content

**Context:** the owner asked to number demo services (`خدمت ۱`, `خدمت ۲`) and replace them
later, and allowed demo imagery.

**Decision:** names and body text are clearly placeholder (`خدمت ۱`, «متن نمونه»). Demo
photographs are free-licence Unsplash images stored locally, listed in
`static/img/demo/SOURCES.md`, used as atmosphere and never described as Temakar's own work.
No statistics, clients, certificates or dates are invented.

**Consequences:** the site looks like a demo until content is replaced through the admin;
`docs/COPY-DRAFT.md` lists every string that needs owner approval.

## 2026-11-11: Google Maps embed in the footer and contact page

**Context:** `PRODUCT.md` mentions a map link without a heavy embed, but the owner explicitly
asked for a Google Map in the footer and on the contact page.

**Decision:** one lazy-loaded iframe per page, 16:9 or 21:9 with reserved space, plus an
external link as fallback. No API key; `frame-src` allows only Google Maps hosts.

**Consequences:** third-party content inside an iframe; it is lazy, has a title, and the page
stays usable if it fails to load. Revisit if a keyed Maps Embed API is preferred.

## 2026-11-11: Email notification deferred, message is always stored

**Context:** the owner wants email sending eventually but asked to postpone its details.

**Decision:** every message is saved to the database and visible in the admin. Email is sent
only when `CONTACT_NOTIFY_EMAIL` and an SMTP backend are configured; the UI never claims an
email was delivered.

**Consequences:** enable email later by environment variables only, no code change.


## 2026-11-11: A project-local Postgres cluster for development

**Context:** the product database is PostgreSQL, but the installed server on this machine
required a superuser password that the owner had not provided, so the project was running
on a temporary SQLite switch.

**Decision:** `scripts/dev-db.ps1` creates and runs a separate PostgreSQL 18 cluster in
`.pgdata/` on port `5439`, user `temakar`, with `trust` authentication limited to
`127.0.0.1`. Logging goes to `.pgdata/log/`. Production never uses this cluster.

**Alternatives:** asking for the system superuser password again (blocked the build);
SQLite for the whole build (diverges from the product engine).

**Consequences:** the development database must be started after a reboot
(`.\scripts\dev-db.ps1 start`); `.pgdata/` is git-ignored and disposable. The full test
suite passes on both SQLite (`pytest`) and PostgreSQL (`TEST_DB=postgres pytest`).


## 2026-11-12: Redesign toward a poster direction with a technical illustration

**Context:** the owner rejected the first visual direction as dry. The brief asked for a
graphic, animated page; the first build had a type-only hero, an orange accent and a giant
word band that the owner asked to remove.

**Decision:** adopt the dealt "Loud and flat" poster direction (seed 1239267070) with a
redrawn palette in the blue/gray/yellow family the owner named: deep navy fields, a cool
paper ground and one safety-yellow action. The hero pairs a short two-line headline with an
isometric structure drawn in code (SVG, 67 elements, strokes animate in, slow drift, pointer
parallax). Inner pages open with a photographic masthead and a navy panel that overlaps it.
Sections alternate flat fields: navy, paper, ink, yellow, blue.

**Alternatives:** the dealt Epilogue-only palette (cream/coral/green) conflicted with the
owner's palette constraint; the "name as monument" direction would have made the headline
larger, against the explicit request for a smaller, calmer h1.

**Consequences:** the SVG is generated by `scripts/generate_hero_svg.py` and inlined by
`templates/partials/hero_art.html`; its styles are element attributes so the strict CSP
never blocks them. Persian keeps Estedad and English uses Epilogue, so the inspector's
"font not dealt" warning stays on Persian pages by design.

## 2026-11-12: Owner-requested removals

**Context:** direct instructions from the owner after reviewing the first build.

**Decision:** the header loses its contact button (the menu keeps one); the footer loses the
language switch; the language link reads "EN"/"FA"; working hours leave the contact page;
the full-width contact word band is replaced by a compact blue panel with a button; the
footer map is 320px wide with `z=16` (a third of its former size, zoomed in).

**Consequences:** `SiteSettings.hours_*` still exists in the admin for future use but is no
longer rendered. The language switch is now only in the header and the mobile menu.


## 2026-11-12: Blue and grey palette, calmer type, real content

**Context:** the owner rejected the blue and yellow pairing as unrefined and asked for blue and
grey, a smaller language switch, no oversized type on the services page, and removal of the
closing contact band. They also supplied the company's real English copy and four services.

**Decision:** the yellow accent is gone; the palette is now deep navy, cool paper, ink and one
blue accent with a light blue step for text on dark panels. The services list drops from 57px to
32px on desktop and 18px on phones. The language switch is 38x34 with a one-pixel border. The
"do you have a project" band is removed from every page. Real content is imported by
`seed_content`, which deactivates (never deletes) the old demo rows.

**Consequences:** every page now carries one photograph (its masthead) until the owner supplies
company photos, so the inspector's four-picture floor fails on all of them; this is expected and
recorded in `docs/QA-REPORT.md`. Working hours return to the contact page and footer because the
owner's new copy includes them, superseding the earlier removal request. The model gained
`title_fa` as optional and `SiteSettings.phone_secondary`; Persian content falls back to English
until translations arrive.


## 2026-11-12: Services are flat, and the copy is bilingual

**Context:** the owner said the category and service layers are unnecessary, that each of the four
services is a peer, and asked for professional Persian translations written by the agent.

**Decision:** the `ServiceCategory` model and the `category` field are removed (migration 0003);
each service is a single record with a globally unique slug and lives at
`/our-services/<slug>/`. The services page lists the four services once, with an animated
two-dimensional logo per service instead of a summary. The header gained a services dropdown with
the same four links. Persian copy for the about page, mission, vision and all four service bodies
is written by the agent as a faithful translation and can be edited in the admin.

**Consequences:** the HTMX category filter and the category pages are gone; the brief's two-level
model is superseded by an explicit owner instruction, recorded here. The empty demo records are
deactivated. Persian pages fall back to English only where a Persian field is still empty.


## 2026-11-13: A colour rhythm instead of adjacent dark fields

**Context:** the owner saw the home's "what we do" section merging into the footer, and the about
page splitting into a light top and a dark bottom.

**Decision:** the palette is treated as three base surfaces plus one accent: paper, paper two, ink,
plus the navy used for image panels and the blue accent. Two large dark fields never touch: the
services list now sits on the second paper surface, the footer is the only ink field on the home,
and the vision panel on the about page is light with its own summit graphic. The accent survives in
buttons, link hovers and the single closing call-to-action band. Working hours are removed from the
model and the contact page; the contact map now sits under the address block instead of a separate
section. The services menu keeps its 380ms entrance but uses `display` so a closed menu is out of the
accessibility tree and out of the inspector's text scan.


## 2026-11-16: The hero becomes a still photograph with moving clouds

**Context:** the owner supplied a poster and a ten second cloud clip and asked to drop every
previous hero effect.

**Decision:** the halo, grid, streaks and haze are removed together with their markup and styles.
The hero shows the poster first, then sets the video source and plays it muted, inline and looped;
the video fades in only when playback actually starts, so there is never a black frame. Both layers
use `object-fit: cover` with the same position, and the hero's aspect keeps the frame from jumping.
With `prefers-reduced-motion` the source is never set and no video request is made. If autoplay is
blocked or the file fails, the poster simply stays.
