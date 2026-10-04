"""Country sections (/uk/, /ie/, …), the global home / country chooser (/) and the pricing chooser (/pricing/).

Every country has three pages — home, pricing, FAQ — each carrying the full hreflang cluster.
Copy lives in countries.py; the launch-day CTA switch is countries.SUBSCRIBE.
"""
import countries as CS
import local_guides as LG
import pages
from countries import C, ORDER, PLAN_LINES, PLAN_NAMES

ORG_ID = 'https://coglass.net/#org'
SIGNUP_URL = 'https://accounts.coglass.co.uk/subscribe'

KIND_PATH = {'home': '', 'pricing': 'pricing/', 'faq': 'faq/'}
X_DEFAULT = {'home': '/', 'pricing': '/pricing/', 'faq': '/'}


def cpath(c, kind):
    return f'/{c["slug"]}/{KIND_PATH[kind]}'


def alternates(kind):
    out = []
    for k in ORDER:
        for h in C[k]['hreflang']:
            out.append((h, cpath(C[k], kind)))
    out.append(('x-default', X_DEFAULT[kind]))
    return out


def org(site):
    return {'@type': 'Organization', '@id': ORG_ID, 'name': 'Coglass', 'legalName': 'Halliday Morrow Ltd',
            'url': f'{site}/', 'logo': f'{site}/assets/img/coglass-icon-512.png',
            'email': 'contact@coglass.co.uk', 'telephone': '+44 121 517 0383',
            'areaServed': [C[k]['code'] for k in ORDER] + ['IM', 'JE', 'GG', 'GI']}


def offers(site, c):
    return [{'@type': 'Offer', 'name': f'Coglass {n}', 'price': str(c['num'][k]), 'priceCurrency': c['currency'],
             'url': f'{site}{cpath(c, "pricing")}#plans',
             'eligibleRegion': [{'@type': 'Country', 'name': h.split('-')[1]} for h in c['hreflang']],
             'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': str(c['num'][k]), 'priceCurrency': c['currency'],
                                    'unitText': 'MONTH', 'valueAddedTaxIncluded': False}}
            for n, k, _ in PLAN_NAMES]


def software(site, url, offer_list):
    return {'@type': 'SoftwareApplication', 'name': 'Coglass', 'applicationCategory': 'BusinessApplication',
            'operatingSystem': 'iOS, Android, Web', 'url': url, 'publisher': {'@id': ORG_ID}, 'offers': offer_list}


def plan_cta(ctx, c, k, n):
    if c['subscribe']:
        q = f'?plan={k}' + ('' if c['key'] == 'uk' else f'&country={c["slug"]}')
        return f'{SIGNUP_URL}{q}', f'Start 14-day trial<span class="sr-only"> on {n}</span>'
    return f'{ctx["DEMO"]}?country={c["slug"]}&plan={k}', f'Book a demo<span class="sr-only"> for {n}</span>'


def plans_html(ctx, c, full=True):
    e = ctx['e']
    out = ''
    for n, k, pop in PLAN_NAMES:
        lines = PLAN_LINES[k] if full else PLAN_LINES[k][:4]
        if full:
            href, label = plan_cta(ctx, c, k, n)
        else:
            href, label = f'{cpath(c, "pricing")}#plans', f'See the {n} plan'
        out += (f'<div class="plan{" pop" if pop else ""}">{"<span class=tag>Most popular</span>" if pop else ""}<h3>{n}</h3>'
                f'<p class="pr">{c["prices"][k]}</p><p class="per">{c["per"]}</p>'
                f'<ul>{"".join(f"<li>{e(x)}</li>" for x in lines)}</ul>'
                f'<a class="btn{" acc" if pop else ""} block" href="{href}">{label}</a></div>')
    return out


def hero_ctas(ctx, c):
    demo = f'<a class="btn acc lg" href="{ctx["demo_href"](c)}">Book a demo</a>'
    if c['subscribe']:
        return demo + f'<a class="btn lg" href="{cpath(c, "pricing")}#plans">Start a 14-day trial</a>'
    return demo + f'<a class="btn lg" href="{cpath(c, "pricing")}">See {c["short"]} pricing</a>'


