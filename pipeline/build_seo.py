#!/usr/bin/env python3
"""Build SEO city/county pages, audience pages, sitemap, robots into docs/. Public data only: business name, city, permit date."""
import sys, os, json, html, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_feed as bf
BASE = "https://thepecanpie69-art.github.io/storefrontscout/"
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
L9, L19, L29 = "https://buy.stripe.com/28E4gzfzF7mpc6Qd6ogEg00", "https://buy.stripe.com/7sYbJ1gDJ225daU9UcgEg01", "https://buy.stripe.com/14AfZhcntcGJ7QA5DWgEg02"
CITIES = ["Dallas", "Fort Worth", "Plano", "Frisco", "McKinney", "Denton", "Arlington", "Irving", "Garland", "Carrollton", "Allen", "Lewisville", "Richardson", "Mansfield", "Grand Prairie", "Flower Mound", "Keller", "Southlake"]
COUNTIES = ["Dallas", "Tarrant", "Collin", "Denton"]
CSS = "body{font-family:system-ui,sans-serif;max-width:860px;margin:0 auto;padding:20px;line-height:1.5;color:#222}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:6px;text-align:left;font-size:14px}.b{display:inline-block;background:#0a7;color:#fff;padding:10px 14px;border-radius:6px;text-decoration:none;margin:4px 6px 4px 0}nav a{margin-right:10px}footer{margin-top:40px;font-size:13px;color:#555;border-top:1px solid #ddd;padding-top:10px}"
def slug(s): return s.lower().replace(" ", "-")
FOOT = ('<footer><p>StorefrontScout. Data: Texas Comptroller public sales tax permit records. Contact, cancel or unsubscribe: '
        '<a href="mailto:storefrontscout@mail.grokbot.com">storefrontscout@mail.grokbot.com</a>. If we ever emailed you, reply STOP and we won\'t email again.</p>'
        '<p><a href="index.html">Home</a> · <a href="new-businesses-dfw.html">All DFW areas</a> · <a href="for-commercial-cleaners.html">For cleaners</a> · <a href="for-insurance-agents.html">For insurance agents</a></p></footer>')
CTA = (f'<p><a class="b" href="{L9}">Get the full 30-day list ($9)</a><a class="b" href="{L19}">Weekly feed, $19/mo founding</a>'
       f'<a class="b" style="background:#333" href="{L29}">$29/mo standard</a></p>')
def page(fn, title, desc, body):
    open(os.path.join(D, fn), "w").write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      f'<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{BASE}{fn}"><style>{CSS}</style></head><body>'
      f'<nav><a href="index.html">StorefrontScout</a></nav>{body}{FOOT}</body></html>\n')
def table(rows, n=15):
    rows = sorted(rows, key=lambda r: r["permit_issued"], reverse=True)[:n]
    t = "".join(f"<tr><td>{html.escape(r['business'])}</td><td>{html.escape(r['city'])}</td><td>{r['permit_issued']}</td></tr>" for r in rows)
    return f"<table><tr><th>Business</th><th>City</th><th>Permit issued</th></tr>{t}</table>"
def weekly(rows, today, n=10):
    cut = (today - dt.timedelta(days=7)).isoformat()
    rows = sorted([r for r in rows if r["permit_issued"] >= cut], key=lambda r: r["permit_issued"], reverse=True)[:n]
    if not rows: return "<h2>This week's new openings (free)</h2><p>No new permits in this area in the last 7 days. Check back next Monday.</p>"
    t = "".join(f"<tr><td>{html.escape(r['business'])}</td><td>{html.escape(r['city'])}</td><td>{r['permit_issued']}</td></tr>" for r in rows)
    return (f"<h2>This week's {len(rows)} new openings (free)</h2><p>Free sample: up to 10 businesses that received a Texas sales tax permit in the last 7 days (as of {today}). "
            "Public business records only; sole proprietors and likely home addresses are removed. Data is provided as-is and may contain errors; a permit doesn't guarantee a business is open. "
            "We're a new, small service.</p>"
            f"<table><tr><th>Business</th><th>City</th><th>Permit issued</th></tr>{t}</table>{CTA}")
