"""Audit the module lesson inventory and inline JavaScript without loading the site.

Run from any directory: python scripts/audit_lessons.py
Requires Python 3.11+ and Node.js. No dependencies or network access.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [12, 8, 11, 15, 11, 9, 17, 10, 7]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.current = None
        self.title = ''
        self.in_title = False
        self.lang = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'title':
            self.in_title = True
        if tag == 'script':
            kind = attrs.get('type', '').lower()
            self.current = [] if 'src' not in attrs and kind in ('', 'text/javascript', 'application/javascript', 'module') else None
            self.module = kind == 'module'
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.current is not None:
            self.current.append(data)
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.current is not None:
            self.scripts.append((''.join(self.current), self.module))
            self.current = None

def audit():
    errors, inventory, counts = [], [], []
    scripts_checked = 0
    for module in range(1, 10):
        pages = sorted((ROOT / f'm{module}').glob('licao-*/index.html'))
        counts.append(len(pages))
        for path in pages:
            rel = path.relative_to(ROOT).as_posix()
            raw = path.read_bytes()
            page = Page()
            page.feed(raw.decode('utf-8', errors='strict'))
            if not page.title.strip():
                errors.append(f'{rel}: missing title')
            if page.lang != 'pt-PT':
                errors.append(f'{rel}: lang must be pt-PT')
            if not path.parent.name.startswith(f'licao-m{module}-'):
                errors.append(f'{rel}: module mismatch')
            for number, (source, is_module) in enumerate(page.scripts, 1):
                command = ['node'] + (['--input-type=module'] if is_module else []) + ['--check']
                result = subprocess.run(command, input=source, text=True, encoding='utf-8', capture_output=True, timeout=15)
                scripts_checked += 1
                if result.returncode:
                    errors.append(f'{rel}: script {number}: {result.stderr.strip()}')
            inventory.append({'path': rel, 'title': page.title, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    if counts != EXPECTED:
        errors.append(f'Baseline inventory changed: expected {EXPECTED}, found {counts}. Review additions/removals before updating EXPECTED.')
    return {'module_counts': counts, 'total': sum(counts), 'inline_scripts_checked': scripts_checked, 'errors': errors, 'lessons': inventory}

if __name__ == '__main__':
    try:
        result = audit()
    except (OSError, UnicodeError, subprocess.TimeoutExpired) as error:
        print(f'Audit could not run: {error}', file=sys.stderr)
        sys.exit(2)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    sys.exit(bool(result['errors']))


