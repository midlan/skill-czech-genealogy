---
name: czech-genealogy
description: Genealogický výzkum v českých a slovenských pramenech a údržba rodokmenu v Gramps. Použij, když uživatel hledá předky, sestavuje rodokmen, potřebuje žádost na matriku (doslovný výpis), hledá v digitalizovaných matrikách (eBadatelna SOA Praha, SOA Třeboň, Porta fontium, ARON, Litoměřice, Opava), čte matriční zápis, legionářskou kartu VÚA nebo upravuje soubor .gramps. Czech/Slovak genealogy, family tree, parish registers, archives, Gramps XML.
compatibility: Shell s Pythonem 3 a přístupem k internetu (archivní portály, Mapy.com API). Volitelně ImageMagick (náhledy, slepení dlaždic), xmllint (validace .gramps) a prohlížeč pro portály bez nástroje. Orchestrace subagentů je navržená pro Claude Code.
metadata:
  author: midlan
  version: "2.0"
  repository: https://github.com/midlan/czech-genealogy
---

# Česká genealogie: matriky, archivy, Gramps

Postup pro sestavování rodokmenu z českých (a slovenských) pramenů. S uživatelem komunikuj česky.

## Zásady komunikace
- Když se ptáš na chybějící nebo nejasný údaj, vždy uveď **celé jméno osoby a její vztah k uživateli** (např. „Marie Houdková, matka tvého pradědy Jana, neboli praprababička“) a **nápovědu, kde údaj hledat** (konkrétní kniha, snímek, rubrika, doklad v rodině).
- Odlišuj, co je **doloženo zápisem**, co je **rodinné podání** a co je **hypotéza**. Hypotézy nikdy nezapisuj jako fakt.
- Nejistá čtení označuj `[nejisté]` a uváděj varianty.
- **Nikdy nesestavuj odkaz podle vzoru.** Do citací dávej jen adresy, které byly skutečně načteny; když nejde ověřit, uveď místo odkazu vyhledávací dotaz.
- Rodná čísla do rodokmenu nezapisuj (osobní identifikátor, pro rodokmen zbytečný).

## Kde co najdeš
Čti jen to, co aktuální krok potřebuje:

| Soubor | Kdy |
|---|---|
| [references/matriky-a-archivy.md](references/matriky-a-archivy.md) | právní rámec matrik (lhůty, § 25, osvojení), šablona žádosti na matriku, přehled archivů, VÚA (legionáři, žádost o spis) |
| [references/nastroje-archivy.md](references/nastroje-archivy.md) | hledání knih a stahování snímků z portálů bez prohlížeče (`scripts/archivy/`) |
| [references/farnosti.md](references/farnosti.md) | ověřená přiřazení obcí k farnostem a knihám (doplňuj nové nálezy) |
| [references/cteni-zapisu.md](references/cteni-zapisu.md) | čtení zápisů: zkratky, poznámky na okraji, indexy, typické chyby; hledání sňatků a sourozenců |
| [references/orchestrace.md](references/orchestrace.md) | delegování na čtecí subagenty, povinná kontrola jejich práce, šablona zadání |
| [references/archive-reader.md](references/archive-reader.md) | instrukce pro čtecího agenta (jak najít knihu, stáhnout originál, číst, co vrátit) |
| [references/gramps.md](references/gramps.md) | úpravy `.gramps`: verzování, zdroje a citace, spolehlivost, štítky, místa a souřadnice, média, kmotři |

Skripty: `scripts/archivy/` (portály archivů, převzato z sarsonj/rodokmen-skill, MIT), `scripts/souradnice_mapy.py` (souřadnice domů podle čísla popisného přes Mapy.com API).

## Pracovní postup
1. Ze známých údajů urči další krok: nejdřív **narození** osoby (uvede rodiče, prarodiče, často datum sňatku rodičů), pak **sňatek rodičů** (uvede data narození a rodiče snoubenců). Co je ještě na matrice (lhůty 100/75 let), řeš žádostí – viz matriky-a-archivy.md.
2. Hledání v digitalizovaných matrikách proveď nástroji ze `scripts/archivy/`, ideálně přes **čtecí subagenty** (orchestrace.md). Prohlížeč jen jako záloha. Když nemáš shell ani subagenty (např. chat), připrav uživateli prompt pro agenta podle šablony v orchestrace.md.
3. **Validuj každý obrázek sám:** přečti originál, porovnej s přepisem čtecího agenta, oprav chyby (časté: povolání, jména obcí, svědci, roky a měsíce v poznámkách) a výslovně je uživateli uveď. Negativní nález platí jen pro skutečně přečtený rozsah.
4. Doplň do rodokmenu podle gramps.md – vždy jako **novou verzi souboru** (`_v2`, `_v3`…), vstup nikdy nepřepisuj; validuj proti DTD a zkontroluj duplicitní handle a neplatné odkazy.
5. Nové ověřené přiřazení obce k farnosti/knize doplň do farnosti.md (nebo ho navrhni správci skillu).
6. Navrhni další kolo: kde je strom nejkratší a co je online dosažitelné; co vyžaduje žádost (matrika, SOkA, VÚA) a odhad ceny.

## Nejdůležitější pravidla rodokmenu (podrobnosti v gramps.md)
- Každý údaj má citaci se zdrojem v repozitáři a signaturou; spolehlivost: vysoká = matrika a úřední doklad, normální = rodinné podání nebo neověřený přepis, nízká = odvozené údaje, velmi nízká = hypotéza, velmi vysoká = jen DNA.
- Štítky `ověřeno`, `hypotéza`, `k dohledání`.
- Místa v hierarchii stát → kraj → okres → obec → část obce → číslo popisné.
- Originály snímků: název `<datum>_<typ>_<příjmení>_<zdroj>.jpg`, jeden soubor = jedna událost (jinak kopie), názvy se nikdy nemění, originály se neupravují, duplicity podle kontrolního součtu.
- Kmotři a svědci nejsou osoby, ale strukturovaná poznámka události; ohlášky do poznámky ke sňatku.
- Archivy povolují kopie jen pro soukromé studium – strom s obrázky nezveřejňuj.
