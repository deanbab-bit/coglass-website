"""Country sections: one entry per country site (/uk/, /ie/, /au/, …).

LAUNCH-DAY SWITCH
-----------------
`SUBSCRIBE` below decides, per country, whether the plan buttons go to card checkout on
accounts.coglass.co.uk ("Start 14-day trial") or to the demo form ("Book a demo").
The accounts site only bills in GBP today, so every country except the UK is False.
On launch day, once accounts.coglass.co.uk has Stripe prices in that currency, flip the
country to True and re-run `python3 _src/build.py`. Nothing else needs to change.

`WHATSAPP_LIVE` does the same for the WhatsApp wording: False = "coming soon, waiting on
Meta's approval" (true today, see DECISIONS.md D15); True = WhatsApp described as live.

`PORTAL_LIVE` / `WEBSHOP_LIVE` do the same for the customer portal and the webshop: False =
"coming soon, included in your plan when it launches" (Dean, 9 Oct 2026 — both are off in the
app until their PORTAL_LIVE / WEBSHOP_LIVE instance switch is on); True = described as live.
In the JSON content, write `{{portal::live text::soon text}}` or `{{webshop::live text::soon text}}`
(see launch_text below); in Python, `portal(live, soon)` / `shop(live, soon)`.

Content rules (see the PR): only claim what the app does today or what the region/tax
launch PRs deliver. Values marked `unconfirmed` in the app's src/lib/region.ts (NA, BW, MT
standards, phone ranges, bank fields…) are deliberately NOT mentioned here.
"""

SUBSCRIBE = {
    'uk': True,
    'ie': False,
    'au': False,
    'nz': False,
    'za': False,
    'na': False,
    'bw': False,
    'mt': False,
}

WHATSAPP_LIVE = False
PORTAL_LIVE = False
WEBSHOP_LIVE = False

# The one line used wherever both are mentioned together while they're coming soon.
PORTAL_SHOP_SOON = 'The customer portal and the online shop are coming soon, and will be included in your plan when they launch.'

ORDER = ['uk', 'ie', 'au', 'nz', 'za', 'na', 'bw', 'mt']

# Plan allowances are the same in every country; only the price changes.
PLAN_LINES = {
    'starter': ['1 office login', '3 fitters on the phone app', '150 orders a month', '1 email inbox', '1 shop-floor device', '100 SMS a month', 'Unlimited AI glass scans'],
    'professional': ['3 office logins', '8 fitters on the phone app', '500 orders a month', '3 email inboxes', '2 shop-floor devices', '300 SMS a month', 'Unlimited AI glass scans'],
    'business': ['7 office logins', '12 fitters on the phone app', '1,500 orders a month', '7 email inboxes', '4 shop-floor devices', '750 SMS a month', 'Unlimited AI glass scans'],
}
PLAN_NAMES = [('Starter', 'starter', False), ('Professional', 'professional', True), ('Business', 'business', False)]


def wa(live, soon):
    return live if WHATSAPP_LIVE else soon


def portal(live, soon):
    return live if PORTAL_LIVE else soon


def shop(live, soon):
    return live if WEBSHOP_LIVE else soon


def portal_shop_soon_sentence():
    """One sentence for whichever of the two is still coming soon ('' once both are live)."""
    if not PORTAL_LIVE and not WEBSHOP_LIVE:
        return PORTAL_SHOP_SOON
    if not PORTAL_LIVE:
        return 'The customer portal is coming soon, and will be included in your plan when it launches.'
    if not WEBSHOP_LIVE:
        return 'The online shop is coming soon, and will be included in your plan when it launches.'
    return ''


def feature_live(key):
    """Is this feature (FEATURES key / page slug part) live? Unknown keys are live."""
    if key in ('portal', 'customer-portal', 'coglass-feature-customer-portal'):
        return PORTAL_LIVE
    if key in ('webshop', 'coglass-feature-webshop'):
        return WEBSHOP_LIVE
    return True


_LAUNCH = __import__('re').compile(r'\{\{(portal|webshop)::(.*?)::(.*?)\}\}', __import__('re').S)


def launch_text(s):
    """`{{portal::live::soon}}` / `{{webshop::live::soon}}` → the text for today's switch."""
    if not isinstance(s, str):
        return s
    return _LAUNCH.sub(lambda m: m.group(2) if (PORTAL_LIVE if m.group(1) == 'portal' else WEBSHOP_LIVE) else m.group(3), s)


def launch_data(v):
    """launch_text over a whole content JSON value (strings, lists, dicts)."""
    if isinstance(v, str):
        return launch_text(v)
    if isinstance(v, list):
        return [launch_data(x) for x in v]
    if isinstance(v, dict):
        return {k: launch_data(x) for k, x in v.items()}
    return v


