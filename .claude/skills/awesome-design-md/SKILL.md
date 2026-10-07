---
name: awesome-design-md
description: Apply a real-world design system from the Awesome DESIGN.md collection (74 DESIGN.md files extracted from sites such as Stripe, Linear, Vercel, Apple, Notion, Nike). Use when asked to make UI "look like <brand>", to use, pick or add a DESIGN.md, to match a known site's design language, or when a new page or app needs a consistent, high-quality visual system instead of a generic look.
---

# Awesome DESIGN.md

A DESIGN.md is a plain-text design system in the Google Stitch DESIGN.md format: colors with
semantic roles, typography hierarchy, component styling with states, layout and spacing scale,
depth and elevation, do's and don'ts, responsive rules, and an agent prompt guide. Coding agents
read it to produce UI that stays visually consistent.

This skill bundles 74 of them, extracted from real websites by VoltAgent/awesome-design-md,
at `references/<slug>/DESIGN.md` (relative to this skill's directory). Nothing is loaded until you
open a file, so pick one, then read it in full.

## How it works

1. Pick a design system from the catalog below. Match the brand the user named; when the user only
   gives a vibe, choose by the catalog description (see the hints under "Choosing by vibe").
2. Read the whole `references/<slug>/DESIGN.md` before writing any UI code. The one-line catalog
   entry is not enough to build from.
3. Decide the scope with the user's request in mind:
   - One-off task: follow the file for this task only.
   - Adopting it for the project: copy the file to the project root as `DESIGN.md` (the location
     Stitch and coding agents look for) and tell the user you did so. Keep only one `DESIGN.md`
     at the root.
4. Build with the file's actual tokens: the exact hex values and their roles, the font families
   and type scale, the spacing scale, component states, shadow and elevation rules, and the
   Do's and Don'ts. The "Agent Prompt Guide" section at the end of each file has ready-to-use
   prompt snippets and a quick color reference.
5. Keep to one system per UI. Mixing two systems usually reads as generic, which defeats the
   point. If the user wants a blend, say which file is the base and borrow only named tokens.
6. Use these files for design language only: palette, type, spacing, component behavior. Do not
   reproduce a brand's logo, name, or trademarked assets, and do not build something that could
   be mistaken for the real site.

## Choosing by vibe

- Dark developer tool, precise and dense: `linear.app`, `vercel`, `raycast`, `supabase`, `warp`, `cursor`
- Warm editorial, calm, readable: `notion`, `claude`, `mintlify`, `cal`
- Premium consumer, photography-led: `apple`, `airbnb`, `nike`, `tesla`
- Fintech trust, clean and structured: `stripe`, `wise`, `coinbase`, `revolut`
- Bold, high-energy brand: `spotify`, `nvidia`, `binance`, `ferrari`, `bmw-m`
- Playful SaaS: `lovable`, `figma`, `miro`, `zapier`, `posthog`
- Magazine and media: `wired`, `theverge`
- Retro web: `dell-1996`, `nintendo-2001`

## Catalog

Each entry is `**Name** (slug)`; the file is `references/<slug>/DESIGN.md`.

### AI & LLM Platforms

- **Claude** (`claude`): Anthropic's AI assistant. Warm terracotta accent, clean editorial layout
- **Cohere** (`cohere`): Enterprise AI platform. Vibrant gradients, data-rich dashboard aesthetic
- **ElevenLabs** (`elevenlabs`): AI voice platform. Dark cinematic UI, audio-waveform aesthetics
- **Minimax** (`minimax`): AI model provider. Bold dark interface with neon accents
- **Mistral AI** (`mistral.ai`): Open-weight LLM provider. French-engineered minimalism, purple-toned
- **Ollama** (`ollama`): Run LLMs locally. Terminal-first, monochrome simplicity
- **OpenCode AI** (`opencode.ai`): AI coding platform. Developer-centric dark theme
- **Replicate** (`replicate`): Run ML models via API. Clean white canvas, code-forward
- **Runway** (`runwayml`): AI creative-tools platform with an editorial film-festival aesthetic — cinematic dark heroes, paper-white reading bands, single proprietary sans, and pure black pill CTAs
- **Together AI** (`together.ai`): Open-source AI infrastructure. Technical, blueprint-style design
- **VoltAgent** (`voltagent`): AI agent framework. Void-black canvas, emerald accent, terminal-native
- **xAI** (`x.ai`): Elon Musk's AI lab. Stark monochrome, futuristic minimalism

### Developer Tools & IDEs

- **Cursor** (`cursor`): AI-first code editor. Sleek dark interface, gradient accents
- **Expo** (`expo`): React Native platform. Dark theme, tight letter-spacing, code-centric
- **Lovable** (`lovable`): AI full-stack builder. Playful gradients, friendly dev aesthetic
- **Raycast** (`raycast`): Productivity launcher. Sleek dark chrome, vibrant gradient accents
- **Superhuman** (`superhuman`): Fast email client. Premium dark UI, keyboard-first, purple glow
- **Vercel** (`vercel`): Frontend deployment platform. Black and white precision, Geist font
- **Warp** (`warp`): Modern terminal. Dark IDE-like interface, block-based command UI

### Backend, Database & DevOps

- **ClickHouse** (`clickhouse`): Fast analytics database. Yellow-accented, technical documentation style
- **Composio** (`composio`): Tool integration platform. Modern dark with colorful integration icons
- **HashiCorp** (`hashicorp`): Infrastructure automation. Enterprise-clean, black and white
- **MongoDB** (`mongodb`): Document database. Green leaf branding, developer documentation focus
- **PostHog** (`posthog`): Product analytics. Playful hedgehog branding, developer-friendly dark UI
- **Sanity** (`sanity`): Headless content platform with a dark-first editorial marketing surface — 112px display type, IBM Plex Mono technical eyebrows, and a single coral-red accent reserved for the highest-priority CTA
- **Sentry** (`sentry`): Error monitoring. Dark dashboard, data-dense, pink-purple accent
- **Supabase** (`supabase`): Open-source Firebase alternative. Dark emerald theme, code-first

### Productivity & SaaS

- **Cal.com** (`cal`): Open-source scheduling. Clean neutral UI, developer-oriented simplicity
- **Intercom** (`intercom`): Customer messaging. Friendly blue palette, conversational UI patterns
- **Linear** (`linear.app`): Project management for engineers. Ultra-minimal, precise, purple accent
- **Mintlify** (`mintlify`): Documentation platform. Clean, green-accented, reading-optimized
- **Notion** (`notion`): All-in-one workspace. Warm minimalism, serif headings, soft surfaces
- **Resend** (`resend`): Email API for developers. Minimal dark theme, monospace accents
- **Zapier** (`zapier`): Automation platform. Warm orange, friendly illustration-driven
- **Slack** (`slack`): Workplace messaging. Deep aubergine primary, cream-lavender hero gradients, blue inline links, pill CTAs

### Design & Creative Tools

- **Airtable** (`airtable`): Spreadsheet-database hybrid. Colorful, friendly, structured data aesthetic
- **Clay** (`clay`): Creative agency. Organic shapes, soft gradients, art-directed layout
- **Figma** (`figma`): Collaborative design tool. Vibrant multi-color, playful yet professional
- **Framer** (`framer`): Website builder. Bold black and blue, motion-first, design-forward
- **Miro** (`miro`): Visual collaboration. Bright yellow accent, infinite canvas aesthetic
- **Webflow** (`webflow`): Visual web builder. Blue-accented, polished marketing site aesthetic

### Fintech & Crypto

- **Binance** (`binance`): Crypto exchange. Bold Binance Yellow on monochrome, trading-floor urgency
- **Coinbase** (`coinbase`): Crypto exchange. Clean blue identity, trust-focused, institutional feel
- **Kraken** (`kraken`): Crypto trading platform. Purple-accented dark UI, data-dense dashboards
- **Mastercard** (`mastercard`): Global payments network. Warm cream canvas, orbital pill shapes, editorial warmth
- **Revolut** (`revolut`): Digital banking. Sleek dark interface, gradient cards, fintech precision
- **Stripe** (`stripe`): Payment infrastructure. Signature purple gradients, weight-300 elegance
- **Wise** (`wise`): International money transfer. Bright green accent, friendly and clear

### E-commerce & Retail

- **Airbnb** (`airbnb`): Travel marketplace. Warm coral accent, photography-driven, rounded UI
- **Meta** (`meta`): Tech retail store. Photography-first, binary light/dark surfaces, Meta Blue CTAs
- **Nike** (`nike`): Athletic retail. Monochrome UI, massive uppercase Futura, full-bleed photography
- **Shopify** (`shopify`): E-commerce platform. Dark-first cinematic, neon green accent, ultra-light display type
- **Starbucks** (`starbucks`): Coffee retail flagship. Four-tier earth-green system, warm cream canvas, proprietary SoDoSans typography

### Media & Consumer Tech

- **Apple** (`apple`): Consumer electronics. Premium white space, SF Pro, cinematic imagery
- **HP** (`hp`): PC and printer maker. Pure white canvas, HP Electric Blue signal CTA, geometric Forma DJR Micro, blue chevron decorations
- **IBM** (`ibm`): Enterprise technology. Carbon design system, structured blue palette
- **NVIDIA** (`nvidia`): GPU computing. Green-black energy, technical power aesthetic
- **Pinterest** (`pinterest`): Visual discovery platform. Red accent, masonry grid, image-first
- **PlayStation** (`playstation`): Gaming console retail. Three-surface channel layout, cyan hover-scale interaction
- **SpaceX** (`spacex`): Space technology. Stark black and white, full-bleed imagery, futuristic
- **Spotify** (`spotify`): Music streaming. Vibrant green on dark, bold type, album-art-driven
- **The Verge** (`theverge`): Tech editorial media. Acid-mint and ultraviolet accents, Manuka display type
- **Uber** (`uber`): Mobility platform. Bold black and white, tight type, urban energy
- **Vodafone** (`vodafone`): Global telecom brand. Monumental uppercase display, Vodafone Red chapter bands
- **WIRED** (`wired`): Tech magazine. Paper-white broadsheet density, custom serif, ink-blue links

### Automotive

- **BMW** (`bmw`): Luxury automotive. Dark premium surfaces, precise German engineering aesthetic
- **BMW M** (`bmw-m`): Performance automotive. Motorsport-inspired contrast, M color accents, precision-driven layout
- **Bugatti** (`bugatti`): Luxury hypercar. Cinema-black canvas, monochrome austerity, monumental display type
- **Ferrari** (`ferrari`): Luxury automotive. Chiaroscuro black-white editorial, Ferrari Red with extreme sparseness
- **Lamborghini** (`lamborghini`): Luxury automotive. True black cathedral, gold accent, LamboType custom Neo-Grotesk
- **Renault** (`renault`): French automotive. Vivid aurora gradients, NouvelR proprietary typeface, zero-radius buttons
- **Tesla** (`tesla`): Electric vehicles. Radical subtraction, cinematic full-viewport photography, Universal Sans

### Retro Web · DESIGN.md Nostalgia

- **Dell (1996)** (`dell-1996`): Catalog-era enterprise web. Literal black page frame, flat color-block "ribbon cards", chunky Helvetica-Black titles over Times Roman body, and hand-cut GIF stickers (NEW! bursts, award seals, beveled product photos)
- **Nintendo.com (2001)** (`nintendo-2001`): Y2K "console chrome" web. Brushed-periwinkle beveled metal panels, a halftone-dotted carbon nav glowing amber, outlined Arial-Black box-art wordmarks over circuit-board hero fields, and a pixel Mario welcome bubble
