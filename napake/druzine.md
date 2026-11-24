> Strojni vir družin je `druzine.json` (isti seznam, bere ga hook `git-hooks/commit-msg` in `stej.py`). Ta datoteka je berljiv opis; ob spremembi družine popravi oboje.

# Družine vzrokov napak glasovnih agentov (zaprt seznam)

Vir: ontologija napak 20. 11. 2026 (1. 10.–20. 11., 494 popravkov). Tabela popravkov: `popravki-2026-11-20.csv` v tej mapi. Če napaka ne sodi v nobeno družino: `drugo` (in predlog nove družine Chebu).

### 1. `vrednost-modela-brez-dokaza` — 73 (Večer 40, Jože 26, Jana 5, Jure 2), ponavljanje 34
**Definicija:** koda vzame klic modela dobesedno, tudi kadar vrednost, polje, možnost ali sklic gost ni rekel ali je rekel drugače. Druga oblika: naknadna preverba »je to v gostovih besedah« je preozka ali preširoka.

**Primera:**
- d5cbeb5 (Jože): gost reče »Še slanino gor«, model pa pošlje »za vse jedi«.
- 942a382 (Jože): Jože reče »Pečenosti izberi žal nimamo«, čeprav gost take besede ni rekel.
- Pri Večeru 2d16831: »priti« / »prit« se zavrne.

**Krog:** model je vir resnice, koda pa poskuša za njim dokazati, da je vrednost res povedana, po bližini besed. Vsaka nova oblika je bodisi preozka bodisi preširoka. Večerjeva veriga števnikov a30d620 → 5e3d0d5 → c948c0f → c67e0fe sama zapiše »se vrti v krogu«.

**Kandidat:** obrni smer.
- Model pove samo, na katero vprašanje ali polje gost odgovarja.
- Vrednost izpelje koda iz gostove izjave proti zaprtemu naboru (dnevi, števniki, ponujene možnosti odprtega vprašanja).
- Ko je ne najde, vpraša, namesto da sprejme modelovo.
- Pri Jožetu: odgovor na »Ste mislili …?« razreši koda proti ponujenim možnostim, modelov argument je samo namig.

### 2. `pomen-po-seznamu-besed` — 45 (Prebil 18, Večer 14, Jože 8, Jana 4, Bojan 1), ponavljanje 25
**Definicija:** koda presodi namen izjave (ja/ne, dovoljenje za oddajo, slovo, »v redu«, »kaj?«, zanikanje) po seznamu besed ali enem signalu, brez sobesedila.

**Primera:**
- 9009f4c (Prebil): »Ja, lahko daš.« je zavrnjen, povzetek prebran osemkrat.
- 2958148 (Jana): »V redu, hvala za pomoč. Nasvidenje.« velja za potrditev povzetka.

**Krog:**
- Vsaka nova oblika (»ne, ni treba«, »kar daj«, »Ja, seveda, ne.«) je nova vrstica v seznamu.
- Preširok seznam spusti napačne (575b57e: »mhm«; 406322c).
- Vsak agent ima svoj seznam.

**Kandidat:** ena skupna funkcija v jedru »razvrsti odgovor na zastavljeno vprašanje«.
- Dobi besedilo vprašanja in celo izjavo.
- Vrne da / ne / vprašanje / nejasno.
- Deterministična je samo za kratke čiste oblike, sicer model izbira iz zaprtega nabora.
- »Nejasno« vedno pomeni, da vpraša znova.
- Regresija je en korpus resničnih odgovorov iz vseh klicev vseh agentov.

### 3. `besedilo-ali-izgovor` — 37 (Jože 15, Jana 10, Večer 6, Prebil 3, drugi 3), ponavljanje 16
**Primera:**
- 1c8053b (Večer): »Slov Bistrica«.
- a477e53 (Jože): »0,33 L«.
- ebe79c2: 33 od 113 zapisov izgovora je bilo napačnih.

**Krog:**
- Zapisi izgovora so bili fonetične ocene brez poslušanja.
- Tabele ulic in krajev so se dopolnjevale trikrat (1c8053b, e438ffe, 36de7e2).

**Kandidat:**
- En skupni modul »pripravi besedilo za glas« (števila, okrajšave, tuja imena) in en slovar izgovora za vse agente.
- Ti ga preveriš s poslušanjem enkrat.
- Test gre čez VSE vnose baze in kataloga, ne primer za primerom.

### 4. `vezava-na-napacen-dogodek` — 25 (Prebil 8, Jože 6, Jana 4, Večer 4, FD 2, Jure 1), ponavljanje 15
**Primera:**
- 0b716d5 (Prebil): gost reče »Ne, priimek je Novak«, staro orodje pa nato priimek prepiše.
- a2dc2d3 (Jože): gostov »ja« razreši tudi drugo, še nerešeno pijačo.