def _wa_point(where):
    return ('WhatsApp-first messaging',
            wa(f'Booking confirmations, on-the-way messages and quotes go out on WhatsApp — the way customers in {where} '
               'expect to hear from you — with replies landing on the job.',
               f'Customers in {where} would rather WhatsApp than text. WhatsApp messaging is built into Coglass and waiting on '
               "Meta's approval; until it switches on, email, SMS and the chat on your quote and tracking pages work today."))


def _wa_faq(where):
    return ('Can I message customers on WhatsApp?',
            wa(f'Yes. WhatsApp is the default way Coglass messages customers in {where}: booking confirmations, on-the-way '
               'messages and quotes, with replies in your inbox and on the job.',
               "WhatsApp is built and waiting on Meta's approval, so it's coming soon. Until then you can reach customers by "
               'email, SMS and the chat on your quote and tracking pages.'))


OFFLINE_FAQ = ('Does the phone app work without signal?',
               'Yes. Surveys — measurements, drawings, photos, access notes and GPS — and fitting sign-offs are saved on the '
               'phone and sync when you are back in signal. The shop-floor iPad app also keeps working if the workshop wifi '
               'drops. The office web app needs an internet connection.')

XERO_FAQ = ('Does it work with Xero?',
            'Yes. Invoices, payments and supplier bills push to Xero, coded to the accounts and tax rates you choose from '
            'your own Xero organisation.')

C = {}

# ----------------------------------------------------------------------------- United Kingdom
C['uk'] = dict(
    code='GB', slug='uk', name='United Kingdom', short='UK', in_name='the UK', lang='en-GB', og_locale='en_GB',
    hreflang=['en-GB', 'en-IM', 'en-JE', 'en-GG', 'en-GI'],
    currency='GBP', sym='£', prices={'starter': '£89', 'professional': '£199', 'business': '£399'},
    num={'starter': 89, 'professional': 199, 'business': 399}, inbox='£7.50', tax='VAT', per='per month + VAT',
    price_tax=' + VAT', tax_short='+ VAT',
    price_basis='Prices exclude VAT.',
    eyebrow='Built for UK glass &amp; glazing companies',
    h1='Every job, from enquiry to paid.',
    lead='Quotes with real glass drawings, a planner your fitters actually use, purchase orders to suppliers, and VAT invoices '
         'that look the part. One system for the office, the van and the workshop.',
    title='Coglass UK | Glazing Software for Glaziers, Glass Merchants & Sealed Unit Makers',
    description='Quotes with real glass drawings, surveys, production, supplier POs, fitting and VAT invoicing for UK glass and '
                'glazing companies. From £89 a month + VAT. Covers the Isle of Man, Jersey, Guernsey and Gibraltar.',
    why_h2='Why UK glaziers choose Coglass',
    why=[
        ('Drawn, priced and ordered properly', 'Shapes, holes, cut-outs, Georgian bars and leaded lights drawn to size in mm — '
         'the same drawing prices the line and goes on the quote, the supplier PO and the cutting sheet.'),
        ('VAT invoices and Xero', 'Deposit, proforma and final invoices with your VAT number, payments recorded, and everything '
         'pushed to Xero. Customers can pay by card from the invoice link.'),
        ('Texts under your company name', 'Booking confirmations and on-the-way texts go out from your own business name, '
         'with email and the quote-page chat alongside.'),
        ('Safety glazing in critical locations', 'Guidance for critical locations based on Approved Document K and BS 6262-4, '
         'right where you specify the glass.'),
        ('Fitters who use it', 'Today\'s jobs, surveys drawn on the phone, per-pane sign-off with photos and a signature — and it '
         'keeps working with no signal.'),
        ('A UK team', 'Coglass is made by Halliday Morrow Ltd in England. Talk to the people who build it, during UK business hours.'),
    ],
    proof=[('From £89', 'a month + VAT'), ('Every feature', 'on every plan'), ('No setup fee', 'no minimum term'), ('UK team', 'made in England')],
    support='Our team is in the UK. Email or call during UK business hours and we usually reply within one working day; '
            'inside Coglass there is also a chat button.',
    tz_note=None,
    tax_notes=[
        'All prices exclude VAT, which is added at the UK rate (currently 20%).',
    ],
    # (name, accounts-site country code for /subscribe?country=…, how we bill there)
    crown=[
        ('Isle of Man', 'im', 'The Isle of Man is in the UK VAT area, so UK VAT is added at 20% as it is in the UK.'),
        ('Jersey', 'je', 'Jersey is outside the UK VAT area, so no UK VAT is added for a Jersey business. Jersey GST is a local tax; '
                   'check with your accountant whether you need to account for it.'),
        ('Guernsey', 'gg', 'Guernsey is outside the UK VAT area and has no VAT or GST, so no UK VAT is added for a Guernsey business.'),
        ('Gibraltar', 'gi', 'Gibraltar is outside the UK VAT area and has no VAT, so no UK VAT is added for a Gibraltar business.'),
    ],
    faq=[
        ('Is Coglass built for UK glass and glazing companies?', 'Yes. It holds full IGU make-ups (DGU/TGU, cavity, spacer, gas), '
         'every edge and shape, and a drawing canvas for holes, Georgian bars, lead and diamond — plus a 1:1 lay-under template '
         'the factory copies onto the glass. It is not a general CRM adapted to glass.'),
        ('Do you cover the Isle of Man, Jersey, Guernsey and Gibraltar?', 'Yes — they are covered by the UK site and priced in '
         'pounds. The Isle of Man is in the UK VAT area, so UK VAT is added; for businesses in Jersey, Guernsey and Gibraltar no '
         'UK VAT is added. When you sign up, choose your island or Gibraltar as the country — the pricing page has a link for '
         'each.'),
        ('How does the trial work?', 'Pick a plan on the pricing page. We take your card at sign-up and charge nothing for 14 '
         'days; cancel before the trial ends and you pay nothing. If you would rather see it first, book a demo.'),
        XERO_FAQ,
        OFFLINE_FAQ,
        ('Can you help us set it up?', 'Yes — book a demo and we will go through your products, prices and team with you. There '
         'is no setup fee.'),
        _wa_faq('the UK'),
    ],
)

