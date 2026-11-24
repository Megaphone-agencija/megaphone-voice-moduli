# Dogovori po družinah napak (Chebo + Claude, 24. 11. 2026)

Kratek zapis, kaj sva dogovorila pri razlagi ontologije. Nič od tega še ni zgrajeno. Vir: ontologija napak 20. 11.

## Štetje vrtenja v krogu
- Šteje VSAK commit popravka (tudi popravki prejšnjih popravkov).
- Preverba vsakih ~10 popravkov čez vse agente + dnevna varnostna preverba; brez zaklepov. Če ne ustreza, na dva dni.

## Družine
1+2. **Vrednost modela brez dokaza + pomen po seznamu besed** → ena skupna funkcija »razberi odgovor na zastavljeno vprašanje«: (1) koda (besede iz jedilnika/sopomenke, kratke čiste oblike), (2) ozko vprašanje modelu z zaprtim naborom (možnosti / da-ne-popravek-vprašanje-ne vem), (3) »ne vem« → vpraša znova. Model ne more zapisati vrednosti zunaj ponujenih možnosti. Pomen: »mhm«, »Ja, seveda, ne.«, »V redu, hvala, nasvidenje« = DA; kaj sledi, določi vprašanje (Večer »Želite še kaj?« → počakaj; Prebil »Lahko oddam?« → oddaj). Zbirka pravih odgovorov za preverbo natančnosti.
3. **Izgovor** → skupna pravila (števila, datumi, okrajšave) + slovar po dejavnosti (gostinstvo, avtoservis, dostava) + slovar stranke; samodejna preverba vseh imen vnaprej (poslušaš samo, kar najde ali je novo).
4. **Vezava na napačen dogodek** → oštevilčeni stavki in vprašanja; osnova Prebilova koda z dvema popravkoma (številka ob koncu prepoznave, številka potuje z zapisom).
5. **Iskanje v katalogu** → en iskalnik za vse poti; sopomenke iz pravih Sonioxovih zapisov (»stejk«, »Romer Kvele«, »tesarjeva«), toleranca 1–2 črki → »Ste mislili …?«, števnikov ne izrezuj; po dveh poskusih zapis na listek z oznako »preveri kuhinja« (zaenkrat vedno; »tega nimamo« šele po preverbi). Zvočni pari na istem jedilniku (hišna Koakola / Coca-Cola): koda jih vnaprej označi; ob omembi kateregakoli agent vedno ponudi obe možnosti.
11. **Model ne zapiše povedanega** → preverba »vse omenjeno je zapisano« ne zapisuje tiho, ampak vpraša (»Ste mislili Coca-Colo?«; pri zvočnem paru obe možnosti); agent po vsaki jedi pove, kaj je zapisal; dan/ura iz razčlenjevalnika (8); pri več stvareh štetje (dve vozili → vpraša za drugo).
6. **Obrat brez govorca** → en čuvaj obrata: po gostovem stavku v X s (predlog 3, ni potrjeno) koda izgovori stalni stavek; modela ne zažene znova.
7. **Slišanost** → slišano = Asterisk javi konec predvajanja tega stavka; vse drugo = ni slišano. POGOJ: najprej preveriti zanesljivost oznak v dnevnikih klicev.
8. **Oblika vrednosti** → en razčlenjevalnik časa/datuma za vse (pozna »zdaj«, smer naprej/nazaj), ena tabela govorjenih oblik; neznano → ozko vprašanje + preverba smiselnosti; dvoumno → vprašanje.
9. **Novo prepiše staro** → vsak stavek je dejanje dodaj (privzeto) / popravi / odstrani; toliko mest kot stvari; zavrnitev izbriše samo zavrnjeno; potrditev spremembe pove koda.
10. **Dva govorca** → pred obratom ena odločitev, kdo govori; kjer koda lahko prevzame, model nima besede; vsak podatek prebran enkrat.
12. **Model oblikuje stalni stavek** → NIZKA PRIORITETA (Chebo: ko so bila besedila popravljena, je bilo v redu). Brez posebnega popravka; načelo »stalne stavke govori koda« ostane tam, kjer že je.
13. **Prekinitev pokvari stanje** → kratek »ja«/»mhm«/šum ni prekinitev (za vse); prava prekinitev: agent utihne, vprašanje ostane odprto, gostove besede so lahko odgovor (funkcija 1+2), sicer krajša ponovitev; prekinjeno ≠ izrečeno; ena koda za vse. Večerova odločitev 17. 11. (prekinjen povzetek → vpraša, ali lahko preda) ostane. Občutljivost zaznave pri Večeru je že zmanjšana → prenesti nastavitev k ostalim.
14. **Pravilo v promptu izgubljeno/protislovno** → prompti čim krajši, kar lahko gre v kodo; oznake in preverba samo za Chebove izrecne odločitve (~10–15 na agenta), da ne izginejo brez njegovega »da«; preverba dolžine: cilj 5–6 tisoč znakov na vozlišče, trda zgornja meja ~10 tisoč (Chebo 13. 11.); novo pravilo zadnja možnost.
15. **Vprašanje v zanki** → stanje vprašanj v jedru (isti seznam oštevilčenih vprašanj kot pri 4): odgovorjeno se ne ponovi; največ 2 poskusa, drugič drugače in z možnostmi; nato počaka na konec naročanja ali »preveri kuhinja«; med narekom brez starih vprašanj. Jože: dodatek ponudi ENKRAT na koncu naročila.
16. **Jed dvakrat na listku** → ena vrata v jedru: prvi kos vedno; nov kos ŽE ZAPISANE jedi samo ob »še« ali številu (ali odgovoru na vprašanje, ki ga je sprožilo število). Ponovljeno ime brez »še«/števila ne doda (Chebo; nadomesti predlog pregleda). Število brez »še« pri že zapisani jedi NASTAVI skupno količino (»Dva pad thaia« → 2), »še dva« prišteje (Chebo 20. 11.). »Zraven tega ribeya omako …« → ribeye ostane 1, omaka gre nanj. Ob ponovljenem imenu brez »še«/števila agent reče: »{jed} že imam na seznamu, ste mislili dodati še kakšno drugo jed?« (»ja« = gost bo naročil drugo jed → počakaj/»Katero?«; istemu artiklu se kos NE doda; pri pijači: »{pijača} že imam na seznamu, želite morda še kakšno pijačo?«). »Ja« brez odprtega da/ne vprašanja = medmet: agent nadaljuje, nič ne zapiše, ne komentira.
17. **Notranje besedilo na glas** → obrnjena preverba (imena polj samodejno iz opisa orodij; v glas samo navadna slovenska poved, brez kode/angleškega razmišljanja/dobesednih delov navodil; kar ne prestane, koda izreče stalni stavek). Prioriteta: nad družino 12, pod ostalimi (redko, a bedna napaka).
18. **Zunanji ponudnik** → en skupni modul na ponudnika (Soniox, Entrim/OpenRouter, Pipecat, pošta), popravek enkrat za vse; dimni test ob vsaki namestitvi (ključ, ime modela, dve orodji v enem kosu, kratek stavek glasu), ob padcu se namestitev ustavi. Prioriteta nizka–srednja, poceni.
19. **Oddaja odloči model** → stanje oddaje samo v kodi; stavke o opravljenem dejanju (»oddano«, »zapisal sem«, »potrjeno«) govori koda šele po dejanju; klic se ne konča pred oddajo (slovo → »Preden se posloviva, lahko oddam?«); neuspeh = resnica + izhod. Osnova: Juretova zapornica.
20. **Vpraša za znan podatek** → brez svojega popravka: vprašanja samo za prazna polja (seznam vprašanj, 15); znan podatek se potrdi, ne vpraša (»Vas lahko pokličemo na številko, s katere kličete?«); povedano v prvem stavku razbere funkcija 1/8.
21. **Prepis brez prilagoditve** → VISOKA PRIORITETA (Chebo: pri Prebilu ~teden izgube; »vzemi iz Jane in prilagodi« brez CL; dogovor »dve vozili« ni prišel noter). Prepis samo prek CL z ID-ji in testi; vsak dogovor = CL vrstica s testom; naloga za prepis brez CL ID-jev zavrnjena (hook podagent-pravila.py; Codexu enako piše orkestrator); zemljevid modulov našteje »odvisno od agenta« (spol, pomen ja/ne, vrsta podatka, ključi nastavitev); spol in podobno v nastavitvah; dimni test preveri nastavitve. Štetje commitov to družino podceni. NUJNO: natančen popis vedenja vsakega modula (vsaka zmožnost z oznako, predpostavke, nastavitve, česa ne zna, testi) in navzkrižna primerjava CL novega agenta s popisi → pokrito / s prilagoditvijo / razvij; popis se posodobi ob vsaki spremembi modula (preverba v pripravljeno.py).
22. **Priloga že v jedi** → podatek »vključeno« pri vsaki jedi v vseh jedilnikih (Chebo 22. 10.: vključeno ≠ priloga s ceno); ena pot v jedru: »Pomfri že pride zraven. Želite še dodatno porcijo?« (Jure že ima); test čez cel jedilnik. Potrjeno.

