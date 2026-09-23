// Renders posts from a plain-text file (news/posts.txt) into any element with data-news-src.
(function () {
  function esc(s) { return s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  function linkify(s) { return esc(s).replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener" class="text-accent-ink underline">$1</a>'); }
  function parse(text) {
    const posts = [];
    text.replace(/\r/g, '').split(/^---\s*$/m).forEach(block => {
      const lines = block.split('\n').filter(l => !/^\s*#/.test(l));
      while (lines.length && !lines[0].trim()) lines.shift();
      if (lines.length < 2) return;
      const date = lines[0].trim().replace(/[-\/]/g, '.');
      if (!/^\d{4}\.\d{1,2}\.\d{1,2}$/.test(date)) return;
      const [y, m, d] = date.split('.');
      const norm = `${y}.${m.padStart(2, '0')}.${d.padStart(2, '0')}`;
      const body = lines.slice(2).join('\n').trim();
      posts.push({ date: norm, title: lines[1].trim(), body });
    });
    posts.sort((a, b) => b.date.localeCompare(a.date));
    posts.forEach((p, i) => { p.id = 'n' + p.date.replace(/\./g, '') + '-' + i; });
    return posts;
  }
  document.querySelectorAll('[data-news-src]').forEach(el => {
    fetch(el.dataset.newsSrc, { cache: 'no-cache' }).then(r => r.ok ? r.text() : Promise.reject()).then(text => {
      const posts = parse(text);
      if (!posts.length) return;
      if (el.dataset.newsFull !== undefined) {
        el.innerHTML = posts.map(p => `<article class="news-post" id="${p.id}"><time>${p.date}</time><h2>${esc(p.title)}</h2>${p.body ? `<div class="news-body">${p.body.split(/\n{2,}/).map(par => `<p>${linkify(par).replace(/\n/g, '<br/>')}</p>`).join('')}</div>` : ''}</article>`).join('');
        if (location.hash) { const t = document.querySelector(location.hash); if (t) t.scrollIntoView(); }
      } else {
        const limit = parseInt(el.dataset.newsLimit || '3', 10);
        el.innerHTML = posts.slice(0, limit).map(p => `<li><a href="${el.dataset.newsBase || ''}#${p.id}"><time>${p.date}</time><span>${esc(p.title)}</span></a></li>`).join('');
      }
    }).catch(() => {});
  });
})();
