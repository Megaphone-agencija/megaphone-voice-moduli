---
name: gradnja-agentov
description: Obvezen postopek za glasovne agente (Jana, Jože, Fine dining, Prebil, Večer in novi) na lastni arhitekturi. Uporabi ga vedno, ko začenjaš delati novega glasovnega agenta, delaš večji popravek ali novo funkcijo obstoječega, popravljaš napako iz klica ali Codexovo najdbo, ali pišeš nalogo za podagenta ali Codex. Prisili checklist (CL) z ID-ji, nosilci in merili, zemljevid modulov za prepis in nalogo iz CL.
---

# Gradnja glasovnih agentov

Cilj: ponovljiv postopek, v katerem nov agent ali večji popravek ne začne z ohlapno nalogo. **Brez CL ni dela; naloga za izvajalca nastane iz CL, ne iz proze.** (Prebil: ohlapna naloga Codexu je zahtevala veliko popravkov; ko je nastal CL, je delo steklo v nekaj dneh.) ElevenLabsa ni več; vsi agenti tečejo na lastni arhitekturi (Pipecat, Asterisk, Soniox, jedro v kodi).

Shema (Chebo, 7. 10. 2026): **01 Zahteve → 02 Arhitektura → 03 Povezave → 04 Izvedba**, s povratno zanko. Vsaka zahteva ima ID, ki ga nosijo arhitektura, pogodba, naloga, test in poročilo. Pot (nov agent ali popravek) in podrobnosti vsake faze: `references/faze.md`.

Skripte poganjaj z `python3 ~/.claude/skills/gradnja-agentov/scripts/<ime>.py`.

## Korak 0: ugotovi pot

- **Nov agent ali nova funkcija** → faze 01–04.
- **Napaka iz klica, Codexova najdba, popravek** → najprej FILTER: `scripts/pravila.py` (Večer: `--projekt vecer`). Na prvem »ne« se ustaviš (zapiši, ne popravljaj). Če prestane: poišči ID v CL; če ga ni, je to novo poslovno pravilo → dopolni CL (faza 01) in Chebo potrdi; šele nato nadaljuj od faze 02 za ta ID.
- Ne začni brez izrecnega naročila (»naredi«, »pojdi«). Pogovor, skica in strinjanje niso naročilo.

## Faza 01: Zahteve (CL)

Naredi: CL po `references/predloga-checklista.md` (skeleton `references/cl-skeleton.md`): zahteve z ID, pričakovanim vedenjem s primerom, nosilcem, merilom, testom/scenarijem, statusom in virom; dobesedna besedila z ID; konflikti; znane napake; odprta vprašanja.
**Zapora:** `scripts/preveri_cl.py CL.md` vrne 0 (med pisanjem `--dovoli-odprto`) IN Chebo potrdi CL. Brez tega ne v fazo 02.

## Faza 02: Arhitektura

Prebereš: `references/moduli.md` (kdo je kaj že naredil), `scripts/pravila.py --pregled`.
Naredi: (1) vsaka zahteva dobi **enega glavnega nosilca**: Koda / LLM / Glasovni sloj / Vsebina (odločitvena tabela v `faze.md`); (2) merilo uspeha in test ali scenarij; (3) za vsako funkcijo vir za prepis iz `moduli.md` (datoteka @ commit), »novo« samo z utemeljitvijo; (4) pregled pred gradnjo: seznam vrzeli; (5) skica.
**Zapora:** vsak ID ima nosilca in merilo; Chebo potrdi razdelitev nosilcev in skico.

## Faza 03: Povezave

Naredi: pogodbo po `references/predloga-pogodb.md`: podatkovna shema (eno dejstvo, en lastnik), pogodbe orodij (vhod, izhod, status), pogodba oddaje, pogoji prehodov, sledljivost ID → polje/orodje → test.
**Zapora:** razdelek 7 pogodbe izpolnjen; Chebo potrdi.

## Faza 04: Izvedba

