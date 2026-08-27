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
BODY_MUTED  = "#6E6E80"   # body / secondary text (AA on white: 4.99)
META        = "#5E5E6E"   # small print / dates (AA 6.4 — was #9A9AAB @ 2.8)
PURPLE      = "#9C1AE6"   # vivid violet (brand primary, AA 5.67 on white)
MAGENTA     = "#B3117A"   # deep magenta for TEXT/buttons (AA 6.4 on white)
MAGENTA_POP = "#F5179E"   # bright magenta — decorative / large text only (logo)
GRAD_A      = "#7B2FF7"   # gradient start (indigo-purple)
GRAD_B      = "#D6148C"   # gradient end, tuned so white text passes AA (4.84)
CYAN        = "#12D8E8"
YELLOW      = "#F6E400"
BLUE        = "#4B2FF7"
BORDER      = "#ECECF3"

# Font pairing recommended by ui-ux-pro-max for art galleries / creative
# studios ("Fashion Forward"). To restore the original WHOOP-match look,
# set both of these back to "Poppins" and re-run.
FONT_HEAD = "Syne"        # expressive display headings (Google Font)
FONT_BODY = "Manrope"     # clean, readable body (Google Font)

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
        "&nbsp;&nbsp;&nbsp;Journal&nbsp;&nbsp;&nbsp;Shop"
        "&nbsp;&nbsp;&nbsp;Contact",
        HEAD_DARK, "center", 14, weight=500)], 50)
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
# BLOG / JOURNAL PAGES
# ===========================================================================
def article_card(i, cat, title, excerpt, meta, col_size=33, label=None):
    return column([
        img(tile_url(i, 640, 440, label or cat), rounded=14),
        spacer(16),
        eyebrow(cat, MAGENTA, "left"),
        spacer(8),
        heading(title, "h4", HEAD_DARK, "left", FONT_HEAD, 700, 22, 1.3,
                -0.3),
        spacer(8),
        paragraph(excerpt, BODY_MUTED, "left", 15, 1.7),
        spacer(10),
        paragraph(meta, META, "left", 13, 1.4),
        spacer(24),
    ], col_size)


def s_featured_post():
    img_col = column([img(tile_url(6, 900, 620, "Featured"), 18)], 55)
    text_col = column([
        eyebrow("Featured · Studio Notes", MAGENTA, "left"),
        spacer(12),
        heading("Why I paint in the loudest colours I can find", "h2",
                HEAD_DARK, "left", FONT_HEAD, 800, 40, 1.2, -0.5),
        spacer(14),
        paragraph("A long read on colour, chaos and process — and why "
                  "restraint has never really been my thing.",
                  BODY_MUTED, "left", 18, 1.75),
        spacer(16),
        paragraph("By Whatshername&nbsp;&nbsp;·&nbsp;&nbsp;13 Aug 2026"
                  "&nbsp;&nbsp;·&nbsp;&nbsp;6 min read",
                  META, "left", 14, 1.4),
        spacer(22),
        button("Read the Article", align="left", link="#"),
    ], 45)
    return section([img_col, text_col],
                   {**bg(WHITE, 90, 60), "gap": "wider"})


