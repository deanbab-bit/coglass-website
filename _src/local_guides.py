"""Local guides: country-specific pages under each country section (/au/as-1288-safety-glass/, …).

They exist to give each country section genuinely local content — the standard, the tax rule or
the way of working that is particular to that country — so the section has more than a home,
pricing and FAQ page to rank with.

Rules for the copy (same as countries.py, stricter because these pages talk about regulations):
  * The explainer text is GENERAL GUIDANCE about the rule itself, written from the official
    source listed under `sources`. Every page says it is not legal or tax advice.
  * The "Where Coglass fits" list (`coglass`) only says what the app does TODAY. Per-country tax
    rates, tax-invoice headings, reverse charge, local bank formats and local safety-glazing
    rule tables are still being built behind flags in the app (TAX_SETTINGS_FULLY_LIVE = false,
    region PRs R2/R4 open) — none of that is claimed here. When it ships, add it to `coglass`.
  * These pages have no equivalent in other countries, so they carry no hreflang alternates:
    each is self-canonical (the layout adds the canonical tag).

Copy lives in GUIDES below; rendering is `guide_page`. Built from country_pages.build().
"""
import html

from countries import C

UPDATED = 'October 2026'
DATE_MODIFIED = '2026-10-04'


def gpath(c, g):
    return f'/{c["slug"]}/{g["slug"]}/'


def guides_for(c):
    return GUIDES.get(c['key'], [])


def ext(label, url):
    return f'<a href="{url}" rel="noopener">{label}</a>'


def guide_page(ctx, c, g, org, cta_band):
    e, site = ctx['e'], ctx['SITE']
    home = f'/{c["slug"]}/'
    sections = ''.join(f'<h2>{e(h)}</h2>\n{html}\n' for h, html in g['sections'])
    fits = ''.join(f'<li>{x}</li>' for x in g['coglass'])
    fits_note = f'<p>{g["coglass_note"]}</p>' if g.get('coglass_note') else ''
    sources = ''.join(f'<li>{ext(e(lbl), url)}</li>' for lbl, url in g['sources'])
    others = [o for o in guides_for(c) if o['slug'] != g['slug']]
    more = ''.join(f'<li><a href="{gpath(c, o)}">{e(o["nav"])}</a></li>' for o in others)
    more += (f'<li><a href="{home}">Coglass in {e(c["in_name"])}</a></li>'
             f'<li><a href="/{c["slug"]}/pricing/">Pricing in {e(c["currency"])}</a></li>'
             f'<li><a href="/{c["slug"]}/faq/">{e(c["short"])} FAQ</a></li>')
    body = f'''<section class="page-head"><div class="wrap">
  <nav aria-label="Breadcrumb" class="fine" style="margin:0 0 12px"><a href="{home}">Coglass in {e(c['in_name'])}</a> <span aria-hidden="true">›</span> Guides for glaziers</nav>
  <h1>{e(g['h1'])}</h1>
  <p>{e(g['lead'])}</p>
  <p class="updated" style="margin-top:14px">General guidance, not legal or tax advice. Last checked: {UPDATED}.</p>
</div></section>
<article class="prose">
{sections}
<h2>Where Coglass fits</h2>
{fits_note}
<ul class="checks">{fits}</ul>
<p>Want to see it on your own jobs? <a href="{ctx['demo_href'](c)}">Book a demo</a> or <a href="/{c['slug']}/pricing/">see pricing in {e(c['currency'])}</a>.</p>
<h2>Sources</h2>
<ul>{sources}</ul>
<p class="fine">This page explains the rules in general terms. Standards and tax rules change, and how they apply depends on the job — check the source, your building control body or your accountant before relying on it.</p>
<h2>More for glaziers in {e(c['in_name'])}</h2>
<ul class="related">{more}</ul>
</article>
{cta_band(ctx, c, g['cta'][0], g['cta'][1])}'''
    url = site + gpath(c, g)
    jsonld = {'@context': 'https://schema.org', '@graph': [
        org(site),
        {'@type': 'Article', 'headline': g['h1'], 'description': g['description'], 'inLanguage': c['lang'],
         'dateModified': DATE_MODIFIED, 'mainEntityOfPage': url, 'author': {'@id': 'https://coglass.net/#org'},
         'publisher': {'@id': 'https://coglass.net/#org'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': f'Coglass in {c["in_name"]}', 'item': site + home},
            {'@type': 'ListItem', 'position': 2, 'name': g['nav'], 'item': url}]},
    ]}
    return ctx['layout'](path=gpath(c, g), title=g['title'], description=g['description'], body=body,
                         current=gpath(c, g), og_title=g['h1'], jsonld=jsonld, lang=c['lang'],
                         og_locale=c['og_locale'], alternates=None, country=c)


def guides_section(ctx, c):
    """The 'Guides for glaziers in X' block on the country home."""
    e = ctx['e']
    gs = guides_for(c)
    if not gs:
        return ''
    tiles = ''.join(f'<li class="tile"><h3>{e(g["nav"])}</h3><p>{e(g["blurb"])}</p>'
                    f'<a href="{gpath(c, g)}">Read the guide<span class="sr-only">: {e(g["nav"])}</span>&nbsp;→</a></li>' for g in gs)
    return f'''<section class="sect" id="guides">
  <div class="wrap">
    <div class="sect-head"><span class="kicker">Guides for glaziers in {e(c['in_name'])}</span><h2>The local rules, in plain English</h2><p>Short guides to the standards and paperwork glaziers in {e(c['in_name'])} deal with — and where Coglass helps.</p></div>
    <ul class="tiles why" style="list-style:none;padding:0;margin:0">{tiles}</ul>
  </div>
</section>
'''


def footer_links(country):
    """One line of local-guide links for the footer of that country's pages."""
    if not country:
        return ''
    gs = guides_for(country)
    if not gs:
        return ''
    e = html.escape
    links = ' · '.join(f'<a href="{gpath(country, g)}">{e(g["nav"])}</a>' for g in gs)
    return f'\n    <p class="countries"><span>Guides for glaziers in {e(country["in_name"])}:</span> {links}.</p>'


GUIDES = {}


# ============================================================================ shared "Where Coglass fits" lines
# Each is true in the app today (see the PR's claim → proof table). Keep them that way.
FIT_SURVEY = ('<strong>Surveys on the phone.</strong> Each opening is measured, drawn and photographed, with notes, GPS and '
              'the access level — and it works with no signal, syncing when you are back in coverage.')
FIT_SPEC = ('<strong>The glass written down once.</strong> The product and make-up you pick on the line goes on the quote, the '
            "supplier's purchase order and the workshop's cutting sheet, so everyone works from the same specification.")
FIT_DOCS = ('<strong>Paperwork on the job.</strong> Keep certificates, product sheets and photos in the job\'s Documents tab, '
            'next to the quote and invoice.')
FIT_XERO = ('<strong>Xero.</strong> Invoices, payments and supplier bills push to your Xero organisation, coded to the '
            'accounts and tax rates you choose from your own Xero settings — your returns are then done in Xero.')
FIT_INVOICES = ('<strong>Deposit, proforma and final invoices</strong> from the job, with payments recorded against them '
                'and overdue invoices flagged.')
FIT_RAMS = ('<strong>A risk assessment and method statement on every job.</strong> Hazards, who is at risk and the controls, '
            'the method step by step, PPE, equipment and emergency notes — filled in on the desktop or the phone, and '
            'exported as a PDF. The equipment list is pre-filled from the access level recorded on the survey.')
FIT_HIRE = ('<strong>Scaffold and access hire priced properly.</strong> Set up scaffold, a tower or a MEWP as a hire item '
            'with a day rate; it is charged once per job, not per pane, and you can raise a hire order to the hire company.')
FIT_OFFLINE = ('<strong>The apps keep working offline.</strong> Surveys and fitting sign-offs are saved on the phone, and the '
               'shop-floor iPad keeps its production board, then both sync when the connection is back.')


