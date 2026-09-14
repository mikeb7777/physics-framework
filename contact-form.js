// The message form on the contact and discussions pages.
//
// Messages go to Formspree, which emails them on. Paste the form ID from the
// Formspree dashboard (the part after /f/ in the form's endpoint) into
// FORM_ID below; that is the only change needed to switch the form on. Until
// then the form says it is not connected yet and offers the email address,
// so no visitor loses a message they typed.
(function () {
  var FORM_ID = 'mnpqkjqo';
  var EMAIL = 'ic2.info@proton.me';

  document.querySelectorAll('form[data-contact-form]').forEach(function (form) {
    var button = form.querySelector('button[type="submit"]');
    var status = form.querySelector('.form-status');
    var label = button ? button.textContent : '';

    function say(message, kind) {
      if (!status) return;
      status.textContent = '';
      status.className = 'form-status' + (kind ? ' form-status-' + kind : '');
      var parts = message.split(EMAIL);
      parts.forEach(function (part, i) {
        status.appendChild(document.createTextNode(part));
        if (i < parts.length - 1) {
          var a = document.createElement('a');
          a.href = 'mailto:' + EMAIL;
          a.textContent = EMAIL;
          status.appendChild(a);
        }
      });
    }

    if (!FORM_ID) {
      say('This form is not connected yet. Please write to ' + EMAIL + ' in the meantime.', 'info');
    } else {
      form.action = 'https://formspree.io/f/' + FORM_ID;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!FORM_ID) {
        say('This form is not connected yet. Please write to ' + EMAIL + ' and your message will reach us.', 'info');
        return;
      }
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (button) { button.disabled = true; button.textContent = 'Sending...'; }
      say('', '');
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      }).then(function (response) {
        if (response.ok) {
          form.reset();
          say('Thank you. Your message has been sent, and we will reply by email.', 'ok');
          return;
        }
        return response.json().then(function (data) {
          var detail = data && data.errors ? data.errors.map(function (e) {
            var m = String(e.message || '').trim();
            m = m.charAt(0).toUpperCase() + m.slice(1);
            return m && '.!?'.indexOf(m.slice(-1)) < 0 ? m + '.' : m;
          }).join(' ') : '';
          say('Your message could not be sent. ' + (detail ? detail + ' ' : '') + 'Please try again, or write to ' + EMAIL + '.', 'error');
        }, function () {
          say('Your message could not be sent. Please try again, or write to ' + EMAIL + '.', 'error');
        });
      }).catch(function () {
        say('Your message could not be sent. Please check your connection and try again, or write to ' + EMAIL + '.', 'error');
      }).then(function () {
        if (button) { button.disabled = false; button.textContent = label; }
      });
    });
  });
})();
