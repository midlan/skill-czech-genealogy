# Gramps – údržba rodokmenu

Kdy číst: vždy před úpravou souboru `.gramps`.

- Výměnný formát: **Gramps XML (`.gramps`)**, ne GEDCOM (GEDCOM ztrácí typy rodin, hlavní rodiče a poznámky; `ADDR` u událostí s místem Gramps zahodí).
- **Vždy vycházej z posledního exportu uživatele**, případně z poslední verze, kterou jsi poslal, pokud uživatel potvrdí, že nic neměnil. Uživatel importuje do **nového prázdného** rodokmenu (import do stávajícího = duplicity).
- **Verzování: vstupní soubor nikdy nepřepisuj.** Každá úprava = nový soubor vedle vstupu: `rodokmen.gramps` → `rodokmen_v2.gramps` → `rodokmen_v3.gramps`… Pokud název už končí `_vN`, zvyš N; nikdy nepřepiš existující soubor (když `_vN` existuje, vezmi první volné číslo). Jako vstup ber nejvyšší verzi, pokud uživatel neurčí jinak, a na začátku i na konci napiš, ze kterého souboru vycházíš a jaký soubor vznikl. Starší verze nemaž – slouží jako záloha a k porovnání.
- Změny dělej skriptem (Python, `xml.etree`): nové osoby/události/citace/zdroje/místa/poznámky s unikátními handle a navazujícími ID; existující záznamy upravuj cíleně. Dodržuj pořadí elementů podle DTD (person: gender, name, eventref, …, childof, parentin, noteref, citationref; family: rel, father, mother, eventref, childref, noteref, citationref; event: type, dateval/daterange, place, description, noteref, citationref).
- Datum: `dateval val="YYYY-MM-DD"`, `type="before"` / `"about"`, rozsah `daterange start/stop`.
- Vztah dítěte: `childref` `frel`/`mrel` = Birth, Adopted, Stepchild…; osvojení jako druhá rodina + událost Adopted; hlavní rodiče = první `childof` (uživatel může přeřadit v zobrazení Vztahy → Seřadit).
- Rodné a vdané jméno jako dvě jména (Birth Name + Married Name, `alt="1"`).
- Před odesláním: validace proti DTD (`xmllint --dtdvalid grampsxml.dtd`, DTD z repozitáře gramps-project), kontrola duplicitních handle a neplatných odkazů.

## Zdroje, repozitáře, citace
- **Repozitář** = instituce, kde zdroj leží (SOA Praha, SOA Třeboň, matriční úřad Mladá Boleslav, VÚA–VHA, Rodinný archiv…). **Zdroj** = kniha/fond s odkazem na repozitář a **signaturou** (`reporef callno`, např. „Radošovice 13“). **Citace** = konkrétní stránka/snímek, URL a vazba na médium.
- Každý údaj má citaci; rodinné podání je samostatný zdroj v repozitáři „Rodinný archiv / rodinné podání“.
- **Spolehlivost citace** (Gramps confidence):
  - **velmi vysoká** – jen genetické (DNA) testy,
  - **vysoká** – matriční zápis, doslovný výpis, rodný list a jiný úřední doklad,
  - **normální** – rodinné podání podané jako fakt; přepis zatím neověřený proti originálu,
  - **nízká** – podání typu „možná to tak bylo“; nepřímé odvození (např. datum úmrtí dopočtené z věku),
  - **velmi nízká** – hypotéza (např. ztotožnění s legionářskou kartou).

## Štítky
- `ověřeno` – údaj potvrzený originálem, `hypotéza` – nepotvrzené ztotožnění nebo výklad, `k dohledání` – známá mezera (chybí zápis, nečitelné příjmení). Štítky přiřazuj osobám, událostem i citacím; slouží uživateli jako filtr a seznam práce.