def cta_band(ctx, c, h, p):
    e = ctx['e']
    second = (f'<a class="btn ghost-light lg" href="{cpath(c, "pricing")}#plans">See plans and start a trial</a>' if c['subscribe']
              else f'<a class="btn ghost-light lg" href="{cpath(c, "pricing")}">See pricing</a>')
    return f'''<section class="cta-band">
  <div class="wrap">
    <h2>{e(h)}</h2>
    <p>{e(p)}</p>
    <div class="ctas"><a class="btn acc lg" href="{ctx["demo_href"](c)}">Book a demo</a>{second}</div>
  </div>
</section>'''


def other_countries(c, kind, label):
    links = ' · '.join(f'<a href="{cpath(C[k], kind)}" data-country="{k}">{C[k]["name"]}</a>' for k in ORDER if k != c['key'])
    return f'<p class="fine other-cty">{label} {links}</p>'


def local_features(ctx, c):
    """The feature grid, minus things that only fit the UK today."""
    e, I = ctx['e'], ctx['ICON']
    out = ''
    for i, t, x, bs, l in pages.FEATURES:
        if c['key'] not in ('uk', 'global') and i in ('webshop', 'fleet'):
            continue  # webshop delivery coverage and MOT reminders are UK-only today
        if i == 'invoice':
            x = f'Deposit, proforma and final invoices with {c["tax"]}, payments recorded, and Xero.'
            bs = ['Overdue invoices flagged', f'{c["tax"]} on every invoice', 'Invoices and payments push to Xero']
        if i == 'chat':
            bs = (['Gmail and Outlook inbox', 'SMS under your company name', CS.wa('WhatsApp and Messenger', 'Messenger and WhatsApp coming soon')]
                  if c['key'] == 'uk' else ['Gmail and Outlook inbox', 'SMS and email updates', CS.wa('WhatsApp messages', 'WhatsApp coming soon')])
        out += (f'<li class="fcard">{I[i]}<h3>{e(t)}</h3><p>{e(x)}</p><ul>{"".join(f"<li>{e(b)}</li>" for b in bs)}</ul>'
                f'<a class="more" href="/{l}">{e(t)} in detail<span aria-hidden="true">&nbsp;→</span></a></li>')
    return out


def faq_html(ctx, items):
    e = ctx['e']
    return ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items)


def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


