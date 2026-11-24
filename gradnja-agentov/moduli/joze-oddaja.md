# Jože: oddaja (povzetek, dvojna potrditev, listek po e-pošti, neznan izid)

- **Poti** (relativno na koren Jožeta): `jedro/listek_backend.py` (423 vrstic: zapora oddaje, listek, opozorilo), `jedro/moduli/joze_listek.py` (izris listka), `jedro/summary.py` (vprašanja za oddajo), `jedro/klic.py` (`_potrdi`, vprašanje za oddajo, 929-1009), `oddaja/listek_eposta.py` (SMTP), `oddaja/neoddano.py` (trajni zapis), `govor/klic_jj.py` (sestava klica za prevzem), `govor/app.py:1222` (preverba mape ob zagonu).
- **Izvor**: Jože `abcfdc4` (veja `joze-sproti`), pregledano 2026-11-24, samo branje čistega izvoza.
- **Kaj je živo**: `govor/klic_jj.py::naredi_klic_prevzem` (vrstice 100-114) sestavi `Klic` nad `ListekBackend` s transportom `TransportListek` (Zoho SMTP), trajnim zapisom `TrajniZapis` in opozorilom po istem transportu. Nastavitev: `nastavitve/restavracija.yaml` (`listek`, `spremljanje`, `besedila`, `placilo`, `embalaza_doplacilo`).
- **Mrtvo za Jožeta** (ni zmožnost, samo uvoženo): `jedro/jj_backend.py` (Janin rezervacijski backend, Venue), `govor/jj_transport.py` (HTTP do Tovarne idej), `klic_jj.naredi_klic` in `klic_jj.restavracija()` (pot `restavracije/jack-and-joe/restavracija.yaml` v tem repozitoriju ne obstaja), rezervacijski del `jedro/summary.py` (`summary_from_prepared`, `correction_summary`, `branje_podatkov`: »Vaša rezervacija je …«). `klic_jj.py:18,23` jih uvozi ob zagonu (potrebna `aiohttp`), zato jih ni mogoče samo pozabiti.

## Zmožnosti

