# Skica: kako priti do »ista koda, drugi podatki« (Jože in Jure)

- **Merilo za konec** (Chebo): `diff -r` kode (vsi `*.py` razen `tests/`) med Jožetom in Juretom = 0, in zbirki testov obeh agentov sta zeleni. Danes: Jure proti Jožetovemu `abcfdc4` 21 obstoječih datotek (+1584 / −1111) in 5 novih (+456); izmerjeno v `00-system/napake/porocila/f1-6-trismerno-2026-11-24.md`.
- **Stanje**: skica, nič ni narejeno. Testov nisem zagnal (v okolju ni `pytest`). Datoteke `skupno/` v Kratochwillu in vsebina `nastavitve/btc/restavracija.yaml` (razen ključev) **niso prebrane**; predlogi za ključe so iz kode.
- **Številke vrstic**: Jože `abcfdc4`; za Jurejeve vrstice pišem »(Jure)« (`468eafb`, `prevzem/`).
- **Preverjeno za predloge**: nalagalnik kataloga `KatalogNarocila` **ne zavrača neznanih ključev** (poskus na kopiji `katalog-joze.yaml`: dodana `skupine[0].vloga` in `izdelki[0].tehtano`, nalaganje je uspelo). Torej so nova polja v katalogu varna za dodati; zavrača pa jih lahko `preveri_nastavitev` za `restavracija.yaml` (to polje je treba posebej pregledati).

## Najprej: korak 0, vlitje (ni podatek, je pogoj)

Dokler Jure in Jože nimata iste kode, `diff -r` ne more biti 0. Korak 0: vliti Jožetovih 851 vrstic v Jurejevo drevo (22 konfliktov v 5 datotekah, od tega 15 v `flows.py`; glej poročilo, razdelek 2) in dobljeno kodo kopirati v obe drevesi. Po koraku 0 je `diff -r` = 0, a koda še vsebuje veje po imenu agenta (`JURE`, `PREVZEM_BTC`). Vsi naslednji koraki jih zamenjajo s podatki **in po vsakem ostane `diff -r` = 0 in obe zbirki zeleni**. Če kateri korak ne gre skozi obe zbirki, se ne nadaljuje.

## Vrstni red (blokira nalaganje, nato aktivno povsod, nato spi)

| Korak | Tema | Zakaj tu |
|---|---|---|
| 1 | T1, samo nalaganje | **Blokira**: `prevzem_govor.py:368` `_OBVEZNI_KLJUCI` vsebuje `pecenost` in `teza`; restavracija brez teh blokov sploh ne naloži nastavitve. Jure drži 25 ključev ostanka (`govor.pecenost`) samo zato |
| 2 | T6 | Aktivno povsod in Jure je moral spreminjati kodo; `GOVOR_AGENT` privzeto `joze` (Jože) in `jure` (Jure) je že razlika v kodi (`profil.py:~285`) |
| 3 | T8 | Stikala v profilu (Python) so jedro razlike; brez tega T4 in T7 ne moreta biti podatek |
| 4 | T4, T3 | Besedila in izgovor: Jure ju je moral spreminjati v kodi |
| 5 | T7, T9 | Prompti, zahteve na katalog |
| 6 | T1 (ostalo), T2, T5, T10 | Spijo, če katalog nima teh imen; zadnje |

## Deset tem: predlog

Za vsako: **kje v podatkih** (kateri ključ), **kaj ostane v kodi**. Ključi, ki jih Jure že ima, so označeni z (že).

### T1. Pečenost, teža, tehtane jedi (korak 1 za nalaganje, ostalo korak 6)

