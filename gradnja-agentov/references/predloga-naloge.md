# Predloga naloge (brief) za podagenta in za Codex

Naloga nastane **iz CL** (zahteve po ID), pogodbe in zemljevida modulov, ne iz proze. Pišeš jo ti kot orkestrator in zanjo odgovarjaš: izvajalec ne vidi hooka, ne pozna CLAUDE.md in ne ve, česa ne sme izumiti. Brez izpolnjenih razdelkov 2 do 5 naloge ne pošlji. Pri popravku napake je obvezna tudi vrstica `Vir:` (razdelek 1), pri prepisu/gradnji modula ali agenta vsaj ena CL oznaka (razdelek 2); brez tega hook `podagent-pravila.py` klic zavrne.

Uporabi za: podagent Sonnet/Haiku (kratek odmerek dela), Codex (izvajalec ali pregledovalec; razdelek 9 dodatno). Zapiši jo v datoteko in jo daj izvajalcu kot pot; v pogovor jo prilepi samo, če je kratka.

---

## Predloga (kopiraj in izpolni)

```markdown
# Naloga: <agent> — <kaj, z besedami za Cheba> (<datum>)

## 1. Cilj
<2–3 stavki: kaj gost/Chebo vidi drugače po nalogi; en konkreten primer pogovora.>
Vir: <samo pri popravku napake; obvezno. Pravi klic (id, datum in ura) ali tek pravega modela z DOBESEDNO gostovo izjavo. Vrstica se začne z `Vir:`.>
Fazna zapora: CL <ime/različica> je potrjen (Chebo, <datum>); pogodba <pot> potrjena; ta naloga je skica <pot>, potrjena <datum>.

## 2. Zahteve iz CL (po ID)
| ID | Zahteva | Nosilec | Merilo uspeha | Test / scenarij |
|---|---|---|---|---|
| <ID> | <prepis iz CL> | <…> | <…> | <…> |
Naloga za prepis/gradnjo modula ali agenta (prepiši, prevzemi, prenesi, »iz Jane«, nov agent) mora navesti vsaj eno CL oznako (oblika `P-VO-01`, `KP-BS-27`, `M-ID-13`, `KS-PO-08`); brez nje je naloga zavrnjena.
Samo te zahteve spadajo v nalogo. Kar ni v tabeli, ne popravljaj; če se ti zdi, da manjka zahteva, jo napiši v poročilo (ne izumljaj pravila).

## 3. Moduli: kaj prepisati (obvezno; vir: references/moduli.md)
| Funkcija | Vir (datoteka @ commit) | Kaj prilagoditi | Česa NE pisati na novo |
|---|---|---|---|
| <npr. povzetek iz kode> | `<oznaka:pot>` @ `<sha>` | <samo nujno: polja, besedila> | <npr. sestave povzetka, števca poskusov> |
Kopiraj iz **commita**, ne iz necommitanega dela. Vsako kopijo zapiši v `IZVOR.json` (repository, commit, source_path, source_sha256, status prevzeta/prilagojena, adaptation).
**Novo (ni ustreznika v nobenem agentu):** <seznam; za vsako zapiši, kje si iskal>. Vse ostalo je prepis.

## 4. Merilo tega agenta
<prilepi izpis `python3 ~/.claude/skills/gradnja-agentov/scripts/pravila.py --projekt <agent>`: FILTER, mehanizmi, kakovost, preverjanje. Za Večer `--projekt vecer`.>
Najdbe in popravke razvrsti po FILTRU pred delom. Novo pravilo v prompt je zadnja možnost; meja dolžine osnova + vozlišče: 5–6k znakov (največ ~10k).

## 5. Testi
- Ukaz: `<npr. PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:govor:tests .venv/bin/python -m unittest discover -s tests -t . -v>`
- Pred začetkom zeleni: <št. testov>. Po nalogi mora biti zelenih: <št.> + novi.
- Za vsak ID iz razdelka 2 mora obstajati test z komentarjem `# CL: <ID>`; test je napisan **pred** popravkom in na starem stanju pade, kjer gre za popravek napake (reprodukcija). Test reprodukcije gre **skozi cel cevovod pogovora** (glej spodaj) z gostovo izjavo iz klica in nosi komentar `# klic: <id klica ali scenarija>`. Commit popravka nosi v telesu vrstici `Družina: <ime iz /home/chebo/MAIOS/00-system/napake/druzine.md>` in `Reprodukcija: <pot/do/test_x.py::Razred::test_ime>` (ali `Reprodukcija: ni — <razlog>`), pred zadnjo vrstico `Co-Authored-By` (razdelek 8). To preveri `scripts/pripravljeno.py`; šteje samo padec preverbe (failure), ne sesutja testa (error, npr. napaka pri uvozu ali klic funkcije, ki je na starem stanju ni).
- Test mora imeti isti »zdaj« kot backend (zamrznjen datum je dal lažne napake).
- Cel pogovor skozi cevovod (`<test iz moduli.md, razdelek Testno ogrodje>`), ne samo enote.
- **Brez pravega modela:** ne kliči OpenRouterja in ne poganjaj celotnega nabora testov. Delaj lokalno (posneti odgovori modela, skriptirani zapisi), na primerih iz Chebovih klicev, vsak test čez vsaj DVE vozlišči (prenos zahtev med vozlišči). Pravi model požene samo orkestrator, enkrat, ko je cel popravek gotov (tik pred »kliči«): Chebov klicani scenarij 3×.
- Ne poganjaj plačljivih klicev/modelov brez izrecnega dovoljenja v tej nalogi: <dovoljeno/ne>.

