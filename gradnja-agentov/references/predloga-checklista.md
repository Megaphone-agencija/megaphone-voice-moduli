# Predloga poslovnega checklista (CL) za nov agent

Kopiraj `cl-skeleton.md` (razdelek 3) v projekt agenta (`docs/checklist-<agent>.md`), izvirnik pusti prazen. CL piše orkestrator iz virov (Chebove odločitve, klici, spletna stran naročnika); Chebo ga potrdi (faza 01).

Preverjalnik: `python3 scripts/preveri_cl.py docs/checklist-<agent>.md` (osnutek: dodaj `--dovoli-odprto`). Neizpolnjena predloga PADE (označevalci `<…>`), kar je namen.

## 1. Kaj je ostalo iz obstoječe predloge in kaj se je spremenilo

Obstoječa predloga: `/home/chebo/MAIOS/02-knowledge/Megaphone/Voice AI agenti/Predloga poslovnega checklista rezervacijskega agenta.md` (2. 10. 2026, različica 1). Ni v celoti aktualna po Prebilu:

| Del stare predloge | Stanje | Kaj narediti |
|---|---|---|
| Rubrike A–I (obseg, podatki rezervacije, ponudba, termini, slot filling in readback, popravki, povzetek in oddaja, vmesne informacije, API) | Aktualne kot **seznam vprašanj** za rezervacijske agente. Ne ustrezajo vsakemu agentu (Prebil in Večer ju nista uporabila). | Preberi jo kot kontrolni seznam vprašanj za Cheba. Rubriko, ki ne velja, zapiši z `ne velja` in razlogom. Njenih vrstic ne kopiraj. |
| Oznake `A01`, `B05`… | Opuščene. Prebil in Večer uporabljata `P-ZA-01`, `M-ID-03`. | Uporabi `PREDPONA-SKLOP-ŠT` (razdelek 2). |
| Status `velja / ne velja + razlog / še ne vemo` | Nadomeščen s `potrjeno / iz virov / ODPRTO / ne velja` (razdelek 2). | Uporabi novega. |
| Pravila: ne prenašaj vrednosti druge restavracije; vir in dokaz nista status; za vsako rubriko mora biti status | Ostanejo v veljavi. | Upoštevaj. |
| Razdelek J (sledljivost proti obstoječemu agentu) in kontrola popolnosti | Nadomešča ju stolpec `Test` in preverjalnik. | Ne uporabljaj. |
| **Manjka** (dodano): stolpci `Nosilec`, `Merilo uspeha`, `Test / scenarij`; razdelek besedil z ID-ji; zapora »CL zaprt« | Novo, ker brez teh Codex ne dobi dovolj določene naloge (Prebil, 9.–10. 11.). | Spodaj. |

## 2. Format (to preverja `preveri_cl.py`)

**ID** = `PREDPONA-SKLOP-ŠT`: predpona agenta (1–3 črke: `P` Prebil, `M` Večer), sklop (2 črki), dvomestna številka. Primer `P-ZA-04`. ID se nikoli ne spremeni in ne ponovi; črtana zahteva ostane s statusom `ne velja`. Test, naloga in poročilo se sklicujejo samo na ID.

**Stolpci tabele zahtev** (imena morajo biti taka, vrstni red je prost):

| Stolpec | Vsebina | Preverjalnik pade, če |
|---|---|---|
| `ID` | identifikator | manjka, ni v obliki, podvojen v datoteki |
| `Zahteva` (ali »Pričakovano vedenje«) | kaj mora veljati + konkreten primer gosta in agenta | je prazna |
| `Nosilec` | **en** glavni: `Koda`, `LLM`, `Glasovni sloj` ali `Vsebina`; podpora v oklepaju: `Koda (podpora: LLM)` | manjka, ni eden od štirih, več glavnih |
| `Merilo uspeha` | merljivo: število, dobeseden stavek, »0 oddaj v 20 ponovitvah« | je prazno, `?`, `TODO`, `<…>`, krajše od 10 znakov |
| `Test / scenarij` | pot do testa (`tests/…::test_ime`) ali ID scenarija ali »živi klic« z opisom | je prazno, `?`, `TODO`, `<…>` |
| `Status` | `potrjeno` (Chebova odločitev + datum), `iz virov` (Chebo naj potrdi), `ODPRTO`, `ne velja – razlog` | `ODPRTO` (CL ni zaprt), `ne velja` brez razloga |
| `Vir` | kdo/kaj/kdaj | (ni preverjeno; vseeno obvezen po dogovoru) |

Nosilci (kaj pomenijo; odločitveno pravilo je v `faze.md`, faza 02): **Koda** = jedro (stanje, validacija, povzetek, zapora, oddaja, števci); **LLM** = razumevanje pomena, zajem, razjasnitev, naravni govor; **Glasovni sloj** = ASR, TTS, prekinitve, oznake predvajanja, tišina, telefonija; **Vsebina** = potrjena dejstva, besedila, nastavitve, meni, urnik, napotitve.

**Status ODPRTO** je dovoljen samo v osnutku. Ko Chebo CL potrdi, ostane 0 vrstic `ODPRTO`; kar čaka zunanjega (npr. dogovor s stranko), dobi ID v razdelku »Zunanje odvisnosti« in status `ne velja – čaka <kdo>` ali se odloči, da je zahteva izven obsega.

**V fazi 04** dodaj sklic v teste: komentar `# CL: P-ZA-04` ob testu (zgled: Večer, `tests/test_obrat.py`). Nato `preveri_cl.py CL.md --testi tests/` pade za vsak ID brez omembe. Za scenarije (posnet model, zaklenjena tabela pričakovanj) je ID zahteve v polju `vir` ali komentarju vrstice.

## 3. Skeleton

Datoteka `cl-skeleton.md` v tej mapi: `cp` v `docs/checklist-<agent>.md` in izpolni. Razdelki `Obseg` … `Zunanje odvisnosti` so predlog sklopov (po Prebilu in Večeru); sklop, ki ga agent nima, zapiši z eno vrstico `ne velja – razlog`. Sklop, ki ga agent ima, a ga tu ni, dodaj.

## 4. Kako piši dobro vrstico

- **Zahteva** = vedenje, ki ga gost sliši ali ki ga vidi zapis, s primerom. »Agent odda enkrat« ni zahteva brez primera: »gost reče ‚ja‘ po slišanem povzetku → natanko ena oddaja«.
- **Merilo** loči zahtevo od želje: besedilo dobesedno enako, število oddaj, število ponovitev, število zavrnjenih potrditev. Merila za agenta (kapitalne napake ≤ 1/100 klicev, napačni podatki 0) so v `pravila.py`; za svoj agent jih izrecno potrdi pri Chebu, ne podeduj (Prebil: »za Prebil niso posebej potrjeni«).
- **Test / scenarij**: v fazi 01 je lahko opis scenarija (»gost reče X, agent mora Y«); do konca faze 04 postane pot do testa.
- Poslovno pravilo, ki ga CL ne pokriva, ni odločitev agenta: dopolni CL (povratna zanka v `faze.md`).
- Ne mešaj zahteve in stare ugotovitve testa (HTML shema procesa: »Zahtevano vedenje ločimo od zgodovinske ugotovitve testa«). Napaka iz klica gre v tabelo znanih napak, ne v zahtevo.
