"""Porovnání dvou verzí rodokmenu podle handle (NEW / DEL / MOD), atribut change se ignoruje.

    python -X utf8 gramps_diff.py <stará.gramps> <nová.gramps>

Hodí se ke kontrole, že skript verze změnil jen to, co měl, a k porovnání
exportu uživatele s poslední odeslanou verzí (chybí-li něco, export je neúplný).
"""
import sys, gzip, io, difflib, xml.etree.ElementTree as ET

NS = '{http://gramps-project.org/xml/1.7.2/}'


def load(f):
    data = open(f, 'rb').read()
    if data[:2] == b'\x1f\x8b':
        data = gzip.decompress(data)
    d = {}
    for e in ET.parse(io.BytesIO(data)).getroot().iter():
        h = e.get('handle')
        if h:
            c = ET.fromstring(ET.tostring(e))
            c.attrib.pop('change', None)
            d[h] = (e.tag.replace(NS, ''), e.get('id'), ET.tostring(c, encoding='unicode'))
    return d


a, b = load(sys.argv[1]), load(sys.argv[2])
for h in b:
    if h not in a:
        print('NEW ', b[h][0], b[h][1])
        print('    ', b[h][2][:700].replace('\n', ' '))
for h in a:
    if h not in b:
        print('DEL ', a[h][0], a[h][1])
for h in a:
    if h in b and a[h][2] != b[h][2]:
        print('MOD ', a[h][0], a[h][1])
        for l in difflib.unified_diff(a[h][2].split('\n'), b[h][2].split('\n'), lineterm='', n=0):
            if l[:2] not in ('--', '++', '@@'):
                print('    ', l.strip()[:400])
