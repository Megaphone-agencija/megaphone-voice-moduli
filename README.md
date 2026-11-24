# megaphone-voice-moduli

Skupna zaloga za gradnjo glasovnih agentov (Jana, Jože, Fine dining, Prebil, Večer, Kratochwill in novi).

## Kaj je notri

- `gradnja-agentov/` — skill za gradnjo agentov: checklist, popisi modulov (`moduli/`), predloge nalog in skripte, ki preverjajo, ali je delo pripravljeno.
- `napake/` — seznam družin napak (`druzine.json`, `druzine.md`), hooki za commite (`git-hooks/`), štetje napak (`stej.py`, `test_stej.py`) in poročila.

## Kje je glavna kopija

Glavna kopija je LOKALNO v MAIOS: `/home/chebo/MAIOS/04-workflows/megaphone-voice-moduli/`. Vse deluje tudi brez GitHuba. GitHub je samo varnostna kopija in skupna točka.

Stare poti ostajajo veljavne (simbolne povezave):

- `/home/chebo/MAIOS/04-workflows/Skills/gradnja-agentov` kaže sem
- `/home/chebo/MAIOS/00-system/napake` kaže sem
- `~/.claude/skills/gradnja-agentov` kaže na staro pot, ta pa sem
- `core.hooksPath` v repozitorijih agentov kaže na `00-system/napake/git-hooks`

## Kje so pravila

Pravila (FILTER, mehanizmi) so samo v Obsidianu (`Agent-Shared/PRAVILA.md`). Tukaj jih ni kopiranih, da ne nastaneta dve različici.

## Izvajalne datoteke

`stanje-stetja.json`, `opozorila.log` in podobno nastajajo ob zagonu, zato so v `.gitignore` in jih ne pošiljamo na GitHub.
