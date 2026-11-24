# Prevzem hrane: kaj bi bilo treba za novo restavracijo spremeniti (podatki ali koda)

- **Namen**: za agenta za prevzem hrane (Jože) preveriti trditev »za novo restavracijo samo zamenjaš podatke«. Vir: šest popisov v tej mapi (`joze-*.md`) in primerjava Jureta proti Jožetu.
- **Jože**: `abcfdc4` (veja `joze-sproti`), čist izvoz commita; številke vrstic veljajo za ta commit. **Jure**: `prevzem/` v repozitoriju Kratochwill, veja `jure-zapornica`, commit `468eafb`, drevo čisto (`git status` brez sprememb). Datum: 2026-11-24. Nič ni bilo zagnano; vse je branje kode, diff in grep.
- **Kako brati oznake**: *podatek (OK)* = vrednost je v yaml, katalogu ali tekstovni datoteki restavracije: zamenjaš datoteko, kode ne diraš. *koda (problem)* = vrednost ali pravilo je v `.py`: za novo restavracijo je treba urediti kodo.

## 1. Povzetek (odgovor na vprašanje)

**Jedro še ni »samo podatki«.** Jure je dokaz: nastal je iz Jožeta z dodanimi 1214 vrsticami in 130 odstranjenimi v 18 obstoječih datotekah, plus 5 novimi moduli (456 vrstic: `cas_cakanja`, `jedilnik_btc`, `oddaja_btc`, `neoddano_jsonl`, `prevezava_nazaj`). V kodi je 8 stikal, ki jih je moral dodati v profil, in 13 mest, kjer koda sprašuje »ali sem Jure« (`JURE`, `jure()`, `PREVZEM_BTC`).

Večino dodanega ni »J&J proti Kratochwillu«, ampak **nove zmožnosti, ki jih Kratochwill potrebuje** (čas čakanja, povratni klic, ponudba iz jedilnika). To je v redu, če so vklopljene s podatkom. Slabše so tri druge stvari: (a) stikala so v Pythonu (`profil.py`), ne v yaml; (b) besedila, regexi in imena datotek so po agentu zapisani v kodi; (c) J&J-pojmi (pečenost, tehtane jedi, domača kola) so v jedru vezani na imena: vedenje spi, če katalog teh imen nima, a blok `govor.pecenost` ostane obvezen za nalaganje, zato ga Jure drži kot prazen ostanek.

| Kaj | Število | Vir |
|---|---|---|
| Vrstic »vezano na J&J v kodi« v popisih | 132 (BESEDILO 36, PRAVILO 28, IME-JEDI 27, ŠTEVILO 20, IME-AGENTA 10, NASLOV 6, REGEX 5) | `VEZ-*` v `joze-*.md`; štetje s skripto iz tabel |
| Od tega samo poimenovanje (IME-AGENTA, ne vpliva na vedenje) | 10 | isto |
| Isti problem opisan v več popisih | veliko (npr. pečenost v 5 popisih, »Koakola« v 4); zato so spodaj združeni v 10 tem | razdelek 2 |
| Mesta, kjer koda pri Juretu sprašuje, kdo je agent | 13 (`app.py` 10, `klic_jj.py` 2, `zakljucek.py` 1) | `grep` po `prevzem/` |
| Stikala v profilu Jureta (Python) | 8 | razdelek 3 |
| Stikala Jureta v yaml (podatek, dobro) | 11 | razdelek 3 |

**Nepreverjeno**: koliko dni bi bila zamenjava na novi restavraciji z današnjo kodo (nisem je poskusil). Spodnje ocene truda (majhno/srednje/veliko) so moja presoja iz velikosti sprememb, ne meritev.

## 2. Kaj zamenjati pri novi restavraciji

### 2.1 Podatki (OK): to se zamenja z datotekami

| Kaj | Pot (Jože) | Opomba |
|---|---|---|
| Jedilnik (izdelki, skupine, različice, dodatki, sopomenke, izgovor, `vkljuceno`, embalaža) | `nastavitve/katalog-joze.yaml` | živi katalog; `katalog.yaml` je staro. Shema polj: `joze-nastavitve.md` |
| Besedila, ki jih izgovori koda (`govor.*`, `besedila.*`) | `nastavitve/restavracija.yaml` | večina stavkov je že tu; preverja jih `prevzem_govor.preveri_nastavitev` |
| Urnik, korak prevzema, čas priprave, rok naročanja | `nastavitve/restavracija.yaml` `moduli.prevzem` | pri Juretu tudi `cas_cakanja` |
| Ime za gosta, govorec, glas (Jure) | `restavracija.yaml`: `ime_za_gosta`, `ime_v_besedilih`, `govorec`, `glas` | glas je pri Juretu že podatek; pri Jožetu je v kodi (VEZ-NAS-10) |
| Prejemnik listka, kopija, opozorilo | `restavracija.yaml` `listek.*` | |
| Stikala vedenja jedra | `restavracija.yaml` `moduli.narocilo.*` (`brez_cen`, `alergija_zastavica`, `ponudi_dodatke`, `ze_vkljuceno_samo_ista`, `neznana_embalaza_narocljiva`) | to je pravi vzorec; dodani so jih Jure |
| Pozdrav, prompt | `nastavitve/pozdrav.txt`, `prompti/*.txt` | **past**: yaml ključa `pozdrav` in `prompt` kažeta na datoteki, ki ju koda ne bere; živa sta `prompti/pozdrav_joze.txt` in `prompti/prompt_joze_*.txt` (VEZ-NAS-09). Zamenjati je treba oboje |

### 2.2 Koda (problem): 10 tem, ki jih je treba spraviti v podatke

Vsaka tema združuje več `VEZ-*` vrstic. Polna tabela vseh 132 je v dodatku (razdelek 5).

