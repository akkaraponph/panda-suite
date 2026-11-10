#!/usr/bin/env python3
"""Build the GitHub Pages docs from repository Markdown."""
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
REPO = 'https://github.com/akkaraponph/panda-suite'
SKILLS = [
    ('panda-lead', 'Panda Lead'),
    ('panda-craft', 'Panda Craft'),
    ('panda-git', 'Panda Git'),
    ('panda-brainstorm', 'Panda Brainstorm'),
    ('panda-research', 'Panda Research'),
    ('panda-learn', 'Panda Learn'),
    ('panda-requirements', 'Panda Requirements'),
    ('panda-impact', 'Panda Impact'),
    ('panda-plan', 'Panda Plan'),
    ('panda-spec', 'Panda Spec'),
    ('panda-execute', 'Panda Execute'),
    ('panda-test', 'Panda Test'),
    ('panda-debugger', 'Panda Debugger'),
    ('panda-sec', 'Panda Sec'),
    ('panda-perf', 'Panda Perf'),
    ('panda-review', 'Panda Review'),
    ('panda-simplify', 'Panda Simplify'),
    ('panda-refactor', 'Panda Refactor'),
    ('buddhist-method', 'Buddhist Method'),
    ('panda-write', 'Panda Write'),
    ('panda-manual', 'Panda Manual'),
    ('panda-release', 'Panda Release'),
    ('panda-skill-lab', 'Panda Skill Lab'),
]


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / 'site/assets', OUT / 'assets')
    shutil.copy2(ROOT / 'images/branding.png', OUT / 'assets/branding.png')
    (OUT / '.nojekyll').touch()
    usage = (ROOT / 'docs/usage.md').read_text()
    readme = (ROOT / 'README.md').read_text()
    version = json.loads((ROOT / 'plugin.json').read_text())['version']
    pages = {}

    def add(slug, title, source, text=None):
        pages[slug] = (title, source, text if text is not None else (ROOT / source).read_text())

    add('index', 'Welcome', 'site/index.md')
    install = readme.split('## Install from this checkout\n', 1)[1].split('\n## Examples', 1)[0]
    add('installation', 'Installation', 'README.md', '# Install Panda Suite\n\n' + install)
    add('usage', 'Complete usage guide', 'docs/usage.md')
    catalog = '# Find your skill\n\nChoose a specialist directly, or let [Panda Lead](panda-lead.html) select the activities your task needs. Each guide includes inputs, a copyable prompt, and expected results.\n\n'
    catalog += '| Skill | Use it for |\n| --- | --- |\n'
    table = readme.split('| Skill | Use it for |', 1)[1].split('\n\n', 1)[0]
    for line in table.splitlines():
        match = re.match(r'\| `([^`]+)` \| (.+) \|', line)
        if match:
            name, desc = match.groups()
            catalog += f'| [{name}]({name}.html) | {desc} |\n'
    add('skills', 'Skill directory', 'README.md', catalog)
    packaged = {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}
    assert packaged == {slug for slug, _ in SKILLS}, 'Update the site skill list for the packaged catalog'
    for slug, title in SKILLS:
        if slug == 'panda-lead':
            body = usage.split('## Choose a workflow\n', 1)[1].split('\n## Product discovery', 1)[0]
        else:
            match = re.search(r'^### ' + re.escape(title) + r'\n(.*?)(?=^##? |^### |\Z)', usage, re.M | re.S)
            if not match:
                raise ValueError(f'Missing usage section: {title}')
            body = match.group(1)
        intro = ('Examples use **standalone Codex** names. For a Codex plugin, use '
                 '`$panda-suite:' + slug + '`; for a Claude Code plugin, use '
                 '`/panda-suite:' + slug + '`. See [all invocation formats](usage.html#invoke-a-skill).\n\n')
        add(slug, title, 'docs/usage.md', '# ' + title + '\n\n' + intro + body +
            f'\n\n## Skill instructions\n\nRead the [full {title} instructions]({REPO}/blob/main/skills/{slug}/SKILL.md) in the repository.\n')
    for slug, title, source in [
        ('routing', 'Workflows and routing', 'docs/routing.md'),
        ('architecture', 'Architecture', 'docs/architecture.md'),
        ('skill-contract', 'Extend the suite', 'docs/skill-contract.md'),
        ('integration', 'Upstream maintenance', 'docs/integration.md'),
        ('verification', 'Verification record', 'docs/verification.md'),
        ('release-v1-1-1', 'Release v1.1.1', 'docs/v1.1.1.md'),
        ('release-v1-2-0', 'Release v1.2.0', 'docs/v1.2.0.md'),
        ('release-v1-5-1', 'Release v1.5.1', 'docs/v1.5.1.md'),
        ('release-v1-5-0', 'Release v1.5.0', 'docs/v1.5.0.md'),
        ('release-v1-4-0', 'Release v1.4.0', 'docs/v1.4.0.md'),
        ('release-v1-3-0', 'Release v1.3.0', 'docs/v1.3.0.md'),
        ('notices', 'Source and license notices', 'SOURCE_NOTICES.md'),
        ('thai', 'ภาพรวมภาษาไทย', 'README.th.md'),
        ('maintaining', 'Maintain this site', 'site/maintaining.md'),
    ]:
        add(slug, title, source)
    source_routes = {source: slug + '.html' for slug, (_, source, _) in pages.items()
                     if slug not in {s for s, _ in SKILLS} | {'skills', 'installation'}}
    source_routes['README.md'] = 'index.html'
    source_routes['docs/usage.md'] = 'usage.html'
    # Generated page links stay relative to the project path on GitHub Pages.
    def url_rewrite(url, source):
        if url.startswith(('#', '/', 'https:', 'http:', 'mailto:', 'data:')):
            return url
        parts = urlsplit(url)
        if parts.path.endswith('.html'):
            return url
        resolved = (ROOT / source).parent.joinpath(parts.path).resolve()
        try:
            path = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            raise ValueError(f'Link outside repository: {source}: {url}')
        frag = '#' + parts.fragment if parts.fragment else ''
        if path in source_routes:
            return source_routes[path] + frag
        if path.startswith('images/'):
            return 'assets/' + Path(path).name
        return REPO + '/blob/main/' + path + frag

    groups = [
        ('Get started', [('index', 'Welcome'), ('installation', 'Installation'), ('skills', 'Skill directory'), ('usage', 'Complete usage guide')]),
        ('Skills', SKILLS),
        ('Project', [('routing', 'Workflows and routing'), ('architecture', 'Architecture'), ('skill-contract', 'Extend the suite'), ('integration', 'Upstream maintenance'), ('verification', 'Verification record'), ('release-v1-5-1', 'Release v1.5.1'), ('release-v1-5-0', 'Release v1.5.0'), ('release-v1-4-0', 'Release v1.4.0'), ('release-v1-3-0', 'Release v1.3.0'), ('release-v1-2-0', 'Release v1.2.0'), ('release-v1-1-1', 'Release v1.1.1'), ('notices', 'Source and licenses'), ('thai', 'ภาษาไทย'), ('maintaining', 'Maintain this site')]),
    ]
    search = []
    template = (ROOT / 'site/template.html').read_text()
    for slug, (title, source, content) in pages.items():
        md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc', 'sane_lists'], extension_configs={'toc': {'permalink': False}})
        rendered = md.convert(content)
        rendered = re.sub(r'(href|src)="([^"]+)"', lambda m: m[1] + '="' + html.escape(url_rewrite(html.unescape(m[2]), source), quote=True) + '"', rendered)
        nav = ''
        for group, entries in groups:
            nav += f'<div class="nav-group"><p>{group}</p>'
            for target, label in entries:
                current = ' aria-current="page"' if target == slug else ''
                nav += f'<a href="{target}.html"{current}>{label}</a>'
            nav += '</div>'
        toc = md.toc if len(md.toc_tokens) else ''
        hero = '<figure class="brand-art"><img src="assets/branding.png" alt="Panda Suite cyberpunk panda artwork" width="836" height="471"><figcaption>Think clearly. Build carefully. Ship confidently.</figcaption></figure>' if slug == 'index' else ''
        values = {'title': html.escape(title), 'nav': nav, 'toc': toc, 'content': rendered, 'version': html.escape(version), 'source': REPO + '/blob/main/' + source, 'hero': hero, 'lang': 'th' if slug == 'thai' else 'en', 'page': slug}
        result = template
        for key, value in values.items():
            result = result.replace('{{' + key + '}}', value)
        (OUT / (slug + '.html')).write_text(result)
        plain = html.unescape(re.sub('<[^>]+>', ' ', rendered))
        search.append({'title': title, 'url': slug + '.html', 'text': re.sub(r'\s+', ' ', plain)})
    (OUT / 'search.json').write_text(json.dumps(search, ensure_ascii=False))
    print(f'Built {len(pages)} pages, including {len(SKILLS)} skill guides, in {OUT}')


if __name__ == '__main__':
    build()
