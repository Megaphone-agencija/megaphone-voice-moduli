# Pravila: kdaj pognati skripto in kam kažejo mehanizmi agenta

**Pravila (FILTER, mehanizmi, kakovost, preverjanje, »Ne izumljaj tople vode«, pregled pred gradnjo) NISO v tem skillu.** Ena tema ima eno mesto in to je Obsidian (`Agent-Shared/PRAVILA.md`, `Agent-Shared/glasovni-agenti-nacela.md`). Skripta jih ob vsakem zagonu prebere v živo, zato se ne razhajajo.

```bash
python3 ~/.claude/skills/gradnja-agentov/scripts/pravila.py                    # splošni FILTER, Codexove najdbe, tople vode z moduli, šest mehanizmov, kakovost, preverjanje
python3 ~/.claude/skills/gradnja-agentov/scripts/pravila.py --projekt vecer    # + Večerov vratar 0–6 in M1–M8
python3 ~/.claude/skills/gradnja-agentov/scripts/pravila.py --pregled          # + »Pregled pred gradnjo« (graf, prompti, potek klica, uveljavljene rešitve)
```

`--projekt` sprejme tudi `jana`, `joze`, `fine-dining`, `prebil`; ti dobijo splošni izpis (pravila za svoj agent glej spodaj). Če skripta pade (izhodna koda 2), se je struktura Obsidianovih datotek spremenila: preberi obe datoteki ročno in popravi skripto (izluščanje je prepis iz `~/.claude/hooks/pravila-vrata.py`).

## Kdaj poženeš

| Trenutek | Ukaz | Kaj narediš z izpisom |
|---|---|---|
| Faza 02 (arhitektura), preden Chebo potrdi razdelitev nosilcev | `--pregled` (in `--projekt vecer` za Večer) | Naredi seznam vrzeli PRED gradnjo (točke pregleda). |
| Vsak popravek obstoječega agenta (napaka iz klica, Codexova najdba) | privzeto | Pojdi skozi FILTER po vrsti; na prvem »ne« se ustaviš. |
| Pišeš nalogo za podagenta ali Codex | `--projekt <agent>` | Izpis prilepi v razdelek 4 naloge (`predloga-naloge.md`). Izvajalec hooka ne vidi. |
| Faza 04, ko razvrščaš padec testa ali klica | privzeto | Najprej razvrsti (test / odločitev / prava napaka), šele nato popravljaj. |

## Merilo posameznega agenta: kam kažejo mehanizmi

| Agent | Mehanizmi in FILTER | Opomba |
|---|---|---|
| Jana, Jože | FILTER 1–3 + šest mehanizmov (Obsidian, `glasovni-agenti-nacela.md` razdelek 2) | Jože ima v repozitoriju `docs/PRAVILA.md` kot kopijo; vir je Obsidian. |
| Fine dining | Isto kot Jana (splošno) | `docs/pravila/PRAVILA-FILTER.md` in `docs/pravila/mehanizmi-M1-M8.md` sta kopiji; druga je Večerov seznam M1–M8, ki za druge agente po Chebovi odločitvi 19. 10. NE velja. Lastni mehanizmi Fine dining v repozitoriju niso zapisani (odprto). |
| Prebil | FILTER + šest mehanizmov; kapitalne napake po CL `P-KV-01` (`docs/checklist-prebil.md`) | `AGENTS.md` povzema FILTER; M1–M8 so v CL uporabljeni kot merilo, ne kopirani. Ali Prebil dobi lasten seznam mehanizmov, ni odločeno (odprto). |
| Večer | Vratar 0–6 + M1–M8 (`--projekt vecer`); repozitorij `docs/vecer-mehanizmi.md` | CL `docs/checklist-mediji.md`; kanon klicev in testi po mehanizmih. |
| Nov agent | FILTER + šest mehanizmov; lastne mehanizme zgradi iz lastnih dokazov šele po prvih klicih (Večer 19. 10.: »ne moreš samo kopi pejst«) | Mehanizme ne kopiraj iz drugega agenta. |