# ---------------------------------------------------------------------------- country home
def country_home(ctx, c):
    e, site = ctx['e'], ctx['SITE']
    src, alt, w, h = ctx['IMG']['planning']
    hero_img = f'<div class="shot"><div class="bar" aria-hidden="true"><i></i><i></i><i></i></div><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high"></div>'
    img = lambda k: f'<div class="framed"><img src="{ctx["IMG"][k][0]}" alt="{e(ctx["IMG"][k][1])}" width="{ctx["IMG"][k][2]}" height="{ctx["IMG"][k][3]}" loading="lazy" decoding="async"></div>'
    proof = ''.join(f'<li><b>{e(a)}</b>{e(b)}</li>' for a, b in c['proof'])
    why = ''.join(f'<li class="tile"><h3>{e(t)}</h3><p>{e(x)}</p></li>' for t, x in c['why'])
    trust_items = ['Phone, iPad & web apps', 'Xero connected', 'No setup fee'] if c['key'] == 'uk' else \
        ['Phone, iPad & web apps', f'Priced in {c["currency"]}', f'UK-based team supporting {c["in_name"]}']
    crown = ''
    if c.get('crown'):
        crown = ('<p class="fine" style="margin-top:14px">Also covers the Isle of Man, Jersey, Guernsey and Gibraltar — '
                 f'<a href="{cpath(c, "pricing")}#crown">how VAT works there</a>.</p>')
    faq_items = c['faq'][:4]
    body = f'''<section class="hero">
  <div class="wrap grid">
    <div class="copy">
      <span class="eyebrow">{c['eyebrow']}</span>
      <h1>{e(c['h1'])}</h1>
      <p class="lead">{e(c['lead'])}</p>
      <div class="ctas">{hero_ctas(ctx, c)}</div>
      {ctx['trust'](trust_items)}{crown}
    </div>
    <div class="visual">{hero_img}{ctx['phone']('Today · Gary', [('f', '08:00 Fitting', 'School · 1h 30m'), ('s', '10:30 Survey', 'Kitchen + bay · 45m'), ('f', '13:00 Fitting', 'Offices · 2h')])}</div>
  </div>
</section>
<section class="strip" aria-label="At a glance">
  <div class="wrap"><ul>{proof}</ul></div>
</section>
<section class="sect">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Coglass in {e(c['in_name'])}</span><h2>{e(c['why_h2'])}</h2><p>{e(c['support'])}</p></div>
    <ul class="tiles why" style="list-style:none;padding:0;margin:0">{why}</ul>
  </div>
</section>
<section class="sect alt">
  <div class="wrap split">
    <div class="split-text">
      <span class="kicker">The work bench</span>
      <h2>Draw it once. Quote it, order it, make it.</h2>
      <p>Each pane is drawn to size in mm with its shape, holes, cut-outs, Georgian bars or leaded lights. The same drawing prices the line, goes on the quote, the supplier's purchase order and the workshop's cutting sheet.</p>
      <ul class="checks"><li>Full double- and triple-glazed unit make-ups, cavity set per line</li><li>Edgework, toughening, laminating — in-house or bought in</li><li>Trade price lists and quantity breaks applied automatically</li></ul>
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
      <ul class="checks"><li>Barcode labels for every pane</li><li>Sealed-unit steps checked pane by pane</li><li>Keeps working when the workshop wifi drops</li></ul>
      <a class="btn" href="/coglass-feature-production.html">See production</a>
    </div>
    {img('production')}
  </div>
</section>
<section class="sect alt">
  <div class="wrap split">
    <div class="split-text">
      <span class="kicker">Coglass on the iPad</span>
      <h2>Run the whole business from an iPad</h2>
      <p>The office CRM in Safari, the production board at the bench, a trade counter with live pricing, and surveys and fittings on site — all on the same jobs.</p>
      <ul class="checks"><li>Quotes, the planner and invoices in the browser</li><li>Cut list, scan to advance and sealed-unit steps in the workshop</li><li>Counter sales signed for on screen</li></ul>
      <a class="btn" href="/coglass-ipad.html">Coglass on the iPad</a>
    </div>
    <div class="ipad-frame"><img src="{ctx['IMG']['ipad-planner'][0]}" alt="{e(ctx['IMG']['ipad-planner'][1])}" width="1600" height="1112" loading="lazy" decoding="async"></div>
  </div>
</section>
<section class="sect alt" id="features">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Everything in Coglass</span><h2>From the first enquiry to the final payment</h2><p>Every plan includes all of it. Plans differ by how many people use Coglass and how much you put through it.</p></div>
    <ul class="fgrid" style="list-style:none;padding:0;margin:0">{local_features(ctx, c)}</ul>
    {pages.more_features_html(ctx)}
  </div>
</section>
{pages.flow_html(ctx)}
<section class="sect">
  <div class="wrap split">
    <div class="split-text">
      <span class="kicker">For the team on the road</span>
      <h2>The phone app your fitters will actually use</h2>
      <p>Today's jobs, surveys drawn on the phone, per-pane sign-off with photos and a signature, clock in and out — and it keeps working with no signal.</p>
      <div class="ctas">
        <a class="btn acc" href="https://apps.apple.com/app/coglass-glass-glazing-crm/id6761371345" rel="noopener">Download for iPhone &amp; iPad</a>
        <a class="btn" href="https://play.google.com/store/apps/details?id=com.coglass.app" rel="noopener">Get it on Google Play</a>
      </div>
      <p class="fine">Staff sign in with the login their company gives them. <a href="/coglass-feature-mobile.html">More about the app</a>.</p>
    </div>
    {ctx['big_phone']('Fitting · Northgate School', [('f', 'Classroom 1 — left', 'Fitted · 2 photos'), ('f', 'Classroom 1 — right', 'Fitted'), ('d', 'Corridor', 'Not fitted · broken — re-order'), ('', 'Customer signature', 'Signed 11:42')])}
  </div>
</section>
<section class="sect alt">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Pricing in {e(c['in_name'])}</span><h2>Simple monthly plans in {e(c['currency'])}</h2><p>Every plan includes the web app, the phone app for fitters and the shop-floor iPad app. Prices exclude {e(c['tax'])}. No setup fee, no minimum term.</p></div>
    <div class="plans">{plans_html(ctx, c, full=False)}</div>
  </div>
</section>
{LG.guides_section(ctx, c)}<section class="sect">
  <div class="wrap" style="max-width:860px">
    <div class="sect-head"><span class="kicker">Questions</span><h2>Coglass in {e(c['in_name'])}: common questions</h2></div>
    <div class="faq">{faq_html(ctx, faq_items)}</div>
    <p style="margin-top:18px"><a href="{cpath(c, 'faq')}">All questions about Coglass in {e(c['in_name'])} →</a></p>
    {other_countries(c, 'home', 'Coglass in other countries:')}
  </div>
</section>
{cta_band(ctx, c, 'See it on your own kind of jobs', 'Book a demo and we will walk you through Coglass with the glass you sell and the way you work.')}'''
    url = site + cpath(c, 'home')
    jsonld = {'@context': 'https://schema.org', '@graph': [org(site), software(site, url, offers(site, c))]}
    return ctx['layout'](path=cpath(c, 'home'), title=c['title'], description=c['description'], body=body,
                         current=cpath(c, 'home'), og_title=c['title'].split(' | ')[0] + ' — every glass job, from enquiry to paid',
                         jsonld=jsonld, lang=c['lang'], og_locale=c['og_locale'], alternates=alternates('home'), country=c)