# ============================================================================ Australia
GUIDES['au'] = [
    dict(
        slug='as-1288-safety-glass', nav='AS 1288 and safety glass',
        blurb='Where Grade A safety glass is needed — doors, side panels, low-level glazing and bathrooms — and how to keep it on the job.',
        title='AS 1288 Safety Glass Guide for Australian Glaziers | Coglass',
        description='A plain-English guide to AS 1288:2021 and the NCC human-impact rules: doors, door side panels, low-level '
                    'glazing, bathrooms and safety-glass marking — for Australian glaziers.',
        h1='AS 1288 and safety glass: a guide for Australian glaziers',
        lead='Which glass goes where under AS 1288 and the NCC — doors, side panels, low-level glazing and bathrooms — and how to '
             'make sure the glass you specified is the glass that gets ordered and fitted.',
        sections=[
            ('What AS 1288 covers', '''<p>AS 1288 <em>Glass in buildings — Selection and installation</em> is the Australian Standard for choosing and installing glass. The current edition is <strong>AS 1288:2021</strong>, the fifth edition, which replaced AS 1288‑2006 in June 2021. It covers glass for wind loading, human impact and special uses such as overhead glazing and barriers.</p>
<p>The National Construction Code (NCC) brings it in. For Class 2 to 9 buildings, NCC Volume One references AS 1288. For houses, NCC Volume Two lets you use AS 1288 for glass selection and safety glazing (or AS 2047 for windows), and the ABCB Housing Provisions set out deemed-to-satisfy rules in Part 8: windows (8.2), glass sizing and installation (8.3) and human impact (8.4).</p>'''),
            ('Where Grade A safety glazing is needed in houses', '''<p>Part 8.4 of the ABCB Housing Provisions (Glazing — human impact) sets out the locations where people are most likely to walk into glass. In plain terms:</p>
<ul>
<li><strong>Doors</strong> — Grade A safety glazing. Unframed doors need toughened glass at least 10 mm thick.</li>
<li><strong>Door side panels</strong> — framed glass less than 300 mm from the nearest edge of the doorway opening must be Grade A, with limited exceptions for annealed glass based on a sight-line test.</li>
<li><strong>Low-level glazing</strong> — where the lowest sight line is less than 500 mm above the highest abutting finished floor, use Grade A safety glazing, or annealed glass at least 5 mm thick up to 1.2 m².</li>
<li><strong>Bathrooms, ensuites and shower screens</strong> — all glazing less than 2.0 m above the highest abutting finished level must be Grade A safety glazing.</li>
</ul>
<p>Grade A safety glass is toughened or laminated glass. Commercial buildings follow AS 1288 itself through NCC Volume One, which has its own detail — read the standard for those jobs.</p>'''),
            ('Marking: prove what went in', '''<p>Safety glass has to be permanently marked — etched, or with a label that cannot be reused once removed — showing the standard, the manufacturer, the grade, the thickness and the type. AS/NZS 2208 is the standard for safety glazing materials. On a replacement job, the mark on the glass coming out is also a quick check of what was there before.</p>'''),
            ('A simple routine that avoids the expensive mistake', '''<ol>
<li><strong>At the survey</strong>, note where each opening is: in a door, beside a door, low down, or in a wet area. A photo of each opening makes it obvious later.</li>
<li><strong>When you quote</strong>, put the glass type and grade on the line — "6.38 mm laminated Grade A", not just "clear".</li>
<li><strong>When you order</strong>, make sure the purchase order carries the same description, so the supplier makes what you quoted.</li>
<li><strong>On the day</strong>, check the mark on the glass before it goes in.</li>
</ol>'''),
        ],
        coglass_note='Coglass does not check your glass against AS 1288 for you — that stays with you and the standard. What it does is keep the specification consistent from survey to fitting:',
        coglass=[FIT_SURVEY, FIT_SPEC, FIT_DOCS],
        sources=[
            ('Standards Australia — AS 1288:2021 published', 'https://www.standards.org.au/blog/as-1288-2021'),
            ('ABCB — Housing Provisions Part 8.4, Glazing: human impact (NCC 2022)', 'https://www.abcb.gov.au/editions/ncc-2022/adopted/housing-provisions/8-glazing/part-84-glazing-human-impact'),
            ('ABCB — NCC Volume One referenced documents', 'https://www.abcb.gov.au/editions/ncc-2022/adopted/volume-one/2-referenced-documents/referenced-documents'),
        ],
        cta=('Keep the glass you quoted the glass you fit', 'Book a demo and we will show you a job going from survey to purchase order to fitting in Coglass.'),
    ),
    dict(
        slug='gst-tax-invoices', nav='GST tax invoices',
        blurb='What an Australian tax invoice must show, the $82.50 and $1,000 thresholds, and getting it all into BAS.',
        title='GST Tax Invoices for Australian Glaziers | Coglass',
        description='What a GST tax invoice must show in Australia: your ABN, the words "tax invoice", GST at 10%, the $82.50 '
                    'and $1,000 thresholds, the 28-day rule and BAS — a guide for glaziers.',
        h1='GST tax invoices: a guide for Australian glaziers',
        lead='What your invoices need to show for GST, when you need the buyer\'s ABN on them, and how the figures get to your BAS.',
        sections=[
            ('GST in one paragraph', '''<p>GST is 10% on most goods and services sold in Australia, including glass and glazing work. You must register for GST once your turnover is $75,000 or more a year. Most businesses report GST quarterly on their Business Activity Statement (BAS); monthly reporting applies at $20 million or more, or if the ATO directs it.</p>'''),
            ('What a tax invoice must show', '''<p>A tax invoice lets a GST-registered customer — a builder, a shopfitter, a property manager — claim the GST back. It must show:</p>
<ul>
<li>that it is intended to be a tax invoice (heading it "Tax invoice" is the simplest way);</li>
<li>your identity and your ABN;</li>
<li>the date it was issued;</li>
<li>a brief description of what was sold — the glass, the work, the quantities;</li>
<li>the GST amount, or a statement that the total price includes GST.</li>
</ul>'''),
            ('The thresholds that catch people out', '''<div class="table-wrap"><table>
<tr><th scope="col">Sale (including GST)</th><th scope="col">What you need to do</th></tr>
<tr><td>$82.50 or less</td><td>No tax invoice needed.</td></tr>
<tr><td>Over $82.50 and under $1,000</td><td>A tax invoice with the details above, if the customer asks.</td></tr>
<tr><td>$1,000 or more</td><td>The tax invoice must also show the buyer's identity or ABN.</td></tr>
</table></div>
<p>If a customer asks for a tax invoice, you must give it to them within 28 days. Most glaziers simply issue one on every job — and on a $1,000-plus job for a business customer, put their business name and ABN on it from the start.</p>'''),
            ('Deposits and progress payments', '''<p>Many glazing jobs take a deposit before glass is ordered. GST generally follows the payment or the invoice, depending on whether you account on a cash or accruals basis — ask your accountant which applies to you, and make sure the deposit invoice and the final invoice add up to the job, so GST isn't counted twice.</p>'''),
        ],
        coglass_note='Coglass is not BAS software. It produces the invoices and hands them to Xero, where your BAS is prepared:',
        coglass=[FIT_INVOICES, FIT_XERO,
                 '<strong>Customers pay by card</strong> from the invoice link when you connect your own Stripe account, and the payment is recorded on the invoice.'],
        sources=[
            ('ATO — Tax invoices', 'https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/tax-invoices'),
            ('ATO — Registering for GST', 'https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/registering-for-gst'),
            ('ATO — How Australian GST works', 'https://www.ato.gov.au/businesses-and-organisations/international-tax-for-business/gst-for-non-resident-businesses/how-australian-gst-works'),
        ],
        cta=('Invoices out, payments in, BAS in Xero', 'Book a demo and we will show you a job from deposit invoice to paid, and how it lands in Xero.'),
    ),
    dict(
        slug='swms-working-at-height', nav='SWMS and working at height',
        blurb='When a Safe Work Method Statement is required for glazing work, and keeping one with every job.',
        title='SWMS for Glaziers: Working at Height Over 2 m in Australia | Coglass',
        description='When Australian glaziers need a Safe Work Method Statement (SWMS): high-risk construction work, the 2 metre '
                    'fall rule, what a SWMS covers, and keeping it on the job.',
        h1='SWMS and working at height: a guide for Australian glaziers',
        lead='Glazing work above the ground floor is often high-risk construction work. Here is when a Safe Work Method Statement '
             'is required, what goes in it, and how to keep one with every job.',
        sections=[
            ('When you need a SWMS', '''<p>Under the model Work Health and Safety (WHS) Regulations, construction work that involves a risk of a person falling more than <strong>2 metres</strong> is high-risk construction work. A Safe Work Method Statement must be prepared <em>before</em> that work starts, and the work must be done in line with it.</p>
<p>For glaziers that commonly means first-floor and higher windows, shopfronts and curtain walling worked from scaffold or a mobile elevating work platform, balustrades on balconies and stairwells, and overhead glazing. Other high-risk categories can apply too — for example work near traffic or powered mobile plant.</p>
<p>WHS laws are made by each state and territory. Most follow the model regulations; South Australia moved from a 3 metre to a 2 metre threshold on 1 July 2026. Check your own regulator's guidance — SafeWork NSW, WorkSafe Victoria, WorkSafe Queensland and so on.</p>'''),
            ('What a SWMS covers', '''<ul>
<li>the high-risk construction work being done;</li>
<li>the hazards and risks of that work;</li>
<li>the control measures, and how they will be put in place, monitored and reviewed;</li>
<li>written so the workers doing the job can follow it — and kept available on site.</li>
</ul>
<p>A generic SWMS copied from job to job tends to miss what is different about this site: the access, the ground conditions, the size and weight of the panes, who else is working nearby.</p>'''),
            ('Make the survey do the work', '''<p>The person who surveys the job already knows how high the openings are, how you will get to them and what access equipment you will need. Capture it then — access level, photos of the elevation, notes on the ground and parking — and the SWMS for the fitting crew starts from facts rather than a blank template.</p>'''),
        ],
        coglass_note='Coglass keeps a risk assessment and method statement with each job. It is a record you fill in, not a state-specific SWMS template — check it against your regulator\'s requirements:',
        coglass=[FIT_RAMS, FIT_SURVEY, FIT_HIRE],
        sources=[
            ('Safe Work Australia — Working at heights (construction)', 'https://safeworkaustralia.gov.au/duties-tool/construction/hazards-information/working-heights'),
            ('SafeWork SA — Lowering the height threshold', 'https://safework.sa.gov.au/news-and-alerts/news/news/2025/lowering-height-threshold-will-raise-safety-standards'),
        ],
        cta=('Every job with its safety paperwork', 'Book a demo and we will show you a survey turning into a job, a risk assessment and a fitting.'),
    ),
    dict(
        slug='glazing-software-australia', nav='Coglass across Australia',
        blurb='Support hours from Sydney to Perth, working out of range, and setting Coglass up for your business.',
        title='Glazing Software Across Australia: Sydney to Perth | Coglass',
        description='Coglass for glaziers across Australia — Sydney, Melbourne, Brisbane, Perth, Adelaide, Hobart, Darwin and '
                    'Canberra: support hours in your time zone, working out of range, and getting set up.',
        h1='Glazing software for glaziers across Australia',
        lead='From Sydney to Perth: when you can reach our team, how Coglass copes with long drives and patchy coverage, and how '
             'we get you set up.',
        sections=[
            ('Support hours in your time zone', '''<p>Our team is in the UK. Email any time and we usually reply within one UK working day; demos are booked at a time that suits you, early morning or evening. How far ahead of the UK you are depends on your city and the season:</p>
<div class="table-wrap"><table>
<tr><th scope="col">City</th><th scope="col">Time zone</th><th scope="col">Ahead of the UK, Nov–Mar</th><th scope="col">Ahead of the UK, Apr–Sep</th></tr>
<tr><th scope="row">Sydney, Melbourne, Canberra, Hobart</th><td>AEST / AEDT</td><td>11 hours</td><td>9 hours</td></tr>
<tr><th scope="row">Brisbane</th><td>AEST (no daylight saving)</td><td>10 hours</td><td>9 hours</td></tr>
<tr><th scope="row">Adelaide</th><td>ACST / ACDT</td><td>10½ hours</td><td>8½ hours</td></tr>
<tr><th scope="row">Darwin</th><td>ACST (no daylight saving)</td><td>9½ hours</td><td>8½ hours</td></tr>
<tr><th scope="row">Perth</th><td>AWST (no daylight saving)</td><td>8 hours</td><td>7 hours</td></tr>
</table></div>
<p class="fine">For a few weeks in October and around the start of April, both countries are on summer time at once and the gap is an hour different — Sydney is then 10 hours ahead.</p>'''),
            ('Long drives and patchy coverage', '''<p>A survey two hours up the highway, a fitting on a rural block with one bar of signal: the phone app is built for it. Surveys, drawings, photos and fitting sign-offs are saved on the phone and sync when you are back in range. The planner shows which ready jobs are close to the day's other stops, scored by driving distance rather than a straight line, so a long drive can pick up a second job on the way.</p>'''),
            ('Getting set up', '''<p>Coglass is priced in Australian dollars and sold to registered businesses. Book a demo and we will show you Coglass with the glass you sell, then set your account up with you — your products, trade prices, team and vans. There is no setup fee and no minimum term.</p>'''),
        ],
        coglass_note='What you get, wherever you are in Australia:',
        coglass=[FIT_OFFLINE,
                 '<strong>A planner for spread-out work.</strong> Drag surveys, fittings and deliveries onto people and vans, and see which ready jobs are near the day\'s other stops by driving distance.',
                 FIT_XERO],
        sources=[
            ('Australian Government — Time zones and daylight saving', 'https://info.australia.gov.au/about-australia/facts-and-figures/time-zones-and-daylight-saving'),
            ('NSW Government — Daylight saving', 'https://www.nsw.gov.au/about-nsw/daylight-saving'),
        ],
        cta=('Talk to us at a time that suits you', 'Book a demo and we will find a time that works for your time zone.'),
    ),
]


