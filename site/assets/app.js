const menu = document.querySelector('#menu');
const sidebar = document.querySelector('#sidebar');
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  sidebar.classList.toggle('open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && sidebar.classList.contains('open')) {
    menu.click();
    menu.focus();
  }
});
document.querySelectorAll('pre').forEach(pre => {
  const code = pre.querySelector('code');
  if (!code) return;
  const button = document.createElement('button');
  button.className = 'copy';
  button.textContent = 'Copy';
  button.setAttribute('aria-label', 'Copy code example');
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Select to copy';
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }
    setTimeout(() => { button.textContent = 'Copy'; }, 2200);
  });
  pre.prepend(button);
});
const input = document.querySelector('#search');
const results = document.querySelector('#search-results');
const status = document.querySelector('#search-status');
const nav = document.querySelector('nav');
let indexPromise;
let sequence = 0;
document.querySelector('#search-form').addEventListener('submit', event => event.preventDefault());
input.addEventListener('input', async () => {
  const request = ++sequence;
  const query = input.value.trim().toLowerCase();
  results.replaceChildren();
  results.hidden = !query;
  nav.hidden = Boolean(query);
  if (!query) { status.textContent = ''; return; }
  try {
    indexPromise ||= fetch('search.json').then(response => {
      if (!response.ok) throw new Error('Search unavailable');
      return response.json();
    }).catch(error => { indexPromise = undefined; throw error; });
    const index = await indexPromise;
    if (request !== sequence) return;
    const terms = query.split(/\s+/);
    const matches = index.filter(page => terms.every(term => (page.title + ' ' + page.text).toLowerCase().includes(term)))
      .sort((a, b) => Number(b.url === query + '.html') - Number(a.url === query + '.html') || Number(b.title.toLowerCase().includes(query)) - Number(a.title.toLowerCase().includes(query))).slice(0, 12);
    status.textContent = `${matches.length} results`;
    if (!matches.length) { results.textContent = 'No results. Try a skill name or a task such as “review”.'; return; }
    matches.forEach(page => {
      const link = document.createElement('a');
      link.href = page.url;
      link.textContent = page.title;
      const excerpt = document.createElement('small');
      const position = Math.max(0, page.text.toLowerCase().indexOf(terms[0]) - 35);
      excerpt.textContent = page.text.slice(position, position + 120) + '…';
      link.append(excerpt);
      results.append(link);
    });
  } catch {
    if (request !== sequence) return;
    status.textContent = 'Search could not load';
    results.textContent = 'Search could not load. Clear the search to browse the guides.';
  }
});
