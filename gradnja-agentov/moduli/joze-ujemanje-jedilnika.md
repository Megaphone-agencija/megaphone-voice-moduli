# Jože: ujemanje gostove besede z jedilnikom (popis modula)

- **Viri (pod `Joze - glasovni agent`, vrstice za commit abcfdc4):** `jedro/moduli/ujemanje_jedilnika.py` (198), `govor/menu_spotter.py` (297), `scripts/meritev_ujemanja.py` (54); pot iskanja v `jedro/moduli/katalog_narocila.py` (`poisci` 652 do 872, `poisci_povsod` 444, `omembe` 236, `_mehko` 382, `ujema_izbiro` 310, `_koakola_ali_cola` 611) in `jedro/moduli/narocilo_joze.py` (`_poisci` 249, `_vrsta_iz_kataloga` 412, `_zozi_z_neznano` 371).
- **Stanje:** Jože `abcfdc4` (veja `joze-sproti`), datum popisa 2026-11-24. Samo branje kode in testov (čist izvoz `git archive abcfdc4`), nič ni bilo zagnano.
- **Kaj je živo:** isto kot v `joze-jedro-narocila.md`: `NarociloJoze` + `katalog-joze.yaml`. `menu_spotter.py` kliče `govor/flows.py` (varovalka po gostovi izjavi). Skripta `meritev_ujemanja.py` je razvojno orodje, ne teče v klicu.
- **Oblika testov:** `pot::ime_testa` brez imena razreda.
- **Kako deluje v eni povedi:** gostova fraza → žetoni (brez šumnikov, števila z besedo kot števke, ZDA = ameriški) → brez polnil → vsak žeton mora imeti ustreznico v imenu izdelka (enak ali v drugem sklonu = 1, tipkarska napaka = manj kot 1) → zmagovalec, če je za 0,15 boljši od drugega, sicer dvoumnost z imeni. Ujemanje s slabšo podobnostjo (manj kot 1) je vedno vprašanje, nikoli tiha potrditev.

## Zmožnosti