def s_blog_grid():
    tabs = section([column([paragraph(
        '<strong style="color:%s">All</strong>&nbsp;&nbsp;&nbsp;&nbsp;'
        'Studio&nbsp;Notes&nbsp;&nbsp;&nbsp;&nbsp;Shows&nbsp;&nbsp;&nbsp;&nbsp;'
        'Process&nbsp;&nbsp;&nbsp;&nbsp;Prints&nbsp;&nbsp;&nbsp;&nbsp;News'
        % PURPLE, BODY_MUTED, "center", 16, 1.5, weight=600)])], inner=True)

    posts = [
        ("Studio Notes", "The colours I keep coming back to",
         "Five pigments that show up in almost everything I make, and why.",
         "11 Aug 2026 · 4 min"),
        ("Shows", "Behind the scenes of &ldquo;Loud Quiet&rdquo;",
         "Hanging a full room of large canvases the night before opening.",
         "02 Aug 2026 · 5 min"),
        ("Process", "How a painting actually starts",
         "From a blurry feeling to a first mark — my messy beginning.",
         "24 Jul 2026 · 6 min"),
        ("Prints", "What &lsquo;limited edition&rsquo; really means",
         "A plain-English guide to editions, numbering and archival prints.",
         "15 Jul 2026 · 3 min"),
        ("News", "New murals coming to the high street",
         "Three commissions announced for the autumn — here's the plan.",
         "03 Jul 2026 · 2 min"),
        ("Studio Notes", "On making loud art quietly",
         "Why the noisiest paintings come from the calmest mornings.",
         "21 Jun 2026 · 4 min"),
    ]
    rows, row = [], []
    for i, (cat, title, exc, meta) in enumerate(posts):
        row.append(article_card(i + 1, cat, title, exc, meta, 33))
        if len(row) == 3:
            rows.append(section(row, {"gap": "extended"}, inner=True))
            row = []
    if row:
        rows.append(section(row, {"gap": "extended"}, inner=True))
    load = column([spacer(14), button("Load More Articles", link="#")])
    return section([column([tabs, spacer(40)] + rows + [load])],
                   bg(BG_LIGHT, 90, 90))


# ---- single article ----
def s_article_hero():
    col = column([
        eyebrow("Studio Notes", "rgba(255,255,255,0.85)"),
        spacer(14),
        heading("Street art, colour theory, and painting out loud", "h1",
                WHITE, "center", FONT_HEAD, 800, 52, 1.12, -1, mobile=34),
        spacer(16),
        paragraph("By Whatshername&nbsp;&nbsp;·&nbsp;&nbsp;13 August 2026"
                  "&nbsp;&nbsp;·&nbsp;&nbsp;6 min read",
                  "rgba(255,255,255,0.9)", "center", 15, 1.5),
    ])
    return section([col], gradient_bg(GRAD_A, GRAD_B, 135, 110, 90))


def quote_block(text, who):
    inner = [
        heading(text, "h4", HEAD_DARK, "left", FONT_HEAD, 600, 24, 1.5, -0.3,
                extra={"typography_font_style": "italic"}),
        spacer(10),
        paragraph(who, MAGENTA, "left", 14, 1.4, weight=700),
    ]
    s = {"background_background": "classic", "background_color": BG_LIGHT,
         "border_radius": radius(14), "padding": px(28, 32, 28, 32),
         "border_border": "solid", "border_width": px(0, 0, 0, 5),
         "border_color": MAGENTA}
    return section([column(inner)], s, inner=True)


def mini_post(i, title, date):
    return section([
        column([img(tile_url(i, 200, 200, "·"), 10)], 30),
        column([
            heading(title, "h6", HEAD_DARK, "left", FONT_HEAD, 600, 15, 1.35,
                    -0.2),
            paragraph(date, META, "left", 12, 1.3),
        ], 70),
    ], {"gap": "narrow"}, inner=True)


def sidebar_card(title, elements):
    kids = [heading(title, "h5", HEAD_DARK, "left", FONT_HEAD, 700, 18, 1.3,
                    -0.3), spacer(16)] + elements
    return section([column(kids)], card(WHITE, 26), inner=True)