## Skica »manj krpanja« (20. 11.) v procesu
- A–D že zgrajeni (needs-review) in ostanejo.
- E (korpus za družino 2) = test natančnosti funkcije »razberi odgovor« (1+2); zbiranje pravih odgovorov začne takoj.
- F (jutranji agent) = del dnevne preverbe vrtenja; potrebuje seznam družin in vrstici Vrsta/Družina.

Skupni deli (opažanje): seznam vprašanj (1, 2, 4, 6, 7, 13, 15), funkcija »razberi odgovor« (1, 2, 9, 11), čuvaj (6), iskalnik (5, 11), razčlenjevalnik časa (8).

## Seznam za gradnjo (vrstni red določiva na koncu)
- Preverba vrtenja (10 popravkov + dnevno), vrstici Vrsta/Družina v commitu.
- Zapora za Codex (2 vrstici v nastavitvah).
- Testni gost NIMA splošnega/izmišljenega odgovora: ko za vprašanje nima realnega odgovora iz klica (ali potrjenega od Cheba), tek USTAVI z »vrzel orodja: manjka odgovor na <vprašanje>«. Izvedba pravila iz Agent-Shared/PRAVILA.md pod FILTER (Chebo, 24. 11.: nov korak iz popravka se pred testom pokrije z realnim odgovorom).
- Naloga popravka brez vrstice `Vir:` (pravi klic ali tek z dobesedno gostovo izjavo) je zavrnjena (hook podagent-pravila.py).
- Preverba zanesljivosti oznak MARK_MEDIA (pogoj za 7).
- Nov repozitorij Megaphone-agencija/megaphone-voice-moduli (skill gradnja-agentov, popisi modulov, družine, dogovori); lokalna delovna kopija v MAIOS 04-workflows/Skills/gradnja-agentov.
- Zavarovanje MAIOS: osebni žeton iz naslova remote v datoteko s ključi + pomožni program za ta repo (žeton za Megaphone nima dostopa do Mhardook/MAIOS, preverjeno); nato Chebo prekliče stari žeton.
- Popravki vzrokov po družinah (zgoraj).