## 5a. Druge oblike iste napake (obvezno pri popravku napake)
Napaka, ki jo popravljaš, je ena oblika. Gost bo isto rekel tudi drugače. Popravek se začne z vrstico `Vir:` (razdelek 1): brez pravega klica ali teka pravega modela z gostovo izjavo napake morda ni (testni gost je na »Ste mislili Steak, Steak Hugo ali Steak na rukoli?« odgovoril »Ja.«, kar ni realno, in skoraj smo popravljali neobstoječo napako).
Oblike niso nove napake: so test, ali popravek odpravi vzrok. Napaka, ki jo popravljaš, je FILTER že prestala; oblika, ki pade zaradi drugega mehanizma, gre v poročilo kot »izven obsega« (točka 6), ne v popravek.
Preden popravljaš:
1. Zapiši vsaj 10 drugih oblik iste situacije. Najprej vzemi prave gostove izjave iz tabele
   ontologije (`/home/chebo/MAIOS/00-system/napake/popravki-2026-11-20.csv`, stolpca `druzina` in
   gostove_besede, ista družina, vsi agenti). POZOR: stolpec vsebuje tudi
   agentove stavke; vzemi samo, kar je rekel gost. Šele nato si oblike izmisli. Pokrij:
   običajnega gosta, gosta, ki govori nemarno (polovični stavki, »mhm«, popravek sredi stavka,
   napačen prepis ASR), gosta, ki reče dve stvari naenkrat (»Ja, ampak …«).
2. **Nasprotne oblike:** zapiši še 3–5 stavkov, ki so podobni po besedah ali začetku, a morajo dati drug izid (zavrnitev, vprašanje, popravek, slovo). Za »Ja, lahko daš.« npr. »Ja, ampak brez čebule.«, »Ja … ne, čakaj.«, »Ja … ne, čakaj, letnik je napačen.«. (»V redu, hvala, nasvidenje.« ni slovo: pomeni DA, Chebo 24. 11. 2026.) Tudi tu najprej prave gostove izjave iz tabele. Vsaka je test z `# nasprotna: <n>` in mora biti zelena po popravku. Če pričakovanega izida ni v CL, je to predlog odločitve (točka 5), ne test. Če izid odloča odziv modela, velja kot pri točki 3: ne skriptiraj, naštej pod »za pravi model«.
3. Oblike razdeli na dve skupini:
   a) KODA ODLOČI iz gostovega besedila (razvrstitev odgovora, iskanje v katalogu, števniki,
      vezava na vprašanje): vsako zapiši kot test (`# CL: <ID>`, `# oblika: <n>`) in jo spravi
      skozi enako kot glavni test.
   b) ODVISNO OD ODZIVA MODELA (kaj model pošlje v orodje): odziva modela si NE izmišljuj
      in ga ne skriptiraj. Obliko samo naštej v poročilu pod »za pravi model«.