def s_article_body():
    p = BODY_MUTED
    main = column([
        img(tile_url(2, 960, 560, "Featured+Image"), 18),
        spacer(28),
        paragraph("There's a myth that good taste means restraint. I've never "
                  "believed it. The work that moves me is the work that isn't "
                  "afraid to be too much — too bright, too fast, too honest.",
                  p, "left", 18, 1.85),
        paragraph("This piece started, like most of them, with a feeling I "
                  "couldn't name. So I reached for the loudest colour on the "
                  "table and started making marks until the feeling had a "
                  "shape.", p, "left", 18, 1.85),
        spacer(14),
        quote_block("&ldquo;Colour is the place where our brain and the "
                    "universe meet.&rdquo;", "— a line I keep above the easel"),
        spacer(20),
        heading("Colour as a language", "h3", HEAD_DARK, "left", FONT_HEAD,
                700, 30, 1.25, -0.5),
        spacer(10),
        paragraph("Every hue carries a mood. Magenta shouts, cyan hums, "
                  "yellow laughs. When I put them next to each other, I'm "
                  "really writing a sentence — the composition is just "
                  "grammar.", p, "left", 18, 1.85),
        spacer(10),
        img(tile_url(4, 960, 520, "In+the+Studio"), 18),
        spacer(24),
        paragraph("By the end, the painting knows more than I did when I "
                  "started. That's the whole point of making it.",
                  p, "left", 18, 1.85),
        spacer(22),
        paragraph('<strong style="color:%s">Filed under:</strong> '
                  '&nbsp;Studio Notes&nbsp;&nbsp;·&nbsp;&nbsp;Process'
                  '&nbsp;&nbsp;·&nbsp;&nbsp;Colour' % HEAD_DARK,
                  BODY_MUTED, "left", 14, 1.6),
    ], 64)

    cats = []
    for name in ["Studio Notes (12)", "Shows (6)", "Process (9)",
                 "Prints (4)", "News (7)"]:
        cats.append(paragraph(
            f'<a href="#" style="color:{HEAD_DARK};text-decoration:none">'
            f'{name}</a>', HEAD_DARK, "left", 15, 2.1))

    recents = [
        mini_post(1, "The colours I keep coming back to", "11 Aug 2026"),
        spacer(16),
        mini_post(3, "How a painting actually starts", "24 Jul 2026"),
        spacer(16),
        mini_post(5, "New murals coming to the high street", "03 Jul 2026"),
    ]

    tags = [paragraph(
        "&nbsp;Colour&nbsp; &nbsp;Acrylic&nbsp; &nbsp;Studio&nbsp; "
        "&nbsp;Prints&nbsp; &nbsp;Shows&nbsp; &nbsp;Process&nbsp;",
        PURPLE, "left", 14, 2.4, weight=600)]

    sidebar = column([
        sidebar_card("Categories", cats),
        spacer(24),
        sidebar_card("Recent Posts", recents),
        spacer(24),
        sidebar_card("Tags", tags),
    ], 32)
    return section([main, sidebar], {**bg(WHITE, 80, 80), "gap": "wider"})


def s_related():
    head = column([
        eyebrow("Keep Reading"),
        spacer(12),
        heading("More from the journal", "h2", HEAD_DARK, "center",
                FONT_HEAD, 700, 40, 1.15, -0.5),
    ])
    posts = [
        ("Studio Notes", "The colours I keep coming back to",
         "Five pigments that show up in almost everything I make.",
         "11 Aug 2026 · 4 min"),
        ("Shows", "Behind the scenes of &ldquo;Loud Quiet&rdquo;",
         "Hanging a full room of canvases the night before opening.",
         "02 Aug 2026 · 5 min"),
        ("Process", "How a painting actually starts",
         "From a blurry feeling to a first mark on the canvas.",
         "24 Jul 2026 · 6 min"),
    ]
    cards = section([article_card(i + 7, c, t, e, m, 33)
                     for i, (c, t, e, m) in enumerate(posts)],
                    {"gap": "extended"}, inner=True)
    return section([column([head, spacer(44), cards])], bg(BG_LIGHT, 90, 90))


# ===========================================================================
# ELEMENTOR PRO — THEME BUILDER TEMPLATES (dynamic)
# ===========================================================================
# These use Pro "Theme" widgets that pull the real post data automatically,
# so no fragile dynamic-tag encoding is needed. Assign display conditions
# after import (documented in the README).

def w_nav_menu():
    s = {"menu": "", "align_items": "center", "pointer": "underline",
         "menu_typography_typography": "custom",
         "menu_typography_font_family": FONT_HEAD,
         "menu_typography_font_weight": "500",
         "menu_typography_font_size": size(15),
         "color_menu_item": HEAD_DARK, "color_menu_item_hover": PURPLE,
         "pointer_color_hover": PURPLE}
    return widget("nav-menu", s)


def w_archive_title():
    s = {"header_size": "h1", "align": "center", "title_color": WHITE}
    s.update(typo(FONT_HEAD, 800, 60, 1.05, -1))
    return widget("archive-title", s)


