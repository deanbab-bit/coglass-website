"""Hand-written pages: home, pricing, demo request, support + legal wrappers, 404, sitemap."""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
LASTMOD = '2026-10-03'

PLANS = [
    # name, key, price, lines, popular
    ('Starter', 'starter', '£89', ['1 office login', '3 fitters on the phone app', '150 orders a month', '1 email inbox', '1 shop-floor device', '100 SMS a month', 'Unlimited AI glass scans'], False),
    ('Professional', 'professional', '£199', ['3 office logins', '8 fitters on the phone app', '500 orders a month', '3 email inboxes', '2 shop-floor devices', '300 SMS a month', 'Unlimited AI glass scans'], True),
    ('Business', 'business', '£399', ['7 office logins', '12 fitters on the phone app', '1,500 orders a month', '7 email inboxes', '4 shop-floor devices', '750 SMS a month', 'Unlimited AI glass scans'], False),
]

FEATURES = [
    # icon, title, text, bullets, link
    ('orders', 'Jobs & orders', 'Every job from first enquiry to paid invoice in one record the whole team can see.', ['Statuses for glazing, collection and delivery jobs', 'Notes, photos and documents on the job', '“Needs attention” flags for jobs left sitting'], 'coglass-feature-orders.html'),
    ('quote', 'Quoting', 'Quotes priced from your catalogue and trade price lists, with the drawing on every line.', ['Branded PDF quotes and quote options', 'Customer accepts or declines online', 'Deposits asked for automatically'], 'coglass-feature-quoting.html'),
    ('survey', 'Surveys', 'Measure on the phone — shapes, photos, access notes and GPS — even with no signal.', ['Works offline, syncs later', 'Photos per opening', 'Survey straight onto the work bench'], 'coglass-feature-surveys.html'),
    ('igu', 'Glass specs', 'Full DGU/TGU make-ups, edges, shapes, holes, cut-outs, Georgian bars and leaded lights.', ['Cavity and spacer set per line', 'Drawn to size in mm', '1:1 lay-under template print'], 'coglass-feature-glass-specs.html'),
    ('production', 'Production', 'One board from To plan to Made, with the shop-floor iPad at the bench.', ['Barcode labels and scan to advance', 'In-house or bought-in operations', 'IGU sealing steps'], 'coglass-feature-production.html'),
    ('po', 'Suppliers', 'Purchase orders with the drawing on them, receipts, and automatic chasers when glass is late.', ['Numbered POs per job', 'AI reads supplier price-list PDFs', 'Outwork orders to processors'], 'coglass-feature-suppliers.html'),
    ('schedule', 'Planning', 'Drag surveys, fittings and deliveries onto people and vans for the day or week.', ['Holidays block the board', 'Nearby ready jobs suggested', 'Fitters see their day on the phone'], 'coglass-feature-scheduling.html'),
    ('fitting', 'Fitting & delivery', 'Per-pane sign-off on site with photos, GPS and the customer\'s signature.', ['Partial fits and re-orders flagged', 'Delivery and collection proof', 'Draft invoice raised on completion'], 'coglass-feature-fitting.html'),
    ('invoice', 'Invoicing', 'Deposit, proforma and final invoices with UK VAT, payments and Xero.', ['Overdue invoices flagged', 'Customers pay online from the link', 'Invoices and payments push to Xero'], 'coglass-feature-invoicing.html'),
    ('chat', 'Customer messages', 'Email, SMS and quote-page chat on the job, with automatic updates as it moves.', ['Gmail and Outlook inbox', 'SMS under your company name', 'Messenger and WhatsApp coming soon'], 'coglass-feature-communication.html'),
    ('webshop', 'Webshop', 'A branded shop where trade customers order cut-to-size on their own prices.', ['Card or PayPal checkout, or enquiry only', 'Embeds in your own website', 'Orders drop straight into Coglass'], 'coglass-feature-webshop.html'),
    ('fleet', 'Fleet', 'Vans on the planner, MOT dates and reminders, and the paperwork with the vehicle.', ['Daily van per person', 'MOT history and certificates', 'Reminders before the MOT is due'], 'coglass-feature-fleet.html'),
]

