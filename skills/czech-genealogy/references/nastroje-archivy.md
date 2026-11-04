# Strojový přístup k archivům (bez prohlížeče)

Kdy číst: před hledáním v digitalizovaných matrikách a před zadáním úlohy čtecímu agentovi.

Nástroje ve složce `scripts/archivy/` (převzaté z projektu sarsonj/rodokmen-skill, licence MIT) hledají knihy a stahují originály snímků přímo z portálů – **bez Chromu a bez přihlášení**. Spouštěj je z pracovní složky rodokmenu (tam vzniká mezipaměť `pracovni/.cache_*`): `python -I <cesta ke skillu>/scripts/archivy/<nástroj> …`, na Windows `python -I -X utf8 …`. Nápověda = nástroj bez parametrů. Náhled, výřez a slepení dlaždic potřebují **ImageMagick** (`magick`; Windows `winget install ImageMagick.ImageMagick`); stažení celého snímku z eBadatelny ho nepotřebuje.

| Archiv | Nástroj | Poznámky |
|---|---|---|
| SOA Praha – eBadatelna | `ebadatelna.py hledat "Obec"` → `matriky "Obec"` (matrikaId, kniha, druh, roky, fara, snímky) → `info <matrikaId>` (obsah, rozvržení stran po vesnicích) → `snimek <matrikaId> <snímek> <soubor.jpg> [nahled] [x0,y0,x1,y1]`; `link` = trvalý odkaz | Celý originál jedním požadavkem. Archiválie (urbáře, gruntovní knihy): `a-info`, `a-snimek` (id z adresy `…/archivalieId/<id>`). Údržba denně kolem 4:44. |
| SOA Třeboň – DigiArchiv | `trebon.py misto "Obec"` (**zkontroluj vypsaný název a okres**) → `svazky <id>` → `rejstrik <id_knihy> <písmeno>` (dobrovolnický jmenný rejstřík, ne u všech knih) → `snimek <id_knihy> <snímek> <soubor.jpg>` | Bez přihlášení; snímek slepí z dlaždic (ImageMagick). Prázdný rejstřík = rejstřík chybí, ne „osoba tam není“. |
| SOA Plzeň – Porta fontium | `portafontium.py fara <fara>` → `info <kniha>` (u knih po vesnicích folia obcí) → `snimek <kniha> <snímek> <soubor.jpg>` | Obec → fara nástroj nehledá (stránka `portafontium.eu/searching/register?search_api_views_fulltext_1=<obec>`). Snímek ≈ folio. |
| SOA Zámrsk – ARON | `aron_search.py "Obec[,Fara]"` → `aron_img.py <apu_id> info` → `aron_img.py <apu_id> <snímek> 0 <soubor.jpg>` (0 = plné rozlišení, 1 = poloviční na orientaci) | Stejnojmenné obce zužuj čárkou („Vinice,Hořice“). |
| SOA Litoměřice | `soal_zoomify.py <cesta> 0 <soubor.jpg>` | Knihu a cestu k obrázkům najdi v prohlížeči, snímky pak jen nástrojem. **Po ~100 rychlých požadavcích na aplikaci blokace na 30 min.** |
| ZA Opava | `soal_zoomify.py "<celá adresa obrázku>" 0 <soubor.jpg>` | Hledání jen v prohlížeči (ochrana proti robotům, CAPTCHU řeší uživatel, nikdy agent); denní limity. |
| AHMP Praha | `ahmp_search.sh "Farnost"` → `ahmp_scan.py <XID> <snímek> <soubor.jpg>` | Nový digi.ahmp.cz nepoužívat (ochrana proti robotům). |
| Pražské policejní přihlášky 1850–1914 | `policie_prihlasky.py <Příjmení> [Jméno] [od] [do]`, `karta …` | Nepokrývá předměstí samostatná do 1922 (Smíchov, Vinohrady, Žižkov, Karlín). |
| Noviny | `kramerius.py '<SOLR dotaz>'` (NK ČR), `anno.py '"Jméno"' od do` (rakouské noviny, jména německy), `anno_snap.py` | Jen vodítka, ztotožňuj podle více údajů. |
| Matricula (Rakousko, Bavorsko, Polsko) | `matricula_dl.sh`, `matricula_batch.sh` | Adresu obrázku (s csrf) je nutné vzít z prohlížeče. |

Pravidla pro nástroje:
- **Ohled na server:** stahuj jen snímky, které čteš; žádné hromadné stahování knih; na orientaci (hledání roku/měsíce) používej `nahled` nebo nižší rozlišení, plné jen u nalezeného zápisu.
- Originál ukládej pod názvem podle pravidel médií (viz [gramps.md](gramps.md) → Média) rovnou do složky snímků; výřezy na čtení dávej do pracovní složky (`pracovni/`), originál neupravuj.
- Podpříkaz `svazek` zapisuje do `data/svazky.json` v pracovní složce (formát projektu rodokmen-skill) – v tomto workflow ho nepotřebuješ, citace patří do Gramps.
- Když nástroj selže kvůli změně portálu, popiš chybu, přepni na prohlížeč (viz [archive-reader.md](archive-reader.md)) a navrhni uživateli nahlásit problém v upstreamu.
- **Prohlížeč (Chrome)** je jen záložní cesta: Litoměřice/Opava (najít knihu), MZA Brno – Acta Publica, FamilySearch, MyHeritage a portály bez nástroje.
