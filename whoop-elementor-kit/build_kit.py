#!/usr/bin/env python3
"""
Builder for the "PULSE" Elementor Template Kit.
An original, WHOOP-inspired fitness / wearable-performance design system.

Run:  python3 build_kit.py
Outputs Elementor-importable page/section template JSON into ./templates/
"""
import json
import os
import secrets

OUT = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# DESIGN SYSTEM
# ---------------------------------------------------------------------------
BG_BASE      = "#0A0B0F"   # near-black page background
BG_SURFACE   = "#14161C"   # card / panel
BG_ELEVATED  = "#1C1F27"   # raised card
TEXT_PRIMARY = "#FFFFFF"
TEXT_MUTED   = "#9CA0AD"
ACCENT       = "#00F0A4"   # electric teal-green (primary action)
ACCENT_DARK  = "#00C888"
ACCENT_2     = "#FF4D5E"   # coral (energy / alerts)
BORDER       = "#262A33"

FONT_HEAD = "Sora"         # geometric athletic display (Google Font)
FONT_BODY = "Inter"        # clean body (Google Font)


def nid():
    """7-char hex id, matching Elementor's id style."""
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


# ---------------- typography helpers ----------------
def typo(family, weight, fsize, lh=None, ls=None, transform=None):
    d = {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_weight": str(weight),
        "typography_font_size": size(fsize),
    }
    if lh is not None:
        d["typography_line_height"] = size(lh, "em")
    if ls is not None:
        d["typography_letter_spacing"] = size(ls, "px")
    if transform:
        d["typography_text_transform"] = transform
    return d


def heading(text, tag="h2", color=TEXT_PRIMARY, align="center",
            family=FONT_HEAD, weight=800, fsize=44, lh=1.1, ls=-0.5,
            transform="", mobile=None, extra=None):
    s = {"title": text, "header_size": tag, "align": align,
         "title_color": color}
    s.update(typo(family, weight, fsize, lh, ls, transform))
    if mobile:
        s["typography_font_size_mobile"] = size(mobile)
    if extra:
        s.update(extra)
    return widget("heading", s)


def paragraph(html, color=TEXT_MUTED, align="center", fsize=18, lh=1.7,
              max_w=None):
    s = {"editor": f"<p>{html}</p>", "align": align, "text_color": color}
    s.update(typo(FONT_BODY, 400, fsize, lh))
    if max_w:
        s["_element_custom_width"] = size(max_w, "%")
    return widget("text-editor", s)


def button(text, bg=ACCENT, color=BG_BASE, align="center", ghost=False,
           link="#"):
    s = {
        "text": text,
        "align": align,
        "link": {"url": link, "is_external": "", "nofollow": ""},
        "border_radius": radius(50),
        "text_padding": px(18, 38, 18, 38),
        "button_text_color": color,
    }
    s.update(typo(FONT_HEAD, 600, 15, transform="uppercase"))
    s["typography_letter_spacing"] = size(0.5)
    if ghost:
        s.update({
            "background_color": "rgba(255,255,255,0)",
            "button_text_color": TEXT_PRIMARY,
            "border_border": "solid",
            "border_width": px(1, 1, 1, 1),
            "border_color": BORDER,
        })
    else:
        s["background_color"] = bg
    return widget("button", s)


def eyebrow(text, color=ACCENT):
    s = {"title": text, "header_size": "h6", "align": "center",
         "title_color": color}
    s.update(typo(FONT_HEAD, 700, 14, transform="uppercase"))
    s["typography_letter_spacing"] = size(2.5)
    return widget("heading", s)


def spacer(h):
    return widget("spacer", {"space": size(h)})


def icon_box(icon, title, desc):
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "title_text": title,
        "description_text": desc,
        "position": "top",
        "title_color": TEXT_PRIMARY,
        "description_color": TEXT_MUTED,
        "primary_color": ACCENT,
        "icon_size": size(34),
        "icon_space": size(22),
        "text_align": "left",
    }
    s.update({f"title_typography_{k}": v
              for k, v in typo(FONT_HEAD, 700, 22, 1.3).items()})
    s.update({f"description_typography_{k}": v
              for k, v in typo(FONT_BODY, 400, 16, 1.7).items()})
    return widget("icon-box", s)


# section background presets
def bg(color, top=110, bottom=110):
    return {
        "background_background": "classic",
        "background_color": color,
        "padding": px(top, 0, bottom, 0),
    }


def card(color=BG_SURFACE, pad=36):
    return {
        "background_background": "classic",
        "background_color": color,
        "border_radius": radius(20),
        "padding": px(pad, pad, pad, pad),
        "border_border": "solid",
        "border_width": px(1, 1, 1, 1),
        "border_color": BORDER,
    }


def wrap(title, content, ttype="page"):
    return {"content": content, "page_settings": {},
            "version": "0.4", "title": title, "type": ttype}


