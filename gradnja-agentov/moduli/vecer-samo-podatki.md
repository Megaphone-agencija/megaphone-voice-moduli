# Večer: kaj bi bilo treba za novo medijsko hišo spremeniti (podatki ali koda)

- **Namen**: preveriti trditev »nova medijska hiša (drug časopis ali druga Večerova izdaja) = ista koda + drugi podatki, v enem dnevu«. Vir: osem popisov `vecer-*.md` v tej mapi (poleg `vecer-model-pogovor.md`, ki ga naloga ni zahtevala, a vsebuje pozive in shemo orodja).
- **Stanje**: Večer `c878782`, veja `splosna-pravila` (17. 11. 2026), čist izvoz `git archive`. To je najnovejše stanje, ki vsebuje `main` `60a75e1` in `faza-7` `8ed5317` (obe sta prednika; 226 commitov nad faza-7). **Ni v `main`.** Veja `paket-1-javni-vhod` (`0d49152`: omejitve javnega vhoda) in `docs/vecer-jezik-dopolnitev-20261104` (`c4ad204`) NISTA vključeni. Datum 2026-11-24. Samo branje; testi niso bili zagnani, nič ni bilo zagnano.
- **Kako brati oznake**: *podatek (OK)* = vrednost je v yaml, txt ali bazi: zamenjaš datoteko, kode ne diraš. *koda (problem)* = vrednost ali pravilo je v `.py`: za novo hišo je treba urediti kodo. **Trije nivoji**: slovenščina in domena »reklamacija dostave časopisa« sta v kodi v redu in ne štejeta kot VEZ; VEZ je samo to, kar je specifično za Večer ali za eno hišo.

## 1. Povzetek (odgovor na vprašanje)

**Jedro še ni »samo podatki«.** Besedila, pozivi, izgovor krajev in večina številk so res podatki, vendar so trije sklopi trdo v kodi: **pravila rešitve in odpisa**, **zaprti seznami vrst težave in šifrant** ter **pot do podatkov hiše** (`mediji/vecer/` je vpisan na 6 mestih). Poleg tega v kodi ni ciljne evidence za zapis (samo lokalni SQLite), ni uvoza baze naročnikov (samo skripta za Večerov CSV) in ni telefonije (klic pride samo prek brskalnika).

| Kaj | Število | Vir |
|---|---|---|
| Zmožnosti v popisih (ID `XXX-nn`) | 479 | `preveri_vecer_popise.py` iz tabel (ne ocena) |
| Od tega »ni testa« (celica testa je samo »ni testa«) | 20 | isto; še 10 celic omenja »ni testa« samo delno |
| Vrstic »vezano na Večer v kodi« (VEZ) | 171 | isto |
| VEZ po kategoriji | PRAVILO 66, ŠTEVILO 37, BESEDILO 26, NASLOV 21, IME-VECER 16, REGEX 3, IME-AGENTA 2 | isto |
| Testi (`def test_`) v izvozu | 2950 (vključno s `tests/zvok/`) | `grep -c "def test_"` po `tests/` |
| Datoteke v `kanon/` (scenariji, orakelj; samo za Večer) | 807 | `find kanon -type f` |
| Oznake besedil M-BS v `besedila.yaml` | 73 (README repozitorija pravi 61: zastarelo; 64 minus 3 zavržene = 61 pri uskladitvi 15. 10., nato dodanih 12) | `grep -c "^  M-BS-"` |
| Listi v `mediji/vecer/nastavitev.yaml` | 24; po popisu STA bere kodo 19, 5 je mrtvih (`verzija`, `najvec_za_mehko_primerjavo`, `najvec_v_seznamu`, `zacetek_delovnega_casa`, `narocniska_sluzba_e_naslov`) | `vecer-jedro-stanje.md`, VEZ-STA-11 |

VEZ se v popisih podvajajo (isti problem v več popisih, npr. šifrant `dwh.py` v ISK, ZAP in STA); spodnjih 12 tem jih združuje.

**Nepreverjeno**: koliko dni bi res trajala zamenjava na novi hiši (nobena stranka še ni bila vzpostavljena; ocene truda zato ne dajem). Ali so pragovi ujemanja imen (`ujemanje.py:21-25`) dobri za drugo bazo: meritev ni v izvozu. Ali na strežniku danes teče pravi Soniox in pravi model (komentar `deploy/vecer-poc.service:1` kaže lažni način).