| ID | Kaj natančno počne | Predpostavke | Podatki/nastavitve, ki jih bere | Test |
|---|---|---|---|---|
| UJE-01 | Razbitje na žetone: »petinštirideset do šestdeset« postane `45 60`, »ZDA« in »ameriški« sta ista beseda, brez šumnikov, 60+ je »60 več«. Vsak izdelek se mora najti po imenu z jedilnika in v štirih govorjenih oblikah (kot na jedilniku, brez oklepaja, v tožilniku, »vašo ...«). | | katalog: `ime`, `sinonimi`, `govori` | `tests/test_joze_pokritost_jedilnika.py::test_vsak_izdelek_po_imenu_in_govorjenih_oblikah` |
| UJE-02 | Prag besede 0,80: ena zamenjana ali manjkajoča črka je `potrdi_ujemanje` (»Ste mislili ...?«) ali dvoumnost, nikoli tihi zapis napačnega izdelka (373 umetnih napak: 369 vprašanj, 4 tiho). | Prag je izmerjen na tem katalogu (VEZ-UJE-03) | koda: `PRAG_BESEDE` | `tests/test_joze_pokritost_jedilnika.py::test_ena_zamenjana_crka_nikoli_tiho_napacen_izdelek` |
| UJE-03 | Slaba podobnost je vprašanje: »tesarjevo solato« → vprašanje »cesarjeva solata«, ne zapis. | | | `tests/test_joze_pokritost_jedilnika.py::test_slaba_podobnost_je_vprasanje_nikoli_tiha_potrditev` |
| UJE-04 | Ocena izdelka = povprečje ocen žetonov × (0,5 + 0,5 × delež imena, ki ga je gost povedal): »ribeye« je ribeye, ne »Jack's Ribeye«; najboljši mora biti za 0,15 boljši, sicer dvoumnost z naštetimi kandidati. | | koda: `PRAG_RAZLIKE` | `tests/test_joze_pokritost_jedilnika.py::test_chebovi_primeri_iz_zivega_klica` |
| UJE-05 | Kratke besede (pod 5 črk: števke, »mali«) se ujemajo samo točno ali brez končnega samoglasnika (»mali« ~ »mala«, ne »malina«); sklon: skupen začetek in končnica iz seznama (»solato« ~ »solata«). | | koda: `MIN_DOLZINA`, `_KONCNICE` | `tests/test_joze_pokritost_jedilnika.py::test_kratke_besede_samo_natancno_in_cesar_ne_ujame_drugega` |
| UJE-06 | Polnila odpadejo (z, s, iz, do, dni, gram, govedina, meso, steak, ekstra ...), poleg njih še `nepomembne_besede` kataloga: »slovenski steak zorjen« ujame slovenski ribeye. | | koda: `POLNILA`; katalog: `nepomembne_besede` | `tests/test_joze_popravki_sim2.py::test_zorjen_v_gostovi_besedi_ne_prepreci_ujemanja_slovenskega` |
| UJE-07 | Tuje besede nimajo zadetka: sushi, carbonara, »ribeye z japonsko govedino« (29 od 30 v meritvi). | | | `tests/test_joze_pokritost_jedilnika.py::test_negativni_primeri_brez_zadetka` |
| UJE-08 | Pogosta slovenska beseda, ki jedilnika ni (»pa en tako«), ni kandidat za izdelek (`je_splosna_fraza`): brez »Ste rekli tako?«. Velja šele po `ni_najdeno`. | | koda: `SPLOSNE_BESEDE` | `tests/govor/test_klic_16_11_k8b.py::test_b5_tako_ni_izdelek_brez_vprasanja` |
| UJE-09 | Eksaktno iskanje po imenu, sopomenki, govorjenem imenu (`govori`) in kratkem imenu različice (`razlicica`); kolizija imen med različnimi osnovami je napaka kataloga. | | katalog: `ime`, `sinonimi`, `govori`, `razlicica` | `tests/test_joze_klic_9_11_2.py::test_govorjeno_ime_najde_izdelek` |
| UJE-10 | Kolizija sopomenk: deljene sopomenke variant so dovoljene, različne vrste jih ločijo. | | katalog: `sinonimi`, `osnova` | `tests/test_joze_katalog.py::test_deljene_sopomenke_variant_in_locene_vrste` |
| UJE-11 | Vrstni red besed ni razlika: »ribeye steak slovenski« = »slovenski ribeye steak«; vzdevek in različica v poljubnem vrstnem redu. | | katalog: `razlicica`, `sinonimi` | `tests/test_joze_popravki_sim2.py::test_vrstni_red_besed_ni_razlika` |
| UJE-12 | Skupne besede (»koktajl«, »burger«, »ameriški steak«): naštejejo kandidate skupine; `lastnosti_vzdevki` (»s slanino«) zožijo po opisu; `vrstni_red: kot_izdelki` določi vrstni red naštevanja. | | katalog: `skupine` (`izraz`, `sinonimi`, `skupine`, `izdelki`, `lastnosti`, `lastnosti_vzdevki`, `rod`, `mn_rod`) | `tests/test_joze_katalog.py::test_siroka_skupina_in_lastnosti` |
| UJE-13 | Splošna beseda in družina različic: »kola« → »Navadno ali Zero?«; izdelek z več različicami nastopi kot eno ime (osnova); gost z gramaturo misli izdelek sam. | | katalog: `splosne_besede`, `razlicice_s`, `osnova`, `ime_osnove` | `tests/test_joze_odlocitve_3_11.py::test_5_cola_brez_razlicice_vprasa_navadno_ali_zero` |
| UJE-14 | Iskanje čez cel katalog (`poisci_povsod`): jedi, priloge, pijače in dodatki so ena množica; vrsto določi najdena postavka (model vrsto pogosto napačno pošlje); točna ujemanja premagajo približna (»Margerita« je pica, ne koktajl »Margarita«). | | katalog: vse vrste | `tests/test_joze_iskanje_povsod.py::test_vsaka_priloga_in_vsak_dodatek_se_najde_brez_vrste` |
| UJE-15 | Napačna vrsta: beseda je na jedilniku, a pod drugo vrsto (»pomfri« kot jed) → `napacna_vrsta`; prilogo ob jedi pripne `dodaj`. | | | `tests/test_joze_katalog.py::test_vrste_in_brez_iskanja_po_sestavinah` |
| UJE-16 | Omemba je del daljšega imena druge postavke (»pa še cel pečen krompir« ni pomfri); najdaljše ujemanje zmaga (`_razsiri_omembe`). | | | `tests/test_joze_iskanje_povsod.py::test_omemba_je_del_daljsega_imena_druge_postavke` |
| UJE-17 | Jed in dodatek v popačenem imenu (»tesarjevo solato s popečenimi rakovimi repki«): `potrdi_ujemanje` s kanoničnim imenom jedi, dodatek se zapiše šele ko gost jed potrdi. | Samo en kandidat in dodatek natanko ustreza izbirnemu dodatku te jedi | katalog: `dodatki` jedi | `tests/test_joze_pokritost_jedilnika.py::test_tesarjevo_solato_je_vprasanje_cesarjeva_solata` |
| UJE-18 | Ujemanje izbir in dodatkov (`ujema_izbiro`): ime, `izgovor` in `sinonimi` izbire; »ekstra čebula« = čebula; približno ujemanje (ena črka) samo ob natanko enem dodatku jedi in vedno kot vprašanje. | | katalog: `skupine_dodatkov.*.izbire` (`ime`, `izgovor`, `sinonimi`) | `tests/test_joze_iskanje_povsod.py::test_priblizno_ujemanje_dodatka_je_vprasanje` |
| UJE-19 | Koakola ali Coca-Cola: »vašo Coca-Colo« je domača Koakola (namig vaša, domača, hišna); mešan stavek je dvoumnost, nikoli tiha Coca-Cola. | Katalog ima obe imeni `koakola` in `kokakola` | katalog: pijači Koakola in Coca-Cola | `tests/test_joze_pokritost_jedilnika.py::test_koakola_in_kokakola_se_ne_zamenjata_v_obe_smeri` |
| UJE-20 | Pijača z volumnom: »Römerquelle 0,75«, »tri deci«; velikostna beseda (»ta mali, 0,33«) je ob volumnu odveč; govorjena oblika ö/o je ista. | Volumen je v imenu (VEZ-NAR-10) | katalog: ime pijače | `tests/test_joze_sproti_jedro.py::test_velikostna_beseda_ob_volumnu_ne_prepreci_ujemanja` |
| UJE-21 | Smash burger: »s dvema pleskavicama« izbere varianto po številu pleskavic v imenu. | Ime vsebuje »2x smash pleskavica« | katalog: ime variante | `tests/test_joze_regresije_b.py::test_smash_pleskavice` |
| UJE-22 | Gramatura gosta razreši dvoumnost med različicami (po oznaki, sicer po tehtanih izdelkih). | | katalog: gramatura v imenu, `enota` | `tests/test_joze_razred_zapis.py::test_tehtana_jed_ostane_pri_svojih_gramih` |
| UJE-23 | Zožitev po lastnosti iz izjave: »ameriški tristo gramov, slovenski štiristo« → stavek s težo odloči; števke zožijo naprej (»45 do 60 dni«). | Različice iste osnove | katalog: `razlicica` | `tests/test_joze_popravki_sim3.py::test_drugi_del_izjave_slovenski_stiristo_zozi_na_slovenske` |
| UJE-24 | Postopno zoževanje: kar je koda pravkar naštela (`med`), zoži gostov odgovor; velja samo za eno naslednjo izjavo. | | (stanje `dvoumno_med`) | `tests/test_joze_popravki_sim2.py::test_zoževanje_velja_samo_za_naslednjo_izjavo` |
| UJE-25 | Približno ujemanje (tipkarska napaka v imenu družine, SequenceMatcher nad 0,85) je vedno `potrdi_ujemanje` z do 3 kandidati. | | koda: prag 0,85 | `tests/test_joze_katalog.py::test_priblizno_ujemanje_zahteva_potrditev` |
| UJE-26 | Sopomenke, ki jih gost reče, a jih katalog nima (iz ponovitev živih klicev), ujame podobnost. | | katalog: `sinonimi` | `tests/test_joze_iskanje_povsod.py::test_sopomenke_iz_ponovitev_jih_podobnost_ujame` |
| UJE-27 | `omembe`: v izjavi poišče imena izdelkov kot zaporedje besed (enaka beseda ali drug sklon), po klavzulah; dve do tri približne omembe (»fuse tea« ~ »Fuze Tea«) samo za vprašanje. | | katalog: imena izdelkov, `skupine` | `tests/govor/test_jozef_prepoznava.py::test_celo_ime_v_razlicnih_sklonih_in_stavkih` |
| UJE-28 | Spotter: kar gost z jedilnika pove, model pa ne pokliče (»Cockta in Coca-Cola«), koda zapiše sama z orodjem `dodaj`. | Model je končal obrat | katalog | `tests/govor/test_jozef_prepoznava.py::test_model_izpusti_pijaco_koda_jo_zapise_gost_ne_vpraša_za_zapisano` |
| UJE-29 | Spotter: kaj NI naročilo (zanikanje, vprašanje, čakanje, omemba za »s/z/iz«, »brez«, splošna beseda, beseda pod štiri črke) - raje zgreši, kot zapiše napačno. | | koda: `SPLOSNE_ENO`, `NEGACIJE_PRED`, `PREDLOGI_PRED` | `tests/govor/test_jozef_prepoznava.py::test_zanikanja_in_popravki_ne_sprozijo_zapisa` |
| UJE-30 | Spotter: splošne besede in skupine niso naročilo (»burgerje«, »solato«, »pijačo«); samo koktajl in špric sta. | | koda: `SKUPINE_NAROCILO` | `tests/govor/test_jozef_prepoznava.py::test_splosne_besede_in_skupine_niso_naroceno` |
| UJE-31 | Spotter dodatki: »pa še eno omako iz jurčkov zraven« zapiše dodatek, če gost pove celo ime, ime ni dvoumno in je dodatek neobvezen (omake iz obvezne izbire vedno vpraša koda). | | katalog: `dodatki`, `skupine_dodatkov` | `tests/govor/test_jozef_prepoznava.py::test_z_omako_po_jedi_je_naroceno_dodatek_p6` |
| UJE-32 | Spotter ne podvaja: izdelek, ki je že v naročilu (katera koli različica iste osnove), v čakalni vrsti ali ga je kdo poklical pod katerim koli imenom, se ne zapiše. | | | `tests/govor/test_jozef_prepoznava.py::test_nikoli_ne_podvoji_kar_je_model_zapisal_tudi_pod_drugim_imenom` |
| UJE-33 | Spotter: priloga, ki je že del naročene jedi (`vkljuceno`, ime), ni samostojna priloga (»perutničke s chipsom«). | | katalog: `vkljuceno` | `tests/govor/test_jozef_prepoznava.py::test_p1_perutnicke_s_chipsom_v_imenu_chips_ni_se_samostojna_priloga` |
| UJE-34 | Spotter: Coca-Cola in Koakola sta ena družina (Soniox ju meša): edina varna pot je vprašanje. | Isto kot UJE-19 | katalog | `tests/govor/test_jozef_prepoznava.py::test_vasa_coca_cola_je_koakola_varovalka_ne_zapise_coca_cole` |
| UJE-35 | Spotter: približna omemba gre v vrsto za vprašanje, nikoli tiho. | | | `tests/govor/test_jozef_prepoznava.py::test_priblizna_omemba_gre_v_vrsto_za_vprasanje_nikoli_tiho` |
| UJE-36 | Spotter: izjava, ki je odgovor na vprašanje, ki ga je koda zastavila v prejšnji izjavi, ne išče dodatkov. | Stanje `izbire_stanje` iz govora | | `tests/govor/test_jozef_prepoznava.py::test_odgovor_na_vprasanje_kode_je_znak_iz_izbire_stanje` |
| UJE-37 | Opomba, ki je samo dodatek z jedilnika (»omaka iz jurčkov«), se zapiše kot dodatek in ne kot opomba (ne podvoji). | | katalog: imena dodatkov | `tests/govor/test_k20.py::test_omaka_z_jedilnika_v_opombi_je_zapisana_kot_dodatek_in_opomba_ni_podvojena` |
| UJE-38 | Meritev pragov (`scripts/meritev_ujemanja.py`): na katalogu izmeri pokritost govorjenih oblik, 373 umetnih tipkarskih napak in tuje besede pri pragovih 0,70 do 0,90. | Zagon z `PYTHONPATH=tests:.`; uvozi `tests.test_joze_pokritost_jedilnika` | katalog (pot kot argument) | ni testa |