**Krog:** dogodki se povežejo po vrstnem redu, števcu ali času. Primer je Prebilova veriga svežine izjave 54335b1 → 0b716d5 → 2a0915d → 48344f0.

**Kandidat:** vsak dogodek nosi identiteto (id izjave, vprašanja, stavka). Odgovor in orodje se vežeta na id; v jedru je ena vrsta odprtih vprašanj z id-ji.

### 5. `iskanje-v-katalogu-ali-evidenci` — 25 (Jože 20, Večer 4, Jana 1), ponavljanje 6
**Primera:**
- 471db60 (Večer): »Kovač« za »Kovačič«.
- 93f9670 (Jože): »tesarjevo solato«.
- 4793447: Römerquelle.

**Krog:**
- Vsak sklon, umlaut in vzdevek posebej.
- Poti za jedi, priloge in dodatke so imele različna iskanja (94c1f41).

**Kandidat:** ena normalizacija in en iskalnik za vse poti. Test čez cel katalog krat vsi skloni.

### 6. `obrat-brez-govorca` — 24 (Večer 7, Jana 6, Jože 5, FD 3, Prebil 2, Jure 1), ponavljanje 6
**Primera:**
- 1c7eb24 (Jana): reče »Hvala.« in utihne.
- 1c59cb4 (Jure): na »O, 4.« molči.
- de4a884 (Jože): na »Ja?« molči.

**Krog:** vsaka pot, kjer nihče ne spregovori, je zakrpana posebej (rok tu, ujeta izjema tam).

**Kandidat:** ena nespremenljiva zahteva cevovoda: po vsaki gostovi izjavi mora v X sekundah priti zvok. En nadzornik obrata za vse agente ob izteku izgovori kodni stavek.

### 7. `slisanost-napacen-dokaz` — 23 (Jana 9, Prebil 4, Večer 4, FD 3, Jože 3), ponavljanje 13
**Primera:**
- dd87310 (Jana): povzetek velja za slišanega 0,65 s pred koncem zvoka.
- 4e4771e (FD): po napaki TTS odda, gost pa ni slišal.

**Krog:** dokaz se je menjal (časovnik, BotStoppedSpeaking, zadnja beseda, katerakoli oznaka) in vsak je imel luknjo. Kopije v FD so imele iste luknje (bde41e1).

**Kandidat:** en vir resnice, Asteriskova oznaka predvajanja za ID točno tega stavka. Vsaka negotovost pomeni »ni slišano«, zato agent ponovi. En modul za vse.

### 8. `oblika-vrednosti-ni-znana` — 23 (Večer 13, Jože 3, Jana 2, Bojan 2, Prebil 2, FD 1), ponavljanje 11
**Primera:**
- a30d620 (Večer): »oktobra je bilo dvakrat na začetku«.
- fba67fe (FD): sprejme »prejšnji petek«.
- 20673ef: »zdaj že drugi dan«.

**Krog:** vsak agent ima svoj razčlenjevalnik časa, ki se širi obliko za obliko.

**Kandidat:** en skupni razčlenjevalnik časa in datuma ter en korpus govorjenih oblik iz vseh klicev. Nova oblika je vrstica v korpusu, ne nova koda.

### 9. `novo-prepise-staro` — 22 (Večer 11, Jana 4, Prebil 3, FD 2, Jože 2), ponavljanje 6
**Primera:**
- c25040e (FD): »alergija na arašide … brez glutena«, arašidi izginejo.
- 56f8e86 (Večer): »pa naj se odpiše tudi za petek« zamenja dneve.
- 462699e (Jana): zavrnitev termina izbriše osebe.

**Krog:** podatkovni model ima eno mesto za nekaj, česar je lahko več. Primeri: ena rešitev za vse dni, ena čakajoča razjasnitev, ena zastavica.

**Kandidat:** zapis kot seznam dejanj (dodaj / popravi / odstrani), ki se združijo. Brisanje samo ob izrecnem popravku. Mest je toliko, kolikor stvari obstaja.

### 10. `dva-govorca-isti-obrat` — 20 (Jana 9, Jože 6, FD 2, Prebil 2, Jure 1), ponavljanje 7
**Primera:**
- dd38529 (Jana): model reče »Torej Jaka Test, štiri osebe …«, nato še kodni povzetek.
- fc18bf1 (Jože): gost dvakrat sliši »Imamo več možnosti«.

**Krog:** dušenje modela velja samo na delu poti (56370d9 samo za »Hvala.«, 093f967 samo ob nekaterih poteh).