| # | Tema | Stanje pri drugi restavraciji | Kje v kodi (glavna mesta) | Zakaj je problem | Predlog: kako v podatke | Trud (moja ocena) |
|---|---|---|---|---|---|---|
| T1 | **Pečenost, teža, tehtane jedi so v jedru zapisane kot imena**: skupina se imenuje `'pečenost'`, tehtana jed ima enoto `'100 g'`/`'g'`/`'1 g'`, privzeto 300 g, 27 ključev bloka `govor.pecenost` je obvezen | **Nalaganje: blokira** (blok `pecenost` je obvezen). Vedenje: spi, če katalog nima skupine »pečenost« (Jure kode ni spreminjal, obdržal je prazen ostanek) | `jedro/moduli/narocilo_joze.py:181,208,220,757,1159`; `joze_spremembe.py:539,569,675`; `joze_listek.py:48`; `joze_izgovor.py:209`; `jedro/klic.py:323`; `govor/prevzem_govor.py:368,481,501`; `govor/flows.py:3408,3441,3641,3981,4486,6743` (VEZ-NAR-01..07, PRE-09..13, GOV-08..13, NAS-15,18, ODD-09) | Restavracija brez steakov sploh ne naloži nastavitve (blok `pecenost` obvezen). Jure ga je moral obdržati kot zavajajoč ostanek (25 ključev, »Kako naj vam ga spečemo?«), čeprav BTC pečenosti nima | V katalog polje skupine `vloga: pecenost` (ali `tip: lestvica`) in polje izdelka `tehtano: {enota, korak, privzeto}`; koda bere vlogo, ne imena; blok `govor.pecenost` obvezen samo, če katalog skupino z vlogo ima | veliko (11 mest v 5 datotekah + flows) |
| T2 | **Imena izdelkov in besed v kodi** (domača kola »Koakola«, smash burger, »pica/burger« kot odvečna beseda, `stejk`→`steak`, splošne besede steak/burger/solata, skupine koktajli/spritz) | **Spi**, če katalog nima teh imen (npr. `_koakola_ali_cola` ob prvi vrstici preveri, da katalog ima `koakola` in `kokakola`, in vrne `None`; Jure kode ni spreminjal). Splošne besede in sopomenke delujejo vedno, a prilegajo se samo, kjer imena sovpadajo | `katalog_narocila.py:611,695,709,717`; `narocilo_joze.py:610`; `govor/menu_spotter.py:29,34,155`; `govor/narocanje_sproti.py:195,199`; `govor/flows.py:6451`; `ujemanje_jedilnika.py:37,61,90`; `joze_dobesedno.py:15` (VEZ-NAR-09,13..16,19, UJE-01,02,05,07..10, GOV-05..07, NAS-17,19,20) | Nova restavracija s kolo, drugimi skupinami ali drugimi splošnimi besedami dobi J&J obnašanje (npr. vprašanje »Ste mislili našo domačo Koakolo ali Coca-Colo?«) ali pa ujemanje odpove | V katalog: `enake_besede`, `nepomembne_besede` (že obstaja delno), `splosne_besede` po skupini, `zamenljivo` (par z namigi in razlago), `skupine.*.naroci_skupno`; v kodi samo slovnična polnila | srednje |
| T3 | **Izgovor za TTS**: ~120 imen jedi, ime lokala »Džæk-end-Džou«, pečenost »Rêr«, kratice ZDA | **Aktivno** za vsako restavracijo na Jožetovem profilu (`IMENA_PRAVILA if JOZE`); Jure je moral dodati `if JURE` | `govor/tts_priprava.py:35,47`; `govor/app.py:210,217`; `joze_izgovor.py:178` (VEZ-GOV-01..04, NAS-11,12,21, NAR-18) | Jure je to rešil s skupno datoteko `skupno/izgovor-kratochwill.yaml` in funkcijo `pravila_btc`, a izbor vseeno poteka z `if JURE` v `app.py:223-225` | Ena datoteka `izgovor.yaml` na restavracijo (shema `izgovor-1` je pri Juretu že; vzeti jo) in kodi samo `pravila_iz_datoteke`; izbira s potjo iz nastavitve, ne z imenom agenta | majhno (Jure je predlogo že naredil) |
| T4 | **Besedila, ki jih gost sliši, a so v kodi** | **Aktivno**; Jure je moral prepisati v `profil.py` (11 stavkov v `privzeta_besedila` in 3 regexi) in `zakljucek.py` | `jedro/moduli/prevzem.py:130-164,194`; `jedro/listek_backend.py:181,266,277-309`; `jedro/summary.py:11,13`; `jedro/klic.py:91`; `govor/flows.py:168,2157,2569`; `govor/zakljucek.py:65`; `govor/profil.py:161-222` (VEZ-PRE-01..05,17,21, ODD-01..04,08,11..14, GOV-14,15,18..23) | Gost slišal stavek, ki ga ni mogoče zamenjati brez kode; rezerve v kodi so podvojene z yaml in tiho zakrijejo manjkajoč ključ | Vsi stavki v `govor.*`/`besedila.*`/`listek.predloga`; rezerve v kodi odstraniti, `preveri_nastavitev` naj zahteva ključe; profil naj ima samo strukturo | srednje (veliko majhnih mest) |
| T5 | **Številke in pragovi** (prag ujemanja 0,80/0,15/5; »veliko naročilo« 10 kosov; največ vprašanj 3; čas tišine 8 s, klic 390/470 s; rok opozorila 15 s; največ 3 popravke) | Aktivno za vsak katalog; ali so pragovi na drugem katalogu pravi, ni preverjeno (Jure kode ni spreminjal) | `ujemanje_jedilnika.py:28`; `katalog_narocila.py:276`; `narocilo_joze.py:127`; `govor/flows.py:5612,3932,165,167`; `govor/zakljucek.py:53`; `listek_backend.py:237,412`; `prevzem_govor.py:434,776,786` (VEZ-UJE-03,06, PRE-06,07,14, ODD-06,07, GOV-24,25, NAS-13,22) | Pragovi ujemanja so izmerjeni na J&J katalogu (235 izdelkov); na drugem katalogu so lahko napačni. `pravila.tisina` in `najdaljsi_klic_s` v yaml obstajata, a ju koda ne bere | yaml `ujemanje.*`, `govor.meje.*`, `pravila.*`; po zamenjavi kataloga zagnati `scripts/meritev_ujemanja.py` | majhno do srednje |
| T6 | **Poti, glas, vrata, mape, imena okolja, časovni pas** | **Aktivno**; Jure je moral spremeniti `app.py` in `klic_jj.py` (13 mest `if JURE`/`jure()`) | `govor/app.py:59,87,143-145,154,1227`; `govor/klic_jj.py:26,27,85,97`; `oddaja/neoddano.py:25`; `oddaja/listek_eposta.py:28`; `govor/predaja.py:37` (VEZ-NAS-09,10, ODD-15..18, GOV-26,27,30) | Za vsako novo restavracijo je treba urediti `app.py` in `klic_jj.py`; Jure je to storil s kopijo vej `if JURE ...` | Ena nastavitev procesa: pot do mape restavracije (parameter zagona), iz nje glas, vrata, mapo klicev, mapo neoddanih, SMTP, časovni pas, imena pozdrava in promptov | srednje |
| T7 | **Prompti vsebujejo J&J**: ime restavracije, `jackandjoe.si`, »več kot dvajset burgerjev«, primeri (Cheese, Fanta, The Boss, Bud Spencer), pravila (dostave ni, plačilo ob prevzemu); osnova + vozlišče 7087 od 7100 znakov | **Aktivno**; Jure je napisal 6 novih datotek promptov in pozdrava | `prompti/prompt_joze_osnova.txt:2,13,14,16,17,18`; `prompti/pozdrav_joze.txt:1`; `tests/govor/test_prompti_joze.py:30,187` (VEZ-NAS-01..08) | Prompt se po CL piše na novo za vsakega agenta (zemljevid modulov); zahteva testa po nizu »Jack & Joe Lenart« je J&J | Predloga prompta z mesti `{ime_za_gosta}`, `{agent_ime}`, `{spletna_stran}`, primeri iz kataloga; meja znakov kot nastavitev | srednje (vsebina, ne koda) |
| T8 | **Vrstni red korakov in graf vozlišč** (ura, ime, priimek, telefon, povzetek) je fiksen v kodi; vozlišča in orodja po vozliščih so v Python profilu | **Aktivno**; Jure je moral dodati 8 stikal v profil | `govor/flows.py:5611-5760` (`JOZE_KLJUCI_KORAKOV`, `jozef_korak_kljuc`); `govor/profil.py:194-222` (VEZ-GOV-17,18) | Jure korak ure izpusti s stikaloma `cas_cakanja` in `povzetek_brez_vprasanja`, torej vsaka drugačna zaporedja zahtevajo novo stikalo v kodi | `koraki:` kot urejen seznam v yaml (ime, vozlišče, orodja, pogoj) in profil, zgrajen iz yaml | veliko |
| T9 | **Zahteve na katalog, ki so J&J** (embalaža mora biti `zaprta/odprta/neznana`; zaprt seznam vrst jed/priloga/dodatek/pijača; volumen in gramatura se berejo iz BESEDILA imena, »0,75 L«, »300-350 g«) | Aktivno; Jure je moral nastaviti `neznana_embalaza_narocljiva: da`, sicer jedro zavrne 55 pijač | `katalog_narocila.py:15,39,94,670,683`; `narocilo_joze.py:312` (VEZ-NAR-10,11,21,22) | Če ime nima »0,33 L«, volumen ne deluje; jedilnik z drugo vrsto ne naloži | Polji `volumen_l`, `gramatura` pri varianti; embalaža opcijska (privzeto zaprta); `vrste` v katalogu | srednje |
| T10 | **Vrata in protokoli z imenom agenta** (`protokol: joze-3-razvoj`, razred `NarociloJoze`, `jozef_*` v 150 funkcijah in ključih stanja, `JOZE_*` spremenljivke, Janin `JJBackend`/`TransportJJ` uvoz ob zagonu) | Aktivno (`jedro/nastavitev.py` zavrne vsako drugo vrednost), a brez vpliva na vedenje; poimenovanje je kozmetika | `jedro/nastavitev.py:115-147`; `govor/flows.py` povsod; `klic_jj.py:18` (VEZ-NAR-23,24, ODD-19,20, GOV-28,31, NAS-14) | Vedenje ni vezano, a ime in uvoz mrtve poti vlečeta Janin in J&J kontekst v vsakega naslednjega; `jedro/nastavitev.py` prisili 6 vrednosti (`vhod`, `oddaja_ponovitev`, `poskusi_na_podatek` = 3, `tiha_ponovitev_oblike` = 2, `preveri_ponovitev` = 1, `protokol`), ključi v yaml so videz izbire | Preimenovati pri prvem prepisu (modul `narocilo`), odstraniti mrtvo pot, dovoliti vrednosti iz nastavitve | majhno (mehanično) |

