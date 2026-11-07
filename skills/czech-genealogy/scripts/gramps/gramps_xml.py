"""Pomocné funkce pro úpravy Gramps XML (ElementTree).

Použití ve skriptu verze (vstup nikdy nepřepisuje, výstup je nový soubor):

    import sys; sys.path.insert(0, '<cesta ke skillu>/scripts/gramps')
    from gramps_xml import G, NS
    g = G('rodokmen_v7.gramps')            # .gramps (gzip i nekomprimované) nebo .xml
    p = g.byid('person', 'I0049')
    g.addnote(p, 'Text poznámky')
    g.save('rodokmen_v8.gramps')            # .gramps se ukládá gzip jako export Gramps

Nové objekty dostávají unikátní handle a navazující ID, podřízené prvky se
vkládají v pořadí podle DTD (ORDER). Potom vždy spusť gramps_validate.py.
"""
import xml.etree.ElementTree as ET, re, time, os, gzip, io
NSU = 'http://gramps-project.org/xml/1.7.2/'
NS = '{' + NSU + '}'
ET.register_namespace('', NSU)
CH = str(int(time.time()))
ORDER = {
    'person': ['gender', 'name', 'eventref', 'lds_ord', 'objref', 'address', 'attribute', 'url', 'childof', 'parentin', 'personref', 'noteref', 'citationref', 'tagref'],
    'family': ['rel', 'father', 'mother', 'eventref', 'lds_ord', 'objref', 'childref', 'attribute', 'noteref', 'citationref', 'tagref'],
    'event': ['type', 'dateval', 'daterange', 'datespan', 'datestr', 'place', 'description', 'attribute', 'noteref', 'citationref', 'objref', 'tagref'],
    'citation': ['dateval', 'daterange', 'datespan', 'datestr', 'page', 'confidence', 'noteref', 'objref', 'srcattribute', 'sourceref', 'tagref'],
    'source': ['stitle', 'sauthor', 'spubinfo', 'sabbrev', 'noteref', 'objref', 'srcattribute', 'reporef', 'tagref'],
    'placeobj': ['ptitle', 'pname', 'code', 'coord', 'placeref', 'location', 'objref', 'url', 'noteref', 'citationref', 'tagref'],
    'object': ['file', 'attribute', 'noteref', 'dateval', 'daterange', 'datespan', 'datestr', 'citationref', 'tagref'],
}


