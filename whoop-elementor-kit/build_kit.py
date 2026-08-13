#!/usr/bin/env python3
"""
Builder for the "Whatshername" Elementor Template Kit.

A bright, vibrant creative-portfolio design system inspired by the WHOOP
template style: white backgrounds, bold Poppins headings, and signature
purple -> magenta gradients with cyan / yellow / pink pops.

Built for the artist Whatshername.uk to showcase (and later sell) her art.

Run:  python3 build_kit.py
Outputs Elementor-importable page/section JSON into ./templates/
"""
import json
import os
import secrets

OUT = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# DESIGN SYSTEM  (extracted from the WHOOP screenshots)
# ---------------------------------------------------------------------------
WHITE       = "#FFFFFF"
BG_LIGHT    = "#F7F7FB"   # very light section background
HEAD_DARK   = "#26263A"   # near-black heading charcoal
BODY_MUTED  = "#6E6E80"   # body / secondary text
PURPLE      = "#9C1AE6"   # vivid violet (brand primary)
MAGENTA     = "#F5179E"   # hot magenta (accent / buttons)
GRAD_A      = "#7B2FF7"   # gradient start (indigo-purple)
GRAD_B      = "#F0139C"   # gradient end (magenta)
CYAN        = "#12D8E8"
YELLOW      = "#F6E400"
BLUE        = "#4B2FF7"
BORDER      = "#ECECF3"

FONT_HEAD = "Poppins"     # bold geometric headings (Google Font)
FONT_BODY = "Poppins"     # body (lighter weights)

# colourful tile palette for gallery/portfolio placeholders
TILE_COLORS = ["9C1AE6", "F5179E", "12D8E8", "F6E400", "4B2FF7", "12D8B0",
               "FF6FA5", "7B2FF7", "FF7A45", "B8E62C", "1EC9FF", "E01FA0"]


def nid():
    return secrets.token_hex(4)[:7]


# ---------------- element builders ----------------
def section(elements, settings=None, inner=False):
    return {"id": nid(), "elType": "section",
            "settings": settings or {}, "elements": elements, "isInner": inner}


def column(elements, size=100, extra=None):
    s = {"_column_size": size, "_inline_size": None}
    if extra:
        s.update(extra)
    return {"id": nid(), "elType": "column", "settings": s,
            "elements": elements, "isInner": False}


def widget(wtype, settings):
    return {"id": nid(), "elType": "widget", "settings": settings,
            "elements": [], "widgetType": wtype}


def px(top, right, bottom, left, unit="px"):
    linked = top == right == bottom == left
    return {"unit": unit, "top": str(top), "right": str(right),
            "bottom": str(bottom), "left": str(left), "isLinked": linked}


