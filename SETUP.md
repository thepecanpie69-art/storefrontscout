# Human-only steps (one time), then agents run it
1. **New, separate Stripe account** (do NOT use NodTap's): create a new account (or a new separate account under your login via "New account") with its own business profile and **its own bank account for payouts**. Complete identity verification. Create 3 Payment Links: $9 one-time, $19/mo, $29/mo. Paste the URLs into `config.example.env` / `docs/index.html` (replace REPLACE_*).
2. **GitHub repo**: create a repo, push this folder, enable Actions, and enable Pages: Settings → Pages → Deploy from branch `main`, folder `/docs`.
3. **Free email sender**: Resend or Brevo free tier; verify sender domain; add `EMAIL_API_KEY` as a repo secret and `EMAIL_PROVIDER`, `FROM_EMAIL` as repo variables.
4. **Postal address** for CAN-SPAM (PO box or virtual mailbox) → `POSTAL_ADDRESS` variable.
5. **Optional domain** (~$10/yr) for credibility and email deliverability.
6. **Approvals**: approve the landing page copy, `outreach_template.md`, then set repo variable `SEND_ENABLED=1` to turn delivery on.
Subscribers: until a Stripe webhook is added, agents append paid emails to `subscribers.csv` (columns: email,active).

## Maintenance (agents)
- Chain/franchise filter: edit `pipeline/chain_exclusions.txt` (one name per line). Also auto-excluded: outlet # > 3, out-of-state taxpayer, corporate-style names.
- Weekly run writes `output/feed_*.csv` (workflow artifact) and refreshes `docs/sample.csv`. Delivery is dry-run until `SEND_ENABLED=1`.