# ============================================================================ New Zealand
GUIDES['nz'] = [
    dict(
        slug='nzs-4223-3-safety-glazing', nav='NZS 4223.3 safety glazing',
        blurb='What NZS 4223.3 covers, how it links to Building Code clause F2, and a routine that keeps the right glass on the job.',
        title='NZS 4223.3 Safety Glazing Guide for NZ Glaziers | Coglass',
        description='A plain-English guide to NZS 4223.3:2016 human impact safety glazing for New Zealand glaziers: what it covers, '
                    'how F2/AS1 and the Building Code use it, and keeping the specification right from survey to fit.',
        h1='NZS 4223.3 safety glazing: a guide for New Zealand glaziers',
        lead='How human-impact safety glazing works under the New Zealand Building Code, what NZS 4223.3 covers, and a simple routine '
             'that makes sure the glass you specified is the glass that goes in.',
        sections=[
            ('The standard and the Building Code', '''<p><strong>NZS 4223.3:2016</strong> <em>Glazing in buildings — Part 3: Human impact safety requirements</em> is the New Zealand standard for glass that people could walk into, fall against or break. The 2016 edition (with Amendment 1, May 2016) replaced NZS 4223.3:1999.</p>
<p>It is a way of complying with the Building Code. MBIE's Acceptable Solution <strong>F2/AS1</strong> — for clause F2, <em>Hazardous building materials</em> — cites it for human impact, including glazing in bathrooms, and it is also cited for clause B1 (Structure) and F4 (Safety from falling).</p>'''),
            ('What it applies to', '''<p>NZS 4223.3 applies to glazing that is wholly or partly within <strong>2000 mm of the floor or ground</strong> and isn't protected from impact. Inside that zone, the standard sets out where safety glazing is needed and how the glass must be selected — the places people are most likely to collide with glass, such as doors and the panels beside them, low-level glazing, and bathrooms and shower areas.</p>
<p>The exact zones, grades and sizes are in the standard itself. Don't assume they are the same as Australia's AS 1288 — the two are separate standards.</p>'''),
            ('A routine that avoids the expensive mistake', '''<ol>
<li><strong>At the measure-up</strong>, note where each opening is — in or beside a door, low down, in a bathroom, on a stair or landing — and take a photo.</li>
<li><strong>When you quote</strong>, put the glass type and safety grade on the line, not just "clear".</li>
<li><strong>When you order</strong>, make sure the purchase order carries the same description, so the supplier makes what you quoted.</li>
<li><strong>On the day</strong>, check the safety-glass mark on each pane before it goes in, and keep a photo for the job file.</li>
</ol>'''),
        ],
        coglass_note='Coglass does not check your glass against NZS 4223.3 — that stays with you and the standard. It keeps the specification consistent from measure-up to fitting:',
        coglass=[FIT_SURVEY, FIT_SPEC, FIT_DOCS],
        sources=[
            ('MBIE Building Performance — NZS 4223.3:2016', 'https://codehub.building.govt.nz/resources/4223-32016-nzs'),
            ('MBIE Building Performance — F2 Hazardous building materials: acceptable solutions', 'https://www.building.govt.nz/building-code-compliance/f-safety-of-users/f2-hazardous-building-materials/acceptable-solutions-and-verification-methods'),
        ],
        cta=('Keep the glass you quoted the glass you fit', 'Book a demo and we will show you a job going from measure-up to purchase order to fitting in Coglass.'),
    ),
    dict(
        slug='gst-taxable-supply-information', nav='GST and taxable supply information',
        blurb='GST at 15% and what your invoices must show since tax invoices became "taxable supply information" in 2023.',
        title='GST Invoices for NZ Glaziers: Taxable Supply Info | Coglass',
        description='What New Zealand glaziers\' invoices must show for GST since 1 April 2023: taxable supply information, the '
                    '$200 and $1,000 thresholds, GST at 15% and the 28-day rule.',
        h1='GST invoices in New Zealand: a guide for glaziers',
        lead='Since April 2023 the rules talk about "taxable supply information" rather than tax invoices. Here is what your '
             'invoices need to show at each price level.',
        sections=[
            ('What changed in 2023', '''<p>From <strong>1 April 2023</strong>, Inland Revenue replaced the old tax invoice rules with <strong>taxable supply information</strong> (TSI). You no longer need one particular document — the information can be spread across invoices, contracts and statements — but most glaziers still send one invoice with everything on it, and you can still head it "Tax invoice". GST is 15%.</p>'''),
            ('What to show, by price', '''<div class="table-wrap"><table>
<tr><th scope="col">Supply (including GST)</th><th scope="col">Information to give</th></tr>
<tr><td>$200 or less</td><td>Your name, the date, a description of what was supplied, and the amount.</td></tr>
<tr><td>Over $200, up to $1,000</td><td>All of the above, plus your GST number, and either the amounts before and after GST with the GST shown, or the GST-inclusive total with a statement that it includes GST.</td></tr>
<tr><td>Over $1,000</td><td>All of the above, plus details that identify a GST-registered buyer — for example their name and an address, phone number, email, NZBN or website.</td></tr>
</table></div>
<p>If a GST-registered customer asks for the information on a supply over $200, you must give it within 28 days.</p>'''),
            ('In practice', '''<p>Builders, property managers and commercial customers will usually need the over-$1,000 information, so get their business details at the quote stage rather than chasing them at invoice time. Make sure deposit and final invoices add up to the job so the GST isn't counted twice.</p>'''),
        ],
        coglass_note='Coglass is not GST-return software. It produces the invoices and hands them to Xero, where your GST return is prepared:',
        coglass=[FIT_INVOICES, FIT_XERO,
                 '<strong>Customers pay by card</strong> from the invoice link when you connect your own Stripe account, and the payment is recorded on the invoice.'],
        sources=[
            ('Inland Revenue — Tax invoices for GST', 'https://www.ird.govt.nz/gst/tax-invoices-for-gst'),
            ('Inland Revenue — How tax invoices for GST work', 'https://www.ird.govt.nz/gst/tax-invoices-for-gst/how-tax-invoices-for-gst-work'),
        ],
        cta=('Invoices out, payments in, GST in Xero', 'Book a demo and we will show you a job from deposit invoice to paid, and how it lands in Xero.'),
    ),
    dict(
        slug='health-and-safety-working-at-height', nav='Health & safety and working at height',
        blurb='Your duties under HSWA 2015, site-specific safety plans, and notifying WorkSafe about work at height.',
        title='Health & Safety for NZ Glaziers: HSWA & Heights | Coglass',
        description='Health and safety for New Zealand glaziers: PCBU duties under HSWA 2015, site-specific safety plans, working at '
                    'height and when to notify WorkSafe — with safety paperwork kept on every job.',
        h1='Health and safety on glazing jobs in New Zealand',
        lead='Your duties as a PCBU, the site-specific safety plans main contractors ask for, and the work at height you must tell '
             'WorkSafe about before you start.',
        sections=[
            ('Your duty as a PCBU', '''<p>Under the <strong>Health and Safety at Work Act 2015</strong>, a glazing business is a PCBU — a person conducting a business or undertaking. Its primary duty is to ensure, so far as is reasonably practicable, the health and safety of its workers and of anyone else affected by its work: a safe work environment, safe plant and structures, and safe systems of work. Carrying and installing large panes, cutting, and working off ladders and scaffold are the obvious risks in glazing.</p>'''),
            ('Site-specific safety plans', '''<p>A <strong>site-specific safety plan</strong> (SSSP) sets out the hazards on a particular job and how they will be controlled. It isn't a document the Act itself names, but it is a common way to show you are meeting your duties, and main contractors routinely ask subcontractors for one before they come on site. A good one is about <em>this</em> site — access, heights, pane sizes and weights, who else is working nearby — not a copy of the last job's.</p>'''),
            ('Working at height and notifying WorkSafe', '''<p>WorkSafe's guidance <em>Working at height in New Zealand</em> expects businesses to manage the risk of falls on every job. Some work must also be notified to WorkSafe at least 24 hours before it starts — including construction work where someone could fall <strong>5 metres or more</strong>, and putting up or taking down scaffolding with that fall risk.</p>
<p>There are exclusions: work on a house up to and including two full storeys, work done from a ladder only, and minor or routine maintenance and repair. Check WorkSafe's notifications page for the full wording before relying on an exclusion.</p>'''),
        ],
        coglass_note='Coglass keeps the safety paperwork with each job. It is a record you fill in, not an official SSSP template — check it against what your main contractor and WorkSafe expect:',
        coglass=[FIT_RAMS, FIT_SURVEY, FIT_HIRE],
        sources=[
            ('WorkSafe — Introduction to the Health and Safety at Work Act 2015', 'https://www.worksafe.govt.nz/managing-health-and-safety/getting-started/introduction-hswa-special-guide'),
            ('WorkSafe — Working at height in New Zealand', 'https://www.worksafe.govt.nz/topic-and-industry/working-at-height/working-at-height-in-nz/'),
            ('WorkSafe — Notifying hazardous work', 'https://worksafe.govt.nz/notifications/hazardous-work/'),
            ('Site Safe — Site-specific safety plans', 'https://www.sitesafe.org.nz/products-and-services/sssp/'),
        ],
        cta=('Every job with its safety paperwork', 'Book a demo and we will show you a measure-up turning into a job, a risk assessment and a fitting.'),
    ),
]