# ===========================================================================
# SECTIONS
# ===========================================================================
def s_nav():
    logo = column([heading("PULSE", "h4", TEXT_PRIMARY, "left",
                           FONT_HEAD, 800, 26, 1, 1)], 25)
    menu = column([paragraph(
        "Features&nbsp;&nbsp;&nbsp;Membership&nbsp;&nbsp;&nbsp;"
        "Science&nbsp;&nbsp;&nbsp;Support", TEXT_MUTED, "center", 15)], 50)
    cta = column([button("Join Now", align="right")], 25)
    return section([logo, menu, cta],
                   {**bg(BG_BASE, 26, 26),
                    "border_border": "solid",
                    "border_width": px(0, 0, 1, 0),
                    "border_color": BORDER})


def s_hero():
    col = column([
        eyebrow("Wearable Performance"),
        spacer(18),
        heading("KNOW YOUR BODY.<br>UNLOCK YOUR POTENTIAL.", "h1",
                TEXT_PRIMARY, "center", FONT_HEAD, 800, 72, 1.03, -1.5,
                mobile=40),
        spacer(20),
        paragraph("24/7 tracking of strain, recovery and sleep. Personalised "
                  "insights that turn your data into real performance gains.",
                  TEXT_MUTED, "center", 20, 1.7),
        spacer(34),
        section([
            column([button("Start Free Trial")], 50),
            column([button("Watch Film", ghost=True)], 50),
        ], {"content_width": {"unit": "px", "size": 420, "sizes": []}},
            inner=True),
    ])
    return section([col], {
        **bg(BG_BASE, 130, 130),
        "background_overlay_background": "gradient",
    })


def s_stats():
    stats = [("24/7", "Continuous Tracking"),
             ("5", "Sleep Stages Measured"),
             ("100+", "Data Points / Second"),
             ("0", "Buttons to Charge")]
    cols = []
    for num, label in stats:
        cols.append(column([
            heading(num, "h3", ACCENT, "center", FONT_HEAD, 800, 52, 1, -1),
            paragraph(label, TEXT_MUTED, "center", 15, 1.5),
        ], 25))
    return section(cols, bg(BG_SURFACE, 60, 60))


def s_features():
    head = column([
        eyebrow("Why Pulse"),
        spacer(14),
        heading("Built for people who<br>take performance seriously.",
                "h2", TEXT_PRIMARY, "center", FONT_HEAD, 800, 46, 1.12, -0.5),
    ])
    feats = [
        ("fas fa-heart-pulse", "Recovery Score",
         "Every morning, know exactly how ready your body is to perform, "
         "recover or rest."),
        ("fas fa-bolt", "Strain Coach",
         "Real-time exertion tracking guides how hard to push to hit your "
         "goals without burning out."),
        ("fas fa-moon", "Sleep Tracking",
         "Automatic sleep staging and a smart coach that tells you exactly "
         "when to go to bed."),
        ("fas fa-utensils", "Stress Monitor",
         "Continuous stress readings help you spot patterns and build "
         "healthier daily habits."),
        ("fas fa-person-running", "Activity Detection",
         "Auto-detects 90+ activities and logs the effort so you never have "
         "to press start."),
        ("fas fa-shield-heart", "Health Alerts",
         "Get notified of meaningful changes in your resting heart rate and "
         "respiratory data."),
    ]
    fcols = []
    for icon, t, d in feats:
        fcols.append(column([icon_box(icon, t, d)], 33,
                            {"space_between_widgets": 0}))
    grid = section(fcols, {"gap": "extended"}, inner=True)
    body_col = column([head, spacer(50), grid])
    return section([body_col], bg(BG_BASE, 110, 110))


def s_showcase():
    text_col = column([
        eyebrow("The Membership", ACCENT),
        spacer(16),
        heading("Hardware included.<br>Insight that never stops.", "h2",
                TEXT_PRIMARY, "left", FONT_HEAD, 800, 42, 1.12, -0.5),
        spacer(18),
        paragraph("Your membership includes the device, free upgrades and "
                  "continuous coaching. No upfront hardware cost — just press "
                  "go and let the data work for you.", TEXT_MUTED, "left",
                  18, 1.75),
        spacer(26),
        button("See What's Included", align="left"),
    ], 50)
    img_col = column([
        widget("image", {
            "image": {"url": "https://via.placeholder.com/640x560/14161C/"
                             "00F0A4?text=PULSE+Band", "id": ""},
            "border_radius": radius(24),
        })
    ], 50)
    return section([text_col, img_col],
                   {**bg(BG_BASE, 90, 90), "gap": "wider"})


