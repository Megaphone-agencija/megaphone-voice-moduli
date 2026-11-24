# Namerno pokvarjen CL (za preizkus preverjalnika)

Vsaka vrstica razen prve ima eno napako (opis napake je v celici »Zahteva«). Preverjalnik mora pasti.

## 1. Obseg

| ID | Zahteva | Nosilec | Merilo uspeha | Test / scenarij | Status | Vir |
|---|---|---|---|---|---|---|
| SZ-OB-01 | Dobra vrstica: zbere težavo za vsako kolo. | LLM | V 10 od 10 scenarijev se opis zapiše | tests/test_obseg.py::test_a | potrjeno | Chebo |
|  | Brez identifikatorja. | Koda | Merilo je dovolj dolgo in konkretno | tests/test_obseg.py::test_b | potrjeno | Chebo |
| SZ-OB-01 | Podvojen identifikator. | Koda | Merilo je dovolj dolgo in konkretno | tests/test_obseg.py::test_c | potrjeno | Chebo |
| SZ-OB-03 | Nosilec manjka. |  | Merilo je dovolj dolgo in konkretno | tests/test_obseg.py::test_d | potrjeno | Chebo |
| SZ-OB-04 | Dva glavna nosilca. | Koda + LLM | Merilo je dovolj dolgo in konkretno | tests/test_obseg.py::test_e | potrjeno | Chebo |
| SZ-OB-05 | Neznan nosilec. | Model | Merilo je dovolj dolgo in konkretno | tests/test_obseg.py::test_f | potrjeno | Chebo |
| SZ-OB-06 | Merilo je vprašaj. | Koda | ? | tests/test_obseg.py::test_g | potrjeno | Chebo |
| SZ-OB-07 | Testa ni. | Koda | Merilo je dovolj dolgo in konkretno |  | potrjeno | Chebo |
| SZ-OB-08 | Test je neizpolnjen označevalec iz predloge. | Koda | Merilo je dovolj dolgo in konkretno | <test ali scenarij> | potrjeno | Chebo |
| SZ-OB-09 | Status je odprt. | Koda | Merilo je dovolj dolgo in konkretno | scenarij S-09 | ODPRTO | Chebo |
| SZ-OB-10 | Ne velja brez razloga. | Koda | Merilo je dovolj dolgo in konkretno | scenarij S-10 | ne velja | Chebo |
| SZ_OB_11 | ID v napačni obliki. | Koda | Merilo je dovolj dolgo in konkretno | scenarij S-11 | potrjeno | Chebo |