Odgovor gosta na vprašanje z možnostmi (`izbrana_moznost`), zoževanje neznane besede z razdaljo (`_zozi_z_neznano`) in podobne pijače (`_dopolni_podobne_pijace`) so opisani v `joze-jedro-narocila.md` (NAR-11, NAR-12, NAR-46, NAR-47), ker spreminjajo stanje naročila.

## Kaj je že podatek (OK)

Katalog `katalog-joze.yaml` (235 izdelkov z variantami; 516 sopomenk na osnovnih vpisih; 137 vpisov z `govori`; 26 s `razlicica`; 4 s `splosne_besede` in `razlicice_s`; skupine: 24) nosi: `sinonimi`, `govori`, `govori_osnove`, `razlicica`, `splosne_besede`, `razlicice_s`, `kratko`, `skupine` (z `izraz`, `sinonimi`, `lastnosti_vzdevki`), `nepomembne_besede`, `napacne_kombinacije`, `izgovor` in `sinonimi` pri izbirah, `prag_stevilo_namesto_seznama`. Za novo restavracijo je to glavno delo (podatki), koda se ne dotakne.

## Česa ne zna

- Ne zna ujemanja po zvoku (fonetika); razdalja je črkovna. Zapis Sonioxa (»Cocto«, »rebuy«) ujame samo z dodatnimi pravili (NAR-46, NAR-47).
- Seznami besed (polnila, splošne besede, sklonske končnice, števila z besedo do 500) so slovenski; za drug jezik je treba zamenjati kodo.
- Števila z besedo so omejena na nabor (1 do 10, 25, 30, 40, 45, 50, 60, 65, 70, 75, 80, 90, 100, 200 do 500): »dvanajst« ali »trinajst« v jedi ne postane 12 (nepreverjeno, branje kode: `_STEVILA`).
- Spotter ne razume zapletenih stavkov z več zanikanji (raje zgreši); izjava, v kateri gost isto jed naroči dvakrat v različnih izjavah, dobi drugi kos samo prek modela (znana omejitev v glavi `menu_spotter.py`).
- Pragovi veljajo za J&J katalog; za drug jedilnik jih je treba ponovno izmeriti (skripta obstaja).

