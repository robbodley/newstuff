# Session Handoff — Whatshername.uk site kit

Context so this work can continue in another Claude Code session (desktop /
terminal) without re-explaining anything.

## What this is
An Elementor Pro **template kit** for the artist **Whatshername.uk** — a
contemporary pop artist (bold, colourful, character-led paintings). The site
showcases her work and (later) sells originals + prints.

## Direction chosen (important)
We tried a few looks and **landed on a MINIMALIST editorial style** (inspired by
a Banksy-style WordPress site the user liked):
- White space, hairline dividers, a small **circular red marker**
- **Typewriter fonts**: Special Elite (headings) + Courier Prime (body)
- One **light-red accent**: `#E0574F` decorative, `#BF3B34` for text (AA-safe)
- **Artwork framed on white** — loud art inside a quiet frame
- Ink `#2B2B2B`, body `#4A4A4A`, muted `#8A8A8A`, bar `#3C3C3C`, line `#E6E6E6`

An earlier BRIGHT gradient kit (Poppins/Syne, purple→magenta) was **retired** at
the user's request — do not bring it back unless asked.

## Repo layout (`whoop-elementor-kit/`)
- `build_kit.py` — Python generator; run `python3 build_kit.py` to rebuild all
  templates in `templates/` **and** repackage `whatshername-kit.zip`. All
  colours/fonts are constants at the top.
- `templates/` — Elementor JSON: pages (home, gallery, about, shop, contact,
  single-article) + Theme Builder (tb-header, tb-footer, tb-archive,
  tb-single-post).
- `whatshername-kit.zip` — native Elementor **Import/Export Kit** (one-click).
- `preview.html` — full standalone preview of every page (colourful CSS
  stand-ins for the real paintings).
- `SHOP-SETUP.md` — WooCommerce setup guide.
- `README.md` — import + setup instructions.

## Status — done
- Minimalist kit complete: 6 pages + 4 Theme Builder templates, global
  colours/fonts, dynamic blog (Archive + Single Post via Pro widgets).
- Accessibility: colour palette passes WCAG AA (audited with the
  `ui-ux-pro-max` skill).
- Shop **page scaffold** added (framed products + price + Add-to-Cart), plus a
  full WooCommerce write-up in `SHOP-SETUP.md`.

## Status — open / next steps
1. **Real artwork**: template JSON ships grey placeholders. Swap for real
   photos via WordPress **Media Library** (user has the paintings). The 5 sample
   paintings shared in chat could not be embedded (they were chat images, not
   files) — if continuing, ask the user to attach the image files.
2. **Dynamic WooCommerce shop**: build a real Products-widget shop page + a
   Single Product Theme Builder template in this minimalist style (waiting on
   the user installing WooCommerce and adding products).
3. Optional: About/Contact copy is placeholder — replace with the artist's real
   bio, address, socials.

## Environment notes
- Develop on branch `claude/website-template-review-hvskls`; commit + push there.
- This kit was built on Claude Code **web** (locked-down network). Running
  locally gives normal internet (e.g. can fetch reference sites directly).
- The `ui-ux-pro-max` design skill was cloned to help; install it locally with
  `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` then
  `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`.
