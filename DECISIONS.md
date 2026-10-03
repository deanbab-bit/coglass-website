# Decisions needed from the owner (website)

The October 2026 rebrand made every page consistent with what the code does today. Where the
right answer is a business or legal choice, the page says what is true now and the source
carries an HTML comment `<!-- [[DECISION: Dn …]] -->` at the spot to change. Edit the source
under `_src/` and re-run `python3 _src/build.py`.

| # | Decision | What the site says today | Where |
|---|---|---|---|
| D1 | **Take real card payments now?** Stripe on the accounts box is in TEST mode, so the "Start 14-day trial" buttons on /pricing go to a checkout that can't take a real card. | Every page leads with **Book a demo** (the lead form). "Start a 14-day trial" links go to /pricing/#plans, whose buttons go to accounts.coglass.co.uk/subscribe. | `_src/pages.py` pricing() |
| D2 | **Trial with or without a card.** | Card taken at sign-up, nothing charged for 14 days (what the accounts code does). | pricing, terms §4, refunds, FAQ |
| D3 | **Trial capped or uncapped.** The code gives every trial the full system with no limits (`TRIAL_LICENCE` = enterprise). | "During the trial every feature is switched on with no limits; your plan's limits apply from the first payment." | pricing, terms §4 |
| D4 | **Add-on prices** — extra office login, extra fitter, SMS top-ups, white-label app (£79 one-off setup in the product notes, never published). Is the £7.50 inbox price still right in Stripe? | Inbox £7.50/month; the rest "Ask us"; extras are added by email, because they can't be bought from the account yet. | pricing |
| D5 | **Refund policy** — keep the current wording (no part-month refunds except our mistakes/faults)? | Unchanged except the cancel route and the "extras" paragraph. | refunds |
| D6 | **Data retention after cancellation.** Nothing in the code deletes a tenant; a lapsed account goes read-only. The old DPA promised deletion 30 days after the end. | "Kept read-only; we don't delete it automatically; ask and we'll delete it." No period promised. | refunds, DPA §10, privacy |
| D7 | **Repeat trials** (same company starting a second 14-day trial). | Not mentioned. | — |
| D8 | **Plan-change proration.** The old text promised "upgrade immediate + charge the difference, downgrade at renewal" — that depends on the Stripe billing-portal settings. | "The billing page shows any part-month charge or credit before you confirm." | refunds |
| D9 | **ICO registration number** for the privacy policy. | Omitted until supplied. | privacy |
| D10 | **Sub-processor list.** Added Expo (push), OpenStreetMap Nominatim (address lookup), the public OSRM server (routing), PayPal and Meta; removed Unipile (switched off 2026-08-02). Confirm the "Where" column, whether to keep using the free public Nominatim/OSRM servers, and **where off-site backups are held** (no host is named anywhere). The DPA promises 30 days' notice before adding a sub-processor — **existing customers should be emailed** about these additions. | Updated list. | DPA §7 |
| D11 | **Backup retention period** (old text: 90 days). | No period promised. | DPA §10 |
| D12 | **Cloudflare Turnstile** on the demo form — create a Turnstile site, paste the public site key into `assets/lead-form.js`, and make HQ `/api/leads` verify the token. | Off; honeypot + time-to-submit check only. | `assets/lead-form.js` |
| D13 | **Support address** — the brand mockup shows support@coglass.co.uk; every page and the legal documents use contact@coglass.co.uk. | contact@coglass.co.uk everywhere. | footer, legal |
| D14 | **Testimonials** — the approved mockup had a placeholder quote. No real testimonial exists, so none is shown. | None. | home |
| D15 | **WhatsApp / Messenger launch.** | "Coming soon — waiting on Meta's approval." | communication, home, FAQ, privacy |