### 2.3 Predlog vrstnega reda (da bi bila nova restavracija en dan dela)

Razvrščeno po tem, kaj je **aktivno za vsako restavracijo** in kaj je Jure **moral spremeniti** (to je dokaz, ne ugibanje). Teme, ki spijo ob drugem jedilniku, so zadnje.

1. **T6, T4, T3** (aktivno, Jure je moral spreminjati kodo): ena pot do mape restavracije; vsa besedila in rezerve iz yaml, profil samo struktura; izgovor iz datoteke (Jure ima shemo `izgovor-1` že narejeno). Merilo: nova restavracija zažene proces samo z novo mapo in ne sliši nobenega J&J stavka ali imena.
2. **T1, samo nalaganje**: `govor.pecenost` in `govor.teza` ne smeta biti obvezna za restavracijo brez steakov. Vedenje pečenosti spi, a nalaganje blokira.
3. **T8**: seznam korakov v yaml, da stikala v profilu odpadejo (drugo največje delo).
4. **T7, T9**: prompt kot predloga; katalog z vrednostmi (`volumen_l`, `gramatura`) namesto razbiranja iz imena.
5. **T2, T5, T10, preostanek T1** (spijo ali so nepreverjeni): ob prvi restavraciji z drugačnim jedilnikom poženi `scripts/meritev_ujemanja.py` in preveri, kaj se sproži. Pečenost in domača kola sta tihi samo, dokler katalog nima teh skupin in imen; če ju ima, se vklopita.

## 3. Jure proti Jožetu: kaj je moral spremeniti v KODI

**Metoda.** Za vsako datoteko v `prevzem/` sem vzel najbližji Jožetov commit (najmanjša razlika med `7c24286`, `df02294`, `19cc929`, `d2f97f6`, `63e1aa2`, `c821a03`, `910e156`, `ae527c6`, `abcfdc4`) in naredil `diff`. Ker Jure po `IZVOR.json` sproti prenaša Jožetove popravke (Entrim `63e1aa2`/`c821a03`, R4a `ae527c6`, k17 `d2f97f6`), so v številkah tudi taki prenosi; število je zato zgornja meja za »Jure samo«. Podatkovnih datotek (yaml, besedilo) in testov nisem štel med kodo. Seznam `spremenjene_datoteke` v Juretovem `IZVOR.json` je nepopoln: `joze_priloge.py` (89 vrstic razlike), `menu_spotter.py` (28) in `joze_cakajoce.py` (2) se razlikujejo, a niso navedeni; zaupati je diffu.

**Preverjeno proti današnjemu Jožetu `abcfdc4`** (grep po `govor/`, `jedro/`, `nastavitve/`, `oddaja/`, `vhodi/`): imena `lazna_potrditev_modela`, `_nosilec_v_stavku`, `potrditev_namesto_zapornice`, `jozef_stavki_modela_odpadejo`, `_enako_ime_vprasanje`, `ponovitev_kratko`, `razlicica_je_ponovitev`, `kolicina_skupaj`, `jure_povzetek`, `izteci_vkljucena_vprasanja`, `ze_vkljuceno_samo_ista`, `_priloga_pripeta_k_jedi`, `jedi_modela`, `cas_cakanja`, `povratni_klic`, `rezervacija_nazaj`, `brez_cen`, `alergija_zastavica`, `sheet_zapis`, veja za velikostne besede ob pijači in fraza »sem se zmotil« v varovalu: **0 zadetkov**, torej Jože teh stvari danes nima. `oznake_so_razlocljive` Jože ima (razred D).

Razredi: **A** = nova zmožnost, ki jo agent potrebuje (potrebuje kodo, ne podatka); **B** = splošni popravek jedra, ki bi moral nazaj v skupni modul (Jože ga nima); **C** = razlika med restavracijama, ki bi morala biti podatek, a je v kodi (dokaz, da jedro ni »samo podatki«); **D** = prenos iz Jožeta (ni Jurejevo).

