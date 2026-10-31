#!/usr/bin/env python3
"""Weekly DFW new-storefront lead feed. Stdlib only. Source: TX Comptroller (data.texas.gov jrea-zgmq)."""
import argparse, csv, datetime as dt, html, json, os, re, urllib.parse, urllib.request
API = "https://data.texas.gov/resource/jrea-zgmq.json"
COUNTIES = {"220": "Tarrant", "057": "Dallas", "043": "Collin", "061": "Denton"}
# NAICS prefix -> (trades, angle)
MAP = [
 ("722", "Cleaning; Insurance", "New restaurant: needs nightly kitchen/floor cleaning plus general liability & liquor/food-spoilage cover."),
 ("721", "Cleaning; Insurance", "New lodging: recurring housekeeping overflow and property/liability insurance."),
 ("8121", "Cleaning; Insurance", "New salon/spa: daily sanitation standards and professional liability cover."),
 ("6211", "Cleaning; Insurance", "New medical/dental office: clinical-grade cleaning and malpractice/BOP review."),
 ("62", "Cleaning; Insurance", "New care facility: sanitation contract and liability/workers' comp cover."),
 ("44", "Cleaning; Insurance", "New retail storefront: after-hours floor/window cleaning and BOP/inventory insurance."),
 ("45", "Cleaning; Insurance", "New retail storefront: after-hours floor/window cleaning and BOP/inventory insurance."),
 ("7139", "Cleaning; Insurance", "New fitness/recreation venue: daily locker/equipment cleaning and high-liability cover."),
 ("811", "Insurance", "New repair shop: garagekeepers & general liability; shop floor degreasing."),
 ("23", "Insurance", "New contractor: GL, commercial auto and workers' comp quotes."),
 ("42", "Cleaning; Insurance", "New wholesale/warehouse site: warehouse cleaning and property/cargo cover."),
 ("31", "Cleaning; Insurance", "New manufacturer: industrial cleaning and property/product liability cover."),
 ("32", "Cleaning; Insurance", "New manufacturer: industrial cleaning and property/product liability cover."),
 ("33", "Cleaning; Insurance", "New manufacturer: industrial cleaning and property/product liability cover."),
 ("5", "Cleaning; Insurance", "New office-based business: weekly office cleaning and BOP/cyber cover."),
]
HOME_HINT = re.compile(r"\b(STE|SUITE|UNIT|BLDG|#)\b", re.I)
BIZ_WORDS = re.compile(r"\b(LLC|INC|CORP|CO|LTD|LP|PLLC|COMPANY|GROUP|SERVICES?|STORE|SHOP|CAFE|GRILL|MARKET)\b", re.I)

def fetch(days, limit):
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    codes = ",".join(f"'{c}'" for c in COUNTIES)
    q = {"$where": f"outlet_county_code in({codes}) AND outlet_permit_issue_date >= '{since}'",
         "$limit": str(limit), "$order": "outlet_permit_issue_date DESC"}
    with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(q), timeout=60) as r:
        return json.load(r)

def classify(naics):
    for p, t, a in MAP:
        if naics.startswith(p): return t, a
    return None, None

_EXC = [l.strip().upper() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chain_exclusions.txt")) if l.strip() and not l.startswith("#")]
CORP_HINT = re.compile(r"\b(INCORPORATED|CORPORATION|HOLDINGS|FINANCIAL|ENTERPRISES OF|USA)\b|\d{3,}\s*$", re.I)
MAX_OUTLET = 3  # outlet_number > 3 => taxpayer runs many locations statewide (chain)

def is_chain(r):
    names = (r.get("outlet_name", "") + " | " + r.get("taxpayer_name", "")).upper()
    if any(x in names for x in _EXC): return True
    try:
        if int(r.get("outlet_number", "1")) > MAX_OUTLET: return True
    except ValueError: pass
    if r.get("taxpayer_state", "TX") != "TX": return True  # out-of-state HQ
    return bool(CORP_HINT.search(r.get("outlet_name", "")))

def keep(r):
    if is_chain(r): return False
    # Exclude sole proprietors (org type IS = individual) and likely home addresses
    if r.get("taxpayer_organization_type", "").startswith("IS"): return False
    name = r.get("outlet_name", "")
    addr = r.get("outlet_address", "")
    if r.get("taxpayer_address") == addr and not HOME_HINT.search(addr) and not BIZ_WORDS.search(name): return False
    return True

def build(days, limit):
    out = []
    for r in fetch(days, limit):
        if not keep(r): continue
        trades, angle = classify(r.get("outlet_naics_code", ""))
        if not trades: continue
        out.append({"business": r.get("outlet_name", "").title(), "address": r.get("outlet_address", "").title(),
            "city": r.get("outlet_city", "").title(), "zip": r.get("outlet_zip_code", ""),
            "county": COUNTIES.get(r.get("outlet_county_code"), ""), "naics": r.get("outlet_naics_code", ""),
            "permit_issued": r.get("outlet_permit_issue_date", "")[:10], "first_sales": r.get("outlet_first_sales_date", "")[:10],
            "fits": trades, "sales_angle": angle})
    return out

def write(leads, prefix):
    os.makedirs(os.path.dirname(prefix) or ".", exist_ok=True)
    with open(prefix + ".csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(leads[0].keys()) if leads else ["business"]); w.writeheader(); w.writerows(leads)
    md = [f"# DFW New Storefronts: {len(leads)} leads ({dt.date.today()})", "",
          "Source: Texas Comptroller public sales tax permit data. No phone/email included.", "",
          "| Business | City | Fits | Angle |", "|---|---|---|---|"]
    md += [f"| {l['business']} | {l['city']} | {l['fits']} | {l['sales_angle']} |" for l in leads]
    open(prefix + ".md", "w").write("\n".join(md) + "\n")
    rows = "".join(f"<tr><td>{html.escape(l['business'])}<br><small>{html.escape(l['address'])}, {html.escape(l['city'])} {l['zip']}</small></td>"
                   f"<td>{l['permit_issued']}</td><td>{html.escape(l['fits'])}</td><td>{html.escape(l['sales_angle'])}</td></tr>" for l in leads)
    open(prefix + ".html", "w").write(f"<h2>DFW New Storefronts — {len(leads)} leads</h2><p>Full CSV attached. Source: Texas Comptroller public permit data.</p>"
        f"<table border=1 cellpadding=4><tr><th>Business</th><th>Permit</th><th>Fits</th><th>Angle</th></tr>{rows}</table>{{{{FOOTER}}}}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=7); ap.add_argument("--limit", type=int, default=5000)
    ap.add_argument("--sample", type=int, default=10); ap.add_argument("--out", default="output"); ap.add_argument("--site", default="docs")
    a = ap.parse_args(); leads = build(a.days, a.limit)
    d = dt.date.today().isoformat()
    write(leads, f"{a.out}/feed_{d}")
    # sample: spread across trades, one per business
    write(leads[:: max(1, len(leads)//a.sample)][:a.sample], f"{a.out}/sample")
    import shutil; os.makedirs(a.site, exist_ok=True); shutil.copy(f"{a.out}/sample.csv", f"{a.site}/sample.csv")
    print(f"{len(leads)} leads -> {a.out}/feed_{d}.csv ; sample -> {a.out}/sample.csv")
