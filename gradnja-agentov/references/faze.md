# Faze: kaj nastane, kdo potrdi, kaj prebrati

Ogrodje: Chebova shema procesa `/home/chebo/Desktop/Dnevno /Megaphone-proces-arhitekture.html` (7. 10. 2026; pozor na presledek za »Dnevno«). CL je vir zahtev, arhitektura določi, kdo jih izvaja, pogodbe povežejo bloke, izvedba in testi se vežejo na iste ID-je. V shemi je »EL / glasovni sloj«; ker ElevenLabsa ni več v rabi, je tu samo **glasovni sloj** (lastna arhitektura: Pipecat, Asterisk, Soniox).

| Faza | Nastane | Potrdi | Zapora (brez tega naprej ne greš) |
|---|---|---|---|
| 01 Zahteve | CL (`predloga-checklista.md`) | Chebo | `preveri_cl.py` brez napak in brez ODPRTO; Chebova potrditev |
| 02 Arhitektura | nosilec + merilo + test na vsaki zahtevi; seznam vrzeli; skica; tabela modulov | Chebo (razdelitev nosilcev in skica) | vsak ID ima nosilca in merilo; za vsako funkcijo je vir iz `moduli.md` ali izrecno »novo« |
| 03 Povezave | pogodba (`predloga-pogodb.md`) | Chebo | razdelek 7 pogodbe izpolnjen; vsak ID Koda/LLM v sledljivosti |
| 04 Izvedba | naloga, koda na veji, testi, zapis različice | Chebo (živi klic, »namesti«) | `preveri_cl.py --testi` brez napak; QA je sam poganjal teste; `pripravljeno.py` ZRELO; nič na produkcijo brez »namesti« |

Dve splošni zapori: **izrecno naročilo** (»naredi«, »pojdi«; pogovor, skica in strinjanje niso naročilo) in **nič na produkcijo, merge v main, push, namestitev, preusmeritev številke brez Chebovega neposrednega »namesti«**.

## Pot: nov agent ali večji popravek?

- **Nov agent ali nova funkcija:** vse štiri faze. CL je lahko dopolnitev obstoječega.
- **Večji popravek obstoječega agenta** (napaka iz klica, Codexova najdba): (1) FILTER (`pravila.py`) – na prvem »ne« konec; (2) če popravek zahteva novo poslovno pravilo ali spremeni obstoječega, dopolni CL (nov ID, stari se ne preštevilčijo) in Chebo potrdi; (3) faza 02 samo za zadevne ID-je (nosilec: najnižja plast); (4) pogodba samo če se spremeni vhod/izhod orodja; (5) faza 04 z nalogo iz CL ID-jev. Brez CL ID-ja ni naloge.

## Faza 01: Zahteve

Preberi: stari CL drugih agentov kot vzorec (`moduli.md` kaže na Prebilov `docs/checklist-prebil.md` in Večerov `docs/checklist-mediji.md`), obstoječo predlogo (`predloga-checklista.md`, razdelek 1), vire naročnika (spletna stran, intervjuji, klici). Ne prenašaj vrednosti druge restavracije ali podjetja.

1. Izpolni CL neodvisno iz virov; ugibanja so `ODPRTO`, ne `iz virov`.
2. Konflikti med viri gredo v tabelo; velja novejša izrecna Chebova odločitev.
3. Tabela znanih napak (iz klicev) in scenarijev ima ID-je in poveže na zahteve.
4. Odprta vprašanja za Cheba: predlog + zakaj je pomembno; ne vprašaj znova, kar je potrjeno.
5. `preveri_cl.py CL.md --dovoli-odprto` med pisanjem; brez `--dovoli-odprto` pred potrditvijo.

## Faza 02: Arhitektura

Preberi: `moduli.md`, `pravila.md` (`pravila.py --pregled`), `/home/chebo/MAIOS/02-knowledge/Megaphone/Voice AI agenti/Predloga arhitekture rezervacijskega agenta.md` (aksiom: rezervacija se ne odda, dokler niso zbrani obvezni podatki, gost ne potrdi aktualnih vrednosti in ne dovoli oddaje; vrstni red pogojev operacij).

