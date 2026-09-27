# DESIGN.md - UI guidance for the AI Buddy

> Read this before touching `frontend/`. The goal is to ship a UI that looks like a thoughtful student product, not a tutorial demo. Level 2 of the evaluation explicitly rewards UX, polish, mobile-friendliness, and **creativity** (see `BRIEF.md`, section 7), so good UI is not cosmetic - it's points.

## Important: this is a starting point, not a template

If every project at the event ships the same chat-on-the-left / sources-on-the-right layout in a cream-and-charcoal palette, the room sees through it. Level 2 lists `creativity` as its own scored axis, alongside `user experience`, `interactivity`, `product quality`. The defaults below are meant to spare you a from-scratch UI - they are NOT meant to be copied wholesale.

**Pick at least 2-3 of these variation axes and diverge** before you submit:

- **Palette**: replace the placeholder oklch values below with something tied to *your* concept (warm academic, cold institutional, vibrant student-life, monochrome with one accent, brutalist black-and-white). Don't ship the default tokens.
- **Typography pairing**: Fraunces + Inter is *one* option. Tiempos + IBM Plex, Playfair + Sohne, Bricolage + General Sans, Editorial New + Suisse all work. The pairing tells the user what kind of buddy this is - pick deliberately.
- **Layout metaphor**: a chat is the fastest path, but the brief explicitly lists alternatives - dashboard, guided journey, sectioned planner, interactive map, timeline, card-deck, onboarding flow. A non-chat layout is automatically more memorable to a judge who has just seen 30 chats.
- **Density and rhythm**: tight Bloomberg-terminal vs roomy editorial vs Apple-marketing-airy. Pick one and commit.
- **Motion**: from zero to subtle hover pulses to full Framer Motion entrances. Zero is fine; what is NOT fine is half-implemented motion that flickers.
- **Illustrations / iconography**: `lucide` icons are fine and free, but commodity. A small custom set (4 verticale glyphs + a hero illustration) is one of the cheapest ways to lift the perceived quality.

If you do nothing else from this file, do this: do not ship the default palette and the default Inter / Fraunces pairing as-is, and do not default to chat-on-the-left if your concept can do something more interesting.

## Default look and feel (one of many)

Editorial, calm, university-grade. The user is a Bocconi student opening this on their laptop or phone. The product is a knowledgeable assistant they trust to answer with sources. Two moves apply regardless of the visual direction you pick:

1. **Confident typography**: one display font for headings, one body font, generous letter-spacing for small uppercase labels (eyebrows / section tags). Don't ship a UI that uses Inter at 14px for everything.
2. **Sources are first-class**: every answer must show *what* it cited (file paths, links). Render them as a structured element next to, below, or revealed-on-tap from the answer, not as a scrappy footnote.

## Stack

- **shadcn/ui** as the base, already de-facto for hackathons. Init with `pnpm dlx shadcn@latest init` and add components with `pnpm dlx shadcn@latest add <component>` (start with `button`, `input`, `textarea`, `card`, `scroll-area`, `badge`, `separator`). Don't hand-roll a button.
- **Tailwind v4 CSS-first**: tokens go in `frontend/src/index.css` under `@theme inline { ... }`. Do NOT create a `tailwind.config.ts`, v4 doesn't need it.
- **TypeScript strict** is already on. Don't loosen it.
- **Mobile-first**: the room votes from phones. Layout works at 360px wide before you add desktop niceties.

## Tokens (paste this into `frontend/src/index.css`, then change them)

The structure below is what makes shadcn components feel coherent - keep that. The *values* are placeholders, change them before you submit. See the "variation axes" at the top of this file.

