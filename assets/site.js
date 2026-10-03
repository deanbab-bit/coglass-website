// Coglass sales site: phone menu toggle.
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
