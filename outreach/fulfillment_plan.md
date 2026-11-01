# Fulfillment automation proposal
1. A customer pays through a Stripe Payment Link. Stripe emails a "new payment"/"new subscription" notice to the account email, storefrontscout@mail.grokbot.com.
2. Preferred: a Stripe webhook isn't possible on static hosting, so a scheduled GitHub Action (hourly) uses a restricted Stripe key (read-only on Checkout Sessions, Subscriptions and Customers) to list new paid sessions and active subscriptions. It writes the customer emails to subscribers.csv, kept as an encrypted GitHub secret or a private gist, never in the public repo.
   - $9 one-time: the 30-day CSV is emailed right away, once.
   - Subscriptions: added to the Monday send. When a subscription is canceled or past due, the customer is removed automatically.
3. Sending: the Monday workflow runs build_feed.py, then send_delivery.py through the Brevo free tier (300/day) or Resend free tier (100/day, 3,000/mo).
4. Fallback until then: an agent reads the Stripe notification emails and drafts the delivery for Clay to approve.

## Clay's one-time steps
- Sign up for Brevo or Resend free, using storefrontscout@mail.grokbot.com. Verify the sender (single sender, or a domain if one is bought).
- Add GitHub repo secrets: BREVO_API_KEY (or RESEND_API_KEY), STRIPE_RESTRICTED_KEY (read-only, created in the StorefrontScout Stripe account), POSTAL_ADDRESS.
- Get a PO box or virtual mailbox for the CAN-SPAM footer (not a home address).
- Add the payout bank in Stripe.
- Approve the refund/cancel policy wording on the site, and the cold email templates.