# ============================================================================ South Africa
GUIDES['za'] = [
    dict(
        slug='sans-10400-n-safety-glazing', nav='SANS 10400-N safety glazing',
        blurb='What Part N of the building regulations asks of glazing, SANS 1263-1 and the NRCS mark on safety glass.',
        title='SANS 10400-N Safety Glazing Guide for South African Glaziers | Coglass',
        description='A plain-English guide to SANS 10400-N (Part N: Glazing) for South African glaziers: what regulation N1 requires, '
                    'SANS 1263-1 safety glazing, the NRCS VC 9003 mark, and keeping the specification right on every job.',
        h1='SANS 10400-N safety glazing: a guide for South African glaziers',
        lead='What Part N of the National Building Regulations asks of glazing, how SANS 1263-1 and the NRCS compulsory '
             'specification fit in, and a routine that keeps the right glass on the job.',
        sections=[
            ('What Part N requires', '''<p>Part N of the National Building Regulations deals with glazing. Regulation <strong>N1</strong> says glazing must be securely fixed and durable, withstand the wind loads it can expect, keep water out, and be visible to people walking towards it. It also says glass and plastics must give a level of safety suited to where the glazing is and how many people will be around it.</p>
<p>You are <em>deemed to satisfy</em> the regulation if the glazing material is <strong>selected, fixed and marked in accordance with SANS 10400-N</strong>. SANS 10137, the code of practice for installing glazing in buildings, is commonly specified alongside it.</p>'''),
            ('Where safety glazing comes in', '''<p>SANS 10400-N identifies the places where people are most likely to collide with glass and where safety glazing is needed — glass in doors and close to doors, low-level glass near the floor, and glass around baths and showers among them. The exact distances, heights and pane-size exceptions are set out in the standard; work from a current copy rather than a rule of thumb.</p>'''),
            ('Performance and marking: SANS 1263-1 and the NRCS', '''<p>Safety glazing must perform to <strong>SANS 1263-1</strong>, and each pane must be permanently marked so the mark can be seen after installation.</p>
<p>Safety glass is also covered by the National Regulator for Compulsory Specifications' compulsory specification <strong>VC 9003</strong> (in force since 16 July 2014). On top of the SANS 1263-1 marking, each pane must permanently carry an <strong>"NRCS"</strong> approval mark with its number, in letters at least 2.5 mm high. Checking that mark on delivery is a quick way to catch glass that should never have reached site.</p>'''),
            ('A routine that avoids the expensive mistake', '''<ol>
<li><strong>At the measure</strong>, note where each opening is — in or near a door, low down, by a bath or shower — and take a photo.</li>
<li><strong>When you quote</strong>, put the glass type and safety classification on the line, not just "clear".</li>
<li><strong>When you order</strong>, make sure the purchase order carries the same description.</li>
<li><strong>On delivery and on the day</strong>, check the SANS 1263-1 and NRCS marks before the glass goes in.</li>
</ol>'''),
        ],
        coglass_note='Coglass does not check your glass against SANS 10400-N — that stays with you and the standard. It keeps the specification consistent from measure to fitting:',
        coglass=[FIT_SURVEY, FIT_SPEC, FIT_DOCS],
        sources=[
            ('National Building Regulations — Regulation N1, type and fixing of glazing', 'https://www.acts.co.za/national-building/r2378_n1__type_and_fixing_of_g'),
            ('Government of South Africa — NRCS compulsory specification notices', 'https://www.gov.za/documents/notices/national-regulator-compulsory-specifications-act-compulsory-specification-40'),
        ],
        cta=('Keep the glass you quoted the glass you fit', 'Book a demo and we will show you a job going from measure to purchase order to fitting in Coglass.'),
    ),
    dict(
        slug='vat-tax-invoices', nav='VAT tax invoices',
        blurb='Full and abridged tax invoices, the R5,000 and R50 thresholds, and the 21-day rule.',
        title='VAT Tax Invoices for SA Glaziers: the R5,000 Rule | Coglass',
        description='What a South African VAT tax invoice must show: full versus abridged tax invoices, the R5,000 and R50 '
                    'thresholds, the 21-day rule and VAT at 15% — a guide for glaziers.',
        h1='VAT tax invoices: a guide for South African glaziers',
        lead='When you need a full tax invoice, when an abridged one will do, and what each must show — so your customers can '
             'claim their input VAT and SARS has nothing to query.',
        sections=[
            ('VAT at 15%', '''<p>The standard VAT rate in South Africa is <strong>15%</strong>. The increase to 15.5% announced for May 2025 was withdrawn in April 2025, and the February 2026 Budget left the rate unchanged.</p>'''),
            ('Full or abridged: the thresholds', '''<div class="table-wrap"><table>
<tr><th scope="col">Consideration (including VAT)</th><th scope="col">What you issue</th></tr>
<tr><td>R50 or less</td><td>No tax invoice needed — a till slip is acceptable.</td></tr>
<tr><td>More than R50, up to R5,000</td><td>An abridged tax invoice is allowed.</td></tr>
<tr><td>More than R5,000</td><td>A full tax invoice.</td></tr>
</table></div>
<p>A tax invoice must be issued within <strong>21 days</strong> of the supply.</p>'''),
            ('What a full tax invoice must show', '''<ul>
<li>the words "Tax Invoice", "VAT Invoice" or "Invoice";</li>
<li>your name, address and VAT registration number;</li>
<li>the customer's name, address and — where they have one — VAT registration number;</li>
<li>a serial number and the date of issue;</li>
<li>a description of the goods or services, with the quantity or volume;</li>
<li>the value of the supply, the VAT charged and the total.</li>
</ul>
<p>An abridged tax invoice can leave out the customer's details. Most glazing jobs for builders and companies are well over R5,000, so collect the customer's registered name, address and VAT number when you quote, not when you invoice.</p>'''),
        ],
        coglass_note='Coglass is not VAT-return software. It produces the invoices and hands them to Xero, where your VAT201 figures are prepared:',
        coglass=[FIT_INVOICES, FIT_XERO],
        sources=[
            ('SARS — Tax invoices', 'https://www.sars.gov.za/businesses-and-employers/government/tax-invoices/'),
            ('SAnews — Proposed VAT increase officially withdrawn', 'https://www.sanews.gov.za/south-africa/proposed-vat-increase-officially-withdrawn'),
        ],
        cta=('Invoices out, payments in, VAT in Xero', 'Book a demo and we will show you a job from deposit invoice to paid, and how it lands in Xero.'),
    ),
    dict(
        slug='power-cuts-offline-working', nav='Working through power cuts and dead spots',
        blurb='Keeping surveys, fittings and the workshop going when the power or the signal drops.',
        title='Glazing Through Power Cuts & No Signal in South Africa | Coglass',
        description='How Coglass keeps South African glaziers working when the power or signal drops: surveys and fitting sign-offs '
                    'saved on the phone, and a shop-floor iPad that keeps going when the workshop wifi is down.',
        h1='Working through power cuts and dead spots',
        lead='Load-shedding has been suspended since May 2025, but local outages, load reduction and patchy signal haven\'t gone '
             'away. Here is how to keep jobs moving when the connection doesn\'t.',
        sections=[
            ('Where things stand', '''<p>Eskom suspended load-shedding in May 2025, and by September 2026 it reported more than 470 days in a row without it. Local <strong>load reduction</strong> still affects some areas, and Eskom's target is to end it by March 2027. Add network dead spots on site and the odd router failure in the workshop, and any system that stops when the internet drops will cost you time.</p>'''),
            ('What actually needs to keep working', '''<ul>
<li><strong>On site</strong> — measuring, drawing and photographing openings, and signing off a fitting with the customer.</li>
<li><strong>In the workshop</strong> — seeing what to cut next and marking panes as made.</li>
<li><strong>In the office</strong> — less urgent: quotes and invoices can wait an hour, as long as nothing captured on site or at the bench is lost.</li>
</ul>'''),
            ('A sensible setup', '''<ul>
<li>Keep the office router and modem on a small UPS, so a short outage doesn't drop the connection.</li>
<li>Charge phones and tablets in the van and the workshop, and keep a power bank on every fitting team.</li>
<li>Use apps that save to the device first and sync later, rather than ones that need a live connection for every tap.</li>
</ul>'''),
        ],
        coglass_note='How Coglass behaves when the connection goes:',
        coglass=[FIT_OFFLINE, FIT_SURVEY,
                 '<strong>Nothing to re-type.</strong> Changes made offline queue on the device and sync on their own when the connection is back, with a visible banner while they are waiting.',
                 '<strong>The office web app needs a connection</strong> — it runs in the browser, so it waits for the power or the line to come back.'],
        sources=[
            ('Eskom — 2026 winter performance statement', 'https://www.eskom.co.za/eskom-fully-meets-2026-winter-demand-eaf-remains-at-its-highest-level-since-2020-67-79-and-diesel-expenditure-declines-by-r4-84-billion-or-81-64-to-deliver-energy-security/'),
            ('Eskom — Winter outlook statement', 'https://www.eskom.co.za/media-statement-winter-outlook-for-power-grid-again-predicts-no-loadshedding-system-stability-enables-key-energy-security-decisions-to-be-updated/'),
        ],
        cta=('See it work with the wifi off', 'Book a demo and we will show you a survey and a fitting captured offline and syncing afterwards.'),
    ),
]