FAQ = [
    ('Is Coglass built for glass and glazing companies?', 'Yes. It holds full IGU make-ups (DGU/TGU, cavity, spacer, gas), every edge and shape, and a drawing canvas for holes, Georgian bars, lead and diamond — plus a 1:1 lay-under template the factory copies onto the glass. It is not a general CRM adapted to glass.'),
    ('Does the survey app work with no signal?', 'Yes. Measurements, drawings, photos, access notes and GPS are captured on the phone and sync when you are back in signal.'),
    ('Does it work on iPhone, Android and the web?', 'Yes — the office uses the web app in a browser, fitters use the iPhone or Android app, and the workshop uses the shop-floor app on an iPad.'),
    ('Does it work with Xero?', 'Yes. Invoices, payments and supplier bills push to Xero, coded to the accounts and VAT rates you choose. Customers can also pay an invoice online from its link.'),
    ('How does the trial work?', 'Pick a plan on the pricing page. We take your card at sign-up and charge nothing for 14 days; cancel before the trial ends and you pay nothing. If you would rather see it first, book a demo and we will walk you through it.'),
    ('Can you help us set it up?', 'Yes — book a demo and we will go through your products, prices and team with you. There is no setup fee.'),
    ('Is WhatsApp included?', 'WhatsApp and Facebook Messenger are built and waiting on Meta\'s approval, so they are coming soon. Email, SMS and the customer chat on quote and tracking pages work today.'),
]


def legal(ctx, name, path, title, description):
    raw = open(os.path.join(HERE, 'legal', f'{name}.html')).read()
    h1 = re.search(r'<!-- h1: (.*?) -->', raw).group(1)
    intro = re.search(r'<!-- intro: (.*?) -->', raw).group(1)
    body_src = re.sub(r'<!-- (h1|intro): .*? -->\n', '', raw)
    body = f'''<section class="page-head"><div class="wrap"><h1>{h1}</h1><p>{intro}</p></div></section>
<article class="prose">
{body_src}</article>'''
    return ctx['layout'](path=path, title=title, description=description, body=body, current=path)


