#!/usr/bin/env python3
"""
Minimalist "Whatshername" Elementor Pro kit generator.

Editorial / gallery aesthetic: white space, hairline dividers, a circular
red marker, typewriter fonts (Special Elite + Courier Prime), a single light-red
accent, and framed artwork on white.

Run:  python3 build_minimal.py
Outputs to ./templates-minimal/ and packages ./whatshername-minimal-kit.zip
"""
import json
import os
import secrets
import shutil
import zipfile
import datetime

OUT = os.path.join(os.path.dirname(__file__), "templates-minimal")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- tokens
WHITE   = "#FFFFFF"
INK     = "#2B2B2B"
BODY    = "#4A4A4A"
MUTED   = "#8A8A8A"
BAR     = "#3C3C3C"
BAR_INK = "#EDEDED"
LINE    = "#E6E6E6"
FRAME   = "#E0E0E0"
RED     = "#E0574F"   # light red accent (decorative)
RED_INK = "#BF3B34"   # darker red for text/links (AA on white)

FONT_DISPLAY = "Special Elite"   # typewriter display (400 only)
FONT_BODY    = "Courier Prime"   # typewriter body

BRAND = "Whatshername"
# swap these for real artwork in the WordPress Media Library after import
def art_ph(label="Artwork"):
    return f"https://via.placeholder.com/900x1200/f2f2f2/999999?text={label}"


def nid():
    return secrets.token_hex(4)[:7]


# ---------------------------------------------------------------- builders
def section(elements, settings=None, inner=False):
    return {"id": nid(), "elType": "section", "settings": settings or {},
            "elements": elements, "isInner": inner}


def column(elements, size=100, extra=None):
    s = {"_column_size": size, "_inline_size": None}
    if extra:
        s.update(extra)
    return {"id": nid(), "elType": "column", "settings": s,
            "elements": elements, "isInner": False}


def widget(wtype, settings):
    return {"id": nid(), "elType": "widget", "settings": settings,
            "elements": [], "widgetType": wtype}