# ----------------------------------------------------------------------------- Ireland
C['ie'] = dict(
    code='IE', slug='ie', name='Ireland', short='Ireland', in_name='Ireland', lang='en-IE', og_locale='en_IE',
    hreflang=['en-IE'],
    currency='EUR', sym='€', prices={'starter': '€109', 'professional': '€239', 'business': '€469'},
    num={'starter': 109, 'professional': 239, 'business': 469}, inbox='€9.00', tax='VAT', per='per month, no VAT added',
    price_tax=', no VAT added', tax_short='No VAT added',
    price_basis='No VAT added — prices are for VAT-registered businesses (reverse charge).',
    eyebrow='Built for glaziers in Ireland',
    h1='Glazing software for Irish glaziers — from enquiry to paid.',
    lead='Quotes priced in euro with the glass drawn on every line, surveys on the phone even where there is no signal, supplier '
         'orders, scheduling and invoices. One system for the office, the van and the workshop.',
    title='Coglass Ireland | Glazing Software for Irish Glaziers & Glass Merchants',
    description='Glazing software for Irish glaziers: quotes in euro with glass drawings, offline surveys, supplier orders, '
                'scheduling, Irish VAT invoices and Xero. From €109 a month for VAT-registered businesses, no VAT added.',
    why_h2='Why Coglass suits glaziers in Ireland',
    why=[
        ('Euro quotes and Irish VAT', 'Quotes and invoices in euro, with your VAT number on them and the Irish VAT rates — '
         '13.5% for supply-and-fit work and 23% for supply only.'),
        ('Eircode on every address', 'Keep the Eircode with each customer and site address, so it is on the job for the '
         'fitter heading out to a rural address.'),
        ('Grant jobs kept together', 'For SEAI windows and doors grant work, keep the survey, photos, Declarations of '
         'Performance and other paperwork on the job, ready for the claim.'),
        _wa_point('Ireland'),
        ('Surveys with no signal', 'Measure, draw and photograph every opening on the phone. It all syncs when you are back in '
         'coverage.'),
        ('Xero, set up your way', 'Invoices, payments and supplier bills push to your Xero organisation, coded to your own '
         'accounts and VAT rates.'),
    ],
    proof=[('From €109', 'a month, no VAT added'), ('Hosted in the EU', 'data held in Germany'), ('Same clock', 'as our UK team'), ('iPhone · Android · web', '')],
    support='Our team is in the UK, on the same clock as Ireland. Email or call during business hours and we usually reply '
            'within one working day; inside Coglass there is also a chat button.',
    tz_note=None,
    # TODO(OSS): once the EU non-Union OSS registration is in Stripe Tax, buyers without a VAT number can be
    # sold to again (Irish VAT at 23% added at checkout). Then restore the "No VAT number? You can still sign up"
    # line below, the matching FAQ sentence, and the per/price_tax/price_basis wording above ("+ VAT").
    tax_notes=[
        'Coglass is sold to VAT-registered businesses by Halliday Morrow Ltd, a UK company. No VAT is added to our prices.',
        'Give us your Irish VAT number when you sign up (we check it on the EU VIES register): no VAT is added to our '
        'invoice and you account for it yourself under the reverse charge.',
    ],
    sms_note='Irish SMS sender IDs must be registered with ComReg before texts show your business name; until yours is, '
             'use email or the quote-page chat.',
    faq=[
        ('Can I use Coglass in Ireland?', 'Yes. Coglass is sold in Ireland in euro, and quotes and invoices go out in euro with '
         'Irish VAT.'),
        ('How is VAT handled on my Coglass subscription?', 'Coglass is sold to VAT-registered businesses. Give us your Irish VAT '
         'number when you sign up: no VAT is added to our invoice — you account for it under the reverse charge. For now you '
         'need a VAT number to subscribe.'),
        ('Which VAT rates can I use on my own quotes?', 'Irish glazing work usually needs two: 13.5% for supply-and-fit and 23% '
         'for supply only. Both are available, so each job can carry the rate that applies to it.'),
        ('Where is my data held?', 'In the EU — on servers in Germany.'),
        ('What hours is support?', 'Our team is in the UK, on the same time as Ireland. Email or call during business hours; we '
         'usually reply within one working day.'),
        _wa_faq('Ireland'),
        OFFLINE_FAQ,
        XERO_FAQ,
    ],
)

