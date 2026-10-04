// Coglass sales site: phone menu toggle + country suggestion.
(function () {
  document.documentElement.classList.remove('no-js');
  var head = document.querySelector('.site-head');
  var btn = document.querySelector('.menu-btn');
  if (!head || !btn) return;
  btn.addEventListener('click', function () {
    var open = head.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && head.classList.contains('open')) {
      head.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-label', 'Open menu');
      btn.focus();
    }
  });
})();

// Country suggestion. NEVER redirects: every page stays crawlable at its own URL (Googlebot
// included). It only shows a dismissible bar offering the visitor's own country section,
// guessed from (1) a country they picked before, (2) the browser time zone, (3) the browser
// language. Keep the list in step with _src/countries.py.
(function () {
  var NAMES = { uk: 'the UK', ie: 'Ireland', au: 'Australia', nz: 'New Zealand', za: 'South Africa', na: 'Namibia', bw: 'Botswana', mt: 'Malta' };
  var SITE_NAMES = { uk: 'Coglass UK', ie: 'Coglass Ireland', au: 'Coglass Australia', nz: 'Coglass New Zealand', za: 'Coglass South Africa', na: 'Coglass Namibia', bw: 'Coglass Botswana', mt: 'Coglass Malta' };
  var TZ = {
    'Europe/London': 'uk', 'Europe/Belfast': 'uk', 'Europe/Isle_of_Man': 'uk', 'Europe/Jersey': 'uk', 'Europe/Guernsey': 'uk', 'Europe/Gibraltar': 'uk',
    'Europe/Dublin': 'ie', 'Pacific/Auckland': 'nz', 'Pacific/Chatham': 'nz', 'Africa/Johannesburg': 'za',
    'Africa/Windhoek': 'na', 'Africa/Gaborone': 'bw', 'Europe/Malta': 'mt'
  };
  var LANG = { GB: 'uk', IM: 'uk', JE: 'uk', GG: 'uk', GI: 'uk', IE: 'ie', AU: 'au', NZ: 'nz', ZA: 'za', NA: 'na', BW: 'bw', MT: 'mt' };
  var STORE = 'coglass-country', DISMISS = 'coglass-suggest-dismissed';

  function get(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* private mode */ } }

  function guess(useSaved) {
    var saved = get(STORE);
    if (useSaved !== false && saved && NAMES[saved]) return saved;
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      if (TZ[tz]) return TZ[tz];
      if (tz.indexOf('Australia/') === 0) return 'au';
    } catch (e) { /* old browser */ }
    var langs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < langs.length; i++) {
      var m = /^en-([a-z]{2})$/i.exec(langs[i] || '');
      if (m && LANG[m[1].toUpperCase()]) return LANG[m[1].toUpperCase()];
    }
    return null;
  }
  window.coglassGuessCountry = guess;

  var bar = document.getElementById('cty-suggest');
  var current = bar ? bar.getAttribute('data-current') : '';

  // Remember explicit picks from the chooser / country links.
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('[data-country]') : null;
    if (a && NAMES[a.getAttribute('data-country')]) set(STORE, a.getAttribute('data-country'));
  });

  // On a country section, a visitor who picked this country before sees nothing; anyone else is
  // offered the country their browser points to. Elsewhere the saved pick wins.
  if (current && get(STORE) === current) return;
  var c = guess(!current);
  if (!c) return;

  // Highlight the guessed country on the chooser grids.
  var cards = document.querySelectorAll('.ccard[data-country="' + c + '"]');
  for (var j = 0; j < cards.length; j++) cards[j].classList.add('is-suggested');

  if (!bar || c === current || get(DISMISS) === c) return;
  var path = location.pathname;
  var kind = /\/pricing\/?$/.test(path) ? 'pricing/' : (/\/faq\/?$/.test(path) ? 'faq/' : '');
  var href = '/' + c + '/' + kind;
  var text = current ? ('You are looking at ' + SITE_NAMES[current] + '. In ' + NAMES[c] + '?') : ('In ' + NAMES[c] + '? See prices and details for your country.');

  var wrap = document.createElement('div'); wrap.className = 'wrap';
  var p = document.createElement('p'); p.textContent = text;
  var go = document.createElement('a'); go.className = 'btn acc'; go.href = href; go.setAttribute('data-country', c);
  go.textContent = 'Go to ' + SITE_NAMES[c];
  var x = document.createElement('button'); x.type = 'button'; x.textContent = 'No thanks';
  x.setAttribute('aria-label', 'Dismiss country suggestion');
  x.addEventListener('click', function () { set(DISMISS, c); bar.hidden = true; });
  wrap.appendChild(p); wrap.appendChild(go); wrap.appendChild(x);
  bar.appendChild(wrap);
  bar.setAttribute('role', 'region');
  bar.setAttribute('aria-label', 'Country suggestion');
  bar.hidden = false;
})();
