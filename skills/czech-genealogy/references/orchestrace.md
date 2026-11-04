# Orchestrace: hlavní agent + čtecí subagenti

Kdy číst: když deleguješ hledání v archivech na subagenty nebo připravuješ prompt pro jiného agenta.

Cíl: uživatel nemusí ručně přenášet zadání a výsledky mezi modely.

**Role**
- **Hlavní agent = silnější model (Opus).** Plánuje úlohy, píše zadání subagentům, **kontroluje veškerou jejich práci**, čte rukopis, rozhoduje o totožnosti osob, komunikuje s uživatelem a jako jediný zapisuje do rodokmenu.
- **Čtecí subagent = levnější model (Sonnet).** Prochází archivy nástroji ze `scripts/archivy/` (záložně v Chromu), listuje knihami, stahuje originály a dělá *předběžný* přepis. Do rodokmenu nikdy nezapisuje, nic neobjednává ani neodesílá, nezadává hesla.

**Spuštění**
- Předpoklad: Claude Code se shellem a Pythonem 3 (a ImageMagickem). Chrome (`claude --chrome` nebo `/chrome`) je potřeba jen pro portály bez nástroje; přihlašuje se vždy uživatel sám.
- Subagenta spouštěj nástrojem Agent s `model: "sonnet"`, nejlépe jako předdefinovaného agenta `archive-reader` (Claude Code: `~/.claude/agents/archive-reader.md`, viz README repozitáře). V jiných nástrojích dej subagentovi jako instrukce soubor [archive-reader.md](archive-reader.md).
- Čtecí agent potřebuje shell (nástroje ze `scripts/archivy/`, ořez a zvětšení obrázků) a čtení obrázků – v zadání to výslovně povol a uveď absolutní cestu ke složce `scripts/archivy/`.
- Výstupy si určí hlavní agent: subagent ukládá obrázky do pracovní složky (např. `rodokmen/nalezy/`) pod přesnými názvy ze zadání, přepis průběžně zapisuje do pracovního souboru a vrací strukturovaný report.

**Paralelní běh**
- Paralelně spouštěj nejvýš **2–3 subagenty**, každého s jiným archivem nebo jinou knihou – i s nástroji kvůli zátěži serverů a limitům archivů (Litoměřice, Opava).
- V prohlížeči pracuje každý subagent **ve vlastní nové záložce** a sahá jen na svou záložku. Všichni sdílejí jedno rozšíření a jeden prohlížeč; souběh není zaručeně stabilní. Pokud se objeví chyby, zasekávání nebo se agenti přetahují o záložky, **přepni na sekvenční běh**.
- Úlohy, které na sobě závisí (např. sňatek rodičů až po nalezení narození), dávej jednomu subagentovi postupně.

**Kontrola práce subagenta (povinná, vždy)**
1. Otevři každý stažený obrázek a přečti zápis sám; přepis subagenta ber jen jako vodítko.
2. Zkontroluj citaci (kniha, snímek, strana, URL) a že obrázek odpovídá citaci.
3. Ověř logiku: data, věk, čísla domů, shoda s už doloženými údaji, poznámky na okraji potvrzující totožnost.
4. Projdi, co subagent **neprošel**. **Negativní nález platí jen pro přečtený rozsah:** „nenalezeno v indexu“ nebo „jen horní zápisy“ neznamená „v knize není“ – zadej doplňující čtení celých stránek nebo jiné místo (jiná farnost, kniha ženichovy obce, matrika).
5. Uživateli shrň nálezy a výslovně uveď, co jsi oproti subagentovi opravil.
6. Teprve potom zapiš do rodokmenu.

## Šablona zadání pro čtecího agenta
```
Piš ČESKY. PRAVIDLA: archivy procházej nástroji z <cesta>/scripts/archivy/
(prohlížeč jen když nástroj pro portál není nebo selže); jen čti, nezadávej
hesla, nic neobjednávej; stahuj jen snímky, které čteš (na orientaci náhled);
zaseknutou záložku nahraď novou; každý nález ulož jako ORIGINÁLNÍ obrázek
celé dvoustrany pod uvedeným názvem; nejisté údaje označ [nejisté]
s variantami; odlišuj přepis od výkladu; čti CELÉ stránky, ne jen horní
zápis; u nálezu zkontroluj stranu před a po a v indexu vypiš všechny
zápisy se stejným příjmením; po 2–3 neúspěšných pokusech úlohu popiš
a jdi dál. Smíš používat shell (nástroje, ořez obrázků) a čtení obrázků.
PŘIHLÁŠENÍ: <v kterých archivech je uživatel přihlášený (např. Třeboň)>
UKLÁDÁNÍ: <složka, podsložka pro vedlejší soubory, pracovní soubor s přepisy>
CO VÍME: <kontext osob, data, místa, čp., varianty příjmení,
  jména rodičů pro ověření totožnosti (aspoň 2 shodné údaje)>
UŽ PROVĚŘENO: <kniha, rozsah, výsledek – neopakovat>
ÚLOHY: <očíslované: archiv, farnost/kniha (ID, pokud je známé), známý posun
  folio↔snímek, přesné datum nebo rozsah let, rozsah k přečtení celý,
  limit snímků, název souboru>
VÝSTUP: u každé úlohy rozsah přečtených snímků a způsob čtení (celé
stránky / index), ID knihy, posun folio↔snímek; úplný přepis (dítě/
snoubenci, rodiče, prarodiče, povolání, bydliště, původ, kmotři/svědci,
poznámky „Cop.“, přestupy, úmrtí) s pozicí na stránce; rozpory se
zadáním; citace (archiv, signatura, snímek, strana, URL); u negativního
výsledku návrh dalšího místa; souhrnná tabulka; seznam vedlejších souborů.
```