def main():
    leads = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else bf.build(30, 5000)
    today = dt.date.today(); mon = today.strftime("%B %Y"); pages = []
    for c in CITIES:
        rows = [r for r in leads if r["city"].lower() == c.lower()]
        fn = f"new-businesses-{slug(c)}-tx.html"; pages.append((fn, c))
        page(fn, f"New businesses opening in {c}, TX ({mon})", f"Recently permitted storefronts in {c}, Texas from Texas Comptroller sales tax permit data. Updated {today}.",
          f"<h1>New businesses opening in {c}, TX: {mon}</h1><p>These {c} businesses received a Texas sales tax permit in the last 30 days (as of {today}). "
          f"Sole proprietors, chains and likely home addresses are filtered out. We found {len(rows)} in {c} in that window; below is a sample of the most recent.</p>"
          f"{weekly(rows, today)}<h2>Recent 30 days (sample)</h2>{table(rows)}<h2>Get every new {c} storefront, every Monday</h2><p>The full list adds street address, ZIP, industry code, first-sales date and a sales angle for commercial cleaners and insurance agents. No phone numbers or emails (the public records don't include them).</p>{CTA}")
    for c in COUNTIES:
        rows = [r for r in leads if r["county"] == c]
        fn = f"new-businesses-{slug(c)}-county-tx.html"; pages.append((fn, c + " County"))
        page(fn, f"New businesses in {c} County, TX ({mon})", f"Recently permitted storefronts in {c} County, Texas. Updated {today}.",
          f"<h1>New businesses in {c} County, TX: {mon}</h1><p>{len(rows)} filtered {c} County businesses received a Texas sales tax permit in the last 30 days (as of {today}). </p>{weekly(rows, today)}<h2>Recent 30 days (sample)</h2>{table(rows,20)}{CTA}")
    links = "".join(f'<li><a href="{f}">New businesses in {n}</a></li>' for f, n in pages)
    page("new-businesses-dfw.html", f"New businesses opening in Dallas-Fort Worth ({mon})", "New DFW storefronts by city and county from Texas sales tax permit data.",
      f"<h1>New businesses opening in Dallas-Fort Worth: {mon}</h1><p>{len(leads)} filtered new storefronts across Dallas, Tarrant, Collin and Denton counties in the last 30 days (as of {today}).</p><ul>{links}</ul>{weekly(leads, today)}{CTA}")
    page("for-commercial-cleaners.html", "New DFW commercial cleaning leads | StorefrontScout", "Weekly list of newly permitted DFW restaurants, salons, gyms, offices and shops for commercial cleaning companies.",
      "<h1>For commercial cleaning companies</h1><p>New businesses sign cleaning contracts around the time they open. StorefrontScout gives you a weekly list of DFW storefronts that just received a Texas sales tax permit, so you can reach them early.</p>"
      "<ul><li>Restaurants, salons, gyms, medical offices, retail shops and offices, tagged by trade fit</li><li>Street address, city, ZIP, industry code, permit and first-sales dates</li><li>A one-line suggested angle for each lead</li><li>Chains, out-of-state filers, sole proprietors and likely home addresses filtered out</li></ul>"
      "<p><b>What it isn't:</b> no phone numbers or emails, and no guarantee of a set number of leads. It's a public-records list, cleaned up so you don't have to pull it yourself. We're new, so there are no customer testimonials yet.</p>"
      f"<p>Try one 30-day list for $9 first. If it isn't useful, email us within 7 days for a refund.</p>{CTA}<p>See a sample: <a href=\"new-businesses-dfw.html\">this month's new DFW businesses</a>.</p>")
    page("for-insurance-agents.html", "New DFW business insurance leads | StorefrontScout", "Weekly list of newly permitted DFW businesses for independent insurance agents writing BOP, GL, property and workers' comp.",
      "<h1>For independent insurance agents</h1><p>A business that just got its sales tax permit is opening or recently opened, and often still needs a BOP, general liability, property, commercial auto or workers' comp. StorefrontScout lists these DFW businesses every Monday.</p>"
      "<ul><li>New businesses in Dallas, Tarrant, Collin and Denton counties</li><li>Street address, city, ZIP, industry code, permit and first-sales dates</li><li>A suggested coverage angle for each lead</li><li>Chains, out-of-state filers, sole proprietors and likely home addresses filtered out</li></ul>"
      "<p><b>What it isn't:</b> no phone numbers or emails, and no guarantee of a set number of leads. Follow CAN-SPAM, TCPA and Do-Not-Call rules when you reach out. We're new, so there are no customer testimonials yet.</p>"
      f"<p>Try one 30-day list for $9 first, with a refund within 7 days if it isn't useful.</p>{CTA}<p>See a sample: <a href=\"new-businesses-dfw.html\">this month's new DFW businesses</a>.</p>")
    urls = ["", "new-businesses-dfw.html", "for-commercial-cleaners.html", "for-insurance-agents.html", "dfw-pour-report.html", "catalog.json", "llms.txt"] + [f for f, _ in pages]
    open(os.path.join(D, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(D, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    print(len(urls), "urls")
if __name__ == "__main__": main()
