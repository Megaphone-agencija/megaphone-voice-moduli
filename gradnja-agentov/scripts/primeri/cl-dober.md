# Primer dobrega CL: izmišljeni agent »Servis Zeleni« (sprejem naročil za servis koles)

Primer za preverjalnik (`scripts/preveri_cl.py`). Podatki so izmišljeni.

## 1. Obseg (SZ-OB)

| ID | Zahteva (pričakovano vedenje in primer) | Nosilec | Merilo uspeha | Test / scenarij | Status | Vir |
|---|---|---|---|---|---|---|
| SZ-OB-01 | Agent zbere težavo za vsako kolo, ne le za pnevmatike. Primer: »verižnik škripa« se zapiše kot vsaka druga težava. | LLM | V 10 od 10 scenarijev se opis zapiše brez zavrnitve | tests/test_obseg.py::test_vsaka_tezava (scenarij S-01) | potrjeno | Chebo 9. 11. |
| SZ-OB-02 | Električnih koles agent ne sprejema: pove besedilo SZ-BS-02 in zaključi brez oddaje. | Koda | Pri »e-kolo« ni nobene oddaje; izgovorjeno besedilo je dobesedno SZ-BS-02 | tests/test_obseg.py::test_ekolo_zavrnjeno | potrjeno | Chebo 9. 11. |

## 2. Povzetek in oddaja (SZ-PO)

| ID | Zahteva (pričakovano vedenje in primer) | Nosilec | Merilo uspeha | Test / scenarij | Status | Vir |
|---|---|---|---|---|---|---|
| SZ-PO-01 | Povzetek sestavi in prebere koda iz shranjenih podatkov, model ga ne piše. | Koda | Besedilo povzetka je enako izhodu funkcije povzetka v 100 % scenarijev | tests/test_povzetek.py::test_povzetek_iz_kode | potrjeno | Chebo 9. 11. |
| SZ-PO-02 | »Ja« po slišanem povzetku odda natanko enkrat. | Koda (podpora: Glasovni sloj) | 0 oddaj brez slišanega povzetka, 1 oddaja po »ja«, 0 dvojnih oddaj v 20 ponovitvah | tests/test_oddaja.py::test_enkratna_oddaja | potrjeno | Chebo 9. 11. |
| SZ-PO-03 | Dvoumen odgovor (»hm«) ni potrditev; agent razjasni. | LLM | »hm« in molk v 10 od 10 ponovitev ne sprožita oddaje | scenarij S-07 (posnet model) | iz virov | klic 2 |

## 3. Dobesedna besedila (SZ-BS)

| ID | Zahteva (pričakovano vedenje in primer) | Nosilec | Merilo uspeha | Test / scenarij | Status | Vir |
|---|---|---|---|---|---|---|
| SZ-BS-02 | Besedilo za e-kolo: »Električnih koles ne servisiramo. Poiščite specializiran servis.« | Vsebina | Besedilo v nastavitvah je dobesedno enako temu stavku | tests/test_besedila.py::test_sz_bs_02 | potrjeno | Chebo 9. 11. |
| SZ-BS-03 | Besedilo za brezplačni prevoz kolesa velja šele po potrditvi lastnika. | Vsebina | — | — | ne velja (čaka odločitev lastnika o prevozu) | Chebo 9. 11. |