Kapitalne napake (merilo, Obsidian, razdelek »Kakovost«): misli/navodila na glas, popravljanje same sebe med govorom, neprebran povzetek, napačni podatki, lažna potrditev, dvojna oddaja, obvisel klic. Ciljne vrednosti (≤ 1/100 klicev kapitalnih, 0 napačnih podatkov) so sprejete za Jano, Jožeta in Večer; za nov agent jih potrdi Chebo.

## Kje so pravila zdaj (po skrajšanju hooka, 12. 11. 2026)

Hook ob vsakem promptu (`~/.claude/hooks/pravila-vrata.py`, 523 znakov) izpiše samo: VRATA, napotilo na ta skill, kratko vrstico o podagentih (model, effort, poročilo), kratko vrstico o slogu in, samo če poslušalec ne teče, opozorilo o Slack poslušalcu. Vse ostalo je tu ali na dogodku, ob katerem je potrebno.

| Pravilo (nekdaj v hooku) | Kje je zdaj |
|---|---|
| VRATA: raziskava, skica, Chebova potrditev, implementacija, test; ne začenjaj brez izrecnega naročila | hook ob promptu; zapore faz v `SKILL.md` in `faze.md` |
| Najprej preveri, kaj že obstaja; uveljavljena metoda | `moduli.md`, `pravila.py` (tople vode), `faze.md` faza 02 (za glasovne agente); Obsidian `PRAVILA.md` |
| FILTER, šest mehanizmov, kakovost, preverjanje, »Ne izumljaj tople vode« | `scripts/pravila.py` (v živo iz Obsidiana) |
| Večerov vratar 0–6 in M1–M8 | `scripts/pravila.py --projekt vecer` |
| PREGLED pred gradnjo (prej ob `#filter`) | `scripts/pravila.py --pregled`, `faze.md` faza 02 |
| Podagenti: model (koda, diagnoza, razmišljanje → sonnet + effort high; brez razmišljanja → sonnet low ali haiku), effort vedno izrecno, poročilo v datoteko in nazaj največ 15 vrstic | kratka vrstica v hooku ob promptu (da jo orkestrator pozna pred zagonom) + `podagent-pravila.py` (PreToolUse, Agent; opomnik ob rezultatu klica, dopolnilo za naslednji zagon); naloga: `predloga-naloge.md` |
| Podagentu prepiši merilo svojega agenta (`pravila.py --projekt <agent>`), stanje projekta, modul in datoteko za prepis | `podagent-pravila.py` in `predloga-naloge.md` razdelek 4 |
| Implementacija Sonnetu, Opus je QA | `/home/chebo/CLAUDE.md` razdelek »Orchestration«; `predloga-naloge.md` |
| Slack: poslušalec za kanal svojega projekta, potrditev v niti, branje niti, objava samo kot bot prek `slack-post.py` | vbrizg stanja projekta (`stanje.py`, razdelek »Slack (<projekt>)«); `faze.md` faza 04 |
| Opozorilo »Slack poslušalec ne teče« | ostane v hooku ob promptu (preverja procese) |
| Ključi (`~/.bashrc`, `bash -ic`, nikoli ne izpisuj) | `/home/chebo/CLAUDE.md` razdelek »API ključi« |
| Slog (izid najprej, bulleti, ELI5, kratko) | kratka vrstica v hooku ob promptu; `/home/chebo/CLAUDE.md` »How to explain things to Chebo« |
| Ponovno nalaganje tega skilla po stiskanju konteksta | vrstica ob dogodku po stiskanju (SessionStart, source compact; `startup-context.py`) |

Razhajanji, ki ju nisem razrešil: (1) stari hook je za poročila podagentov, ki morajo preživeti izklop, zahteval kopijo na `~/Desktop`; Obsidian `PRAVILA.md` (5. 11. 2026, novejše) pravi, da agenti Namizja ne smetijo. Velja novejše (poročilo v repo `docs/porocila/` ali scratchpad); podagent-pravila.py kopije na Namizje ne omenja. (2) Besedilo »Moduli« v Obsidianu našteva Jano, Jožeta, Fine dining in Večer, Prebila ne; `moduli.md` ga ima.