1. **Nosilec** vsake zahteve (en glavni, drugi podpirajo):

   | Vprašanje (po vrsti, ustavi se na prvem »da«) | Nosilec |
   |---|---|
   | Obstaja koda, ki bi to vedno izračunala enako, brez konteksta pogovora (stanje, validacija, ura/datum, ujemanje, števci, povzetek, zapora oddaje)? | **Koda** |
   | Je besedilo, nastavitev, dejstvo, meni, urnik, napotitev, ki jo potrdi lastnik? | **Vsebina** |
   | Je zvok, prekinitev, tišina, predvajanje, telefonija, izgovor? | **Glasovni sloj** |
   | Je razumevanje pomena, razjasnitev, ton, naraven odgovor? | **LLM** |

   Načelo: razlika, ki je znana in predvidljiva, sodi v kodo, ne v prompt (Chebo). LLM razvršča nejasen govor, koda računa in odloča. Fiksne stavke izgovori koda; model govori prosto samo, kjer CL to izrecno dovoli (razjasnitev, odgovor izven poteka).
2. **Merilo** in **test/scenarij** vsake zahteve (konkretno, glej predloga CL, razdelek 4).
3. **Moduli**: za vsako funkcijo poišči vir v `moduli.md`; tabelo »funkcija → vir @ commit → kaj prilagoditi → česa ne pisati na novo« zapiši v skico. Novo je izjema; označi in napiši, kje si iskal.
4. **Pregled pred gradnjo** (graf, prompti, potek klica z izjemami, uveljavljene rešitve): seznam vrzeli z rešitvijo in ceno popravka PRED gradnjo. Pri novem agentu še nimaš grafa: pregled opravi na skici (vozlišča, prompti po vozliščih, meja 5–6k znakov na vozlišče).
5. **Skica**: kaj se spremeni, kje, kaj se lahko pokvari. Chebo potrdi skico in razdelitev nosilcev.

## Faza 03: Povezave

Predloga `predloga-pogodb.md`. Iz nosilcev in modulov izpelji polja, pogodbe orodij (vhod/izhod/status), pogodbo oddaje in pogoje prehodov. Skrbi, da noben podatek nima dveh lastnikov in da pogoj oddaje uveljavi koda, ne prompt.

## Faza 04: Izvedba

1. **Naloga** (`predloga-naloge.md`): iz CL ID-jev, pogodbe in tabele modulov; brez izpolnjenih razdelkov 2–5 je ne pošlji. Pri več izvajalcih: ločene datoteke ločenim izvajalcem.
2. **Implementacija** na ločeni veji (Sonnet po navodilih orkestratorju; Codex kot izvajalec ali pregledovalec). Prepisi modulov iz **commita**, vpis v `IZVOR.json`.
3. **Revizija in testi** (Opus QA): sam poženi teste in preberi diff; poročilo izvajalca ni dokaz. Testi: pravi Pipecat cevovod s posnetim modelom skozi cel pogovor (agent se lomi na prehodih), ciljni testi prizadetih scenarijev, poln test pred namestitvijo, nato Chebovi živi klici (obvezni). Pregled prompta naj opravi drug kot avtor; ena tema = eno mesto v promptu. Vsak ID ima test z `# CL: ID`; `preveri_cl.py CL.md --testi tests/`. Skrite oblike, vprašanje »česa popravek ne pokrije« in `pripravljeno.py` (mora reči ZRELO pred »čaka Cheba«): podrobno v `predloga-naloge.md`.
4. **Objavljena različica**: veja, SHA, ukaz in dejanski rezultat testov (koliko zelenih od koliko), kaj je preizkušeno z lažnimi ponudniki in kaj z živim klicem, odprte omejitve. Ne trdi, da je namestitev delujoča, če ni preverjena. Namesti Chebo po svojem »namesti«.

### Koordinacija (iz hooka, 22. 10. 2026; dokler hook tega ne odstrani, velja v obeh)