def _distance_guide(c, slug, blurb, title, description, h1, lead, distances, intro, tax_h, tax, sources):
    rows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in distances)
    return dict(
        slug=slug, nav='Glazing jobs across long distances', blurb=blurb, title=title, description=description, h1=h1, lead=lead,
        sections=[
            ('The distances are the job', f'''<p>{intro}</p>
<div class="table-wrap"><table>
<tr><th scope="col">Route</th><th scope="col">Approximate road distance</th></tr>
{rows}
</table></div>
<p class="fine">Approximate distances by the main roads; check your route.</p>'''),
            ('Get the survey right first time', '''<p>When the site is hours away, a missed measurement or a forgotten photo means another day on the road. Capture everything on the first visit: every opening measured and drawn, photos of each one and of the access, and notes on what the fitting team will need. Then the quote, the glass order and the fitting all work from the same information.</p>'''),
            ('Make each trip count', '''<p>Group work by area: when a job is ready, look at what else is ready nearby before booking the trip, and fit a survey in on the way. Confirm the day with the customer before the van leaves, so nobody drives four hours to a locked gate.</p>'''),
            (tax_h, tax),
        ],
        coglass_note='Coglass is built for work spread over long distances:',
        coglass=[FIT_SURVEY,
                 '<strong>A planner for spread-out work.</strong> Drag surveys, fittings and deliveries onto people and vans, and see which ready jobs are near the day\'s other stops, scored by driving distance rather than a straight line.',
                 '<strong>Customers know when you are coming.</strong> Booking confirmations and on-the-way messages can go out by email, and customers can follow their job on a tracking page on their phone.',
                 FIT_XERO],
        sources=sources,
        cta=('See it on your own jobs', f'Book a demo and we will show you Coglass with the glass you sell and the distances you drive in {c}.'),
    )