# ---------------------------------------------------------------------------- country pricing
def country_pricing(ctx, c):
    e, site = ctx['e'], ctx['SITE']
    CONTACT = ctx['CONTACT']
    if c['subscribe']:
        start = ('<div class="note"><strong>How the trial works.</strong> Your first 14 days are free. We take your card when you start and '
                 'charge nothing until the trial ends — cancel before then and you pay nothing. We email you before the first payment. '
                 "During the trial every feature is switched on with no limits; your plan's limits apply from the first payment.</div>")
        start += f'<p>Prefer to talk first, or want us to set it up with you? <a href="{ctx["demo_href"](c)}">Book a demo</a>.</p>'
    else:
        start = (f'<div class="note"><strong>How to start.</strong> Book a demo and we will show you Coglass on the kind of jobs you do, '
                 f'then set your account up with you — your products, prices and team. You are billed monthly in {e(c["currency"])} '
                 'from the day your account goes live.</div>')
    tax = ''.join(f'<p>{e(t)}</p>' for t in c['tax_notes'])
    crown = ''
    if c.get('crown'):
        rows = ''.join(f'<tr><th scope="row">{e(n)}</th><td>{e(t)}</td></tr>' for n, t in c['crown'])
        crown = f'''<h2 id="crown">Isle of Man, Jersey, Guernsey and Gibraltar</h2>
    <p>Businesses in the Crown Dependencies and Gibraltar use the UK site and pay the UK prices in pounds.</p>
    <div class="table-wrap"><table>
      <tr><th scope="col">Where</th><th scope="col">VAT on your Coglass subscription</th></tr>
      {rows}
    </table></div>
    <p class="fine">This is how we bill you, not tax advice for your own business.</p>'''
    sms = f'<p class="fine">{e(c["sms_note"])}</p>' if c.get('sms_note') else ''
    tz = f'<p>{e(c["support"])}</p>'
    body = f'''<section class="page-head"><div class="wrap"><h1>Coglass pricing in {e(c['in_name'])}</h1><p>Everything in Coglass on every plan, priced in {e(c['currency'])} by the size of your team. Prices exclude {e(c['tax'])}. Last updated: October 2026.</p></div></section>
<section class="sect" style="padding-top:44px">
  <div class="wrap">
    <p style="max-width:780px;color:var(--ink2)">All plans include the full system — orders and quoting, surveys, the work bench, production, supplier orders, scheduling, invoicing, the phone app for fitters, the shop-floor iPad app and the customer portal. Plans differ by how many people use Coglass and how much you put through it, not by which features you get.</p>
    <h2 class="sr-only">Plans</h2>
    <div class="plans" id="plans">{plans_html(ctx, c)}</div>
    {start}
    {other_countries(c, 'pricing', 'Prices for another country:')}
  </div>
</section>
<section class="sect alt">
  <div class="wrap" style="max-width:900px">
    <h2>Extras</h2>
    <p>Need more than your plan includes? Email <a href="mailto:{CONTACT}">{CONTACT}</a> and we'll add it to your subscription — you can't yet buy extras yourself from your account.</p>
    <div class="table-wrap"><table>
      <tr><th scope="col">Extra</th><th scope="col">Price</th></tr>
      <tr><td>Additional shared email inbox</td><td>{c['inbox']} a month + {e(c['tax'])}</td></tr>
      <tr><td>Additional office login (comes with its own inbox)</td><td>Ask us</td></tr>
      <tr><td>Additional fitter on the phone app</td><td>Ask us</td></tr>
      <tr><td>More SMS credit</td><td>Ask us — bought in advance, never billed in arrears</td></tr>
      <tr><td>The app in your own branding (iPhone/Android)</td><td>Ask us</td></tr>
    </table></div>
    {sms}
    <h2>If you reach a limit</h2>
    <div class="table-wrap"><table>
      <tr><th scope="col">When you reach…</th><th scope="col">What happens</th></tr>
      <tr><td>Your monthly orders</td><td>Nothing stops. You keep working, we let you know you are close, and you can move up a plan whenever it works out cheaper.</td></tr>
      <tr><td>Your office logins or fitters</td><td>The next person can't sign in until a place is free, or until we add another login to your plan.</td></tr>
      <tr><td>Your SMS allowance</td><td>Texts pause until the next month's allowance or until more credit is added. Email us and we'll add it.</td></tr>
      <tr><td>AI glass scans</td><td>There is no limit on any plan.</td></tr>
    </table></div>
    <h2>Billing</h2>
    <p>Plans are billed monthly in advance in {e(c['currency'])}, and you pay by card. They roll on month to month — no minimum term and no setup fee. Change plan, update your card or cancel from <strong>Manage billing</strong> at <a href="https://accounts.coglass.co.uk">accounts.coglass.co.uk</a>. See our <a href="/refunds/">cancellation and refund policy</a>.</p>
    <h2>{e(c['tax'])}</h2>
    {tax}
    {crown}
    <h2>Support</h2>
    {tz}
    <h2>Anything bigger</h2>
    <p>Several branches, more than the Business plan allows, or the app under your own name? Email <a href="mailto:{CONTACT}">{CONTACT}</a> and we'll work out what suits.</p>
    <p class="fine">Prices may change; we give existing customers at least 30 days' notice by email first.</p>
  </div>
</section>
{cta_band(ctx, c, 'Not sure which plan fits?', 'Book a demo and we will help you pick — and you can move up a plan any time.')}'''
    url = site + cpath(c, 'pricing')
    jsonld = {'@context': 'https://schema.org', '@graph': [org(site), software(site, url, offers(site, c))]}
    low = c['prices']['starter']
    desc = (f'Coglass plans in {c["in_name"]} from {low} a month + {c["tax"]}, every feature on every plan. '
            f'Billed monthly in {c["currency"]}, no setup fee, no minimum term.')
    return ctx['layout'](path=cpath(c, 'pricing'), title=f'Pricing in {c["in_name"]} | Coglass glazing software — from {low}/month + {c["tax"]}',
                         description=desc, body=body, current=cpath(c, 'pricing'), og_title=f'Coglass pricing — {c["name"]}',
                         jsonld=jsonld, lang=c['lang'], og_locale=c['og_locale'], alternates=alternates('pricing'), country=c)