| ID | Kaj natančno počne | Predpostavke | Podatki/nastavitve, ki jih bere | Test |
|---|---|---|---|---|
| ODD-01 | Povzetek naročila sestavi koda, ne model: »Dvakrat Cheese, medium, enkrat Coca-Cola. Opomba naročila: …. Danes ob dvajsetih, na ime Jaka Novak. Je to pravilno?« Števila z besedami, telefon se ne bere. | Naročilo, ura in ime so zbrani | `moduli.prevzem.izgovor_ure`, `listek.vrstni_red` (samo preverjanje polj) | `tests/test_joze_koraki_4_7.py::test_cela_pot_3_4_5_6_7_do_listka_natanko_enkrat` |
| ODD-02 | Dvojna potrditev: koda vpraša »Vam lahko zdaj preberem povzetek?«, prebere povzetek (»Je to pravilno?«), po prvem »ja« vpraša »Lahko naročilo oddam?« (ali »Naj naročilo oddam?«, »Je v redu, da naročilo oddam?«, vedno različna od zadnje); oddaja šele po drugem »ja«. | Gost je vprašanje slišal do konca | `govor.povzetek_vprasanje` (prvo vprašanje); vprašanje za oddajo je v kodi (`summary.py:11`) | `tests/govor/test_zapornica_k14.py::test_z6_dvojna_potrditev_oddaja_sele_po_drugem_ja` |
| ODD-03 | Oddaja je mogoča samo po slišanem povzetku iste revizije: gostov »ja« pred koncem povzetka ali na staro revizijo ne odda in ne pošlje ničesar. | `potrdi_predstavitev` javi govor | Brez | `tests/test_joze_koraki_4_7.py::test_potrditev_brez_slisanega_povzetka_ne_odda` |
| ODD-04 | Prekinjen povzetek se ne šteje: gost prekine bralni stavek, koda izgovori nov povzetek z novim ID-jem; poznejši dogodki starega ne odklenejo oddaje. | Brez | Brez | `tests/test_prevzem_listek.py::test_interruption_replay_no_transport_and_late_events` |
| ODD-05 | Kratek popravek po slišanem povzetku (do 3 spremembe): »Popravil sem: danes ob osemnajstih. Je zdaj vse pravilno?« Samo spremenjene postavke in ime skupaj; pri več kot treh spremembah ali pri neznani razliki cel povzetek. | Prejšnji povzetek je bil slišan do konca | `besedila.popravek_povzetka` (»Popravil sem: «) | `tests/test_joze_koraki_4_7.py::test_popravek_ure_po_slisanem_povzetku_kratek_popravil_sem` |
| ODD-06 | Pred oddajo se vse preveri znova: naročilo brez odprte izbire, veljavna ura (čas priprave od prve veljavne ure), ime in priimek. Če je ura medtem potekla, potrditev ne odda listka in koda izgovori nov povzetek. | `zdaj()` iz gostitelja | `moduli.prevzem.*` | `tests/test_prevzem_listek.py::test_invalid_time_and_clock_advance_rechecked_at_submit` |
| ODD-07 | Enkratna oddaja: `_submitted` se postavi pred pošiljanjem; ključ oddaje je `sha256('listek:' + klic_id)`; ponovljen `potrdi` vrne shranjeni rezultat, drugi listek se ne pošlje. | Brez | Brez | `tests/govor/test_listek_eposta.py::test_dvojna_potrditev_da_en_mail` |
| ODD-08 | Uspeh je samo izrecen odgovor `202 accepted` z `receipt_id`; vsak drug odgovor (npr. HTTP 502) je neuspeh in sproži opozorilo. Uspeh ni dokaz dostave. | Transport vrne (status, bajti JSON) | Brez | `tests/test_joze_koraki_4_7.py::test_zavrnjen_listek_http_502_tudi_opozori` |
| ODD-09 | Neznan izid je terminalen: timeout, napaka povezave, `TypeError`/`ValueError` ali preklic med oddajo postavijo `outcome_unknown`, klic gre v `konec_neznan`; gost sliši »Oddaje naročila ne morem zanesljivo potrditi. Da ne bi prišlo do dvojnega naročila, preverite pri osebju …« in klic se konča. Brez ponovne oddaje, tudi po obnovi seje. | Brez | `besedila.zakljucek_neznan`, `besedila.neznan_izid` | `tests/test_prevzem_listek.py::test_unknown_and_cancellation_are_terminal_across_restore` |
| ODD-10 | Zaključek po uspešni oddaji izgovori koda (ne model): »Vaše naročilo je bilo posredovano ekipi, ob prevzemu samo povejte vaše ime in priimek. … Hvala in lep dan.« (isto besedilo z e-pošto in brez nje). Klic se konča po koncu govora. | Brez | `besedila.zakljucek_oddano`, `zakljucek_oddano_brez_eposte` | `tests/govor/test_jozef_koraki_4_7.py::test_vprasanje_nato_povzetek_iz_kode_nato_potrditev_odda_listek_in_zakljucek` |
| ODD-11 | Neuspela oddaja (npr. HTTP 502, zavrnitev strežnika): gost sliši isto kot pri neznanem izidu (`zakljucek_neznan`: »… preverite pri osebju.«), listek se ne ponovi, ekipa dobi opozorilo (ODD-28). Besedilo `besedila.napaka_backenda` (»Naročila trenutno ne morem oddati. …«) je v nastavitvi, a ga `ListekBackend` ne sproži, ker ne vrača `http_status` 400/401 (nepreverjeno, da pot `konec_napaka` pri Jožetu res ni dosegljiva). | Brez | `besedila.zakljucek_neznan` | `tests/govor/test_jozef_koraki_4_7.py::test_neuspela_oddaja_gost_sliši_preverite_pri_osebju_opozorilo_nam_listek_se_ne_ponovi` |
| ODD-12 | Prejemniki listka: `listek.kuhinja` (seznam; prvi gre v `To`, ostali v `Cc`), `listek.kopija` v `Cc` samo, če je `kuhinja` neprazna; če je `kuhinja` prazna, gre listek samo na `listek.prejemnik` (testni naslov). Neveljaven naslov ali znak za nov red je izjema ob zagonu. | Naslovi v obliki a@b.c | `listek.prejemnik`, `kuhinja`, `kopija` | `tests/test_joze_koraki_4_7.py::test_naslov_kuhinje_s_kopijo_nam` |
| ODD-13 | Delna zavrnitev prejemnikov (SMTP sprejme, a zavrne enega): če je zavrnjen kateri naslov kuhinje, je to neznan izid + opozorilo; če samo naša kopija, je uspeh z opozorilom v dnevniku. Neberljiv seznam zavrnjenih šteje za zavrnjeno kuhinjo. | Brez | Brez | `tests/govor/test_listek_eposta.py::test_kuhinja_zavrnjena_kopija_sprejeta_je_neznan_izid_in_opozorilo` |
| ODD-14 | Besedilo listka: ime restavracije, »Naročilo za prevzem«, »Prevzem: 2026-10-21 20:00«, »Gost: Jaka Novak«, »Telefon: …«, nato vrstice jedi (»1. 1× CHEESE (medium)«, »   + hrustljava slanina«), opomba, plačilo. | `nova_pogodba` naročilo | `ime_za_gosta` | `tests/test_joze_koraki_4_7.py::test_cela_pot_3_4_5_6_7_do_listka_natanko_enkrat` |
| ODD-15 | Združevanje enakih kosov v listku: dva enaka Cheese z istimi dodatki sta »2× CHEESE (medium)«; dodatki so urejeni, zato vrstni red naštevanja ne loči kosov; izvoz ne spremeni stanja seje. Samostojna priloga: »1× DOMAČ POMFRI (samostojno)«. | Brez | Brez | `tests/test_joze_priloge_listek.py::test_listek_primeri_a_b_c_d` |
| ODD-16 | Tehtana jed na listku: »1× 300 g RIBEYE«, vrstica »TEHTANO: Ekipa pokliče nazaj in uskladi količino.« in »Količina po dogovoru.«, če gost teže ni povedal. | Katalog `enota` 100 g ali 1 g | `moduli.narocilo.tehtano_obvestilo`, `tehtano_privzeta_opomba`, `tehtano_privzeto_g` | `tests/test_prevzem_korak1.py::test_default_weight_notes_restore_and_receipt` |
| ODD-17 | Privzeta pečenost na listku: če je gost ni povedal, a je bil vprašan, listek nosi »Privzeta pečenost: srednje«. | Skupina z imenom `pečenost` | `moduli.narocilo.pecenost_privzeta` | `tests/test_pickup_decisions.py::test_default_doneness_requires_asked_question_and_is_on_receipt` |
| ODD-18 | Alergijsko obvestilo: če opomba, dobesedni stavki ali opomba postavke vsebujejo `alerg`, `intoleranc` ali `celiak`, listek dobi vrstico »ALERGIJA / INTOLERANCA: ekipa naj pokliče gosta; sestave in varnosti jedi ne potrjujemo.« | Brez | `listek.alergija.vzorci`, `listek.alergija.obvestilo` | `tests/test_prevzem_korak1.py::test_weight_allergy_receipt_and_no_alcohol_products` |
| ODD-19 | Gostove dobesedne besede ob opombi (npr. »brez bazilike«) pridejo na listek, tudi če model opombo zapiše drugače ali jo kos odnese; brez podvajanja, če je že pokrito. Vrstica »Opomba gosta (dobesedno): »…««. | Brez | Brez | `tests/test_joze_dobesedno.py::test_sim13_ponovitev_1_bazilika_odnesena_s_kosom_je_na_listku` |
| ODD-20 | Plačilo in embalaža na listku: »Plačilo: ob prevzemu« in »Brez doplačila za embalažo.« | Podatka sta v nastavitvi | `placilo`, `embalaza_doplacilo` (samo vrednost 0 sproži vrstico) | `tests/test_pickup_decisions.py::test_default_doneness_requires_asked_question_and_is_on_receipt` |
| ODD-21 | E-poštni transport: Zoho SMTP `smtp.zoho.eu:587`, STARTTLS pred prijavo, prijava iz okolja, en mail na oddajo, skupna omejitev 20 s (povezava, prijava, pošiljanje). | `ZOHO_SMTP_USER` in `ZOHO_SMTP_PASS` v okolju | Okolje (ne yaml) | `tests/govor/test_listek_eposta.py::test_povezava_je_starttls_pred_prijavo_na_zoho` |
| ODD-22 | Zadeva in glave: »Naročilo za prevzem – 20:00 – Jaka Novak«; ura in ime sta očiščena znakov za nov red in krajša od 60 znakov, zato podatek gosta ne more ustvariti nove glave (`Bcc`). | Brez | Brez | `tests/govor/test_listek_eposta.py::test_podatki_gosta_ne_morejo_v_nove_glave` |
| ODD-23 | Transport nikoli ne ponovi: ponovljen `submission_key` v istem procesu vrne 409 `ze_poslano`; po napaki ni ponovitve. | Isti proces | Brez | `tests/govor/test_listek_eposta.py::test_po_napaki_ni_ponovitve` |
| ODD-24 | Napake SMTP: zavrnjena prijava = 401, zavrnjen naslov ali sporočilo = 502, timeout = `TimeoutError`, napake povezave = `OSError` brez besedila strežnika; poverilnice niso v `repr`, dnevniku ali izjemi. | Brez | Brez | `tests/govor/test_listek_eposta.py::test_skrivnosti_niso_v_repr_ne_v_dnevniku` |
| ODD-25 | Manjkajoče poverilnice (`ZOHO_SMTP_*`) pri sestavi klica = izjema; `app.start_flows` jo ujame in klic teče naprej brez orodij (glasno v dnevniku). | Brez | Okolje | `tests/govor/test_listek_eposta.py::test_poverilnice_iz_okolja_in_manjkajoce_so_napaka` |
| ODD-26 | Trajni zapis neoddanega listka: ob neuspehu ali neznanem izidu se listek zapiše v mapo (privzeto `/var/lib/joze/neoddano`, 0700, atomarno, `fsync`, največ en zapis na klic, ime datoteke iz varnega ID-ja klica) še preden gre karkoli po pošti. Zapis je samo kopija za osebje, ne ponovna oddaja. | Mapa je absolutna in last procesa | Okolje `JOZE_UNSUBMITTED_DIR` | `tests/govor/test_listek_neoddano.py::test_posta_ob_oddaji_pade_listek_je_v_mapi_neoddanih` |
| ODD-27 | Okvara diska ne podre klica: neuspešen zapis je vrstica `JOZE_DURABLE_WRITE_FAILED` brez vsebine listka. | Brez | Brez | `tests/govor/test_listek_neoddano.py::test_okvara_diska_ne_podre_klica_in_je_v_dnevniku_brez_vsebine_listka` |
| ODD-28 | Opozorilo ekipi po e-pošti ob neuspehu ali neznanem izidu: zadeva »OPOZORILO: naročilo za prevzem ni oddano – 20:00 – Jaka Novak«, v telesu razlog, klic, telefon in celoten listek; največ eno na klic, v ozadju (15 s), napaka opozorila ne vpliva na klic. Samo ob `spremljanje.opozorilo_eposta: da`. | Transport za opozorilo | `listek.opozorilo_na`, `spremljanje.opozorilo_eposta` | `tests/test_joze_koraki_4_7.py::test_neuspela_oddaja_opozorilo_nam_listek_se_ne_ponovi` |
| ODD-29 | Potrditev ni uspela (gost pritrdil, a oddaja ni mogoča): koda opozori ekipo in zapiše listek, ne odda. | Brez | Isto kot ODD-28 | `tests/govor/test_listek_neoddano.py::test_potrditev_ni_uspela_opozori_neoddano_zapise_listek_brez_oddaje` |
| ODD-30 | Preklic klica med oddajo: listek in opozorilo se zapišeta, preklic gre naprej (`CancelledError` ni pogoltnjen); konec klica počaka na opozorilo (do 15 s). | Brez | Brez | `tests/govor/test_listek_neoddano.py::test_preklic_med_oddajo_zapise_listek_in_preklic_gre_naprej` |
| ODD-31 | Preverba mape neoddanih ob zagonu storitve (zapis poskusne datoteke s `fsync`); neuspeh ni usoden: dnevnik `JOZE_DURABLE_STORE_UNUSABLE`, klici se sprejemajo naprej. | Brez | Okolje | `tests/test_joze_neoddano.py::test_atomaren_zaseben_zapis_in_preverba` |
| ODD-32 | Obnova seje (snapshot/restore) backenda: predstavljen povzetek, osnutek, uspeh in sidro ure preživijo obnovo; obnova na drug klic ali drugega prejemnika je napaka. | Brez | Brez | `tests/test_prevzem_listek.py::test_snapshot_restores_presentation_and_success` |
| ODD-33 | Sestava klica za prevzem: `Klic` nad `ListekBackend`, nastavitev iz `nastavitve/restavracija.yaml` (naložena enkrat na proces), vprašanja iz kode vedno vklopljena, `zdaj()` = Europe/Ljubljana. | Brez | `nastavitve/restavracija.yaml` | `tests/govor/test_klic_prevzem.py::test_klic_je_nad_listek_backendom_z_vprasanji_iz_kode` |
| ODD-34 | Modul `prevzem` zahteva backend z oznako `listek`; z rezervacijskim backendom je `ValueError` ob sestavi klica. | Brez | Brez | ni testa |
| ODD-35 | `listek.vrstni_red` mora vsebovati natanko vsa polja razen telefona (sicer izjema ob zagonu); polje samo določa, katera polja so v povzetku, besedilo povzetka za Jožeta sestavi koda po fiksnem vrstnem redu. | Brez | `listek.vrstni_red` | ni testa |