## 2. Kaj je že podatek (OK)

| Kaj | Pot | Opomba |
|---|---|---|
| Fiksna besedila, ki jih izgovori koda (73 ID-jev, tipi fiksno/predloga/referencno/samo_primer, 37 alternativnih nizov na 16 referencah, 27 parametrov) | `mediji/vecer/besedila.yaml` | po ID-jih iz CL; glej T8 za 12 ID-jev z Večerovimi vsebinami |
| Pozivi modelu (8 txt, skupaj 107 vrstic) in nastavitev modela (ime, URL, ponudniki, `max_tokens`) | `mediji/vecer/pozivi/*.txt`, `model.yaml` | podatek, a ni predloge (T9) |
| Poskusi, ure, molk, rok pošte (`ure.rok_poste`), kontakt (telefon) | `mediji/vecer/nastavitev.yaml` | rok pošte koda bere iz yaml (VEZ-CAS-07 ugotavlja: brez dvojnika v kodi, ampak ura 19 je še v pozivu in v kanonu, T4) |
| Izgovor krajev (103 ključev) in ulic (44 ročnih + 153 generiranih) | `mediji/vecer/izgovor_krajev_ulic.yaml`, generator `scripts/zgradi_izgovor_ulic.py` | za drugo regijo se `kraji` gradi ročno, generatorja zanje ni (VEZ-BES-11) |
| Seznam krajev za razpoznavanje govora | iz baze (`SELECT DISTINCT kraj`) | podatek, ne koda (ISK) |
| Baza naročnikov (SQLite: `narocnik`, `naslov_fts`, `meta`) | datoteka, pot argument | shema je določena (T6), vsebina je podatek |
| Ponudnik modela, ključi | `deploy/vecer.env.example`, `deploy/pravi-model.conf` | imena spremenljivk so v kodi (T11) |

## 3. Kaj je koda (problem): teme, ki jih je treba spraviti v podatke

Vsaka tema združuje več VEZ vrstic (ID-ji v zadnjem stolpcu). Polna tabela vseh 171 je v popisih.

