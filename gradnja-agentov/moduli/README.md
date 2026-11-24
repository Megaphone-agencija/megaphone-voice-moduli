# Popisi modulov agenta za prevzem hrane (Jože)

Namen: da za novo restavracijo (agent za prevzem hrane) **ne bereš kode**, ampak primerjaš checklist (CL) s popisom, kaj Jožetovo jedro že zna, kaj je podatek in kaj je še vezano na J&J v kodi. Cilj Cheba: nova restavracija = zamenjava podatkov (jedilnik, sopomenke, nastavitve, besedila) v enem dnevu, brez spremembe kode.

**Stanje**: Jože `abcfdc4` (veja `joze-sproti`, 2026-11-24), Jure `468eafb` (veja `jure-zapornica`, `prevzem/`). Vse je branje kode in diff; testi **niso bili zagnani** (v okolju ni `pytest`), ujemanje imen testov je preverjeno s skripto. Jože in Jure se razvijata naprej: ob novem commitu je treba popise obnoviti (skripta spodaj pove, kaj se je premaknilo).

## Kazalo

| Datoteka | Oznake | Kaj pokriva | Zmožnosti | Brez testa | Vrstic »vezano na J&J v kodi« |
|---|---|---|---|---|---|
| `joze-jedro-narocila.md` | `NAR-`, `VEZ-NAR-` | `narocilo_joze`, `katalog_narocila`, `joze_spremembe`, `joze_priloge`, `joze_cakajoce`, `joze_dobesedno`, `joze_izgovor`, `joze_listek` (naročilo iz kataloga: postavke, količine, izbire, dodatki, priloge, popravki) | 63 | 1 | 24 |
| `joze-ujemanje-jedilnika.md` | `UJE-`, `VEZ-UJE-` | `ujemanje_jedilnika`, `menu_spotter`, iskanje jedi, pragovi, `meritev_ujemanja.py` | 38 | 1 | 12 |
| `joze-prevzem.md` | `PRE-`, `VEZ-PRE-` | `prevzem.py` (ura, okno, čas priprave), `prevzem_govor.py` (besedila in vprašanja kode) | 47 | 0 | 21 |
| `joze-govorni-tok.md` | `GOV-`, `VEZ-GOV-` | `flows.py`, zapornica, profil, filtri govora, zaključek, tišina, predaja | 89 | 0 | 31 |
| `joze-oddaja.md` | `ODD-`, `VEZ-ODD-` | `listek_backend`, `listek_eposta`, `neoddano`, povzetek, zapora oddaje, neznan izid | 35 | 2 | 20 |
| `joze-nastavitve.md` | `NAS-`, `VEZ-NAS-` | `restavracija.yaml` (vsi ključi), shema kataloga, prompti, pozdravi, preverjanje nastavitve | 29 | 2 | 24 |
| `prevzem-samo-podatki.md` | `T1`..`T10` | kaj zamenjati pri novi restavraciji (podatek ali koda), 10 tem, razlika Jure proti Jožetu, dodatek z vsemi 132 `VEZ-` vrsticami | | | 132 (skupaj) |
| `preveri_popise.py` | | preveri poti, vrstice in imena testov, prešteje zmožnosti | | | |

**Skupaj**: 301 zmožnosti, 6 brez testa (`ni testa`), 132 vrstic »vezano na J&J v kodi« (štetje s `preveri_popise.py` iz tabel, ne ocena). **Moč testov**: »brez testa« pove samo, da testa nisem našel; skripta preveri le, da imena testov obstajajo. Dodatnih 12 zmožnosti ima test, ki **ne dokazuje Jožetove žive poti**: GOV-16, 17, 23, 86, 102, 103, 105, 106 (test teče samo na Janini poti istega mehanizma; pri 102 in 103 »Jožetova pot ni preizkušena«) in PRE-03, 04, 16, 17 (testi na starem Janinem `Narocilo` ali sintetični nastavitvi). Torej 6 + 12 = 18 od 301 zmožnosti nima testa za Jožetovo živo pot; za ostalih 283 sem po imenu in telesu testa ocenil, da preverja opisano vedenje, a testov nisem zagnal. Zmožnost z oznako `(nepreverjeno)` pomeni, da vedenja nisem mogel potrditi iz kode ali testa.

Zadnji stolpec vsake zmožnosti je test (`pot::ime`) ali `ni testa`. Nekateri testi zadevajo samo Janino pot istega mehanizma (v celici pripisano »Janina pot«): ti dokazujejo mehanizem, ne Jožetove nastavitve.

## Kaj pomeni, če je nekaj »vezano na J&J v kodi«