**Kandidat:** en govorec na obrat, odločen PRED govorom, na enem mestu cevovoda za vse poti. To je mehanizem 2, dosledno izveden.

### 11. `model-ne-zapise-povedanega` — 20 (Jože 14, Prebil 4, Večer 1, Bojan 1), ponavljanje 11
**Primera:**
- dad4c01 (Jože): »pa eno to vašo Coca-Colo«, listek je nima.
- 07c5652 (Bojan): model izpusti »v sredo«.

**Krog:** varovalka tiho dopiše izpuščeno, a omembo bere brez namena. Zanikanje postane naročilo: 6c6d6cc (»Ne bom Cheese in Cockte«), 4a49b46, bdd2aef.

**Kandidat:** preverba »vse omenjeno je zapisano« naj ne zapisuje sama, ampak VPRAŠA (»Ste rekli tudi Coca-Colo?«). Vprašanje je varno ob dvomu, tihi zapis ni.

### 12. `model-oblikuje-stalni-stavek` — 19 (Prebil 7, Jana 6, Večer 5, Jože 1), ponavljanje 11
**Primera:**
- 6c23adc (Prebil): v e-pošti je »Klima je crknila«.
- 7a194b8 (Večer): model prosto preoblikuje odobrena vprašanja.

**Krog:** vsak nov podatek v prostem besedilu modela je nova zakrpa navodila (Janina veriga navodil za orodja v2–v6, Prebilov opis z zgledi).

**Kandidat:** načelo mehanizma 1 do konca. Vsak stavek z obvezno vsebino (povzetek, potrditev, roki, obljube) je predloga v kodi; model govori samo prosto besedilo brez podatkov.

### 13. `prekinitev-pokvari-stanje` — 19 (Večer 10, Jana 6, Jože 1, FD 1, Prebil 1), ponavljanje 7
**Primera:**
- b7f29eb (Večer): »Ja.« med vprašanjem se zavrže, vprašanje se ponovi petkrat.
- e3835e2 (Jože): po »Halo?« prekinjeno vprašanje izgine.

**Krog:** vsako vozlišče ima svoje zastavice za prekinitev. Večerjeva veriga kratkih potrditev in umaknjenih vprašanj (b7f29eb, a4f82e8, 105de10, 601e288) je popravljala eno zastavico za drugo.

**Kandidat:** prekinitev je en dogodek z enim pravilom: kar ni bilo slišano do konca, ni izrečeno. Odprta vprašanja ostanejo odprta. Ena koda namesto zastavic po vozliščih. Povezano s 7.

### 14. `pravilo-v-promptu-izgubljeno-ali-protislovno` — 18 (Jana 12, Jože 3, Večer 3), ponavljanje 10
**Primera:**
- c89a4bf (Večer): pravilo »NI čas dogodka« je izginilo pri krajšanju.
- 3030b10 (Jana): načelo 3 (vprašaj) in načelo 4 (zapiši takoj) za isti primer.

**Krog:** krčenje in razrez promptov sta pravila tiho izgubljala, opazili smo jih šele v klicu (Jana db6e133, bf6ed8d, af4e3c8 v dveh dneh).

**Kandidat:** vsako pravilo prompta ima vsaj en scenarij. Prompt se sme krčiti šele, ko so vsi zeleni.

### 15. `vprasanje-v-zanki` — 15 (Jože 8, Jure 2, Prebil 2, Večer 1, FD 1, Jana 1), ponavljanje 4
**Primera:**
- 6d9d123 (Jože): stara vprašanja po vsaki izjavi, šestkrat.
- 72dc043 (Jure): zanka pri »še tatarska omaka«.
- f2c18bf (Jože): trikrat »imamo več možnosti«.

**Krog:** pravilo proti ponovitvi je pokrivalo eno vrsto vprašanj za drugo (pečenost in teža, nato izbira jedi f2c18bf, nato vsa vprašanja c2e8e0b).

**Kandidat:** stanje vprašanj v jedru (kaj, kolikokrat, s katerimi besedami), ena meja ponovitev in druga oblika ob ponovitvi. Danes pravilo gleda samo zadnje vprašanje (c2e8e0b).

### 16. `jed-dvakrat-na-listku` — 15 (Jože 14, Jure 1), ponavljanje 7
**Primeri:**
- 9640545: »en ocvrti sir« postane petkrat ocvrti sir.
- 1618050: »… potem bi pa še en ribeye steak.« postane »Dvakrat Ribeye Steak ameriški«.
- 9b521d1: gost reče samo »Ja.«, jed pride na listek drugič.

