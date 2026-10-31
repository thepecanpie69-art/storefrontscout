# Agent-Run Business Plan: Research Summary (Oct 31, 2026, CT)

## Bottom line (pushback first)
The generic "Texas new-business lead feed" is a real market, but it is **already crowded with near-identical, agent-style products** built on the same free Comptroller file. A generic clone would compete on price against $20 to $49 products. **It's still worth doing, but only as a narrow vertical feed** where we filter, score, and package leads for one buyer type. Recommended: **"DFW New Storefronts for Commercial Cleaners & Insurance Agents"**, a weekly email plus CSV at $19 to $29/mo, sold self-serve through Stripe Payment Links.

## 1. Data sources checked (live, Oct 31, 2026)
| # | Source | Access | Freshness | Verdict |
|---|---|---|---|---|
| A | TX Comptroller **Active Sales Tax Permit Holders** (data.texas.gov `jrea-zgmq`): https://data.texas.gov/resource/jrea-zgmq.json | Free Socrata API, JSON/CSV, no key needed | Updated 2026-10-31. Has `outlet_permit_issue_date`, `outlet_first_sales_date`, NAICS, and outlet address. **1,138 new outlet permits in Tarrant County (code 220) since Oct 1** | **Best.** Free, clean, and legal. No phone or email |
| B | Dallas **Building Permits** (dallasopendata.com `e7gq-4sah`) | Free Socrata API. Fields: permit type, value, contractor, address, work description | Dataset touched today, but the **newest issued_date is 12/31/25** and there are 0 rows for Oct 2026. Feed looks frozen (likely a system migration) | **Unreliable right now.** Don't build on it |
| C | Fort Worth open data (data.fortworthtexas.gov) | The site loads, but its catalog API returned no JSON | Not verified | Would need browser work. Skip for v1 |

Also exists: data.texas.gov Mixed Beverage permits (`8f4g-cpk9`, updated today), which could be an extra signal for restaurant or bar openings.

## 2. Competitors and pricing (pages checked this session)
**Texas new-business (sales-tax permit) leads, the same data as A:**
- New Storefronts: from **$49/mo**, weekly, about 2,800 Texas outlets per week. https://newstorefrontleads.com/
- Texas Lead Engine: $149/mo per region, $399 statewide. https://texasleadengine.com/
- Texas Business Leads: $126/mo per region, $299 statewide. https://texasbusinessleads.com/subscribe
- MyPermitLeads: $249/mo per metro (adds TABC liquor applications). https://mypermitleads.com/pricing
- PermitPub: statewide from $499/mo. https://permitpub.com/markets/texas-statewide-business-license-leads/

**Building-permit leads:** PingPermit $20/mo, PermitGrab $149, Shovels $599 to $999, Construction Monitor $31 to $1,281, Job Start List $29 to $59 (not open yet). Source: https://jobstartlist.com/guides/permit-lead-services-compared and https://www.shovels.ai/compare/construction-monitor

**What this tells us:** demand is real, since at least five companies charge for it. But the barrier to entry is zero, and several of these look like they launched recently. Our edge can't be the data. It has to be **(1) a narrow buyer, (2) a lower price, and (3) leads that are ready to act on** (filtered by NAICS, with a one-line pitch angle per lead and a map or route order).

## 3. The three niche + data combos evaluated
1. **New storefronts → commercial cleaners, insurance agents, sign shops, POS/merchant services (Source A, DFW).** Every new outlet needs insurance, cleaning, and signage. The data is free, fresh, and stable. Competition is high for generic lists, but nobody is clearly targeting a single trade. **Pick.**
2. **Building permits → roofers, pool, solar, and HVAC subs (Source B).** High value per lead, but Dallas's feed is stale, Fort Worth's isn't verified, and PingPermit already sells this at $20/mo. **Reject for now.**
3. **New auto-related outlets (NAICS 4411/4413/8111) → parts suppliers, detail-supply vendors, and later NodTap B2B.** Very low volume in DFW, so it's a weak standalone product. **But it's an excellent free internal feed for NodTap's B2B prospecting later.**

