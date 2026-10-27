"""The /glass-software/ pillar page: what glass software does, and how to choose it.

A global page (no country), written to answer the searches people make for glass software —
glass shop / glass business management, fabrication and production, quoting, online ordering,
fitting, invoicing — and to link out to the feature pages that go deeper. Keep every claim true
to the app: the webshop and customer portal follow countries.WEBSHOP_LIVE / PORTAL_LIVE.
"""
import countries as CS
from country_pages import ORG_ID

PATH = '/glass-software/'
TITLE = 'Glass Software for Quoting, Production & Fitting | Coglass'
H1 = 'Glass software: quoting, production and fitting for glass businesses'
DESCRIPTION = ('What glass software should do for glass shops, glaziers, merchants and sealed unit makers — quoting, '
               'production, fitting, invoicing — and how to choose it.')
UPDATED = 'October 2026'
DATE_PUBLISHED = '2026-10-27'
DATE_MODIFIED = '2026-10-27'


def _online_ordering():
    if CS.feature_live('webshop'):
        return ('<p>Trade customers can order cut-to-size glass from a <a href="/coglass-feature-webshop.html">webshop</a> '
                'in your branding, on their own agreed prices, and pay by card or PayPal — or send the order as an enquiry '
                'for you to quote. Orders drop straight into Coglass as jobs.</p>')
    return ('<p>Online ordering is where many glass businesses want to go next, so here is exactly where Coglass is. '
            'Today, customers can send an enquiry from a form on your own website straight into Coglass, accept a quote '
            'online from its link, and pay an invoice online. A <a href="/coglass-feature-webshop.html">trade webshop</a> '
            '— cut-to-size ordering on each customer\'s own prices, paid by card or PayPal — is '
            '<strong>coming soon</strong>, and will be included in your plan when it launches.</p>')