# ============================================================================ Namibia
GUIDES['na'] = [
    _distance_guide(
        'Namibia', 'long-distance-glazing-jobs',
        'Surveys far from signal, planning trips from Windhoek to the coast and the south, and VAT basics.',
        'Long-Distance Glazing Jobs in Namibia | Coglass',
        'How Namibian glaziers can run jobs across long distances — Windhoek to Swakopmund, Walvis Bay and Lüderitz: offline '
        'surveys, planning trips and keeping customers informed. Plus VAT basics.',
        'Glazing jobs across long distances in Namibia',
        'When the next job is 360 km away, the survey has to be right first time and every trip has to count. Here is how to plan '
        'for it.',
        [('Windhoek – Swakopmund', 'about 360 km'), ('Windhoek – Walvis Bay', 'about 395 km'), ('Windhoek – Lüderitz', 'about 830–850 km')],
        'Namibian glaziers routinely cover distances that would cross several countries in Europe. A job at the coast is a full day '
        'from Windhoek, and a lot of the road between towns is out of mobile coverage.',
        'VAT basics in Namibia',
        '<p>VAT in Namibia is administered by the Namibia Revenue Agency (NamRA). The standard rate is <strong>15%</strong>, and '
        'registration is compulsory once your taxable supplies pass <strong>N$500,000</strong> in 12 months. Check the detail with '
        'NamRA or your accountant.</p>',
        [('Namibia Revenue Agency — Taxes', 'https://itas.namra.org.na/taxes'),
         ('PwC — Namibia tax reference and rate card (July 2026)', 'https://www.pwc.com/na/en/assets/pdf/namibia-tax-reference-and-rate-card-2026-july.pdf'),
         ('B1 road (Namibia)', 'https://en.wikipedia.org/wiki/B1_road_(Namibia)'),
         ('B2 road (Namibia)', 'https://en.wikipedia.org/wiki/B2_road_(Namibia)')],
    ),
]

# ============================================================================ Botswana
GUIDES['bw'] = [
    _distance_guide(
        'Botswana', 'long-distance-glazing-jobs',
        'Surveys far from signal, planning trips between Gaborone, Francistown and Maun, and VAT basics.',
        'Long-Distance Glazing Jobs in Botswana | Coglass',
        'How glaziers in Botswana can run jobs across long distances — Gaborone, Palapye, Francistown and Maun: offline surveys, '
        'planning trips and keeping customers informed. Plus VAT basics.',
        'Glazing jobs across long distances in Botswana',
        'When a job in Francistown is 435 km from the workshop, the survey has to be right first time and every trip has to count. '
        'Here is how to plan for it.',
        [('Gaborone – Palapye', 'about 270 km'), ('Gaborone – Francistown', 'about 435 km'), ('Francistown – Maun', 'about 480 km'),
         ('Gaborone – Maun', 'about 855 km')],
        'Glaziers in Botswana cover long stretches of the A1 and A3. A job in the north is a full day from Gaborone, and coverage '
        'between towns can be patchy.',
        'VAT basics in Botswana',
        '<p>VAT in Botswana is administered by the Botswana Unified Revenue Service (BURS). The standard rate is <strong>14%</strong> '
        '— it went back to 14% on 1 April 2023 after a temporary cut to 12% — and the new VAT Act that took effect on 1 July 2026 '
        'kept that rate. Check the detail with BURS or your accountant.</p>',
        [('Botswana Unified Revenue Service', 'https://burs.org.bw'),
         ('PwC tax summaries — Botswana, other taxes', 'https://taxsummaries.pwc.com/botswana/corporate/other-taxes'),
         ('KPMG — Botswana tax measures enacted (July 2026)', 'https://kpmg.com/us/en/taxnewsflash/news/2026/07/botswana-corporate-tax-dmtt-vat-enacted.html'),
         ('A1 road (Botswana)', 'https://en.wikipedia.org/wiki/A1_road_(Botswana)'),
         ('A3 road (Botswana)', 'https://en.wikipedia.org/wiki/A3_road_(Botswana)')],
    ),
]


