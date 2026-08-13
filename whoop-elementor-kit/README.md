# Whatshername — Elementor Template Kit

A bright, vibrant creative-portfolio kit for **Whatshername.uk**, built to
match the WHOOP template style: white backgrounds, bold Poppins headings, and
signature **purple → magenta gradients** with cyan / yellow / pink pops.

Designed to showcase the artist's work, take commissions, and grow into an
online shop for prints and originals.

---

## 1. Design system (matched from the WHOOP screenshots)

### Colours

| Role             | Hex        | Use                                    |
|------------------|------------|----------------------------------------|
| White            | `#FFFFFF`  | Page background                        |
| Light            | `#F7F7FB`  | Alternating sections                   |
| Heading          | `#26263A`  | Bold headings (near-black charcoal)    |
| Body             | `#6E6E80`  | Body / secondary text                  |
| **Purple**       | `#9C1AE6`  | Brand primary, links, accents          |
| **Magenta**      | `#F5179E`  | Buttons, eyebrows, highlights          |
| Gradient         | `#7B2FF7 → #F0139C` | Hero, bands, footer, newsletter (135°) |
| Cyan             | `#12D8E8`  | Accent pops                            |
| Yellow           | `#F6E400`  | Accent pops                            |
| Border           | `#ECECF3`  | Hairline borders                       |

### Fonts (free on Google Fonts, built into Elementor)

- **Headings:** `Poppins` — 700 / 800 (bold geometric — matches the WHOOP look)
- **Body:** `Poppins` — 400 / 500

### Signature elements

- **Gradient pill buttons** and gradient section bands (purple → magenta)
- **Rounded cards** with a soft drop shadow
- **Colourful art tiles** in the portfolio grid (each a different vivid hue)

---

## 2. What's in the box

```
whoop-elementor-kit/
├── preview.html                     ← browser preview: Home + Gallery + Shop
├── preview-blog.html                ← browser preview: Journal + Single Article
├── build_kit.py                     ← regenerates the JSON (edit tokens here)
├── templates/
│   ├── home.json                    ← Home page
│   ├── gallery.json                 ← Gallery / portfolio page
│   ├── shop.json                    ← Shop page (scaffold — see §5)
│   ├── blog.json                    ← Journal / blog archive page
│   ├── single-article.json          ← single post + sidebar + related
│   ├── section-hero.json            ← reusable gradient hero
│   ├── section-featured-post.json   ← featured-post block
│   ├── section-services.json        ← 3-card "what I make" block
│   ├── section-gradient-band.json   ← studio band with video
│   └── section-newsletter.json      ← gradient newsletter bar
└── README.md
```

### Page layouts

- **Home:** nav → gradient hero → "Recent Work" grid → 3 service cards
  (Original Paintings / Prints / Commissions) → studio gradient band with a
  video → "A bit about the work" timeline → newsletter bar → footer.
- **Gallery:** gradient page header → filter tabs → 12-tile colourful grid
  with captions → Load More → newsletter → footer.
- **Shop:** gradient page header → product cards (image, title, price, Add to
  Cart) → footer. See §5 before going live.
- **Journal (blog archive):** gradient header → featured post → category tabs
  → 6 article cards → Load More → newsletter → footer.
- **Single Article:** gradient title header (with author/date/read-time) →
  two-column body (article + sidebar of Categories / Recent Posts / Tags) →
  pull-quote → "More from the journal" related grid → newsletter → footer.

### A note on blog pages & dynamic content

`blog.json` and `single-article.json` are **static layouts** — they show the
design with example posts baked in. WordPress blogs are normally *dynamic*
(the theme pulls real posts automatically). Two ways to use these:

1. **Design reference (free Elementor):** use them as the visual blueprint and
   fill in real content by hand, or match your theme's blog styling to them.
2. **Fully dynamic (Elementor Pro):** rebuild them in **Theme Builder** as an
   *Archive* template and a *Single Post* template using the Loop/Posts and
   dynamic widgets, so every real post uses this design automatically. The
   colours, fonts and card styling here map straight onto those widgets.

---

## 3. Import into WordPress / Elementor

**Requirements:** Elementor (free works). A couple of touches (gradient
buttons, Theme-Builder header/footer) are nicer with Elementor Pro but aren't
required.

### Step 1 — Global colours & fonts (do this first)

**Elementor → Site Settings → Global Colors:**

- Primary → `#9C1AE6`  ·  Secondary → `#F5179E`  ·  Text → `#26263A`  ·  Accent → `#12D8E8`

**Global Fonts:**

- Primary (headings) → **Poppins** 700 · Secondary → **Poppins** 800 ·
  Text (body) → **Poppins** 400 · Accent → **Poppins** 600

Click **Update**.

### Step 2 — Import templates

1. **Templates → Saved Templates → Import Templates**.
2. Upload `home.json`, `gallery.json`, `shop.json` (and any `section-*.json`).

### Step 3 — Build the pages

- Create a page (e.g. *Home*) → **Edit with Elementor** → the folder icon
  (Add Template) → **My Templates** → insert **Whatshername — Home**.
- Repeat for **Gallery** and **Shop**. Set *Home* as the front page under
  **Settings → Reading**.

### Step 4 — Make it hers

- Swap the placeholder tiles for real photos of the artwork (each tile is a
  standard Image widget — just replace the image).
- Update copy, the timeline years, prices, and the Font Awesome icons.
- Point the nav links at the real Home / About / Gallery / Shop / Contact pages.

---

## 4. Placeholder images

The templates use grey `via.placeholder.com` images so nothing is broken on
import. Replace each with the real artwork via the Image widget. In the
`preview.html` the tiles are pure CSS gradients (no downloads) so you can see
the colour system instantly.

---

## 5. The Shop — going live later

The `shop.json` page is a **visual scaffold**: static product cards with a
title, price and "Add to Cart" button so the layout is ready. It does **not**
process payments yet. When you're ready to actually sell:

1. Install the free **WooCommerce** plugin (adds cart, checkout, payments,
   shipping, orders).
2. Add each artwork as a **Product** (Original or Print, with price/stock).
3. Replace the static cards with Elementor's **Products** / **Archive**
   widget (or use WooCommerce's shop page) so real add-to-cart works.
4. Connect Stripe/PayPal for payments.

The colours, fonts and card styling here will carry straight over, so the shop
matches the rest of the site out of the box. Ping me when you want to do this
and I'll wire up the WooCommerce version.

---

## 6. Re-theming in one shot

All colours/fonts are constants at the top of `build_kit.py`. Change them and
run `python3 build_kit.py` to rebuild every template with the new palette.

---

## 7. Fidelity note

This matches the WHOOP style from the screenshots you shared (bright, gradient,
Poppins, colourful grid) — rebuilt originally rather than copied, so it's yours
to use freely for the artist's site. Send more screenshots of any specific page
(About, Contact, single artwork) and I'll add matching templates.
