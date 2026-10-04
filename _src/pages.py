"""Hand-written pages: demo request, support + legal wrappers, 404, sitemap.

Home, pricing and the country sections are in country_pages.py."""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
LASTMOD = '2026-10-04'

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
    ('invoice', 'Invoicing', 'Deposit, proforma and final invoices with VAT, payments and Xero.', ['Overdue invoices flagged', 'Customers pay online from the link', 'Invoices and payments push to Xero'], 'coglass-feature-invoicing.html'),
    ('chat', 'Customer messages', 'Email, SMS and quote-page chat on the job, with automatic updates as it moves.', ['Gmail and Outlook inbox', 'SMS under your company name', 'Messenger and WhatsApp coming soon'], 'coglass-feature-communication.html'),
    ('webshop', 'Webshop', 'A branded shop where trade customers order cut-to-size on their own prices.', ['Card or PayPal checkout, or enquiry only', 'Embeds in your own website', 'Orders drop straight into Coglass'], 'coglass-feature-webshop.html'),
    ('fleet', 'Fleet', 'Vans on the planner, MOT or roadworthiness dates and reminders, and the paperwork with the vehicle.', ['Daily van per person', 'Test history and certificates', 'Reminders before the vehicle test is due'], 'coglass-feature-fleet.html'),
    ('scan', 'AI glass scan', 'Glass sizes read out of a customer\'s email, matched to your products and prices, and added to an order.', ['Reads quantities and sizes', 'Matched to your catalogue', 'You check before it\'s added'], 'coglass-feature-ai-glass-scan.html'),
    ('portal', 'Customer portal', 'A branded login for homeowners and trade customers to see and act on their jobs.', ['Next visit, add to calendar', 'Approve quotes, pay deposits', 'Trade sites, statements, supply orders'], 'coglass-feature-customer-portal.html'),
    ('track', 'Live tracking', 'An on-our-way text with a tracking link, sent when the fitter sets off.', ['Arrival window and stop number', 'Message the office or the fitter', 'No app for the customer'], 'coglass-feature-tracking.html'),
    ('label', 'Glass labels', 'A barcode label on every pane, scanned in at goods-in.', ['Job, opening and size on the label', 'Scan to mark glass received', 'Job shows ready for fitting'], 'coglass-feature-glass-labels.html'),
]

# Shown under the feature grid on the home pages.
MORE_FEATURES = [('Coglass on the iPad', 'coglass-ipad.html'), ('Paperwork done for you', 'coglass-feature-paperwork.html'),
                 ('Xero', 'coglass-feature-xero.html'), ('Mobile app', 'coglass-feature-mobile.html')]

# "How a job flows" — the home pages' timeline. (title, text, link)
FLOW = [
    ('Enquiry', 'An email or a call becomes an order — the AI glass scan reads the sizes out of the email for you.', 'coglass-feature-ai-glass-scan.html'),
    ('Survey', 'Measure, draw and photograph every opening on the phone or iPad, even with no signal.', 'coglass-feature-surveys.html'),
    ('Quote', 'Priced from your catalogue with the glass drawn on each line; the customer accepts online.', 'coglass-feature-quoting.html'),
    ('Glass ordered', 'Purchase orders to your supplier from the job, with the drawing on them — or onto your own production board.', 'coglass-feature-suppliers.html'),
    ('Labels', 'A barcode label on every pane; scan it in when the glass arrives and the job shows ready.', 'coglass-feature-glass-labels.html'),
    ('Fitting', 'Booked on the planner, an on-our-way text to the customer, per-pane sign-off and a signature on site.', 'coglass-feature-fitting.html'),
    ('Paid', 'The invoice is drafted when the fitting is signed off; the customer pays online and it goes to Xero.', 'coglass-feature-invoicing.html'),
]


def flow_html(ctx):
    e = ctx['e']
    items = ''.join(f'<li><h3><a href="/{l}">{e(t)}</a></h3><p>{e(x)}</p></li>' for t, x, l in FLOW)
    return f'''<section class="sect" id="how-a-job-flows">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">How a job flows</span><h2>From the first email to the money in the bank</h2><p>One record follows the job the whole way — the office, the van and the workshop all see the same thing.</p></div>
    <ol class="steps flow">{items}</ol>
  </div>
</section>'''


def more_features_html(ctx):
    e = ctx['e']
    links = ''.join(f'<li><a href="/{l}">{e(t)}</a></li>' for t, l in MORE_FEATURES)
    return f'<p class="fine" style="margin:22px 0 10px">Also in Coglass:</p><ul class="related">{links}</ul>'


