// "Book a demo / talk to us" lead form → https://hq.coglass.app/api/leads (manual review in HQ).
//
// Spam defences, all client-side (a determined bot can skip them — the server must
// still validate; see the PR notes for what HQ should check):
//   1. Honeypot: the hidden "website" field. Humans never see it; if it has a value we
//      show the normal success screen and send nothing. (HQ already receives this field
//      as `website` and can drop the lead too.)
//   2. Time-to-submit: a form completed in under MIN_FILL_MS is treated as a bot the same way.
//   3. Cloudflare Turnstile (widget "Coglass website forms", Managed mode, hostnames
//      coglass.net + coglass.co.uk). The token is sent as `turnstileToken` and HQ
//      /api/leads verifies it server-side with the secret (siteverify). Tokens are
//      single-use and expire after 5 minutes, so the widget is reset after any failed
//      send and when the token expires. Set the key to '' to switch it off.
(function () {
  var TURNSTILE_SITE_KEY = '0x4AAAAAAFpk9A5Ts04mQYKE'; // public site key (safe to publish)
  var MIN_FILL_MS = 4000;
  var ENDPOINT = 'https://hq.coglass.app/api/leads';

  var form = document.getElementById('lead-form');
  if (!form) return;
  var startedAt = Date.now();
  var btn = document.getElementById('lead-submit');
  var btnLabel = btn.textContent;
  var errorEl = document.getElementById('lead-error');
  var turnstileToken = '';

  // Country: from ?country= (country-section CTAs pass it), else the visitor's earlier pick or
  // browser guess (site.js), else left for them to choose. Sent to HQ as `country` (ISO code)
  // and also written at the top of the message, so it reaches HQ even if /api/leads ignores
  // unknown fields. ?plan= (plan buttons) is passed on the same way.
  var CODES = { uk: 'GB', ie: 'IE', au: 'AU', nz: 'NZ', za: 'ZA', na: 'NA', bw: 'BW', mt: 'MT', other: '' };
  var params = new URLSearchParams(window.location.search);
  var countrySel = document.getElementById('lead-country');
  var plan = (params.get('plan') || '').replace(/[^a-z]/g, '').slice(0, 20);
  if (countrySel) {
    var pre = (params.get('country') || '').toLowerCase();
    if (!(pre in CODES) && window.coglassGuessCountry) pre = window.coglassGuessCountry() || '';
    if (pre in CODES) countrySel.value = pre;
  }

  if (TURNSTILE_SITE_KEY) {
    window.coglassTurnstileOk = function (t) { turnstileToken = t; };
    window.coglassTurnstileReset = function () { turnstileToken = ''; };
    var slot = document.getElementById('turnstile-slot');
    slot.innerHTML = '<div class="cf-turnstile" data-sitekey="' + TURNSTILE_SITE_KEY + '" data-callback="coglassTurnstileOk"'
      + ' data-expired-callback="coglassTurnstileReset" data-error-callback="coglassTurnstileReset"'
      + ' data-action="lead" data-size="flexible" data-theme="light"></div>';
    var s = document.createElement('script');
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
    s.async = true; s.defer = true;
    document.head.appendChild(s);
  }

  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }
  function showSuccess() {
    form.style.display = 'none';
    var ok = document.getElementById('lead-ok');
    ok.style.display = 'block';
    ok.focus();
  }
  function resetTurnstile() {
    // A token can only be checked once — after a failed send, get a fresh one.
    turnstileToken = '';
    try { if (TURNSTILE_SITE_KEY && window.turnstile) window.turnstile.reset(); } catch (e) {}
  }
  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.style.display = 'block';
    btn.disabled = false;
    btn.textContent = btnLabel;
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    errorEl.style.display = 'none';

    var honeypot = document.getElementById('lead-website').value;
    if (honeypot || Date.now() - startedAt < MIN_FILL_MS) { showSuccess(); return; }
    if (TURNSTILE_SITE_KEY && !turnstileToken) { showError('Please wait a moment for the security check above the button to finish, then try again.'); return; }

    var cKey = countrySel ? countrySel.value : '';
    var cName = countrySel && countrySel.selectedIndex > 0 ? countrySel.options[countrySel.selectedIndex].text : '';
    var tags = (cName ? '[Country: ' + cName + '] ' : '') + (plan ? '[Plan: ' + plan + '] ' : '');
    var body = {
      company: val('lead-company'),
      name: val('lead-name'),
      email: val('lead-email'),
      phone: val('lead-phone'),
      message: (tags + val('lead-message')).trim(),
      country: CODES[cKey] || cKey,
      plan: plan,
      website: honeypot,
    };
    if (TURNSTILE_SITE_KEY) body.turnstileToken = turnstileToken;

    btn.disabled = true;
    btn.textContent = 'Sending…';
    try {
      var res = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      var data = await res.json().catch(function () { return {}; });
      if (!res.ok) { resetTurnstile(); showError(data.error || 'Something went wrong. Please try again, or email contact@coglass.co.uk.'); return; }
      showSuccess();
    } catch (err) {
      resetTurnstile();
      showError('Could not connect. Please try again, or email contact@coglass.co.uk.');
    }
  });
})();