# ----------------------------------------------------------------------------- Australia
C['au'] = dict(
    code='AU', slug='au', name='Australia', short='Australia', in_name='Australia', lang='en-AU', og_locale='en_AU',
    hreflang=['en-AU'],
    currency='AUD', sym='A$', prices={'starter': 'A$169', 'professional': 'A$379', 'business': 'A$759'},
    num={'starter': 169, 'professional': 379, 'business': 759}, inbox='A$14.50', tax='GST', per='per month, no GST added',
    price_tax=', no GST added', tax_short='No GST added',
    price_basis='No GST added — prices are for GST-registered businesses with an ABN.',
    eyebrow='Built for glaziers in Australia',
    h1='Glazing software for Australian glaziers — quote, fit and get paid.',
    lead='Quotes with the glass drawn on every line, surveys on the phone even out of range, purchase orders to suppliers, '
         'scheduling and GST tax invoices. One system for the office, the ute and the workshop.',
    title='Coglass Australia | Glazing Software for Australian Glaziers',
    description='Glazing software for Australian glaziers: quotes with glass drawings, offline surveys, supplier orders, '
                'scheduling, GST tax invoices with your ABN, and Xero. From A$169 a month for GST-registered businesses, no GST added.',
    why_h2='Why Coglass suits glaziers in Australia',
    why=[
        ('GST tax invoices', 'Invoices headed "Tax invoice", with your ABN and GST at 10% — and quotes in Australian dollars.'),
        ('Safety glass clearly specified', 'For AS 1288 work, put the glass and its AS/NZS 2208 safety-glass grade on the line '
         'itself, so the quote, the purchase order and the job sheet all agree.'),
        ('Surveys out of range', 'Measure, draw and photograph every opening on the phone, wherever the job is. It syncs '
         'when you are back in coverage.'),
        ('Customers pay by card', 'Connect your Stripe account and customers can pay an invoice by card from its link.'),
        ('Xero, set up your way', 'Invoices, payments and supplier bills push to your Xero organisation, coded to your own '
         'accounts and GST rates.'),
        ('Drawn and priced properly', 'Shapes, holes, cut-outs and IGU make-ups drawn to size in mm, priced from your own '
         'catalogue and trade price lists.'),
    ],
    proof=[('From A$169', 'a month, no GST added'), ('Every feature', 'on every plan'), ('No setup fee', 'no minimum term'), ('iPhone · Android · web', '')],
    support='Our team is in the UK. Australian business hours overlap our early morning and late evening — the east coast is '
            '9 to 11 hours ahead of the UK, depending on the season and your state. Email any time and we usually reply within '
            'one UK working day; we will agree a demo time that suits you.',
    tz_note='The east coast is 9 to 11 hours ahead of the UK (Perth 7 to 8).',
    tax_notes=[
        'Coglass is sold to GST-registered businesses by Halliday Morrow Ltd, a UK company. No GST is added to our prices.',
        'Give us your ABN when you sign up and confirm your business is registered for GST.',
    ],
    faq=[
        ('Can I use Coglass in Australia?', 'Yes. Coglass is sold in Australia in Australian dollars, to GST-registered businesses.'),
        ('Will my invoices say "Tax invoice" and show my ABN?', 'Yes. Invoices are headed "Tax invoice" and show your ABN and the '
         'GST at 10%.'),
        ('Is my Coglass subscription charged GST?', 'No GST is added. Coglass is sold to GST-registered businesses: give us your '
         'ABN when you sign up and confirm you are registered for GST.'),
        ('What hours is support?', 'Our team is in the UK, which is 9 to 11 hours behind the east coast. Email any time and we '
         'usually reply within one UK working day; demos are booked at a time that suits you.'),
        OFFLINE_FAQ,
        XERO_FAQ,
        ('Can customers pay online?', 'Yes. Connect your Stripe account and customers can pay an invoice by card from its link.'),
    ],
)