- **Ključ**: v katalogu `skupine[].vloga: pecenost` (za Jožetove steake) in `izdelki[].tehtano: {enota, korak, privzeto_g}`; v `restavracija.yaml` bloka `govor.pecenost` in `govor.teza` postaneta **neobvezna**: obvezna samo, če katalog skupino z `vloga: pecenost` ali izdelek s `tehtano` ima. Jurejev btc yaml izgubi 25 ključev ostanka.
- **V kodi ostane**: logika izbire z lestvico in tehtanja (ista za vse), a bere `vloga` in `tehtano`, ne imen `'pečenost'` in enot `'100 g'`, `'g'`, `'1 g'`.
- **Mesta**: `narocilo_joze.py:181,208,1159-1160`; `joze_spremembe.py:539,569,675`; `joze_listek.py:48`; `joze_izgovor.py:209`; `klic.py:323`; `prevzem_govor.py:368,481,501`; `flows.py:3408,3441,3641,3981,6743`.
- **Preveriti**: ali `preveri_nastavitev` zavrača neznane ključe v katalogu ali yaml (v katalogu ne).

### T2. Imena izdelkov in besed v kodi (korak 6; plus Jurejeve vezi)

- **Ključ**: katalog `enake_besede`, `splosne_besede`, `zamenljivo` (par z namigi), `skupine[].naroci_skupno: true`, `skupine[].izraz`; za »K pici ali posebej?« novo besedilo `besedila.k_jedi_ali_posebej` s `{vrsta_jedi}` (že imamo `govor.sklic.vrsta_jedi` po skupini).
- **V kodi ostane**: algoritem ujemanja; samo slovnična polnila (z, s, iz, do).
- **Jurejeve vezi, ki jih je treba odstraniti**: `narocilo_joze.py:476-477` (Jure) skupina `'pizze'` in besedilo »K pici/jedi ali posebej?«; `menu_spotter.py:198` (Jure) seznam `pizzo/pici/pice/pizze`. Oboje v katalog (`skupine[].ime_v_vprasanju`) ali `govor.sklic.vrsta_jedi`.
- **Mesta pri Jožetu**: `katalog_narocila.py:611,695,709,717`; `narocilo_joze.py:610`; `menu_spotter.py:29,34,155`; `narocanje_sproti.py:195,199`; `flows.py:6451`; `ujemanje_jedilnika.py:37,61,90`; `joze_dobesedno.py:15`.

### T3. Izgovor za TTS (korak 4)

- **Ključ**: `restavracija.yaml` → `izgovor: <pot do datoteke>` (shema `izgovor-1`, Jure jo že ima kot `skupno/izgovor-kratochwill.yaml`); za Jožeta ista shema z ~120 imeni, kraticami in »Džæk-end-Džou«; `PECENOST_IZGOVOR` (Rêr …) gre v isto datoteko.
- **V kodi ostane**: `tts_priprava.pravila_iz_datoteke(pot)` = Jurejev `pravila_btc` (`tts_priprava.py:136-160` (Jure)), preimenovan; brez vej `IMENA_PRAVILA if JOZE`, `PECENOST_IZGOVOR if JOZE and not JURE`, `pravila_btc() if JURE` (`app.py:223,225` (Jure)); `joze_izgovor.py:178` kratice iz iste datoteke.
- **Mesta pri Jožetu**: `tts_priprava.py:35,47`; `app.py:210,217`; `joze_izgovor.py:178`.

### T4. Besedila, ki jih gost sliši, a so v kodi (korak 4)

- **Ključ**: `govor.*`, `besedila.*`, `listek.predloga` (že); iz `profil.py` (Jure) gre v yaml: `PREVZEM_BTC.privzeta_besedila` (11 stavkov), `vprasanja_razlicice`, `popravek_razlicice`, `branje_telefona_razlicice`, `zavrnitev_privzeto`, `napaka_backenda_privzeto` → `govor.*`; trije regexi `odgovor_na_povzetek`, `lazna_potrditev`, `gostovo_slovo` → `govor.vzorci.*` kot **seznam fraz** (regex sestavi koda); `NAVODILO_ZAKLJUCEVANJE_BTC` (`zakljucek.py:69,273` (Jure)) → `besedila.navodilo_zakljucevanje`; `govor.btc: da` (`prevzem_govor.py:406-456` (Jure)) → ločena stikala: `govor.ena_razlicica_vprasanja`, `govor.brez_cen` (že).
- **V kodi ostane**: sestavljanje stavkov, `preveri_nastavitev`, ki zahteva ključe (rezerve v kodi odpadejo).
- **Mesta pri Jožetu**: `prevzem.py:130-164,194`; `listek_backend.py:181,266,277-309`; `summary.py:11,13`; `klic.py:91`; `flows.py:168,2157,2569`; `zakljucek.py:60,65`; `profil.py:161-222`. Za Jurejeve že obstoječe ključe: `besedila.povzetek_predloga`, `besedila.povzetek_vprasanje_konec` (že).