## Vrstni red gradnje (PREDLOG 24. 11., čaka Chebov »naredi«)

Načelo: en del naenkrat; najprej na enem agentu, nato prenos k ostalim prek popisa modula in CL. Vsak del gre skozi 5a in pripravljeno.py (ZRELO). Merilo uspeha: čez 3 tedne delež popravkov prejšnjih popravkov (izhodišče 44 %).

**Faza 0 — zaščite procesa (majhno, takoj zmanjša izgubo časa)**
1. Seznam družin (druzine.yaml) + vrstici Vrsta/Družina v commitu + preverba na 10 popravkov in dnevno (vključno z jutranjim agentom F).
2. Testni gost brez izmišljenih odgovorov (vrzel ustavi tek) + naloga popravka brez `Vir:` zavrnjena.
3. Naloga za prepis brez CL ID-jev zavrnjena.
4. Zapora za Codex (2 vrstici) + zavarovanje žetona MAIOS (Chebo nato prekliče stari žeton).
5. Repozitorij megaphone-voice-moduli z lokalno kopijo.

**Faza 1 — popis modulov (nujno, pogoj za prenos)**
6. Natančen popis vedenja modulov + navzkrižna primerjava s CL.

**Faza 2 — skupni deli v jedru (pilot pri Jožetu, nato prenos)**
7. Dokaz za nov kos + »vključeno« (16, 22) — majhno, krog teče danes (jurčki).
8. Seznam vprašanj z oštevilčenimi stavki (4, 15, 20; temelj za 1, 2, 6, 7, 13).
9. Funkcija »razberi odgovor« + zbirka pravih odgovorov E (1, 2, 9, 11).
10. Čuvaj obrata + en govorec na obrat + oddaja v kodi (6, 10, 19).
11. Iskalnik + sopomenke iz klicev + zvočni pari (5, 11).
12. Razčlenjevalnik časa + tabela oblik (8).
13. Slišanost (najprej preverba MARK_MEDIA) + prekinitve (7, 13).

