# Poslovni checklist: <agent> (<datum>)

Različica: <n>. Potrdil: <Chebo, datum>. Viri: <seznam: odločitve, klici, spletna stran naročnika, intervju>.
Agent dela (3 vrstice): <kaj sprejme, kaj zapiše/odda, česa ne sme obljubiti>.

## Potek običajnega klica
| Korak | Kaj se zgodi | Pogoste izjeme (ID zahtev) |
|---|---|---|
| 1. Pozdrav | <…> | <…> |

## 1. Obseg (<PR>-OB)
| ID | Zahteva (pričakovano vedenje in primer) | Nosilec | Merilo uspeha | Test / scenarij | Status | Vir |
|---|---|---|---|---|---|---|
| <PR>-OB-01 | <kaj agent dela in česa ne; primer> | <Koda/LLM/Glasovni sloj/Vsebina> | <merljivo> | <test ali scenarij> | <status> | <vir> |

## 2. Pozdrav in pričakovanja (<PR>-PZ)
(isti stolpci)

## 3. Zajem podatkov in njihova veljavnost (<PR>-ZA)
(isti stolpci; vsako polje posebej: obvezno/neobvezno, vir podatka, kaj če gost popravi)

## 4. Vsebina domene (<PR>-<DO>): termin, naročilo, vozilo, naslov …
(isti stolpci)

## 5. Čas in koledar (<PR>-CS)
## 6. Povzetek, potrditev in oddaja (<PR>-PO)
(povzetek sestavi koda; kdaj je oddaja dovoljena; natanko enkrat; neznan izid)
## 7. Popravki in odvisnosti (<PR>-PP)
## 8. Zapis, pošta, hramba (<PR>-PM)
## 9. Zaključek in tišina (<PR>-ZK)
## 10. Napotitve in vprašanja izven poteka (<PR>-NP)
## 11. Kdo govori: koda ali model (<PR>-KG)
## 12. Ritem, prekinitve (<PR>-RI)
## 13. Kakovost: kapitalne napake (<PR>-KV)
(merilo agenta: kapitalno / spodrsljaj; glej `pravila.py`)
## 14. Zunanje odvisnosti (<PR>-ZU): API, naročnikovi podatki, hramba, pravna podlaga

## Dobesedna besedila (<PR>-BS)
Besedila izgovori koda. Isti stolpci: Nosilec `Vsebina`, Merilo »v nastavitvah dobesedno enako temu stavku«, Test = test besedil.
| ID | Zahteva (kje + dobesedno besedilo v »…«; `[…]` je podatek iz klica) | Nosilec | Merilo uspeha | Test / scenarij | Status | Vir |
|---|---|---|---|---|---|---|
| <PR>-BS-01 | pozdrav: »<besedilo>« | Vsebina | <merilo> | <test> | <status> | <vir> |

## Scenariji (S) in dokazi
| ID | Kaj gost reče / kaj se zgodi | Pričakovan izid | Zahteve (ID) | Vir (klic, datum) |
|---|---|---|---|---|
| S-01 | <…> | <…> | <ID, ID> | <…> |

## Konflikti med viri
| ID | Konflikt | Rešitev (velja novejša izrecna Chebova odločitev) |
|---|---|---|
| K-01 | <…> | <…> |

## Znane napake iz klicev, ki jih mora rešitev preprečiti
| ID | Kaj se je zgodilo (klic, obrat) | Zahteve (ID) | Regresijski scenarij |
|---|---|---|---|
| Z-01 | <…> | <ID> | <S-xx> |

## Odprta vprašanja za Cheba
| ID | Vprašanje | Zakaj je pomembno | Predlog |
|---|---|---|---|
| O-01 | <…> | <…> | <…> |

## Zapora »CL zaprt«
- [ ] 0 vrstic `ODPRTO` v tabelah zahtev, `preveri_cl.py` brez napak.
- [ ] Vsaka zahteva ima nosilca, merilo in test ali scenarij.
- [ ] Chebo je potrdil CL (datum, različica).
