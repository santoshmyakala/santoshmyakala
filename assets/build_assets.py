"""Generate the profile's theme-aware SVG assets (header, impact strip, capability map).

    python assets/build_assets.py      # rewrites assets/*.svg

Numbers in the impact strip are counted from the public repositories; update METRICS when they change.
"""

import re
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(__file__).resolve().parent
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(bg1="#0d1117", bg2="#151b2c", card="#161b22", border="#30363d", text="#e6edf3", muted="#9da7b3",
                 a1="#58a6ff", a2="#a371f7", a3="#3fb950", a4="#f0883e", grid="#1f2a3a"),
    "light": dict(bg1="#ffffff", bg2="#eef3fb", card="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#57606a",
                  a1="#0969da", a2="#8250df", a3="#1a7f37", a4="#bc4c00", grid="#d8e1ec"),
}

METRICS = [  # (value, label) — verifiable from the repositories
    ("15+", "years in IT"),
    ("12", "years DevOps & cloud"),
    ("13", "tested project repos"),
    ("13", "Terraform stacks tested"),
    ("191", "automated tests in CI"),
    ("100%", "images signed + SBOM"),
]

PILLARS = [
    ("Cloud foundation", "a1", ["AWS · Azure landing zones", "Hub-spoke + firewall inspection", "Terraform with offline tests", "Serverless · Kubernetes · DR"]),
    ("Secure delivery", "a3", ["Reusable CI · GitOps (Argo CD)", "SAST · SCA · IaC · DAST", "Sigstore signing · SBOM", "Kyverno admission · Falco"]),
    ("AI infrastructure", "a4", ["NVIDIA GPU Operator · MIG", "Slurm · Kueue · PyTorch DDP", "EFA / InfiniBand · Lustre", "DCGM GPU health & cost"]),
    ("MLOps & agentic AI", "a2", ["DVC · MLflow · model APIs", "Claude agents · tool use · RAG", "Guardrails · human approval", "Evals as regression gates"]),
]


def header(t):
    nodes = [(905, 70, "AWS"), (1060, 70, "Azure"), (980, 150, "K8s"), (880, 230, "GPU"), (1090, 230, "LLM")]
    edges = [(0, 2), (1, 2), (2, 3), (2, 4), (0, 1), (3, 4)]
    e = "".join(
        f'<path class="edge" style="animation-delay:{i * 0.4}s" d="M{nodes[a][0]} {nodes[a][1]} L{nodes[b][0]} {nodes[b][1]}"/>'
        for i, (a, b) in enumerate(edges)
    )
    n = "".join(
        f'<g><circle class="node" cx="{x}" cy="{y}" r="26"/><text class="nl" x="{x}" y="{y + 5}">{esc(lbl)}</text></g>'
        for x, y, lbl in nodes
    )
    chips = ["Cloud Architect", "DevOps & SRE", "Platform Engineering", "MLOps & AI Infrastructure"]
    cx, chip = 64, ""
    for c in chips:
        w = 16 + len(c) * 8.6
        chip += f'<rect x="{cx}" y="190" width="{w:.0f}" height="30" rx="15" class="chip"/><text class="ct" x="{cx + w / 2:.0f}" y="210">{esc(c)}</text>'
        cx += w + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-labelledby="t d">