### 3.1 Spremembe po datotekah

| Datoteka (Jure `prevzem/…`) | Razlika (+/−) proti najbližjemu Jožetu | Kaj je spremenjeno | Razred |
|---|---|---|---|
| `govor/flows.py` | +733 / −58 (baza `d2f97f6`) | povratni klic in prevezava nazaj k rezervaciji (~255 vrstic, novi orodji `rezervacija_nazaj`, `povratni_klic`); `jure_povzetek` (povzetek brez vprašanja); `jure_po_oddaji` (KS-PO-08: »Je še kaj?« po oddaji); ponovljen odgovor o različici (KP-NA-10, ~100 vrstic); `kolicina_skupaj_nastavi` (KP-NA-11, ~100 vrstic); `lazna_potrditev_modela`, `jedi_modela` (F2: model ne imenuje jedi, ki jih ni); zapornica obvod (`potrditev_namesto_zapornice`, `jozef_stavki_modela_odpadejo`); čas čakanja da/ne; razlog zavrnitve po dnevu; korak ure izpuščen (`ura_po_kodi`); `s_jure` v `zgradi_vozlisce` | A (večina), B (`lazna_potrditev_modela`, zapornica obvod), C (vejitve po profilu) |
| `govor/profil.py` | +63 / −4 | 8 novih polj profila (`cas_cakanja`, `povzetek_brez_vprasanja`, `po_oddaji_vprasanje`, `se_kaj_po_vsakem`, `kolicina_skupaj`, `prevezava_nazaj`, `povratni_klic`, `orodja_ura_gosta`); cel profil `PREVZEM_BTC` (vozlišča, orodja, `vprasanja_razlicice`, `popravek_razlicice`, `branje_telefona_razlicice`, `zavrnitev_privzeto`, `napaka_backenda_privzeto`, `odgovor_na_povzetek`, `lazna_potrditev`, `privzeta_besedila` z 11 stavki); `iz_okolja` sprejme `jure` in ga naredi privzetega | C (stavki in regexi v Pythonu) |
| `govor/prevzem_govor.py` | +110 / −19 (baza `df02294`) | validacija za `govor.btc`/`brez_cen` (manj različic, besedila brez cene); `ponovitev_kratko` (krajša ponovitev vprašanja); `_osnove_kandidatov`, `_oznake_imen`, `oznake_so_razlocljive` (D, iz Jožetovega `ae527c6`, prilagojeno) | A in D; **C**: validacija se razlikuje po zastavici `btc` |
| `jedro/moduli/narocilo_joze.py` | +118 / −7 (baza `df02294`) | `brez_cen`, `alergija_zastavica`, `ponudi_dodatke`, `ze_vkljuceno_samo_ista` (vsa iz yaml); odgovor na vprašanje o ponudbi (`_navodilo_ponudbe`); `potrditev_cas_cakanja`; `_enako_ime_vprasanje` (»K pici ali posebej?«); izbira vrste ob enaki besedi; `kaj=jed` pri dodatku | A |
| `jedro/moduli/joze_priloge.py` | +80 / −4 | KP-NA-09: vprašanje o vključeni prilogi samo za isto jed, zapomnjen odgovor, `izteci_vkljucena_vprasanja`, `_priloga_pripeta_k_jedi` | A (stikalo `ze_vkljuceno_samo_ista` v yaml) |
| `jedro/klic.py` | +55 / −3 | čas čakanja, ura prevzema po kodi (`nastavi_cas_prevzema`), pred odprtjem (`ura_izbere_gost`), razlog zavrnitve, vprašanje o številki klica, alergija v listku | A |
| `jedro/moduli/prevzem.py` | +14 / −2 (baza `7c24286`) | `CasCakanja` (rok naročanja po dnevih iz urnika) | A |
| `jedro/listek_backend.py` | +28 / −4 | `alergija`, povzetek iz predloge (`povzetek_predloga`), vprašanje konec (`povzetek_vprasanje_konec`), `sheet_zapis` | A (ključi v yaml) |
| `jedro/moduli/katalog_narocila.py` | +23 / 0 | `Ponudba` iz `jedilnik_kategorije` (ponudba iz jedilnika, F1); velikostne besede ob pijači (»radenska mala«) | A in B |
| `govor/menu_spotter.py` | +23 / −3 | »mehika, ta naj bo pa s tuno«: beseda za »s/z« je dodatek, če je v stavku jed, ki ga ima (`_nosilec_v_stavku`) | B |
| `govor/app.py` | +47 / −16 | `JURE` zastavica; pozdrav, predpona prompta, glas, mapa klicev, vrata po agentu; `jure_uvod`; izbira izgovora (`pravila_btc`) in izklop `PECENOST_IZGOVOR` za Jureta; neoddano v JSONL | **C** (največ) |
| `govor/klic_jj.py` | +48 / −8 | `jure()`, pot nastavitve po agentu (`nastavitve/btc/`), transport Sheet + e-pošta (`naredi_transport_btc`), prejemnik iz okolja, mapa `skupno/` | C |
| `govor/tts_priprava.py` | +20 / 0 | `pravila_btc()` bere `skupno/izgovor-kratochwill.yaml` | C (dober vzorec, a priklop je if JURE) |
| `govor/zakljucek.py` | +14 / −1 | `govori()` brez konca klica; `NAVODILO_ZAKLJUCEVANJE_BTC` brez J&J spletne strani | A in **C** (navodilo po profilu) |
| `govor/varovalo.py` | +2 / −1 | nova imena v seznamu puščanja (`cas_cakanja_*`, `rezervacija_nazaj`, `povratni_klic`); fraza »sem se zmotil« | B in A |
| `vhodi/nastavitev.py` | +10 / −2 (baza `7c24286`) | katalog sme biti v `skupno/`; `cas_cakanja.urnik` iz `skupno/razpolozljivost.py` | A (vhod poti: **C**, mapa je nastavitev, ne koda) |
| `jedro/moduli/joze_listek.py` | +2 / −1 | `alergija` v izvozu listka | A |
| `jedro/moduli/joze_cakajoce.py` | +2 / 0 | `item_id` pri čakajoči prilogi (KP-NA-09) | A |

**Nove datoteke (koda):** `jedro/moduli/cas_cakanja.py` (105 vrstic), `jedro/moduli/jedilnik_btc.py` (199, prepis Bojanovega `jedilnik.py`), `oddaja/oddaja_btc.py` (69), `oddaja/neoddano_jsonl.py` (39), `govor/prevezava_nazaj.py` (44). Nove podatkovne datoteke: `nastavitve/btc/restavracija.yaml` (287 vrstic), pozdrav, prompt, 5 promptov `prompt_jure_*`, `pozdrav_jure.txt`. Testi `tests/jure/`: 285 testov v 25 datotekah (štetje `def test_`; nezagnano).