def home(ctx):
    e, I, DEMO, TRIAL = ctx['e'], ctx['ICON'], ctx['DEMO'], ctx['TRIAL']
    img = lambda k, cls='framed': f'<div class="{cls}"><img src="{ctx["IMG"][k][0]}" alt="{e(ctx["IMG"][k][1])}" width="{ctx["IMG"][k][2]}" height="{ctx["IMG"][k][3]}" loading="lazy" decoding="async"></div>'
    src, alt, w, h = ctx['IMG']['planning']
    hero_img = f'<div class="shot"><div class="bar" aria-hidden="true"><i></i><i></i><i></i></div><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high"></div>'
    tiles = [
        ('shaped', 'Shaped glass', 'Arches, gables, holes and cut-outs drawn to size and priced.', 'coglass-feature-glass-specs.html'),
        ('georgian', 'Georgian & lead', 'Georgian bars, square and diamond leaded lights, drawn on the pane.', 'coglass-feature-glass-specs.html'),
        ('igu', 'IGU make-ups', 'Glass per leaf, cavity, spacer and gas on every line.', 'coglass-for-sealed-units.html'),
        ('po', 'Supplier POs', 'Order glass in a click, with the drawing on the PO.', 'coglass-feature-suppliers.html'),
        ('ipad', 'Shop-floor iPad', 'Cut list, scan to advance, collection sign-off.', 'coglass-feature-production.html'),
    ]
    tiles_html = ''.join(f'<li class="tile">{I[i]}<h3>{e(t)}</h3><p>{e(x)}</p><a href="/{l}">More<span class="sr-only"> about {e(t.lower())}</span> →</a></li>' for i, t, x, l in tiles)
    aud = [
        ('glazier', 'Glaziers', 'Survey, quote, book the van, fit and get paid — office, site and workshop in step.', 'coglass-feature-fitting.html', 'How fitting works'),
        ('merchant', 'Glass merchants', 'Trade counter, cut-to-size webshop, trade price lists, stock and deliveries.', 'coglass-for-merchants.html', 'Coglass for merchants'),
        ('igu', 'Sealed unit makers', 'Take and price DGU/TGU units by make-up, then track them through production.', 'coglass-for-sealed-units.html', 'Coglass for unit makers'),
        ('processor', 'Processors', 'Cutting, edgework, toughening and IGU sealing on one board — in-house or bought-in.', 'coglass-feature-production.html', 'The production board'),
        ('counter', 'Trade counters', 'Walk-in quotes and orders in seconds with Quick Go, signed off at the counter.', 'coglass-for-merchants.html', 'Counter sales'),
    ]
    aud_html = ''.join(f'<li class="tile">{I[i]}<h3>{e(t)}</h3><p>{e(x)}</p><a href="/{l}">{e(lt)} →</a></li>' for i, t, x, l, lt in aud)
    feats = ''.join(
        f'<li class="fcard">{I[i]}<h3>{e(t)}</h3><p>{e(x)}</p><ul>{"".join(f"<li>{e(b)}</li>" for b in bs)}</ul>'
        f'<a class="more" href="/{l}">{e(t)} in detail<span aria-hidden="true">&nbsp;→</span></a></li>'
        for i, t, x, bs, l in FEATURES)
    plans = ''.join(
        f'<div class="plan{" pop" if pop else ""}">{"<span class=tag>Most popular</span>" if pop else ""}<h3>{n}</h3><p class="pr">{p}</p><p class="per">per month + VAT</p>'
        f'<ul>{"".join(f"<li>{e(x)}</li>" for x in lines[:4])}</ul><a class="btn{" acc" if pop else ""} block" href="/pricing/#plans">See the {n} plan</a></div>'
        for n, k, p, lines, pop in PLANS)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    body = f'''<section class="hero">
  <div class="wrap grid">
    <div class="copy">
      <span class="eyebrow">Built for UK glass &amp; glazing companies</span>
      <h1>Every job, from enquiry to paid.</h1>
      <p class="lead">Quotes with real glass drawings, a planner your fitters actually use, purchase orders to suppliers, and invoices that look the part. One system for the office, the van and the workshop.</p>
      <div class="ctas"><a class="btn acc lg" href="{DEMO}">Book a demo</a><a class="btn lg" href="{TRIAL}">Start a 14-day trial</a></div>
      {ctx['trust'](['Phone, iPad & web apps', 'Xero connected', 'No setup fee'])}
    </div>
    <div class="visual">{hero_img}{ctx['phone']('Today · Gary', [('f', '08:00 Northgate School', 'Fitting · 1h 30m'), ('s', '10:30 Patel', 'Survey · 45m'), ('f', '13:00 Riverside Offices', 'Fitting · 2h')])}</div>
  </div>
</section>
<section class="strip" aria-label="At a glance">
  <div class="wrap"><ul>
    <li><b>From £89</b>a month + VAT</li>
    <li><b>14 days</b>free trial</li>
    <li><b>Every feature</b>on every plan</li>
    <li><b>iPhone · Android · web</b></li>
  </ul></div>
</section>
<section class="sect">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Made for glass</span><h2>Made for glass, not bolted on</h2><p>The things a general CRM can't do — drawn, priced and sent to the supplier properly.</p></div>
    <ul class="tiles" style="list-style:none;padding:0;margin:0">{tiles_html}</ul>
  </div>
</section>
<section class="sect alt">
  <div class="wrap split">
    <div class="split-text">
      <span class="kicker">The work bench</span>
      <h2>Draw it once. Quote it, order it, make it.</h2>
      <p>Each pane is drawn to size with its shape, holes, cut-outs, Georgian bars or leaded lights. The same drawing prices the line, goes on the quote, the supplier's purchase order and the workshop's cutting sheet.</p>
      <ul class="checks"><li>Full DGU/TGU make-ups, cavity set per line</li><li>Edgework, toughening, laminating — in-house or bought in</li><li>Trade price lists and quantity breaks applied automatically</li></ul>
      <a class="btn" href="/coglass-feature-glass-specs.html">See glass specs</a>
    </div>
    {img('bench')}
  </div>
</section>
<section class="sect">
  <div class="wrap split rev">
    <div class="split-text">
      <span class="kicker">The workshop</span>
      <h2>The whole shop floor on one board</h2>
      <p>Every line lands on the production board when the job is ordered — waiting on a supplier, glass in, in production, ready, made. At the bench, the shop-floor iPad shows the cut list and moves panes on with a barcode scan.</p>
      <ul class="checks"><li>Barcode labels for every pane</li><li>IGU sealing steps checked pane by pane</li><li>Keeps working when the workshop wifi drops</li></ul>
      <a class="btn" href="/coglass-feature-production.html">See production</a>
    </div>
    {img('production')}
  </div>
</section>
<section class="sect alt">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">What your customers receive</span><h2>Quotes and invoices that look the part</h2><p>Your logo and details, the drawing on every line, and a link to accept the quote — or pay the invoice — online.</p></div>
    <div class="docs">
      <figure style="margin:0"><div class="doc"><img src="{ctx['IMG']['quote'][0]}" alt="{e(ctx['IMG']['quote'][1])}" width="900" height="855" loading="lazy" decoding="async"></div><figcaption class="cap">A real quotation PDF from a demo account with made-up details.</figcaption></figure>
      <figure style="margin:0"><div class="doc"><img src="{ctx['IMG']['invoice'][0]}" alt="{e(ctx['IMG']['invoice'][1])}" width="900" height="643" loading="lazy" decoding="async"></div><figcaption class="cap">The matching invoice.</figcaption></figure>
    </div>
  </div>
</section>
<section class="sect">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Who it's for</span><h2>One system for every kind of glass business</h2></div>
    <ul class="tiles" style="list-style:none;padding:0;margin:0">{aud_html}</ul>
  </div>
</section>
<section class="sect alt" id="features">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Everything in Coglass</span><h2>From the first enquiry to the final payment</h2><p>Every plan includes all of it. Plans differ by how many people use Coglass and how much you put through it.</p></div>
    <ul class="fgrid" style="list-style:none;padding:0;margin:0">{feats}</ul>
  </div>
</section>
<section class="sect">
  <div class="wrap split">
    <div class="split-text">
      <span class="kicker">For the team on the road</span>
      <h2>The phone app your fitters will actually use</h2>
      <p>Today's jobs, surveys drawn on the phone, per-pane sign-off with photos and a signature, clock in and out — and it keeps working with no signal.</p>
      <div class="ctas">
        <a class="btn acc" href="https://apps.apple.com/gb/app/coglass-glass-glazing-crm/id6761371345" rel="noopener">Download for iPhone &amp; iPad</a>
        <a class="btn" href="https://play.google.com/store/apps/details?id=com.coglass.app" rel="noopener">Get it on Google Play</a>
      </div>
      <p class="fine">Staff sign in with the login their company gives them. <a href="/coglass-feature-mobile.html">More about the app</a>.</p>
    </div>
    {ctx['big_phone']('Fitting · Northgate School', [('f', 'Classroom 1 — left', 'Fitted · 2 photos'), ('f', 'Classroom 1 — right', 'Fitted'), ('d', 'Corridor', 'Not fitted · broken — re-order'), ('', 'Customer signature', 'Signed 11:42')])}
  </div>
</section>
<section class="sect alt">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Pricing</span><h2>Simple monthly plans</h2><p>Every plan includes the web app, the phone app for fitters and the shop-floor iPad app. Prices exclude VAT. No setup fee, no minimum term.</p></div>
    <div class="plans">{plans}</div>
  </div>
</section>
<section class="sect">
  <div class="wrap" style="max-width:860px">
    <div class="sect-head"><span class="kicker">Questions</span><h2>Frequently asked questions</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>
{ctx['cta_band']('See it on your own kind of jobs', 'Book a demo and we will walk you through Coglass with the glass you sell and the way you work — or pick a plan and start a 14-day trial.')}'''
    jsonld = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Organization', '@id': 'https://coglass.co.uk/#org', 'name': 'Coglass', 'legalName': 'Halliday Morrow Ltd',
             'url': 'https://coglass.co.uk/', 'logo': 'https://coglass.co.uk/assets/img/coglass-icon-512.png',
             'email': 'contact@coglass.co.uk', 'telephone': '+44 121 517 0383', 'areaServed': 'GB'},
            {'@type': 'WebSite', '@id': 'https://coglass.co.uk/#website', 'url': 'https://coglass.co.uk/', 'name': 'Coglass',
             'publisher': {'@id': 'https://coglass.co.uk/#org'}},
            {'@type': 'SoftwareApplication', 'name': 'Coglass', 'applicationCategory': 'BusinessApplication',
             'operatingSystem': 'iOS, Android, Web', 'url': 'https://coglass.co.uk/', 'publisher': {'@id': 'https://coglass.co.uk/#org'},
             'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'GBP', 'lowPrice': '89', 'highPrice': '399', 'offerCount': '3',
                        'description': 'Monthly plans, excluding VAT. 14-day trial.'}},
            {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
        ],
    }
    return ctx['layout'](path='/', title='Coglass | Software for Glaziers, Glass Merchants & Sealed Unit Makers (UK)',
                         description='Quotes with real glass drawings, surveys, production, supplier POs, fitting and invoicing in one system for UK glass and glazing companies. From £89/month + VAT, 14-day trial.',
                         body=body, current='/', og_title='Coglass — every glass job, from enquiry to paid', jsonld=jsonld)