- Ključi so v `~/.bashrc`; naložiš jih z `bash -ic '…'`. Nikoli jih ne izpiši; preveri samo, ali so nastavljeni. GitHub push: `https://x-access-token:$GITHUB_TOKEN@github.com/…`.
- Slack: poslušalec za kanal SVOJEGA projekta mora teči (`python3 -u ~/.claude/hooks/slack-poslusaj.py <mapa .koordinacija> <oznaka>`; poti v glavi skripte); tujega kanala ne poslušaj in o njem ne poročaj. Vsebinsko Codexovo sporočilo: takoj v nit »videl, potrjujem prevzem dela«, nato delo, nato rezultat v nit. Pred »čakam Codexa« preberi nit. Chebo ne lepi sporočil.
- Na Slack piši samo kot bot Claude (`<projekt>/.koordinacija/slack-post.py`), nikoli prek Slack MCP (`slack_send_message`), ker ta piše v Chebovem imenu. Prebil nima `.koordinacija/`; njegova nit je v `AGENTS.md`.

## Povratna zanka

| Dogodek | Kaj narediš |
|---|---|
| Napaka v klicu ali testu | FILTER (`pravila.py`). Če prestane: določi odgovorni blok (nosilec iz CL), popravi tam, zapiši v tabelo znanih napak (ID `Z-nn`) in dodaj **regresijski scenarij** z `# CL:` ID zadevne zahteve. |
| Napaka je v testu ali prepisu | Popravi test; ne popravljaj agenta. |
| Ne prestane FILTRA | Zapiši (backlog); ne popravljaj in ne blokiraj namestitve na testno stran. |
| Novo poslovno pravilo ali Chebova odločitev | Dopolni CL z novim ID (nosilec, merilo, test), Chebo potrdi, nato faza 02 za ta ID. CL, prompt in koda se ne smejo razhajati: uskladi na enem mestu. |
| Najdba Codexa | Najprej FILTER; »blokator DA« ni razlog za popravek. |
| Oblika iz 5a pade | Ni nova napaka; je test, ali popravek odpravi vzrok. Napaka sama mora še vedno prestati FILTER. Oblika z drugim mehanizmom → backlog, ne popravek. |
| Oblika zahteva odločitev, ki je ni v CL | Ne implementiraj; predlog v poročilo, odloči Chebo (ne izumljaj pravila); zapis v dnevnik `odlocitve.csv`. |

## Kar je ostalo uporabno iz starih skillov (ElevenLabs; zgodovina, tu samo načela)

Vir: `_arhiv-elevenlabs/elevenlabs-workflow-vozlisca`, `gostinski-demo-agent`, `vecer-korpus-in-qa`. Dokazano na ElevenLabsu, na lastni arhitekturi ni ponovno preverjeno:

- **Zelena luč ni dokaz.** Vedno preberi surov prepis pogovora, ne samo izida ocenjevalca ali testa (ocenjevalec je trikrat označil pravilno vedenje za kršitev in šest krogov popravkov je šlo za napako, ki je ni bilo).
- **Dobesedni obvezni stavek citiraj v promptu, prepovedane fraze opiši abstraktno** (naštete prepovedane fraze model posnema).
- **Zgodovine napak ne piši v prompt.** Pravilo naj bo ena poved; zgodba (zakaj) sodi v dokumentacijo. Podvojeno pravilo centraliziraj na eno mesto.
- **Krčenje prompta**: strojna primerjava vseh narekovajnih citatov pred in po; kontrolnega seznama pravil ne sestavlja isti agent, ki prepisuje.
- **Menjava modela**: preveri prehode med vozlišči (ob nejasnem odgovoru ostane na mestu), povzetek pred oddajo, in da model v orodje ne pošilja izmišljenih vrednosti (surovi argumenti klica).
- **Drug ASR dokazuje točnost prepisa, ne namena govorca.** Ob dvoumnem zaporedju vprašaj testerja.
- **Ozek vzorec podceni.** Šteje obrate s podatkom, ne z imenom podatka; poročaj v deležih.
- **Pravi telefonski klic**, ne samo widget ali simulacija: ASR napake pri imenih in naslovih se pokažejo šele na pravi liniji.