Razdelek je v vsakem popisu. Kategorije: **IME-JEDI** (ime jedi, pijače ali skupine v kodi), **PRAVILO** (pravilo ali struktura, vezana na J&J jedilnik ali potek), **BESEDILO** (stavek, ki ga gost sliši), **ŠTEVILO** (konstanta), **REGEX** (vzorec nad izjavo), **NASLOV** (e-pošta, pot, strežnik), **IME-AGENTA** (samo poimenovanje, ne vpliva na vedenje). Vsaka vrstica ima predlog, kam v podatke. Združeno po temah in z vrstnim redom: `prevzem-samo-podatki.md`.

## Navodilo: navzkrižna primerjava CL nove restavracije s popisi

Naredi to v fazi 01/02 (ko je CL osnutek, pred nalogami za izvajalce), za vsako vrstico CL z nosilcem `Koda` ali `Vsebina` (vrstice z nosilcem `LLM` ali `Glasovni sloj` preglej enako, a za govorni tok iskanje poteka v `joze-govorni-tok.md`).

1. **Poišči vrstico v popisih.** `grep -n -i "<ključna beseda>" 04-workflows/Skills/gradnja-agentov/moduli/joze-*.md` z vsaj **dvema** različnima besedama (npr. »pečenost« in »teža«; »rok naročanja« in »narocila_do«). Če po dveh iskanjih ni zadetka, je to **manjka**, ne »pokrito«.
2. **Razvrsti v točno eno od treh:**

| Razvrstitev | Pogoj | Kaj zapišeš |
|---|---|---|
| **pokrito** | zmožnost (`XXX-nn`) obstaja **in** vsa vrednosti, ki jih CL zahteva, so podatek (yaml, katalog, besedilo: stolpec »Podatki/nastavitve«) **in** na to zmožnost ne kaže noben `VEZ-` | ID zmožnosti, ključ v yaml/katalogu, ki ga je treba izpolniti |
| **prilagoditev** | zmožnost obstaja, a (a) nanjo kaže `VEZ-` (vrednost ali pravilo je v kodi, npr. pečenost, domača kola, besedilo na listku), ali (b) CL zahteva drugačno vedenje, kot ga daje privzeto (npr. brez cen, drugačen vrstni red korakov), ali (c) zmožnost ima oznako `(nepreverjeno)` ali `ni testa` | ID zmožnosti + `VEZ-` ID + predlog iz popisa; ali je prilagoditev **podatek** (stikalo v yaml, ki ga jedro že pozna) ali **koda** |
| **manjka** | zmožnosti ni v popisih Jožeta | Če jo ima Jure, napiši vir (razdelek 3.1 v `prevzem-samo-podatki.md`: datoteka, funkcija) in »prepisati iz Jureta«; sicer »nova koda, v nalogi to izrecno napiši« (pravilo »poišči obstoječ modul«, `references/moduli.md`) |

3. **Zapiši izhod** kot dodaten stolpec ali razdelek v CL, ena vrstica na ID zahteve:

   `| P-XX-nn | pokrito / prilagoditev / manjka | NAR-12, PRE-03 | VEZ-NAR-01 | kaj zamenjati (podatek ali koda) |`

4. **Preštej**: koliko vrstic je pokritih, koliko prilagoditev (ločeno podatkovnih in kodnih) in koliko manjka. Merilo za »en dan«: **manjka = 0** in **kodnih prilagoditev = 0**. Vsaka kodna prilagoditev je razlog, da se najprej izvede ustrezna tema iz `prevzem-samo-podatki.md` (T1 do T10), ne da se kodo spreminja za to restavracijo.
5. **Pravila**: (a) zmožnost, ki ima test samo na Janini poti, štej kot pokrito z opombo; (b) »pokrito« nikoli ne pomeni, da obstaja test za novo restavracijo, ampak da obstaja mehanizem; test za CL ID dopiši po `predloga-checklista.md`; (c) ne prenašaj vrednosti J&J (cene, jedi, besedila) v novo restavracijo, čeprav so v katalogu ali yaml kot primer; (d) kar je v CL Chebova odločitev in ni v popisu, je »manjka«, tudi če je videti trivialno.

## Kar Jože nima, Jure pa (preverite, preden napišete »manjka«)

Popisi `joze-*.md` te zmožnosti **ne** vsebujejo. Jure `468eafb` (`prevzem/`) jih ima; vir za prepis (iz razdelka 3.1 `prevzem-samo-podatki.md`):

