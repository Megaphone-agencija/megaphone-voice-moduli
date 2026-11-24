#!/usr/bin/env python3
"""Preveri popise Večera (`vecer-*.md` v tej mapi) proti čistemu izvozu Večerovega commita.

Uporaba:
  mkdir /tmp/vecer-izvoz && git -C <worktree splosna-pravila> archive c878782 | tar -x -C /tmp/vecer-izvoz
  python3 preveri_vecer_popise.py /tmp/vecer-izvoz            # preveri poti, vrstice, teste, prešteje
  python3 preveri_vecer_popise.py /tmp/vecer-izvoz --vzorec 40  # izpiše 40 naključnih navedenih vrstic (pot:vrstica -> besedilo) za ročni pregled

Preveri: (1) vsaka `pot:vrstica` obstaja in vrstica ni prek konca datoteke; (2) vsak `tests/...py::ime` obstaja kot `def ime`;
(3) prešteje zmožnosti (ID `XXX-nn`), vrstice z »ni testa« in vrstice `VEZ-*` po kategoriji. Nič ne zažene in ničesar ne spremeni.
Izhodna koda 0 = vse poti in testi obstajajo.
"""
import collections
import glob
import os
import random
import re
import sys

MAPA = os.path.dirname(os.path.abspath(__file__))
PREDPONE = r"(?:medij|mediji|kanon|rp2|scripts|tests|deploy|docs)"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    vzorec = 0
    if "--vzorec" in sys.argv:
        vzorec = int(sys.argv[sys.argv.index("--vzorec") + 1])
        args = [a for a in args if a != str(vzorec)]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__)
        return 2
    koren = args[0]
    teste = {}
    vrstice_cache = {}
    napake = []
    skupaj = collections.Counter()
    vse_poti = []

    def vrstice(pot):
        if pot not in vrstice_cache:
            try:
                with open(os.path.join(koren, pot), encoding="utf-8", errors="replace") as f:
                    vrstice_cache[pot] = f.read().split("\n")
            except OSError:
                vrstice_cache[pot] = None
        return vrstice_cache[pot]

    def ima_test(pot, ime):
        if not os.path.exists(os.path.join(koren, pot)):
            return False
        if pot not in teste:
            teste[pot] = open(os.path.join(koren, pot), encoding="utf-8").read()
        return re.search(r"def " + re.escape(ime.split("::")[-1]) + r"\b", teste[pot]) is not None

    for datoteka in sorted(glob.glob(os.path.join(MAPA, "vecer-*.md"))):
        ime_d = os.path.basename(datoteka)
        zm = nt = 0
        vez = collections.Counter()
        for vrstica in open(datoteka, encoding="utf-8"):
            m = re.match(r"\|\s*((?:VEZ-)?[A-Z]{3}-\d+)\s*\|", vrstica)
            id_ = m.group(1) if m else "-"
            if m and id_.startswith("VEZ-"):
                if ime_d != "vecer-samo-podatki.md":
                    celice = [c.strip() for c in vrstica.strip().strip("|").split("|")]
                    vez[celice[3] if len(celice) > 3 else "?"] += 1
            elif m and ime_d != "vecer-samo-podatki.md":
                zm += 1
                nt += "ni testa" in vrstica.lower()
            for pot, st in re.findall(r"`?(" + PREDPONE + r"/[\w./-]+\.(?:py|yaml|txt|md|sh|json|html|js|conf|service|yml|example)):(\d+)", vrstica):
                v = vrstice(pot)
                vse_poti.append((ime_d, id_, pot, int(st)))
                if v is None:
                    napake.append((ime_d, id_, "pot ne obstaja", pot))
                elif int(st) > len(v):
                    napake.append((ime_d, id_, "vrstica prek konca datoteke", f"{pot}:{st}"))
            for pot, t in re.findall(r"`?(tests/[\w./-]+\.py)::([\w:]+)", vrstica):
                if not ima_test(pot, t):
                    napake.append((ime_d, id_, "test ne obstaja", f"{pot}::{t}"))
        if ime_d != "vecer-samo-podatki.md":
            print(f"{ime_d}: zmožnosti {zm}, brez testa {nt}, VEZ {sum(vez.values())} {dict(vez)}")
        skupaj["zmožnosti"] += zm
        skupaj["brez testa"] += nt
        skupaj["VEZ"] += sum(vez.values())
    print("SKUPAJ", dict(skupaj), "navedenih pot:vrstica", len(vse_poti))
    for n in napake:
        print("NAPAKA", *n)
    print(f"napak: {len(napake)}")
    if vzorec:
        random.seed(1)
        for ime_d, id_, pot, st in random.sample(vse_poti, min(vzorec, len(vse_poti))):
            v = vrstice(pot)
            if v and st <= len(v):
                print(f"{ime_d} {id_} {pot}:{st} -> {v[st-1].strip()[:150]}")
    return 1 if napake else 0


if __name__ == "__main__":
    sys.exit(main())
