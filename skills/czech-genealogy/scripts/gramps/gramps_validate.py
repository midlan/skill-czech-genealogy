"""Kontrola souboru Gramps XML: validace proti DTD, duplicitní handle, neplatné odkazy.

    python gramps_validate.py <soubor.gramps|.xml> [cesta/k/grampsxml.dtd]

Soubor může být gzip (export Gramps) i nekomprimovaný. DTD: druhý parametr,
proměnná GRAMPS_DTD, nebo se hledá v obvyklých instalacích Gramps. Potřebuje lxml
(pip install lxml). Návratový kód 0 = vše v pořádku.
"""
import sys, os, gzip, glob, collections
from lxml import etree


def find_dtd():
    if len(sys.argv) > 2:
        return sys.argv[2]
    if os.environ.get('GRAMPS_DTD'):
        return os.environ['GRAMPS_DTD']
    pats = [r'C:\Program Files\Gramps*\share\gramps\grampsxml.dtd',
            '/usr/share/gramps/grampsxml.dtd', '/usr/local/share/gramps/grampsxml.dtd',
            '/Applications/Gramps.app/Contents/Resources/share/gramps/grampsxml.dtd']
    for p in pats:
        hits = sorted(glob.glob(p))
        if hits:
            return hits[-1]
    sys.exit('DTD nenalezeno – zadej cestu nebo GRAMPS_DTD (soubor grampsxml.dtd z repozitáře gramps-project)')


raw = open(sys.argv[1], 'rb').read()
if raw[:2] == b'\x1f\x8b':
    raw = gzip.decompress(raw)
doc = etree.fromstring(raw, etree.XMLParser(load_dtd=False, resolve_entities=False, no_network=True))
dtd = etree.DTD(find_dtd())
ok = dtd.validate(doc)
print('DTD:', 'OK' if ok else 'CHYBY')
for e in list(dtd.error_log)[:20]:
    print('  ', e)
hs = [e.get('handle') for e in doc.iter() if e.get('handle')]
dup = [h for h, n in collections.Counter(hs).items() if n > 1]
known = set(hs)
bad = sorted({e.get('hlink') for e in doc.iter() if e.get('hlink') and e.get('hlink') not in known})
print('handle:', len(hs), '| duplicitní:', dup or 'žádné', '| neplatné odkazy:', bad or 'žádné')
sys.exit(0 if ok and not dup and not bad else 1)
