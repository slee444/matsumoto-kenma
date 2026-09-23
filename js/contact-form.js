// Sends any <form data-contact-form> to the Google Apps Script endpoint.
// Adds: form type, the page the visitor came from, and the form page URL.
(function () {
  var GAS_URL = 'https://script.google.com/macros/s/AKfycbz60vxcOiC2MGQWxyGBzV093rX9zkrbsthYv6AHNb84vJCyKgXXzzkUuUJtC60UBeV8/exec';

  function sourcePage() {
    var ref = document.referrer || '';
    if (!ref) return '（直接アクセス・ブックマークなど）';
    try {
      var u = new URL(ref);
      if (u.origin === location.origin) return u.href;
      return '外部サイト：' + u.href;
    } catch (e) { return ref; }
  }

  document.querySelectorAll('form[data-contact-form]').forEach(function (form) {
    var box = form.closest('[data-form-wrap]') || form.parentNode;
    var success = box.querySelector('[data-form-success]');
    var errBox = form.querySelector('[data-form-error]');
    var btn = form.querySelector('button[type="submit"]');
    var src = sourcePage();

    // キャンペーンページ（?from=monitor）から来たときは、内容欄に下書きを入れておく
    var msg = form.querySelector('textarea[name="message"]');
    if (msg && !msg.value && /[?&]from=monitor\b/.test(location.search)) {
      msg.value = '事例づくりモニターについて相談したいです。\n希望のプラン：\n今のホームページ：ある／ない';
    }

    function showError(msg, el) {
      errBox.textContent = msg;
      errBox.classList.remove('hidden');
      if (el && el.focus) el.focus();
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errBox.classList.add('hidden');

      // required checks (text/select/textarea + radio/checkbox groups)
      var groups = {};
      var fields = form.querySelectorAll('[name]');
      for (var i = 0; i < fields.length; i++) {
        var el = fields[i];
        if (el.name === 'website') continue;
        if (el.type === 'radio' || el.type === 'checkbox') {
          if (el.hasAttribute('required')) groups[el.name] = el;
          continue;
        }
        if (el.hasAttribute('required') && !el.value.trim()) {
          return showError('「' + (el.dataset.label || '必須項目') + '」を入力してください。', el);
        }
        if (el.type === 'email' && el.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim())) {
          return showError('メールアドレスの形式をご確認ください。', el);
        }
      }
      for (var name in groups) {
        if (!form.querySelector('[name="' + name + '"]:checked')) {
          return showError('「' + (groups[name].dataset.label || '選択項目') + '」を選んでください。', groups[name]);
        }
      }

      // collect values in form order, with Japanese labels
      var data = new FormData(form);
      var seen = {}, list = [], flat = {};
      for (var j = 0; j < fields.length; j++) {
        var f = fields[j];
        if (seen[f.name] || f.name === 'website') continue;
        seen[f.name] = true;
        var val = data.getAll(f.name).join('、');
        flat[f.name] = val;
        var labelEl = form.querySelector('[name="' + f.name + '"][data-label]');
        list.push([labelEl ? labelEl.dataset.label : f.name, val]);
      }

      var payload = {
        formType: form.dataset.contactForm,
        name: flat.name || '',
        email: flat.email || '',
        fields: list,
        sourceUrl: src,
        pageUrl: location.href,
        hp: data.get('website') || ''
      };
      var params = new URLSearchParams(flat);   // old format, kept so the current script still works
      params.set('payload', JSON.stringify(payload));

      btn.disabled = true;
      var label = btn.querySelector('[data-btn-text]');
      if (label) label.textContent = '送信中…';

      fetch(GAS_URL, { method: 'POST', mode: 'no-cors', body: params })
        .then(function () {
          form.classList.add('hidden');
          if (success) success.classList.remove('hidden');
          window.scrollTo({ top: box.getBoundingClientRect().top + window.scrollY - 100, behavior: 'smooth' });
        })
        .catch(function () {
          showError(form.dataset.contactForm === 'web'
            ? '送信できませんでした。お手数ですが、時間をおいてもう一度お試しください。'
            : '送信できませんでした。お手数ですが、お電話（044-333-8412）かメールでご連絡ください。');
          btn.disabled = false;
          if (label) label.textContent = '送信する';
        });
    });
  });
})();