def pricing(ctx):
    e = ctx['e']
    plans = ''.join(
        f'<div class="plan{" pop" if pop else ""}">{"<span class=tag>Most popular</span>" if pop else ""}<h3>{n}</h3><p class="pr">{p}</p><p class="per">per month + VAT</p>'
        f'<ul>{"".join(f"<li>{e(x)}</li>" for x in lines)}</ul><a class="btn{" acc" if pop else ""} block" href="https://accounts.coglass.co.uk/subscribe?plan={k}">Start 14-day trial<span class="sr-only"> on {n}</span></a></div>'
        for n, k, p, lines, pop in PLANS)
    body = f'''<section class="page-head"><div class="wrap"><h1>Pricing</h1><p>Everything in Coglass on every plan, priced by the size of your team. Prices exclude VAT. Last updated: October 2026.</p></div></section>
<section class="sect" style="padding-top:44px">
  <div class="wrap">
    <p style="max-width:780px;color:var(--ink2)">All plans include the full system — orders and quoting, surveys, the work bench, production, supplier orders, scheduling, invoicing, the phone app for fitters, the shop-floor iPad app and the customer portal. Plans differ by how many people use Coglass and how much you put through it, not by which features you get.</p>
    <h2 class="sr-only">Plans</h2>
    <div class="plans" id="plans">{plans}</div>
    <div class="note"><strong>How the trial works.</strong> Your first 14 days are free. We take your card when you start and charge nothing until the trial ends — cancel before then and you pay nothing. We email you before the first payment. During the trial every feature is switched on with no limits; your plan's limits apply from the first payment.</div>
    <!-- [[DECISION: D1 card checkout live]] The trial buttons go to accounts.coglass.co.uk/subscribe (Stripe Checkout). Stripe is in TEST mode on the box, so no real payment can be taken until it is switched to live. Until then the home page and every feature page lead with "Book a demo". -->
    <!-- [[DECISION: D3 trial capped or not]] The sentence about limits matches the code today (trial = full system, uncapped). -->
    <p>Prefer to talk first, or want us to set it up with you? <a href="{ctx['DEMO']}">Book a demo</a>.</p>
  </div>
</section>
<section class="sect alt">
  <div class="wrap" style="max-width:900px">
    <h2>Extras</h2>
    <p>Need more than your plan includes? Email <a href="mailto:{ctx['CONTACT']}">{ctx['CONTACT']}</a> and we'll add it to your subscription — you can't yet buy extras yourself from your account.</p>
    <div class="table-wrap"><table>
      <tr><th scope="col">Extra</th><th scope="col">Price</th></tr>
      <tr><td>Additional shared email inbox</td><td>£7.50 a month + VAT</td></tr>
      <tr><td>Additional office login (comes with its own inbox)</td><td>Ask us</td></tr>
      <tr><td>Additional fitter on the phone app</td><td>Ask us</td></tr>
      <tr><td>More SMS credit</td><td>Ask us — bought in advance, never billed in arrears</td></tr>
      <tr><td>The app in your own branding (iPhone/Android)</td><td>Ask us</td></tr>
    </table></div>
    <!-- [[DECISION: D4 add-on prices]] Office login, fitter, SMS top-up and white-label app prices are not published anywhere; the £7.50 inbox price is carried over from the old page and should be checked against Stripe. -->

    <h2>If you reach a limit</h2>
    <div class="table-wrap"><table>
      <tr><th scope="col">When you reach…</th><th scope="col">What happens</th></tr>
      <tr><td>Your monthly orders</td><td>Nothing stops. You keep working, we let you know you are close, and you can move up a plan whenever it works out cheaper.</td></tr>
      <tr><td>Your office logins or fitters</td><td>The next person can't sign in until a place is free, or until we add another login to your plan.</td></tr>
      <tr><td>Your SMS allowance</td><td>Texts pause until the next month's allowance or until more credit is added. Email us and we'll add it.</td></tr>
      <tr><td>AI glass scans</td><td>There is no limit on any plan.</td></tr>
    </table></div>

    <h2>Billing</h2>
    <p>Plans are billed monthly in advance by card and roll on month to month — no minimum term and no setup fee. Change plan, update your card or cancel from <strong>Manage billing</strong> at <a href="https://accounts.coglass.co.uk">accounts.coglass.co.uk</a>. See our <a href="/refunds/">cancellation and refund policy</a>.</p>
    <h2>VAT</h2>
    <p>All prices exclude VAT, which is added at the UK rate (currently 20%).</p>
    <h2>Anything bigger</h2>
    <p>Several branches, more than the Business plan allows, or the app under your own name? Email <a href="mailto:{ctx['CONTACT']}">{ctx['CONTACT']}</a> and we'll work out what suits.</p>
    <p class="fine">Prices may change; we give existing customers at least 30 days' notice by email first.</p>
  </div>
</section>
{ctx['cta_band']('Not sure which plan fits?', 'Book a demo and we will help you pick — or start on Starter and move up any time.')}'''
    jsonld = {'@context': 'https://schema.org', '@type': 'Product', 'name': 'Coglass', 'brand': 'Coglass',
              'offers': [{'@type': 'Offer', 'name': n, 'price': p.strip('£'), 'priceCurrency': 'GBP',
                          'url': f'https://coglass.co.uk/pricing/#plans'} for n, k, p, l, pop in PLANS]}
    return ctx['layout'](path='/pricing/', title='Pricing | Coglass glazing software — from £89/month + VAT',
                         description='Coglass plans from £89 a month + VAT, every feature on every plan. 14-day trial: card taken at sign-up, nothing charged until the trial ends.',
                         body=body, current='/pricing/', og_title='Coglass pricing', jsonld=jsonld)