<title id="t">Santoshkumar Myakala</title>
<desc id="d">Cloud Architect, DevOps and SRE, Platform Engineering, MLOps and AI Infrastructure. 15+ years; Scania, Volvo Cars, Hexagon.</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="ac" x1="0" x2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a1']}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="8s" repeatCount="indefinite"/></linearGradient>
<pattern id="g" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{t['grid']}"/></pattern>
<radialGradient id="f" cx=".8" cy=".5" r=".6"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="m"><rect width="1200" height="300" fill="url(#f)"/></mask>
<style>
.n{{font:700 50px {FONT};fill:{t['text']}}} .k{{font:600 13px {MONO};fill:{t['a1']};letter-spacing:2.5px}}
.s{{font:400 17px {FONT};fill:{t['muted']}}} .chip{{fill:{t['card']};stroke:{t['border']}}} .ct{{font:600 13px {FONT};fill:{t['text']};text-anchor:middle}}
.node{{fill:{t['card']};stroke:{t['a1']};stroke-width:1.6}} .nl{{font:600 12px {MONO};fill:{t['text']};text-anchor:middle}}
.edge{{stroke:{t['a2']};stroke-width:1.6;fill:none;stroke-dasharray:5 7;animation:flow 2.4s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-48}}}} @media (prefers-reduced-motion:reduce){{.edge{{animation:none}}}}
</style></defs>
<rect width="1200" height="300" rx="16" fill="url(#bg)"/><rect width="1200" height="300" rx="16" fill="url(#g)" mask="url(#m)"/>
{e}{n}
<text class="k" x="64" y="70">BUILD · SECURE · SCALE</text>
<text class="n" x="62" y="128">Santoshkumar Myakala</text>
<rect x="64" y="146" width="470" height="3" rx="1.5" fill="url(#ac)"/>
<text class="s" x="64" y="176">15+ years · Scania · Volvo Cars (ECARX) · Hexagon · Stockholm, Sweden</text>
{chip}
<text class="s" x="64" y="262" style="font-size:15px">Cloud platforms, secure software supply chains and GPU / AI infrastructure — as tested code.</text>
</svg>"""


def impact(t):
    w, gap = 186, 10
    tiles = ""
    for i, (value, label) in enumerate(METRICS):
        x = i * (w + gap)
        color = t[["a1", "a1", "a3", "a2", "a4", "a3"][i]]
        tiles += (f'<g class="tile" style="animation-delay:{i * 0.12:.2f}s"><rect x="{x}" y="0" width="{w}" height="104" rx="12" '
                  f'fill="{t["card"]}" stroke="{t["border"]}"/><rect x="{x}" y="0" width="{w}" height="4" rx="2" fill="{color}"/>'
                  f'<text x="{x + w / 2}" y="56" class="v" fill="{color}">{esc(value)}</text>'
                  f'<text x="{x + w / 2}" y="84" class="l">{esc(label)}</text></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1166" height="106" viewBox="0 0 1166 106" role="img" aria-label="{esc('; '.join(f'{v} {l}' for v, l in METRICS))}">
<style>.v{{font:800 34px {FONT};text-anchor:middle}} .l{{font:500 12.5px {FONT};fill:{t['muted']};text-anchor:middle}}
.tile{{animation:rise .7s ease-out both}} @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.tile{{animation:none}}}}</style>
{tiles}</svg>"""


def capability_map(t):
    w, h, gap = 270, 230, 28
    cols = ""
    for i, (title, accent, items) in enumerate(PILLARS):
        x = i * (w + gap)
        c = t[accent]
        rows = "".join(f'<circle cx="{x + 24}" cy="{96 + j * 34}" r="4" fill="{c}"/><text x="{x + 38}" y="{101 + j * 34}" class="it">{esc(it)}</text>'
                       for j, it in enumerate(items))
        cols += (f'<rect x="{x}" y="10" width="{w}" height="{h}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>'
                 f'<rect x="{x}" y="10" width="{w}" height="50" rx="14" fill="{c}" fill-opacity=".12"/>'
                 f'<text x="{x + 20}" y="42" class="h" fill="{c}">{i + 1:02d} · {esc(title)}</text>{rows}')
        if i < len(PILLARS) - 1:
            ax = x + w + 4
            cols += f'<path class="arrow" d="M{ax} 125 l{gap - 8} 0" stroke="{t["muted"]}"/><path d="M{ax + gap - 12} 120 l6 5 -6 5" fill="none" stroke="{t["muted"]}" stroke-width="1.6"/>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1164" height="250" viewBox="0 0 1164 250" role="img" aria-label="{esc('Capability map: ' + ', '.join(p[0] for p in PILLARS))}">
