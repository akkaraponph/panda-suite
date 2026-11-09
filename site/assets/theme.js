(() => {
  const root = document.documentElement;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const storageKey = 'panda-docs-theme';
  let preference;
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored === 'light' || stored === 'dark') preference = stored;
  } catch {
    // The toggle still works when browser storage is unavailable.
  }

  function applyTheme() {
    const theme = preference || (system.matches ? 'dark' : 'light');
    root.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]')
      ?.setAttribute('content', theme === 'dark' ? '#18151f' : '#392c73');
    const toggle = document.querySelector('#theme-toggle');
    if (toggle) {
      toggle.hidden = false;
      toggle.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  }

  // Run before the stylesheet so a saved dark theme does not flash light.
  applyTheme();
  system.addEventListener('change', () => {
    if (!preference) applyTheme();
  });
  document.addEventListener('DOMContentLoaded', () => {
    applyTheme();
    document.querySelector('#theme-toggle').addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try {
        localStorage.setItem(storageKey, preference);
      } catch {
        // Keep this page usable even when the preference cannot be saved.
      }
      applyTheme();
    });
  });
})();
