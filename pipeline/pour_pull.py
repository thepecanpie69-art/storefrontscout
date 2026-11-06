"""DFW Pour Report: pending new TABC alcohol-license applications in Dallas/Tarrant/Collin/Denton.
Source: TABC via Texas Open Data Portal, dataset mxm5-tdpj. Business fields only."""
import csv, json, re, os, urllib.request, urllib.parse
OUT = os.environ.get("POUR_OUT", "output")
os.makedirs(OUT, exist_ok=True)
COUNTIES = ["DALLAS","TARRANT","COLLIN","DENTON"]
where = "upper(county) in(" + ",".join(f"'{c}'" for c in COUNTIES) + ")"
url = "https://data.texas.gov/resource/mxm5-tdpj.json?" + urllib.parse.urlencode(
    {"$where": where, "$order": "submission_date DESC", "$limit": 5000})
rows = json.load(urllib.request.urlopen(url))
ENTITY = re.compile(r"\b(LLC|L\.L\.C|INC|CORP|CORPORATION|CO\b|COMPANY|LP|L\.P|LTD|LLP|PLLC|PARTNERS|GROUP|HOLDINGS|ENTERPRISES|RESTAURANT|CLUB|ASSOCIATION|CHURCH|FOUNDATION|TRUST|VENTURES|HOSPITALITY|MANAGEMENT|SOCIETY|CITY OF|UNIVERSITY)", re.I)
RESID = re.compile(r"\b(DR|DRIVE|LN|LANE|CT|COURT|CIR|CIRCLE|TRL|TRAIL|WAY|PL|PLACE|COVE|CV|TER|TERRACE|LOOP)\.?$", re.I)
UNIT = re.compile(r"(STE|SUITE|UNIT|#|BLDG|BUILDING)", re.I)
TEMP = {"NT"}  # temporary/event permits: not new storefronts
keep, drop = [], {"individual":0,"likely_home":0,"temp_event":0}
for r in rows:
    owner, addr = r.get("owner",""), r.get("address","").strip()
    if r.get("license_type") in TEMP: drop["temp_event"]+=1; continue
    if not ENTITY.search(owner): drop["individual"]+=1; continue
    if RESID.search(addr) and not UNIT.search(addr) and not re.search(r"\b(FWY|PKWY|HWY|BLVD|EXPY|PIKE|RD|ROAD|AVE|ST)\b", addr, re.I):
        drop["likely_home"]+=1; continue
    r["submission_date"] = r.get("submission_date","")[:10]; r["zip"]=r.get("zip","")[:5]; r["county"]=r.get("county","").title()
    keep.append(r)
cols = ["submission_date","license_type","applicationstatus","owner","address","city","zip","county","application_id"]
# Free sample: one row per owner (most recent first) so 10 slots show 10 businesses, not duplicate permit types.
seen, sample = set(), []
for r in keep:
    key = r.get("owner","").strip().casefold()
    if not key or key in seen: continue
    seen.add(key); sample.append(r)
    if len(sample) >= 10: break
for fn, data in (("dfw_pending.csv", keep), ("sample.csv", sample)):
    with open(os.path.join(OUT,fn),"w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
print("raw", len(rows), "kept", len(keep), "sample_unique", len(sample), "dropped", drop)
