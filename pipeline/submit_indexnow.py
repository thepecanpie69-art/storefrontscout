#!/usr/bin/env python3
"""Submit docs/sitemap.xml URLs to IndexNow (Bing/Yandex/etc.). Free; no account."""
import json, os, re, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "thepecanpie69-art.github.io"
KEY = "1e71b31a94e0970021eecdf79bf1b16b"
KEY_LOC = f"https://{HOST}/storefrontscout/{KEY}.txt"
BASE = f"https://{HOST}/storefrontscout/"
def urls_from_sitemap():
    xml = open(os.path.join(ROOT, "docs", "sitemap.xml")).read()
    return re.findall(r"<loc>(.*?)</loc>", xml)
def main():
    urls = urls_from_sitemap()
    if len(sys.argv) > 1:
        urls = [u if u.startswith("http") else BASE + u.lstrip("/") for u in sys.argv[1:]]
    # IndexNow caps batches; sitemap is ~30 URLs so one shot is fine.
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOC, "urlList": urls}).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            print("IndexNow", resp.status, len(urls), "urls")
    except urllib.error.HTTPError as e:
        print("IndexNow", e.code, e.read()[:200], file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    main()