# ---------------------------------------------------------------------------- country FAQ
def country_faq(ctx, c):
    e, site = ctx['e'], ctx['SITE']
    body = f'''<section class="page-head"><div class="wrap"><h1>Coglass in {e(c['in_name'])}: questions and answers</h1><p>Prices, tax, support hours and how Coglass works for glaziers in {e(c['in_name'])}.</p></div></section>
<section class="sect" style="padding-top:44px">
  <div class="wrap" style="max-width:860px">
    <div class="faq">{faq_html(ctx, c['faq'])}</div>
    <p style="margin-top:22px">Something else? Email <a href="mailto:{ctx['CONTACT']}">{ctx['CONTACT']}</a>, see <a href="/support/">help &amp; support</a>, or <a href="{cpath(c, 'pricing')}">compare plans in {e(c['currency'])}</a>.</p>
    {other_countries(c, 'faq', 'Questions for another country:')}
  </div>
</section>
{cta_band(ctx, c, 'Want to see it first?', 'Book a demo and we will show you Coglass on the kind of jobs you do.')}'''
    jsonld = {'@context': 'https://schema.org', '@graph': [org(site), faq_ld(c['faq'])]}
    return ctx['layout'](path=cpath(c, 'faq'), title=f'Coglass in {c["in_name"]} — FAQ | Glazing software',
                         description=f'Questions about Coglass in {c["in_name"]}: prices in {c["currency"]}, {c["tax"]}, support hours, '
                                     'working offline, Xero and messaging customers.',
                         body=body, current=cpath(c, 'faq'), og_title=f'Coglass in {c["in_name"]} — FAQ', jsonld=jsonld,
                         lang=c['lang'], og_locale=c['og_locale'], alternates=alternates('faq'), country=c)