# ----------------------------------------------------------------------------- New Zealand
C['nz'] = dict(
    code='NZ', slug='nz', name='New Zealand', short='New Zealand', in_name='New Zealand', lang='en-NZ', og_locale='en_NZ',
    hreflang=['en-NZ'],
    currency='NZD', sym='NZ$', prices={'starter': 'NZ$209', 'professional': 'NZ$469', 'business': 'NZ$939'},
    num={'starter': 209, 'professional': 469, 'business': 939}, inbox='NZ$17.50', tax='GST', per='per month, no GST added',
    price_tax=', no GST added', tax_short='No GST added',
    price_basis='No GST added — prices are for GST-registered businesses.',
    eyebrow='Built for glaziers in New Zealand',
    h1='Glazing software for New Zealand glaziers.',
    lead='Quotes with the glass drawn on every line, surveys on the phone even out of coverage, purchase orders to suppliers, '
         'scheduling and GST invoices. One system for the office, the van and the workshop.',
    title='Coglass New Zealand | Glazing Software for NZ Glaziers',
    description='Glazing software for New Zealand glaziers: quotes with glass drawings, offline surveys, supplier orders, '
                'scheduling, GST invoices and Xero. From NZ$209 a month for GST-registered businesses, no GST added.',
    why_h2='Why Coglass suits glaziers in New Zealand',
    why=[
        ('GST at 15%', 'Quotes and invoices in New Zealand dollars, with your GST number and GST at 15%.'),
        ('Safety glass clearly specified', 'For NZS 4223.3 work, put the glass and its safety-glass grade on the line itself, '
         'so the quote, the purchase order and the job sheet all agree.'),
        _wa_point('New Zealand'),
        ('Surveys out of coverage', 'Measure, draw and photograph every opening on the phone, wherever the job is. It syncs '
         'when you are back in coverage.'),
        ('Xero, set up your way', 'Invoices, payments and supplier bills push to your Xero organisation, coded to your own '
         'accounts and GST rates.'),
        ('Customers pay by card', 'Connect your Stripe account and customers can pay an invoice by card from its link.'),
    ],
    proof=[('From NZ$209', 'a month, no GST added'), ('Every feature', 'on every plan'), ('No setup fee', 'no minimum term'), ('iPhone · Android · web', '')],
    support='Our team is in the UK, 11 to 13 hours behind New Zealand depending on the season, so our working day is your '
            'evening and night. Email any time and we usually reply within one UK working day; we will agree a demo time that '
            'suits you.',
    tz_note='New Zealand is 11 to 13 hours ahead of the UK.',
    tax_notes=[
        'Coglass is sold to GST-registered businesses by Halliday Morrow Ltd, a UK company. No GST is added to our prices.',
        'Give us your GST number when you sign up.',
    ],
    faq=[
        ('Can I use Coglass in New Zealand?', 'Yes. Coglass is sold in New Zealand in NZ dollars, to GST-registered businesses.'),
        ('Do my invoices show GST?', 'Yes — your GST number and GST at 15%, with quotes and invoices in NZ dollars.'),
        ('Is my Coglass subscription charged GST?', 'No GST is added. Coglass is sold to GST-registered businesses: give us your '
         'GST number when you sign up.'),
        ('What hours is support?', 'Our team is in the UK, 11 to 13 hours behind you. Email any time and we usually reply within '
         'one UK working day; demos are booked at a time that suits you.'),
        _wa_faq('New Zealand'),
        OFFLINE_FAQ,
        XERO_FAQ,
    ],
)

