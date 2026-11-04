# czech-genealogy

Skill pro [Claude](https://claude.ai), který pomáhá s **genealogickým výzkumem v českých a slovenských matrikách a archivech** a s údržbou rodokmenu v programu [Gramps](https://gramps-project.org).

*A Claude skill for Czech and Slovak genealogy research: civil and parish registers, regional archives, request templates, reading old records and maintaining a family tree in Gramps. The skill itself is written in Czech.*

## Co skill umí

- **Matriky:** pravidla zákona č. 301/2000 Sb. (lhůty 100/75/30 let, § 25 pro potomky, doslovný výpis, omezení u osvojení) a šablona žádosti na matriční úřad.
- **Archivy:** kde hledat a jak fungují prohlížeče – SOA Praha (eBadatelna), SOA Třeboň (DigiArchiv), Litoměřice, Zámrsk, Plzeň (Porta fontium), Opava, Brno (Actapublica), SOkA, slovenské matriky na FamilySearch.
- **Vojenské prameny:** Databáze legionářů VÚA–VHA, legionářské osobní spisy, žádost přes PDF formulář, co znamenají kódy na kartách.
- **Čtení zápisů:** poznámky na okraji (sňatky, přestupy mezi církvemi, legitimace), nemanželské děti, dobové názvy míst a povolání, typické chyby v přepisech.
- **Strojový přístup k archivům:** nástroje bez prohlížeče a bez přihlášení pro SOA Praha (eBadatelna), SOA Třeboň, SOA Plzeň (Porta fontium), SOA Zámrsk (ARON), AHMP, snímky z Litoměřic a Opavy, pražské policejní přihlášky a noviny – převzato z [sarsonj/rodokmen-skill](https://github.com/sarsonj/rodokmen-skill) (MIT).
- **Orchestrace agentů:** hlavní agent (silnější model, Opus) plánuje a kontroluje, čtecí subagenti (levnější model, Sonnet) procházejí digitalizované matriky nástroji (záložně v Chromu) a stahují originály. Hlavní agent každý zápis znovu přečte a ověří, než ho zapíše do rodokmenu.
- **Souřadnice domů:** skript pro Mapy.com API dohledá souřadnice podle čísla popisného a ohlídá záměnu s čísly orientačními a místními částmi (API klíč zdarma na [developer.mapy.com](https://developer.mapy.com/account/projects)).
- **Gramps:** doplňování nových údajů do exportu ve formátu Gramps XML (`.gramps`) s citacemi zdrojů, validace proti DTD, rodné a vdané jméno, osvojení, nemanželské děti.

Skill dodržuje otevřený formát [Agent Skills](https://agentskills.io) (`SKILL.md` s frontmatter, podrobnosti v `references/`, skripty v `scripts/`), takže ho lze použít i v jiných nástrojích než Claude.

## Instalace

### Jiné nástroje (Codex CLI, Gemini CLI…)
Zkopírujte (nebo nalinkujte) složku `skills/czech-genealogy` do složky skillů svého nástroje, např. `~/.codex/skills/czech-genealogy` nebo `~/.gemini/skills/czech-genealogy`, případně podle dokumentace nástroje. Pro čtecí subagenty dejte subagentovi jako instrukce soubor `references/archive-reader.md`.

### Claude (claude.ai, desktop)
1. Stáhněte složku [`skills/czech-genealogy`](skills/czech-genealogy) (nebo celý repozitář jako ZIP).
2. Zabalte složku `czech-genealogy` do ZIPu.
3. V nastavení Claude v sekci se skilly nahrajte ZIP jako nový skill.

### Claude Code
Zkopírujte skill a čtecího agenta (stejný příkaz slouží i k aktualizaci – starou verzi skillu nejdřív smaže):

```bash
tmp=$(mktemp -d) && git -C "$tmp" clone https://github.com/midlan/skill-czech-genealogy.git \
  && src=$(echo "$tmp"/*) \
  && rm -rf ~/.claude/skills/czech-genealogy \
  && mkdir -p ~/.claude/skills && cp -r "$src/skills/czech-genealogy" ~/.claude/skills/ \
  && mkdir -p ~/.claude/agents && cp "$src/agents/archive-reader.md" ~/.claude/agents/ \
  && rm -rf "$tmp"
```

Repozitář se naklonuje do prázdné dočasné složky, takže příkaz funguje bez ohledu na to, jak git pojmenovává klonované složky. Po zkopírování se dočasná složka smaže.

Nástroje pro archivy potřebují Python 3 a [ImageMagick](https://imagemagick.org) (Windows: `winget install ImageMagick.ImageMagick`). Chrome (`claude --chrome` nebo příkaz `/chrome`) je potřeba jen pro portály bez nástroje (MZA Brno, vyhledání knihy v Litoměřicích a Opavě, FamilySearch); přihlašujete se vždy sami. Jako hlavní model zvolte Opus (`/model`). Čtecí subagenti běží na modelu Sonnet. Paralelně doporučujeme nejvýš 2–3 subagenty, každý ve vlastní záložce; při potížích přepněte na sekvenční běh.

## Použití

Stačí začít mluvit o rodokmenu, matrikách nebo předcích, např.:

- „Pomoz mi sestavit rodokmen z otcovy strany, děda se jmenoval…“
- „Napiš žádost na matriku o doslovný výpis zápisu narození mé babičky.“
- „Přečti tenhle zápis z matriky a doplň ho do mého rodokmenu v Gramps.“ (přiložte obrázek a export `.gramps`)
- „Dej mi prompt pro Claude Code, ať v eBadatelně najde sňatek mých prapraprarodičů.“

## Struktura

```
skills/
└── czech-genealogy/
    ├── SKILL.md                    # hlavní instrukce (načítají se celé)
    ├── references/                 # podrobnosti, načítají se podle potřeby
    │   ├── matriky-a-archivy.md    # právo, žádosti, přehled archivů, VÚA
    │   ├── nastroje-archivy.md     # nástroje pro archivy bez prohlížeče
    │   ├── farnosti.md             # ověřená přiřazení obcí k farnostem a knihám
    │   ├── cteni-zapisu.md         # čtení zápisů, typické chyby
    │   ├── orchestrace.md          # hlavní agent + čtecí subagenti, šablona zadání
    │   ├── archive-reader.md       # instrukce pro čtecího agenta
    │   └── gramps.md               # údržba rodokmenu v Gramps
    └── scripts/
        ├── souradnice_mapy.py  # souřadnice domů podle čp. přes Mapy.com API
        └── archivy/            # nástroje pro archivy bez prohlížeče (z sarsonj/rodokmen-skill, MIT)
agents/
└── archive-reader.md     # definice subagenta pro Claude Code (Sonnet), instrukce čte z references/archive-reader.md
```

## Upozornění

Skill obsahuje praktické postupy, nikoli právní radu. Ceníky, provoz badatelen a podmínky archivů se mohou měnit – ověřujte je na webech příslušných institucí. Kopie archiválií slouží obvykle jen ke studijním účelům; řiďte se podmínkami jednotlivých archivů.

## Licence

[MIT](LICENSE) © 2026 Milan Davídek. Nástroje ve složce `skills/czech-genealogy/scripts/archivy/` jsou také pod MIT, © Jindřich Šaršon (viz níže).

## Poděkování

Nástroje ve složce `skills/czech-genealogy/scripts/archivy/` pocházejí z projektu [rodokmen-skill](https://github.com/sarsonj/rodokmen-skill) Jindřicha Šaršona (licence MIT, text v `scripts/archivy/LICENSE-rodokmen-skill`). Opravy nástrojů prosím hlaste přednostně tam.