| Tema | Kaj je trdo v kodi | Pot:vrstica (primeri) | Predlog, kako v podatke | VEZ |
|---|---|---|---|---|
| **T1 Pot do podatkov hiše** | Pot `mediji/vecer/` je privzeta na 6 mestih; hiše ni mogoče izbrati z nastavitvijo. | `medij/besedila.py:15`, `medij/nastavitev.py:10`, `medij/govor/pozivi.py:16`, `medij/govor/model.py:42`, `medij/prenos/izgovor_krajev_ulic.py:22`, `scripts/zgradi_izgovor_ulic.py:38` | ena spremenljivka okolja (ime hiše ali mapa), vsi nalagalniki berejo od tam | STA-05, BES-09, MOD-21, RES-20, VRS-06, ZAP-19 |
| **T2 Pravila rešitve in odpisa** | Matrika »kaj se ponudi«: nadomestni izvod samo ob nedostavi in samo za današnji dan, odpis samo za pretekle dneve, zamuda (`prepozno`) nikoli rešitve, zavrnitev, »vseeno«. Zaprt seznam rešitev. Pomen »odpis = odšteje od računa« je v kodi. | `medij/vrstni_red.py:562-593`, `medij/obrat.py:149`, `medij/stanje.py:18`, `medij/zapis.py:120-146`, `medij/prenos/dwh.py` | tabela `pravila_resitve` v yaml (vrsta težave, starost dneva, način dostave, pred uro, trajanje; kaj ponudi, kaj zapiše, katera besedila). Predlog po popisu RES. | RES-03..06, 12, 13, 22, VRS-08, ZAP-04, 06 |
| **T3 Pošta in rok 19. ure** | Oblika pravila: samo nedostava, samo danes, samo način `posta`, samo pred `ure.rok_poste`; »tiha pot« (brez povzetka, predaje, zaključka); ura 19 je še v pozivu in v kanonu. Pravilo je podvojeno tudi v `pogovor.py:834`. | `medij/vrstni_red.py:267-285, 536-543`, `mediji/vecer/pozivi/cas.txt:7`, `kanon/orodja/zgradi_resitev.py:323,768` | pravilo v tabeli iz T2; ura v pozivu iz parametra | RES-01, 02, 11, VRS-07, ZAP-10, MOD-04 |
| **T4 Prag »nad tednom« in staro obdobje** | Meja 7 dni na 5 mestih; izrazi »že mesec«, »par tednov« vedno sprožijo predajo; staro ohlapno obdobje nikoli odpisa; razponi ohlapnih časov (5 do 9 dni ...) in okno enega meseca. | `medij/ohlapni_datum.py:28,99`, `medij/ohlapni_cas.py:34-40`, `medij/vrstni_red.py:288-309`, `medij/zapis.py:58-75,171` | `trajanje_predaja_dni`, `okno_ponavljanja_dni` v yaml; tabela ohlapnih časov kot yaml | RES-07..10, CAS-09..11, VRS-11, ZAP-05 |
| **T5 Koledar in delovni čas** | Izvod izide vsak koledarski dan (»že tretji dan« izpelje včeraj, predvčeraj); delovnik pon do pet; ura 15 je še enkrat literal; 12 državnih praznikov iz spomina, `PRAZNIKI_PREGLEDANI = False`. Ključ `ure.zacetek_delovnega_casa` ni v uporabi. | `medij/dnevi.py:62,69`, `medij/delovni_cas.py:13-15,41,53`, `medij/obrat.py:671` | koledar izhajanja (dnevi v tednu, prazniki) v yaml; ura 15 samo iz `ure.konec_delovnega_casa` | CAS-01..06, 13, STA-10, ZAP-11, 13 |
| **T6 Vrste težave, šifrant, shema zapisa** | Zaprt seznam 13 vrst težave (`VELJAVNE_VRSTE`), neznana vrsta se ne sprejme; ponovljen v shemi orodja, pozivih, `ref.py`, `popravek.py`; šifrant 26 Večerovih nazivov DWH, vrstni red šifer, meja 7 dni, odločitev »samo 2 od 10 drugih vrst imata šifro«; shema zapisa zaprta. | `medij/stanje.py:20-24`, `medij/govor/orodje.py:25-39`, `medij/prenos/dwh.py:22-33,62-81,84,104`, `medij/zapis.py:24-50`, `mediji/vecer/pozivi/razlog.txt:4` | `vrste.yaml` (ime, ima čas, ima rešitev, šifra v ciljnem sistemu); shema orodja, poziv in šifrant se generirajo iz nje | STA-01, 02, MOD-05..07, ZAP-01..03, 07, 08, ISK-17, 18 |
| **T7 Ciljni sistem zapisa** | Zapis gre samo v lokalno SQLite (en SQLite na klic); v kodi ni URL-ja, žetona ali konektorja; `Okolje.dnevnik` je `object`, `Pogovor` ujame samo `sqlite3.Error`, `ValueError`, `TypeError`; format `event_id` in `operation_id` je trd. | `medij/dnevnik.py:160-174`, `medij/izvajalec.py:46,48,269-273`, `medij/zvok/scenariji.py:343` | vmesnik ponora z implementacijo po hiši; ime ponora v yaml (načrtovano v `docs/nacrt-implementacije.md:112,280`, faza 11, ni narejeno) | ZAP-09, 20, 21 |
| **T8 Besedila vezana na kodo** | 12 od 73 ID-jev ima dobesedno Večer, e-naslov `narocnina@vecer.com` (8 referenc v 6 ID-jih) ali »od sedmih do petnajstih« z besedami; 17 je vezanih na pravila ali službe brez imena, 44 splošnih. Pričakovani nabor je `range(1, 77)` brez M-BS-17, 24, 57; nov parameter zahteva vpis v `SLOTI_RAZRED` in polnilec. Logika po literalih besedil (`"M-BS-18"`, `"nadomestni izvod"`). `OPOMBA_*` so hkrati signal v kodi (`povzetek.py:195`). | `mediji/vecer/besedila.yaml:441-809`, `medij/besedila.py:18-46`, `medij/izvajalec.py:77-98`, `medij/obrat.py:857`, `medij/vrstni_red.py:593`, `medij/povzetek.py:195` | parametri `{medij}`, `{e_naslov}`, `{delovni_cas}`; pričakovani nabor iz yaml; opombe z oznako (koda) ločeno od besedila | BES-01..08, RES-18, 19, STA-03 |
| **T9 Stavki v kodi in prompti** | Stavki za klicatelja ali operaterko v `.py` (npr. `NADOMESTNO_RACUNALNIK = "Sem Večerov AI asistent."`, uvodi povzetka, odpisne fraze, 34 nizov za operaterke v `zapis.py`, `obrat.py`, `stanje.py`, `izvajalec.py` (štetje iz popisa BES)). Pozivi: Večerovih je 8 vrstic v 3 datotekah (`osnova.txt:2,20,31`, `naslov.txt:4,5,9`, `cas.txt:6,7`), vrednosti zaprtih seznamov v 20 vrsticah v 7 datotekah; predloge s parametri ni; `razlog.txt` 5991 znakov od 6000. | `medij/govor/pogovor.py:55,61,803`, `medij/povzetek.py:23,27`, `medij/vrstni_red.py:307,311-321`, `medij/zapis.py`, `mediji/vecer/pozivi/` | stavke v yaml z ID-jem iz CL; poziv kot predloga z `{medij}`, `{kraji}`, `{rok_poste}` | BES-12..17, STA-04, ZAP-14..18, RES-16, 17, MOD-01..03, 15, 16, VRS-04, 05 |
| **T10 Uvoz baze naročnikov** | Splošnega uvoza ni. Edina gradnja je `rp2/zgradi_realno_bazo.py`: Večerova `narocniki.csv` in `narocnine.csv`, vrste `PRAVNA OSEBA`, `ŠOLE`, `KOLPORTER` so ustanove, pravilo »aktiven naročnik«, zunanji `ingest.py` (ni v izvozu). Shema nima publikacije, izdaje, šifre dostave, naročnine. Pragovi ujemanja imen (0,6 / 0,65 / 0,75 / 0,15 / 4) so prepisani iz JS in niso nastavljivi. | `rp2/zgradi_realno_bazo.py:6-8,29-31,50,138-165`, `medij/prenos/ujemanje.py:21-25`, `medij/imenik.py:30,251,502` | uvoz iz CSV po preslikavi stolpcev v yaml; pragovi v nastavitvi, ob menjavi baze ponovno izmerjeni | ISK-01..03, 12..16 |
| **T11 Model in ključi** | Imena ključev `OPENROUTER_API_KEY_VECER`, `OPENROUTER_API_KEY`, `ENTRIM_API_KEY`, glava `X-Title`, ime loggerja `vecer.model`; rezerva (telo zahtevka) prirejena Entrimu; zaprti seznami v shemi orodja (7 namenov, 13 stranskih vrst, 2 načina dostave); filter prepovedanih besed (odločitve lastnika). | `medij/govor/model.py:35,39-42,516,537`, `medij/govor/orodje.py:25-39`, `medij/govor/filter.py:99`, `medij/govor/potrditev.py:26` | imena spremenljivk v `model.yaml`; seznami iz `vrste.yaml` (T6) | MOD-06, 07, 13, 20..23, 26 |
| **T12 Govorni sloj in namestitev** | Klic pride samo prek brskalnika (WebSocket `wss://vecer-poc.meniji.si/ws` prek Cloudflare tunela); telefonije (SIP, Twilio, Asterisk) ni. Domena, tunel, ime storitve `vecer-poc`, uporabnik `vecer`, `/srv/vecer`, Janine storitve kot predpogoj, dovoljena izvora (Lovable). STT/TTS: Soniox, glas `Rui`, model `tts-rt-v2`, hitrost 1,1; en hkraten klic. Skripte za prvo namestitev ni. | `deploy/vecer-poc.service`, `deploy/namesti-k5.sh:12,23`, `deploy/cloudflared-vecer.yml:2`, `medij/zvok/javni.py:13`, `medij/zvok/soniox.py:30,32,141`, `medij/zvok/streznik.py:33` | ponudnik, glas, domena, poti v env/yaml; predloga namestitve po hiši; telefonija je nova koda (faza 11 načrtovana) | GSL-01..13, 17..20 |