# ----------------------------------------------------------------------------- South Africa
C['za'] = dict(
    code='ZA', slug='za', name='South Africa', short='South Africa', in_name='South Africa', lang='en-ZA', og_locale='en_ZA',
    hreflang=['en-ZA'],
    currency='ZAR', sym='R', prices={'starter': 'R1,969', 'professional': 'R4,399', 'business': 'R8,809'},
    num={'starter': 1969, 'professional': 4399, 'business': 8809}, inbox='R165', tax='VAT', per='per month, no VAT added',
    price_tax=', no VAT added', tax_short='No VAT added',
    price_basis='No VAT added — prices are for VAT-registered businesses.',
    eyebrow='Built for glaziers in South Africa',
    h1='Glazing software for South African glaziers.',
    lead='Quotes in rand with the glass drawn on every line, surveys on your cellphone even without signal, purchase orders to '
         'suppliers, scheduling and tax invoices. One system for the office, the bakkie and the workshop.',
    title='Coglass South Africa | Glazing Software for South African Glaziers',
    description='Glazing software for South African glaziers: quotes in rand with glass drawings, offline surveys, supplier '
                'orders, scheduling, VAT tax invoices and Xero. From R1,969 a month for VAT-registered businesses, no VAT added.',
    why_h2='Why Coglass suits glaziers in South Africa',
    why=[
        ('Rand quotes and VAT tax invoices', 'Quotes and invoices in rand, with your VAT number and VAT at 15% — and your '
         'banking details on the invoice for EFT.'),
        ('Safety glass clearly specified', 'For SANS 10400-N work, put the glass and its SANS 1263-1 safety-glass marking on the '
         'line itself, so the quote, the purchase order and the job sheet all agree.'),
        _wa_point('South Africa'),
        ('Keeps working offline', 'The phone and iPad apps save surveys, sign-offs and the production board on the device, '
         'so a dropped signal or a power cut at the workshop doesn\'t stop the job. They sync when the connection is back.'),
        ('Drawn and priced properly', 'Shapes, holes, cut-outs and IGU make-ups drawn to size in mm, priced from your own '
         'catalogue and trade price lists.'),
        ('Xero, set up your way', 'Invoices, payments and supplier bills push to your Xero organisation, coded to your own '
         'accounts and VAT rates.'),
    ],
    proof=[('From R1,969', 'a month, no VAT added'), ('Every feature', 'on every plan'), ('1–2 hours', 'from our UK team'), ('iPhone · Android · web', '')],
    support='Our team is in the UK, one to two hours behind South Africa, so our working days largely overlap. Email or call '
            'during business hours and we usually reply within one working day.',
    tz_note='South Africa is 1 to 2 hours ahead of the UK.',
    tax_notes=[
        'Coglass is sold to VAT-registered businesses by Halliday Morrow Ltd, a UK company. No VAT is added to our prices.',
        'Give us your VAT number when you sign up.',
    ],
    faq=[
        ('Can I use Coglass in South Africa?', 'Yes. Coglass is sold in South Africa in rand, to VAT-registered businesses.'),
        ('Do my quotes and invoices show VAT?', 'Yes — in rand, with your VAT number and VAT at 15%, and your banking details '
         'on the invoice for EFT.'),
        ('Is my Coglass subscription charged VAT?', 'No VAT is added. Coglass is sold to VAT-registered businesses: give us your '
         'VAT number when you sign up.'),
        ('What happens when the power or signal goes?', 'The phone and iPad apps keep working: surveys, fitting sign-offs and '
         'the production board are saved on the device and sync when the connection is back. The office web app needs an '
         'internet connection.'),
        ('What hours is support?', 'Our team is in the UK, one to two hours behind you. Email or call during business hours; we '
         'usually reply within one working day.'),
        _wa_faq('South Africa'),
        XERO_FAQ,
    ],
)

