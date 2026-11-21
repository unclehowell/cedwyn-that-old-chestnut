#!/usr/bin/env python3
"""Apply data/reply-dates-*.json to public/_db/view.json: for each listed id, set the title's
'reply of date not yet read' to 'reply of <date>', and set date, provenance.date and finding.negative_date.
Nothing else in a record changes. Keeps the file's compact one-line format. Usage:
  python3 tools/apply_reply_dates.py data/reply-dates-2026-11-19.json
(Claude seat, 19 Nov 2026)"""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
VIEW = ROOT / 'public' / '_db' / 'view.json'
fix = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))['dates']
v = json.loads(VIEW.read_text(encoding='utf-8'))
n = 0
for c in v.get('chestnuts', []):
    f = fix.get(c.get('id'))
    if not f: continue
    d = f['date']
    c['title'] = c['title'].replace('reply of date not yet read', 'reply of ' + d)
    c['date'] = {'display': d, 'sort': d, 'precision': 'day'}
    c.setdefault('provenance', {})['date'] = d
    c.setdefault('finding', {})['negative_date'] = d
    n += 1
VIEW.write_text(json.dumps(v, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print('dated', n, 'of', len(fix))