def w_archive_posts():
    s = {"_skin": "classic",
         "classic_columns": "3", "classic_columns_tablet": "2",
         "classic_columns_mobile": "1",
         "classic_row_gap": {"unit": "px", "size": 40, "sizes": []},
         "classic_show_excerpt": "yes", "classic_excerpt_length": 18,
         "classic_meta_data": ["date", "comments"],
         "classic_read_more_text": "Read more →",
         "title_color": HEAD_DARK, "excerpt_color": BODY_MUTED,
         "meta_color": META}
    s.update({f"title_typography_{k}": v
              for k, v in typo(FONT_HEAD, 700, 22, 1.3).items()})
    return widget("archive-posts", s)


def w_post_title(color=WHITE, align="center", fsize=52):
    s = {"title_tag": "h1", "align": align, "title_color": color}
    s.update(typo(FONT_HEAD, 800, fsize, 1.12, -1))
    return widget("theme-post-title", s)


def w_post_info(color=WHITE, align="center"):
    s = {"align": align, "text_color": color, "icon_color": color}
    s.update({f"list_typography_{k}": v
              for k, v in typo(FONT_BODY, 500, 14).items()})
    return widget("post-info", s)


def w_featured_image(rounded=18):
    return widget("theme-post-featured-image",
                  {"image_size": "large", "align": "center",
                   "image_border_radius": radius(rounded)})


def w_post_content():
    s = {"text_color": BODY_MUTED}
    s.update(typo(FONT_BODY, 400, 18, 1.85))
    return widget("theme-post-content", s)


def w_related_posts():
    s = {"_skin": "classic",
         "posts_post_type": "post", "posts_posts_per_page": 3,
         "classic_columns": "3", "classic_columns_mobile": "1",
         "classic_row_gap": {"unit": "px", "size": 32, "sizes": []},
         "classic_show_excerpt": "yes", "classic_excerpt_length": 14,
         "classic_meta_data": ["date"],
         "title_color": HEAD_DARK, "excerpt_color": BODY_MUTED,
         "meta_color": META}
    s.update({f"title_typography_{k}": v
              for k, v in typo(FONT_HEAD, 700, 20, 1.3).items()})
    return widget("posts", s)


def t_header():
    logo = column([heading(BRAND, "h4", MAGENTA_POP, "left", FONT_HEAD, 700, 26,
                           1, -0.5)], 25)
    nav = column([w_nav_menu()], 50)
    cta = column([button("Commission", align="right", small=True)], 25)
    return [section([logo, nav, cta],
                    {**bg(WHITE, 18, 18), "border_border": "solid",
                     "border_width": px(0, 0, 1, 0), "border_color": BORDER})]


def t_footer():
    return [s_newsletter(), s_footer()]


def t_archive():
    header = section([column([
        eyebrow("The Journal", "rgba(255,255,255,0.85)"),
        spacer(12), w_archive_title(), spacer(12),
        paragraph("Essays, studio notes and news from behind the canvas.",
                  "rgba(255,255,255,0.9)", "center", 18, 1.7),
    ])], gradient_bg(GRAD_A, GRAD_B, 135, 100, 100))
    grid = section([column([w_archive_posts()])], bg(BG_LIGHT, 90, 90))
    return [header, grid]


def t_single():
    header = section([column([
        w_post_title(WHITE, "center", 52),
        spacer(16), w_post_info(WHITE, "center"),
    ])], gradient_bg(GRAD_A, GRAD_B, 135, 110, 80))
    body = section([column([
        w_featured_image(18), spacer(30), w_post_content(),
    ])], {**bg(WHITE, 70, 70),
          "content_width": {"unit": "px", "size": 820, "sizes": []}})
    related = section([column([
        eyebrow("Keep Reading"), spacer(12),
        heading("More from the journal", "h2", HEAD_DARK, "center",
                FONT_HEAD, 700, 40, 1.15, -0.5),
        spacer(40), w_related_posts(),
    ])], bg(BG_LIGHT, 90, 90))
    return [header, body, related]