## Kaj je vezano na J&J v KODI

| ID | Pot:vrstica | Kaj je trdo | Kategorija | Predlog |
|---|---|---|---|---|
| VEZ-UJE-01 | `jedro/moduli/ujemanje_jedilnika.py:37` | `POLNILA` vsebuje `steak`, `steaka`, `steaki`, `stejk`, `govedina`, `meso`: v J&J so to besede, ki jed opisujejo, a je ne razlikujejo. Katalog `nepomembne_besede` ima iste besede še enkrat (podvojeno). | IME-JEDI | samo `nepomembne_besede` v katalogu; koda ima samo slovnična polnila (z, s, iz, do) |
| VEZ-UJE-02 | `jedro/moduli/ujemanje_jedilnika.py:61` | `_ENAKE`: zda = usa = amerika = ameriški; slovenija = slovenski; vec = plus; bbq = barbecue; dollar = dolar; chips = cips; halloumi = halumi (J&J jedi in mesa). | IME-JEDI | katalog `enake_besede: [[...], ...]` (en seznam na restavracijo) |
| VEZ-UJE-03 | `jedro/moduli/ujemanje_jedilnika.py:28` | Pragovi `PRAG_BESEDE` 0,80, `PRAG_RAZLIKE` 0,15, `MIN_DOLZINA` 5 so izmerjeni na J&J katalogu (235 izdelkov) in zapisani v kodi. | ŠTEVILO | yaml `ujemanje: {prag_besede, prag_razlike, min_dolzina}` s privzetimi vrednostmi; po zamenjavi kataloga zagnati `meritev_ujemanja.py` |
| VEZ-UJE-04 | `jedro/moduli/ujemanje_jedilnika.py:54` | `_STEVILA`: števila z besedo samo iz nabora, ki ga rabijo J&J imena (petinštirideset, petinšestdeset ... za dneve zorenja, gramature 100 do 500). | ŠTEVILO | generirati iz `stevilo_z_besedo` (`joze_izgovor.py:14`, 1 do 999); jedro `stevilo_iz_besed` (`narocilo_joze.py:65`) to že dela |
| VEZ-UJE-05 | `jedro/moduli/ujemanje_jedilnika.py:90` | `bi bi kju` → `bbq`: napaka razpoznave za BBQ omako. | BESEDILO | `enake_besede` (VEZ-UJE-02) |
| VEZ-UJE-06 | `jedro/moduli/katalog_narocila.py:276` | Pragovi `.85` in `.75` za približne omembe (tudi 650, 793), SequenceMatcher; izmerjeni na J&J. | ŠTEVILO | yaml `ujemanje.prag_priblizne_omembe` |
| VEZ-UJE-07 | `jedro/moduli/katalog_narocila.py:611` | `_koakola_ali_cola`: ključa `koakola`, `kokakola`, besede `coca`, `cola`, `kola`, `koka`, namigi vaša, domača, hišna, stavek »Ste mislili našo domačo Koakolo ali Coca-Colo?« (639). Isto kot VEZ-NAR-13. | IME-JEDI | katalog: par `zamenljivo` z namigi in razlago |
| VEZ-UJE-08 | `govor/menu_spotter.py:29` | `SKUPINE_NAROCILO = koktajli, spritz`: imena skupin J&J kataloga, ki štejejo kot naročilo. | IME-JEDI | katalog: `skupine.*.naroci_skupno: true` |
| VEZ-UJE-09 | `govor/menu_spotter.py:34` | `SPLOSNE_ENO`: steak, burger, solata, pivo, pica, pizza, sladoled, juha, vino, kava, voda, torta, plošča ... (imena J&J skupin in splošne besede), ki same niso naročilo. | IME-JEDI | izpeljati iz `skupine.*.izraz`/`sinonimi` kataloga + kratek yaml seznam splošnih besed |
| VEZ-UJE-10 | `govor/menu_spotter.py:155` | `cola_druzina`: iskanje `katalog.imena["pijaca"]["koakola"]` in `["kokakola"]`; družina kol (Coca-Cola, Koakola). | IME-JEDI | isti podatek `zamenljivo` kot VEZ-UJE-07 |
| VEZ-UJE-11 | `scripts/meritev_ujemanja.py:14` | `TUJI` (sushi, hawaii pizza, fish and chips, ribeye z japonsko govedino, pepsi, fanta limon ...) in `TUJE_PIJACE` (17); privzeta pot `nastavitve/katalog-joze.yaml` (54). | IME-JEDI | `nastavitve/<restavracija>/meritev.yaml` s `tuje_besede` |
| VEZ-UJE-12 | `tests/test_joze_pokritost_jedilnika.py:25` | Testna pomožna funkcija `najden` ima poseben primer za osnovi `pijaca-coca-cola` in `pijaca-domace-gazirane` (ID-ji J&J pijač). | IME-JEDI | prebrati iz podatka `zamenljivo` (VEZ-UJE-07) |

Opombe:
- `KVALIFIKATORJI_DODATKA` (`katalog_narocila.py:64`), `VELIKOSTNE_BESEDE` (65), `SLOVNICNA`, `SPLOSNE_BESEDE`, `_KONCNICE` so slovenščina, ne J&J; po VEZ jih nisem štel.
- Poti iskanja po vrstah (`pic`, `pizz`, `burger` na `katalog_narocila.py:717`, smash regex 695 do 703, »okusi« 709, volumen 683) so v `joze-jedro-narocila.md` kot VEZ-NAR-10, 14, 15, 16.
- Mehanično iskanje (imena iz katalogov proti nizom v `ast` ter regexi): zadetki zunaj zgornjih so komentarji in docstringi (dollar chips, perutničke, omaka iz jurčkov so samo v komentarjih `menu_spotter.py`).

## Povzetek

| Kaj | Število |
|---|---|
| Zmožnosti (UJE) | 38 |
| Brez testa | 1 (UJE-38) |
| VEZ vrstic skupaj | 12 |
| VEZ IME-JEDI | 8 |
| VEZ PRAVILO | 0 |
| VEZ BESEDILO | 1 |
| VEZ ŠTEVILO | 3 |
| VEZ IME-AGENTA | 0 |