def legal(ctx, name, path, title, description):
    raw = open(os.path.join(HERE, 'legal', f'{name}.html')).read()
    h1 = re.search(r'<!-- h1: (.*?) -->', raw).group(1)
    intro = re.search(r'<!-- intro: (.*?) -->', raw).group(1)
    body_src = re.sub(r'<!-- (h1|intro): .*? -->\n', '', raw)
    body = f'''<section class="page-head"><div class="wrap"><h1>{h1}</h1><p>{intro}</p></div></section>
<article class="prose">
{body_src}</article>'''
    return ctx['layout'](path=path, title=title, description=description, body=body, current=path)


def demo(ctx):
    e = ctx['e']
    import countries as CS
    country_opts = '<option value="">Choose…</option>' + ''.join(
        f'<option value="{k}">{e(CS.C[k]["name"])}{" (incl. Isle of Man, Channel Islands, Gibraltar)" if k == "uk" else ""}</option>'
        for k in CS.ORDER) + '<option value="other">Somewhere else</option>'
    body = f'''<section class="page-head"><div class="wrap"><h1>Book a demo</h1><p>Tell us a little about your business and we'll call or email to arrange a time — usually the same working day.</p></div></section>
<section class="sect" style="padding-top:44px">
  <div class="wrap two-col">
    <div class="form-card">
      <form id="lead-form">
        <div id="lead-error" class="form-error" role="alert"></div>
        <div class="field"><label for="lead-company">Company name</label><input type="text" id="lead-company" name="company" autocomplete="organization" required></div>
        <div class="field"><label for="lead-name">Your name <span class="hint">(optional)</span></label><input type="text" id="lead-name" name="name" autocomplete="name"></div>
        <div class="field"><label for="lead-country">Country</label><select id="lead-country" name="country" autocomplete="country">{country_opts}</select></div>
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
        <li><h3>You decide</h3><p>If it suits, pick a plan and we'll help you load your products, prices and team.</p></li>
      </ol>
      <p class="fine" style="margin-top:18px">Rather email? <a href="mailto:{ctx['CONTACT']}">{ctx['CONTACT']}</a> · or call <a href="tel:+441215170383">{ctx['PHONE_INTL']}</a> (UK).</p>
      <p class="fine">Want to see prices first? <a href="/pricing/">Pricing for your country</a>.</p>
    </div>
  </div>
</section>'''
    return ctx['layout'](path='/signup.html', title='Book a demo | Coglass', description='Book a demo of Coglass, the software for glass and glazing companies. Tell us about your business and we will be in touch, usually the same working day.',
                         body=body, current='/signup.html', scripts='<script src="/assets/lead-form.js?v=4" defer></script>\n')


def not_found(ctx):
    body = f'''<section class="notfound"><div class="wrap">
  <p class="kicker">Error 404</p>
  <h1>We can't find that page</h1>
  <p style="color:var(--ink2);max-width:520px;margin:0 auto 26px">It may have moved, or the link may be wrong. Try one of these instead.</p>
  <div class="ctas"><a class="btn pri lg" href="/">Go to the home page</a><a class="btn lg" href="/#features">See all features</a><a class="btn lg" href="/pricing/">Pricing</a><a class="btn lg" href="/support/">Help</a></div>
</div></section>'''
    return ctx['layout'](path='/404.html', title='Page not found | Coglass', description='This page could not be found.', body=body, noindex=True)


SITEMAP = [
    ('/signup.html', '0.7', 'monthly'),
    ('/coglass-for-merchants.html', '0.8', 'monthly'), ('/coglass-for-sealed-units.html', '0.8', 'monthly'),
] + [(f'/coglass-feature-{s}.html', '0.7', 'monthly') for s in
     ['orders', 'quoting', 'surveys', 'glass-specs', 'production', 'suppliers', 'scheduling', 'fitting', 'invoicing',
      'communication', 'webshop', 'fleet', 'mobile', 'ai-glass-scan', 'customer-portal', 'tracking', 'glass-labels',
      'paperwork', 'xero']] + [
    ('/coglass-ipad.html', '0.8', 'monthly'),
    ('/support/', '0.5', 'monthly'), ('/terms/', '0.3', 'yearly'), ('/privacy/', '0.3', 'yearly'),
    ('/refunds/', '0.3', 'yearly'), ('/dpa/', '0.3', 'yearly'),
]