# ===========================================================================
# ABOUT + CONTACT PAGES
# ===========================================================================
def s_about_intro():
    portrait = column([img(tile_url(6, 620, 720, "Portrait"), 18)], 45)
    text = column([
        eyebrow("Meet the Artist", MAGENTA, "left"),
        spacer(12),
        heading("Hi, I'm Whatshername — I make loud, feeling-first art.",
                "h2", HEAD_DARK, "left", FONT_HEAD, 800, 40, 1.2, -0.5),
        spacer(16),
        paragraph("I'm a contemporary painter working in acrylic and mixed "
                  "media. My work is about big feelings and the colours that "
                  "come with them — joy, noise, restlessness and calm.",
                  BODY_MUTED, "left", 18, 1.8),
        paragraph("Based in London, I show work in galleries, paint murals, "
                  "and make limited prints so the art can live in more homes.",
                  BODY_MUTED, "left", 18, 1.8),
        spacer(20),
        button("See the Gallery", align="left", link="#"),
    ], 55)
    return section([portrait, text], {**bg(WHITE, 100, 90), "gap": "wider"})


def s_about_values():
    head = column([
        eyebrow("How I Work"),
        spacer(12),
        heading("What guides the work", "h2", HEAD_DARK, "center",
                FONT_HEAD, 700, 44, 1.15, -0.5),
    ])
    cards = section([
        service_card("fas fa-heart", "Feeling first",
                     "Every piece starts as an emotion, not a plan. The "
                     "colour follows the feeling.", PURPLE),
        service_card("fas fa-fill-drip", "Colour without apology",
                     "I use the loudest colours I can find and let them "
                     "argue with each other.", MAGENTA),
        service_card("fas fa-hands-holding-circle", "Made to be lived with",
                     "Art shouldn't sit in storage. I make work — and prints "
                     "— meant for real walls.", CYAN),
    ], {"gap": "extended"}, inner=True)
    return section([column([head, spacer(46), cards])], bg(BG_LIGHT, 100, 100))


def s_contact_body():
    info = column([
        eyebrow("Say Hello", MAGENTA, "left"),
        spacer(12),
        heading("Let's make something together.", "h2", HEAD_DARK, "left",
                FONT_HEAD, 800, 38, 1.2, -0.5),
        spacer(16),
        paragraph("Commissions, print enquiries, press or studio visits — "
                  "drop a note and I'll get back to you within a few days.",
                  BODY_MUTED, "left", 18, 1.8),
        spacer(22),
        paragraph('<strong style="color:%s">Email</strong><br>'
                  'hello@whatshername.uk' % HEAD_DARK, BODY_MUTED, "left",
                  16, 1.9),
        paragraph('<strong style="color:%s">Studio</strong><br>'
                  'Unit 4, Bright Lane, London' % HEAD_DARK, BODY_MUTED,
                  "left", 16, 1.9),
        paragraph('<strong style="color:%s">Instagram</strong><br>'
                  '@whatshername.uk' % HEAD_DARK, BODY_MUTED, "left", 16,
                  1.9),
    ], 45)
    form = column([section([column([w_contact_form()], 100,
                                    {"padding": px(0, 0, 0, 0)})],
                           card(WHITE, 36), inner=True)], 55)
    return section([info, form], {**bg(WHITE, 100, 90), "gap": "wider"})


def w_contact_form():
    fields = [
        {"_id": "name", "field_type": "text", "field_label": "Name",
         "placeholder": "Your name", "required": "true", "width": "100"},
        {"_id": "email", "field_type": "email", "field_label": "Email",
         "placeholder": "you@email.com", "required": "true", "width": "100"},
        {"_id": "subject", "field_type": "text", "field_label": "Subject",
         "placeholder": "Commission / Print / Press", "width": "100"},
        {"_id": "message", "field_type": "textarea", "field_label": "Message",
         "placeholder": "Tell me a little about what you have in mind",
         "required": "true", "width": "100", "rows": 5},
    ]
    s = {"form_name": "Contact", "form_fields": fields,
         "button_text": "Send Message", "button_size": "md",
         "button_width": "100", "button_background_color": MAGENTA,
         "label_typography_typography": "custom",
         "label_typography_font_family": FONT_HEAD,
         "label_typography_font_weight": "600",
         "button_typography_typography": "custom",
         "button_typography_font_family": FONT_HEAD,
         "button_typography_font_weight": "600",
         "button_border_radius": radius(50)}
    return widget("form", s)


