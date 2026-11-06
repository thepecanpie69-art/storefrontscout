"""Refresh the free weekly sample on docs/dfw-pour-report.html from TABC pending-application open data.
Shows business name, city, permit type and filing date only (no street addresses)."""
import csv, datetime as dt, html, os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
out = os.path.join(root, "output"); os.environ["POUR_OUT"] = out
subprocess.run([sys.executable, os.path.join(here, "pour_pull.py")], check=True, cwd=root)
rows = list(csv.DictReader(open(os.path.join(out, "dfw_pending.csv"))))
today = dt.date.today(); cut = (today - dt.timedelta(days=7)).isoformat()
# One row per owner so the free table shows 10 businesses, not duplicate permit types.
wk, seen = [], set()
for r in rows:
    if r["submission_date"] < cut: continue
    key = r.get("owner","").strip().casefold()
    if not key or key in seen: continue
    seen.add(key); wk.append(r)
    if len(wk) >= 10: break
# Keep docs/pour-sample.csv in sync with the unique weekly sample.
import shutil
shutil.copy(os.path.join(out, "sample.csv"), os.path.join(root, "docs", "pour-sample.csv"))
t = "".join(f"<tr><td>{html.escape(r['owner'])}</td><td>{html.escape(r['city'].title())}</td><td>{html.escape(r['license_type'])}</td><td>{r['submission_date']}</td></tr>" for r in wk)
sec = (f"<!--WEEKLY--><h2>This week's {len(wk)} new applications (free)</h2><p>Free sample: up to 10 DFW businesses that filed a new TABC alcohol permit application in the last 7 days (as of {today}). "
       "Public TABC open data, business fields only; individual applicants and likely home addresses are removed. Provided as-is and may contain errors; a pending application doesn't guarantee a permit or an opening. "
       "Not affiliated with or endorsed by TABC.</p>"
       f"<table><tr><th>Applicant</th><th>City</th><th>Permit type</th><th>Filed</th></tr>{t}</table>"
       '<p><a class="b" href="https://buy.stripe.com/fZu00j9bheOR3Ak7M4gEg03">Get the full current list ($15)</a> <a class="b" href="https://buy.stripe.com/00w14nevBeOR5Is8Q8gEg04">Weekly, $29/mo</a></p><!--/WEEKLY-->')
p = os.path.join(root, "docs", "dfw-pour-report.html"); s = open(p).read()
s = re.sub(r"<!--WEEKLY-->.*?<!--/WEEKLY-->", lambda m: sec, s, flags=re.S) if "<!--WEEKLY-->" in s else s.replace("<h2>Who it's for</h2>", sec + "<h2>Who it's for</h2>", 1)
open(p, "w").write(s); print(len(wk), "weekly rows")