# ---------------------------------------------------------------------------- choosers
def chooser_cards(ctx, kind):
    e = ctx['e']
    cards = ''
    for k in ORDER:
        c = C[k]
        extra = '<span class="sub">Also the Isle of Man, Jersey, Guernsey &amp; Gibraltar</span>' if k == 'uk' else ''
        cards += (f'<li><a class="ccard" href="{cpath(c, kind)}" data-country="{k}" hreflang="{c["lang"]}">'
                  f'<span class="code" aria-hidden="true">{c["code"]}</span><span class="nm">{e(c["name"])}</span>{extra}'
                  f'<span class="pr">From {c["prices"]["starter"]} a month + {c["tax"]}</span></a></li>')
    return f'<ul class="cgrid">{cards}</ul>'


GLOBAL_FAQ = [
    ('Which countries is Coglass sold in?', 'The United Kingdom (including the Isle of Man, Jersey, Guernsey and Gibraltar), Ireland, '
     'Australia, New Zealand, South Africa, Namibia, Botswana and Malta. Each has its own prices in local currency.'),
    ('Is Coglass built for glass and glazing companies?', 'Yes. It holds full sealed-unit make-ups (double and triple glazed, cavity, '
     'spacer, gas), every edge and shape, and a drawing canvas for holes, Georgian bars, lead and diamond — plus a 1:1 lay-under '
     'template the factory copies onto the glass. It is not a general CRM adapted to glass.'),
    CS.OFFLINE_FAQ,
    ('Does it work on iPhone, Android and the web?', 'Yes — the office uses the web app in a browser, fitters use the iPhone or '
     'Android app, and the workshop uses the shop-floor app on an iPad.'),
    CS.XERO_FAQ,
    ('Who makes Coglass?', 'Halliday Morrow Ltd, a company registered in England & Wales. Our team is in the UK and supports every '
     'country we sell in.'),
]