### T5. Številke in pragovi (korak 6)

- **Ključ**: yaml `ujemanje.{prag_besede, prag_razlike, min_dolzina, prag_priblizne_omembe}`, `govor.meje.*`, `moduli.narocilo.veliko_narocilo_kosov`, `pravila.tisina`, `pravila.najdaljsi_klic_s`, `pravila.poskusi_na_podatek` (zadnja dva obstajata, a ju koda ne bere).
- **V kodi ostane**: privzete vrednosti kot rezerva ni dovoljena; ključi so obvezni. Po zamenjavi kataloga: `scripts/meritev_ujemanja.py` (mejna vrednost za prag).
- **Mesta**: `ujemanje_jedilnika.py:28`; `katalog_narocila.py:276`; `narocilo_joze.py:127`; `flows.py:165,167,3932,5612`; `zakljucek.py:53`; `listek_backend.py:237,412`; `prevzem_govor.py:434,776,786`.

### T6. Poti, glas, vrata, mape, imena okolja (korak 2)

- **Ključ**: nov blok v `restavracija.yaml`: `proces: {pozdrav: pot, prompti: predpona, glas (že), vrata, mapa_klicev, neoddano: {vrsta: jsonl|mapa, okolje: IME}, skupno: pot, oddaja: {vrsta: sheet|eposta}, okolje_predpona: ...}`. `GOVOR_AGENT` samo izbere **mapo nastavitve** (npr. `nastavitve/` ali `nastavitve/btc/`); profil se zgradi iz nje (T8).
- **V kodi ostane**: nalagalnik bere `proces.*`; imena spremenljivk okolja (`KRATOCHWILL_*`, `JURE_*`, `JOZE_*`) pridejo iz yaml ali iz enega niza predpone.
- **Veje po imenu, ki odpadejo (Jure)**: `app.py:83,88,144,156,223,225,966,1040,1041,1253,1260` (10 mest razen definicije); `klic_jj.py:34,66-72,150`; `zakljucek.py:273`; privzeta vrednost `or "jure"` proti Jožetovemu `or "joze"` (`profil.py:285` (Jure)): privzeto naj bo prazno = napaka, ime pride iz zagona.
- **Mesta pri Jožetu**: `app.py:59,87,143-145,154,1227`; `klic_jj.py:26,27,85,97`; `neoddano.py:25`; `listek_eposta.py:28`; `predaja.py:37`.
- **Uvozi iz `skupno/`**: `klic_jj.py:28-30` (Jure), `vhodi/nastavitev.py:6,33,36-42` (Jure), `tts_priprava.py:141` (Jure): pot do `skupno/` naj bo `proces.skupno`; uvoz `razpolozljivost` samo ob `moduli.prevzem.cas_cakanja` (zdaj že tako); **ostane pogoj, da Jožetovo drevo teče brez `skupno/`** (preverjeno ni; test: zagon Jožetovih testov brez mape).

### T7. Prompti vsebujejo J&J (korak 5)

- **Ključ**: `proces.prompti` (predpona/imena datotek); v promptu mesta `{ime_za_gosta}`, `{agent_ime}`, `{spletna_stran}`, `{primeri}` iz yaml/kataloga; meja znakov (`test_prompti_joze.py:30,187`) kot nastavitev.
- **V kodi ostane**: sestavljanje `osnova + vozlišče` (`app.py:144-147`), nič po imenu agenta (`_predpona = "jure" if JURE else "joze"` odpade).
- **Mesta**: `prompti/prompt_joze_osnova.txt:2,13,14,16,17,18`; `prompti/pozdrav_joze.txt:1`; Jure ima ločene datoteke `prompt_jure_*` (že podatek).

