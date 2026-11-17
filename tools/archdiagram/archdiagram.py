#!/usr/bin/env python3
"""Render a YAML architecture spec into animated, theme-aware SVG diagrams.

    python archdiagram.py spec.yaml [more.yaml ...] [--icons DIR]

Each spec produces <out>-dark.svg and <out>-light.svg next to it (or at `out:`). The SVGs are
self-contained: brand logos are inlined from the icon directory and generic components use
the glyphs in glyphs.py, so they render inside a GitHub README <img>/<picture> with no external
requests. Packets move along each connection with SMIL <animateMotion>; viewers who ask for
reduced motion get a static diagram.

Spec (coordinates are grid units unless noted):

    title: AWS three-tier platform
    subtitle: Optional second line
    grid: {dx: 180, dy: 150}          # cell size in px
    groups:
      - {id: vpc, label: VPC 10.0.0.0/16, icon: amazonwebservices, color: orange, box: [1, 0, 4, 2]}
    nodes:
      - {id: alb, label: Public ALB, sub: TLS 1.3 · WAF, icon: loadbalancer, at: [1, 1], color: blue,
         badge: "x3", stack: true, pulse: true}
    edges:
      - {from: users, to: alb, label: HTTPS, kind: data, route: hv, via: [[1.5, 0]], at: 0.5}

Edge kinds: data (blue), secure (green, encrypted), control (purple, dashed), async (amber),
deny (red, blocked before the target), metrics (teal). Routes: straight, hv, vh, hvh, vhv.
"""
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from xml.sax.saxutils import escape

import yaml

from glyphs import GLYPHS, glyph

HERE = Path(__file__).resolve().parent
DEFAULT_ICONS = HERE.parent.parent / "assets" / "icons"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#11161f", card="#161b22", border="#30363d", text="#e6edf3",
                 muted="#9da7b3", tile="#ffffff", pill="#0d1117", grid="#1b2230"),
    "light": dict(bg="#ffffff", panel="#f8fafc", card="#ffffff", border="#d0d7de", text="#1f2328",
                  muted="#57606a", tile="#ffffff", pill="#ffffff", grid="#eef1f5"),
}
# accent colours: (dark-theme, light-theme)
COLORS = {
    "blue": ("#58a6ff", "#0969da"), "green": ("#3fb950", "#1a7f37"), "purple": ("#bc8cff", "#8250df"),
    "orange": ("#ff9a3c", "#d4600b"), "red": ("#ff6b6b", "#cf222e"), "teal": ("#39d0c8", "#0e8a83"),
    "amber": ("#e3b341", "#9a6700"), "pink": ("#ff7ab8", "#bf3989"), "gray": ("#8b949e", "#6e7781"),
    "azure": ("#3ea6ff", "#0063b1"), "nvidia": ("#86d42a", "#4b8a00"),
}
KINDS = {
    "data": ("blue", "Request / data flow", False),
    "secure": ("green", "Encrypted / authenticated", False),
    "control": ("purple", "Control plane / deploy", True),
    "async": ("amber", "Async / events", False),
    "metrics": ("teal", "Telemetry", True),
    "deny": ("red", "Blocked by policy", False),
}


def esc(s) -> str:
    return escape(str(s), {'"': "&quot;"})