def global_home(ctx):
    e, I, site = ctx['e'], ctx['ICON'], ctx['SITE']
    tiles = [
        ('shaped', 'Shaped glass', 'Arches, gables, holes and cut-outs drawn to size and priced.', 'coglass-feature-glass-specs.html'),
        ('georgian', 'Georgian & lead', 'Georgian bars, square and diamond leaded lights, drawn on the pane.', 'coglass-feature-glass-specs.html'),
        ('igu', 'Sealed-unit make-ups', 'Glass per leaf, cavity, spacer and gas on every line.', 'coglass-for-sealed-units.html'),
        ('po', 'Supplier POs', 'Order glass in a click, with the drawing on the PO.', 'coglass-feature-suppliers.html'),
        ('ipad', 'Runs on an iPad', 'Office, shop floor, trade counter and site — the whole business on one device.', 'coglass-ipad.html'),
    ]
    tiles_html = ''.join(f'<li class="tile">{I[i]}<h3>{e(t)}</h3><p>{e(x)}</p><a href="/{l}">More<span class="sr-only"> about {e(t.lower())}</span> →</a></li>' for i, t, x, l in tiles)
    aud = [
        ('glazier', 'Glaziers', 'Survey, quote, book the van, fit and get paid — office, site and workshop in step.', 'coglass-feature-fitting.html', 'How fitting works'),
        ('merchant', 'Glass merchants', 'Trade counter, trade price lists, stock and deliveries.', 'coglass-for-merchants.html', 'Coglass for merchants'),
        ('igu', 'Sealed unit makers', 'Take and price double- and triple-glazed units by make-up, then track them through production.', 'coglass-for-sealed-units.html', 'Coglass for unit makers'),
        ('processor', 'Processors', 'Cutting, edgework, toughening and unit sealing on one board — in-house or bought-in.', 'coglass-feature-production.html', 'The production board'),
    ]
    aud_html = ''.join(f'<li class="tile">{I[i]}<h3>{e(t)}</h3><p>{e(x)}</p><a href="/{l}">{e(lt)} →</a></li>' for i, t, x, l, lt in aud)
    src, alt, w, h = ctx['IMG']['planning']
    hero_img = f'<div class="shot"><div class="bar" aria-hidden="true"><i></i><i></i><i></i></div><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high"></div>'
    body = f'''<section class="hero">
  <div class="wrap grid">
    <div class="copy">
      <span class="eyebrow">Software for glass &amp; glazing companies</span>
      <h1>Every job, from enquiry to paid.</h1>
      <p class="lead">Quotes with real glass drawings, a planner your fitters actually use, purchase orders to suppliers, and invoices that look the part. One system for the office, the van and the workshop — in the UK, Ireland, Australia, New Zealand, Southern Africa and Malta.</p>
      <div class="ctas"><a class="btn acc lg" href="#countries">Choose your country</a><a class="btn lg" href="{ctx['DEMO']}">Book a demo</a></div>
      {ctx['trust'](['Phone, iPad & web apps', 'Xero connected', 'Prices in your currency'])}
    </div>
    <div class="visual">{hero_img}{ctx['phone']('Today · Gary', [('f', '08:00 Fitting', 'School · 1h 30m'), ('s', '10:30 Survey', 'Kitchen + bay · 45m'), ('f', '13:00 Fitting', 'Offices · 2h')])}</div>
  </div>
</section>
<section class="sect alt" id="countries">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Choose your country</span><h2>Coglass where you work</h2><p>Prices in your currency, your tax on quotes and invoices, and support hours for your time zone.</p></div>
    {chooser_cards(ctx, 'home')}
  </div>
</section>
<section class="sect">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Made for glass</span><h2>Made for glass, not bolted on</h2><p>The things a general CRM can't do — drawn, priced and sent to the supplier properly.</p></div>
    <ul class="tiles" style="list-style:none;padding:0;margin:0">{tiles_html}</ul>
  </div>
</section>
<section class="sect alt">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">What your customers receive</span><h2>Quotes and invoices that look the part</h2><p>Your logo and details, the drawing on every line, and a link to accept the quote online.</p></div>
    <div class="docs">
      <figure style="margin:0"><div class="doc"><img src="{ctx['IMG']['quote'][0]}" alt="{e(ctx['IMG']['quote'][1])}" width="900" height="855" loading="lazy" decoding="async"></div><figcaption class="cap">A real quotation PDF from a UK demo account with made-up details.</figcaption></figure>
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
    <ul class="fgrid" style="list-style:none;padding:0;margin:0">{local_features(ctx, dict(key='global', tax='VAT or GST'))}</ul>
    {pages.more_features_html(ctx)}
  </div>
</section>
{pages.flow_html(ctx)}
<section class="sect">
  <div class="wrap" style="max-width:860px">
    <div class="sect-head"><span class="kicker">Questions</span><h2>Frequently asked questions</h2></div>
    <div class="faq">{faq_html(ctx, GLOBAL_FAQ)}</div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>See it on your own kind of jobs</h2>
    <p>Pick your country for local prices, or book a demo and we will walk you through Coglass with the glass you sell.</p>
    <div class="ctas"><a class="btn acc lg" href="{ctx['DEMO']}">Book a demo</a><a class="btn ghost-light lg" href="#countries">Choose your country</a></div>
  </div>
</section>'''
    all_offers = [o for k in ORDER for o in offers(site, C[k])]
    jsonld = {'@context': 'https://schema.org', '@graph': [
        org(site),
        {'@type': 'WebSite', '@id': f'{site}/#website', 'url': f'{site}/', 'name': 'Coglass', 'publisher': {'@id': ORG_ID}},
        software(site, f'{site}/', all_offers),
        faq_ld(GLOBAL_FAQ),
    ]}
    return ctx['layout'](path='/', title='Coglass | Software for Glaziers, Glass Merchants & Sealed Unit Makers',
                         description='Quotes with real glass drawings, surveys, production, supplier POs, fitting and invoicing in one system '
                                     'for glass and glazing companies in the UK, Ireland, Australia, New Zealand, South Africa, Namibia, '
                                     'Botswana and Malta.',
                         body=body, current='/', og_title='Coglass — every glass job, from enquiry to paid', jsonld=jsonld,
                         lang='en', og_locale='en_GB', alternates=alternates('home'))