def sitemap_xml(site):
    import country_pages
    entries = country_pages.sitemap_entries() + [(p, pr, c, None) for p, pr, c in SITEMAP]
    out = ''
    for p, pr, c, alts in entries:
        links = ''.join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{site}{ap}"/>\n' for h, ap in (alts or []))
        out += (f'  <url>\n    <loc>{site}{p}</loc>\n{links}    <lastmod>{LASTMOD}</lastmod>\n'
                f'    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f'{out}</urlset>\n')


def build(ctx):
    import country_pages
    out = {
        'signup.html': demo(ctx),
        'coglass-ipad.html': ipad(ctx),
        '404.html': not_found(ctx),
        'terms/index.html': legal(ctx, 'terms', '/terms/', 'Terms of Service | Coglass', 'The terms between Halliday Morrow Ltd (Coglass) and businesses that subscribe to Coglass.'),
        'refunds/index.html': legal(ctx, 'refunds', '/refunds/', 'Cancellation & Refunds | Coglass', 'How to cancel Coglass, when access ends, what happens to your data and when we refund.'),
        'privacy/index.html': legal(ctx, 'privacy', '/privacy/', 'Privacy Policy | Coglass', 'How Coglass handles personal data on this website, in subscription accounts and inside the Coglass apps.'),
        'dpa/index.html': legal(ctx, 'dpa', '/dpa/', 'Data Processing Agreement | Coglass', 'The UK GDPR Article 28 terms between Halliday Morrow Ltd and Coglass customers, including the sub-processor list.'),
        'support/index.html': legal(ctx, 'support', '/support/', 'Help & Support | Coglass', 'Help signing in to Coglass, common questions, and how to contact the Coglass team.'),
    }
    out.update(country_pages.build(ctx))
    out['sitemap.xml'] = sitemap_xml(ctx['SITE'])
    out['robots.txt'] = f'User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /og-image.html\n\nSitemap: {ctx["SITE"]}/sitemap.xml\n'
    return out


def ipad(ctx):
    e, I = ctx['e'], ctx['ICON']
    src, alt, w, h = ctx['IMG']['ipad-planner']
    hero = (f'<div class="ipad-frame"><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high"></div>'
            '<p class="cap">The real planner in a browser at iPad landscape size (1180 × 820), on a local demo account with made-up details.</p>')
    checks = lambda xs: '<ul class="checks">' + ''.join(f'<li>{e(x)}</li>' for x in xs) + '</ul>'

    def block(kicker, h2, p, items, visual, link=None, rev=False, alt_bg=False):
        more = f'<a class="btn" href="{link[1]}">{e(link[0])}</a>' if link else ''
        return f'''<section class="sect{" alt" if alt_bg else ""}">
  <div class="wrap split{" rev" if rev else ""}">
    <div class="split-text">
      <span class="kicker">{e(kicker)}</span>
      <h2>{e(h2)}</h2>
      <p>{e(p)}</p>
      {checks(items)}
      {more}
    </div>
    <div>{visual}</div>
  </div>
</section>'''

    office = block('The office', 'The whole office CRM in Safari on the iPad',
                   'Coglass runs in the browser, so the iPad gets the same office system as the desktop — no separate app to learn. Sign in at your own Coglass address and work from the sofa, the showroom or the customer\'s kitchen table.',
                   ['Orders, quotes and the work bench', 'The planner — drag jobs onto people and vans', 'Invoices, payments and the inbox', 'Customers, products, suppliers and settings',
                    'Best in landscape; fold the side menu away for more room'],
                   ctx['shot']('/assets/img/orders.webp', ctx['IMG']['orders'][1], 1600, 867), ('See jobs & orders', '/coglass-feature-orders.html'))
    shop = block('The shop floor', 'The production board on an iPad at the bench',
                 'The shop-floor app is part of the Coglass app on the App Store. Lay it on the bench and the workshop sees every pane that needs making, in the order it needs making.',
                 ['Six lanes: To plan, Waiting supplier, Glass in, In production, Ready, Made', 'Cut list by station, with the glass drawing beside it',
                  'Scan to advance — with the iPad camera or a keyboard-wedge yard scanner', 'Sealed units: “Sealed” stays locked until every pane is ready',
                  'Keeps working when the workshop wifi drops, and catches up after', 'One shared iPad, with a PIN for each person'],
                 ctx['panel']('Shop floor · cut list', [('s', 'Cutting · 4 panes', '0003 · 6mm Toughened Clear · 900 × 1800 × 4'),
                                                         ('f', 'Edgework · 2 panes', '0004 · arrised edges · scan to advance'),
                                                         ('d', 'Sealing · waiting', '0001 · DGU — 1 of 2 panes ready'),
                                                         ('', 'Offline — 3 changes waiting', 'Will sync when the wifi is back')],
                              'Drawn illustration of the shop-floor app.'),
                 ('See production', '/coglass-feature-production.html'), rev=True, alt_bg=True)
    counter = block('The trade counter', 'Quote, sell and sign it out at the counter',
                    'The Counter tab turns the same iPad into a trade-counter till for cut-to-size glass. Pick the product, type the size, add the processes — the price updates as you go.',
                    ['Live pricing from your catalogue as you add sizes and processes', 'Holes and cut-outs drawn on the same drawing editor the fitters use',
                     'Record the sale as cash, card taken or on account — the invoice is raised for you', 'The customer signs for the glass on screen; the signed collection note is emailed to them'],
                    ctx['panel']('Counter · cash sale', [('s', '6mm Toughened Clear · 500 × 700', '2 × · arrised edges · 1 hole Ø 12 mm'),
                                                          ('s', 'Price', 'Updates as you type'),
                                                          ('f', 'Card taken', 'Payment recorded against the invoice'),
                                                          ('', 'Customer signs for it', 'Collection note emailed')],
                                 'Drawn illustration of the Counter tab.'),
                    ('Coglass for merchants', '/coglass-for-merchants.html'))
    site = block('On site', 'Surveys and fittings on the iPad too',
                 'The fitters\' app runs on iPhone, Android phones and the iPad. A bigger screen helps when you are drawing an arched top-light or a run of Georgian bars on the survey.',
                 ['Surveys: shapes drawn to size, photos per opening, GPS and access notes', 'Works with no signal and syncs when you are back in range',
                  'Per-pane fitting sign-off — fitted, partial or not fitted, with photos', 'The customer signs on screen when the job is done'],
                 ctx['big_phone']('Survey · K. Khan', [('s', 'Front bedroom — left', '1200 × 900 · DGU · 2 photos'), ('s', 'Kitchen', '600 × 400 · toughened · cut-out'),
                                                       ('s', 'Access', 'Ladder · first floor'), ('', 'Offline — will sync', '3 openings saved')]),
                 ('See surveys', '/coglass-feature-surveys.html'), rev=True, alt_bg=True)
    manager = block('Manager mode', 'Run the office from the app when you\'re out',
                    'Owners and office managers who sign in to the Coglass app get more than the fitters\' day: the jobs that need you, the inbox, quoting and the planner.',
                    ['Home: new enquiries, quotes waiting, orders to place and money to collect', 'Messages: read and reply to customer emails, or start a new one',
                     'Quote on the work bench and send the quote from the app', 'Move a booking: press and hold it on the planner and drag it to a new time or person',
                     'Record a payment or send a pay-online link'],
                    ctx['big_phone']('Planning · Tue', [('f', '08:00 Gary · Fitting', 'Riverside Offices · hold to move'), ('s', '10:00 Sam · Survey', 'Mrs A. Patel'),
                                                        ('d', '13:00 Dan · Delivery', 'D. Harris'), ('', 'Messages · 2 new', 'Reply by email')]),
                    ('More about the app', '/coglass-feature-mobile.html'))
    apps = ('<div class="ctas"><a class="btn acc lg" href="https://apps.apple.com/app/coglass-glass-glazing-crm/id6761371345" rel="noopener">Download for iPhone &amp; iPad</a>'
            f'<a class="btn lg" href="{ctx["DEMO"]}">Book a demo</a></div>')
    body = f'''<section class="hero">
  <div class="wrap grid">
    <div class="copy">
      <span class="eyebrow">Coglass on the iPad</span>
      <h1>Run your whole glazing business from an iPad</h1>
      <p class="lead">The office in Safari, the production board at the bench, a trade counter, and surveys and fittings on site — one system, on one kind of device, all looking at the same jobs.</p>
      {apps}
      <p class="fine">The app is for staff of companies that use Coglass — you sign in with the login your company gives you.</p>
      {ctx['trust'](['Office, workshop, counter & site', 'Works offline in the workshop and on site', 'Every feature on every plan'])}
    </div>
    <div class="visual">{hero}</div>
  </div>
</section>
<section class="strip" aria-label="Four places, one iPad">
  <div class="wrap"><ul><li><b>Office</b>quotes, planner, invoices</li><li><b>Shop floor</b>board, cut list, scanning</li><li><b>Counter</b>price, sell, sign out</li><li><b>On site</b>survey, fit, sign off</li></ul></div>
</section>
{office}
{shop}
{counter}
{site}
{manager}
<section class="sect alt">
  <div class="wrap">
    <h2 style="font-size:22px">More of Coglass</h2>
    <ul class="related">{''.join(f'<li><a href="/{s}.html">{e(n)}</a></li>' for s, n in ctx['RELATED'] if s != 'coglass-ipad')}</ul>
  </div>
</section>
{ctx['cta_band']('See it on an iPad', 'Book a demo and we will show you the office, the shop floor and the counter on the kind of jobs you do.')}'''
    return ctx['layout'](path='/coglass-ipad.html', title='Glazing Software for iPad | Office, Shop Floor, Counter & Site | Coglass',
                         description='Run your glazing business from an iPad: the Coglass office CRM in Safari, the shop-floor production board, a trade counter with live pricing, and surveys and fittings on site.',
                         body=body, current='/coglass-ipad.html', og_title='Run your whole glazing business from an iPad')