| Zmožnost | Kje pri Juretu (`prevzem/`) | Stikalo |
|---|---|---|
| Čas čakanja, ura prevzema izračuna koda, klic pred odprtjem (uro izbere gost), rok po dnevih | `jedro/moduli/cas_cakanja.py`, `jedro/klic.py` (`nastavi_cas_prevzema`, `ura_izbere_gost`, `razlog_zavrnitve`), `jedro/moduli/prevzem.py` | profil `cas_cakanja`, yaml `moduli.prevzem.cas_cakanja` |
| Povzetek brez vprašanja za dovoljenje; »Še kaj?« po vsaki izjavi; vprašanje po oddaji | `govor/flows.py` (`jure_povzetek`, `jure_po_oddaji`) | profil `povzetek_brez_vprasanja`, `se_kaj_po_vsakem`, `po_oddaji_vprasanje` |
| Povratni klic (človek, sprememba, preklic), prevezava nazaj k rezervaciji | `govor/flows.py` (razdelek »prevezava nazaj k rezervaciji in povratni klic«), `govor/prevezava_nazaj.py` | profil `povratni_klic`, `prevezava_nazaj` |
| Ponudba iz jedilnika (kaj imate za …?) brez izmišljanja jedi | `jedro/moduli/jedilnik_btc.py`, `katalog_narocila.py` (`Ponudba`), `flows.py` (`FilterVprasanj.jedi_modela`) | katalog z `jedilnik_kategorije` |
| Brez cen v rezultatih orodij, alergija kot zastavica, dodatkov ne ponuja agent | `jedro/moduli/narocilo_joze.py` | yaml `moduli.narocilo.brez_cen`, `alergija_zastavica`, `ponudi_dodatke` |
| Vključena priloga samo za isto jed (KP-NA-09) | `jedro/moduli/joze_priloge.py` | yaml `moduli.narocilo.ze_vkljuceno_samo_ista` |
| Ponovljen odgovor o različici (KP-NA-10); število brez »še« nastavi količino (KP-NA-11) | `govor/flows.py` (`razlicica_je_ponovitev`, `kolicina_skupaj_nastavi`) | besedilo `govor.ze_zapisano`; profil `kolicina_skupaj` |
| Vprašanje »K pici ali posebej?« ob enakem imenu dodatka in priloge | `jedro/moduli/narocilo_joze.py` (`_enako_ime_vprasanje`) | podatek v katalogu |
| Krajša ponovitev vprašanja (drugič, tretjič polno) | `govor/prevzem_govor.py` | yaml `govor.ponovitev_kratko` |
| Oddaja v Google Sheet, neoddano v JSONL | `oddaja/oddaja_btc.py`, `oddaja/neoddano_jsonl.py` | yaml `listek.sheet_zapis` |
| Popravki splošnega jedra (v Jožetu jih ni): beseda za »s/z« je dodatek (`menu_spotter`), lažna potrditev modela odpade, velikostne besede ob pijači, »sem se zmotil« v varovalu | `govor/menu_spotter.py`, `flows.py` (`lazna_potrditev_modela`), `katalog_narocila.py`, `varovalo.py` | brez stikala (veljajo vedno) |

## Preverjanje popisov

```bash
mkdir /tmp/joze-izvoz && git -C ~/.cache/claude-worktrees/joze-sproti archive abcfdc4 | tar -x -C /tmp/joze-izvoz
python3 04-workflows/Skills/gradnja-agentov/moduli/preveri_popise.py /tmp/joze-izvoz
```

Skripta preveri, da vsaka `pot:vrstica` obstaja (vrstica ni prek konca datoteke), da vsak `tests/...py::ime` res obstaja in prešteje zmožnosti, `ni testa` in `VEZ-` po kategoriji. Ne zažene testov in ničesar ne spremeni. Ob novem Jožetovem commitu: zamenjaj `abcfdc4`, ponovi izvoz in poženi; vrstice, ki so se premaknile, ponovno preberi.

## Kaj popisi NE pokrivajo

- Ne dokazujejo, da je koda pravilna ali da testi tečejo (testi niso bili zagnani).
- Ne zajamejo `skupno/` v Kratochwillu (urnik, jedilnik, izgovor, `tabela_sheet`); to je zunaj `prevzem/`.
- Prompte popisujem po vsebini (`joze-nastavitve.md`); novi prompt se piše iz CL (`pravila.md`), ne prepisuje.
- Mrtva koda (`narocilo.py` razen `katalog_iz_slovarja`, `jj_backend.py`, `jj_transport.py`, `katalog.yaml`, `restavracija-protokol-staro.yaml`) je označena v popisih in ni štetja zmožnosti.