def demo(ctx):
    e = ctx['e']
    body = f'''<section class="page-head"><div class="wrap"><h1>Book a demo</h1><p>Tell us a little about your business and we'll call or email to arrange a time — usually the same working day.</p></div></section>
<section class="sect" style="padding-top:44px">
  <div class="wrap two-col">
    <div class="form-card">
      <form id="lead-form">
        <div id="lead-error" class="form-error" role="alert"></div>
        <div class="field"><label for="lead-company">Company name</label><input type="text" id="lead-company" name="company" autocomplete="organization" required></div>
        <div class="field"><label for="lead-name">Your name <span class="hint">(optional)</span></label><input type="text" id="lead-name" name="name" autocomplete="name"></div>
        <div class="field"><label for="lead-email">Work email</label><input type="email" id="lead-email" name="email" autocomplete="email" required></div>
        <div class="field"><label for="lead-phone">Phone <span class="hint">(optional)</span></label><input type="tel" id="lead-phone" name="phone" autocomplete="tel"></div>
        <div class="field"><label for="lead-message">Anything we should know? <span class="hint">(optional)</span></label><textarea id="lead-message" name="message" placeholder="How many people, what you sell or fit, what you use today…"></textarea></div>
        <div class="hp" aria-hidden="true"><label for="lead-website">Leave this empty</label><input type="text" id="lead-website" name="website" tabindex="-1" autocomplete="off"></div>
        <div id="turnstile-slot"></div>
        <button type="submit" class="btn acc lg block" id="lead-submit">Ask us to get in touch</button>
        <p class="fine">We use these details only to contact you about Coglass. See our <a href="/privacy/">privacy policy</a>.</p>
      </form>
      <div id="lead-ok" class="form-ok" tabindex="-1">
        <h2>Thanks — we've got your details</h2>
        <p>We'll call or email you to arrange a demo, usually the same working day. Nothing has been set up or charged.</p>
        <p>Want to look around in the meantime? <a href="/#features">See all features</a> or <a href="/pricing/">compare plans</a>.</p>
      </div>
    </div>
    <div>
      <h2 style="font-size:22px">What happens next</h2>
      <ol class="steps" style="grid-template-columns:1fr">
        <li><h3>We get in touch</h3><p>A quick call to understand what you make, fit or sell, and how you work today.</p></li>
        <li><h3>We show you Coglass</h3><p>On screen, using the kind of jobs you do — quotes, the planner, the phone app, invoices.</p></li>
        <li><h3>You decide</h3><p>If it suits, pick a plan and start a 14-day trial; we'll help you load your products, prices and team.</p></li>
      </ol>
      <p class="fine" style="margin-top:18px">Rather email? <a href="mailto:{ctx['CONTACT']}">{ctx['CONTACT']}</a> · or call <a href="tel:01215170383">{ctx['PHONE']}</a>.</p>
      <p class="fine">Ready to start now? <a href="/pricing/#plans">Pick a plan</a> — your first 14 days are free.</p>
    </div>
  </div>
</section>'''
    return ctx['layout'](path='/signup.html', title='Book a demo | Coglass', description='Book a demo of Coglass, the software for UK glass and glazing companies. Tell us about your business and we will be in touch, usually the same working day.',
                         body=body, current='/signup.html', scripts='<script src="/assets/lead-form.js?v=3" defer></script>\n')