# ============================================================================ United Kingdom
GUIDES['uk'] = [
    dict(
        slug='safety-glazing-approved-document-k', nav='Safety glazing: Approved Document K',
        blurb='Critical locations, BS EN 12600 classes, and the different rules in Wales, Scotland and Northern Ireland.',
        title='Safety Glazing: Approved Document K Guide for UK Glaziers | Coglass',
        description='A plain-English guide to safety glazing in critical locations for UK glaziers: Approved Document K in England, '
                    'BS EN 12600 classes, BS 6262-4, and the rules in Wales, Scotland and Northern Ireland.',
        h1='Safety glazing in critical locations: a guide for UK glaziers',
        lead='Where safety glass is needed under Approved Document K, what "break safely" means in BS EN 12600 terms, and how the rules '
             'differ in Wales, Scotland and Northern Ireland.',
        sections=[
            ('England: Approved Document K', '''<p>In England, glazing that people might walk into is covered by requirement K4 of the Building Regulations and by <strong>Approved Document K</strong> (2013 edition, in force since 6 April 2013), which absorbed the old Approved Document N. Section 5 defines the <strong>critical locations</strong>:</p>
<ul>
<li>glazing in a <strong>door</strong>, between floor level and 1500 mm;</li>
<li>glazing <strong>within 300 mm of the edge of a door</strong>, between floor level and 1500 mm;</li>
<li><strong>any other glazing</strong> between floor level and 800 mm — low-level glazing in walls and partitions.</li>
</ul>'''),
            ('What the glass in a critical location must do', '''<p>In a critical location, glazing should do one of three things:</p>
<ol>
<li><strong>Break safely</strong> — classified to <strong>BS EN 12600</strong> (the pendulum impact test) as <strong>Class 3</strong> or better, or Class C of BS 6206. For door and side-panel panes wider than 900 mm the bar is higher: Class 2 (or Class B).</li>
<li><strong>Be robust, or in small panes</strong> — for example annealed glass at least 6 mm thick in small panes, or 4 mm in traditional leaded lights, within the limits Approved Document K sets out.</li>
<li><strong>Be permanently protected</strong> — behind a screen or barrier that stops people falling against it.</li>
</ol>
<p>In practice that usually means toughened or laminated glass. Approved Document K also covers manifestation (making large panes visible) and safe opening and cleaning — read it in full for those.</p>'''),
            ('BS 6262-4', '''<p><strong>BS 6262-4</strong> is the British Standard code of practice for glazing safety related to human impact; the current edition is BS 6262-4:2018. It is the industry's detailed reference — the Scottish and Irish guidance cite it directly — even though England's Approved Document K works from the BS EN 12600 classes above.</p>'''),
            ('Wales, Scotland and Northern Ireland', '''<ul>
<li><strong>Wales</strong> didn't take England's 2013 merger: glazing safety is still in a Wales-only <strong>Approved Document N</strong>, alongside Wales's own Approved Document K.</li>
<li><strong>Scotland</strong> — Building Standards Technical Handbook, <strong>standard 4.8</strong>: glazing within 800 mm of the floor, any glazing in a door leaf, and glazing within 300 mm of a door leaf and within 1.5 m of the floor should meet BS 6262-4 or be guarded.</li>
<li><strong>Northern Ireland</strong> — <strong>Technical Booklet V</strong> (Glazing), covering regulations 96 to 99.</li>
</ul>'''),
            ('A routine that avoids the expensive mistake', '''<ol>
<li><strong>At the survey</strong>, record where each opening is — in or beside a door, low level, a bathroom — with a photo.</li>
<li><strong>When you quote</strong>, put the glass and its safety class on the line.</li>
<li><strong>When you order</strong>, make sure the purchase order carries the same description.</li>
<li><strong>On the day</strong>, check the safety-glass mark before it goes in.</li>
</ol>'''),
        ],
        coglass_note='Coglass gives guidance — it is not a sign-off, and the final choice stays with you:',
        coglass=[
            '<strong>A heads-up on the line.</strong> On the work bench, when a pane is larger than a quick-reference UK guide for its glass type and thickness, Coglass shows a note; and for larger annealed panes it reminds you that doors, side panels and low-level glazing normally need safety glass. Guidance only, never a hard stop.',
            '<strong>A safety-glazing library.</strong> Coglass comes with notes on doors, low-level glazing, side panels, shower and bath screens, balustrades and overhead glazing that you can edit, switch off or add to.',
            '<strong>Online sales checked.</strong> If you sell glass through the Coglass webshop, customers are asked where the glass is going: non-safety glass is blocked for doors, glass within 300 mm of a door, low-level glazing and bathrooms, and balustrades and overhead glass come to you as an enquiry.',
            FIT_SURVEY, FIT_SPEC],
        sources=[
            ('GOV.UK — Approved Document K: protection from falling, collision and impact', 'https://www.gov.uk/government/publications/protection-from-falling-collision-and-impact-approved-document-k'),
            ('legislation.gov.uk — Building Regulations 2010, Schedule 1', 'https://www.legislation.gov.uk/uksi/2010/2214/schedule/1'),
            ('BSI — BS 6262-4:2018', 'https://knowledge.bsigroup.com/products/glazing-for-buildings-code-of-practice-for-safety-related-to-human-impact'),
            ('Welsh Government — Approved Document N: glazing safety', 'https://www.gov.wales/approved-document-n-glazing-safety-relation-impact-opening-and-cleaning'),
            ('Scottish Government — Building Standards Technical Handbook (domestic), 4.8', 'https://www.gov.scot/publications/building-standards-technical-handbook-2022-domestic/4-safety/4-8-danger-accidents/'),
            ('Department of Finance NI — Technical Booklet V', 'https://www.finance-ni.gov.uk/publications/technical-booklet-v'),
        ],
        cta=('Keep the glass you quoted the glass you fit', 'Book a demo and we will show you a job going from survey to purchase order to fitting in Coglass.'),
    ),
    dict(
        slug='making-tax-digital-xero', nav='Making Tax Digital and Xero',
        blurb='MTD for VAT, the MTD for Income Tax dates for sole traders, and where your glazing software fits.',
        title='Making Tax Digital for Glaziers: VAT, Income Tax & Xero | Coglass',
        description='Making Tax Digital for UK glaziers: MTD for VAT, MTD for Income Tax from April 2026 (£50,000), 2027 (£30,000) '
                    'and 2028 (£20,000), and how job software and Xero fit together.',
        h1='Making Tax Digital: a guide for UK glaziers',
        lead='MTD for VAT already covers every VAT-registered glazier, and MTD for Income Tax started for sole traders in April 2026. '
             'Here is who is in, when, and where your job software fits.',
        sections=[
            ('MTD for VAT', '''<p>Since April 2022, <strong>every VAT-registered business</strong> — whatever its turnover — has had to keep VAT records digitally and file VAT returns through MTD-compatible software. For most glaziers that means accounting software such as Xero, fed by the invoices and bills the business raises.</p>'''),
            ('MTD for Income Tax: sole traders and landlords', '''<p>Making Tax Digital for Income Tax applies to sole traders and landlords according to their <strong>qualifying income</strong> — self-employment plus property income, before expenses:</p>
<div class="table-wrap"><table>
<tr><th scope="col">Qualifying income</th><th scope="col">MTD for Income Tax from</th></tr>
<tr><td>Over £50,000</td><td>6 April 2026 (based on the 2024–25 tax return)</td></tr>
<tr><td>Over £30,000</td><td>6 April 2027</td></tr>
<tr><td>Over £20,000</td><td>6 April 2028</td></tr>
</table></div>
<p>If you are in, you keep digital records and send HMRC quarterly updates through compatible software, then finalise the year. Limited companies are not in MTD for Income Tax. Check your own position with HMRC's eligibility checker or your accountant.</p>'''),
            ('Where job software fits', '''<p>The figures HMRC sees start life on your jobs: deposit invoices, final invoices, card payments, supplier bills for glass. The less re-typing between your job system and your accounts, the fewer errors at quarter end. The usual setup is a job system that raises the paperwork, connected to accounting software that holds the books and files with HMRC. Xero says it is recognised by HMRC for both MTD for VAT and MTD for Income Tax — HMRC now lists compatible software through its online finder.</p>'''),
        ],
        coglass_note='Coglass is not MTD filing software. It raises the paperwork and sends it to Xero, which files with HMRC:',
        coglass=[FIT_INVOICES, FIT_XERO,
                 '<strong>Customers pay by card</strong> from the invoice link when you connect your own Stripe account, and the payment is recorded on the invoice.',
                 '<strong>VAT invoices</strong> with your VAT number, with UK VAT at 20%.'],
        sources=[
            ('GOV.UK — Making Tax Digital for VAT', 'https://www.gov.uk/government/news/making-tax-digital-for-vat-is-coming-are-you-ready'),
            ('GOV.UK — Check if you\'re eligible for Making Tax Digital for Income Tax', 'https://www.gov.uk/guidance/check-if-youre-eligible-for-making-tax-digital-for-income-tax'),
            ('GOV.UK — Find software for Making Tax Digital for Income Tax', 'https://www.gov.uk/guidance/find-software-thats-compatible-with-making-tax-digital-for-income-tax'),
            ('Xero — Making Tax Digital', 'https://www.xero.com/uk/programme/making-tax-digital/income-tax/'),
        ],
        cta=('From invoice to Xero without re-typing', 'Book a demo or start a 14-day trial and connect your Xero organisation.'),
    ),
    dict(
        slug='van-mot-reminders', nav='Van MOTs and reminders',
        blurb='When vans need an MOT, Class 4 versus Class 7, the £1,000 fine, and never missing a due date.',
        title='Van MOT Rules & Reminders for Glazing Companies | Coglass',
        description='MOT rules for glazing vans in the UK: first MOT at three years, Class 4 and Class 7 vans, testing early, the '
                    '£1,000 fine — and MOT reminders for the whole fleet in Coglass.',
        h1='Van MOTs: a guide for glazing companies',
        lead='A van off the road is a fitting that doesn\'t happen. Here are the MOT rules for glazing vans, and how to make sure a '
             'due date never slips past.',
        sections=[
            ('When a van needs an MOT', '''<p>In Great Britain a van needs its first MOT by the <strong>third anniversary of its registration</strong>, then every year. Vans in Northern Ireland are also first tested at three years (it is cars that wait until four there), under the NI testing scheme.</p>'''),
            ('Class 4 or Class 7', '''<div class="table-wrap"><table>
<tr><th scope="col">Van</th><th scope="col">MOT class</th><th scope="col">Maximum fee</th></tr>
<tr><td>Goods vehicle up to 3,000 kg design gross weight</td><td>Class 4</td><td>£54.85</td></tr>
<tr><td>Goods vehicle over 3,000 kg, up to 3,500 kg</td><td>Class 7</td><td>£58.60</td></tr>
</table></div>
<p>Glazing vans with an A-frame and a full load of glass are often in the heavier bracket — check the plated weight, and book a garage that tests Class 7 if you need one.</p>'''),
            ('Book early, keep the date', '''<p>You can have the MOT up to <strong>one month (minus a day)</strong> before it is due and keep the same renewal date — so there's no reason to leave it to the last week. Driving without a valid MOT can mean a fine of up to <strong>£1,000</strong>, and it can affect your insurance. GOV.UK runs a free reminder service by text or email, a month before each due date.</p>'''),
            ('Running a fleet', '''<p>With several vans, the dates spread across the year and get lost. Keep them in one list with the paperwork, decide who books them, and give yourself a series of nudges rather than a single reminder.</p>'''),
        ],
        coglass_note='Coglass keeps the fleet with the jobs:',
        coglass=[
            '<strong>MOT dates for every van</strong>, flagged OK, due soon or overdue, with the certificates stored on the vehicle.',
            '<strong>Reminders that escalate.</strong> Set, per van, how many days ahead and how many nudges; Coglass reminds the team in its notifications as the date approaches, on the day, and if it lapses.',
            '<strong>Log each MOT</strong> with the date it was done and the next due date, so the reminders count down to the right day.',
            '<strong>Vans on the planner.</strong> Put a van with each person for the day, or let staff pick theirs on the phone — with a history of who drove what, and when.'],
        sources=[
            ('GOV.UK — When to get an MOT', 'https://www.gov.uk/getting-an-mot/when-to-get-an-mot'),
            ('GOV.UK — MOT test fees', 'https://www.gov.uk/getting-an-mot/mot-test-fees'),
            ('GOV.UK — Get an MOT reminder', 'https://www.gov.uk/mot-reminder'),
            ('nidirect — How the MOT scheme works', 'https://www.nidirect.gov.uk/articles/how-mot-scheme-works'),
        ],
        cta=('Keep every van on the road', 'Book a demo or start a 14-day trial and add your fleet.'),
    ),
]