def s_contact_map():
    return section([column([
        widget("google_maps", {"address": "London, UK",
                               "zoom": {"unit": "px", "size": 12,
                                        "sizes": []},
                               "height": {"unit": "px", "size": 420,
                                          "sizes": []},
                               "css_filters_css_filter": "custom",
                               "css_filters_saturate": {"unit": "px",
                                                        "size": 0,
                                                        "sizes": []}})
    ])], {"padding": px(0, 0, 0, 0)})


# ===========================================================================
# ASSEMBLE + WRITE
# ===========================================================================
def write(name, data):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("wrote", path)


# ---------------------------------------------------------------------------
# PAGES (content only — global Header/Footer templates wrap them)
# ---------------------------------------------------------------------------
PAGES = {
    "home": ("Home", [
        s_hero(), s_recent(), s_services(), s_band(), s_about()]),
    "about": ("About", [
        s_page_header("About", "About the Artist",
                      "Contemporary painter. Big feelings, louder colours."),
        s_about_intro(), s_about_values(), s_about()]),
    "gallery": ("Gallery", [
        s_page_header("Portfolio", "Gallery",
                      "A living collection of paintings, prints and murals — "
                      "filter by type or just scroll and enjoy."),
        s_gallery_body()]),
    "shop": ("Shop", [
        s_page_header("Buy Art", "Shop",
                      "Take a piece home. Original paintings and limited "
                      "prints, shipped worldwide."),
        s_shop_body()]),
    "blog": ("Journal", [
        s_page_header("The Journal", "Studio Journal",
                      "Essays, studio notes and news from behind the "
                      "canvas."),
        s_featured_post(), s_blog_grid()]),
    "single-article": ("Article (static)", [
        s_article_hero(), s_article_body(), s_related()]),
    "contact": ("Contact", [
        s_page_header("Contact", "Say Hello",
                      "Commissions, prints, press and studio visits."),
        s_contact_body(), s_contact_map()]),
}

for slug, (title, content) in PAGES.items():
    write(f"{slug}.json", wrap(f"{BRAND} — {title}", content, "page"))

# ---------------------------------------------------------------------------
# THEME BUILDER TEMPLATES (Elementor Pro — dynamic)
# ---------------------------------------------------------------------------
THEME_TEMPLATES = {
    "header":      ("Header", "header", t_header()),
    "footer":      ("Footer", "footer", t_footer()),
    "archive":     ("Journal Archive", "archive", t_archive()),
    "single-post": ("Single Post", "single-post", t_single()),
}
for slug, (title, dtype, content) in THEME_TEMPLATES.items():
    write(f"tb-{slug}.json", wrap(f"{BRAND} — {title}", content, dtype))

# ---------------------------------------------------------------------------
# REUSABLE SECTION BLOCKS
# ---------------------------------------------------------------------------
write("section-hero.json", wrap(f"{BRAND} — Hero", [s_hero()], "section"))
write("section-featured-post.json", wrap(f"{BRAND} — Featured Post",
                                         [s_featured_post()], "section"))
write("section-services.json", wrap(f"{BRAND} — Services",
                                    [s_services()], "section"))
write("section-gradient-band.json", wrap(f"{BRAND} — Gradient Band",
                                         [s_band()], "section"))
write("section-newsletter.json", wrap(f"{BRAND} — Newsletter",
                                      [s_newsletter()], "section"))


# ===========================================================================
# ELEMENTOR "IMPORT/EXPORT KIT" PACKAGE  (one-click import, Pro)
# ===========================================================================
import shutil
import zipfile
import datetime

KIT_DIR = os.path.join(os.path.dirname(__file__), "kit-build")
KIT_ZIP = os.path.join(os.path.dirname(__file__), "whatshername-kit.zip")