Opombe:
- **Nespremenljive predpostavke domene** (niso VEZ, a veljajo): časopis izhaja po dnevih, reklamacija je o dostavi, klicatelj govori slovensko; zaprti seznami potrditev in zanikanj (`potrditev.py`), slovnica povzetka (`povzetek.py`, `_SE_DNI` do 8) so samo slovenski (`vecer-povzetek-zapis.md`, Česa ne zna). Za hišo z drugim jezikom ni poti brez kode.
- **Test in kanon**: 2950 testov in 807 datotek v `kanon/` nosijo Večerova besedila, kraje in odločitve (npr. 762 scenarijev po popisu MOD). Nova hiša mora ta korpus pripraviti sama; `tests/pomozno.py` naloži Večerovo nastavitev.
- **Mrtva koda** v izvozu (samo testi jo kličejo): `medij/prenos/zozenje.py` razen `mehka_podobnost`, `medij/prenos/crkovanje.py`, povzetkovni del `dwh.py:158-305`, `zapis.RESITVE` z `ni_na_voljo`, `Dan` in `Stanje.dnevi`, `SledilnikZapisa`. Ne štejejo kot zmožnost; pri prevzemu jih odstrani.

## 4. Top 5 ovir

1. **Pravila rešitve in odpisa niso podatek** (T2, T3, T4). To je poslovno pravilo Večera (nadomestni izvod samo danes, odpis samo za pretekle dneve, meja tednov, pošta do 19. ure) in je vtkano v `vrstni_red.py:562-593`, `obrat.py:149`, `ohlapni_datum.py:28`. Samo dve stvari sta nastavljivi: `ure.rok_poste` in `poskusi.resitev_razjasnitve`. Hiša brez odpisa ali z drugim pragom potrebuje spremembo kode.
2. **Vrste težave, šifrant in shema zapisa so zaprti** (T6). 13 vrst, 26 šifer DWH, zaprta shema in isti seznami v promptih in orodju. Nova vrsta posega istočasno v kodo, poziv in teste; neznana vrsta se ne sprejme (`obrat.py:364`: vrsta se zapiše samo, če je v `VELJAVNE_VRSTE`).
3. **Ni ciljne evidence in ni uvoza baze naročnikov** (T7, T10). Zapis konča v lokalnem SQLite brez konektorja; baza se gradi samo iz Večerovih CSV. Obe sta potrebni za produkcijsko hišo, nobena ni nastavitev.
4. **Besedila, pozivi in poti so vezani na Večer** (T1, T8, T9). Pot `mediji/vecer/` na 6 mestih, 12 besedil z Večerovimi vsebinami, 8 vrstic v pozivih, stavki v `.py`, pričakovani nabor 73 ID-jev v kodi. Vse to je rešljivo s podatki, a ne brez sprememb kode.
5. **Klic pride samo prek brskalnika in namestitev je privezana na Večerov strežnik** (T12). Telefonije ni, domena in poti na strežniku so vtkane, ponudnik govora je izbran v kodi.

Naslednje za njimi: koledar izhajanja in delovnik (T5), ker koda predpostavlja izvod vsak dan.

## 5. Nepreverjeno in omejitve

- Popisi so branje kode (podagenti, nato moj pregled): poti, številke vrstic in imena testov so preverjeni s `preveri_vecer_popise.py` (vse obstajajo); za vseh 171 VEZ vrstic sem izpisal prvi dve citirani vrstici kode in jih pregledal glede na trditev (vzorec, ne popolna preverba vsake trditve). Telesa testov so bila brana le delno; »test obstaja« ni dokaz, da test res preverja opisano vedenje.
- Testi niso bili zagnani (po nalogi; v repozitoriju so tudi živi testi s pravim modelom, ki se vklopijo z `VECER_ZIVI_TESTI=1`).
- Datoteke `deploy/*.env` in ključi niso bili brani; samo imena spremenljivk.
- Veja `paket-1-javni-vhod` ni vključena: omejitve javnega vhoda (velikost sporočila, število napačnih sporočil, 12 minut zvoka) in obravnava nepričakovane napake obrata niso v tem popisu.