class Diagram:
    def __init__(self, spec: dict, icons: Path):
        self.spec, self.icons = spec, icons
        for item in [*spec.get("groups", []), *spec.get("nodes", []), *spec.get("edges", [])]:
            for key in ("label", "sub"):
                if key in item:
                    item[key] = str(item[key])
        g = spec.get("grid", {})
        self.dx, self.dy = g.get("dx", 180), g.get("dy", 150)
        self.x0, self.y0 = g.get("x0", 110), g.get("y0", 150 if spec.get("subtitle") else 130)
        self.nw, self.nh = spec.get("node", {}).get("w", 136), spec.get("node", {}).get("h", 100)
        self.uid = 0
        self.rects: dict[str, tuple[float, float, float, float]] = {}  # id -> cx, cy, hw, hh
        for gr in spec.get("groups", []):
            x, y, w, h = self.group_box(gr)
            self.rects[gr["id"]] = (x + w / 2, y + h / 2, w / 2, h / 2)
        for n in spec.get("nodes", []):
            cx, cy = self.pt(n["at"])
            icons = n["icon"] if isinstance(n.get("icon"), list) else [n.get("icon")]
            auto = max(len(n["label"]) * 7.9 + 22, len(n.get("sub", "")) * 6.1 + 20, len(icons) * 46 + 14)
            w, h = n.get("w", max(self.nw, auto)), n.get("h", self.nh)
            self.rects[n["id"]] = (cx, cy, w / 2, h / 2)
        # warn when cards in the same row/column leave too little room for an arrow and a packet
        items = [(k, v) for k, v in self.rects.items() if k in {n["id"] for n in spec.get("nodes", [])}]
        for i, (a, ra) in enumerate(items):
            for b, rb in items[i + 1:]:
                if abs(ra[1] - rb[1]) < 1 and abs(ra[0] - rb[0]) - ra[2] - rb[2] < 44:
                    print(f"  ! tight horizontal gap {a} <-> {b}: {abs(ra[0] - rb[0]) - ra[2] - rb[2]:.0f}px")
                if abs(ra[0] - rb[0]) < 1 and abs(ra[1] - rb[1]) - ra[3] - rb[3] < 36:
                    print(f"  ! tight vertical gap {a} <-> {b}: {abs(ra[1] - rb[1]) - ra[3] - rb[3]:.0f}px")

    # ---------- geometry ----------
    def pt(self, p):
        return self.x0 + p[0] * self.dx, self.y0 + p[1] * self.dy

    def group_box(self, gr):
        c0, r0, c1, r1 = gr["box"]
        pad = gr.get("pad", 0)
        padx, pady_top, pady_bot = self.nw / 2 + 22 + pad, self.nh / 2 + 50 + pad + gr.get("pad_top", 0), self.nh / 2 + 18 + pad
        x0, y0 = self.pt((c0, r0))
        x1, y1 = self.pt((c1, r1))
        return x0 - padx, y0 - pady_top, (x1 - x0) + 2 * padx, (y1 - y0) + pady_top + pady_bot

    @staticmethod
    def clip(rect, toward):
        cx, cy, hw, hh = rect
        dx, dy = toward[0] - cx, toward[1] - cy
        if dx == 0 and dy == 0:
            return cx, cy
        t = min(hw / abs(dx) if dx else math.inf, hh / abs(dy) if dy else math.inf)
        return (cx + dx * t, cy + dy * t) if t < 1 else (cx, cy)

    def endpoint(self, ref):
        if isinstance(ref, (list, tuple)):
            x, y = self.pt(ref)
            return (x, y, 0, 0)
        return self.rects[ref]

    def route(self, e):
        a, b = self.endpoint(e["from"]), self.endpoint(e["to"])
        off = e.get("offset", [0, 0])  # shift the whole edge in px (for parallel edges)
        a = (a[0] + off[0], a[1] + off[1], a[2], a[3])
        b = (b[0] + off[0], b[1] + off[1], b[2], b[3])
        mids = [self.pt(v) for v in e.get("via", [])]
        r = e.get("route", "straight")
        if not mids:
            if r == "hv":
                mids = [(b[0], a[1])]
            elif r == "vh":
                mids = [(a[0], b[1])]
            elif r == "hvh":
                mx = (a[0] + b[0]) / 2
                mids = [(mx, a[1]), (mx, b[1])]
            elif r == "vhv":
                my = (a[1] + b[1]) / 2
                mids = [(a[0], my), (b[0], my)]
        start = self.clip(a, mids[0] if mids else b[:2])
        end = self.clip(b, mids[-1] if mids else a[:2])
        pad = 6
        ex, ey = end[0] - (mids[-1][0] if mids else start[0]), end[1] - (mids[-1][1] if mids else start[1])
        ln = math.hypot(ex, ey) or 1
        end = (end[0] - ex / ln * pad, end[1] - ey / ln * pad)
        pts = [start, *mids, end]
        return [p for i, p in enumerate(pts) if i == 0 or math.dist(p, pts[i - 1]) > 0.5]

    @staticmethod
    def path_d(pts, radius=12):
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(1, len(pts) - 1):
            p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
            l1, l2 = math.dist(p0, p1), math.dist(p1, p2)
            r = min(radius, l1 / 2, l2 / 2)
            a = (p1[0] + (p0[0] - p1[0]) * r / l1, p1[1] + (p0[1] - p1[1]) * r / l1)
            b = (p1[0] + (p2[0] - p1[0]) * r / l2, p1[1] + (p2[1] - p1[1]) * r / l2)
            d += f" L{a[0]:.1f},{a[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {b[0]:.1f},{b[1]:.1f}"
        return d + f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"

    @staticmethod
    def along(pts, frac):
        segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        total, target = sum(segs), sum(segs) * frac
        for i, s in enumerate(segs):
            if target <= s or i == len(segs) - 1:
                t = target / s if s else 0
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t), total
            target -= s
        return pts[-1], total

    # ---------- icons ----------
    def icon(self, name, x, y, size, color):
        if name in GLYPHS:
            body = glyph(name, color)
            return body.replace("<svg ", f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" ', 1)
        src = (self.icons / f"{name}.svg").read_text()
        self.uid += 1
        p = f"i{self.uid}"
        vb = re.search(r'viewBox="([^"]+)"', src).group(1)
        inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
        inner = re.sub(r'id="([^"]+)"', rf'id="{p}-\1"', inner)
        inner = re.sub(r"url\(#([^)]+)\)", rf"url(#{p}-\1)", inner)
        inner = re.sub(r'href="#([^"]+)"', rf'href="#{p}-\1"', inner)
        return f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" viewBox="{vb}">{inner}</svg>'

    # ---------- render ----------
    def render(self, theme: str) -> str:
        t = THEMES[theme]
        ti = 0 if theme == "dark" else 1
        col = lambda c: COLORS.get(c, (c, c))[ti]  # noqa: E731
        self.uid = 0
        out_groups, out_edges, out_packets, out_nodes, out_labels = [], [], [], [], []
        xs, ys = [], []

        for gr in self.spec.get("groups", []):
            x, y, w, h = self.group_box(gr)
            c = col(gr.get("color", "gray"))
            xs += [x, x + w]
            ys += [y, y + h]
            dash = "" if gr.get("solid") else ' stroke-dasharray="6 5"'
            label = esc(gr["label"])
            out_groups.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" fill="{c}" fill-opacity="0.06" '
                f'stroke="{c}" stroke-opacity="0.75" stroke-width="1.4"{dash}/>')
            lx = x + 14
            if gr.get("icon"):
                out_groups.append(f'<rect x="{lx:.1f}" y="{y + 10:.1f}" width="24" height="24" rx="6" fill="{t["tile"]}" stroke="{c}" stroke-opacity=".5"/>')
                out_groups.append(self.icon(gr["icon"], lx + 3, y + 13, 18, c))
                lx += 32
            out_groups.append(f'<text x="{lx:.1f}" y="{y + 27:.1f}" class="gl" fill="{c}">{label}</text>')
            if gr.get("sub") and (lx - x) + len(gr["label"]) * 7.6 + 10 + len(gr["sub"]) * 6.4 < w - 10:
                out_groups.append(f'<text x="{lx + len(gr["label"]) * 7.6 + 16:.1f}" y="{y + 27:.1f}" class="gs">{esc(gr["sub"])}</text>')

        used = []
        for i, e in enumerate(self.spec.get("edges", [])):
            kind = e.get("kind", "data")
            cname, _, dashed = KINDS[kind]
            if kind not in used:
                used.append(kind)
            c = col(e.get("color", cname))
            pts = self.route(e)
            d = self.path_d(pts)
            pid = f"p{i}"
            xs += [p[0] for p in pts]
            ys += [p[1] for p in pts]
            dash = ' stroke-dasharray="5 6"' if dashed else ""
            marker = "" if kind == "deny" else f' marker-end="url(#a-{kind})"'
            both = f' marker-start="url(#s-{kind})"' if e.get("both") else ""
            out_edges.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{c}" stroke-opacity="0.85" stroke-width="2"{dash}{marker}{both}/>')
            if not dashed:
                out_edges.append(f'<path d="{d}" class="flow" fill="none" stroke="{c}" stroke-width="2" stroke-opacity=".9"/>')
            _, length = self.along(pts, 0.5)
            dur = max(1.6, length / e.get("speed", 110))
            n = e.get("packets", 2 if length > 160 else 1)
            shape = e.get("packet", "lock" if kind == "secure" else "dot")
            for k in range(n):
                begin = f"-{dur * k / n:.2f}s"
                if kind == "deny":
                    motion = (f'<animateMotion dur="{dur:.2f}s" begin="{begin}" repeatCount="indefinite" keyPoints="0;0.82;0.82" '
                              f'keyTimes="0;0.8;1" calcMode="linear"><mpath href="#{pid}" xlink:href="#{pid}"/></animateMotion>'
                              f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.8;1" dur="{dur:.2f}s" begin="{begin}" repeatCount="indefinite"/>')
                else:
                    motion = (f'<animateMotion dur="{dur:.2f}s" begin="{begin}" repeatCount="indefinite" rotate="0">'
                              f'<mpath href="#{pid}" xlink:href="#{pid}"/></animateMotion>')
                if shape == "lock":
                    body = (f'<rect x="-6" y="-3" width="12" height="9" rx="2" fill="{c}"/>'
                            f'<path d="M-3.5,-3 v-2.5 a3.5,3.5 0 0 1 7,0 v2.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
                            f'<circle cx="0" cy="1.5" r="1.3" fill="{t["bg"]}"/>')
                elif shape == "doc":
                    body = (f'<rect x="-5" y="-6.5" width="10" height="13" rx="1.5" fill="{c}"/>'
                            f'<path d="M-2.5,-2 h5 M-2.5,1 h5 M-2.5,4 h3" stroke="{t["bg"]}" stroke-width="1.2"/>')
                elif shape == "box":
                    body = (f'<path d="M0,-7 L6.5,-3.5 L6.5,3.5 L0,7 L-6.5,3.5 L-6.5,-3.5 Z" fill="{c}"/>'
                            f'<path d="M-6.5,-3.5 L0,0 L6.5,-3.5 M0,0 V7" fill="none" stroke="{t["bg"]}" stroke-width="1"/>')
                elif shape == "db":
                    body = (f'<path d="M-6,-5 v10 a6,2.5 0 0 0 12,0 v-10" fill="{c}"/><ellipse cx="0" cy="-5" rx="6" ry="2.5" fill="{c}" '
                            f'stroke="{t["bg"]}" stroke-width="1"/>')
                else:
                    body = f'<circle r="7" fill="{c}" opacity=".25"/><circle r="4" fill="{c}"/>'
                out_packets.append(f'<g class="pk">{body}{motion}</g>')
            if kind == "deny":
                (bx, by), _ = self.along(pts, 0.88)
                out_packets.append(f'<g transform="translate({bx:.1f},{by:.1f})"><circle r="10" fill="{t["bg"]}" stroke="{c}" stroke-width="2"/>'
                                   f'<path d="M-4,-4 L4,4 M4,-4 L-4,4" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/></g>')
            if e.get("label"):
                (lx, ly), _ = self.along(pts, e.get("at", 0.5))
                lx += e.get("ldx", 0)
                ly += e.get("ldy", 0)
                lines = str(e["label"]).split("\n")
                w = max(len(s) for s in lines) * 6.3 + 16
                h = 16 * len(lines) + 4
                txt = "".join(f'<tspan x="{lx:.1f}" dy="{0 if j == 0 else 14}">{esc(s)}</tspan>' for j, s in enumerate(lines))
                out_labels.append(f'<rect x="{lx - w / 2:.1f}" y="{ly - h / 2:.1f}" width="{w:.1f}" height="{h}" rx="{min(h / 2, 9)}" '
                                  f'fill="{t["pill"]}" stroke="{c}" stroke-opacity=".7"/>'
                                  f'<text x="{lx:.1f}" y="{ly - h / 2 + 14.5:.1f}" class="el" fill="{c}">{txt}</text>')

        for n in self.spec.get("nodes", []):
            cx, cy, hw, hh = self.rects[n["id"]]
            w, h = hw * 2, hh * 2
            x, y = cx - hw, cy - hh
            c = col(n.get("color", "blue"))
            xs += [x, x + w]
            ys += [y, y + h]
            g = []
            if n.get("stack"):
                for s in (8, 4):
                    g.append(f'<rect x="{x + s:.1f}" y="{y - s:.1f}" width="{w:.1f}" height="{h:.1f}" rx="14" fill="{t["card"]}" stroke="{c}" stroke-opacity=".35"/>')
            if n.get("pulse"):
                g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="14" fill="none" stroke="{c}" stroke-width="2" class="pulse"/>')
            g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="14" fill="{t["card"]}" stroke="{c}" stroke-opacity=".8" stroke-width="1.3"/>')
            g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="4" rx="2" fill="{c}" opacity=".9"/>')
            icons = n["icon"] if isinstance(n.get("icon"), list) else [n.get("icon", "server")]
            tile, gap = 40, 6
            tw = len(icons) * tile + (len(icons) - 1) * gap
            ix = cx - tw / 2
            iy = y + 10
            for name in icons:
                g.append(f'<rect x="{ix:.1f}" y="{iy:.1f}" width="{tile}" height="{tile}" rx="10" fill="{t["tile"]}" stroke="{t["border"]}"/>')
                g.append(self.icon(name, ix + 7, iy + 7, tile - 14, c if name in GLYPHS else c))
                ix += tile + gap
            g.append(f'<text x="{cx:.1f}" y="{y + 68:.1f}" class="nl">{esc(n["label"])}</text>')
            if n.get("sub"):
                g.append(f'<text x="{cx:.1f}" y="{y + 85:.1f}" class="ns">{esc(n["sub"])}</text>')
            if n.get("badge"):
                bw = len(str(n["badge"])) * 7 + 14
                g.append(f'<rect x="{x + w - bw + 6:.1f}" y="{y - 9:.1f}" width="{bw}" height="18" rx="9" fill="{c}"/>'
                         f'<text x="{x + w - bw / 2 + 6:.1f}" y="{y + 4:.1f}" class="bd" fill="{t["bg"]}">{esc(n["badge"])}</text>')
            out_nodes.append(f'<g class="nd">{"".join(g)}</g>')

        margin = 28
        title_h = 74 if self.spec.get("subtitle") else 56
        legend_h = 44
        min_x, max_x = min(xs) - margin, max(xs) + margin
        min_y, max_y = min(ys) - margin, max(ys) + margin
        width = max(max_x - min_x, self.spec.get("min_width", 760))
        top = min_y - title_h
        height = (max_y - top) + legend_h

        legend, lx = [], min_x + 20
        ly = max_y + 16
        for kind in used:
            cname, text, dashed = KINDS[kind]
            c = col(cname)
            dash = ' stroke-dasharray="5 6"' if dashed else ""
            legend.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 28}" y2="{ly}" stroke="{c}" stroke-width="2"{dash}/>'
                          f'<circle cx="{lx + 14}" cy="{ly}" r="4" fill="{c}"/>'
                          f'<text x="{lx + 36}" y="{ly + 4}" class="lg">{esc(text)}</text>')
            lx += 36 + len(text) * 6.6 + 26

        markers = "".join(
            f'<marker id="a-{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{col(v[0])}"/></marker>'
            f'<marker id="s-{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{col(v[0])}"/></marker>' for k, v in KINDS.items())

        title = esc(self.spec["title"])
        sub = self.spec.get("subtitle", "")
        aria = esc(self.spec.get("alt", self.spec["title"] + (". " + sub if sub else "")))
        tx, ty = min_x + 22, top + 34
        css = f"""
.tt{{font:700 19px {FONT};fill:{t['text']}}} .st{{font:400 13px {FONT};fill:{t['muted']}}}
.gl{{font:700 13px {FONT}}} .gs{{font:400 12px {FONT};fill:{t['muted']}}}
.nl{{font:600 13px {FONT};fill:{t['text']};text-anchor:middle}} .ns{{font:400 11px {FONT};fill:{t['muted']};text-anchor:middle}}
.el{{font:600 11px {FONT};text-anchor:middle}} .lg{{font:400 12px {FONT};fill:{t['muted']}}} .bd{{font:700 11px {FONT};text-anchor:middle}}
.flow{{stroke-dasharray:3 14;animation:dash 1.1s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:-17}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.8}}100%{{transform:scale(1.12,1.18);opacity:0}}}}
.nd{{animation:pop .6s ease-out both}} @keyframes pop{{from{{opacity:0}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.pk,.pulse{{display:none}}.flow,.nd{{animation:none}}}}
"""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width:.0f}" height="{height:.0f}" '
                f'viewBox="{min_x:.1f} {top:.1f} {width:.1f} {height:.1f}" role="img" aria-label="{aria}">\n'
                f'<title>{title}</title>\n<style>{css}</style>\n<defs>{markers}</defs>\n'
                f'<rect x="{min_x:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" rx="18" fill="{t["panel"]}" stroke="{t["border"]}"/>\n'
                f'<text x="{tx:.1f}" y="{ty:.1f}" class="tt">{title}</text>\n'
                + (f'<text x="{tx:.1f}" y="{ty + 22:.1f}" class="st">{esc(sub)}</text>\n' if sub else "")
                + "\n".join(out_groups) + "\n" + "\n".join(out_edges) + "\n" + "\n".join(out_nodes) + "\n"
                + "\n".join(out_packets) + "\n" + "\n".join(out_labels) + "\n" + "".join(legend) + "\n</svg>\n")


def build(spec_path: Path, icons: Path) -> list[Path]:
    specs = yaml.safe_load(spec_path.read_text())
    specs = specs if isinstance(specs, list) else [specs]
    written = []
    for spec in specs:
        out = spec_path.parent / spec.get("out", spec_path.stem)
        d = Diagram(spec, icons)
        for theme in ("dark", "light"):
            p = out.parent / f"{out.name}-{theme}.svg"
            p.write_text(d.render(theme))
            written.append(p)
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("specs", nargs="+", type=Path)
    ap.add_argument("--icons", type=Path, default=DEFAULT_ICONS)
    a = ap.parse_args()
    for s in a.specs:
        for p in build(s, a.icons):
            print(p)
