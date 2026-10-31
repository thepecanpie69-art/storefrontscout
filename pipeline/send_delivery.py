#!/usr/bin/env python3
"""Delivery stub: emails latest feed to subscribers via Resend or Brevo. DRY RUN unless SEND=1."""
import base64, csv, glob, json, os, urllib.request
E = os.environ
FOOTER = (f"<hr><small>You get this because you subscribed to DFW New Storefronts. "
          f"{E.get('POSTAL_ADDRESS','[POSTAL ADDRESS]')} · <a href='{E.get('UNSUBSCRIBE_URL','#')}'>Unsubscribe</a></small>")
def main():
    feed = sorted(glob.glob("output/feed_*.csv"))[-1]; body = open(feed[:-4] + ".html").read().replace("{{FOOTER}}", FOOTER)
    subs = [r["email"] for r in csv.DictReader(open(E.get("SUBSCRIBERS_FILE", "subscribers.csv"))) if r.get("active", "1") == "1"] if os.path.exists(E.get("SUBSCRIBERS_FILE","subscribers.csv")) else []
    att = base64.b64encode(open(feed, "rb").read()).decode()
    for to in subs:
        if E.get("SEND") != "1": print("DRY RUN ->", to); continue
        if E.get("EMAIL_PROVIDER", "resend") == "resend":
            url, hdr = "https://api.resend.com/emails", {"Authorization": "Bearer " + E["EMAIL_API_KEY"]}
            data = {"from": E["FROM_EMAIL"], "to": [to], "subject": "DFW New Storefronts this week", "html": body, "attachments": [{"filename": os.path.basename(feed), "content": att}]}
        else:
            url, hdr = "https://api.brevo.com/v3/smtp/email", {"api-key": E["EMAIL_API_KEY"]}
            data = {"sender": {"email": E["FROM_EMAIL"]}, "to": [{"email": to}], "subject": "DFW New Storefronts this week", "htmlContent": body, "attachment": [{"name": os.path.basename(feed), "content": att}]}
        req = urllib.request.Request(url, json.dumps(data).encode(), {**hdr, "Content-Type": "application/json"})
        print(to, urllib.request.urlopen(req).status)
    print(f"{len(subs)} subscribers processed from {feed}")
if __name__ == "__main__": main()