def px(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": t == r == b == l}


def size(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


def radius(n):
    return {"unit": "px", "top": str(n), "right": str(n), "bottom": str(n),
            "left": str(n), "isLinked": True}


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


def heading(text, tag="h2", color=INK, align="center", fsize=34, lh=1.15,
            ls=0, mobile=None, family=FONT_DISPLAY, weight=400):
    s = {"title": text, "header_size": tag, "align": align,
         "title_color": color}
    s.update(typo(family, weight, fsize, lh, ls))
    if mobile:
        s["typography_font_size_mobile"] = size(mobile)
    return widget("heading", s)


def paragraph(html, color=BODY, align="center", fsize=16, lh=1.85, weight=400):
    s = {"editor": f"<p>{html}</p>", "align": align, "text_color": color}
    s.update(typo(FONT_BODY, weight, fsize, lh))
    return widget("text-editor", s)


def kicker(text, align="center", color=MUTED):
    s = {"title": text, "header_size": "h6", "align": align,
         "title_color": color}
    s.update(typo(FONT_BODY, 400, 12, transform="uppercase"))
    s["typography_letter_spacing"] = size(4)
    return widget("heading", s)


def link_button(text, align="center", link="#"):
    s = {"text": text, "align": align,
         "link": {"url": link, "is_external": "", "nofollow": ""},
         "background_color": "rgba(0,0,0,0)", "button_text_color": INK,
         "border_border": "solid", "border_width": px(0, 0, 2, 0),
         "border_color": RED, "border_radius": radius(0),
         "text_padding": px(6, 2, 8, 2)}
    s.update(typo(FONT_BODY, 700, 13, transform="uppercase"))
    s["typography_letter_spacing"] = size(2)
    return widget("button", s)


def spacer(h):
    return widget("spacer", {"space": size(h)})


def marker():
    """Hairline-topped circular red icon marker."""
    icon = widget("icon", {
        "selected_icon": {"value": "fas fa-bars", "library": "fa-solid"},
        "view": "stacked", "shape": "circle", "primary_color": RED,
        "size": size(15), "align": "center"})
    return section([column([icon])], {
        "padding": px(30, 0, 30, 0),
        "border_border": "solid", "border_width": px(1, 0, 0, 0),
        "border_color": LINE,
        "content_width": {"unit": "px", "size": 520, "sizes": []}})


def framed(url, label="Artwork"):
    image = widget("image", {"image": {"url": url, "id": ""},
                             "image_size": "full", "align": "center"})
    return section([column([image], 100, {
        "background_background": "classic", "background_color": WHITE,
        "border_border": "solid", "border_width": px(1, 1, 1, 1),
        "border_color": FRAME, "padding": px(14, 14, 14, 14),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 14, "blur": 30,
                                  "spread": 0, "color": "rgba(0,0,0,0.08)"}})],
        inner=True)


def caption(title, meta, price=None):
    els = [spacer(12),
           heading(title, "h5", INK, "left", 16, 1.3),
           paragraph(meta, MUTED, "left", 12, 1.4)]
    if price:
        els.append(paragraph(price, RED_INK, "left", 13, 1.4, weight=700))
    return els


def piece(url, title, meta, price=None, label="Artwork", col=33):
    return column([framed(url, label)] + caption(title, meta, price), col)


def wsec(elements, top=90, bottom=90, color=WHITE, extra=None):
    s = {"background_background": "classic", "background_color": color,
         "padding": px(top, 0, bottom, 0)}
    if extra:
        s.update(extra)
    return section(elements, s)


def wrap(title, content, ttype="page"):
    return {"content": content, "page_settings": {}, "version": "0.4",
            "title": title, "type": ttype}


# ---------------------------------------------------------------- pieces data
WORKS = [
    ("Love, Always", "Original · Acrylic", "£1,200"),
    ("Little Icon", "Original · Mixed media", "£1,450"),
    ("Sweetheart", "Original · Acrylic", "£1,100"),
    ("Blue Mood", "Original · Acrylic", "£980"),
    ("Firestarter", "Original · Acrylic", "£1,350"),
    ("Hearts on Fire", "Print · Edition of 25", "£95"),
]


# ---------------------------------------------------------------- theme parts
def t_header():
    brand = column([heading(BRAND, "h4", WHITE, "left", 24, 1)], 40)
    nav = column([widget("nav-menu", {
        "menu": "", "align_items": "right",
        "color_menu_item": BAR_INK, "color_menu_item_hover": RED,
        "menu_typography_typography": "custom",
        "menu_typography_font_family": FONT_BODY,
        "menu_typography_font_size": size(12),
        "menu_typography_letter_spacing": size(2),
        "menu_typography_text_transform": "uppercase"})], 60)
    return [wsec([brand, nav], 18, 18, BAR)]


def t_footer():
    inner = column([
        heading(BRAND, "h4", INK, "center", 20, 1),
        spacer(12),
        paragraph('<a href="#" style="color:%s">Work</a>&nbsp;&nbsp;·&nbsp;&nbsp;'
                  '<a href="#" style="color:%s">About</a>&nbsp;&nbsp;·&nbsp;&nbsp;'
                  '<a href="#" style="color:%s">Journal</a>&nbsp;&nbsp;·&nbsp;&nbsp;'
                  '<a href="#" style="color:%s">Shop</a>&nbsp;&nbsp;·&nbsp;&nbsp;'
                  '<a href="#" style="color:%s">Contact</a>'
                  % (MUTED, MUTED, MUTED, MUTED, MUTED),
                  MUTED, "center", 12, 1.6),
        spacer(14),
        paragraph("© 2026 Whatshername.uk — original artwork, hand-painted "
                  "in the UK.", MUTED, "center", 12, 1.5),
    ])
    return [wsec([inner], 46, 46, WHITE,
                 {"border_border": "solid", "border_width": px(1, 0, 0, 0),
                  "border_color": LINE})]


# ---------------------------------------------------------------- pages
def hero(kick, title, sub=None, big=66, mobile=40, pad_top=100, pad_bot=60):
    els = [kicker(kick), spacer(20),
           heading(title, "h1", INK, "center", big, 1.1, 1, mobile)]
    if sub:
        els += [spacer(18), paragraph(sub, MUTED, "center", 15, 1.6)]
    return wsec([column(els)], pad_top, pad_bot)


def p_home():
    statement = wsec([column([
        heading("The Work", "h2", INK, "center", 30),
        spacer(16),
        paragraph("Bold, hand-painted characters bursting with colour, hearts "
                  "and movement — each an original on canvas, signed and one "
                  "of a kind.", BODY, "center", 17, 1.9),
        paragraph('The frame is quiet on purpose. The '
                  '<span style="color:%s">art</span> does the shouting.'
                  % RED_INK, BODY, "center", 17, 1.9),
    ])], 66, 40, WHITE, {"content_width": {"unit": "px", "size": 720,
                                           "sizes": []}})
    selected = wsec([column([
        heading("Selected Work", "h2", INK, "center", 30),
        spacer(40),
        section([piece(art_ph(WORKS[i][0].split()[0]), WORKS[i][0],
                       WORKS[i][1]) for i in (0, 1, 3)],
                {"gap": "wide"}, inner=True),
        spacer(44),
        link_button("View the full gallery", link="#"),
    ])], 70, 90)
    return [hero("Contemporary Pop Artist", BRAND,
                 "Loud, playful, character-led paintings — one of a kind."),
            marker(), statement, marker(), selected]


def p_gallery():
    tabs = paragraph('<strong style="color:%s">All</strong>&nbsp;&nbsp;&nbsp;'
                     'Originals&nbsp;&nbsp;&nbsp;Prints&nbsp;&nbsp;&nbsp;'
                     'Hearts&nbsp;&nbsp;&nbsp;Sold' % RED_INK,
                     MUTED, "center", 13, 1.5, weight=700)
    rows, row = [], []
    for i, (t, m, pr) in enumerate(WORKS):
        row.append(piece(art_ph(t.split()[0]), t, m, pr))
        if len(row) == 3:
            rows.append(section(row, {"gap": "wide"}, inner=True))
            rows.append(section([column([spacer(30)])], inner=True))
            row = []
    if row:
        rows.append(section(row, {"gap": "wide"}, inner=True))
    body = wsec([column([tabs, spacer(40)] + rows +
                        [spacer(20), link_button("Load more work")])], 40, 90)
    return [hero("The Collection", "Gallery", big=54, pad_top=80,
                 pad_bot=30), body]


def p_about():
    split = wsec([
        column([framed(art_ph("Portrait"), "Portrait")], 42),
        column([
            kicker("In the studio", "left"),
            spacer(10),
            heading("I paint the characters we grew up with — loud, and full "
                    "of heart.", "h2", INK, "left", 28, 1.25),
            spacer(14),
            paragraph("I'm a contemporary pop artist. My work takes familiar, "
                      "playful characters and reimagines them in thick paint, "
                      "scribbled hearts and colour that won't sit still.",
                      BODY, "left", 17, 1.9),
            paragraph("Every canvas is an original — hand-painted, signed, and "
                      "made to make someone smile.", BODY, "left", 17, 1.9),
            spacer(20),
            link_button("See the gallery", "left"),
        ], 58),
    ], 70, 90, WHITE, {"gap": "wider"})
    return [hero("Meet the Artist", "About", big=54, pad_top=80, pad_bot=30),
            split]


def p_contact():
    info = wsec([column([
        paragraph("Commissions, prints, press &amp; studio visits.",
                  BODY, "center", 16, 1.7),
        spacer(8),
        paragraph('<strong style="color:%s">hello@whatshername.uk</strong>'
                  '&nbsp;&nbsp;·&nbsp;&nbsp;Unit 4, Bright Lane, London'
                  '&nbsp;&nbsp;·&nbsp;&nbsp;@whatshername.uk' % INK,
                  MUTED, "center", 14, 1.7),
    ])], 60, 20, WHITE, {"content_width": {"unit": "px", "size": 720,
                                           "sizes": []}})
    form = wsec([column([c_form()])], 30, 90, WHITE,
                {"content_width": {"unit": "px", "size": 560, "sizes": []}})
    return [hero("Say Hello", "Contact", big=54, pad_top=80, pad_bot=10),
            info, marker(), form]


def c_form():
    fields = [
        {"_id": "name", "field_type": "text", "field_label": "Name",
         "placeholder": "Your name", "required": "true", "width": "100"},
        {"_id": "email", "field_type": "email", "field_label": "Email",
         "placeholder": "you@email.com", "required": "true", "width": "100"},
        {"_id": "message", "field_type": "textarea", "field_label": "Message",
         "placeholder": "Tell me what you have in mind", "required": "true",
         "width": "100", "rows": 4},
    ]
    s = {"form_name": "Contact", "form_fields": fields,
         "button_text": "Send Message", "button_size": "sm",
         "button_background_color": INK,
         # minimalist: underline-only fields
         "border_width": {"unit": "px", "top": "0", "right": "0",
                          "bottom": "1", "left": "0", "isLinked": False},
         "border_color": INK, "field_background_color": "rgba(0,0,0,0)",
         "label_typography_typography": "custom",
         "label_typography_font_family": FONT_BODY,
         "label_typography_text_transform": "uppercase",
         "label_typography_letter_spacing": size(2),
         "label_typography_font_size": size(12),
         "button_typography_typography": "custom",
         "button_typography_font_family": FONT_BODY,
         "button_typography_text_transform": "uppercase",
         "button_typography_letter_spacing": size(2)}
    return widget("form", s)


def p_single_static():
    body = wsec([column([
        kicker("Studio Notes"),
        spacer(14),
        heading("Why every painting starts with a scribble", "h1", INK,
                "center", 40, 1.2, 0, 30),
        spacer(14),
        paragraph("By Whatshername&nbsp;&nbsp;·&nbsp;&nbsp;13 August 2026",
                  MUTED, "center", 13, 1.5),
        spacer(36),
        framed(art_ph("Featured"), "Featured"),
        spacer(30),
        paragraph("Before the characters ever appear, there's a page of pure "
                  "chaos — loops, scribbles and false starts. It looks like "
                  "nothing. It's the most important part of the whole piece.",
                  BODY, "left", 17, 1.95),
        paragraph("The scribble is where the feeling lives. Everything painted "
                  "on top is just me chasing it until it holds still.",
                  BODY, "left", 17, 1.95),
    ])], 70, 80, WHITE, {"content_width": {"unit": "px", "size": 720,
                                           "sizes": []}})
    return [body]


PAGES = {
    "home": ("Home", p_home()),
    "gallery": ("Gallery", p_gallery()),
    "about": ("About", p_about()),
    "contact": ("Contact", p_contact()),
    "single-article": ("Article (static)", p_single_static()),
}


# ---------------------------------------------------------------- dynamic (Pro)
def t_archive():
    header = hero("Studio Journal", "Journal", big=54, pad_top=80, pad_bot=20)
    posts = widget("archive-posts", {
        "_skin": "classic", "classic_columns": "1",
        "classic_show_excerpt": "yes", "classic_excerpt_length": 22,
        "classic_meta_data": ["date"], "classic_read_more_text": "Read more",
        "title_color": INK, "excerpt_color": BODY, "meta_color": MUTED})
    posts["settings"].update({f"title_typography_{k}": v for k, v in
                              typo(FONT_DISPLAY, 400, 26, 1.2).items()})
    return [header, wsec([column([posts])], 20, 90, WHITE,
                         {"content_width": {"unit": "px", "size": 760,
                                            "sizes": []}})]


def t_single():
    title = widget("theme-post-title", {"title_tag": "h1", "align": "center",
                                        "title_color": INK})
    title["settings"].update(typo(FONT_DISPLAY, 400, 44, 1.15, 0))
    info = widget("post-info", {"align": "center", "text_color": MUTED})
    info["settings"].update({f"list_typography_{k}": v for k, v in
                             typo(FONT_BODY, 400, 13).items()})
    fi = widget("theme-post-featured-image", {"image_size": "large",
                                             "align": "center"})
    content = widget("theme-post-content", {"text_color": BODY})
    content["settings"].update(typo(FONT_BODY, 400, 17, 1.95))
    body = wsec([column([title, spacer(14), info, spacer(30), fi, spacer(28),
                         content])], 70, 80, WHITE,
                {"content_width": {"unit": "px", "size": 760, "sizes": []}})
    related = wsec([column([
        heading("More from the journal", "h2", INK, "center", 30),
        spacer(30),
        widget("posts", {"_skin": "classic", "classic_columns": "3",
                         "posts_posts_per_page": 3,
                         "classic_show_excerpt": "", "classic_meta_data": [],
                         "title_color": INK})])], 60, 90, WHITE,
        {"border_border": "solid", "border_width": px(1, 0, 0, 0),
         "border_color": LINE})
    return [body, related]


THEME = {
    "header": ("Header", "header", t_header()),
    "footer": ("Footer", "footer", t_footer()),
    "archive": ("Journal Archive", "archive", t_archive()),
    "single-post": ("Single Post", "single-post", t_single()),
}


# ---------------------------------------------------------------- write + kit
def write(name, data):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(data, f, indent=2)
    print("wrote", name)


for slug, (title, content) in PAGES.items():
    write(f"{slug}.json", wrap(f"{BRAND} — {title}", content, "page"))
for slug, (title, dtype, content) in THEME.items():
    write(f"tb-{slug}.json", wrap(f"{BRAND} — {title}", content, dtype))


def site_settings():
    def c(i, t, col):
        return {"_id": i, "title": t, "color": col}

    def ty(i, t):
        return {"_id": i, "title": t, "typography_typography": "custom",
                "typography_font_family": FONT_DISPLAY,
                "typography_font_weight": "400"}
    return {"settings": {
        "system_colors": [c("primary", "Primary", RED_INK),
                          c("secondary", "Secondary", INK),
                          c("text", "Text", BODY),
                          c("accent", "Accent", RED)],
        "custom_colors": [c("bar", "Bar", BAR), c("line", "Line", LINE)],
        "system_typography": [ty("primary", "Primary"),
                              ty("secondary", "Secondary"),
                              ty("text", "Text"), ty("accent", "Accent")],
        "custom_typography": [],
        "body_typography_typography": "custom",
        "body_typography_font_family": FONT_BODY}}


def build_kit():
    kdir = os.path.join(os.path.dirname(__file__), "kit-build-min")
    if os.path.isdir(kdir):
        shutil.rmtree(kdir)
    pdir = os.path.join(kdir, "content", "page")
    tdir = os.path.join(kdir, "templates")
    os.makedirs(pdir)
    os.makedirs(tdir)

    def dump(p, d):
        with open(p, "w") as f:
            json.dump(d, f, indent=2)

    man = {"name": "whatshername-minimal", "title": "Whatshername — Minimal",
           "description": "Minimalist typewriter gallery kit.",
           "author": "Whatshername.uk", "version": "1.0.0",
           "elementor_version": "3.20.0",
           "created": datetime.datetime.utcnow().isoformat() + "Z",
           "thumbnail": False, "site": "https://whatshername.uk",
           "plugins": [{"name": "Elementor", "plugin": "elementor/elementor",
                        "pluginUri": "https://elementor.com/",
                        "version": "3.20.0"},
                       {"name": "Elementor Pro",
                        "plugin": "elementor-pro/elementor-pro",
                        "pluginUri": "https://elementor.com/pro/",
                        "version": "3.20.0"}],
           "templates": {}, "content": {"page": {}}, "wp-content": {},
           "site-settings": {"globalColors": True, "globalTypography": True,
                             "settings": True, "themeStyleSettings": True}}
    pid = 2001
    for slug, (title, content) in PAGES.items():
        d = wrap(f"{BRAND} — {title}", content, "page")
        d["metadata"] = {"template_type": "wp-page"}
        dump(os.path.join(pdir, f"{pid}.json"), d)
        man["content"]["page"][str(pid)] = {
            "id": pid, "title": f"{BRAND} — {title}", "doc_type": "wp-page",
            "thumbnail": False, "show_instructions": False}
        pid += 1
    cond = {"header": [{"type": "include", "name": "general"}],
            "footer": [{"type": "include", "name": "general"}],
            "archive": [{"type": "include", "name": "archive"}],
            "single-post": [{"type": "include", "name": "singular",
                             "sub_name": "post"}]}
    tid = 1001
    for slug, (title, dtype, content) in THEME.items():
        d = wrap(f"{BRAND} — {title}", content, dtype)
        d["metadata"] = {"template_type": dtype}
        dump(os.path.join(tdir, f"{tid}.json"), d)
        man["templates"][str(tid)] = {"id": tid, "title": f"{BRAND} — {title}",
                                      "doc_type": dtype, "type": dtype,
                                      "conditions": cond[slug]}
        tid += 1
    dump(os.path.join(kdir, "site-settings.json"), site_settings())
    dump(os.path.join(kdir, "manifest.json"), man)
    zpath = os.path.join(os.path.dirname(__file__),
                         "whatshername-minimal-kit.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(kdir):
            for fn in files:
                full = os.path.join(root, fn)
                z.write(full, os.path.relpath(full, kdir))
    print("built kit:", os.path.basename(zpath))


build_kit()
print("\nMinimal tokens: ink", INK, "| red", RED, "/", RED_INK,
      "| fonts", FONT_DISPLAY, "/", FONT_BODY)