## Místa
- **Hierarchie:** stát (dobový název s rozsahem let, např. Rakousko-Uhersko / Československo / Česko) → kraj → okres (dobový) → obec → část obce → **číslo popisné** jako samostatné místo typu Building/House. Alternativní názvy (německé – Jungbunzlau, Wlaschim) jako další jména místa.
- **Souřadnice pro domy:** strojově přes Mapy.com API skriptem `scripts/souradnice_mapy.py` (cesta od kořene skillu) (ne přes prohlížeč). Připrav CSV `id;dotaz;cast;cp;obec` (např. `P0107;Podchlumí 78, Mladá Boleslav;Podchlumí;78;Mladá Boleslav`), spusť `python scripts/souradnice_mapy.py mista.csv -o souradnice.csv`. Klíč v proměnné `MAPY_API_KEY` (získá se na https://developer.mapy.com/account/projects, základní tarif zdarma); když chybí, požádej o něj uživatele. Skript přijme jen adresu se stejným **číslem popisným** (ne orientačním, ne evidenčním) ve stejné části obce; u „nenalezeno“ projdi sloupec kandidátů ručně – časté chyby: stejné čp. v jiné místní části (Horka × Bakov), stejnojmenná část jiné obce, čp. „268-II“ = městská část Mladá Boleslav II. Alternativa bez klíče: RÚIAN (CSV adresních míst ČÚZK, souřadnice v S-JTSK). Historická čísla popisná se mohla přečíslovat nebo dům zanikl – u čp. z 19. století uveď v poznámce, že shoda s dnešním domem je předpoklad; pokud adresu nelze ztotožnit, dej souřadnice části obce/ulice/obce a do poznámky napiš, co přesně souřadnice označují. Souřadnice obcí pro vyšší úrovně hierarchie.
- Stejné místo zakládej jen jednou a odkazuj na něj (žádné duplikáty textových míst).

## Média (skeny zápisů a dokladů)
- `.gramps` obrázky neobsahuje, jen na ně odkazuje. Používej **relativní cesty** vůči základní cestě k médiím nastavené v Gramps (Předvolby), kterou uživatel nasměruje na složku se skeny.
- **Pojmenování souborů:** `<datum>_<typ>_<příjmení>_<zdroj>.jpg`, jen ASCII bez diakritiky a mezer, např.
  - `1872-01-30_O_Malinovsky-Kozelova_SOAPraha-Radosovice13-s050.jpg`
  - `1881-09-12_N_Malinovsky-Karel_SOATrebon-Milevsko16-s057.jpg`
  - `1953-05-13_N_Malinovsky-Karel_MatrikaMB-N5-str214.jpg`
  - `1974-12-18_RL_Davidek-Robert_rodinny-archiv.jpg`
  - Typ: `N` narození, `O` oddaní, `Z` zemřelí, `RL` rodný list, `DV` doslovný výpis, `OSV` osvojení (dodatečný zápis), `VUA` vojenský archiv, `DOK` jiný dokument. Datum = datum události; u sňatku obě příjmení.
  - **Jeden soubor = jedna událost.** Je-li na stejné dvoustraně další zápis, vytvoř **kopii** pojmenovanou podle té události (celá dvoustrana, žádný výřez). Kopie mají stejnou koncovku zdroje, takže při řazení leží vedle sebe.
  - **Jednou vytvořený název se nikdy nemění** – Gramps odkazuje cestou a přejmenování by rozbilo odkazy. Nový nález = nová kopie.
  - **Originály nikdy neupravuj** (ořez, otočení, kontrast); výřezy dělej v Gramps jako region.
  - Totožné kopie se poznají podle **kontrolního součtu** (např. `sha256sum`, PowerShell `Get-FileHash`). Použij ho ke zjištění, zda už sken máš (před stažením/kopírováním), k seskupení kopií téhož snímku a ke kontrole, že se originál nezměnil.
  - Metadata do EXIF nepiš; autoritou pro to, kdo je na snímku, je Gramps.
- Médium připoj **k citaci**; volitelně i **k osobě s výřezem** (region) jejího zápisu.
- Archivy povolují kopie zpravidla jen pro soukromé studium – strom s obrázky nezveřejňuj (např. veřejný Gramps Web). Pro zálohu nebo přenos i s obrázky lze vytvořit **Gramps XML Package (`.gpkg`)**.

## Kmotři, svědci a další osoby ze zápisu
- **Nezakládej je jako osoby** (výjimka: prokázaný příbuzný). Zapiš je do **poznámky události** ve strukturovaném tvaru, aby se daly později strojově vytěžit:
  `Kmotři: Jméno Příjmení, stav/povolání, obec čp.; … | Svědci: … | Porodní bába: … | Oddávající/křtící: … | Ohlášky: data, farnosti`