## 4. Legal and compliance (honest flags, not legal advice)
- **Data resale:** Comptroller data is public information under the Texas Public Information Act, and competitors resell it openly. Keep a source link on every record and don't claim "exclusive."
- **Never include sole-proprietor personal names or home addresses** (taxpayer org type `IS`). Filter them out. This mirrors New Storefronts' practice and avoids privacy and doxxing complaints.
- **CAN-SPAM** applies to B2B cold email: a truthful From and subject, a physical postal address, a working opt-out honored within 10 days, and no purchased email lists. Use a PO box or virtual address, never Clay's home.
- **TCPA / Texas telemarketing law (Bus. & Com. Code ch. 304):** **no cold calls or texts by agents.** Email and inbound only.
- **Platform ToS:** the free email providers (Gmail, Resend free, Brevo free) ban or throttle cold bulk sending. Keep cold outreach under about 30 per day from a dedicated domain, or rely on inbound (SEO pages and directories).
- **Stripe:** lead-list sales are allowed. List a clear refund policy on the site.

## 5. Build plan (near-zero cost)
**Stack (all free tiers):**
- **Data:** the data.texas.gov Socrata API.
- **Compute:** a GitHub Actions cron job (free) runs a Python script weekly or daily.
- **Site:** GitHub Pages or Cloudflare Pages, showing a landing page, a free sample, and a public "new DFW storefronts this week" teaser for SEO.
- **Payments:** Stripe Payment Links (no code), with a Stripe webhook or a daily Stripe API poll to pull the subscriber list.
- **Email delivery:** Resend or Brevo free tier (about 100 to 300 emails per day) for subscriber delivery.
- **Domain:** about $10 per year. This is the only real cost, and it's optional at first (a *.pages.dev subdomain works).

**What the agents do (daily or weekly):**
1. Pull the new permits since the last run, then filter to DFW counties (Dallas, Tarrant, Collin, Denton) and drop re-permits (first-sales date more than 90 days before the permit) and sole-proprietor rows.
2. Classify each lead by NAICS and generate a per-trade angle, e.g. "restaurant, opens Nov 1 → needs hood cleaning + GL insurance".
3. Build a CSV for each trade plus an email digest, then send them to active Stripe subscribers.
4. Publish the free teaser page (top 10 this week) to build SEO and capture emails.
5. Outreach agent: find local cleaners and insurance agents with public business emails (company websites), send a short CAN-SPAM-compliant email offering a free sample week, and log any opt-outs.
6. Report weekly to Clay on subscribers, MRR, churn, and send counts.

**Pricing:** $19/mo per trade per metro (founding price), $29 standard, or a $9 one-time "last 30 days" CSV. That undercuts every competitor found ($49 and up for Texas-wide lists).

**Realistic timeline:** build in 1 to 2 days, with the first free-sample signups in weeks 1 to 2. **First paying customer is likely in 3 to 8 weeks.** $500 MRR (about 25 subscribers) is plausible in 3 to 6 months if outreach and SEO work, and it could also stall at $0 to $100. Treat this as a learning lab, not income.

## 6. One-time human steps (Clay only)
1. Confirm the Stripe account is activated (identity and bank already done?) and approve creating 2 to 3 Payment Links.
2. Create a GitHub account or repo (or approve agent use of the connected GitHub) and enable Pages and Actions.
3. Sign up for Resend or Brevo (free) and verify the sending domain's DNS. Provide a business postal address for CAN-SPAM (a PO box or virtual mailbox).
4. Optional: buy a domain (about $10 per year).
5. Approve the outreach email template once. After that, agents run within the agreed limits.

## 7. Better alternative? (considered)
- An **AI-tool or "vibe-coding fixer"** product fits Clay's audience, but delivering it needs human-quality judgment and support. It's less autonomous.
- The **lead feed** wins on autonomy: the data is structured, delivery is deterministic, and payments are self-serve. Its weakness is competition, which we answer by going narrow and cheap. If there are 0 paid conversions after 8 weeks, pivot the same pipeline to a different buyer, such as sign shops or POS resellers. Re-checking takes about 1 hour of agent time.

## 8. NodTap connection points (later)
- The same pipeline filtered to auto NAICS codes (8111 repair, 811192 car wash/detail, 4411 dealers) gives NodTap a free weekly list of **new DFW auto-service businesses** to recruit as partners.
- Later, the lead-business brand could sell "trust badge" onboarding to those new shops through a NodTap referral.