## Česa ne zna

- Gostu po klicu ne pošlje nič (ne SMS, ne e-pošte); `kontakt.eposta: izklopljena`. Zaključek reče samo, da je naročilo posredovano ekipi.
- Ne ve, ali je listek dospel: uspeh je »strežnik je sporočilo sprejel«, ne dostava ali branje (komentar `listek_backend.py:4`).
- Ne ponovi oddaje po neznanem izidu (zavestno: dvojno naročilo je hujše od izgubljenega); osebje odloči po opozorilu in zapisu.
- Nima naslova kuhinje: `listek.kuhinja: []`, listek gre samo na testni naslov Megaphone (`andrej@megaphoneagency.eu`) (`nastavitve/restavracija.yaml:127-134`, `TODO kuhinja`).
- Ne podpira oddaje po HTTP (Venue) ali drugega transporta kot SMTP (Janin `jj_backend.py` je v repozitoriju, a za Jožeta mrtev).
- Ne podpira več prejemnikov z različnimi vsebinami (en listek, vsi prejemniki isto).
- Brez priponke, PDF ali tiskalnika.
- Opozorilo ekipi odpove, če je pokvarjen sam poštni strežnik; zato je trajni zapis na disku narejen prej in neodvisno.
- Ura: oddaja je mogoča samo za današnji dan (glej `joze-prevzem.md`).

