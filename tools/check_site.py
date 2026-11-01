#!/usr/bin/env python3
"""Check the static site without installing anything (Python 3.9+)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit
from collections import Counter
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
errors = []
resources = set()
links = set()
external_links = set()

class Scan(HTMLParser):
    def __init__(self, page):
        super().__init__(); self.page = page
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'iframe', 'frame', 'frameset', 'applet', 'embed', 'object', 'form'):
            errors.append(f'{self.page}: obsolete or unexpected active element <{tag}>')
        for key, value in attrs:
            if key.startswith('on'):
                errors.append(f'{self.page}: unexpected event handler {key}')
            if key not in ('href', 'src', 'background', 'action', 'data') or not value:
                continue
            parsed = urlsplit(value)
            if parsed.scheme in ('mailto', 'tel', 'data') or value.startswith('#'):
                continue
            if parsed.netloc or parsed.scheme:
                if tag == 'a' and key == 'href':
                    external_links.add(value); continue
                errors.append(f'{self.page}: external resource {value}'); continue
            # A project Pages URL has a repository prefix: root-relative URLs
            # would incorrectly escape it, even if they work on the custom domain.
            if value.startswith('/'):
                errors.append(f'{self.page}: root-relative URL {value}')
            path = unquote(urlsplit(urljoin('https://local.invalid/' + self.page, value)).path).lstrip('/')
            if not path or path.endswith('/'):
                path += 'index.html'
            target = SITE / path
            if not target.is_file() or path not in all_paths:
                errors.append(f'{self.page}: missing or incorrectly capitalized local file {path}')
            (links if tag == 'a' else resources).add(path)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

all_paths = {str(p.relative_to(SITE)) for p in SITE.rglob('*') if p.is_file()}
pages = sorted(p for p in SITE.glob('*.html'))
for page in pages:
    content = page.read_text(encoding='utf-8')
    if re.search(r'homestead\.com|realtracker|/~site/|/defaultUser/', content, re.I):
        errors.append(f'{page.name}: leftover legacy dependency')
    if not re.search(r'charset\s*=\s*[\"\']?UTF-8', content, re.I):
        errors.append(f'{page.name}: missing UTF-8 declaration')
    Scan(page.name).feed(content)

for svg in SITE.rglob('*.svg'):
    try:
        ET.fromstring(svg.read_text())
    except ET.ParseError as e:
        errors.append(f'{svg.name}: invalid SVG: {e}')

report = json.loads((ROOT/'reports/cleanup.json').read_text())
for name, digest in report['original_media_sha256'].items():
    file = SITE/name
    if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
        errors.append(f'{name}: original media is missing or changed')
if len(pages) != report['published_html_pages']:
    errors.append('HTML page count differs from the original archive')
if not (SITE/'.nojekyll').is_file():
    errors.append('Missing .nojekyll')
if (SITE/'CNAME').exists() and (SITE/'CNAME').read_text().strip() != 'weimarfamily.org':
    errors.append('Unexpected domain in docs/CNAME')

result = {
    'passed': not errors,
    'html_pages_checked': len(pages),
    'unchanged_original_media_verified': len(report['original_media_sha256']),
    'local_link_targets_checked': len(links),
    'local_resource_targets_checked': len(resources),
    'external_links_preserved_not_crawled': len(external_links),
    'preexisting_missing_photos_marked': len(report['missing_photos']),
    'errors': errors,
}
print(json.dumps(result, indent=2))
if '--save' in sys.argv:
    (ROOT/'reports/verification.json').write_text(json.dumps(result, indent=2)+'\n')
sys.exit(0 if result['passed'] else 1)