4. Obliko iz skupine a) smeš pustiti rdečo samo, če bi zelena nasprotovala CL ali Chebovi
   izrecni odločitvi.
5. Če oblika zahteva odločitev, ki je ni v CL: NE implementiraj je. V poročilo napiši obliko,
   predlagano privzeto vedenje in zakaj (razdelek 2: ne izumljaj pravila).
6. Oblike, ki rabijo DRUG mehanizem kot napaka, ki jo popravljaš, ne popravljaj. Zapiši jih
   kot »izven obsega: <oblika> — <zakaj drug mehanizem>«.
7. Dodajanje oblik na seznam besed ni popravek vzroka. Če tvoj popravek za vsako obliko
   doda svojo vrstico v seznam, to napiši v poročilo.
8. **Nerealne oblike:** izmišljena oblika je dovoljena, ne sme pa biti nerealna ali brez sobesedila (npr. »Ja.« na vprašanje »Kakšen šnicl boste?«). Nerealna oblika ne šteje in ne sproži popravka. Nov korak (vprašanje agenta), za katerega nimaš realnega gostovega odgovora, je »vrzel orodja« ali predlog odločitve (točka 5), ne test.
Oblike in nasprotne oblike so preverbe, ne seznam za kodo. Popravek, ki katerokoli od njih zapiše kot niz v kodo ali v seznam besed, ni popravek vzroka (Chebovo načelo: splošno pravilo, ne naštevanje).
Seznam vseh oblik (številka, besedilo, skupina a / b / nasprotna, status) daj v poročilo pod naslov `## Oblike`. Statusi oblik: `zelena / rdeča / odločitev (točka 5) / za pravi model (skupina b) / izven obsega / nerealna (točka 8) / vrzel orodja (točka 8)`.

## 6. Omejitve
- Veja: `<ime>`. **Brez** merge v main, push, namestitve na strežnik, spremembe Asterisk/dialplana, preusmeritve številke: to naredi samo Chebo po svojem »namesti«.
- Skrivnosti (ključi, env datoteke) nikoli v repozitorij, poročilo ali pogovor; ključe samo preveri, ali so nastavljeni.
- V drugih agentih samo beri. Ne uvajaj runtime povezav med agenti.
- **Prompt:** pred vsako spremembo prompta preberi CEL prompt (osnova + vsa zadevna vozlišča; ne grep, ne odlomek, ne spomin) in preveri, da sprememba ne nasprotuje nobeni drugi vrstici, tudi pogojnim pravilom drugje. Za posredovane naloge to zahtevo ponovi.
- Datotek ne ustvarjaj na Namizju. Delovne datoteke v scratchpad/temp, trajna poročila v repo (`docs/porocila/`).

## 7. Poročilo
- **Celotno poročilo v datoteko:** `<pot, npr. <repo>/docs/porocila/<ime>-<datum>.md>`.
- Meni vrni **največ 15 vrstic**: izid (opravljeno/delno/ne), spremenjene datoteke, testi (ukaz, koliko zelenih od koliko, SHA), odprto/vprašanja, pot do poročila.
- **Ne pokrije:** oblike in primeri, za katere veš, da popravek ne dela, in zakaj (ali »nič znanega«). Ta vrstica gre tudi v 15 vrstic, ki jih vrneš.
- **`## Klicni list`** (5–8 vrstic, za Cheba, preprosta slovenščina): (1) izvirni Chebov stavek iz klica, ki je padel, in kaj mora zdaj slišati — obvezno; (2) neobvezno ena podobna in ena nasprotna oblika, najraje iz pravih gostovih izjav, in kaj mora slišati; (3) vrstica »Ne pokrije«.
- Predlogi odločitev (5a točka 5): vsaka v svoji vrstici `Predlog odločitve: <oblika> → <privzeto vedenje> — <zakaj>`.
- Loči: kaj si preveril ti, kaj si prevzel brez preverjanja. Ne trdi, da deluje v živo, če si zagnal samo lažne ponudnike.

