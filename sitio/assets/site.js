// Enclave IA · interacciones mínimas. El sitio funciona sin este archivo.
(function () {
  var es = document.documentElement.lang.indexOf('es') === 0;
  var text = es
    ? { ok: 'Aprobado por Coordinación Académica · resumen enviado', back: 'Devuelto con comentarios · no se envió nada' }
    : { ok: 'Approved by Academic Coordination · summary sent', back: 'Returned with comments · nothing was sent' };

  var log = document.querySelector('[data-log]');
  var buttons = document.querySelectorAll('[data-decision]');
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      if (!log) return;
      var li = document.createElement('li');
      li.className = 'new';
      var t = document.createElement('time');
      t.textContent = '10:43';
      var s = document.createElement('span');
      s.textContent = text[b.getAttribute('data-decision')];
      li.appendChild(t);
      li.appendChild(s);
      log.appendChild(li);
      buttons.forEach(function (x) { x.disabled = true; });
    });
  });

  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var note = document.querySelector('[data-copied]');
      var value = b.getAttribute('data-copy');
      function shown() { if (note) note.hidden = false; }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(shown, function () {});
      }
    });
  });
})();
