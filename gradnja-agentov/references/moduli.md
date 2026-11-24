# Zemljevid modulov: funkcija × agent

Namen: pravilo »poišči obstoječ modul, preden pišeš novega« (Obsidian `Agent-Shared/PRAVILA.md`, »Ne izumljaj tople vode« → Moduli). Preberi pred fazo 02 (dodelitev nosilcev) in vsakič, ko pišeš nalogo za izvajalca (`predloga-naloge.md`).

**Stanje pregleda: 12. 11. 2026** (samo branje kode, nič ni bilo zagnano). Commiti: Jana `2fa56e7`, Jože `8d31c5e`, Fine dining `acce692`, Prebil `82e6e01` (veja `prebil-zajem`; `docs/checklist-prebil.md` in `docs/porocila/` še nista commitana), Večer main `60a75e1`, Večer veja faza-7 `8ed5317`.

## Kako brati

- Celica = poti do datotek, v obliki `OZNAKA:pot`. Prazna celica (`ni`) pomeni: v kodi tega agenta nisem našel ustreznika. Nič ni uganjeno; če nečesa nisem našel, tako piše.
- Oznake korenov (vse pod `/home/chebo/MAIOS/09-projects/`):
  `J` = `POC glasovni agent/megaphone-voice-poc` (Jana) · `JO` = `Joze - glasovni agent` · `FD` = `Fine dining - glasovni agent` · `PR` = `Prebil - glasovni agent` · `VE` = `Večer - glasovni agenti/vecer-hetzner-poc` (main) · `V7` = `Večer - glasovni agenti/vecer-hetzner-poc-faza7` (veja `faza-7`, še ni v main).
- Poti preverja `scripts/preveri_moduli.py` (vsaka pot v tej datoteki mora obstajati). Po vsaki spremembi zemljevida ga poženi.
- »Priporočen vir« je moja presoja iz branja kode in primerjave datotek (`diff`), ne iz živih klicev. Kjer je napisano »isto kot J«, je datoteka bajt za bajtom enaka Janini ali se razlikuje za nekaj vrstic.
- Pred prepisom: kopiraj iz **commita**, ne iz necommitanega dela (pravilo v `AGENTS.md` Prebila); novo kopijo zapiši v `IZVOR.json` ciljnega agenta (polja: `repository`, `commit`, `source_path`, `source_sha256`, `status` = prevzeta/prilagojena, `adaptation`).
- Večer main nima govornega sloja (Pipecat, zvok); ta je na veji `faza-7` (`V7`). Večer ima svoje jedro (`medij/`), ne Janinega `Klic`.

## Jedro (brez glasu in omrežja)