## 8. Jezik
- Commiti, PR, README: preprosta slovenščina. Prva vrstica commita in naslov PR: kaj se spremeni za gosta ali Cheba (npr. »Prebil: po slišanem povzetku ‚ja' odda«), brez imen funkcij. Opis PR: 2–4 povedi z zgledom, nato razdelek »Tehnično«.
- Vrstice v telesu commita, tik PRED `Co-Authored-By` (hook `00-system/napake/git-hooks/commit-msg` jih preverja; ključ s šumnikom git ne razume kot trailer, zato jih piši kot samostojne vrstice):
  - `Vrsta: popravek` (popravek napake glasovnega agenta) + `Družina: <slug>` (točno en `slug` iz `00-system/napake/druzine.json`; če nobena ne ustreza, `drugo`);
  - ali `Vrsta: ni-popravek` + `Podvrsta: funkcija|test|dokument|izvor|cl|infra|refaktor|orodje`; pri `ni-popravek` brez »(prej: …)« v prvi vrstici;
  - `Prenos-iz: <agent>` samo če je to prenos že popravljenega iz drugega agenta (tak commit se ne šteje kot nova napaka).
  - Ob vsakem popravku `stej.py` pogleda zadnjih 10 popravkov (vseh 6 repozitorijev); družina ≥3 odpre kartico »Analiza vzroka«.
- Zadnja vrstica commita: `Co-Authored-By: <kot določa sistemsko opozorilo seje>`; opis PR se konča z oznako, ki jo določa seja.
```

## Dodatek za Codex (pripni razdelek 9)

```markdown
## 9. Codex
- Delaj v Slack niti projekta, ne na novi; vsebinski odgovor v isto nit. Najprej potrdi prevzem v niti.
- Vsako najdbo razvrsti po FILTRU (korak 0 in 2). **Blokator** označi samo, če najdba prestane korak 0 (dokaz iz pravega ali Chebovega klica oziroma ponovljiv padec) in je kapitalna po merilu agenta. Najdba s sintetičnimi podatki ali redkim robom je zapis v backlog, ne blokator.
- Pregled kopije: primerjaj z izvorom iz IZVOR.json (diff), ne z domnevo.
```

---

## Navodila orkestratorju (ne gredo v nalogo)

1. **Model in trud:** vsak popravek kode (tudi ena vrstica), diagnoza in razmišljanje → Sonnet, effort high. Delo brez razmišljanja (vnos besedil po predlogi, kopiranje, zagon testov) → Sonnet low ali Haiku. Effort vedno izrecno. (Vir: hook `pravila-vrata.py`, 21.–22. 10.)
2. **Vzporedni podagenti** samo za ločene datoteke; delo v isti datoteki gre enemu zaporednemu.
3. **Prompt:** zahtevo »preberi cel prompt« (CLAUDE.md, »Voice Agent Prompt Edits«) ponovi v vsaki nalogi, ki se je dotika. Izvajalec jo sicer ne pozna.
3a. **Zapori v hooku (24. 11. 2026):** `podagent-pravila.py` zavrne klic podagenta, ki (a) popravlja napako glasovnega agenta in nima vrstice `Vir:`, ali (b) prepisuje/gradi modul ali agenta za glasovne agente in nima CL oznake. Raziskava, branje in razvrščanje gredo skozi. Izvajalec hooka ne vidi: vrstico `Vir:` in CL oznake napiši v nalogo.
4. **Ne verjemi poročilu:** po končani nalogi sam poženi teste in preberi diff (Opus je QA). Poročilo ni dokaz implementacije. Preberi tudi izpis padca testa reprodukcije na starem stanju (`pripravljeno.py` ga izpiše) in ga primerjaj s prepisom klica: simptom mora biti isti.
5. **GitHub jezik** (PR, commit, README): pravilo »razumljiv jezik« iz Obsidiana ponovi v vsaki nalogi, ki commita ali odpira PR (razdelek 8).
6. Nit pred »čakam Codexa« preberi (Slack nit projekta); Chebo ne lepi sporočil.
7. **Skrite oblike:** preden pošlješ nalogo popravka, Opus napiše 3–5 drugih oblik iste napake (vsaj ena od skritih oblik je nasprotna) samo kot seznam stavkov (gostova izjava + pričakovano vedenje) v `/home/chebo/MAIOS/00-system/pripravljeno/<ime repozitorija>/skrite-<veja>.md`. Testno datoteko `skrite-<veja>.py` iz seznama naredi ločen podagent (Sonnet low, ne popravljalec in ne v njegovi seji), ker Opus ne piše kode (CLAUDE.md »Orchestration«). Popravljalec seznama in testa ne vidi (ne omenjaj ju v nalogi). `pripravljeno.py --skrite` požene test na vrhu veje.
8. **»Česa ne pokrije?«:** po poročilu podagentu prek SendMessage pošlji »Katerih oblik gostovega odgovora tvoj popravek ne pokrije? Naštej konkretne stavke.« Primerjaj z njegovim `## Oblike` in s skritimi oblikami; vsaka nova oblika postane test ali vrstica v backlogu, preden popravek gre naprej.
9. **Predlogi odločitev:** vsak predlog najprej preveri v PLUR in Obsidian `Agent-Shared/decisions-log.md`; že odločeno označi »že odločeno« z virom in ne sprašuj znova. Ostale daj Chebu. Predloge iz vseh projektov zberi in jih Chebu pošlji enkrat na dan v enem sporočilu, oštevilčene, vsak s priporočilom, da lahko odgovori »1 da, 2 ne, 3: …«. Takoj samo, če odločitev blokira vejo, ki je sicer ZRELA. Vsako Chebovo odločitev zapiši v `/home/chebo/MAIOS/00-system/napake/odlocitve.csv`. Ko ima neka vrsta odločitve ≥ 20 primerov in ≥ 90 % sprejetih, Chebu predlagaj, da jo podagent odslej implementira sam; velja šele po Chebovi potrditvi, za vsako vrsto posebej (Chebo, 20. 11. 2026).
10. **Pred predajo Chebu:** `python3 ~/.claude/skills/gradnja-agentov/scripts/pripravljeno.py <repo> ...` mora izpisati ZRELO. NI ZRELO ne gre v »čaka Cheba«.

11. **Začasno: primerjava Sonnet proti Opusu (Chebo, 20. 11. 2026; velja za naslednjih 5 popravkov napak, nato točko odstrani).**
    - Isto nalogo (isti razdelki 2–5a, ista beseda) dobita dva podagenta vzporedno: Sonnet (effort high) in Opus (effort high), vsak v svojem worktreeju na svoji veji `<veja>-sonnet` in `<veja>-opus`. To je izjema od točke 1 (koda → Sonnet) in od pravila »Opus ne piše kode«, ki velja samo za orkestratorja; odobril jo je Chebo.
    - Skrite oblike (točka 7) so ene, za oba enake; noben podagent jih ne vidi. Skrite oblike: ena skupna datoteka `skrite-<veja>.py` (veja brez pripone -sonnet/-opus) za obe veji.
    - Na obeh vejah poženi `pripravljeno.py ... --skrite <...>.py --model sonnet-high` oz. `--model opus-high`.
    - V `/home/chebo/MAIOS/00-system/napake/primerjava-modelov.csv` zapiši vrstico za vsak model: skrite oblike (vseh, padlo), število oblik v `## Oblike`, vrstice diffa brez testov (`git diff --stat <osnova>..<veja> -- . ':!tests'`), `samo_seznam_besed` (da/ne: ali popravek za oblike le dodaja vnose v seznam besed), tokeni in čas iz obvestila podagenta, izid pripravljeno (ZRELO/NI ZRELO), `izbran`.
    - Naprej gre veja z manj padlimi skritimi oblikami; ob enakem številu manjši diff brez seznama besed. Drugo vejo pusti (ne briši), dokler Chebo ne vidi povzetka.
    - Pravi model 3× poženi samo na izbrani veji. Na neizbrani veji pripravljeno.py zaradi manjkajočega pravega modela in Codexa vrne NI ZRELO; to je pričakovano. Za primerjavo štejejo vrstice testi, reprodukcija, poročilo in skrite oblike; v CSV stolpec `pripravljeno` zapiši `NI ZRELO (brez pravega modela)`.
    - Štetje: v `/home/chebo/MAIOS/05-tasks/in-progress/2026-11-20-primerjava-sonnet-opus.md` dopiši vrstico za vsak opravljen popravek. Po 5. popravku Chebu pošlji povzetek (tabela iz CSV, tvoje priporočilo) in mu prepusti odločitev, kateri model popravlja naprej; nato točko 11 odstrani.