### T8. Koraki, vozlišča, stikala v profilu (korak 3)

- **Ključ**: nov blok `profil:` v `restavracija.yaml`: 8 stikal (`cas_cakanja`, `povzetek_brez_vprasanja`, `po_oddaji_vprasanje`, `se_kaj_po_vsakem`, `kolicina_skupaj`, `prevezava_nazaj`, `povratni_klic`, `orodja_ura_gosta`), `vozlisca`, `orodja_vozlisca`, `orodja_ostala`; `PREVZEM_BTC` in `PREVZEM_JJ` (`profil.py:194-222` pri Jožetu, `232-277` (Jure)) odpadeta kot konstanti, `iz_yaml()` jih zgradi.
- **V kodi ostane**: razred `ProfilPrevzem` (struktura) in polja; uporaba stikal v `flows.py` (isto kot danes). Koraki kot urejen seznam (`JOZE_KLJUCI_KORAKOV`, `flows.py:5611`) so druga faza.
- **Merilo**: iz `profil.py` odide ~60 vrstic (Jure) in v `app.py`/`klic_jj.py` nobenega `iz_okolja() is PREVZEM_BTC`.

### T9. Zahteve na katalog (korak 5)

- **Ključ**: `moduli.narocilo.neznana_embalaza_narocljiva` (že), `izdelki[].volumen_l`, `izdelki[].gramatura: {od, do}`, `vrste` v katalogu (privzeto štiri), embalaža opcijska.
- **V kodi ostane**: razčlenjevanje besedila imena kot rezerva za katalog brez teh polj.
- **Mesta**: `katalog_narocila.py:15,39,94,670,683`; `narocilo_joze.py:312`.

### T10. Poimenovanje in protokol (korak 6, mehanično)

- **Ključ**: `moduli.narocilo.protokol: narocilo-v1` (Jure ima ostanek `joze-3-razvoj`, `jedro/nastavitev.py:145` zavrne vse drugo).
- **V kodi ostane**: preimenovanje `joze_*`/`jozef_*` ni vedenje; naj ga opravi ločen mehanični commit po tem, ko je `diff -r` = 0.

## Kar prejšnja skica ni imela (Jurejeve vezi, ki jih je treba pospraviti)

| Vez | Mesto (Jure) | Kam |
|---|---|---|
| Besedila in regexi `PREVZEM_BTC` | `profil.py:232-277` | T4, T8 |
| `NAVODILO_ZAKLJUCEVANJE_BTC` | `zakljucek.py:69,273` | T4 |
| `govor.btc` kot ime agenta v validaciji | `prevzem_govor.py:406,411,440,451-456` | T4 |
| `skupno/` poti in uvoz `URNIK` | `klic_jj.py:28-30`, `vhodi/nastavitev.py:6,33,36-42`, `tts_priprava.py:141` | T6, T3 |
| Vrata, mapa klicev, `JURE_*`, `KRATOCHWILL_*`, privzeti `GOVOR_AGENT` | `app.py:59,156,1253,1260`; `klic_jj.py:35,133`; `neoddano_jsonl.py:12`; `prevezava_nazaj.py:12-14`; `profil.py:285` | T6 |
| Skupina `'pizze'` in besedilo »K pici« | `narocilo_joze.py:476-477`, `menu_spotter.py:198` | T2 |

## Kaj ni zajeto

- Koliko dni dela je to: ni ocenjeno (ni merjeno).
- Ali bi obe zbirki ostali zeleni po koraku 0: ni preverjeno.
- Pečenost/teža v Jožetu in Jurejev `jedilnik_btc.Ponudba` imata različna modela podatkov (katalog); morebiten prekrivajoč ključ v katalogu nisem preveril.