**Faza 3 — ostalo**
14. Izgovor: slovarji po dejavnosti + preverba vnaprej (3).
15. Moduli ponudnikov + dimni test ob namestitvi (18, 21).
16. Prompti: oznake Chebovih odločitev + preverba dolžine (14).
17. Notranje besedilo na glas (17), stalni stavki (12, nizko).

## PREDNOSTNO: dokaz koncepta prevzema (Chebo, 24. 11. 2026)
Nobeden od agentov še nima stranke. Cilj zdaj: agent za prevzem hrane (jedro Jože/Jure) dela brez težav (vsa naročila, pečenosti, priloge), kot Jana pri rezervacijah; nova restavracija nato v enem dnevu samo s podatki.
- Vir jedra: Jože (J&J). Dokaz »samo podatki«: Jure (Kratochwill) na istem jedru brez sprememb kode.
- Faza 2 najprej samo za prevzem: 2.7 dokaz za nov kos + vključeno, 2.8 seznam vprašanj (pečenost, zanke), 2.9 razberi odgovor, 2.10 čuvaj/en govorec/oddaja, 2.11 iskalnik/sopomenke/zvočni pari; 2.13 slišanost kot skupni del.
- Popis modulov (1.6) najprej za prevzem: kaj je splošno jedro, kaj podatek restavracije.
- Prenos k Jani, Prebilu, Fine diningu, Večeru (2.12 razčlenjevalnik časa itd.) kasneje.
- MERILO KONCEPTA: (1) Chebovi klicani scenariji za Jožeta 3× pravi model brez napake na listku; (2) Jure na istem jedru z drugim jedilnikom: enak izid brez spremembe kode; (3) nova restavracija: samo podatkovne datoteke, preverba »samo podatki« zelena.

## Tri panoge, vsaka »off-the-shelf« (Chebo, 24. 11. 2026)
Restavracije (Jana rezervacije, Jože/Jure prevzem), avtoservis (Prebil), medijske hiše (Večer; zanimanje znotraj Večera že obstaja). Za vsako: nova stranka = samo podatki. Vrstni red: prevzem (dokaz koncepta) → Večer → Prebil. Popis modulov in merilo »samo podatki« po istem vzorcu za vsako panogo.
