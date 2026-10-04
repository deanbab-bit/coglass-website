#!/usr/bin/env python3
"""Builds the static Coglass sales site.

    python3 _src/build.py

Writes every page into the repo root (index.html, coglass-feature-*.html, pricing/index.html, …)
from one layout, so the header, footer, meta tags and styles can't drift between pages.

  _src/content/*.json   feature / audience page copy (one file per page)
  _src/pages.py         home, pricing, legal, support, demo-request and 404 bodies
  assets/site.css       the shared stylesheet (all pages)

Edit those, re-run this script, commit the generated HTML with them. The output is plain
static HTML — nginx serves it as-is, nothing runs at request time.
"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
sys.path.insert(0, SRC)
from icons import ICON  # noqa: E402
import pages  # noqa: E402

# The main international site. coglass.co.uk forwards page-for-page to it (nginx.conf).
SITE = 'https://coglass.net'
CONTACT = 'contact@coglass.co.uk'
PHONE = '0121 517 0383'
DEMO = '/signup.html'
TRIAL = '/pricing/#plans'
SIGN_IN = 'https://accounts.coglass.co.uk'
ASSET_V = '5'
PHONE_INTL = '+44 121 517 0383'
e = html.escape

LOGO_SVG = ('<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" rx="14" fill="#123447"/>'
            '<rect x="9" y="9" width="46" height="46" rx="9" fill="none" stroke="#3fa9d6" stroke-width="4.5"/>'
            '<path d="M32 11V53M11 32H53" stroke="#3fa9d6" stroke-width="4.5" stroke-linecap="round"/></svg>')

NAV = [('Features', '/#features'), ('For merchants', '/coglass-for-merchants.html'),
       ('Sealed units', '/coglass-for-sealed-units.html'), ('Mobile app', '/coglass-feature-mobile.html'),
       ('Pricing', '/pricing/'), ('Help', '/support/')]


def nav_for(country):
    if not country:
        return NAV
    s = country['slug']
    return [('Features', f'/{s}/#features'), ('For merchants', '/coglass-for-merchants.html'),
            ('Mobile app', '/coglass-feature-mobile.html'),
            ('Pricing', f'/{s}/pricing/'), ('FAQ', f'/{s}/faq/'), ('Help', '/support/')]


def demo_href(country):
    return f'{DEMO}?country={country["slug"]}' if country else DEMO


def header(current, country=None):
    links = ''.join(
        f'<a href="{href}"{" aria-current=page" if href == current else ""}>{e(t)}</a>' for t, href in nav_for(country))
    home = f'/{country["slug"]}/' if country else '/'
    cty = (f'<a class="cty" href="/#countries"><span class="sr-only">Country: </span>{e(country["short"])}'
           f'<span class="sr-only"> (change country)</span></a>') if country else \
          '<a class="cty" href="/#countries">Country</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="{home}" aria-label="Coglass home">{LOGO_SVG}<span>COGLASS</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <svg class="bars" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      <svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
    <div class="head-ctas">
      {cty}
      <a class="btn" href="{SIGN_IN}">Sign in</a>
      <a class="btn pri" href="{demo_href(country)}">Book a demo</a>
    </div>
  </div>
</header>'''


def footer(country=None):
    import countries as _cs
    uk = (not country) or country['key'] == 'uk'
    phone_txt, phone_tel = (PHONE, '01215170383') if uk else (PHONE_INTL, '+441215170383')
    clinks = ' · '.join(f'<a href="/{k}/"{" aria-current=page" if country and country["key"] == k else ""}>{_cs.C[k]["name"]}</a>'
                        for k in _cs.ORDER)
    pricing = f'/{country["slug"]}/pricing/' if country else '/pricing/'
    return f'''<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/" aria-label="Coglass home">{LOGO_SVG}<span>COGLASS</span></a>
        <p style="margin:12px 0 0;max-width:340px">Software for glass and glazing companies — quotes, surveys, production, fitting and invoicing in one system. Made in the UK.</p>
      </div>
      <div>
        <h2>Product</h2>
        <ul>
          <li><a href="/#features">All features</a></li>
          <li><a href="{pricing}">Pricing</a></li>
          <li><a href="/coglass-feature-mobile.html">Mobile app</a></li>
          <li><a href="/coglass-feature-webshop.html">Webshop</a></li>
          <li><a href="/coglass-for-merchants.html">For glass merchants</a></li>
          <li><a href="/coglass-for-sealed-units.html">For sealed unit makers</a></li>
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li><a href="{demo_href(country)}">Book a demo</a></li>
          <li><a href="mailto:{CONTACT}">{CONTACT}</a></li>
          <li><a href="tel:{phone_tel}">{phone_txt}</a></li>
          <li><a href="/support/">Help &amp; support</a></li>
          <li><a href="{SIGN_IN}">Sign in to your account</a></li>
        </ul>
      </div>
      <div>
        <h2>Legal</h2>
        <ul>
          <li><a href="/terms/">Terms of Service</a></li>
          <li><a href="/privacy/">Privacy Policy</a></li>
          <li><a href="/refunds/">Cancellation &amp; refunds</a></li>
          <li><a href="/dpa/">Data Processing Agreement</a></li>
        </ul>
      </div>
    </div>
    <p class="countries"><span>Coglass in:</span> {clinks}. The UK site also covers the Isle of Man, Jersey, Guernsey and Gibraltar.</p>
    <div class="legal">Coglass is a product of Halliday Morrow Ltd, registered in England &amp; Wales, company no. 17358542 · VAT no. 526 4805 84 · Registered office: 39a The Riddings, Sutton Coldfield, England, B76 1RW. © 2026 Halliday Morrow Ltd.</div>
  </div>
</footer>'''


def layout(*, path, title, description, body, current=None, og_title=None, jsonld=None, scripts='', noindex=False,
           lang='en-GB', og_locale='en_GB', alternates=None, country=None):
    url = SITE + path
    alt = ''.join(f'<link rel="alternate" hreflang="{h}" href="{SITE}{p}">\n' for h, p in (alternates or []))
    og_t = og_title or title
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n' if jsonld else ''
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    canonical = '' if noindex else f'<link rel="canonical" href="{url}">\n'
    return f'''<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{robots}{canonical}{alt}<meta property="og:type" content="website">
<meta property="og:site_name" content="Coglass">
<meta property="og:title" content="{e(og_t)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{og_locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_t)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#123447">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;family=Raleway:wght@700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
{ld}</head>
<body>
{header(current, country)}
<div class="suggest" id="cty-suggest" data-current="{country['key'] if country else ''}" hidden></div>
<main id="main">
{body}
</main>
{footer(country)}
<script src="/assets/site.js?v={ASSET_V}" defer></script>
{scripts}</body>
</html>
'''


# ---------------------------------------------------------------- shared bits
def trust(items):
    tick = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg>'
    return '<ul class="trust">' + ''.join(f'<li>{tick}{e(t)}</li>' for t in items) + '</ul>'


def shot(src, alt, w, h, bar=True):
    b = '<div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>' if bar else ''
    return f'<div class="shot">{b}<img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>'


def cta_band(h, p):
    return f'''<section class="cta-band">
  <div class="wrap">
    <h2>{e(h)}</h2>
    <p>{e(p)}</p>
    <div class="ctas"><a class="btn acc lg" href="{DEMO}">Book a demo</a><a class="btn ghost-light lg" href="{TRIAL}">See plans and start a trial</a></div>
  </div>
</section>'''


def phone(title, rows):
    rs = ''.join(f'<div class="pc {c}"><b>{e(a)}</b>{e(b)}</div>' for c, a, b in rows)
    return f'<div class="phone" aria-hidden="true"><div class="scr"><p class="t">{e(title)}</p>{rs}</div></div>'


def panel(title, rows, note=''):
    """A drawn app panel in the app's style, for features with no real screenshot yet."""
    rs = ''.join(
        f'<div class="pc {c}" style="font-size:13px;padding:10px 12px;margin-bottom:8px"><b style="font-size:14px">{e(a)}</b>{e(b)}</div>'
        for c, a, b in rows)
    n = f'<p class="cap">{e(note)}</p>' if note else ''
    return (f'<div class="shot" role="img" aria-label="{e(title)}"><div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<div style="background:var(--bg);padding:18px 18px 10px"><p style="font-weight:800;color:var(--navy);margin:0 0 12px">{e(title)}</p>{rs}</div></div>{n}')