def not_found(ctx):
    body = f'''<section class="notfound"><div class="wrap">
  <p class="kicker">Error 404</p>
  <h1>We can't find that page</h1>
  <p style="color:var(--ink2);max-width:520px;margin:0 auto 26px">It may have moved, or the link may be wrong. Try one of these instead.</p>
  <div class="ctas"><a class="btn pri lg" href="/">Go to the home page</a><a class="btn lg" href="/#features">See all features</a><a class="btn lg" href="/pricing/">Pricing</a><a class="btn lg" href="/support/">Help</a></div>
</div></section>'''
    return ctx['layout'](path='/404.html', title='Page not found | Coglass', description='This page could not be found.', body=body, noindex=True)


SITEMAP = [
    ('/', '1.0', 'weekly'), ('/pricing/', '0.9', 'monthly'), ('/signup.html', '0.8', 'monthly'),
    ('/coglass-for-merchants.html', '0.9', 'monthly'), ('/coglass-for-sealed-units.html', '0.9', 'monthly'),
] + [(f'/coglass-feature-{s}.html', '0.8', 'monthly') for s in
     ['orders', 'quoting', 'surveys', 'glass-specs', 'production', 'suppliers', 'scheduling', 'fitting', 'invoicing',
      'communication', 'webshop', 'fleet', 'mobile']] + [
    ('/support/', '0.5', 'monthly'), ('/terms/', '0.3', 'yearly'), ('/privacy/', '0.3', 'yearly'),
    ('/refunds/', '0.3', 'yearly'), ('/dpa/', '0.3', 'yearly'),
]