1. **Naloga** iz CL po `references/predloga-naloge.md`: zahteve po ID, modul in datoteka za prepis, kaj prilagoditi, česa ne pisati na novo, merilo agenta (izpis `pravila.py --projekt <agent>`), zeleni testi, oblika poročila (celo v datoteko, nazaj ≤ 15 vrstic), jezik commitov (preprosta slovenščina); pri popravku napake obvezno razdelek 5a (druge oblike). Ti si orkestrator: za to odgovarjaš ti.
2. **Implementacija** na ločeni veji. Prepise iz commita vpiši v `IZVOR.json`.
3. **Revizija in testi:** sam poženi teste in preberi diff, poročilu ne verjemi. Med delom lokalno brez pravega modela (brez OpenRouterja), na primerih iz Chebovih klicev, vsak test čez vsaj dve vozlišči; pravi model samo enkrat, ko je cel popravek gotov (tik pred »kliči«): Chebov klicani scenarij 3×. Podagent pravega modela in celotnega nabora ne poganja. Cel pogovor skozi cevovod; vsak ID ima test z `# CL: ID`; `scripts/preveri_cl.py CL.md --testi tests/` vrne 0. Skrite oblike in `scripts/pripravljeno.py` (ZRELO pred predajo Chebu): `references/predloga-naloge.md`.
4. **Objavljena različica:** veja, SHA, ukaz in rezultat testov, kaj je preizkušeno z lažnimi ponudniki in kaj z živim klicem, odprte omejitve.
**Zapora:** nič na produkcijo, merge v main, push, namestitev ali preusmeritev številke brez Chebovega neposrednega »namesti«.

## Pravila popravkov (FILTER pred vsakim popravkom)

Prompt IN koda. Vprašanja po vrsti: je res (pravi klic ali ponovljiv padec, ne testni izmislek)? je prav razumljeno (besedilo ali sobesedilo; agent ali test)? najnižja plast (ena pravilna izvedba → koda; sicer izboljšaj obstoječe načelo; novo pravilo je zadnja možnost)? Natančno besedilo, mehanizme, kakovost in merilo agenta dobiš z `scripts/pravila.py`; pravil tu ne prepisujemo (ena tema, eno mesto: Obsidian). Kam kažejo mehanizmi vsakega agenta: `references/pravila.md`.

Povratna zanka: napaka → odgovorni blok (nosilec iz CL) + regresijski scenarij; novo poslovno pravilo → dopolnitev CL (nov ID). Podrobno v `references/faze.md`.

## Trdna pravila

- **Najprej poišči, potem piši** (»Ne izumljaj tople vode«). Novo samo, kjer ustreznika ni, in to izrecno označi. `scripts/preveri_moduli.py` preveri, da zemljevid še kaže na obstoječe datoteke.
- **Prompt:** pred vsako spremembo preberi CEL prompt (osnova + zadevna vozlišča; ne grep, ne odlomek) in preveri protislovja z vsemi vrsticami; zahtevo ponovi v vsaki nalogi, ki se prompta dotika. Meja osnova + vozlišče: 5–6k znakov, največ ~10k.
- **Ključi** samo preveri, ali so nastavljeni; nikoli jih ne izpiši. Datotek ne ustvarjaj na Namizju.

## Datoteke

| Datoteka | Kdaj |
|---|---|
| `references/faze.md` | podrobnosti faz, zapore, povratna zanka, koordinacija (Slack, ključi) |
| `references/predloga-checklista.md`, `cl-skeleton.md` | faza 01 |
| `references/moduli.md` | faza 02 in vsaka naloga: funkcija × agent, pot do kode, vir za prepis |
| `references/predloga-pogodb.md` | faza 03 |
| `references/predloga-naloge.md` | faza 04: naloga za podagenta in Codex |
| `references/pravila.md` | kdaj pognati `pravila.py`, kam kažejo mehanizmi agenta |
| `scripts/pravila.py`, `preveri_cl.py`, `preveri_moduli.py` | pravila v živo; preverjalnik CL; preverjalnik poti v zemljevidu |
| `scripts/vzporedni_testi.py <koren> <python> -j 10 -o padci.txt` | cela zbirka po modulih na več jedrih (Chebo 13. 11. 2026). Večer: ~8 min namesto ~12; zaporedni zagon je imel 124 padcev zaradi medsebojnega vpliva testov, po modulih jih skoraj ni. Padec ponovi z modulom samim, da ločiš časovno nestabilnost od regresije. |
| `scripts/pripravljeno.py <repo> [--veja] [--osnova main] [--python] [--pythonpath] [--cl] [--porocilo] [--skrite] [--model]` | ena preverba, ali je veja zrela za Cheba: testi, CL, dokaz pred/po (`Reprodukcija:`), poročilo (Oblike, Ne pokrije), skrite oblike, 3× pravi model in Codex vezana na SHA (`/home/chebo/MAIOS/00-system/pripravljeno/<repo>/`). Izhod 0 = ZRELO. |
| `scripts/primeri/` | dober in pokvarjen CL, primer testov s sklici na ID |