# Real screenshots (from a local demo instance with made-up data) where we have one,
# otherwise a drawn panel in the app's style.
IMG = {
    'planning': ('/assets/img/planning.webp', 'The Coglass planning board: a day of fittings, surveys and a delivery booked across two fitters and a surveyor', 1600, 867),
    'production': ('/assets/img/production.webp', 'The production board with lanes from To plan to Made', 1600, 867),
    'orders': ('/assets/img/orders.webp', 'The Orders list with status, job type and amount owed for each job', 1600, 867),
    'bench': ('/assets/img/bench-drawing.webp', 'An arched double-glazed unit on the work bench, drawn with Georgian bars and two drilled holes', 1400, 638),
    'vehicles': ('/assets/img/vehicles.webp', 'The vehicles list with MOT due dates', 1400, 245),
    'quote': ('/assets/img/quote-pdf.webp', 'A quotation PDF with the arched unit drawn on its line', 900, 855),
    'invoice': ('/assets/img/invoice-pdf.webp', 'An invoice PDF with totals and balance due', 900, 643),
}

FEATURE_VISUAL = {
    'coglass-feature-orders': ('img', 'orders'),
    'coglass-feature-quoting': ('img', 'quote'),
    'coglass-feature-invoicing': ('img', 'invoice'),
    'coglass-feature-scheduling': ('img', 'planning'),
    'coglass-feature-production': ('img', 'production'),
    'coglass-feature-glass-specs': ('img', 'bench'),
    'coglass-feature-fleet': ('img', 'vehicles'),
    'coglass-for-merchants': ('img', 'production'),
    'coglass-for-sealed-units': ('img', 'quote'),
    'coglass-feature-communication': ('panel', 'Inbox', [
        ('s', 'Mrs A. Patel · Email', '“Could you quote for the two misted units in the bay?” — linked to order #0002'),
        ('f', 'Order #0001 · SMS sent', 'Booking confirmed for Monday 8am — sent from your company name.'),
        ('d', 'D. Harris · Quote page chat', '“Is the arched top-light toughened?”'),
    ], 'Drawn illustration of the inbox.'),
    'coglass-feature-suppliers': ('panel', 'Supplier orders', [
        ('s', '0008-1 · Purchase order', 'DGU 4-16-4 arched, Georgian 3×2 · Expected Thu'),
        ('d', '0009-1 · Overdue — chased once', '12 × DGU 4-20-4 Low-E Argon'),
        ('f', '0005-1 · Received', '2 × DGU obscure · into Glass in'),
    ], 'Drawn illustration of the supplier orders list.'),
    'coglass-feature-webshop': ('panel', 'Your webshop', [
        ('s', 'DGU 4-16-4 Clear', 'Enter your sizes · price updates as you type'),
        ('f', '6mm Toughened Clear', 'Trade price applied for logged-in accounts'),
        ('d', 'Checkout', 'Pay by card, PayPal, or send as an enquiry'),
    ], 'Drawn illustration of a webshop.'),
    'coglass-feature-surveys': ('phone', 'Survey · Mr K. Khan', [
        ('s', 'Front bedroom — left', '1200 × 900 · DGU · 2 photos'),
        ('s', 'Kitchen', '600 × 400 · toughened · cut-out'),
        ('s', 'Access', 'Ladder · first floor'),
        ('', 'Offline — will sync', '3 openings saved'),
    ]),
    'coglass-feature-fitting': ('phone', 'Fitting · Northgate School', [
        ('f', 'Classroom 1 — left', 'Fitted · 2 photos'),
        ('f', 'Classroom 1 — right', 'Fitted'),
        ('d', 'Corridor', 'Not fitted · broken — re-order'),
        ('', 'Customer signature', 'Signed 11:42'),
    ]),
    'coglass-feature-mobile': ('phone', 'Today · Gary', [
        ('f', '08:00 Northgate School', 'Fitting · 1h 30m'),
        ('s', '10:30 Patel', 'Survey · 45m'),
        ('f', '13:00 Riverside Offices', 'Fitting · 2h'),
        ('', 'Clocked in 07:42', 'Van NV21 GLZ'),
    ]),
}