<style>.h{{font:700 15px {FONT}}} .it{{font:400 13.5px {FONT};fill:{t['text']}}}
.arrow{{stroke-width:1.6;stroke-dasharray:4 4;animation:flow 1.8s linear infinite}} @keyframes flow{{to{{stroke-dashoffset:-16}}}}
@media (prefers-reduced-motion:reduce){{.arrow{{animation:none}}}}</style>
{cols}</svg>"""


STACK = [  # (category, [(icon file, label)]) — only technologies used in roles or public repos
    ("Cloud", [("amazonwebservices", "AWS"), ("azure", "Azure"), ("googlecloud", "Google Cloud")]),
    ("Containers & GitOps", [("docker", "Docker"), ("kubernetes", "Kubernetes"), ("helm", "Helm"), ("argocd", "Argo CD")]),
    ("CI/CD", [("jenkins", "Jenkins"), ("gitlab", "GitLab CI"), ("githubactions", "GitHub Actions"),
               ("azuredevops", "Azure DevOps"), ("bitbucket", "Bitbucket"), ("jfrog", "JFrog")]),
    ("IaC & security", [("terraform", "Terraform"), ("ansible", "Ansible"), ("trivy", "Trivy"), ("falco", "Falco")]),
    ("Monitoring & tracing", [("prometheus", "Prometheus"), ("grafana", "Grafana"), ("opentelemetry", "OpenTelemetry"),
                              ("datadog", "Datadog"), ("powerbi-chart", "Power BI")]),
    ("Logging", [("loki", "Loki"), ("elasticsearch", "Elasticsearch"), ("logstash", "Logstash"), ("kibana", "Kibana")]),
    ("AI, GPU & ML", [("nvidia", "NVIDIA"), ("pytorch", "PyTorch"), ("mlflow", "MLflow"), ("dvc", "DVC"),
                      ("scikitlearn", "scikit-learn"), ("fastapi", "FastAPI"), ("claude", "Claude")]),
    ("Operating systems", [("linux", "Linux"), ("redhat", "Red Hat"), ("suse", "SUSE"), ("ubuntu", "Ubuntu"),
                           ("debian", "Debian"), ("kali", "Kali Linux"), ("qnx-text", "QNX")]),
    ("Languages", [("python", "Python"), ("bash", "Bash"), ("c", "C"), ("cplusplus", "C++"), ("java", "Java"),
                   ("groovy", "Groovy"), ("javascript", "JavaScript"), ("go", "Go"), ("rust", "Rust")]),
    ("Python data stack", [("pandas", "pandas"), ("numpy", "NumPy"), ("matplotlib", "Matplotlib"), ("jupyter", "Jupyter")]),
    ("Data engineering", [("hadoop", "Hadoop"), ("hive", "Hive"), ("apachespark", "Spark"), ("kafka", "Kafka"),
                          ("airflow", "Airflow"), ("nifi", "NiFi"), ("databricks", "Databricks")]),
    ("Databases & servers", [("postgresql", "PostgreSQL"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("redis", "Redis"),
                             ("dynamodb", "DynamoDB"), ("cosmosdb", "Cosmos DB"), ("nginx", "Nginx")]),
]


def _inline_icon(name: str, x: float, y: float, size: float) -> str:
    """Embed an icon SVG as a nested <svg>, prefixing its ids so several icons can share one document."""
    src = (OUT / "icons" / f"{name}.svg").read_text()
    view_box = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
    inner = re.sub(r'id="([^"]+)"', rf'id="{name}-\1"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", rf"url(#{name}-\1)", inner)
    inner = re.sub(r'href="#([^"]+)"', rf'href="#{name}-\1"', inner)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{view_box}">{inner}</svg>'


def stack(t):
    label_w, tile, gap, row_h, width = 180, 64, 22, 104, 1164
    per_line, rows, y0, k = 7, "", 0, 0
    for category, items in STACK:
        lines = -(-len(items) // per_line)
        rows += f'<text x="0" y="{y0 + 38}" class="cat">{esc(category)}</text>'
        rows += (f'<line x1="0" y1="{y0 + lines * row_h - 8}" x2="{width}" y2="{y0 + lines * row_h - 8}" '
                 f'stroke="{t["border"]}" stroke-dasharray="2 6"/>')
        for n, (icon, label) in enumerate(items):
            r, i, k = n // per_line, n % per_line, k + 1
            y = y0 + r * row_h
            x = label_w + i * (tile + gap + 48)
            rows += (f'<g class="t" style="animation-delay:{k * 0.03:.2f}s">'
                     f'<rect x="{x}" y="{y + 4}" width="{tile}" height="{tile}" rx="14" fill="#ffffff" stroke="{t["border"]}"/>'
                     + _inline_icon(icon, x + 12, y + 16, 40) +
                     f'<text x="{x + tile / 2}" y="{y + tile + 22}" class="lbl">{esc(label)}</text></g>')
        y0 += lines * row_h
    height = y0
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc('Tech stack: ' + '; '.join(c + ': ' + ', '.join(l for _, l in it) for c, it in STACK))}">
<style>.cat{{font:700 15px {FONT};fill:{t['text']}}} .lbl{{font:500 12px {FONT};fill:{t['muted']};text-anchor:middle}}
.t{{animation:pop .5s ease-out both}} @keyframes pop{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.t{{animation:none}}}}</style>
{rows}</svg>"""


for theme, t in THEMES.items():
    (OUT / f"stack-{theme}.svg").write_text(stack(t))
    (OUT / f"header-{theme}.svg").write_text(header(t))
    (OUT / f"impact-{theme}.svg").write_text(impact(t))
    (OUT / f"capabilities-{theme}.svg").write_text(capability_map(t))
print("assets written")