def size(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


def radius(n):
    return {"unit": "px", "top": str(n), "right": str(n),
            "bottom": str(n), "left": str(n), "isLinked": True}


def typo(family, weight, fsize, lh=None, ls=None, transform=None):
    d = {"typography_typography": "custom",
         "typography_font_family": family,
         "typography_font_weight": str(weight),
         "typography_font_size": size(fsize)}
    if lh is not None:
        d["typography_line_height"] = size(lh, "em")
    if ls is not None:
        d["typography_letter_spacing"] = size(ls, "px")
    if transform:
        d["typography_text_transform"] = transform
    return d


def heading(text, tag="h2", color=HEAD_DARK, align="center",
            family=FONT_HEAD, weight=700, fsize=44, lh=1.15, ls=-0.5,
            transform="", mobile=None, extra=None):
    s = {"title": text, "header_size": tag, "align": align,
         "title_color": color}
    s.update(typo(family, weight, fsize, lh, ls, transform))
    if mobile:
        s["typography_font_size_mobile"] = size(mobile)
    if extra:
        s.update(extra)
    return widget("heading", s)


def paragraph(html, color=BODY_MUTED, align="center", fsize=17, lh=1.8,
              weight=400):
    s = {"editor": f"<p>{html}</p>", "align": align, "text_color": color}
    s.update(typo(FONT_BODY, weight, fsize, lh))
    return widget("text-editor", s)


def button(text, bg=MAGENTA, color=WHITE, align="center", ghost=False,
           link="#", small=False):
    s = {"text": text, "align": align,
         "link": {"url": link, "is_external": "", "nofollow": ""},
         "border_radius": radius(50),
         "text_padding": px(14, 30, 14, 30) if small else px(17, 40, 17, 40),
         "button_text_color": color}
    s.update(typo(FONT_HEAD, 600, 14 if small else 15,
                  transform="uppercase"))
    s["typography_letter_spacing"] = size(0.5)
    if ghost:
        s.update({"background_color": "rgba(255,255,255,0)",
                  "button_text_color": HEAD_DARK,
                  "border_border": "solid",
                  "border_width": px(2, 2, 2, 2),
                  "border_color": PURPLE})
    else:
        s["background_color"] = bg
    return widget("button", s)


def eyebrow(text, color=MAGENTA, align="center"):
    s = {"title": text, "header_size": "h6", "align": align,
         "title_color": color}
    s.update(typo(FONT_HEAD, 700, 13, transform="uppercase"))
    s["typography_letter_spacing"] = size(2)
    return widget("heading", s)


def spacer(h):
    return widget("spacer", {"space": size(h)})


def img(url, rounded=16):
    return widget("image", {"image": {"url": url, "id": ""},
                            "border_radius": radius(rounded),
                            "image_size": "full"})


def tile_url(i, w=600, h=600, label="Art"):
    c = TILE_COLORS[i % len(TILE_COLORS)]
    return f"https://via.placeholder.com/{w}x{h}/{c}/ffffff?text={label}"


# ---------------- backgrounds ----------------
def gradient_bg(a=GRAD_A, b=GRAD_B, angle=135, top=90, bottom=90, radius_n=0):
    d = {"background_background": "gradient",
         "background_color": a,
         "background_color_b": b,
         "background_gradient_type": "linear",
         "background_gradient_angle": {"unit": "deg", "size": angle,
                                       "sizes": []},
         "padding": px(top, 0, bottom, 0)}
    if radius_n:
        d["border_radius"] = radius(radius_n)
    return d


def bg(color, top=100, bottom=100):
    return {"background_background": "classic", "background_color": color,
            "padding": px(top, 0, bottom, 0)}


def card(color=WHITE, pad=32, rounded=18, border=True):
    d = {"background_background": "classic", "background_color": color,
         "border_radius": radius(rounded), "padding": px(pad, pad, pad, pad),
         "box_shadow_box_shadow_type": "yes",
         "box_shadow_box_shadow": {"horizontal": 0, "vertical": 18,
                                   "blur": 50, "spread": 0,
                                   "color": "rgba(38,38,58,0.08)"}}
    if border:
        d.update({"border_border": "solid", "border_width": px(1, 1, 1, 1),
                  "border_color": BORDER})
    return d


def wrap(title, content, ttype="page"):
    return {"content": content, "page_settings": {},
            "version": "0.4", "title": title, "type": ttype}


# ===========================================================================
# SHARED SECTIONS
# ===========================================================================
BRAND = "Whatshername"


def s_nav():
    logo = column([heading(BRAND, "h4", MAGENTA, "left", FONT_HEAD, 700,
                           26, 1, -0.5)], 25)
    menu = column([paragraph(
        "Home&nbsp;&nbsp;&nbsp;About&nbsp;&nbsp;&nbsp;Gallery"
        "&nbsp;&nbsp;&nbsp;Shop&nbsp;&nbsp;&nbsp;Contact",
        HEAD_DARK, "center", 15, weight=500)], 50)
    cta = column([button("Commission", align="right", small=True)], 25)
    return section([logo, menu, cta],
                   {**bg(WHITE, 24, 24),
                    "border_border": "solid", "border_width": px(0, 0, 1, 0),
                    "border_color": BORDER})


def s_footer():
    brand = column([
        heading(BRAND, "h4", WHITE, "left", FONT_HEAD, 700, 24, 1, -0.5),
        spacer(12),
        paragraph("Contemporary artist &amp; visual storyteller. Original "
                  "paintings, limited prints and commissions.",
                  "rgba(255,255,255,0.7)", "left", 15, 1.7),
    ], 40)

    def foot_col(title, items):
        els = [heading(title, "h6", WHITE, "left", FONT_HEAD, 600, 14, 1.4,
                       0.5, "uppercase"), spacer(14)]
        for it in items:
            els.append(paragraph(it, "rgba(255,255,255,0.7)", "left", 15,
                                 2.1))
        return column(els, 20)

    return section([
        brand,
        foot_col("Explore", ["Home", "About", "Gallery", "Shop"]),
        foot_col("Buy Art", ["Original Paintings", "Limited Prints",
                             "Commissions", "Gift Cards"]),
        foot_col("Connect", ["Instagram", "Contact", "Newsletter",
                             "Studio Visits"]),
    ], gradient_bg(GRAD_A, GRAD_B, 120, 70, 55))


def s_newsletter():
    inner = section([
        column([heading("Get new drops &amp; show news in your inbox.", "h3",
                        WHITE, "left", FONT_HEAD, 700, 26, 1.3, -0.3)], 55),
        column([button("Subscribe", bg=HEAD_DARK, align="right")], 45),
    ], {"gap": "wider"}, inner=True)
    return section([column([inner])],
                   {**gradient_bg(GRAD_A, GRAD_B, 120, 44, 44, 24),
                    "margin": px(0, 24, 60, 24)})


# ===========================================================================
# HOME PAGE
# ===========================================================================
def s_hero():
    col = column([
        eyebrow("Contemporary Artist", "rgba(255,255,255,0.85)"),
        spacer(16),
        heading(BRAND, "h1", WHITE, "center", FONT_HEAD, 800, 84, 1.02, -2,
                mobile=52),
        spacer(18),
        paragraph("Bold, colour-drenched paintings and prints exploring "
                  "identity, motion and the noise of modern life.",
                  "rgba(255,255,255,0.9)", "center", 20, 1.7),
        spacer(32),
        button("View the Gallery", bg=WHITE, color=PURPLE, link="#gallery"),
    ])
    return section([col], gradient_bg(GRAD_A, GRAD_B, 135, 150, 150))


def s_recent():
    head = column([
        eyebrow("Recent Work"),
        spacer(12),
        heading("New paintings &amp; drops", "h2", HEAD_DARK, "center",
                FONT_HEAD, 700, 44, 1.15, -0.5),
    ])
    tiles = section([
        column([img(tile_url(0, 640, 760, "Painting"))], 33),
        column([img(tile_url(2, 640, 760, "Series")),
                spacer(24),
                img(tile_url(3, 640, 480, "Study"))], 33),
        column([img(tile_url(1, 640, 760, "Print"))], 33),
    ], {"gap": "extended"}, inner=True)
    return section([column([head, spacer(46), tiles])], bg(WHITE, 100, 90))


def service_card(icon, title, desc, color):
    inner = [
        widget("icon", {"selected_icon": {"value": icon,
                                          "library": "fa-solid"},
                        "primary_color": color, "size": size(30),
                        "align": "left"}),
        spacer(18),
        heading(title, "h4", HEAD_DARK, "left", FONT_HEAD, 700, 24, 1.3,
                -0.3),
        spacer(10),
        paragraph(desc, BODY_MUTED, "left", 16, 1.75),
        spacer(14),
        paragraph(f'<a href="#" style="color:{PURPLE};font-weight:600">'
                  'Read more &rarr;</a>', PURPLE, "left", 15),
    ]
    return column([section([column(inner)], card(WHITE, 36), inner=True)], 33)


def s_services():
    head = column([
        eyebrow("What I Make"),
        spacer(12),
        heading("Ways to bring the work home", "h2", HEAD_DARK, "center",
                FONT_HEAD, 700, 44, 1.15, -0.5),
    ])
    cards = section([
        service_card("fas fa-palette", "Original Paintings",
                     "One-of-a-kind canvases in acrylic and mixed media. "
                     "Signed, certified and ready to hang.", PURPLE),
        service_card("fas fa-layer-group", "Prints &amp; Editions",
                     "Museum-quality giclée prints in limited runs, "
                     "hand-numbered and archival.", MAGENTA),
        service_card("fas fa-wand-magic-sparkles", "Commissions",
                     "Custom pieces made with you — from palette to scale. "
                     "Let's create something personal.", CYAN),
    ], {"gap": "extended"}, inner=True)
    return section([column([head, spacer(46), cards])], bg(BG_LIGHT, 100, 100))


def s_band():
    text_col = column([
        eyebrow("The Studio", "rgba(255,255,255,0.85)", "left"),
        spacer(14),
        heading("I make loud, joyful art for people who feel too much.",
                "h2", WHITE, "left", FONT_HEAD, 700, 38, 1.25, -0.5),
        spacer(16),
        paragraph("Every piece starts as a feeling and ends as colour. Watch "
                  "a short film from inside the studio.",
                  "rgba(255,255,255,0.9)", "left", 18, 1.7),
        spacer(24),
        button("About the Artist", bg=WHITE, color=PURPLE, align="left"),
    ], 50)
    video_col = column([
        widget("video", {
            "video_type": "youtube",
            "youtube_url": "https://www.youtube.com/watch?v=ScMzIvxBSi4",
            "show_image_overlay": "yes",
            "image_overlay": {"url": tile_url(7, 800, 500, "Studio+Film"),
                              "id": ""},
            "lightbox": "yes",
            "aspect_ratio": "169",
            "play_icon_color": WHITE,
            "border_radius": radius(20),
        })
    ], 50)
    return section([text_col, video_col],
                   {**gradient_bg(GRAD_A, GRAD_B, 120, 90, 90),
                    "gap": "wider"})


def s_about():
    head = column([
        eyebrow("The Story"),
        spacer(12),
        heading("A bit about the work", "h2", HEAD_DARK, "center",
                FONT_HEAD, 700, 44, 1.15, -0.5),
    ])

    def item(year, title, desc):
        return column([
            paragraph(year, MAGENTA, "left", 14, 1.4, weight=700),
            heading(title, "h4", HEAD_DARK, "left", FONT_HEAD, 700, 22, 1.3,
                    -0.3),
            spacer(8),
            paragraph(desc, BODY_MUTED, "left", 16, 1.75),
            spacer(6),
            paragraph(f'<a href="#" style="color:{PURPLE};font-weight:600">'
                      'Read more &rarr;</a>', PURPLE, "left", 15),
            spacer(28),
        ], 50)

    grid = section([
        item("2024", "Solo Show — &ldquo;Loud Quiet&rdquo;",
             "A full room of large-scale canvases exploring stillness inside "
             "chaos. Sold out on opening night."),
        item("2023", "Print Studio Launch",
             "Opened a small-batch print studio to make the work affordable "
             "and accessible to more collectors."),
        item("2022", "Public Mural Series",
             "Three city-centre murals commissioned to brighten overlooked "
             "corners of the high street."),
        item("2021", "First Collection",
             "The debut body of work that set the palette and energy the "
             "studio is known for today."),
    ], {"gap": "extended"}, inner=True)
    return section([column([head, spacer(46), grid])], bg(WHITE, 100, 80))


# ===========================================================================
# GALLERY PAGE
# ===========================================================================
def s_page_header(eyebrow_text, title, subtitle):
    col = column([
        eyebrow(eyebrow_text, "rgba(255,255,255,0.85)"),
        spacer(14),
        heading(title, "h1", WHITE, "center", FONT_HEAD, 800, 64, 1.05, -1.5,
                mobile=42),
        spacer(14),
        paragraph(subtitle, "rgba(255,255,255,0.9)", "center", 19, 1.7),
    ])
    return section([col], gradient_bg(GRAD_A, GRAD_B, 135, 100, 100))


def gallery_grid(items, cols=4):
    """items: list of (label, category, title). Returns a section of rows."""
    rows = []
    per = 12 // cols if cols else 100
    col_size = int(100 / cols)
    row = []
    for i, (label, cat, title) in enumerate(items):
        tile = column([
            img(tile_url(i, 600, 600, label), rounded=14),
            spacer(12),
            paragraph(cat, MAGENTA, "left", 12, 1.3, weight=700),
            heading(title, "h5", HEAD_DARK, "left", FONT_HEAD, 600, 18, 1.3,
                    -0.3),
            spacer(20),
        ], col_size)
        row.append(tile)
        if len(row) == cols:
            rows.append(section(row, {"gap": "extended"}, inner=True))
            row = []
    if row:
        rows.append(section(row, {"gap": "extended"}, inner=True))
    return rows


def s_gallery_body():
    tabs = section([column([paragraph(
        '<strong style="color:%s">All</strong>&nbsp;&nbsp;&nbsp;&nbsp;'
        'Paintings&nbsp;&nbsp;&nbsp;&nbsp;Prints&nbsp;&nbsp;&nbsp;&nbsp;'
        'Murals&nbsp;&nbsp;&nbsp;&nbsp;Sold' % PURPLE,
        BODY_MUTED, "center", 16, 1.5, weight=600)])], inner=True)

    items = [
        ("Bloom", "Painting", "Bloom No.4"),
        ("Static", "Print", "Static Hum"),
        ("Rush", "Painting", "Rush Hour"),
        ("Halo", "Mural", "Halo"),
        ("Neon", "Painting", "Neon Sleep"),
        ("Drift", "Print", "Drift"),
        ("Pulse", "Painting", "Pulse"),
        ("Echo", "Print", "Echo Chamber"),
        ("Fizz", "Painting", "Fizz"),
        ("Wave", "Mural", "Wavelength"),
        ("Glow", "Print", "Glow"),
        ("Riot", "Painting", "Colour Riot"),
    ]
    rows = gallery_grid(items, cols=4)
    load = column([spacer(20), button("Load More", link="#")])
    return section([column([tabs, spacer(40)] + rows + [load])],
                   bg(WHITE, 90, 90))


# ===========================================================================
# SHOP PAGE (scaffold for later — swap to WooCommerce for real checkout)
# ===========================================================================
def product_card(i, title, kind, price):
    inner = [
        img(tile_url(i, 600, 600, title.replace(" ", "+")), rounded=14),
        spacer(16),
        paragraph(kind, MAGENTA, "left", 12, 1.3, weight=700),
        heading(title, "h5", HEAD_DARK, "left", FONT_HEAD, 600, 20, 1.3,
                -0.3),
        spacer(6),
        heading(price, "h5", PURPLE, "left", FONT_HEAD, 700, 20, 1.3, 0),
        spacer(16),
        button("Add to Cart", align="left", small=True),
    ]
    return column([section([column(inner)], card(WHITE, 22), inner=True)], 33)


def s_shop_body():
    products = [
        ("Bloom No.4", "Original Painting", "£1,200"),
        ("Static Hum", "Limited Print", "£85"),
        ("Rush Hour", "Original Painting", "£1,450"),
        ("Neon Sleep", "Limited Print", "£85"),
        ("Pulse", "Original Painting", "£980"),
        ("Colour Riot", "Limited Print", "£120"),
    ]
    rows, row = [], []
    for i, (t, k, p) in enumerate(products):
        row.append(product_card(i, t, k, p))
        if len(row) == 3:
            rows.append(section(row, {"gap": "extended"}, inner=True))
            rows.append(section([column([spacer(24)])], inner=True))
            row = []
    if row:
        rows.append(section(row, {"gap": "extended"}, inner=True))
    note = column([spacer(10), paragraph(
        "Prices shown are placeholders. For real checkout, install "
        "WooCommerce and convert these cards to Product widgets.",
        BODY_MUTED, "center", 14, 1.6)])
    return section([column(rows + [note])], bg(BG_LIGHT, 90, 90))


# ===========================================================================
# ASSEMBLE + WRITE
# ===========================================================================
def write(name, data):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("wrote", path)


# Home
write("home.json", wrap(f"{BRAND} — Home", [
    s_nav(), s_hero(), s_recent(), s_services(), s_band(), s_about(),
    s_newsletter(), s_footer(),
], "page"))

# Gallery
write("gallery.json", wrap(f"{BRAND} — Gallery", [
    s_nav(),
    s_page_header("Portfolio", "Gallery",
                  "A living collection of paintings, prints and murals — "
                  "filter by type or just scroll and enjoy."),
    s_gallery_body(),
    s_newsletter(), s_footer(),
], "page"))

# Shop (scaffold)
write("shop.json", wrap(f"{BRAND} — Shop", [
    s_nav(),
    s_page_header("Buy Art", "Shop",
                  "Take a piece home. Original paintings and limited prints, "
                  "shipped worldwide."),
    s_shop_body(),
    s_newsletter(), s_footer(),
], "page"))

# Reusable section blocks
write("section-hero.json", wrap(f"{BRAND} — Hero", [s_hero()], "section"))
write("section-services.json", wrap(f"{BRAND} — Services",
                                    [s_services()], "section"))
write("section-gradient-band.json", wrap(f"{BRAND} — Gradient Band",
                                         [s_band()], "section"))
write("section-newsletter.json", wrap(f"{BRAND} — Newsletter",
                                      [s_newsletter()], "section"))

print("\nDesign tokens:")
print(" white", WHITE, "| purple", PURPLE, "| magenta", MAGENTA,
      "| gradient", GRAD_A, "->", GRAD_B)
print(" fonts:", FONT_HEAD, "(headings) /", FONT_BODY, "(body)")