def site_settings():
    def col(_id, title, color):
        return {"_id": _id, "title": title, "color": color}

    def typ(_id, title, weight):
        return {"_id": _id, "title": title, "typography_typography": "custom",
                "typography_font_family": FONT_HEAD,
                "typography_font_weight": weight}
    return {"settings": {
        "template": "default",
        "system_colors": [
            col("primary", "Primary", PURPLE),
            col("secondary", "Secondary", MAGENTA),
            col("text", "Text", HEAD_DARK),
            col("accent", "Accent", CYAN)],
        "custom_colors": [
            col("gstart", "Gradient Start", GRAD_A),
            col("gend", "Gradient End", GRAD_B),
            col("cyan", "Cyan", CYAN),
            col("yellow", "Yellow", YELLOW)],
        "system_typography": [
            typ("primary", "Primary", "700"),
            typ("secondary", "Secondary", "800"),
            typ("text", "Text", "400"),
            typ("accent", "Accent", "600")],
        "custom_typography": [],
        "default_generic_fonts": "Sans-serif",
        "body_typography_typography": "custom",
        "body_typography_font_family": FONT_BODY,
        "body_typography_font_weight": "400",
    }}


def build_kit():
    if os.path.isdir(KIT_DIR):
        shutil.rmtree(KIT_DIR)
    page_dir = os.path.join(KIT_DIR, "content", "page")
    tmpl_dir = os.path.join(KIT_DIR, "templates")
    os.makedirs(page_dir)
    os.makedirs(tmpl_dir)

    def dump(path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    manifest = {
        "name": "whatshername",
        "title": "Whatshername",
        "description": "Bright creative-portfolio kit for an artist site.",
        "author": "Whatshername.uk",
        "version": "1.0.0",
        "elementor_version": "3.20.0",
        "created": datetime.datetime.utcnow().isoformat() + "Z",
        "thumbnail": False,
        "site": "https://whatshername.uk",
        "plugins": [
            {"name": "Elementor", "plugin": "elementor/elementor",
             "pluginUri": "https://elementor.com/", "version": "3.20.0"},
            {"name": "Elementor Pro",
             "plugin": "elementor-pro/elementor-pro",
             "pluginUri": "https://elementor.com/pro/", "version": "3.20.0"}],
        "templates": {},
        "content": {"page": {}},
        "wp-content": {},
        "site-settings": {"globalColors": True, "globalTypography": True,
                          "settings": True, "themeStyleSettings": True},
    }

    # pages -> content/page/<id>.json
    pid = 2001
    for slug, (title, content) in PAGES.items():
        doc = wrap(f"{BRAND} — {title}", content, "page")
        doc["metadata"] = {"template_type": "wp-page"}
        dump(os.path.join(page_dir, f"{pid}.json"), doc)
        manifest["content"]["page"][str(pid)] = {
            "id": pid, "title": f"{BRAND} — {title}", "doc_type": "wp-page",
            "thumbnail": False, "show_instructions": False}
        pid += 1

    # theme-builder templates -> templates/<id>.json  (+ display conditions)
    conditions = {
        "header": [{"type": "include", "name": "general"}],
        "footer": [{"type": "include", "name": "general"}],
        "archive": [{"type": "include", "name": "archive"}],
        "single-post": [{"type": "include", "name": "singular",
                         "sub_name": "post"}],
    }
    tid = 1001
    for slug, (title, dtype, content) in THEME_TEMPLATES.items():
        doc = wrap(f"{BRAND} — {title}", content, dtype)
        doc["metadata"] = {"template_type": dtype}
        dump(os.path.join(tmpl_dir, f"{tid}.json"), doc)
        manifest["templates"][str(tid)] = {
            "id": tid, "title": f"{BRAND} — {title}", "doc_type": dtype,
            "type": dtype, "conditions": conditions[slug]}
        tid += 1

    dump(os.path.join(KIT_DIR, "site-settings.json"), site_settings())
    dump(os.path.join(KIT_DIR, "manifest.json"), manifest)

    # zip it
    if os.path.exists(KIT_ZIP):
        os.remove(KIT_ZIP)
    with zipfile.ZipFile(KIT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(KIT_DIR):
            for fn in files:
                full = os.path.join(root, fn)
                z.write(full, os.path.relpath(full, KIT_DIR))
    print("built kit:", KIT_ZIP)


build_kit()

print("\nDesign tokens:")
print(" white", WHITE, "| purple", PURPLE, "| magenta", MAGENTA,
      "| gradient", GRAD_A, "->", GRAD_B)
print(" fonts:", FONT_HEAD, "(headings) /", FONT_BODY, "(body)")
