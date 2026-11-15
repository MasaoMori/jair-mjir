// お知らせの分類で絞り込む(静的サイト用。参考サイトのAjax版の代わり)。data-limit があればその件数まで表示する。
document.querySelectorAll('.jair-category-news').forEach(root => {
  const rows = [...root.querySelectorAll('.jair-news-row')];
  const tabs = [...root.querySelectorAll('.jair-news-filters a')];
  const limit = parseInt(root.dataset.limit || '0', 10);
  if (!rows.length || !tabs.length) return;
  const apply = cat => {
    let shown = 0;
    rows.forEach(r => {
      const ok = cat === 'all' || r.dataset.cat === cat;
      const show = ok && (!limit || shown < limit);
      r.hidden = !show;
      if (show) shown++;
    });
    tabs.forEach(t => t.dataset.filter === cat ? t.setAttribute('aria-current', 'true') : t.removeAttribute('aria-current'));
  };
  tabs.forEach(t => t.addEventListener('click', e => { e.preventDefault(); apply(t.dataset.filter); }));
  apply('all');
});