# ----------------------------------------------------------------------------- Namibia
C['na'] = dict(
    code='NA', slug='na', name='Namibia', short='Namibia', in_name='Namibia', lang='en-NA', og_locale='en_NA',
    hreflang=['en-NA'],
    currency='NAD', sym='N$', prices={'starter': 'N$1,969', 'professional': 'N$4,399', 'business': 'N$8,809'},
    num={'starter': 1969, 'professional': 4399, 'business': 8809}, inbox='N$165', tax='VAT', per='per month, no VAT added',
    price_tax=', no VAT added', tax_short='No VAT added',
    price_basis='No VAT added — prices are for VAT-registered businesses.',
    eyebrow='Built for glaziers in Namibia',
    h1='Glazing software for Namibian glaziers.',
    lead='Quotes with the glass drawn on every line, surveys on your phone even far from signal, purchase orders to suppliers, '
         'scheduling and invoices. One system for the office, the bakkie and the workshop.',
    title='Coglass Namibia | Glazing Software for Namibian Glaziers',
    description='Glazing software for glaziers in Namibia: quotes with glass drawings, offline surveys, supplier orders, '
                'scheduling and invoicing. Priced in Namibian dollars, from N$1,969 a month for VAT-registered businesses, no VAT added.',
    why_h2='Why Coglass suits glaziers in Namibia',
    why=[
        ('Priced in Namibian dollars', 'Your subscription is priced in N$. Quotes and invoices go out in your currency, with '
         'your VAT number on them.'),
        ('Surveys far from signal', 'Measure, draw and photograph every opening on the phone, however remote the site. It '
         'syncs when you are back in coverage.'),
        _wa_point('Namibia'),
        ('Drawn and priced properly', 'Shapes, holes, cut-outs and IGU make-ups drawn to size in mm, priced from your own '
         'catalogue and trade price lists.'),
        ('Production and suppliers', 'Purchase orders with the drawing on them, a production board from To plan to Made, and '
         'barcode labels for every pane.'),
        ('Close to our working day', 'Namibia is one to two hours ahead of our UK team, so support and demos fit your '
         'business hours.'),
    ],
    proof=[('From N$1,969', 'a month, no VAT added'), ('Every feature', 'on every plan'), ('1–2 hours', 'from our UK team'), ('iPhone · Android · web', '')],
    support='Our team is in the UK, one to two hours behind Namibia, so our working days largely overlap. Email or call during '
            'business hours and we usually reply within one working day.',
    tz_note='Namibia is 1 to 2 hours ahead of the UK.',
    tax_notes=[
        'Coglass is sold to VAT-registered businesses by Halliday Morrow Ltd, a UK company. No VAT is added to our prices.',
        'Give us your VAT number when you sign up.',
    ],
    faq=[
        ('Can I use Coglass in Namibia?', 'Yes. Coglass is sold in Namibia in Namibian dollars, to VAT-registered businesses.'),
        ('Is my Coglass subscription charged VAT?', 'No VAT is added. Coglass is sold to VAT-registered businesses: give us your '
         'VAT number when you sign up.'),
        ('What hours is support?', 'Our team is in the UK, one to two hours behind you. Email or call during business hours; we '
         'usually reply within one working day.'),
        _wa_faq('Namibia'),
        OFFLINE_FAQ,
        XERO_FAQ,
    ],
)

# ----------------------------------------------------------------------------- Botswana
# Prices: converted from GBP at the Bank of Botswana rate for 2 Oct 2026 (BWP 1 = GBP 0.0563, so £1 = P17.762),
# rounded to the nearest price ending in 9; extra inbox to the nearest P5. Source:
# https://www.bankofbotswana.bw/exchange-rates/2-october-2026
C['bw'] = dict(
    code='BW', slug='bw', name='Botswana', short='Botswana', in_name='Botswana', lang='en-BW', og_locale='en_BW',
    hreflang=['en-BW'],
    currency='BWP', sym='P', prices={'starter': 'P1,579', 'professional': 'P3,539', 'business': 'P7,089'},
    num={'starter': 1579, 'professional': 3539, 'business': 7089}, inbox='P135', tax='VAT', per='per month, no VAT added',
    price_tax=', no VAT added', tax_short='No VAT added',
    price_basis='No VAT added — prices are for VAT-registered businesses.',
    eyebrow='Built for glaziers in Botswana',
    h1='Glazing software for glaziers in Botswana.',
    lead='Quotes with the glass drawn on every line, surveys on your phone even far from signal, purchase orders to suppliers, '
         'scheduling and invoices. One system for the office, the van and the workshop.',
    title='Coglass Botswana | Glazing Software for Glaziers in Botswana',
    description='Glazing software for glaziers in Botswana: quotes with glass drawings, offline surveys, supplier orders, '
                'scheduling and invoicing. Priced in pula, from P1,579 a month for VAT-registered businesses, no VAT added.',
    why_h2='Why Coglass suits glaziers in Botswana',
    why=[
        ('Priced in pula', 'Your subscription is priced in pula. Quotes and invoices go out in your currency, with your VAT '
         'number on them.'),
        ('Surveys far from signal', 'Measure, draw and photograph every opening on the phone, however remote the site. It '
         'syncs when you are back in coverage.'),
        _wa_point('Botswana'),
        ('Drawn and priced properly', 'Shapes, holes, cut-outs and IGU make-ups drawn to size in mm, priced from your own '
         'catalogue and trade price lists.'),
        ('Production and suppliers', 'Purchase orders with the drawing on them, a production board from To plan to Made, and '
         'barcode labels for every pane.'),
        ('Close to our working day', 'Botswana is one to two hours ahead of our UK team, so support and demos fit your '
         'business hours.'),
    ],
    proof=[('From P1,579', 'a month, no VAT added'), ('Every feature', 'on every plan'), ('1–2 hours', 'from our UK team'), ('iPhone · Android · web', '')],
    support='Our team is in the UK, one to two hours behind Botswana, so our working days largely overlap. Email or call during '
            'business hours and we usually reply within one working day.',
    tz_note='Botswana is 1 to 2 hours ahead of the UK.',
    tax_notes=[
        'Coglass is sold to VAT-registered businesses by Halliday Morrow Ltd, a UK company. No VAT is added to our prices.',
        'Give us your VAT number when you sign up.',
    ],
    faq=[
        ('Can I use Coglass in Botswana?', 'Yes. Coglass is sold in Botswana in pula, to VAT-registered businesses.'),
        ('Is my Coglass subscription charged VAT?', 'No VAT is added. Coglass is sold to VAT-registered businesses: give us your '
         'VAT number when you sign up.'),
        ('What hours is support?', 'Our team is in the UK, one to two hours behind you. Email or call during business hours; we '
         'usually reply within one working day.'),
        _wa_faq('Botswana'),
        OFFLINE_FAQ,
        XERO_FAQ,
    ],
)

