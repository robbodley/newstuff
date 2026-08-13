# PULSE — Elementor Template Kit

An original, **WHOOP-inspired** template kit for WordPress + Elementor.
Dark, bold, performance/wearable aesthetic — rebuilt from scratch (no assets
copied from the original), so it's yours to use and customise freely.

> Note: I couldn't load the live `whoop.templatekit.co` demo from this
> environment (network egress is locked down), so this is an *approximation*
> of that fitness/performance style rather than a pixel copy. Send me
> screenshots any time and I'll tune the palette, fonts and layout to match
> more closely.

---

## 1. Design system

### Colours

| Role            | Hex        | Use                                   |
|-----------------|------------|---------------------------------------|
| Background      | `#0A0B0F`  | Page background (near-black)          |
| Surface         | `#14161C`  | Cards, alternating sections           |
| Elevated        | `#1C1F27`  | Featured card                         |
| Text – primary  | `#FFFFFF`  | Headings & key text                   |
| Text – muted    | `#9CA0AD`  | Body / secondary text                 |
| **Accent**      | `#00F0A4`  | Buttons, highlights, stats (teal-green) |
| Accent 2        | `#FF4D5E`  | Energy / alerts (coral)               |
| Border          | `#262A33`  | Hairline borders                      |

### Fonts (both free on Google Fonts, built into Elementor)

- **Headings:** `Sora` — 700 / 800 (geometric, athletic display)
- **Body:** `Inter` — 400 / 500

### Type scale (desktop)

| Element      | Font | Weight | Size  |
|--------------|------|--------|-------|
| H1 (hero)    | Sora | 800    | 72px  |
| H2 (section) | Sora | 800    | 46px  |
| H3           | Sora | 600–800| 34–52px |
| Eyebrow      | Sora | 700    | 14px, uppercase, +2.5 tracking |
| Body         | Inter| 400    | 18–20px |
| Button       | Sora | 600    | 15px, uppercase |

---

## 2. What's in the box

```
whoop-elementor-kit/
├── preview.html            ← open in a browser to see the design
├── build_kit.py            ← regenerates the JSON (edit tokens here)
├── templates/
│   ├── pulse-home.json     ← full home page (nav → hero → stats → features
│   │                          → showcase → pricing → testimonial → CTA → footer)
│   ├── section-hero.json   ← reusable hero block
│   ├── section-features.json
│   ├── section-pricing.json
│   └── section-cta.json
└── README.md
```

---

## 3. How to import into WordPress / Elementor

**Requirements:** Elementor (free is fine for these; a couple of widgets look
best with Elementor Pro, but all core widgets used here work on free).

### Step 1 — Set up the global colours & fonts (do this first)

In WordPress admin: **Elementor → Site Settings → Global Colors**, then set:

- Primary → `#00F0A4`
- Secondary → `#FF4D5E`
- Text → `#FFFFFF`
- Accent → `#9CA0AD`

Then **Global Fonts**:

- Primary (headings) → **Sora**, weight 800
- Secondary → **Sora**, weight 700
- Text (body) → **Inter**, weight 400
- Accent → **Inter**, weight 500

Click **Update**. (The templates use explicit colours too, so they'll look
right even before you do this — but setting globals means one change restyles
the whole site.)

### Step 2 — Import the templates

1. In WordPress admin go to **Templates → Saved Templates**.
2. Click **Import Templates** (top of the page).
3. Upload `templates/pulse-home.json`.
4. Repeat for any of the `section-*.json` blocks you want on hand.

### Step 3 — Use it

- **Whole page:** create/edit a page → edit with Elementor → the folder icon
  (Add Template) → **My Templates** → insert **PULSE — Home**.
- **Single blocks:** same Add-Template dialog, insert the section you want
  (Hero, Pricing, etc.) into any page.

### Step 4 — Swap the placeholders

- Replace the grey `PULSE Band` placeholder image (in the showcase section)
  with your product/hero photo.
- Update copy, prices and the Font Awesome icons on the feature boxes.
- The nav and footer are plain sections; if you use **Elementor Pro** you may
  prefer to rebuild those as a Header/Footer in **Theme Builder**.

---

## 4. Regenerating / re-theming

All colours and fonts are constants at the top of `build_kit.py`. Change them
and run:

```bash
python3 build_kit.py
```

…to rebuild every template JSON with the new palette. Handy if you want to
recolour the whole kit to a different brand in one shot.

---

## 5. Notes on fidelity & licensing

- This is an **inspired-by** rebuild — general layout patterns (hero, stats
  bar, feature grid, pricing tier, CTA) plus an original palette and free
  Google Fonts. Layouts and colour palettes aren't protected, so you're on
  safe ground using this on client or personal sites.
- If you want it to match the original WHOOP kit more closely, share
  screenshots and I'll extract the exact hex values, identify the real fonts
  (or closest free equivalents), and adjust the section structure.
