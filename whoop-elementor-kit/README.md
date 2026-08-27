# Whatshername — Elementor Pro Template Kit (Minimalist)

A quiet, editorial **gallery kit** for the artist **Whatshername.uk** — built so
loud, colourful artwork sits inside a calm frame.

- **White space + hairline dividers**, a small **circular red marker**
- **Typewriter fonts** — *Special Elite* (headings) + *Courier Prime* (body)
- A single **light-red accent** — `#E0574F` (decorative) / `#BF3B34` (text, AA-safe)
- **Artwork framed on white** (thin mat + soft shadow)
- Built for **Elementor Pro**: global Header/Footer + a **dynamic** blog

---

## 1. One-click import

`whatshername-kit.zip` is a native **Elementor Import/Export Kit**.

1. WordPress admin → **Elementor → Tools → Import / Export Kit → Import**.
2. Upload **`whatshername-kit.zip`**, keep everything ticked → **Import**.

That brings in global colours/fonts, all pages, and the Theme Builder templates.
Then do the finishing steps in §4.

> If the one-click import errors on your Elementor version, import the individual
> files in `templates/` via **Templates → Saved Templates → Import** instead.

---

## 2. Design system

| Role | Value |
|------|-------|
| Ink (headings/text) | `#2B2B2B` |
| Body | `#4A4A4A` · muted `#8A8A8A` |
| Accent (light red) | `#E0574F` decorative · `#BF3B34` for text/links (AA 5.4) |
| Top bar | `#3C3C3C`, light text `#EDEDED` |
| Hairline / frame | `#E6E6E6` / `#E0E0E0` |
| Headings | **Special Elite** (400) |
| Body | **Courier Prime** (400 / 700) |

Both fonts are free Google Fonts, built into Elementor.

---

## 3. What's in the box

```
whoop-elementor-kit/
├── whatshername-kit.zip     ← one-click Elementor kit
├── preview.html             ← full site preview (Home→Gallery→About→Shop→Contact→Journal)
├── build_kit.py             ← regenerates every template + the kit zip
├── SHOP-SETUP.md            ← WooCommerce shop setup guide
├── templates/
│   ├── home / gallery / about / shop / contact / single-article .json   (pages)
│   └── tb-header / tb-footer / tb-archive / tb-single-post .json         (Theme Builder)
└── README.md
```

**Pages:** Home, Gallery, About, **Shop**, Contact, plus a static Article.
**Theme Builder (Pro, global/dynamic):** Header, Footer, Journal Archive, Single
Post — so every real blog post you write auto-adopts the design.

---

## 4. Finish setup

1. **Menu:** **Appearance → Menus** — create a menu (Home, About, Gallery,
   Journal, Shop, Contact) and select it in the Header template's **Nav Menu**.
2. **Display conditions** (Theme Builder → each template):
   Header/Footer → *Entire Site*; Archive → *Posts Archive*; Single Post →
   *Singular → Posts*.
3. **Front page:** **Settings → Reading → A static page → Home**.
4. **Contact form:** select the Form widget → *Actions After Submit → Email* →
   set your address.

---

## 5. Add the real artwork

Template JSON never contains images — you add them in WordPress:

1. **Media → Add New**, upload the paintings.
2. Edit a page in Elementor, click each framed **Image** widget, pick the
   painting. (Grey placeholders ship so nothing looks broken beforehand.)
3. In the **Gallery**/**Shop**, duplicate a framed item per new piece and update
   the title / medium / price caption.

The colourful stand-ins in `preview.html` are CSS — they show how loud art looks
inside the quiet frame; your real paintings replace them.

---

## 6. The Shop → selling for real

`shop.json` is a styled **scaffold** (framed products, price, Add-to-Cart) so the
layout is ready. To actually take payments, follow **`SHOP-SETUP.md`** — it walks
through WooCommerce end to end: originals as *stock = 1*, prints as variable
products with sizes/editions, shipping zones, Stripe/PayPal, and rebuilding the
shop + single-product page with Woo's dynamic widgets in this exact style.

Want it done for you? Send your Products list and I'll hand over the dynamic
Shop + Single-Product templates as importable JSON.

---

## 7. Re-theming

All colours/fonts are constants at the top of `build_kit.py`. Change them and run
`python3 build_kit.py` to rebuild every template **and** repackage the kit zip.
