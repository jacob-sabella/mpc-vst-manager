#!/usr/bin/env python3
"""Draws the Plugin Manager skin's artwork into images/ (SVG). Run it after
changing the look; the layout (layout.conf) places these. Colours follow the mockup: near-black panels, grey type,
red for the main action, amber for updates and warnings, green for "tested"."""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
BG, PANEL, LINE, INK, DIM, MUTED = "#0c0c0d", "#151517", "#26272a", "#ececed", "#9da1a7", "#b4b7bc"
RED, AMBER, AMBER_TX, GREEN = "#e0342c", "#f0a830", "#f0b44a", "#7fd6a8"
FONT = "font-family=\"Titillium Web\""


def svg(name, w, h, body):
    open(os.path.join(OUT, name), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>\n' % (w, h, w, h, body))


def text(x, y, s, size, fill, weight=600, anchor="start", spacing=0):
    return '<text x="%g" y="%g" %s font-size="%d" font-weight="%d" fill="%s" text-anchor="%s" letter-spacing="%g">%s</text>' % (
        x, y, FONT, size, weight, fill, anchor, spacing, html.escape(s))


ICON = {   # 24x24 stroke icons, drawn at (x, y) scaled to s
    "down": '<path d="M12 4v11"/><path d="M7 10.5l5 5 5-5"/><path d="M4 20h16"/>',
    "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 4v5h-5"/>',
    "check": '<path d="M4 12.5l5 5L20 6.5"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "trash": '<path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13h10l1-13"/>',
    "warn": '<path d="M12 3L2 21h20L12 3z"/><path d="M12 10v5"/><path d="M12 18v.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6l8-3z"/>',
    "left": '<path d="M15 5l-7 7 7 7"/>',
    "right": '<path d="M9 5l7 7-7 7"/>',
    "nowifi": '<path d="M2 8.5a15 15 0 0 1 20 0"/><path d="M5.5 12a10 10 0 0 1 13 0"/><path d="M9 15.5a5 5 0 0 1 6 0"/><path d="M12 19h.01"/><path d="M3 3l18 18"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
}


def icon(kind, x, y, s, colour, width=2.5):
    return '<g transform="translate(%g %g) scale(%g)" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round">%s</g>' % (
        x, y, s / 24.0, colour, width, ICON[kind])


def button(name, w, h, label, fill, tx, ic=None, stroke=None, dash=False, size=19):
    edge = ""
    if stroke:
        edge = ' stroke="%s" stroke-width="2"%s' % (stroke, ' stroke-dasharray="7 5"' if dash else "")
    body = '<rect x="1" y="1" width="%d" height="%d" rx="8" fill="%s"%s/>' % (w - 2, h - 2, fill, edge)
    tw = len(label) * size * 0.62 + (30 if ic else 0)
    x0 = (w - tw) / 2
    if ic:
        body += icon(ic, x0, h / 2 - 11, 22, tx)
        x0 += 30
    body += text(x0, h / 2 + size * 0.36, label, size, tx, 700, spacing=1.2)
    svg(name, w, h, body)


def main():
    os.makedirs(OUT, exist_ok=True)
    # the page: header, tab well and footer; everything else is live or switched
    grid = "".join('<rect x="%d" y="%d" width="11" height="11" rx="1.5" fill="%s" stroke="%s" stroke-width="2"/>' % (
        x, y, RED if (x, y) == (39, 32) else "none", RED if (x, y) == (39, 32) else INK) for x in (24, 39) for y in (17, 32))
    svg("bg.svg", 1280, 628,
        '<rect width="1280" height="628" fill="%s"/>' % BG
        + '<rect width="1280" height="60" fill="%s"/><rect y="60" width="1280" height="1" fill="%s"/>' % (PANEL, LINE)
        + grid + text(66, 39, "PLUGIN MANAGER", 24, INK, 700, spacing=3)
        + '<rect x="1036" y="15" width="1" height="30" fill="#2e3034"/>'
        + text(1056, 26, "INTERNAL", 14, MUTED, 600, spacing=1)
        + '<rect x="1056" y="37" width="200" height="5" rx="2.5" fill="#2a2b2f"/>'
        + '<rect x="24" y="64" width="580" height="56" rx="8" fill="%s" stroke="%s"/>' % (PANEL, LINE)
        + '<rect y="556" width="1280" height="72" fill="%s"/><rect y="556" width="1280" height="1" fill="%s"/>' % (PANEL, LINE)
        + '<rect x="206" y="576" width="1" height="32" fill="#2e3034"/>')
    svg("net_on.svg", 100, 24, '<circle cx="5" cy="12" r="4.5" fill="#3fbf7f"/>' + text(16, 17, "ONLINE", 15, MUTED, 600, spacing=1))
    svg("net_off.svg", 100, 24, '<circle cx="5" cy="12" r="4.5" fill="%s"/>' % RED + text(16, 17, "OFFLINE", 15, "#ff9a93", 600, spacing=1))
    # a plugin card (the list row's own picture): the thumbnail tile and the checksum shield are part of it
    for name, fill, edge in (("card_off.svg", PANEL, "#222326"), ("card_on.svg", "#1d1e21", RED)):
        svg(name, 1232, 118, '<rect x="1" y="1" width="1230" height="116" rx="10" fill="%s" stroke="%s" stroke-width="2"/>' % (fill, edge)
            + '<rect x="13" y="13" width="92" height="92" rx="8" fill="#24262a" stroke="#34363b"/>'
            + icon("shield", 816, 85, 13, "#7c8086", 2))
    # card buttons
    button("btn_install.svg", 196, 56, "INSTALL", RED, "#ffffff", "down")
    button("btn_update.svg", 196, 56, "UPDATE", AMBER, "#1a1205", "refresh")
    button("btn_installed.svg", 196, 56, "INSTALLED", "none", "#c9ccd1", "check", stroke="#3a3c41")
    button("btn_q_install.svg", 196, 56, "INSTALL · QUEUED", "none", AMBER_TX, "clock", stroke="#b88426", dash=True, size=15)
    button("btn_q_update.svg", 196, 56, "UPDATE · QUEUED", "none", AMBER_TX, "clock", stroke="#b88426", dash=True, size=15)
    button("btn_q_remove.svg", 196, 56, "REMOVE · QUEUED", "none", AMBER_TX, "clock", stroke="#b88426", dash=True, size=15)
    button("btn_disabled.svg", 196, 56, "INSTALL", "#222326", "#5c5f65", "lock", stroke="#2e3034")
    button("btn_reinstall.svg", 96, 56, "REINSTALL", "#26272b", INK, None, stroke="#3a3c41", size=14)
    button("btn_remove.svg", 96, 56, "REMOVE", "#2a1514", "#ff7a72", None, stroke="#6b2a26", size=14)
    svg("more.svg", 44, 56, "".join('<circle cx="22" cy="%d" r="2.6" fill="%s"/>' % (y, MUTED) for y in (21, 28, 35)))
    # badges (the "tested" one gets its device name as live text)
    def badge(name, w, label, colour, edge, ic=None):
        body = '<rect x="0.5" y="0.5" width="%d" height="25" rx="5" fill="none" stroke="%s"/>' % (w - 1, edge)
        x = 10
        if ic:
            body += icon(ic, 9, 6, 14, colour, 2.5)
            x = 28
        svg(name, w, 26, body + text(x, 18, label, 15, colour, 600))
    badge("badge_stable.svg", 72, "Stable", "#d6d8db", "#3a3c41")
    badge("badge_beta.svg", 64, "Beta", AMBER_TX, "#6b5220")
    badge("badge_cpu.svg", 112, "High CPU", AMBER_TX, "#6b5220", "warn")
    badge("badge_old.svg", 104, "Old install", "#c9ccd1", "#4a4c52")
    svg("badge_tested.svg", 200, 26, '<rect x="0.5" y="0.5" width="199" height="25" rx="5" fill="none" stroke="#2f5e46"/>'
        + icon("check", 9, 6, 14, GREEN, 3))
    svg("upd_badge.svg", 24, 24, '<circle cx="12" cy="12" r="12" fill="%s"/>' % AMBER)
    # tabs and filter pills (the option names are drawn on top by the renderer)
    svg("tab_off.svg", 190, 46, '<rect width="190" height="46" rx="6" fill="none"/>')
    svg("tab_on.svg", 190, 46, '<rect x="0.5" y="0.5" width="189" height="45" rx="6" fill="#2a2b2f" stroke="#4a4c52"/>')
    svg("pill_off.svg", 146, 44, '<rect x="0.5" y="0.5" width="145" height="43" rx="22" fill="none" stroke="#3a3c41"/>')
    svg("pill_on.svg", 146, 44, '<rect x="0.5" y="0.5" width="145" height="43" rx="22" fill="#3a3c41" stroke="%s"/>' % INK)
    # banners and empty states
    svg("banner.svg", 636, 36, '<rect x="0.5" y="0.5" width="635" height="35" rx="8" fill="#2a1514" stroke="#6b2a26"/>'
        + icon("warn", 12, 10, 16, "#ff7a72", 2.5))
    svg("offline.svg", 1232, 374, '<rect x="1" y="1" width="1230" height="372" rx="10" fill="none" stroke="#2e3034" stroke-dasharray="6 6"/>'
        + icon("nowifi", 596, 70, 40, DIM, 2) + text(616, 160, "Can’t reach the plugin catalog", 24, INK, 700, "middle")
        + text(616, 192, "Check the MPC’s network connection in Preferences, then refresh.", 17, DIM, 400, "middle"))
    svg("empty.svg", 1232, 374, '<rect x="1" y="1" width="1230" height="372" rx="10" fill="none" stroke="#2e3034" stroke-dasharray="6 6"/>')
    button("btn_refresh.svg", 170, 48, "REFRESH", "none", INK, "refresh", stroke=INK, size=18)
    # footer
    for side in ("left", "right"):
        for name, colour in (("arrow_%s.svg" % side, INK), ("arrow_%s_dim.svg" % side, "#4a4c52")):
            svg(name, 44, 44, '<rect x="0.5" y="0.5" width="43" height="43" rx="8" fill="none" stroke="#3a3c41"/>'
                + icon(side, 12, 12, 20, colour))
    button("updall_on.svg", 188, 52, "UPDATE ALL", "none", AMBER_TX, None, stroke=AMBER, size=18)
    button("updall_off.svg", 188, 52, "UPDATE ALL", "none", "#4a4c52", None, stroke="#3a3c41", size=18)
    button("apply_off.svg", 220, 52, "APPLY", "#2a2b2f", "#6b6e74")
    button("apply_apply.svg", 220, 52, "APPLY", RED, "#ffffff")
    button("apply_preparing.svg", 220, 52, "PREPARING…", "#2a2b2f", MUTED)
    button("apply_ready.svg", 220, 52, "RESTART & APPLY", AMBER, "#1a1205", size=17)
    button("apply_retry.svg", 220, 52, "RETRY", AMBER, "#1a1205", "refresh")
    # the bars: one picture per step (MPC switches them); step 0 of the progress bar is empty, it shows only while downloading
    for k in range(11):
        svg("disk_%02d.svg" % k, 200, 5, '<rect width="%d" height="5" rx="2.5" fill="%s"/>' % (20 * k, DIM) if k else "")
    for k in range(21):
        svg("progress_%02d.svg" % k, 360, 4, ('<rect width="360" height="4" rx="2" fill="#2a2b2f"/>'
                                              '<rect width="%d" height="4" rx="2" fill="%s"/>' % (18 * k, RED)) if k else "")


if __name__ == "__main__":
    main()