### 3.2 Stikala Jureta

| Stikalo | Kje | Stanje | Ocena |
|---|---|---|---|
| `cas_cakanja`, `povzetek_brez_vprasanja`, `po_oddaji_vprasanje`, `se_kaj_po_vsakem`, `kolicina_skupaj`, `prevezava_nazaj`, `povratni_klic`, `orodja_ura_gosta` | polja `ProfilPrevzem` v `govor/profil.py`, uporaba v `flows.py` (vsa), `app.py`/`klic_jj.py`/`varovalo.py` (`cas_cakanja`, `povratni_klic`) | Python | **C**: nova restavracija z drugačnim potekom bi zahtevala novo stikalo v kodi; naj bodo ključi `profil:` v yaml |
| `brez_cen`, `alergija_zastavica`, `ponudi_dodatke`, `ze_vkljuceno_samo_ista`, `neznana_embalaza_narocljiva` | `moduli.narocilo.*` v yaml | podatek | OK, vzorec za ostalo |
| `govor.btc`, `govor.brez_cen`, `govor.ponovitev_kratko` | yaml `govor.*` | podatek, a `govor.btc: da` je ime agenta, ki spremeni validacijo (najmanj 1 različica, besedila brez cene) | **C**: razdeli v konkretna stikala |
| `listek.sheet_zapis`, `moduli.prevzem.cas_cakanja`, `glas` | yaml | podatek | OK |

### 3.3 Kaj Jure dokazuje

- Jure je dokaz, da **nastavitev + katalog + prompti** zadoščajo za večino vsebine (njegov yaml odstrani 41 ključev Jožetovega in doda 51 novih (štetje vseh gnezdenih ključev: 265 proti 275)), a **ne za vedenje**: vsaka razlika v poteku (ni vprašanja o uri, povzetek brez vprašanja, »Še kaj?« po vsaki jedi) je zahtevala kodo in stikalo.
- Jure je moral obdržati ostanke J&J v yaml (blok `govor.pecenost` s 25 ključi, `moduli.narocilo.prag_iskanja`/`prag_dodatkov`, `protokol: joze-3-razvoj`), ker ga koda zahteva ali bere (T1, T10).
- Jure je sam našel popravke splošnega jedra (razred B), ki jih Jože nima: `menu_spotter` (s/z), `lazna_potrditev_modela`, velikostne besede ob pijači, »sem se zmotil« v varovalu. Če se Jure in Jože razhajata, bo tak popravek treba prenesti v obe smeri; to je razlog za en skupni modul.
- Jure sproti prevzema Jožetove popravke (`IZVOR.json` beleži prenose `df02294`, `d2f97f6`, `63e1aa2`, `c821a03`, `ae527c6`; postopek je ročen: `git show`, `merge-file`, popravljanje konfliktov). Kopija brez skupne kode zato stalno zaostaja ali zahteva ročno delo.

## 4. Kaj ni preverjeno

- Koliko od 1214 dodanih vrstic je res samo Jurejevih (razdelitev po razredih A do D je moja razvrstitev hunkov, ne meritev po vrsticah).
- Ali Jure z današnjim `abcfdc4` kot izvorom zgradi (testi niso bili zagnani).
- Trud (majhno/srednje/veliko): presoja.
- `skupno/` (urnik, jedilnik, izgovor, `tabela_sheet`) v Kratochwillu je zunaj `prevzem/`; njegove vsebine nisem bral.

## 5. Dodatek: vseh 132 vrstic »vezano na J&J v kodi«

Vir: razdelek »Kaj je vezano na J&J v KODI« v popisih `joze-jedro-narocila.md`, `joze-ujemanje-jedilnika.md`, `joze-prevzem.md`, `joze-oddaja.md`, `joze-nastavitve.md`, `joze-govorni-tok.md`. Pomen kategorije: IME-JEDI = ime jedi, pijače ali skupine v kodi; PRAVILO = pravilo ali struktura, vezana na J&J jedilnik ali potek; BESEDILO = stavek, ki ga gost sliši; ŠTEVILO = konstanta; REGEX = vzorec nad izjavo; NASLOV = e-pošta, pot, strežnik; IME-AGENTA = samo poimenovanje.