def pricing_chooser(ctx):
    e, site = ctx['e'], ctx['SITE']
    rows = ''.join(
        f'<tr><th scope="row"><a href="{cpath(C[k], "pricing")}" data-country="{k}">{e(C[k]["name"])}</a></th>'
        + ''.join(f'<td>{C[k]["prices"][p]}</td>' for _, p, _ in PLAN_NAMES) + f'<td>{C[k]["tax"]}</td></tr>'
        for k in ORDER)
    body = f'''<section class="page-head"><div class="wrap"><h1>Pricing</h1><p>Everything in Coglass on every plan, priced in your currency by the size of your team. Choose your country for its plans, tax and billing details. Last updated: October 2026.</p></div></section>
<section class="sect" style="padding-top:44px" id="plans">
  <div class="wrap">
    <h2>Choose your country</h2>
    {chooser_cards(ctx, 'pricing')}
    <h2 style="margin-top:44px">Monthly prices at a glance</h2>
    <p style="color:var(--ink2)">Every plan includes the full system. Prices are per month and exclude local VAT or GST.</p>
    <div class="table-wrap"><table>
      <tr><th scope="col">Country</th><th scope="col">Starter</th><th scope="col">Professional</th><th scope="col">Business</th><th scope="col">Plus</th></tr>
      {rows}
    </table></div>
    <p class="fine">The UK prices also apply in the Isle of Man, Jersey, Guernsey and Gibraltar. Elsewhere? <a href="{ctx['DEMO']}">Get in touch</a>.</p>
  </div>
</section>
{ctx['cta_band']('Not sure which plan fits?', 'Book a demo and we will help you pick — and you can move up a plan any time.')}'''
    all_offers = [o for k in ORDER for o in offers(site, C[k])]
    jsonld = {'@context': 'https://schema.org', '@graph': [org(site), software(site, f'{site}/pricing/', all_offers)]}
    return ctx['layout'](path='/pricing/', title='Pricing | Coglass glazing software — plans by country',
                         description='Coglass prices for the UK, Ireland, Australia, New Zealand, South Africa, Namibia, Botswana and Malta. '
                                     'Every feature on every plan, billed monthly in your currency.',
                         body=body, current='/pricing/', og_title='Coglass pricing', jsonld=jsonld,
                         lang='en', og_locale='en_GB', alternates=alternates('pricing'))


def build(ctx):
    out = {'index.html': global_home(ctx), 'pricing/index.html': pricing_chooser(ctx)}
    for k in ORDER:
        c = C[k]
        out[f'{c["slug"]}/index.html'] = country_home(ctx, c)
        out[f'{c["slug"]}/pricing/index.html'] = country_pricing(ctx, c)
        out[f'{c["slug"]}/faq/index.html'] = country_faq(ctx, c)
        for g in LG.guides_for(c):
            out[f'{c["slug"]}/{g["slug"]}/index.html'] = LG.guide_page(ctx, c, g, org, cta_band)
    return out


def sitemap_entries():
    """(path, priority, changefreq, alternates or None)"""
    out = [('/', '1.0', 'weekly', alternates('home')), ('/pricing/', '0.9', 'monthly', alternates('pricing'))]
    for k in ORDER:
        c = C[k]
        out += [(cpath(c, 'home'), '0.9', 'weekly', alternates('home')),
                (cpath(c, 'pricing'), '0.8', 'monthly', alternates('pricing')),
                (cpath(c, 'faq'), '0.6', 'monthly', alternates('faq'))]
        # Local guides have no equivalent in other countries: no hreflang alternates.
        out += [(LG.gpath(c, g), '0.7', 'monthly', None) for g in LG.guides_for(c)]
    return out
