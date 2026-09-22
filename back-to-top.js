/* Back to top: one button, every page.
   Injects the standard circle (brand red, white arrow, bottom right, appears
   after 400px) unless the page already has its own. Pages that hand-rolled one
   keep theirs, so nothing is duplicated. */
(function () {
  if (document.querySelector('.back-to-top')) return;

  var css = document.createElement('style');
  css.textContent =
    '.back-to-top{position:fixed;bottom:2rem;right:2rem;width:44px;height:44px;' +
    'background:#8B0000;color:#fff;border:none;border-radius:50%;cursor:pointer;' +
    'display:flex;align-items:center;justify-content:center;' +
    'box-shadow:0 4px 12px rgba(0,0,0,.3);opacity:0;visibility:hidden;' +
    'transform:translateY(10px);transition:opacity .3s,transform .3s,visibility .3s,background .3s;' +
    'z-index:900}' +
    '.back-to-top.visible{opacity:1;visibility:visible;transform:translateY(0)}' +
    '.back-to-top:hover{background:#6b0000;transform:translateY(-3px)}' +
    '@media (max-width:560px){.back-to-top{bottom:1rem;right:1rem}}';
  document.head.appendChild(css);

  var b = document.createElement('button');
  b.className = 'back-to-top';
  b.type = 'button';
  b.setAttribute('aria-label', 'Back to top');
  b.innerHTML =
    '<svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">' +
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"></path></svg>';
  b.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  document.body.appendChild(b);

  window.addEventListener('scroll', function () {
    b.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
})();