# ----------------------------------------------------------------------------- Malta
C['mt'] = dict(
    code='MT', slug='mt', name='Malta', short='Malta', in_name='Malta', lang='en-MT', og_locale='en_MT',
    hreflang=['en-MT'],
    currency='EUR', sym='€', prices={'starter': '€109', 'professional': '€239', 'business': '€469'},
    num={'starter': 109, 'professional': 239, 'business': 469}, inbox='€9.00', tax='VAT', per='per month, no VAT added',
    price_tax=', no VAT added', tax_short='No VAT added',
    price_basis='No VAT added — prices are for VAT-registered businesses (reverse charge).',
    eyebrow='Built for glaziers in Malta',
    h1='Glazing software for glaziers in Malta.',
    lead='Quotes in euro with the glass drawn on every line, surveys on the phone, purchase orders to suppliers, scheduling and '
         'VAT invoices. One system for the office, the van and the workshop.',
    title='Coglass Malta | Glazing Software for Glaziers in Malta & Gozo',
    description='Glazing software for glaziers in Malta and Gozo: quotes in euro with glass drawings, surveys on the phone, '
                'supplier orders, scheduling and VAT invoicing. From €109 a month for VAT-registered businesses, no VAT added.',
    why_h2='Why Coglass suits glaziers in Malta',
    why=[
        ('Euro quotes and invoices', 'Quotes and invoices in euro, with your VAT number on them.'),
        _wa_point('Malta'),
        ('Drawn and priced properly', 'Shapes, holes, cut-outs and IGU make-ups drawn to size in mm, priced from your own '
         'catalogue and trade price lists.'),
        ('A planner for a busy island', 'Drag surveys, fittings and deliveries onto people and vans, and see which ready jobs '
         'are close to the day\'s other stops.'),
        ('Production and suppliers', 'Purchase orders with the drawing on them, a production board from To plan to Made, and '
         'barcode labels for every pane.'),
        ('Hosted in the EU', 'Your data is held on servers in Germany, and our team is one hour behind you in the UK.'),
    ],
    proof=[('From €109', 'a month, no VAT added'), ('Hosted in the EU', 'data held in Germany'), ('1 hour', 'from our UK team'), ('iPhone · Android · web', '')],
    support='Our team is in the UK, one hour behind Malta. Email or call during business hours and we usually reply within one '
            'working day.',
    tz_note='Malta is 1 hour ahead of the UK.',
    # TODO(OSS): once the EU non-Union OSS registration is in Stripe Tax, buyers without a VAT number can be
    # sold to again (Maltese VAT at 18% added at checkout). Then restore the "No VAT number? You can still sign up"
    # line below, the matching FAQ sentence, and the per/price_tax/price_basis wording above ("+ VAT").
    tax_notes=[
        'Coglass is sold to VAT-registered businesses by Halliday Morrow Ltd, a UK company. No VAT is added to our prices.',
        'Give us your Maltese VAT number when you sign up (we check it on the EU VIES register): no VAT is added to our invoice '
        'and you account for it yourself under the reverse charge.',
    ],
    faq=[
        ('Can I use Coglass in Malta and Gozo?', 'Yes. Coglass is sold in Malta in euro, and quotes and invoices go out in euro.'),
        ('How is VAT handled on my Coglass subscription?', 'Coglass is sold to VAT-registered businesses. Give us your Maltese VAT '
         'number when you sign up: no VAT is added to our invoice — you account for it under the reverse charge. For now you '
         'need a VAT number to subscribe.'),
        ('Where is my data held?', 'In the EU — on servers in Germany.'),
        ('What hours is support?', 'Our team is in the UK, one hour behind Malta. Email or call during business hours; we usually '
         'reply within one working day.'),
        _wa_faq('Malta'),
        OFFLINE_FAQ,
        XERO_FAQ,
    ],
)

for _k, _c in C.items():
    _c['key'] = _k
    _c['subscribe'] = SUBSCRIBE[_k]