RELATED = [
    ('coglass-feature-orders', 'Jobs & orders'), ('coglass-feature-quoting', 'Quoting'),
    ('coglass-feature-surveys', 'Surveys'), ('coglass-feature-glass-specs', 'Glass specs'),
    ('coglass-feature-production', 'Production'), ('coglass-feature-suppliers', 'Suppliers'),
    ('coglass-feature-scheduling', 'Scheduling'), ('coglass-feature-fitting', 'Fitting & delivery'),
    ('coglass-feature-invoicing', 'Invoicing'), ('coglass-feature-communication', 'Customer messages'),
    ('coglass-feature-webshop', 'Webshop'), ('coglass-feature-fleet', 'Fleet'),
    ('coglass-feature-mobile', 'Mobile app'),
]


def visual_html(slug):
    v = FEATURE_VISUAL[slug]
    if v[0] == 'img':
        src, alt, w, h = IMG[v[1]]
        return shot(src, alt, w, h)
    if v[0] == 'panel':
        return panel(v[1], v[2], v[3])
    return big_phone(v[1], v[2])


def big_phone(title, rows_data):
    rows = ''.join(f'<div class="pc {c}" style="font-size:13px;padding:10px 12px;margin-bottom:8px"><b style="font-size:14px">{e(a)}</b>{e(b)}</div>' for c, a, b in rows_data)
    return (f'<div role="img" aria-label="{e(title)} on the Coglass phone app (drawn illustration)" style="max-width:300px;margin:0 auto 40px;border-radius:36px;background:#0d1b22;padding:10px;box-shadow:0 18px 40px rgba(0,0,0,.25)">'
            f'<div style="background:var(--bg);border-radius:28px;padding:22px 14px 26px"><p style="font-weight:800;color:var(--navy);margin:0 0 12px">{e(title)}</p>{rows}</div></div>')


