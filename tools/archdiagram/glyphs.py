"""Generic service glyphs (24x24) for components that have no open brand logo.

Drawn for this project; used alongside brand logos so cloud services (API gateways, queues, functions,
firewalls…) are recognisable without reproducing trademarked service icons.
"""

S = 'fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'

GLYPHS = {
    "user": f'<circle cx="12" cy="8" r="4" {S}/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6" {S}/>',
    "users": f'<circle cx="9" cy="8" r="3.5" {S}/><path d="M2.5 20c1.2-3.4 3.6-5 6.5-5s5.3 1.6 6.5 5" {S}/>'
             f'<circle cx="17" cy="9" r="2.8" {S}/><path d="M16 14.5c2.6 0 4.6 1.4 5.5 4.5" {S}/>',
    "internet": f'<circle cx="12" cy="12" r="9" {S}/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18" {S}/>',
    "loadbalancer": f'<circle cx="12" cy="5" r="2.5" {S}/><circle cx="5" cy="19" r="2.5" {S}/><circle cx="12" cy="19" r="2.5" {S}/>'
                    f'<circle cx="19" cy="19" r="2.5" {S}/><path d="M12 7.5v9M10.5 7l-4.5 9.5M13.5 7l4.5 9.5" {S}/>',
    "firewall": f'<rect x="3" y="4" width="18" height="16" rx="1.5" {S}/><path d="M3 9.3h18M3 14.7h18M9 4v5.3M15 4v5.3'
                f'M6 9.3v5.4M12 9.3v5.4M18 9.3v5.4M9 14.7V20M15 14.7V20" {S}/>',
    "shield": f'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" {S}/><path d="M8.5 12l2.5 2.5 4.5-5" {S}/>',
    "lock": f'<rect x="5" y="10" width="14" height="11" rx="2" {S}/><path d="M8 10V7a4 4 0 018 0v3" {S}/><circle cx="12" cy="15.5" r="1.5" fill="{{c}}"/>',
    "server": f'<rect x="3" y="3.5" width="18" height="7" rx="1.5" {S}/><rect x="3" y="13.5" width="18" height="7" rx="1.5" {S}/>'
              f'<circle cx="7" cy="7" r="1" fill="{{c}}"/><circle cx="7" cy="17" r="1" fill="{{c}}"/>',
    "vm": f'<rect x="3" y="4" width="18" height="13" rx="1.5" {S}/><path d="M8 21h8M12 17v4" {S}/>',
    "container": f'<path d="M12 2.5l8.5 4.8v9.4L12 21.5l-8.5-4.8V7.3z" {S}/><path d="M3.5 7.3L12 12l8.5-4.7M12 12v9.5" {S}/>',
    "function": f'<rect x="3" y="3" width="18" height="18" rx="3" {S}/><path d="M8 18l4.2-9.5M10 6.5c1.5 0 2 .6 2.4 1.5L16 18" {S}/>',
    "queue": f'<rect x="2.5" y="7" width="19" height="10" rx="2" {S}/><path d="M7 7v10M11.5 7v10M16 7v10" {S}/>',
    "topic": f'<circle cx="5" cy="12" r="2.5" {S}/><circle cx="19" cy="5" r="2.5" {S}/><circle cx="19" cy="12" r="2.5" {S}/>'
             f'<circle cx="19" cy="19" r="2.5" {S}/><path d="M7.5 12h9M7 10.7l9.8-4.4M7 13.3l9.8 4.4" {S}/>',
    "database": f'<ellipse cx="12" cy="5.5" rx="8" ry="3" {S}/><path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13'
                f'M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" {S}/>',
    "bucket": f'<path d="M3.5 6h17l-2 14.5h-13z" {S}/><ellipse cx="12" cy="6" rx="8.5" ry="2.5" {S}/>',
    "filesystem": f'<path d="M3 6.5A1.5 1.5 0 014.5 5H10l2 2h7.5A1.5 1.5 0 0121 8.5v10a1.5 1.5 0 01-1.5 1.5h-15A1.5 1.5 0 013 18.5z" {S}/>'
                  f'<path d="M7 13h10M7 16.5h6" {S}/>',
    "cache": f'<path d="M13 2.5L5 13.5h6l-1 8 8-11h-6z" {S}/>',
    "api": f'<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14" {S}/>',
    "gateway": f'<rect x="3" y="4" width="18" height="16" rx="2" {S}/><path d="M7 12h10M13.5 8.5L17 12l-3.5 3.5" {S}/>',
    "dns": f'<circle cx="12" cy="12" r="9" {S}/><path d="M7.5 9.5h9M7.5 14.5h9" {S}/>',
    "cdn": f'<circle cx="12" cy="12" r="3" {S}/><circle cx="4.5" cy="5" r="2" {S}/><circle cx="19.5" cy="5" r="2" {S}/>'
           f'<circle cx="4.5" cy="19" r="2" {S}/><circle cx="19.5" cy="19" r="2" {S}/><path d="M6 6.4l3.8 3.6M18 6.4l-3.8 3.6M6 17.6l3.8-3.6M18 17.6l-3.8-3.6" {S}/>',
    "git": f'<circle cx="6" cy="6" r="2.5" {S}/><circle cx="6" cy="18" r="2.5" {S}/><circle cx="18" cy="9" r="2.5" {S}/>'
           f'<path d="M6 8.5v7M15.6 9.6C11 10.5 7 12 6 15.5" {S}/>',
    "pipeline": f'<circle cx="4.5" cy="12" r="2.5" {S}/><circle cx="12" cy="12" r="2.5" {S}/><circle cx="19.5" cy="12" r="2.5" {S}/>'
                f'<path d="M7 12h2.5M14.5 12H17" {S}/>',
    "gear": f'<circle cx="12" cy="12" r="3.2" {S}/><path d="M12 2.8v2.6M12 18.6v2.6M21.2 12h-2.6M5.4 12H2.8M18.5 5.5l-1.8 1.8'
            f'M7.3 16.7l-1.8 1.8M18.5 18.5l-1.8-1.8M7.3 7.3L5.5 5.5" {S}/><circle cx="12" cy="12" r="6.5" {S}/>',
    "registry": f'<rect x="3" y="14" width="8" height="6" rx="1" {S}/><rect x="13" y="14" width="8" height="6" rx="1" {S}/>'
                f'<rect x="8" y="5" width="8" height="6" rx="1" {S}/>',
    "key": f'<circle cx="7.5" cy="14.5" r="4" {S}/><path d="M10.5 11.5L20 2.5M16 6.5l2.5 2.5M13.5 9l2 2" {S}/>',
    "certificate": f'<rect x="3" y="4" width="18" height="13" rx="1.5" {S}/><path d="M7 8.5h10M7 12h6" {S}/><circle cx="17" cy="16" r="2.5" {S}/>'
                   f'<path d="M15.5 18l-.8 3.5 2.3-1.2 2.3 1.2-.8-3.5" {S}/>',
    "signature": f'<path d="M3 17c2.5-6 4.5-9 6-9 2 0-1.5 9 1 9 1.5 0 2.5-4 4-4 1 0 .5 3 2 3 1 0 2-1 3-2" {S}/><path d="M3 21h18" {S}/>',
    "sbom": f'<path d="M6 3h9l4 4v14H6z" {S}/><path d="M15 3v4h4M9 11h7M9 14.5h7M9 18h4" {S}/>',
    "doc": f'<path d="M6 3h9l4 4v14H6z" {S}/><path d="M15 3v4h4M9 12h7M9 16h5" {S}/>',
    "search": f'<circle cx="10.5" cy="10.5" r="6.5" {S}/><path d="M15.5 15.5L21 21" {S}/>',
    "chart": f'<path d="M3 21h18" {S}/><rect x="5" y="12" width="3" height="7" rx="1" {S}/><rect x="10.5" y="7" width="3" height="12" rx="1" {S}/>'
             f'<rect x="16" y="3.5" width="3" height="15.5" rx="1" {S}/>',
    "logs": f'<rect x="3.5" y="3.5" width="17" height="17" rx="2" {S}/><path d="M7 8h10M7 12h10M7 16h6" {S}/>',
    "alert": f'<path d="M12 3a6 6 0 016 6v4l2 3H4l2-3V9a6 6 0 016-6z" {S}/><path d="M10 19a2 2 0 004 0" {S}/>',
    "eye": f'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" {S}/><circle cx="12" cy="12" r="3" {S}/>',
    "gpu": f'<rect x="5" y="5" width="14" height="14" rx="2" {S}/><rect x="9" y="9" width="6" height="6" {S}/>'
           f'<path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3" {S}/>',
    "model": f'<circle cx="12" cy="5" r="2.2" {S}/><circle cx="5" cy="12" r="2.2" {S}/><circle cx="19" cy="12" r="2.2" {S}/>'
             f'<circle cx="12" cy="19" r="2.2" {S}/><path d="M10.4 6.6L6.6 10.4M13.6 6.6l3.8 3.8M6.6 13.6l3.8 3.8M17.4 13.6l-3.8 3.8M7.2 12h9.6" {S}/>',
    "agent": f'<rect x="4" y="7" width="16" height="12" rx="3" {S}/><path d="M12 7V4M9.5 4h5" {S}/><circle cx="9" cy="13" r="1.4" fill="{{c}}"/>'
             f'<circle cx="15" cy="13" r="1.4" fill="{{c}}"/><path d="M2 12v3M22 12v3" {S}/>',
    "terminal": f'<rect x="2.5" y="4" width="19" height="16" rx="2" {S}/><path d="M6.5 9l3 3-3 3M12 15h5" {S}/>',
    "switch": f'<rect x="2.5" y="8" width="19" height="8" rx="1.5" {S}/><path d="M6 12h.01M9 12h.01M12 12h.01M15 12h.01M18 12h.01" {S}/>',
    "cluster": f'<circle cx="12" cy="12" r="2.5" {S}/><circle cx="5" cy="6" r="2" {S}/><circle cx="19" cy="6" r="2" {S}/>'
               f'<circle cx="5" cy="18" r="2" {S}/><circle cx="19" cy="18" r="2" {S}/><path d="M6.6 7.3l3.4 3M17.4 7.3l-3.4 3M6.6 16.7l3.4-3M17.4 16.7l-3.4-3" {S}/>',
    "scheduler": f'<rect x="3" y="4.5" width="18" height="16" rx="2" {S}/><path d="M3 9.5h18M8 2.5v4M16 2.5v4" {S}/><path d="M8 13.5h3v3H8z" {S}/>',
    "data": f'<path d="M4 6h16M4 12h16M4 18h16" {S}/><circle cx="8" cy="6" r="1.6" fill="{{c}}"/><circle cx="15" cy="12" r="1.6" fill="{{c}}"/>'
            f'<circle cx="10" cy="18" r="1.6" fill="{{c}}"/>',
    "check": f'<circle cx="12" cy="12" r="9" {S}/><path d="M7.5 12.5l3 3 6-6.5" {S}/>',
    "deny": f'<circle cx="12" cy="12" r="9" {S}/><path d="M5.7 5.7l12.6 12.6" {S}/>',
    "bug": f'<rect x="7" y="7" width="10" height="13" rx="5" {S}/><path d="M12 7v13M3 11h4M17 11h4M3 17h4M17 17h4M9 4l1.5 3M15 4l-1.5 3" {S}/>',
    "region": f'<path d="M12 21s-7-6-7-11.5a7 7 0 0114 0C19 15 12 21 12 21z" {S}/><circle cx="12" cy="9.5" r="2.5" {S}/>',
    "backup": f'<path d="M4 12a8 8 0 1 1 2.3 5.7" {S}/><path d="M4 18v-5h5" {S}/><path d="M12 8v4l3 2" {S}/>',
}


def glyph(name: str, color: str) -> str:
    body = GLYPHS[name].replace("{c}", color).replace("{{c}}", color)
    return f'<svg viewBox="0 0 24 24">{body}</svg>'
