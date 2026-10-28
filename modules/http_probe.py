import re
import requests

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]

def probe_host(host, timeout=5):
    for scheme in ("https", "http"):
        url = f"{scheme}://{host}"
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue
        title = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.I | re.S)
        return {
            "host": host,
            "url": r.url,
            "status": r.status_code,
            "server": r.headers.get("Server", ""),
            "title": title.group(1).strip()[:80] if title else "",
            "missing_headers": [h for h in SECURITY_HEADERS if h not in r.headers],
        }
    return None

def probe_hosts(hosts):
    results = []
    for host in hosts:
        if not host:
            continue
        info = probe_host(host)
        if info:
            results.append(info)
    return results