def pricing_card(name, price, period, features, featured=False):
    accent_col = ACCENT if featured else TEXT_PRIMARY
    inner = [
        heading(name, "h5", accent_col, "left", FONT_HEAD, 700, 20, 1.2, 0,
                "uppercase"),
        spacer(10),
        heading(price, "h3", TEXT_PRIMARY, "left", FONT_HEAD, 800, 48, 1, -1),
        paragraph(period, TEXT_MUTED, "left", 14, 1.4),
        spacer(20),
    ]
    for f in features:
        inner.append(paragraph("&#10003;&nbsp;&nbsp;" + f, TEXT_MUTED,
                               "left", 15, 2.0))
    inner.append(spacer(20))
    inner.append(button("Choose Plan",
                        bg=(ACCENT if featured else "rgba(255,255,255,0)"),
                        color=(BG_BASE if featured else TEXT_PRIMARY),
                        ghost=not featured, align="left"))
    card_settings = card(BG_ELEVATED if featured else BG_SURFACE, 40)
    if featured:
        card_settings["border_color"] = ACCENT
    return column([section([column(inner)], card_settings, inner=True)], 33)


def s_pricing():
    head = column([
        eyebrow("Membership Plans"),
        spacer(14),
        heading("Choose your commitment.", "h2", TEXT_PRIMARY, "center",
                FONT_HEAD, 800, 46, 1.1, -0.5),
        spacer(10),
        paragraph("Every plan includes the device, the app and unlimited "
                  "coaching.", TEXT_MUTED, "center", 18, 1.6),
    ])
    cards = section([
        pricing_card("Monthly", "£29", "per month, rolling",
                     ["Device included", "Free upgrades", "Cancel anytime"]),
        pricing_card("Annual", "£19", "per month, billed yearly",
                     ["Everything in Monthly", "2 months free",
                      "Priority support"], featured=True),
        pricing_card("24-Month", "£16", "per month, best value",
                     ["Everything in Annual", "Lowest price",
                      "Free accessories pack"]),
    ], {"gap": "extended"}, inner=True)
    return section([column([head, spacer(46), cards])],
                   bg(BG_SURFACE, 110, 110))


def s_testimonial():
    col = column([
        eyebrow("From the Community"),
        spacer(20),
        heading('"The recovery score completely changed how I train. '
                'I finally stopped overtraining and started making real '
                'progress."', "h3", TEXT_PRIMARY, "center", FONT_HEAD, 600,
                34, 1.35, -0.3),
        spacer(20),
        paragraph("Jordan M. — Marathon runner &amp; Pulse member", ACCENT,
                  "center", 15, 1.5),
    ])
    return section([col], bg(BG_BASE, 100, 100))


def s_cta():
    col = column([
        heading("Ready to know your body?", "h2", BG_BASE, "center",
                FONT_HEAD, 800, 52, 1.1, -1, mobile=34),
        spacer(16),
        paragraph("Join thousands unlocking better sleep, smarter training "
                  "and real recovery.", "#06140F", "center", 19, 1.6),
        spacer(30),
        button("Start Your Free Trial", bg=BG_BASE, color=ACCENT),
    ])
    return section([col], {
        "background_background": "classic",
        "background_color": ACCENT,
        "padding": px(90, 0, 90, 0),
        "border_radius": radius(28),
        "margin": px(0, 24, 60, 24),
    })


def s_footer():
    brand = column([
        heading("PULSE", "h4", TEXT_PRIMARY, "left", FONT_HEAD, 800, 24,
                1, 1),
        spacer(12),
        paragraph("Wearable performance for people who take recovery "
                  "seriously.", TEXT_MUTED, "left", 15, 1.7),
    ], 40)

    def foot_col(title, items):
        els = [heading(title, "h6", TEXT_PRIMARY, "left", FONT_HEAD, 700,
                       14, 1.4, 1, "uppercase"), spacer(14)]
        for it in items:
            els.append(paragraph(it, TEXT_MUTED, "left", 15, 2.1))
        return column(els, 20)

    return section([
        brand,
        foot_col("Product", ["Features", "Membership", "The Device",
                             "The Science"]),
        foot_col("Company", ["About", "Careers", "Press", "Contact"]),
        foot_col("Support", ["Help Centre", "Warranty", "Privacy",
                             "Terms"]),
    ], {**bg(BG_BASE, 70, 50),
        "border_border": "solid", "border_width": px(1, 0, 0, 0),
        "border_color": BORDER})


# ===========================================================================
# ASSEMBLE + WRITE
# ===========================================================================
def write(name, data):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("wrote", path)


home = wrap("PULSE — Home", [
    s_nav(), s_hero(), s_stats(), s_features(), s_showcase(),
    s_pricing(), s_testimonial(), s_cta(), s_footer(),
], "page")
write("pulse-home.json", home)

# reusable section templates (type "section")
write("section-hero.json", wrap("PULSE — Hero", [s_hero()], "section"))
write("section-pricing.json", wrap("PULSE — Pricing", [s_pricing()], "section"))
write("section-features.json", wrap("PULSE — Features", [s_features()], "section"))
write("section-cta.json", wrap("PULSE — CTA Banner", [s_cta()], "section"))

print("\nDesign tokens:")
print(" bg", BG_BASE, "| surface", BG_SURFACE, "| accent", ACCENT,
      "| accent2", ACCENT_2)
print(" fonts:", FONT_HEAD, "/", FONT_BODY)