SECTIONS = [
    ('What glass software does', '''<p>Glass software is a business system built around the thing a glass company actually sells: a pane or a sealed unit made to a size, a make-up and a shape. A general CRM or job-management app can hold a customer and a price. It can't tell a 4/16/4 double-glazed unit from a toughened splashback with two holes, and it can't send the right spec to your supplier or your cutting bench.</p>
<p>Good glass software follows one job from the first enquiry to the money in the bank: the survey, the quote, the glass order, the workshop, the fitting or delivery, and the invoice. Everyone — the office, the van and the shop floor — works from the same record, so nobody retypes a size and nobody rings round to ask where a job has got to.</p>'''),
    ('Glass shop and glass business management', '''<p>For a glass shop, "management software" mostly means knowing where everything is. In Coglass every job has one record with its status, notes, photos, documents and messages. The <a href="/coglass-feature-orders.html">orders list</a> shows each job's stage, how much glass has arrived and what is still owed, and flags jobs that have sat too long in one status so they don't get forgotten.</p>
<p>The trade counter is covered too: Quick Go prices a walk-in or phone enquiry from any page, and a counter sale can be signed for on collection. Staff, roles, holidays and vans live in the same system, and the office, fitters and workshop each get the app that suits them — the web app in a browser, the phone app on site and the shop-floor app on an iPad.</p>'''),
    ('Glass fabrication and production tracking', '''<p>If you cut, process or seal glass yourself, you need to see the workshop at a glance. Every line on an order lands on the <a href="/coglass-feature-production.html">production board</a> — waiting on a supplier, glass in, in production, final checks, ready to go — with rush lines and urgent jobs flagged, and needed-by dates suggested from each product's lead time.</p>
<p>Each operation — edgework, holes, toughening, laminating — can be made in-house or bought in from a processor, and Coglass raises the outwork order when it is bought in. Sealed units are checked pane by pane before they can be marked sealed. Every pane gets a <a href="/coglass-feature-glass-labels.html">barcode label</a> with the job, opening and size, scanned in when the glass arrives. Lead, Georgian and diamond patterns drawn on the job print as a 1:1 template the bench lays the glass onto.</p>'''),
    ('Glass quoting and pricing', '''<p>Glass is priced by area, by edge length, by hole and by process, and trade customers expect their own rates. Coglass prices each line from your catalogue the moment you pick a product, with the pane drawn to size in mm — shapes, holes, cut-outs, Georgian bars and leaded lights — and the drawing goes on the <a href="/coglass-feature-quoting.html">quote</a>.</p>
<ul>
<li><strong>Sealed units</strong> are held as full make-ups: the glass in each leaf, plus the cavity, spacer and gas set on the order line, so you don't need a product for every gap. <a href="/coglass-for-sealed-units.html">More for sealed unit makers</a>.</li>
<li><strong>Toughening and other outwork</strong> can be priced as an operation on the line, and ordered from your processor when the job goes ahead.</li>
<li><strong>Price lists</strong> per customer or customer type, with a discount, quantity breaks and a contract window, are applied automatically, and the prices freeze when the quote is sent.</li>
<li><strong>Supplier price lists</strong> arrive as PDFs; the AI reads the article numbers and prices out of them for you to check, instead of typing them in.</li>
</ul>
<p>Send two or three options in one quote, and the customer accepts or declines online from a link.</p>'''),
    ('Online ordering for glass', None),  # filled by _online_ordering(), which follows the webshop flag
    ('Fitting, delivery and scheduling', '''<p>The <a href="/coglass-feature-scheduling.html">planning board</a> puts surveys, fittings and deliveries onto people and vans by drag and drop. Customers can tick the arrival windows that suit them, Coglass suggests runs of nearby ready jobs, and each fitter sees their day on the phone. Surveys are measured, drawn and photographed on the phone — even with no signal — and go straight onto the job.</p>
<p>On site, fitters <a href="/coglass-feature-fitting.html">sign off each pane</a> as fitted, partly fitted or not fitted, with photos, GPS and the customer's signature. Anything broken or the wrong size is flagged for re-order and keeps the job open until it is re-booked. Customers can get an on-our-way text with a <a href="/coglass-feature-tracking.html">tracking link</a>.</p>'''),
    ('Invoicing and Xero', '''<p>A draft invoice is raised when the job is signed off. <a href="/coglass-feature-invoicing.html">Invoicing</a> covers deposits, proformas and final invoices, with VAT or GST, part payments and overdue invoices flagged, and customers can pay online from the invoice link.</p>
<p>With <a href="/coglass-feature-xero.html">Xero</a> connected, invoices, the payments you record in Coglass and supplier bills are pushed to Xero, coded to the accounts and tax rates you pick from your own Xero organisation. It works in that direction: a payment recorded only in Xero isn't brought back into Coglass.</p>'''),
]

CHECKLIST = [
    'Does it hold a sealed unit as a make-up — each leaf, cavity, spacer and gas — not as a long list of products?',
    'Can it draw the pane — shapes, holes, cut-outs, Georgian and lead — and put that drawing on the quote, the purchase order and the workshop paperwork?',
    'Does it price the way you sell: per m², per edge, per hole, per process, with trade price lists and quantity breaks?',
    'Can each operation be made in-house or bought in, with the outwork order raised for you?',
    'Do your fitters get a phone app that works with no signal, with sign-off per pane rather than one tick for the whole job?',
    'Does it connect to your accounts software, and does it handle VAT or GST in your country and currency?',
    'Are you paying per feature, or is everything included and priced by the size of your team?',
    'Can you see it running on your own kind of jobs before you commit?',
]

