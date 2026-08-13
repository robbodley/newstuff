# Whatshername — Elementor Pro Template Kit

A bright, vibrant creative-portfolio kit for **Whatshername.uk**, matched to the
WHOOP template style: white backgrounds, bold Poppins headings, and signature
**purple → magenta gradients** with cyan / yellow / pink pops.

Built for **Elementor Pro** — with a global Header & Footer, a **dynamic** blog
(Archive + Single Post that style every real post automatically), and pages for
Home, About, Gallery, Shop and Contact.

---

## 1. Fastest path — import the whole kit in one click

`whatshername-kit.zip` is a native **Elementor Import/Export Kit**.

1. WordPress admin → **Elementor → Tools → Import / Export Kit → Import**.
2. Upload **`whatshername-kit.zip`**.
3. Keep everything ticked (Templates, Content, Site Settings) → **Import**.

That brings in the global colours/fonts, all 7 pages, and the 4 Theme Builder
templates (Header, Footer, Archive, Single Post) with display conditions
pre-set. Then jump to **§4** to finish wiring things up.

> **If the one-click import errors** (kit imports can be fussy across Elementor
> versions), use the bulletproof manual route in **§3** instead — same result,
> a few more clicks. The individual JSON files in `templates/` always import.

---

## 2. Design system

### Colours

| Role        | Hex                  | Global slot |
|-------------|----------------------|-------------|
| Purple      | `#9C1AE6`            | Primary     |
| Magenta     | `#F5179E`            | Secondary   |
| Heading     | `#26263A`            | Text        |
| Cyan        | `#12D8E8`            | Accent      |
| Gradient    | `#7B2FF7 → #F0139C` (135°) | Custom: Gradient Start / End |
| Yellow      | `#F6E400`            | Custom      |
| White / Light | `#FFFFFF` / `#F7F7FB` | backgrounds |
| Body text   | `#6E6E80`            | —           |

### Fonts (free Google Fonts, built into Elementor)

- **Headings:** Poppins 700 / 800  ·  **Body:** Poppins 400 / 500

---

## 3. Manual import (bulletproof, works on free too)

### a) Global colours & fonts

**Elementor → Site Settings → Global Colors / Global Fonts** and enter the
values from §2 (Primary `#9C1AE6`, Secondary `#F5179E`, Text `#26263A`, Accent
`#12D8E8`; all fonts **Poppins**). **Update**.

### b) Pages

**Templates → Saved Templates → Import Templates**, upload each of:
`home.json`, `about.json`, `gallery.json`, `shop.json`, `blog.json`,
`contact.json`. Then create a page for each, **Edit with Elementor**, and insert
it from **Add Template → My Templates**.

### c) Theme Builder templates (Pro)

Import these the same way, then open each in **Templates → Theme Builder** and
set the display condition (see §4):

| File | Type | Condition |
|------|------|-----------|
| `tb-header.json` | Header | Entire Site |
| `tb-footer.json` | Footer | Entire Site |
| `tb-archive.json` | Archive | Posts / Blog archive |
| `tb-single-post.json` | Single Post | All Posts |

---

## 4. Finish setup (after either import method)

1. **Menus:** create a menu at **Appearance → Menus** (Home, About, Gallery,
   Journal, Shop, Contact) and select it in the Header template's **Nav Menu**
   widget.
2. **Display conditions** (Theme Builder → each template → *Display Conditions*
   if not already set):
   - **Header / Footer** → *Include → Entire Site*
   - **Archive** → *Include → Archives → Posts Archive* (and/or Categories)
   - **Single Post** → *Include → Singular → Posts*
3. **Front page:** **Settings → Reading → A static page → Home**. Set your
   Journal/blog page as the *Posts page* if you want the archive at a URL.
4. **Swap placeholders:** every grey `via.placeholder.com` tile is a normal
   Image widget — replace with real artwork. Update copy, prices and icons.
5. **Contact form:** open the Contact page, select the **Form** widget →
   *Actions After Submit* → add **Email**, and set the "To" address. (Optional:
   connect to Mailchimp/webhook.)
6. **Map:** the Contact page **Google Maps** widget — set your address; add a
   Google Maps API key under **Elementor → Settings → Integrations** if needed.

---

## 5. The dynamic blog (this is the good part)

`tb-archive.json` and `tb-single-post.json` are **real Theme Builder templates**
using Elementor Pro's dynamic widgets — so you never design a post by hand:

- **Archive** uses the **Archive Posts** widget → automatically lists your real
  posts in the 3-column card grid, with pagination.
- **Single Post** uses **Post Title**, **Post Info**, **Featured Image** and
  **Post Content** (all pull the current post automatically), then a **Posts**
  widget for "More from the journal".

Just write posts in **Posts → Add New** and assign categories — every post picks
up this design. To tune the "related" list, open the Single template's Posts
widget → *Query → Source: Related*.

> The static `single-article.json` / `blog.json` pages are kept too, as visual
> references and for anyone not using the dynamic templates.

---

## 6. What's in the box

```
whoop-elementor-kit/
├── whatshername-kit.zip             ← one-click Elementor kit (§1)
├── preview.html                     ← Home + Gallery + Shop
├── preview-blog.html                ← Journal + Single Article
├── preview-pages.html               ← About + Contact
├── build_kit.py                     ← regenerates everything
├── templates/                       ← individual JSON (manual import)
│   ├── home / about / gallery / shop / blog / contact / single-article .json
│   ├── tb-header / tb-footer / tb-archive / tb-single-post .json  (Pro)
│   └── section-*.json               ← reusable blocks
└── README.md
```

---

## 7. Shop — going live later

`shop.json` is a **visual scaffold** (static product cards) so the layout is
ready. To actually sell: install **WooCommerce**, add each artwork as a Product
(Original or Print), then swap the static cards for WooCommerce/Elementor
**Products** widgets. The styling carries straight over. Say the word and I'll
build the WooCommerce version + a single-product template.

---

## 8. Re-theming in one shot

All colours/fonts are constants at the top of `build_kit.py`. Change them and
run `python3 build_kit.py` to rebuild every template **and** repackage the kit
zip with the new palette.
