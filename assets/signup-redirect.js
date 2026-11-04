// /signup.html is no longer a form — it forwards old "Book a demo" / sign-up links to the plans for the
// visitor's country, where the 14-day trial starts. Loaded (not deferred) in <head> so it runs before the
// meta refresh fallback; the CSP allows no inline script, hence this file.
//   ?country=uk|ie|au|nz|za|na|bw|mt  → /<country>/pricing/#plans
//   ?country=im|je|gg|gi              → /uk/pricing/#crown (UK prices, per-island trial links)
//   anything else / nothing            → /pricing/#plans (country chooser)
(function () {
  var COUNTRIES = ['uk', 'ie', 'au', 'nz', 'za', 'na', 'bw', 'mt'];
  var CROWN = ['im', 'je', 'gg', 'gi'];
  var target = '/pricing/#plans';
  try {
    var m = /[?&]country=([a-z]{2})(?:&|$)/i.exec(window.location.search);
    var c = m ? m[1].toLowerCase() : '';
    if (c === 'gb') c = 'uk';
    if (COUNTRIES.indexOf(c) !== -1) target = '/' + c + '/pricing/#plans';
    else if (CROWN.indexOf(c) !== -1) target = '/uk/pricing/#crown';
  } catch (err) { /* fall through to the chooser */ }
  window.location.replace(target);
})();