| Funkcija | Jana | Jože | Fine dining | Prebil | Večer | Priporočen vir za prepis |
|---|---|---|---|---|---|---|
| Stanje klica, revizije, posnetek in obnova | `J:jedro/klic.py` | `JO:jedro/klic.py` | `FD:jedro/klic.py` | `PR:jedro/klic.py` | `VE:medij/stanje.py`, `VE:medij/obrat.py` (drugačna zasnova) | Rezervacija: Jana. Zbiranje podatkov in oddaja brez termina: Prebil (rezervacijski del je že odstranjen, 752 proti 943 vrstic). |
| Pogodba modula (polja, orodja, rezultat, `Backend`) | `J:jedro/modul.py` | `JO:jedro/modul.py` (isto kot J) | `FD:jedro/modul.py` | `PR:jedro/modul.py` | `VE:medij/vmesniki.py` (drugačna) | Jana; opis: `J:docs/pogodba-modul.md` |
| Nalaganje nastavitve podjetja, preverjanje besedil | `J:jedro/nastavitev.py`, `J:vhodi/nastavitev.py` | `JO:jedro/nastavitev.py`, `JO:vhodi/nastavitev.py` | `FD:jedro/nalaganje.py`, `FD:jedro/nastavitev.py` | `PR:jedro/nastavitev.py`, `PR:nastavitve/nalaganje.py` | `VE:medij/nastavitev.py` | Fine dining (neizpolnjena predloga pade z naštetimi manjkajočimi mesti). Prebil, če mora zagon zavrniti manjkajoča odobrena besedila. |
| Kontakt: ime, priimek, e-pošta, telefon, normalizacija | `J:jedro/moduli/kontakt.py` | `JO:jedro/moduli/kontakt.py` (isto kot J) | `FD:jedro/moduli/kontakt.py` | `PR:jedro/moduli/kontakt.py` (2 vrstici razlike proti J) | ni | Jana |
| Termin: datum, ura, osebe, razumevanje ure (»ob štirih«), okno prihoda | `J:jedro/moduli/termin.py` | `JO:jedro/moduli/termin.py` (isto kot J) | `FD:jedro/moduli/termin.py` | ni (želeni čas ostane dobesedno: `PR:jedro/govorni_datum.py`) | `VE:medij/prenos/cas.py`, `VE:medij/dnevi.py`, `VE:medij/delovni_cas.py` | Jana. Čas v prosti besedi, ki se ne pretvarja v datum: Večer `cas.py`. |
| Naročilo iz kataloga: postavke, dodatki, količine, spremembe | `J:jedro/moduli/narocilo.py` | `JO:jedro/moduli/narocilo_joze.py`, `JO:jedro/moduli/katalog_narocila.py`, `JO:jedro/moduli/joze_spremembe.py` | `FD:jedro/moduli/degustacija.py` (meni, spremljava, alergije po gostu) | ni | ni | Jože (novejši od Janinega `narocilo.py`) |
| Prevzem: ura prevzema, listek | `J:jedro/moduli/prevzem.py` | `JO:jedro/moduli/prevzem.py`, `JO:govor/prevzem_govor.py` | ni | ni | ni | Jože |
| Prost opis težave, zapis dobesedno + oblikovan opis | ni | ni | ni | `PR:jedro/moduli/povprasevanje.py`, `PR:jedro/oblikovani_opis.py`, `PR:govor/prebil_opis.py` | ni | Prebil |
| Vrednost mora biti v gostovi izjavi (dokaz proti izmišljanju, M3) | ni | ni | ni | `PR:govor/prebil_opis.py` (ozek prenos iz Večera, SHA v glavi datoteke) | `VE:medij/govor/orodje.py` | Večer `orodje.py` (`v_izjavi`) |
| Tolerantno ujemanje z bazo ali katalogom | ni | `JO:jedro/moduli/ujemanje_jedilnika.py` (fraza gosta proti jedilniku) | ni | ni | `VE:medij/prenos/ujemanje.py`, `VE:medij/prenos/zozenje.py`, `VE:medij/imenik.py` (naročniki, pragovi izmerjeni na pravi bazi) | Imena in naslovi iz baze: Večer. Jedi iz kataloga: Jože. |
| Črkovanje: e-pošta nazaj po črkah, črkovan priimek ali ulica | `J:jedro/moduli/kontakt.py` (e-pošta) | `JO:jedro/moduli/kontakt.py` | `FD:jedro/moduli/kontakt.py` | `PR:jedro/moduli/kontakt.py` | `VE:medij/prenos/crkovanje.py` (priimek, ulica) | E-pošta: Jana. Črkovan priimek: Večer. |
| Povzetek sestavi koda, vprašanje za oddajo | `J:jedro/summary.py` | `JO:jedro/summary.py` (isto kot J) | `FD:jedro/summary.py` | `PR:jedro/summary.py` (81 vrstic, povpraševanje) | `VE:medij/povzetek.py` (iz shranjene revizije) | Jana; za povpraševanje Prebil |
| Zapora oddaje, enkratna oddaja, neznan izid | `J:jedro/jj_backend.py` | `JO:jedro/listek_backend.py` | `FD:jedro/tovarna_backend.py` | `PR:jedro/listek_backend.py` | `VE:medij/shranjevanje.py`, `VE:medij/zapis.py`, `VE:medij/dnevnik.py` (timeout = neznan izid, `operation_id`) | Oddaja po e-pošti: Prebil (neznan izid je terminalen, brez ponovitve). Oddaja prek HTTP: Fine dining (posplošen Janin). |
| Števec poskusov, meja ponovitev, napake oblike | `J:jedro/klic.py` (`nejasno`, `poskusi_na_podatek`) | `JO:jedro/klic.py` | `FD:jedro/klic.py` | `PR:jedro/klic.py` | `VE:medij/stevci.py` (en števec na podatek, ni ponastavitve) | Jana |
| Vrstni red vprašanj: naslednje vprašanje določi koda | `J:govor/pogovor/flows.py`, `J:govor/pogovor/profil.py` | `JO:govor/flows.py`, `JO:govor/profil.py` | `FD:govor/vprasanja.py`, `FD:govor/pogovor.py` | `PR:govor/flows.py`, `PR:govor/profil.py` | `VE:medij/vrstni_red.py` (čista funkcija: stanje v naslednja akcija) | Ni primerjano, kateri je boljši. Za Pipecat Flows: Jana. Kot vzorec ene tabele in čiste funkcije: Večer. |
| Stalni stavki iz kode, besedila ločena od prompta | `J:restavracije/jack-and-joe/restavracija.yaml` | `JO:nastavitve/restavracija.yaml` | `FD:nastavitve/gric/restavracija.yaml`, `FD:jedro/spol.py` (spol govorca) | `PR:prompti/besedila.yaml`, `PR:prompti/profil.yaml` | `VE:mediji/vecer/besedila.yaml`, `VE:medij/besedila.py`, `VE:tests/test_besedila_cl.py` (besedila proti CL) | Večer (vsako besedilo ima ID iz CL, test jih primerja s CL). Pipecat profil: Prebil. |

