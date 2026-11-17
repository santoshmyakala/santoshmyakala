# archdiagram

Generates the animated architecture, pipeline and workflow diagrams used across my repositories, from a small YAML spec.

- **Icon-based.** Real brand logos (Devicon, MIT; Simple Icons, CC0) for products, and drawn glyphs for generic components such as load balancers, queues, functions, firewalls and GPUs. No cloud-vendor service icons are reproduced.
- **Animated flows.** Packets travel along each connection with SMIL `animateMotion`. Each kind has its own look: data, encrypted/authenticated (padlock packets), async/events, telemetry, control plane, and *blocked by policy* (the packet stops at a ⊗).
- **GitHub-ready.** Each spec renders `-dark.svg` and `-light.svg` for a `<picture>` element. The SVGs are self-contained, with no external requests. Viewers who ask for reduced motion get a static diagram.

```bash
pip install pyyaml
```

```bash
python tools/archdiagram/archdiagram.py path/to/diagrams.yaml
```

```yaml
- out: architecture                 # writes architecture-dark.svg / architecture-light.svg
  title: AWS three-tier platform
  subtitle: optional second line
  grid: {dx: 220, dy: 150}          # cell size in px; positions below are in grid units
  groups:                           # dashed boundaries: VPCs, subnets, clusters, pipelines
    - {id: vpc, label: VPC 10.20.0.0/16, icon: amazonwebservices, color: orange, box: [1, 0, 4, 2]}
  nodes:
    - {id: alb, label: Public ALB, sub: TLS 1.3, icon: loadbalancer, at: [1, 0.5], color: blue, pulse: true}
    - {id: web, label: Nginx tier, icon: nginx, at: [2, 0.5], badge: "×2", stack: true}
  edges:
    - {from: alb, to: web, label: ":80", kind: data}
    - {from: ops, to: vpn, kind: secure}
    - {from: users, to: db, kind: deny, via: [[0, -0.6], [4, -0.6]]}
```

| Field | Values |
|---|---|
| `icon` | a file name in `assets/icons/`, a glyph from `glyphs.py`, or a list of either |
| `color` | `blue` `green` `purple` `orange` `red` `teal` `amber` `pink` `gray` `azure` `nvidia` |
| `kind` | `data` `secure` `async` `metrics` `control` `deny` |
| `route` | `straight` (default) `hv` `vh` `hvh` `vhv`, or explicit `via` points |
| `packet` | `dot` `lock` `doc` `box` `db` |
| node extras | `badge`, `stack` (replicas), `pulse` (highlight), `w`/`h` |
| edge extras | `label`, `at` (label position 0–1), `both`, `offset`, `speed`, `packets` |

The generator warns when neighbouring cards leave too little room for an arrow and a moving packet.
