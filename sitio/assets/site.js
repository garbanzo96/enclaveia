// Enclave IA · interacciones de la portada. El sitio funciona sin este archivo:
// los acordeones son <details>, el ejemplo se lee completo y el correo es un enlace.
// Los textos que cambian viven en atributos data-* del HTML, uno por idioma.
(function () {
  // Acordeones: si el navegador no agrupa los <details> con el mismo name, se cierran a mano.
  document.querySelectorAll('details[name]').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      document.querySelectorAll('details[name="' + d.getAttribute('name') + '"]').forEach(function (o) {
        if (o !== d) o.open = false;
      });
    });
  });

  // Ejemplo anotado: aprobar o devolver agrega una línea al registro.
  var specimen = document.querySelector('[data-specimen]');
  if (specimen) {
    var log = specimen.querySelector('[data-log]');
    var pending = specimen.querySelector('[data-pending]');
    var decided = specimen.querySelector('[data-decided]');
    var status = specimen.querySelector('[data-status]');
    specimen.querySelectorAll('[data-decision]').forEach(function (b) {
      b.addEventListener('click', function () {
        var li = document.createElement('li');
        li.className = 'new';
        var t = document.createElement('time');
        t.textContent = b.getAttribute('data-time');
        var s = document.createElement('span');
        s.textContent = b.getAttribute('data-log-text');
        li.appendChild(t);
        li.appendChild(s);
        log.appendChild(li);
        status.textContent = b.getAttribute('data-status-text');
        pending.hidden = true;
        decided.hidden = false;
      });
    });
    specimen.querySelector('[data-reset]').addEventListener('click', function () {
      var added = log.querySelector('.new');
      if (added) log.removeChild(added);
      decided.hidden = true;
      pending.hidden = false;
    });
  }

  // Recorrido de una consulta: el paso abierto resalta su parte del diagrama.
  var fig = document.querySelector('[data-fig]');
  var steps = document.querySelectorAll('[data-hi]');
  if (fig && steps.length) {
    var nodes = fig.querySelectorAll('[data-stage]');
    var caption = fig.querySelector('[data-fig-caption]');
    var diagrams = fig.querySelectorAll('[data-fig-label]');
    var names = fig.getAttribute('data-stages').split('|');
    var fill = function (tpl, vars) {
      return tpl.replace(/\{(\w+)\}/g, function (_, k) { return vars[k]; });
    };
    var sync = function () {
      var open = document.querySelector('details[data-hi][open]');
      var on = {};
      var stages = open ? open.getAttribute('data-hi').split(' ') : [];
      stages.forEach(function (s) { on[s] = true; });
      nodes.forEach(function (n) {
        var active = !!on[n.getAttribute('data-stage')];
        n.classList.toggle('on', active);
      });
      var vars = {};
      if (open) {
        vars.n = open.getAttribute('data-n');
        vars.title = open.getAttribute('data-title');
        vars.names = stages.map(function (s) { return names[+s]; }).join(fig.getAttribute('data-and'));
      }
      caption.textContent = open ? fill(fig.getAttribute('data-caption-step'), vars) : fig.getAttribute('data-caption-idle');
      diagrams.forEach(function (d) {
        var base = d.getAttribute('data-fig-label');
        d.setAttribute('aria-label', open ? base + ' ' + fill(fig.getAttribute('data-label-step'), vars) : base);
      });
    };
    steps.forEach(function (d) { d.addEventListener('toggle', sync); });
    sync();
  }

  // Copiar la dirección de correo.
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var note = document.querySelector('[data-copied]');
      if (!navigator.clipboard || !navigator.clipboard.writeText) return;
      navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {
        if (!note) return;
        note.textContent = note.getAttribute('data-text');
        setTimeout(function () { note.textContent = ''; }, 3000);
      }, function () {});
    });
  });
})();