FAQ = [
    ('What is glass software?', 'Business software built for companies that sell, process or fit glass. It understands panes and sealed '
     'units — sizes, make-ups, shapes, holes and processes — and runs the job from enquiry and quote through production and '
     'fitting to invoice.'),
    ('Is Coglass only for glaziers?', 'No. It\'s built for glaziers who survey and fit, glass merchants with a trade counter and '
     'deliveries, processors who cut, edge and toughen, and sealed unit makers. Every plan includes every feature.'),
    ('Which countries can I use Coglass in?', 'Coglass is sold in the United Kingdom (including the Isle of Man, Jersey, Guernsey and '
     'Gibraltar), Ireland, Australia, New Zealand, South Africa, Namibia, Botswana and Malta, with prices in local currency and '
     'your tax on quotes and invoices.'),
    ('Does it work on a phone and an iPad?', 'Yes. The office uses the web app in a browser, fitters and surveyors use the iPhone or '
     'Android app, and the workshop uses the shop-floor app on an iPad.'),
    ('Can my customers order glass online?', CS.shop(
        'Yes. Trade customers can order cut-to-size from your branded webshop on their own prices and pay by card or PayPal.',
        'Customers can send an enquiry from your website, accept quotes and pay invoices online today. The trade webshop for '
        'ordering cut-to-size online is coming soon and will be included in your plan when it launches.')),
    CS.XERO_FAQ,
]


def page(ctx, org, cta_band):
    e, site = ctx['e'], ctx['SITE']
    sections = ''
    for h, html in SECTIONS:
        sections += f'<h2>{e(h)}</h2>\n{html if html is not None else _online_ordering()}\n'
    checks = ''.join(f'<li>{e(x)}</li>' for x in CHECKLIST)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    body = f'''<section class="page-head"><div class="wrap">
  <h1>{e(H1)}</h1>
  <p>Whether you run a glass shop, fit glass, sell it to the trade, process it or make sealed units, this page explains what glass software should do for a glass business, where Coglass fits, and what to check before you choose.</p>
  <p class="updated" style="margin-top:14px">Last updated: {UPDATED}.</p>
</div></section>
<article class="prose">
{sections}<h2>How to choose glass software</h2>
<p>Most systems look alike in a sales video. These questions separate software made for glass from software adapted to it:</p>
<ul class="checks">{checks}</ul>
<p>Coglass includes every feature on every plan, priced by how many people use it — <a href="/pricing/">see pricing for your country</a> or <a href="{ctx['DEMO']}">book a demo</a> and we'll walk you through it with the glass you sell. To look around on your own first, <a href="{ctx['TRY_DEMO']}" target="_blank" rel="noopener">try the live demo</a> — no sign-up, and nothing you do is sent to anyone.</p>
<h2>Questions about glass software</h2>
<div class="faq">{faq}</div>
<h2>Read more</h2>
<ul class="related"><li><a href="/coglass-for-merchants.html">For glass merchants</a></li><li><a href="/coglass-for-sealed-units.html">For sealed unit makers</a></li><li><a href="/coglass-feature-glass-specs.html">Glass specs</a></li><li><a href="/coglass-feature-suppliers.html">Suppliers</a></li><li><a href="/coglass-feature-mobile.html">Mobile app</a></li><li><a href="/coglass-ipad.html">Coglass on the iPad</a></li><li><a href="/#features">All features</a></li></ul>
</article>
{cta_band('See it on your own kind of jobs', 'Book a demo and we will walk you through Coglass with the glass you sell and the way you work.')}'''
    url = site + PATH
    jsonld = {'@context': 'https://schema.org', '@graph': [
        org(site),
        {'@type': 'Article', 'headline': H1, 'description': DESCRIPTION, 'inLanguage': 'en',
         'image': f'{site}/og-image.png', 'datePublished': DATE_PUBLISHED, 'dateModified': DATE_MODIFIED,
         'mainEntityOfPage': url, 'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Coglass', 'item': f'{site}/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Glass software', 'item': url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                                            for q, a in FAQ]},
    ]}
    return ctx['layout'](path=PATH, title=TITLE, description=DESCRIPTION, body=body, current=PATH,
                         og_title='Glass software for glass businesses', jsonld=jsonld, lang='en', og_locale='en_GB')