class G:
    def __init__(s, path):
        s.path = path
        data = open(path, 'rb').read()
        if data[:2] == b'\x1f\x8b':
            data = gzip.decompress(data)
        raw = data.decode('utf8')
        s.head = raw[:raw.index('<database')]
        s.tree = ET.parse(io.BytesIO(data))
        s.r = s.tree.getroot()
        s.H = {e.get('handle'): e for e in s.r.iter() if e.get('handle')}
        s.n = 0
        s.tags = {e.get('name'): e.get('handle') for e in s.r.iter(NS + 'tag')}

    def sec(s, name):
        return s.r.find(NS + name)

    def handle(s):
        while True:
            s.n += 1
            h = '_d1%025d' % s.n
            if h not in s.H:
                return h

    def nextid(s, tag, prefix):
        mx = -1
        for e in s.r.iter(NS + tag):
            m = re.match(prefix + r'(\d+)$', e.get('id') or '')
            if m:
                mx = max(mx, int(m.group(1)))
        return '%s%04d' % (prefix, mx + 1)

    def byid(s, tag, i):
        for e in s.r.iter(NS + tag):
            if e.get('id') == i:
                return e
        raise KeyError(i)

    def new(s, section, tag, prefix, attrs=None):
        e = ET.Element(NS + tag)
        h = s.handle()
        e.set('handle', h)
        e.set('change', CH)
        if prefix:
            e.set('id', s.nextid(tag, prefix))
        for k, v in (attrs or {}).items():
            e.set(k, v)
        s.sec(section).append(e)
        s.H[h] = e
        return e

    def insert(s, parent, child):
        """vloží child do parent podle pořadí DTD (za poslední prvek stejného nebo dřívějšího druhu)"""
        order = ORDER[parent.tag[len(NS):]]
        idx = order.index(child.tag[len(NS):])
        pos = len(parent)
        for i, c in enumerate(list(parent)):
            cn = c.tag[len(NS):]
            if cn in order and order.index(cn) > idx:
                pos = i
                break
        parent.insert(pos, child)
        parent.set('change', CH)
        return child

    def ref(s, parent, tag, h, **a):
        e = ET.Element(NS + tag)
        e.set('hlink', h)
        for k, v in a.items():
            e.set(k, v)
        return s.insert(parent, e)

    def sub(s, parent, tag, text=None, **a):
        e = ET.Element(NS + tag)
        if text is not None:
            e.text = text
        for k, v in a.items():
            e.set(k, v)
        return s.insert(parent, e)

    def tag(s, obj, name):
        if not any(t.get('hlink') == s.tags[name] for t in obj.findall(NS + 'tagref')):
            s.ref(obj, 'tagref', s.tags[name])

    def untag(s, obj, name):
        for t in obj.findall(NS + 'tagref'):
            if t.get('hlink') == s.tags[name]:
                obj.remove(t)

    def note(s, text, typ='General'):
        n = s.new('notes', 'note', 'N', {'type': typ})
        ET.SubElement(n, NS + 'text').text = text
        return n

    def addnote(s, obj, text, typ='General'):
        n = s.note(text, typ)
        s.ref(obj, 'noteref', n.get('handle'))
        return n

    def delnote(s, obj, startswith):
        """odstraní z obj odkaz na poznámku začínající textem a smaže ji, pokud na ni nic jiného neodkazuje"""
        for nr in obj.findall(NS + 'noteref'):
            n = s.H[nr.get('hlink')]
            if (n.findtext(NS + 'text') or '').startswith(startswith):
                obj.remove(nr)
                obj.set('change', CH)
                h = n.get('handle')
                if not any(e.get('hlink') == h for e in s.r.iter()):
                    s.sec('notes').remove(n)
                    del s.H[h]
                return True
        return False

    def media(s, fname, desc, date=None):
        o = s.new('objects', 'object', 'O')
        f = ET.SubElement(o, NS + 'file')
        f.set('src', fname)
        f.set('mime', 'image/jpeg' if fname.endswith('.jpg') else 'image/png')
        f.set('description', desc)
        if date:
            ET.SubElement(o, NS + 'dateval').set('val', date)
        return o

    def source(s, title, repo_h, callno, author=None, note=None):
        for e in s.r.iter(NS + 'source'):
            if e.findtext(NS + 'stitle') == title:
                return e
        so = s.new('sources', 'source', 'S')
        s.sub(so, 'stitle', title)
        if author:
            s.sub(so, 'sauthor', author)
        if note:
            s.addnote(so, note, 'Source Note')
        s.ref(so, 'reporef', repo_h, medium='Book', callno=callno)
        return so

    def citation(s, src, page, conf, obj=None, date=None, url=None, tags=('ověřeno',)):
        c = s.new('citations', 'citation', 'C')
        if date:
            s.sub(c, 'dateval', val=date)
        s.sub(c, 'page', page)
        s.sub(c, 'confidence', str(conf))
        if url:
            s.addnote(c, url, 'Citation')
        if obj is not None:
            s.ref(c, 'objref', obj.get('handle'))
        s.ref(c, 'sourceref', src.get('handle'))
        for t in tags:
            s.tag(c, t)
        return c

    def place(s, name, typ, parent=None, alt=()):
        for p in s.r.iter(NS + 'placeobj'):
            pn = p.find(NS + 'pname')
            pr = p.find(NS + 'placeref')
            if pn is not None and pn.get('value') == name and (
                    (pr is None and parent is None) or
                    (pr is not None and parent is not None and pr.get('hlink') == parent.get('handle'))):
                return p
        p = s.new('places', 'placeobj', 'P', {'type': typ})
        s.sub(p, 'pname', value=name)
        for a in alt:
            ET.SubElement(p, NS + 'pname').set('value', a)
        if parent is not None:
            s.ref(p, 'placeref', parent.get('handle'))
        return p

    def event(s, typ, date=None, place=None, desc=None, datetype=None):
        e = s.new('events', 'event', 'E')
        s.sub(e, 'type', typ)
        if date:
            a = {'val': date}
            if datetype:
                a['type'] = datetype
            s.sub(e, 'dateval', **a)
        if place is not None:
            s.ref(e, 'place', place.get('handle'))
        if desc:
            s.sub(e, 'description', desc)
        return e

    def person(s, first, surname, gender):
        p = s.new('people', 'person', 'I')
        s.sub(p, 'gender', gender)
        n = ET.Element(NS + 'name')
        n.set('type', 'Birth Name')
        ET.SubElement(n, NS + 'first').text = first
        ET.SubElement(n, NS + 'surname').text = surname
        s.insert(p, n)
        return p

    def family(s, father=None, mother=None, rel='Married'):
        f = s.new('families', 'family', 'F')
        s.sub(f, 'rel', type=rel)
        if father is not None:
            s.ref(f, 'father', father.get('handle'))
            s.ref(father, 'parentin', f.get('handle'))
        if mother is not None:
            s.ref(f, 'mother', mother.get('handle'))
            s.ref(mother, 'parentin', f.get('handle'))
        return f

    def child(s, fam, ch, frel='Birth', mrel='Birth'):
        a = {} if (frel == 'Birth' and mrel == 'Birth') else {'frel': frel, 'mrel': mrel}
        s.ref(fam, 'childref', ch.get('handle'), **a)
        s.ref(ch, 'childof', fam.get('handle'))

    def eventref(s, obj, ev, role='Primary'):
        s.ref(obj, 'eventref', ev.get('handle'), role=role)

    def save(s, out):
        assert not os.path.exists(out), out + ' existuje!'
        ET.indent(s.tree, '  ')
        body = ET.tostring(s.r, encoding='unicode')
        data = (s.head + body + '\n').encode('utf8')
        if out.endswith('.gramps'):
            data = gzip.compress(data, 9)
        with open(out, 'xb') as f:
            f.write(data)
        print('uloženo', out)