def feature_page(slug, d):
    eyebrow = d['eyebrow'].replace('Feature — ', '')
    h1 = e(d['h1']) + (f' <span style="color:var(--accent)">{e(d["h1_accent"])}</span>' if d['h1_accent'] else '')
    if slug == 'coglass-feature-mobile':
        ctas = ('<a class="btn acc lg" href="https://apps.apple.com/app/coglass-glass-glazing-crm/id6761371345" rel="noopener">Download for iPhone &amp; iPad</a>'
                '<a class="btn lg" href="https://play.google.com/store/apps/details?id=com.coglass.app" rel="noopener">Get it on Google Play</a>')
        note = '<p class="fine">The app is for staff of companies that use Coglass — you sign in with the login your company gives you.</p>'
    else:
        ctas = f'<a class="btn acc lg" href="{DEMO}">Book a demo</a><a class="btn lg" href="{TRIAL}">Start a 14-day trial</a>'
        note = ''
    steps = ''.join(f'<li><h3>{e(t)}</h3><p>{e(x)}</p></li>' for t, x in d['steps'])
    incl = ''
    for t, x in d['included']:
        if '— coming soon' in t:
            t = e(t.replace(' — coming soon', '')) + ' <span class="soon">Coming soon</span>'
        else:
            t = e(t)
        incl += f'<li><strong>{t}</strong>{e(x)}</li>'
    rel = ''.join(f'<li><a href="/{s}.html">{e(n)}</a></li>' for s, n in RELATED if s != slug)
    body = f'''<section class="hero">
  <div class="wrap grid">
    <div class="copy">
      <span class="eyebrow">{e(eyebrow)}</span>
      <h1>{h1}</h1>
      <p class="lead">{e(d['lead'])}</p>
      <div class="ctas">{ctas}</div>
      {note}
      {trust(['14-day trial', 'iPhone, Android & web', 'Every feature on every plan'])}
    </div>
    <div class="visual">{visual_html(slug)}</div>
  </div>
</section>
<section class="sect">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">{e(d['steps_label'])}</span><h2>{e(d['steps_h2'])}</h2><p>{e(d['steps_sub'])}</p></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>
<section class="sect alt">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">{e(d['inc_label'])}</span><h2>{e(d['inc_h2'])}</h2><p>{e(d['inc_sub'])}</p></div>
    <ul class="incl">{incl}</ul>
  </div>
</section>
<section class="sect">
  <div class="wrap">
    <h2 style="font-size:22px">More of Coglass</h2>
    <ul class="related">{rel}</ul>
  </div>
</section>
{cta_band(d['cta_h2'], d['cta_p'])}'''
    title = d['title']
    return layout(path=f'/{slug}.html', title=title, description=d['description'], body=body,
                  current=f'/{slug}.html', og_title=title.split(' | ')[0])


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as fh:
        fh.write(content)
    print('wrote', rel)


def main():
    ctx = dict(big_phone=big_phone, layout=layout, e=e, trust=trust, shot=shot, cta_band=cta_band, phone=phone, panel=panel, IMG=IMG,
               ICON=ICON, DEMO=DEMO, TRIAL=TRIAL, SIGN_IN=SIGN_IN, CONTACT=CONTACT, PHONE=PHONE, PHONE_INTL=PHONE_INTL, SITE=SITE,
               demo_href=demo_href)
    cdir = os.path.join(SRC, 'content')
    for f in sorted(os.listdir(cdir)):
        slug = f[:-5]
        write(f'{slug}.html', feature_page(slug, json.load(open(os.path.join(cdir, f)))))
    for rel, html_ in pages.build(ctx).items():
        write(rel, html_)


if __name__ == '__main__':
    main()
