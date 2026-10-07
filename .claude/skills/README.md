# Project skills

Agent skills installed into this repository for Claude Code (and any other agent that reads
`.claude/skills/`). Each directory holds one skill. Claude Code reads the `SKILL.md` frontmatter
at startup and loads the body only when the skill is used, so unused skills cost almost nothing.
Run `/skills` in Claude Code to list them, toggle them, or confirm they loaded.

| Skill | Invoke | What it does | Upstream source |
|---|---|---|---|
| `design-taste-frontend` | `/design-taste-frontend` | Taste Skill v2: anti-slop frontend design for landing pages, portfolios and redesigns | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) `skills/taste-skill/SKILL.md` |
| `image-to-code` | `/image-to-code` | Generate design reference images first, analyze them, then implement the site to match | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) `skills/image-to-code-skill/SKILL.md` |
| `web-design-guidelines` | `/web-design-guidelines <file-or-pattern>` | Audit UI code against Vercel's Web Interface Guidelines (accessibility, forms, animation, performance, theming) | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) `skills/web-design-guidelines/SKILL.md` |
| `awesome-design-md` | `/awesome-design-md` | 74 DESIGN.md design systems (Stripe, Linear, Vercel, Apple, Notion, ...) with a catalog and rules for applying one | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) `design-md/*/DESIGN.md` |
| `playwright-cli` | `/playwright-cli` | Browser automation and Playwright test workflows through the `playwright-cli` command | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) `skills/playwright-cli/` |

## Pinned versions

Installed 2026-10-07 from these upstream commits:

- Leonxlnx/taste-skill `b482f7a970abb98c4108d4a9f761e458c64cefc8` (MIT)
- vercel-labs/agent-skills `063bee94c3f4df8453406c830b0a7df0f2860278`
- VoltAgent/awesome-design-md `13be5c05c63be24b57581162364167028020f043` (MIT)
- microsoft/playwright-cli `b85c7a736bb473bf55b584e54a09ffa698d6d871` (Apache-2.0), identical to the skill bundled in `@playwright/cli` 0.1.22

The `SKILL.md` files are copied verbatim from upstream, except `awesome-design-md/SKILL.md`,
which is a wrapper written for this repository: upstream ships only the DESIGN.md files, and those
are copied verbatim into `awesome-design-md/references/<slug>/DESIGN.md`.

## Requirements and notes

- `playwright-cli` needs the CLI on the machine: `npm install -g @playwright/cli@latest`. If the CLI
  later reports that the skill here does not match the tool version, run
  `playwright-cli install --skills` from the repo root to refresh it.
- `web-design-guidelines` fetches the current rules from
  `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` on each
  review, so it needs network access for WebFetch.
- `image-to-code` is written around an image-generation step for the reference boards. Without an
  image-generation tool it still works from images you supply.
- `design-taste-frontend` is Taste Skill v2 (experimental upstream). The v1 skill and the other
  taste-skill skills (brutalist, minimalist, soft, redesign, stitch, brandkit, output, imagegen)
  live in the same upstream repo and can be added the same way.

## Updating

Re-copy the upstream paths listed above into the matching directory here, or use the upstream
installers (`npx skills add <repo> --skill <name>` for the first three, `playwright-cli install
--skills` for Playwright). Note that `npx skills add` may lay files out differently (for example
symlinks from `.claude/skills/` into `.agents/skills/`), so check the result before committing.