# ============================================================================ Ireland
GUIDES['ie'] = [
    dict(
        slug='safety-glazing-tgd-d', nav='Safety glazing: TGD D and BS 6262-4',
        blurb='Where safety glazing is needed under the Irish Building Regulations, and how TGD D and TGD K fit together.',
        title='Safety Glazing in Ireland: TGD D & BS 6262-4 | Coglass',
        description='A plain-English guide to safety glazing in Ireland: critical locations under Technical Guidance Document D, '
                    'BS 6262-4, glazing used as guarding under TGD K — for Irish glaziers.',
        h1='Safety glazing in Ireland: a guide for Irish glaziers',
        lead='Which Technical Guidance Document covers safety glazing in Ireland, where it is needed, and a routine that keeps the '
             'right glass on the job.',
        sections=[
            ('It\'s in TGD D, not TGD K', '''<p>In Ireland, the main guidance on safety glazing is <strong>Technical Guidance Document D</strong> (Materials and Workmanship, 2013), paragraph 1.5 — not TGD K, as people often assume. TGD D says unguarded glazing in <strong>critical locations</strong> should be safety glazing in line with the recommendations of <strong>BS 6262-4</strong>.</p>
<p><strong>TGD K</strong> (Stairways, Ladders, Ramps and Guards, 2014) deals with glazing only where it forms guarding — a glass balustrade or a screen protecting a drop — again by reference to BS 6262-4, and points back to TGD D for safety glazing generally.</p>'''),
            ('The critical locations', '''<p>TGD D's diagram follows the same layout as England's Approved Document K. In plain terms, the critical locations are:</p>
<ul>
<li>glazing in <strong>doors</strong>;</li>
<li>glazing in <strong>side panels beside doors</strong>;</li>
<li><strong>low-level glazing</strong> in walls and partitions.</li>
</ul>
<p>The exact heights and widths are in the diagram in TGD D and in BS 6262-4. Glazing in those zones that isn't guarded should be safety glazing — in practice, toughened or laminated glass.</p>'''),
            ('A routine that avoids the expensive mistake', '''<ol>
<li><strong>At the survey</strong>, note where each opening is — in or beside a door, low down, on a stairway or landing — with a photo.</li>
<li><strong>When you quote</strong>, put the glass and its safety class on the line, not just "clear".</li>
<li><strong>When you order</strong>, make sure the purchase order carries the same description.</li>
<li><strong>On the day</strong>, check the safety-glass mark, and keep a photo for the job file — useful for grant paperwork too.</li>
</ol>'''),
        ],
        coglass_note='Coglass doesn\'t sign off safety glazing for you — that stays with you and the guidance. It keeps the specification consistent from survey to fitting:',
        coglass=[FIT_SURVEY, FIT_SPEC, FIT_DOCS],
        sources=[
            ('gov.ie — Technical Guidance Document D (Materials and Workmanship), 2013', 'https://assets.gov.ie/100165/51323749-83aa-4710-81b2-78ef100672f2.pdf'),
            ('gov.ie — Technical Guidance Document K', 'https://www.gov.ie/en/publication/6b632-technical-guidance-document-k-stairways-ladders-ramps-and-guards'),
            ('BSI — BS 6262-4', 'https://knowledge.bsigroup.com/products/glazing-for-buildings-code-of-practice-for-safety-related-to-human-impact'),
        ],
        cta=('Keep the glass you quoted the glass you fit', 'Book a demo and we will show you a job going from survey to purchase order to fitting in Coglass.'),
    ),
    dict(
        slug='vat-rct-eircodes', nav='VAT, RCT and Eircodes',
        blurb='13.5% or 23%, the two-thirds rule, RCT and the reverse charge, and Eircodes on every job.',
        title='VAT, RCT & Eircodes for Irish Glaziers | Coglass',
        description='VAT, RCT and Eircodes for Irish glaziers: 13.5% for supply-and-fit, 23% for goods, the two-thirds rule, '
                    'Relevant Contracts Tax and the VAT reverse charge, and keeping Eircodes on every job.',
        h1='VAT, RCT and Eircodes: a guide for Irish glaziers',
        lead='The two VAT rates on glazing work, when the two-thirds rule changes the rate, how RCT and the reverse charge work for '
             'subcontractors — and why every job should carry its Eircode.',
        sections=[
            ('Two VAT rates', '''<p>Irish glazing work usually involves two VAT rates. Supplying <em>and installing</em> fixtures — construction services — is generally at the reduced rate of <strong>13.5%</strong>. Supplying building materials on their own (glass collected or delivered, not fitted) is at the standard rate of <strong>23%</strong>, as is scaffolding.</p>'''),
            ('The two-thirds rule', '''<p>On a supply-and-fit job, if the <strong>cost of the goods</strong> you use (excluding VAT) is more than <strong>two-thirds</strong> of the total VAT-exclusive price, the goods rate — 23% — applies to the whole job. That can catch a job where the glass is expensive and the fitting is quick. Note it is the <em>cost</em> of the goods to you, not what you charge for them. The rule doesn't apply where the RCT reverse charge applies, or between connected persons.</p>'''),
            ('RCT and the VAT reverse charge', '''<p><strong>Relevant Contracts Tax</strong> applies when a principal contractor pays a subcontractor for construction work. The principal deducts RCT at <strong>0%, 20% or 35%</strong>, depending on the subcontractor's record with Revenue, and all of it runs through Revenue Online Service (ROS).</p>
<p>Where RCT applies, the <strong>VAT reverse charge</strong> applies too: as the subcontractor you invoice without VAT and add the line <em>"VAT on this supply to be accounted for by the principal contractor"</em>, and the principal accounts for the VAT. A glazier working for a builder on one job and a homeowner on the next deals with both kinds of invoice.</p>'''),
            ('Eircodes on every job', '''<p>Every Irish address has a seven-character <strong>Eircode</strong>: a three-character routing key for the area, and a four-character identifier unique to the address — for example <em>A65 F4E2</em>. On rural jobs, where several houses share a townland name, the Eircode is what gets the fitter to the right door. Take it at the enquiry and keep it with the site address.</p>'''),
        ],
        coglass_note='What Coglass does today. RCT deductions and returns are done on ROS, not in Coglass:',
        coglass=[
            '<strong>Eircodes on addresses.</strong> On an Irish account, customer and site addresses have an Eircode field with a format check, and a county picker.',
            FIT_INVOICES, FIT_XERO, FIT_SURVEY],
        sources=[
            ('Revenue — VAT on construction services (Tax and Duty Manual)', 'https://www.revenue.ie/en/tax-professionals/tdm/value-added-tax/part11-immovable-goods/construction-services/construction-servcies.pdf'),
            ('Revenue — The two-thirds rule', 'https://www.revenue.ie/en/vat/vat-on-services/two-thirds-rule/index.aspx'),
            ('Revenue — Relevant Contracts Tax', 'https://www.revenue.ie/en/self-assessment-and-self-employment/rct/index.aspx'),
            ('Revenue — Reverse charge (self-accounting)', 'https://www.revenue.ie/en/vat/what-is-vat/reverse-charge-self-accounting.aspx'),
            ('Eircode — What is Eircode?', 'https://www.eircode.ie/what-is-eircode'),
        ],
        cta=('Every job with the right address', 'Book a demo and we will show you Coglass with the glass you sell and the way you work in Ireland.'),
    ),
]