## Govorni sloj (Pipecat, Asterisk, Soniox)

| Funkcija | Jana | Jože | Fine dining | Prebil | Večer | Priporočen vir za prepis |
|---|---|---|---|---|---|---|
| Varovalo pred TTS: misli, klici orodij, tuje pisave ne gredo na glas | `J:govor/pogovor/varovalo.py` | `JO:govor/varovalo.py` | `FD:govor/varovalo.py` | `PR:govor/varovalo.py` (dodane Prebilove fraze) | `VE:medij/govor/filter.py` | Jana (splošno). Zaznava obljub modela: `PR:govor/profil.py`. |
| En govorec na odgovor (model ali koda, ne oba) | `J:govor/pogovor/flows.py` (`FilterVprasanj`, `podvojen_stavek`) | `JO:govor/flows.py` | `FD:govor/pogovor.py` (vodja klica, ločen od Pipecata) | `PR:govor/flows.py` | `VE:medij/govor/pogovor.py` | Flows: Jana. Brez 4500-vrstičnega `flows.py`: Fine dining `pogovor.py`. |
| Dokaz, da je gost povzetek slišal (`MARK_MEDIA`) | `J:govor/pogovor/oznake.py` | `JO:govor/oznake.py` | `FD:govor/oznake.py`, `FD:govor/slisano.py` | `PR:govor/oznake.py` (isto kot J) | ni; `V7:medij/zvok/govor.py` | Jana |
| Prekinitve gosta, VAD, ignoriranje kratkih izjav | `J:govor/pogovor/prekinitve.py` | `JO:govor/prekinitve.py` | `FD:govor/prekinitve.py` | `PR:govor/prekinitve.py` (isto kot J) | ni; `V7:medij/zvok/ovojnica.py` (generacija izgovora, prekinitev) | Jana |
| Zaključek po oddaji, tišina (opomnika), časovna meja, konec klica | `J:govor/pogovor/zakljucek.py` | `JO:govor/zakljucek.py` | `FD:govor/zakljucek.py` | `PR:govor/zakljucek.py` | ni | Jana |
| Priprava TTS: ton, poudarek popravka, hitrost črkovanja | `J:govor/pogovor/tts_priprava.py` | `JO:govor/tts_priprava.py` | `FD:govor/tts_priprava.py` | `PR:govor/tts_priprava.py` | ni | Jana |
| Izgovor števil, vrstilnikov, datumov | `J:jedro/moduli/termin.py` | `JO:jedro/moduli/termin.py` | `FD:jedro/izgovor.py` | `PR:jedro/govorni_datum.py` | `VE:medij/prenos/izgovor.py`, `VE:medij/prenos/stevilke_besede.py` | Števila nad 6: Fine dining `izgovor.py`. Hišne številke po števkah: Večer. |
| Jezikovni model z rezervo, Soniox STT/TTS | `J:govor/pogovor/app.py` | `JO:govor/app.py` | `FD:govor/llm.py`, `FD:govor/soniox.py` | `PR:govor/app.py` | ni; `V7:medij/zvok/soniox.py` | Fine dining (izločeno v samostojni datoteki). |
| Sestava cevovoda, zagon storitve | `J:govor/pogovor/app.py` | `JO:govor/app.py` | `FD:govor/app.py`, `FD:govor/zagon.py` | `PR:govor/app.py`, `PR:govor/klic_prebil.py` | `V7:medij/zvok/streznik.py`, `V7:medij/zvok/procesor.py` | Prebil (zadnji, zavrne zagon brez konfiguracije) |
| Prompt (osnova + vozlišča) | `J:govor/pogovor/prompt_jj_osnova.txt` | `JO:prompti/prompt_joze_osnova.txt` | `FD:prompti/predloga/prompt.txt` | `PR:prompti/prompt.txt` | `VE:mediji/vecer/pozivi/osnova.txt` | Po vrsti agenta; prompt se ne prepisuje, ampak piše na novo iz CL (meja 5–6k znakov, glej `pravila.md`). |
| Predaja klica človeku, prevezava Jana → Jože | `J:govor/pogovor/predaja.py`, `J:govor/pogovor/prevezava.py`, `J:govor/pogovor/eposta_osebja.py` | `JO:govor/predaja.py`, `JO:govor/prevezava.py` | ni | ni (številko osebja prebere koda) | ni | Jana (`predaja.py` je izklopljena, dokler ni vpisana številka) |
| Zasebni zapis neoddanega, neodvisno opozorilo ekipi brez osebnih podatkov | ni | `JO:jedro/listek_backend.py` (opozorilo po e-pošti) | ni | `PR:oddaja/neoddano.py`, `PR:deploy/opozori_storitev.py`, `PR:deploy/prebil-opozorilo.service` | ni | Prebil |
| Transport oddaje | `J:govor/pogovor/jj_transport.py` | `JO:oddaja/listek_eposta.py` (SMTP), `JO:govor/jj_transport.py` | `FD:oddaja/transport.py` (HTTP) | `PR:oddaja/eposta.py`, `PR:oddaja/predloga.py` (SMTP) | ni (lokalni ponor) | SMTP: Prebil. HTTP: Fine dining. |
| Namestitev | `J:deploy/README.md`, `J:govor/pogovor/megaphone-poc.service` | `JO:deploy/deploy-joze.sh`, `JO:deploy/joze.service` | `FD:deploy/deploy.sh` (suha vaja brez `--zares`), `FD:deploy/fine-dining@.service` | `PR:deploy/pripravi.sh`, `PR:deploy/prebil.service`, `PR:docs/namestitev.md` | ni; `V7:deploy/vecer-poc.service` | Ni primerjano; Prebil je zadnji (zasebni backup, vrnitev), Fine dining ima suho vajo. |
| Izvor kopij | ni | `JO:IZVOR.json` | `FD:IZVOR.json` | `PR:IZVOR.json` | ni | Prebil |

