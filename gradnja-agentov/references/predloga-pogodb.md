# Predloga pogodb (faza 03: povezave)

Pogodba pove, **kaj točno gre med bloki**: iz CL (kaj), nosilcev (kdo) in modulov (`moduli.md`) naredi vhode, izhode in stanje. Kopiraj v `docs/pogodba-<agent>.md`, izpolni, Chebo potrdi. Ne piši nove pogodbe tam, kjer jo agent že ima iz kopiranega modula: pokaži na obstoječo (`J:docs/pogodba-modul.md`, v. 2) in zapiši samo razlike.

Vzor: Janina pogodba `/home/chebo/MAIOS/09-projects/POC glasovni agent/megaphone-voice-poc/docs/pogodba-modul.md` (jedro ↔ govor, oblike podatkov, rezultat orodja, podpis modula), tipi v `jedro/modul.py` (skoraj enaki v Jani, Jožetu, Fine dining in Prebilu; razlike 0 do 11 vrstic) in Prebilov modul `PR:jedro/moduli/povprasevanje.py` kot zgled majhnega modula.

## 1. Podatkovna shema

Eno dejstvo, en lastnik (modul). Imena polj so imena v backendu; slovenska so imena orodij in besedila.

| Polje | Lastnik (modul) | Tip in kanonična oblika | Obvezno | Meje | Kje se normalizira | CL ID |
|---|---|---|---|---|---|---|
| `<ime>` | `<modul>` | `<npr. E.164, YYYY-MM-DD, HH:MM, niz ≤ 100>` | `<da/ne/pogojno>` | `<…>` | `<koda / model>` | `<ID>` |

Normalizacija e-pošte in telefona je vedno v kodi. Model pošilja vrednosti v kanonični obliki, koda jih preveri. Kar iz klica pride samo (caller ID), model ne sprašuje.

## 2. Pogodba orodja (po eno za vsako orodje, ki ga vidi model)

- **Ime in opis** (opis ≤ 200 znakov): `<…>`; orodje ima 1 do 3 polja, vsa neobvezna.
- **Vhod**: `<polja z oblikami iz razdelka 1>`; sprejme katerokoli podmnožico svojih polj, kadarkoli.
- **Izhod** je vedno `{"status", "razlog_za_model", "manjka"}`; dodatni ključi samo z utemeljitvijo.

| `status` | Kdaj | Kaj naredi model |
|---|---|---|
| `ok` | vse sprejeto | nadaljuje |
| `manjka` | sprejeto, a ni dovolj podatkov | vpraša za naslednji manjkajoči podatek |
| `oblika` | napaka modela (tip, oblika) | tiho pokliče znova (meja ponovitev iz števca) |
| `neveljavno` | oblika prava, vrednost ne sprejeta | gostu kratko pove razlog |
| `nedovoljeno` | dejanje zdaj ni dovoljeno (npr. oddaja brez slišanega povzetka) | ravna po razlogu |
| `napaka_backenda` | backend ne odgovori | stalni stavek iz nastavitve |

- **Kdo kliče, kdaj**: `<vozlišče / obrat>`; ali sme v istem obratu skupaj z drugimi orodji (celoten sveženj orodij enega obrata se registrira, preden se katero izvede).
- **Napake in ponovitve**: kateri števec, kakšna meja, kateri varen izhod (en števec, en izhod).
- **CL ID, ki jih orodje izvaja**: `<ID, ID>`.

## 3. Pogodba oddaje (backend)

Vmesnik `Backend` (`jedro/modul.py`): `snapshot`, `restore`, `state`, `pripravi`, `potrdi_predstavitev`, `oddaj`.

| Vprašanje | Odgovor za ta agent |
|---|---|
| Kam gre oddaja (HTTP, SMTP, lokalni ponor) in kdo je transport (`oddaja/…`) | `<…>` |
| Oblika zahtevka in obvezna polja | `<…>` |
| Kaj pomeni uspeh (sprejem na strežniku ni dokaz dostave) | `<…>` |
| Idempotenca: kakšen ključ, kaj ob ponovitvi | `<…>` |
| Neznan izid (timeout, preklic): terminalen, brez samodejne ponovitve? kaj izreče agent | `<…>` |
| Opozorilo ekipi ob neuspehu (brez osebnih podatkov) in zasebni zapis neoddanega | `<…>` |
| Spremembe in odpovedi po oddaji | `<agent napoti na … / API omogoča …>` |

## 4. Stanje in pogoji prehodov

| Operacija | Potrebni dokazi | Kdo uveljavi | Kaj ob nepopolnem pogoju | CL ID |
|---|---|---|---|---|
| Povzetek | vsa obvezna polja zbrana | koda | vpraša za manjkajoče | `<…>` |
| Dovoljenje za oddajo | povzetek **slišan do konca** (ne prekinjen) + jasen »ja« po tem povzetku | koda | ponovi povzetek ali razjasni | `<…>` |
| Popravek | razveljavi prejšnji povzetek in dovoljenje | koda | nov povzetek | `<…>` |
| Oddaja | revizija = revizija slišanega povzetka | koda | `nedovoljeno` | `<…>` |

Za vsako tehnično zmožnost označi: **dokazano** (kje) / **domneva** / **odprto**. Parametri, ki jih ustvari model, sami niso dokaz dogodka (npr. `guest_confirmed=true` ni potrditev gosta).

## 5. Nastavitev podjetja in besedila

- Kaj je podatek (`nastavitve/…yaml`: prejemniki, urnik, številke, meniji) in kaj koda; v kodi ni imen, cen, naslovov podjetja.
- Besedila, ki jih izgovori koda (ID iz CL, razdelek besedil): `<datoteka>`, kdo jih potrdi (Chebo), test, da so enaka CL.
- Zagon zavrne manjkajočo ali neizpolnjeno konfiguracijo (ne tiha privzeta vrednost).

## 6. Sledljivost

| CL ID | Polje / orodje / pogoj | Datoteka (kjer bo izvedeno) | Test |
|---|---|---|---|
| `<ID>` | `<…>` | `<pot>` | `<pot::ime>` |

Vsak CL ID z nosilcem **Koda** ali **LLM** mora imeti vrstico tukaj; ID z nosilcem **Vsebina** gre v razdelek 5; **Glasovni sloj** v `moduli.md` (govorni sloj) in v nalogo.

## 7. Preverjanje pogodbe (zapora faze 03)

- [ ] Nobeno polje nima dveh lastnikov; nobenega podatka ni na dveh mestih z drugačno obliko.
- [ ] Vsak CL ID z nosilcem Koda ali LLM je v razdelku 6.
- [ ] Za vsak razdelek 4 je jasno, kdo uveljavi pogoj (koda, ne prompt).
- [ ] Chebo je potrdil pogodbo.