```css
@import "tailwindcss";

@theme inline {
  --color-background: oklch(0.99 0 0);
  --color-foreground: oklch(0.18 0.02 250);
  --color-muted: oklch(0.96 0.01 250);
  --color-muted-foreground: oklch(0.45 0.02 250);
  --color-accent: oklch(0.55 0.18 25);
  --color-accent-foreground: oklch(0.99 0 0);
  --color-border: oklch(0.92 0.01 250);

  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-display: "Fraunces", "Georgia", serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
}

body {
  font-family: var(--font-sans);
  background: var(--color-background);
  color: var(--color-foreground);
}
```

## One possible layout (chat + sources panel)

This is *one* layout. If you have a more interesting concept (dashboard, journey, map, planner) skip this section. If you don't have a concept yet, this is a safe baseline:

```
+----------------------------------------------------+
| Header: small logo, product name, brand tagline    |
+----------------------------------------------------+
|                                                    |
|  Chat thread         |  Sources / context          |
|  (left, 2/3)         |  (right, 1/3)               |
|                      |                             |
|  - User question     |  - File paths cited         |
|  - Assistant answer  |  - Verticale tag            |
|  - "thinking..."     |  - Open-original links      |
|                      |                             |
+----------------------------------------------------+
| Composer: input + send + verticale chips           |
+----------------------------------------------------+
```

On mobile (`< 768px`), collapse the sources panel into an expandable section under each answer.

Stronger creative directions if you have time and want Level 2 to notice you:

- **4-card landing** (one per verticale) that pre-fills the chat with a verticale-specific question.
- **Interactive Milan map** for `relocation` - neighborhoods, transport zones, rent ranges from Numbeo.
- **Visual timeline** for `study_abroad` - exchange application deadlines as a horizontal scrolling band.
- **Onboarding journey** for international first-years (visa -> codice fiscale -> housing -> SIM -> health card) where each step is a chat-with-a-purpose.
- **Dashboard / planner** with the buddy folded into one panel and other panels showing student-life data (events this week, library hours, dining today).

Pick one that fits your concept, ship it well, and skip the rest.

## Editorial details to ship by default

These cost about 10 minutes total and visibly lift the perceived quality:

- **Eyebrow labels**: small uppercase tags with `tracking-[0.18em] text-xs text-muted-foreground` above section titles ("LIFE ON CAMPUS", "RELOCATION", "SOURCES").
- **Display headings**: use `font-display` for `h1` and `h2`.
- **Verticale badges**: one color per verticale, used consistently. Pick from the `--color-accent` family + 3 muted variants.
- **Empty state**: first time the user opens the app, don't show an empty box. Show 3-4 example questions as clickable chips.
- **Loading state**: when waiting for `/ask`, show a subtle "thinking..." with the verticale being detected. Cap perceived latency.
- **Error state**: if `/ask` fails, show a calm message with a "Try again" button, NOT a red toast that says "Network error 500".

## Accessibility minimum

- All inputs labelled (use `<Label>` from shadcn or `aria-label`).
- Buttons reachable by Tab. Enter submits the composer.
- Color contrast >= 4.5:1 for body text. Run a quick check before submitting.
- Don't rely on color alone to communicate the verticale: badge + label.

## What to avoid

- Floating gradient blobs / glassmorphism / neon: reads as "ChatGPT wrapper #4192".
- Dumping all 4 verticali into one giant home page with marketing copy.
- Custom fonts loaded from 5 CDNs: one display + one body is enough.
- Building a desktop-first layout and squeezing it on mobile.
- Shipping the placeholder `<div>Build me</div>`: the judges WILL see it.

## When the student asks "make the UI nicer"

Don't ask back "what do you have in mind?". Pick ONE concrete move:

1. Add the sources panel if it's missing.
2. Replace the chat composer with a shadcn `<Textarea>` + send button + verticale chips.
3. Add the 4-card landing page that opens the chat with a pre-filled question.
4. Add display typography (`font-display`) on the hero + eyebrow labels on each section.

Show what you did, ask if the direction feels right, then iterate. Don't ship 5 changes at once - one move per turn keeps the student in the loop.