## Testno ogrodje

| Funkcija | Jana | Jože | Fine dining | Prebil | Večer | Priporočen vir za prepis |
|---|---|---|---|---|---|---|
| Cel pogovor skozi pravi Pipecat, posnet model, lažen TTS | `J:tests/govor/test_flows_cevovod.py`, `J:tests/govor/pomozno.py` | `JO:tests/govor/test_flows_cevovod.py` | `FD:tests/test_govor_pipecat.py` | `PR:tests/govor/prebil_cevovod_pomozno.py`, `PR:tests/govor/test_prebil_cevovod.py` | ni; `V7:tests/zvok/test_procesor.py` | Prebil (celoten tok agenta skozi pravi Pipecat; obseg: `PR:docs/qa.md`) |
| Besedilna simulacija celega klica z lažnim modelom po scenariju | ni | ni | `FD:govor/simulacija.py`, `FD:tests/test_govor_simulacija.py` | ni | `VE:scripts/konzola.py`, `VE:tests/govor/pomozno.py`, `VE:tests/govor/test_pogovor.py` | Fine dining (scenarij pade, če kliče orodje, ki ga vozlišče ne ponuja) |
| Simulacija ali ponovitev s PRAVIM modelom (stane) | ni | `JO:tests/replay/simulacija_scenarija.py`, `JO:tests/replay/ponovitev_zapisa.py` | ni | `PR:scripts/simulacija_opisa.py` | `VE:tests/govor/test_zivi_razlog_cas.py`, `VE:tests/govor/test_zivi_naslov.py` (samo z `VECER_ZIVI_TESTI=1`) | Jože (`ponovitev_zapisa.py`: zapis živega klica gre skozi pravi model) |
| Zaklenjena tabela pričakovanj (yaml + kontrolna vsota) | samo na veji `origin/jana-drobno`, ni v main | `JO:tests/pricakovanja/test_pricakovanja.py`, `JO:tests/pricakovanja/01-chebov-scenarij.yaml`, `JO:tests/pricakovanja/zakleni.py` | ni | ni | ni | Jože (vsaka vrstica ima ID, `mora`, `ne_sme`, vir) |
| Živi klic kot trajen regresijski test | ni | `JO:tests/govor/test_klici_zapisi.py` (nov klic = nov JSON) | ni | `PR:docs/porocila/klici-kot-testi.md` (opis, ne koda) | ni | Jože |
| Test po mehanizmih (kapitalne napake kot testi) | `J:tests/govor/test_nacela_koda.py`, `J:tests/govor/test_nacela_popravki.py` | `JO:tests/govor/test_nacela_koda.py` | `FD:tests/test_zascite_visoke.py` | ni | `VE:tests/test_m3_izmisljeno.py`, `VE:tests/test_m6_zatakne.py`, `VE:tests/govor/test_m1_prepis.py` | Večer (test za vsak mehanizem; register popačenih vnosov: `VE:tests/test_m1_popacen_vnos_register.py`) |
| Sklic testa na ID zahteve iz CL (komentar `# CL: ID`) | ni | ni | ni | ni | `VE:tests/test_obrat.py` (21 testnih datotek ima sklic) | Večer. Prebilov CL ima ID-je, a v testih jih ni (iskanje po `P-XX-NN`: 0 zadetkov). |