| ID | Kje | Kategorija | Predlog (kam v podatke) |
|---|---|---|---|
| VEZ-GOV-01 | govor/tts_priprava.py:47 | IME-JEDI | Polje `izgovor` pri izdelku v katalogu (katalog že ima `govori`) ali ključ `govor.izgovor_imen` v restavracija.yaml; koda samo sestavi regex iz podatka |
| VEZ-GOV-02 | govor/app.py:210 | IME-JEDI | `govor.izgovor` v yaml (seznam parov); vklop, kadar ga yaml ima |
| VEZ-GOV-03 | govor/app.py:217 | BESEDILO | `ime_v_besedilih` je že v yaml; dodaj `govor.izgovor_imena_lokala` |
| VEZ-GOV-04 | govor/tts_priprava.py:35 | REGEX | Vzorec iz `ime_v_besedilih` ali ključ `govor.izgovor_meni_za` |
| VEZ-GOV-05 | govor/narocanje_sproti.py:195 | IME-JEDI | Izpeljati iz kataloga (beseda, ki nastopa v več imenih/skupinah) ali `katalog.splosne_besede` |
| VEZ-GOV-06 | govor/flows.py:6451 | IME-JEDI | Isti vir kot VEZ-GOV-05 |
| VEZ-GOV-07 | govor/narocanje_sproti.py:199 | IME-JEDI | Polje `sinonimi` izdelka v katalogu (obstaja); sklon pokrije `_isti_koren` |
| VEZ-GOV-08 | govor/flows.py:3641 | PRAVILO | Ime skupine bi moralo priti iz `govor.pecenost.ime` (v yaml že je: `ime: pečenost`) ali iz zastavice skupine v katalogu |
| VEZ-GOV-09 | govor/flows.py:3408 | PRAVILO | Vklop z zastavico `tehtane_jedi` v `profil.py` ali ko ima katalog polje `gramatura`; sicer se veja ne sproži |
| VEZ-GOV-10 | govor/flows.py:3441 | PRAVILO | Isto kot VEZ-GOV-09 (zastavica) |
| VEZ-GOV-11 | govor/flows.py:3981 | PRAVILO | Pečenost je posebnost J&J jedilnika (Jure jo ima izklopljeno: katalog je nima). Zastavica `profil.pecenost` ali posplošitev na »izbira, ki jo gost pove skupaj z jedjo« |
| VEZ-GOV-12 | govor/flows.py:4689 | PRAVILO | Isto (zastavica); besedilo je že v `govor.pecenost.*` |
| VEZ-GOV-13 | govor/flows.py:6743 | REGEX | Enote iz kataloga (`cena_na`, `enota`), vklop kot VEZ-GOV-09 |
| VEZ-GOV-14 | govor/flows.py:168 | BESEDILO | `govor.trenutek` v yaml (besedilo je že ločeno od prompta v ostalih primerih) |
| VEZ-GOV-15 | govor/flows.py:2157 | BESEDILO | `govor.prehodi` in `govor.uvodi_popravka` v yaml |
| VEZ-GOV-16 | govor/flows.py:3050 | REGEX | Združiti s `profil.lazna_potrditev` (je že v profilu, a z drugim vzorcem) |
| VEZ-GOV-17 | govor/flows.py:5611 | PRAVILO | `profil.koraki` kot urejen seznam korakov (Jure je moral dodati stikala `cas_cakanja`, `povzetek_brez_vprasanja`, da korak ure odpade) |
| VEZ-GOV-18 | govor/profil.py:194 | BESEDILO | Beri iz yaml (`govor.vprasanja.*`); profil naj ostane samo struktura (vozlišča, orodja) |
| VEZ-GOV-19 | govor/profil.py:164 | BESEDILO | yaml `govor`; spol govorca v `govorec` (yaml že ima `govorec: Jože`) |
| VEZ-GOV-20 | govor/profil.py:169 | REGEX | Vzorci iz besedil v yaml (sestavi regex iz `govor.povzetek_vprasanje` in `besedila.*`) |
| VEZ-GOV-21 | govor/profil.py:175 | BESEDILO | Rezerva v kodi naj odpade; zahtevati, da yaml vsebuje vsa besedila (preverjanje v `jedro/nastavitev.py` že obstaja) |
| VEZ-GOV-22 | govor/zakljucek.py:60 | BESEDILO | Premakniti v yaml, kot VEZ-GOV-21 |
| VEZ-GOV-23 | govor/zakljucek.py:65 | BESEDILO | `besedila.navodilo_zakljucevanje` v yaml |
| VEZ-GOV-24 | govor/zakljucek.py:53 | ŠTEVILO | `govor.casi` v yaml |
| VEZ-GOV-25 | govor/flows.py:5612 | ŠTEVILO | `govor.meje` v yaml |
| VEZ-GOV-26 | govor/klic_jj.py:27 | PRAVILO | Pot iz okolja (`RESTAVRACIJA_POT`) ali iz profila; Jure ima svojo mapo `nastavitve/btc/`: `pot_nastavitve_prevzem()` v njegovem `govor/klic_jj.py` izbere pot z `if jure()`, torej je izbira poti spet v kodi |
| VEZ-GOV-27 | govor/predaja.py:37 | IME-AGENTA | Env `PREDAJA_KONTEKST` ali yaml |
| VEZ-GOV-28 | govor/varovalo.py:71 | IME-AGENTA | Seznam imen izpeljati iz `profil.orodja_*` in statusov jedra; fraze iz prompta ostanejo skupne za vse agente |
| VEZ-GOV-29 | govor/tts_priprava.py:22 | REGEX | Sestaviti iz `profil.popravek_razlicice` namesto da je vzorec fiksen v kodi |
| VEZ-GOV-30 | govor/app.py:154 | ŠTEVILO | `govorec.glas` v yaml (ključ `govorec` že obstaja) |
| VEZ-GOV-31 | govor/flows.py:3343 | IME-AGENTA | Poimenovanje (imena `joze_*`, `jozef_*` v 150 funkcijah in ključih stanja); vedenje ni vezano na J&J |
| VEZ-NAR-01 | `jedro/moduli/narocilo_joze.py:181` | PRAVILO | v katalog polje `vloga: pecenost` na skupini; koda bere vlogo, ne imena |
| VEZ-NAR-02 | `jedro/moduli/joze_spremembe.py:569` | PRAVILO | enako kot VEZ-NAR-01 |
| VEZ-NAR-03 | `jedro/moduli/joze_listek.py:48` | PRAVILO | enako kot VEZ-NAR-01 |
| VEZ-NAR-04 | `jedro/moduli/joze_spremembe.py:675` | BESEDILO | izpeljati iz `sinonimi` izbir skupine z vlogo `pecenost` + yaml seznam splošnih besed (karkoli, vseeno) |
| VEZ-NAR-05 | `jedro/moduli/joze_spremembe.py:539` | BESEDILO | rezerva ven iz kode (obvezen yaml ključ, ob manjkajočem napaka ob zagonu); besedilo listka v yaml |
| VEZ-NAR-06 | `jedro/moduli/narocilo_joze.py:1159` | PRAVILO | v katalog `tehtano: {korak: 100}` (ali `enota_teze`); koda bere polje |
| VEZ-NAR-07 | `jedro/moduli/narocilo_joze.py:1160` | ŠTEVILO | rezerva ven; obvezen ključ ob tehtanih jedeh |
| VEZ-NAR-08 | `jedro/moduli/joze_listek.py:72` | BESEDILO | yaml `besedila_listka` |
| VEZ-NAR-09 | `jedro/moduli/narocilo_joze.py:610` | IME-JEDI | sopomenke v katalogu (skupna tabela enakih besed, glej VEZ-UJE-02) |
| VEZ-NAR-10 | `jedro/moduli/katalog_narocila.py:683` | PRAVILO | polje `volumen_l` pri varianti; ime nima vloge |
| VEZ-NAR-11 | `jedro/moduli/katalog_narocila.py:39` | PRAVILO | polje `gramatura: {od, do}` pri varianti |
| VEZ-NAR-12 | `jedro/moduli/joze_spremembe.py:723` | PRAVILO | skupina polje `posodica: true` |
| VEZ-NAR-13 | `jedro/moduli/katalog_narocila.py:611` | IME-JEDI | katalog: par `zamenljivo` z namigi in razlago; za restavracijo brez take pijače se ne uporabi (koda že preveri obstoj obeh imen) |
| VEZ-NAR-14 | `jedro/moduli/katalog_narocila.py:695` | IME-JEDI | katalog `razlicica` (npr. »z dvema pleskavicama«) in splošna sopomenka lastnosti, brez regexa |
| VEZ-NAR-15 | `jedro/moduli/katalog_narocila.py:717` | IME-JEDI | katalog `nepomembne_besede` po vrsti jedi (obstaja že za vse jedi) |
| VEZ-NAR-16 | `jedro/moduli/katalog_narocila.py:709` | IME-JEDI | katalog `nepomembne_besede` ali `izraz` skupine |
| VEZ-NAR-17 | `jedro/moduli/narocilo_joze.py:127` | ŠTEVILO | yaml `moduli.narocilo.veliko_narocilo_kosov` |
| VEZ-NAR-18 | `jedro/moduli/joze_izgovor.py:178` | BESEDILO | yaml `izgovor_kratice` |
| VEZ-NAR-19 | `jedro/moduli/joze_dobesedno.py:15` | IME-JEDI | yaml `dobesedno.splosne_besede` ali izpeljati iz imen skupin kataloga |
| VEZ-NAR-20 | `jedro/moduli/narocilo_joze.py:105` | IME-JEDI | primeri v yaml (`primeri_orodij`) ali splošni primeri |
| VEZ-NAR-21 | `jedro/moduli/katalog_narocila.py:94` | PRAVILO | polje opcijsko (privzeto `zaprta`); ali preimenovati v `za_prevzem: da/ne/neznano` |
| VEZ-NAR-22 | `jedro/moduli/katalog_narocila.py:15` | PRAVILO | `vrste` v katalogu (privzeto štiri) |
| VEZ-NAR-23 | `jedro/nastavitev.py:145` | IME-AGENTA | preimenovati v `protokol: narocilo-v1` (samo poimenovanje) |
| VEZ-NAR-24 | `jedro/moduli/narocilo_joze.py:84` | IME-AGENTA | preimenovati pri prvem prepisu (modul `narocilo`) |
| VEZ-NAS-01 | `prompti/pozdrav_joze.txt:1` | BESEDILO | `pozdrav` iz nastavitve z `{ime_za_gosta}`; test brez imena |
| VEZ-NAS-02 | `prompti/prompt_joze_osnova.txt:2` | BESEDILO | `{agent_ime}`, `{ime_za_gosta}`, spol iz nastavitve |
| VEZ-NAS-03 | `prompti/prompt_joze_osnova.txt:13` | NASLOV | `spletna_stran`, `napotitev_besedilo` v nastavitvi |
| VEZ-NAS-04 | `prompti/prompt_joze_osnova.txt:14` | IME-JEDI | `govor.priporocilo` v nastavitvi |
| VEZ-NAS-05 | `prompti/prompt_joze_osnova.txt:16` | PRAVILO | `govor.alergija_odgovor`, `govor.opomba_odgovor`, `placilo` |
| VEZ-NAS-06 | `prompti/prompt_joze_osnova.txt:8` | IME-JEDI | Primeri iz kataloga ob sestavi prompta (`primeri` v katalogu) |
| VEZ-NAS-07 | `prompti/prompt_joze_vozlisce_narocilo.txt:15` | PRAVILO | Nabor vprašanj iz kataloga (`skupine_dodatkov[].tip`) |
| VEZ-NAS-08 | `tests/govor/test_prompti_joze.py:30` | ŠTEVILO | Meja kot nastavitev; prompt krajšati z izpuščenimi J&J primeri |
| VEZ-NAS-09 | `govor/app.py:87` | IME-AGENTA | Poti iz nastavitve (`prompti.osnova`, `prompti.vozlisca`) |
| VEZ-NAS-10 | `govor/app.py:154` | ŠTEVILO | `govor.glas`, `govor.hitrost` v nastavitvi |
| VEZ-NAS-11 | `govor/app.py:217` | IME-JEDI | `govor.izgovor_pravila` (regex, zvok) v nastavitvi |
| VEZ-NAS-12 | `govor/tts_priprava.py:48` | IME-JEDI | Katalog `izgovor_tts` po izdelku; `ime_za_gosta` namesto »jack« |
| VEZ-NAS-13 | `govor/zakljucek.py:53` | ŠTEVILO | `pravila.tisina`, `pravila.najdaljsi_klic_s` (ključa že obstajata, koda ju ne bere) |
| VEZ-NAS-14 | `jedro/nastavitev.py:115` | ŠTEVILO | Dopusti vrednost iz nastavitve |
| VEZ-NAS-15 | `nastavitve/restavracija.yaml:143` | PRAVILO | Samo katalog |
| VEZ-NAS-16 | `govor/profil.py:176` | NASLOV | Rezervo odstrani, nastavitev je obvezna |
| VEZ-NAS-17 | `jedro/moduli/katalog_narocila.py:613` | IME-JEDI | Katalog `zvocne_dvoumnosti` (seznam osnov in razlaga) |
| VEZ-NAS-18 | `jedro/moduli/joze_spremembe.py:675` | PRAVILO | Sinonimi iz skupine izbir v katalogu, `vloga: pecenost` |
| VEZ-NAS-19 | `jedro/moduli/ujemanje_jedilnika.py:37` | IME-JEDI | `nepomembne_besede` in `sinonimi` v katalogu |
| VEZ-NAS-20 | `govor/menu_spotter.py:29` | IME-JEDI | Katalog `skupine` in `splosne_besede` (polje že obstaja) |
| VEZ-NAS-21 | `jedro/moduli/joze_izgovor.py:178` | BESEDILO | `govor.kratice` ali katalog `izgovor` |
| VEZ-NAS-22 | `jedro/moduli/katalog_narocila.py:15` | ŠTEVILO | Prag je že v katalogu; vrste so pojem sistema (OK) |
| VEZ-NAS-23 | `nastavitve/restavracija.yaml:130` | NASLOV | Podatek (OK) |
| VEZ-NAS-24 | `nastavitve/restavracija.yaml:40` | BESEDILO | Predloga z `{ura}` |
| VEZ-ODD-01 | `jedro/listek_backend.py:277` | BESEDILO | `listek.predloga` (oznake) |
| VEZ-ODD-02 | `jedro/listek_backend.py:353` | BESEDILO | `listek.zadeva` |
| VEZ-ODD-03 | `jedro/listek_backend.py:299` | BESEDILO | `listek.predloga` |
| VEZ-ODD-04 | `jedro/listek_backend.py:306` | PRAVILO | `listek.vrstice_na_koncu` (seznam besedil) |
| VEZ-ODD-05 | `jedro/listek_backend.py:49` | PRAVILO | Dovoli poljuben nabor, ki ima polja iz `vrstni_red` |
| VEZ-ODD-06 | `jedro/listek_backend.py:237` | ŠTEVILO | `pravila.najvec_sprememb_kratkega_popravka` |
| VEZ-ODD-07 | `jedro/listek_backend.py:412` | ŠTEVILO | `listek.roki.*` |
| VEZ-ODD-08 | `jedro/listek_backend.py:402` | BESEDILO | `listek.opozorilo.besedilo`, `zadeva` |
| VEZ-ODD-09 | `jedro/moduli/joze_listek.py:48` | PRAVILO | Polje skupine `vloga: pecenost` v katalogu; oznake v `listek.predloga` |
| VEZ-ODD-10 | `jedro/moduli/joze_listek.py:72` | BESEDILO | Brez privzetih v kodi: ključi obvezni (že so v nastavitvi) |
| VEZ-ODD-11 | `jedro/summary.py:11` | BESEDILO | `govor.oddaja_vprasanje` |
| VEZ-ODD-12 | `jedro/listek_backend.py:181` | BESEDILO | `govor.povzetek_konec`, `govor.popravek_konec` |
| VEZ-ODD-13 | `jedro/klic.py:91` | BESEDILO | Brez privzetega besedila (obvezen ključ) |
| VEZ-ODD-14 | `govor/profil.py:176` | BESEDILO | Samo v nastavitvi; test `test_profil_okolje` primerja podvojena besedila |
| VEZ-ODD-15 | `oddaja/listek_eposta.py:28` | NASLOV | `listek.smtp.gostitelj/vrata` in imena spremenljivk |
| VEZ-ODD-16 | `oddaja/neoddano.py:25` | NASLOV | Okolje `AGENT_NEODDANO_DIR` ali nastavitev |
| VEZ-ODD-17 | `govor/klic_jj.py:27` | NASLOV | Pot kot parameter zagona |
| VEZ-ODD-18 | `govor/klic_jj.py:85` | ŠTEVILO | `casovni_pas` v nastavitvi |
| VEZ-ODD-19 | `govor/klic_jj.py:18` | IME-AGENTA | Odstrani iz prevzemnega agenta |
| VEZ-ODD-20 | `jedro/listek_backend.py:377` | IME-AGENTA | Samo poimenovanje |
| VEZ-PRE-01 | `jedro/moduli/prevzem.py:138` | BESEDILO | `moduli.prevzem.besedila.korak` |
| VEZ-PRE-02 | `jedro/moduli/prevzem.py:140` | BESEDILO | `moduli.prevzem.besedila.zadnji_prevzem` z mestom `{ura}` |
| VEZ-PRE-03 | `jedro/moduli/prevzem.py:156` | BESEDILO | `moduli.prevzem.besedila.ura_ne_obstaja` |
| VEZ-PRE-04 | `jedro/moduli/prevzem.py:130` | BESEDILO | Odstrani rezervo; `preveri_nastavitev` naj zahteva ključe |
| VEZ-PRE-05 | `jedro/moduli/prevzem.py:194` | BESEDILO | `moduli.prevzem.besedila.danes` |
| VEZ-PRE-06 | `jedro/moduli/narocilo_joze.py:127` | ŠTEVILO | `moduli.narocilo.veliko_narocilo_kosov` |
| VEZ-PRE-07 | `govor/flows.py:5612` | ŠTEVILO | Bere iz `pravila.poskusi_na_podatek`, odstrani prisilo na 3 |
| VEZ-PRE-08 | `nastavitve/restavracija.yaml:40` | BESEDILO | Sestavi iz `narocila_do` (`{ura}` + `spoken_time`) |
| VEZ-PRE-09 | `govor/prevzem_govor.py:368` | PRAVILO | Blok `pecenost` obvezen samo, če katalog ima skupino izbire z lestvico |
| VEZ-PRE-10 | `govor/prevzem_govor.py:481` | PRAVILO | Splošen tip »izbira z lestvico« v katalogu (`tip: lestvica`) z besedili v `izbire_vprasanja` |
| VEZ-PRE-11 | `govor/prevzem_govor.py:280` | PRAVILO | Iz kataloga (`izbire[].sinonimi`, `izgovor`) |
| VEZ-PRE-12 | `jedro/moduli/joze_listek.py:48` | PRAVILO | Polje skupine `vloga: pecenost` v katalogu namesto primerjave imena |
| VEZ-PRE-13 | `govor/prevzem_govor.py:501` | ŠTEVILO | Katalog `enota` je že podatek; privzeto naj bo napaka, ne »100 g« |
| VEZ-PRE-14 | `govor/prevzem_govor.py:434` | ŠTEVILO | `govor.meje.*` v nastavitvi |
| VEZ-PRE-15 | `govor/prevzem_govor.py:646` | BESEDILO | `govor.nadomestne_besede` (ali odstrani: katalog že ima `skupine[].izraz`, `mn_rod`) |
| VEZ-PRE-16 | `govor/prevzem_govor.py:742` | PRAVILO | `govor.ni_za_prevzem.najvec_primerov`, vrednosti embalaže v katalogu |
| VEZ-PRE-17 | `govor/profil.py:210` | BESEDILO | `govor.ime.vprasanja` |
| VEZ-PRE-18 | `govor/profil.py:213` | BESEDILO | Ostane v profilu (jezik), ne v restavraciji |
| VEZ-PRE-19 | `govor/flows.py:5611` | IME-AGENTA | Samo poimenovanje, ne vsebina |
| VEZ-PRE-20 | `jedro/moduli/prevzem.py:14` | IME-AGENTA | Samo poimenovanje |
| VEZ-PRE-21 | `govor/flows.py:2569` | BESEDILO | `govor.prehodi` (isto kot VEZ-GOV-15) |
| VEZ-UJE-01 | `jedro/moduli/ujemanje_jedilnika.py:37` | IME-JEDI | samo `nepomembne_besede` v katalogu; koda ima samo slovnična polnila (z, s, iz, do) |
| VEZ-UJE-02 | `jedro/moduli/ujemanje_jedilnika.py:61` | IME-JEDI | katalog `enake_besede: [[...], ...]` (en seznam na restavracijo) |
| VEZ-UJE-03 | `jedro/moduli/ujemanje_jedilnika.py:28` | ŠTEVILO | yaml `ujemanje: {prag_besede, prag_razlike, min_dolzina}` s privzetimi vrednostmi; po zamenjavi kataloga zagnati `meritev_ujemanja.py` |
| VEZ-UJE-04 | `jedro/moduli/ujemanje_jedilnika.py:54` | ŠTEVILO | generirati iz `stevilo_z_besedo` (`joze_izgovor.py:14`, 1 do 999); jedro `stevilo_iz_besed` (`narocilo_joze.py:65`) to že dela |
| VEZ-UJE-05 | `jedro/moduli/ujemanje_jedilnika.py:90` | BESEDILO | `enake_besede` (VEZ-UJE-02) |
| VEZ-UJE-06 | `jedro/moduli/katalog_narocila.py:276` | ŠTEVILO | yaml `ujemanje.prag_priblizne_omembe` |
| VEZ-UJE-07 | `jedro/moduli/katalog_narocila.py:611` | IME-JEDI | katalog: par `zamenljivo` z namigi in razlago |
| VEZ-UJE-08 | `govor/menu_spotter.py:29` | IME-JEDI | katalog: `skupine.*.naroci_skupno: true` |
| VEZ-UJE-09 | `govor/menu_spotter.py:34` | IME-JEDI | izpeljati iz `skupine.*.izraz`/`sinonimi` kataloga + kratek yaml seznam splošnih besed |
| VEZ-UJE-10 | `govor/menu_spotter.py:155` | IME-JEDI | isti podatek `zamenljivo` kot VEZ-UJE-07 |
| VEZ-UJE-11 | `scripts/meritev_ujemanja.py:14` | IME-JEDI | `nastavitve/<restavracija>/meritev.yaml` s `tuje_besede` |
| VEZ-UJE-12 | `tests/test_joze_pokritost_jedilnika.py:25` | IME-JEDI | prebrati iz podatka `zamenljivo` (VEZ-UJE-07) |