def build(ctx):
    out = {
        'index.html': home(ctx),
        'pricing/index.html': pricing(ctx),
        'signup.html': demo(ctx),
        '404.html': not_found(ctx),
        'terms/index.html': legal(ctx, 'terms', '/terms/', 'Terms of Service | Coglass', 'The terms between Halliday Morrow Ltd (Coglass) and businesses that subscribe to Coglass.'),
        'refunds/index.html': legal(ctx, 'refunds', '/refunds/', 'Cancellation & Refunds | Coglass', 'How to cancel Coglass, when access ends, what happens to your data and when we refund.'),
        'privacy/index.html': legal(ctx, 'privacy', '/privacy/', 'Privacy Policy | Coglass', 'How Coglass handles personal data on this website, in subscription accounts and inside the Coglass apps.'),
        'dpa/index.html': legal(ctx, 'dpa', '/dpa/', 'Data Processing Agreement | Coglass', 'The UK GDPR Article 28 terms between Halliday Morrow Ltd and Coglass customers, including the sub-processor list.'),
        'support/index.html': legal(ctx, 'support', '/support/', 'Help & Support | Coglass', 'Help signing in to Coglass, common questions, and how to contact the Coglass team.'),
    }
    urls = ''.join(f'  <url><loc>https://coglass.co.uk{p}</loc><lastmod>{LASTMOD}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n'
                   for p, pr, c in SITEMAP)
    out['sitemap.xml'] = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    out['robots.txt'] = 'User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /og-image.html\n\nSitemap: https://coglass.co.uk/sitemap.xml\n'
    return out
