// Phone menu for the pages whose header was built without one.
//
// A header opts in with data-phone-menu. Below 900px the stylesheet hides its
// row of links and this script supplies the button and a drop-down list,
// copied from those same links so the two can never disagree. Pages that
// already carry a hamburger of their own are left alone.
(function () {
  var header = document.querySelector('.site-header[data-phone-menu]');
  if (!header) return;
  var bar = header.querySelector('.header-container');
  var list = header.querySelector('.main-navigation ul');
  if (!bar || !list || header.querySelector('.hamburger, .pm-toggle')) return;

  // the menu takes the header's own colour, so it matches on light and dark
  // headers; a see-through header colour is made solid, or the page shows
  // through the list
  function paint(el) {
    for (var e = el; e; e = e.parentElement) {
      var bg = getComputedStyle(e).backgroundColor;
      var parts = bg ? bg.replace(/[^0-9.,]/g, '').split(',') : [];
      if (parts.length < 3) continue;
      if (parts.length === 4 && parseFloat(parts[3]) === 0) continue;
      return 'rgb(' + parts[0] + ',' + parts[1] + ',' + parts[2] + ')';
    }
    return '#ffffff';
  }
  var plain = list.querySelector('a:not(.login-link):not(.cta-button):not(.btn-login)') || list.querySelector('a');
  var ink = plain ? getComputedStyle(plain).color : '#2c3e50';

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'pm-toggle';
  btn.setAttribute('aria-label', 'Menu');
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-controls', 'pm-menu');
  btn.style.color = ink;
  btn.innerHTML = '<span></span><span></span><span></span>';

  var menu = document.createElement('div');
  menu.className = 'pm-menu';
  menu.id = 'pm-menu';
  menu.style.background = paint(header);
  menu.style.color = ink;
  var copy = list.cloneNode(true);
  copy.removeAttribute('id');
  menu.appendChild(copy);

  if (getComputedStyle(header).position === 'static') header.style.position = 'relative';
  bar.appendChild(btn);
  header.appendChild(menu);

  function set(open) {
    btn.classList.toggle('open', open);
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  btn.addEventListener('click', function () { set(!menu.classList.contains('open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > (header.classList.contains("bigtoe-header") ? 1100 : 900)) set(false); });
})();
