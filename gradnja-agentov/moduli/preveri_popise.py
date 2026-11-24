#!/usr/bin/env python3
"""Preveri popise v tej mapi (`joze-*.md`, `prevzem-samo-podatki.md`) proti čistemu izvozu Jožetovega commita.

Uporaba:
  mkdir /tmp/joze-izvoz && git -C <worktree joze-sproti> archive abcfdc4 | tar -x -C /tmp/joze-izvoz
  python3 preveri_popise.py /tmp/joze-izvoz

Preveri: (1) vsaka `pot:vrstica` obstaja in vrstica ni prek konca datoteke; (2) vsak `tests/...py::ime` obstaja kot `def ime`;
(3) prešteje zmožnosti (ID `XXX-nn`), vrstice z »ni testa« in vrstice `VEZ-*` po kategoriji. Nič ne zažene in ničesar ne spremeni.
Izhodna koda 0 = vse poti in testi obstajajo.
"""
import collections
import glob
import os
import re
import sys

MAPA = os.path.dirname(os.path.abspath(__file__))
PREDPONE = r"(?:govor|jedro|oddaja|vhodi|nastavitve|prompti|scripts|tests|deploy)"


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__)
        return 2
    koren = sys.argv[1]
    teste = {}
    napake = []
    skupaj = collections.Counter()

    def vrstic(pot):
        try:
            with open(os.path.join(koren, pot), encoding="utf-8", errors="replace") as f:
                return sum(1 for _ in f)
        except OSError:
            return None

    def ima_test(pot, ime):
        if not os.path.exists(os.path.join(koren, pot)):
            return False
        if pot not in teste:
            teste[pot] = open(os.path.join(koren, pot), encoding="utf-8").read()
        return re.search(r"def " + re.escape(ime.split("::")[-1]) + r"\b", teste[pot]) is not None

    for datoteka in sorted(glob.glob(os.path.join(MAPA, "joze-*.md")) + glob.glob(os.path.join(MAPA, "prevzem-samo-podatki.md"))):
        ime_d = os.path.basename(datoteka)
        zm = nt = 0
        vez = collections.Counter()
        for vrstica in open(datoteka, encoding="utf-8"):
            m = re.match(r"\|\s*((?:VEZ-)?[A-Z]{3}-\d+)\s*\|", vrstica)
            id_ = m.group(1) if m else "-"
            if m and id_.startswith("VEZ-"):
                if ime_d.startswith("joze-"):   # v dodatku `prevzem-samo-podatki.md` so iste vrstice v drugi obliki: tam se štejejo samo poti
                    celice = [c.strip() for c in vrstica.strip().strip("|").split("|")]
                    vez[celice[3] if len(celice) > 3 else "?"] += 1
            elif m and ime_d.startswith("joze-"):
                zm += 1
                nt += "ni testa" in vrstica.lower()
            for pot, st in re.findall(r"`?(" + PREDPONE + r"/[\w./-]+\.(?:py|yaml|txt|md|sh)):(\d+)", vrstica):
                n = vrstic(pot)
                if n is None:
                    napake.append((ime_d, id_, "pot ne obstaja", pot))
                elif int(st) > n:
                    napake.append((ime_d, id_, "vrstica prek konca datoteke", f"{pot}:{st}"))
            for pot, t in re.findall(r"`?(tests/[\w./-]+\.py)::([\w:]+)", vrstica):
                if not ima_test(pot, t):
                    napake.append((ime_d, id_, "test ne obstaja", f"{pot}::{t}"))
        print(f"{ime_d}: zmožnosti {zm}, brez testa {nt}, VEZ {sum(vez.values())} {dict(vez)}")
        skupaj["zmožnosti"] += zm
        skupaj["brez testa"] += nt
        skupaj["VEZ"] += sum(vez.values())
    print("SKUPAJ", dict(skupaj))
    for n in napake:
        print("NAPAKA", *n)
    print(f"napak: {len(napake)}")
    return 1 if napake else 0


if __name__ == "__main__":
    sys.exit(main())