## Kaj je vezano na J&J v KODI

| ID | path:vrstica | Kaj je trdo | Kategorija | Predlog (kam v podatke) |
|---|---|---|---|---|
| VEZ-ODD-01 | `jedro/listek_backend.py:277` | Glava in oznake listka: »Naročilo za prevzem«, »Prevzem:«, »Gost:«, »Telefon:«, »E-pošta:« (277-280) | BESEDILO | `listek.predloga` (oznake) |
| VEZ-ODD-02 | `jedro/listek_backend.py:353` | Zadeva e-pošte »Naročilo za prevzem« (tudi `oddaja/listek_eposta.py:47`) | BESEDILO | `listek.zadeva` |
| VEZ-ODD-03 | `jedro/listek_backend.py:299` | »Opomba naročila: « (tudi 148, 178), »Opomba gosta (dobesedno): « (301) | BESEDILO | `listek.predloga` |
| VEZ-ODD-04 | `jedro/listek_backend.py:306` | Vrstici »Plačilo: …« in »Brez doplačila za embalažo.« (309): J&J pravilo plačila ob prevzemu in brez doplačila; stavek je v kodi, pogoj je `embalaza_doplacilo == 0` | PRAVILO | `listek.vrstice_na_koncu` (seznam besedil) |
| VEZ-ODD-05 | `jedro/listek_backend.py:49` | `names != {'prevzem', 'narocilo', 'kontakt'}`: backend dovoli natanko te tri module | PRAVILO | Dovoli poljuben nabor, ki ima polja iz `vrstni_red` |
| VEZ-ODD-06 | `jedro/listek_backend.py:237` | `NAJVEC_SPREMEMB_JOZE = 3` (kratek popravek do tri spremembe, Chebo 16. 11.) | ŠTEVILO | `pravila.najvec_sprememb_kratkega_popravka` |
| VEZ-ODD-07 | `jedro/listek_backend.py:412` | Rok opozorila 15,0 s (in 419 `pocakaj_opozorila(rok_s=15.0)`); `oddaja/listek_eposta.py:30` `ROK_S = 20.0`, `:32` `MAX_IME = 60` | ŠTEVILO | `listek.roki.*` |
| VEZ-ODD-08 | `jedro/listek_backend.py:402` | Besedilo opozorila ekipi (»Naročila za prevzem ni bilo mogoče oddati kuhinji …«) in zadeva »OPOZORILO: naročilo za prevzem ni oddano« (405) | BESEDILO | `listek.opozorilo.besedilo`, `zadeva` |
| VEZ-ODD-09 | `jedro/moduli/joze_listek.py:48` | Skupina se išče po imenu `'pečenost'`; vrstice »(samostojno)« (54), »× « in » g « (55-58), »TEHTANO: « (72), »Privzeta pečenost: « (76), »Opomba: « (78), »   + « (64-70) | PRAVILO | Polje skupine `vloga: pecenost` v katalogu; oznake v `listek.predloga` |
| VEZ-ODD-10 | `jedro/moduli/joze_listek.py:72` | Privzeta besedila v kodi: »Ekipa pokliče nazaj in uskladi količino.« (72), »Količina po dogovoru.« (74), `'srednje'` (76; tudi `joze_spremembe.py:539,516` 300 g) | BESEDILO | Brez privzetih v kodi: ključi obvezni (že so v nastavitvi) |
| VEZ-ODD-11 | `jedro/summary.py:11` | `VPRASANJA_ODDAJE_NAROCILO`: tri različice »Lahko naročilo oddam?« (vrstice 11, 13: `VPRASANJE_PO_POPRAVKU`) | BESEDILO | `govor.oddaja_vprasanje` |
| VEZ-ODD-12 | `jedro/listek_backend.py:181` | Končni stavek povzetka »Je to pravilno?« (181) in »Je zdaj vse pravilno?« (266) v kodi | BESEDILO | `govor.povzetek_konec`, `govor.popravek_konec` |
| VEZ-ODD-13 | `jedro/klic.py:91` | Privzeto besedilo orodja `potrdi` govori o »rezervaciji« (`Oddaj rezervacijo samo po jasni potrditvi…`); Jože ga prepiše z `besedila.opis_potrdi` | BESEDILO | Brez privzetega besedila (obvezen ključ) |
| VEZ-ODD-14 | `govor/profil.py:176` | `privzeta_besedila.zakljucek_oddano` in `zakljucek_oddano_brez_eposte` (vrstici 176-177): isto besedilo kot v nastavitvi (105-106), podvojeno, vključno z »Plačilo je ob prevzemu, brez doplačila za embalažo.« (zakljucek 184 `eposta_osebja`) | BESEDILO | Samo v nastavitvi; test `test_profil_okolje` primerja podvojena besedila |
| VEZ-ODD-15 | `oddaja/listek_eposta.py:28` | `smtp.zoho.eu`, vrata 587, imeni okolja `ZOHO_SMTP_USER`/`ZOHO_SMTP_PASS` (58-59) | NASLOV | `listek.smtp.gostitelj/vrata` in imena spremenljivk |
| VEZ-ODD-16 | `oddaja/neoddano.py:25` | Privzeta mapa `/var/lib/joze/neoddano`; tudi `govor/klic_jj.py:97` in `govor/app.py:59` (`/var/lib/joze/calls`), spremenljivki `JOZE_UNSUBMITTED_DIR`, `JOZE_CALLS_DIR` | NASLOV | Okolje `AGENT_NEODDANO_DIR` ali nastavitev |
| VEZ-ODD-17 | `govor/klic_jj.py:27` | `POT_NASTAVITVE_PREVZEM = nastavitve/restavracija.yaml`; mrtva pot `restavracije/jack-and-joe/restavracija.yaml` (26) | NASLOV | Pot kot parameter zagona |
| VEZ-ODD-18 | `govor/klic_jj.py:85` | Časovni pas `Europe/Ljubljana` (`ljubljanski_cas`) | ŠTEVILO | `casovni_pas` v nastavitvi |
| VEZ-ODD-19 | `govor/klic_jj.py:18` | Uvoz Janinega `JJBackend`, `TransportJJ` (Venue/Tovarna idej, `jj_transport.py:7,23`) in `restavracija()` ob zagonu Jožeta: mrtva pot, a vezana na Jana/J&J | IME-AGENTA | Odstrani iz prevzemnega agenta |
| VEZ-ODD-20 | `jedro/listek_backend.py:377` | Imena dogodkov `JOZE_SUBMISSION_UNKNOWN`, `JOZE_DURABLE_WRITE_FAILED` (385), `govor/app.py:1226` `JOZE_DURABLE_STORE_UNUSABLE` | IME-AGENTA | Samo poimenovanje |

## Povzetek

| Meritev | Število |
|---|---|
| Zmožnosti (ODD) | 35 |
| Brez testa (»ni testa«) | 2 (ODD-34, ODD-35) |
| VEZ vrstice skupaj | 20 |
| BESEDILO | 9 |
| ŠTEVILO | 3 |
| PRAVILO | 3 |
| IME-JEDI | 0 |
| NASLOV | 3 |
| IME-AGENTA | 2 |

Opombe:
- ODD-16, ODD-17, ODD-18, ODD-20 imajo test samo na stari poti `Narocilo` (Janin, `dodaj_postavko`); živa pot `NarociloJoze` ima za ODD-14 in ODD-15 test, vrstice »Plačilo«, »Brez doplačila« in alergija pa so v kodi skupne obema in niso preizkušene na živem naročilu.
- ODD-28: komentar v `listek_backend.py:396` omenja »v ozadju«, test preverja `await pocakaj_opozorila`; razmerje do klica ni preverjeno z živim SMTP.
- Testov nisem zagnal (samo `def test_` v izvozu); ali so zeleni, ni preverjeno.