## Kaj se pri agentih res ponavlja

Šteto iz tabel zgoraj (štirje Pipecat agenti = Jana, Jože, Fine dining, Prebil):

- **V vseh štirih (kopije iz Jane):** `klic.py`, `modul.py`, `kontakt.py`, `summary.py`, `nastavitev.py`, `varovalo.py`, `prekinitve.py`, `zakljucek.py`, `oznake.py`, `tts_priprava.py`. Razlike (število različnih vrstic proti Jani, `diff`): `modul.py` 0 do 11, `kontakt.py` 0 do 32; `klic.py` Jože 10, Prebil 343, Fine dining 405; `prekinitve.py` in `oznake.py` pri Prebilu in Jožetu 0. Prepis torej ni vedno »kopiraj in zaženi«: preveri `diff` proti izvoru.
- **V treh:** `termin.py` (Jana, Jože, Fine dining), `profil.py` / besedila v yaml, `IZVOR.json` (Jože, Fine dining, Prebil).
- **Samo pri enem:** ujemanje z jedilnikom (Jože), degustacija (Fine dining), zasebni zapis neoddanega in opozorilo (Prebil), tabela pričakovanj (Jože), ujemanje z bazo naročnikov, črkovanje priimkov, število poskusov v čisti funkciji (Večer).
- **Večer je drugačen:** svoje jedro (`medij/`), svoje testno ogrodje po mehanizmih in edini sklicuje teste na ID iz CL. Govorni sloj (zvok) je na veji `faza-7`.
- **Pazi:** `docs/PRAVILA.md` pri Jožetu in `docs/pravila/*` pri Fine dining sta KOPIJI pravil; vir je Obsidian (`scripts/pravila.py`). Fine dining `docs/pravila/mehanizmi-M1-M8.md` je kopija Večerovih mehanizmov, ki po Chebovi odločitvi 19. 10. za druge agente NE veljajo.
