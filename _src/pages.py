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
    ('fleet', 'Fleet', 'Vans on the planner, MOT dates and reminders, and the paperwork with the vehicle.', ['Daily van per person', 'MOT history and certificates', 'Reminders before the MOT is due'], 'coglass-feature-fleet.html'),
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
      'communication', 'webshop', 'fleet', 'mobile']] + [
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