**Krog in kandidat:** po pregledu podvajanja (drug agent, 20. 11.) jedro vsak ponovljen `dodaj` sešteje brez dokaza, da gre za nov kos. Zato ena vrata v jedru: »dokaz za nov kos«.

**Pojasnilo k štetju:**
- Popravek količine »ne, ne petkrat sir, enkrat« (e19495f) sem dal v to družino, ker je vzrok isti seštevanje v jedru.
- Pomfri pri siru sem dal v ločeno družino 22, ker je vzrok drug (katalog ne ve, da je priloga že v jedi). S tem odstopam od primera v nalogi, ki je pomfri štel sem.
- Pad thai (20. 11.) še ni commitan, zato ga v tabeli ni.

### 17. `notranje-besedilo-na-glas` — 14 (Jana 10, Jože 4), ponavljanje 8
**Primera:**
- a070618: »Poslal sem party_size 4.«
- cc96b21 (Jože): model gostu izreče lastno napako.

**Krog:** seznam prepovedanih fraz se širi: angleške, slovenske, imena polj, navodila, celo homoglifi (1449a5b).

**Kandidat:** obrni preverbo. V glas gre samo besedilo, ki prestane pozitivno preverbo. Seznam imen polj in orodij se ustvari samodejno iz sheme, ne ročno.

### 18. `zunanji-ponudnik` — 12 (Jana 5, Jože 3, Večer 2, skupno 2), ponavljanje 2
**Primera:**
- 6482ec4: Soniox 401.
- fc7fa0f in 74db35e: isti popravek dvakrat (Entrim pošlje dve jedi v enem kosu, »Radenska pa Fanta«).

**Krog:** ni verige zakrp, a isti popravek je bil narejen dvakrat na dveh mestih.

**Kandidat:** dimni test pogodbe za vsakega ponudnika ob zagonu in ena izvedba v skupnem modulu.

### 19. `oddaja-odloci-model` — 9 (Jana 5, FD 2, Jure 1, Prebil 1), ponavljanje 5
**Primera:**
- 651ccc3 (Jana): »Rezervacija je potrjena. Nasvidenje.« pred oddajo.
- 8b2a072 (Jure): »Naročilo je oddano«, preden je bilo res oddano.

**Krog:** vsak agent je odkril isto posebej (Jana 14. 10., FD 5. 11., Jure 13. 11.), ker rešitev ni bila skupni modul.

**Kandidat:** stanje oddaje samo v kodi. Stavke o oddaji in koncu govori koda po dejanski oddaji, kot to že dela zapornica.

### 20. `vprasa-za-znan-podatek` — 7 (Jana 6, FD 1), ponavljanje 5
**Primera:**
- 9a531bb (Jana): »Na katero številko vam pošljemo potrditev po SMS-u?«, čeprav je številka znana.
- 54a1166 (FD): po »Vsi sedem hodov« vpraša »Za katerega gosta je to?«.

**Krog:** pravilo v promptu se je zaostrovalo v štirih dneh (785b551, 19b816c, 616ee65), dokler ga ni prevzela koda.

**Kandidat:** filter vprašanj po znanih poljih v kodi (616ee65 je to že začel). Pravila v promptu so pogojna.

### 21. `prepis-brez-prilagoditve` — 5 (Prebil 2, FD 1, Jože 1, skupno 1)
**Primera:**
- 779e752 (FD): moški glas reče »zabeležila«.
- c3d41d5 (Prebil): obrnjena polarnost »ne«.

**Krog:** ni verige zakrp; vsakič druga točka, odvisna od agenta.

**Kandidat:** zemljevid modulov v gradnja-agentov za vsak modul našteje, kaj je odvisno od agenta (spol, polarnost, časi, ključi nastavitev). Prepis brez preverbe teh točk ne gre skozi.

### 22. `priloga-ze-v-jedi` — 5 (Jure 4, Jože 1), ponavljanje 4
**Primera:**
- 2a63988 (Jure): »cvrt sir s pomfrijem« doda še samostojni pomfri.
- 2e9f926 (Jože): dollar chips, ki so že v perutničkah.

**Krog:** pri Juretu štirje commiti v dveh urah 18. 11. (2a63988 → 70cf6a0 → 6ca86f0 → 5cdce29), vsak je popravljal posledico prejšnjega.

**Kandidat:** podatek `vkljuceno` v vseh katalogih in ena pot v jedru. Po pregledu podvajanja je pri Juretu že rešeno v podatkih.

`drugo` (19): mešani commiti z več napakami ali brez opisa (npr. b27d820 »štirje popravki jedra«). Hook mora tudi `drugo` šteti kot družino, sicer je izhod v sili.
