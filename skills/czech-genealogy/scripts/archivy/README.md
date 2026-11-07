# Nástroje pro archivy bez prohlížeče

Převzato z projektu [sarsonj/rodokmen-skill](https://github.com/sarsonj/rodokmen-skill) (Jindřich Šaršon, licence MIT – viz `LICENSE-rodokmen-skill`), verze z commitu `a9bbdad` (říjen 2026).

Jediná úprava oproti originálu: v `ebadatelna.py`, `trebon.py`, `portafontium.py` a `aron_img.py` je `ROOT` (kam se ukládají `data/svazky.json` a mezipaměť `pracovni/.cache_*`) místo složky nástroje **aktuální pracovní adresář** (případně proměnná `RODOKMEN_ROOT`), aby nástroje nezapisovaly do složky skillu.

**`ebadatelna.py` nepoužívat:** od listopadu 2026 eBadatelna SOA Praha v robots.txt zakazuje roboty (cesty `/d/` a `/a/`) a nástroji vrací 403; upstream ho vypnul (sarsonj/rodokmen-skill#72). eBadatelna se čte jen v prohlížeči – postup v `references/nastroje-archivy.md`.

Návod k použití je v `SKILL.md` (sekce Strojový přístup k archivům) a v hlavičce každého nástroje (`python <nástroj> bez parametrů`).

Aktualizace z upstreamu: zkopíruj nové verze souborů z `skills/rodokmen/tools/` a znovu proveď úpravu `ROOT` (řádek s komentářem `czech-genealogy`).
