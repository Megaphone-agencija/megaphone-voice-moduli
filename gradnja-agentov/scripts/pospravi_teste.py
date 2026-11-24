#!/usr/bin/env python3
"""Pobriše ostanke testov glasovnih agentov v /tmp (Chebo 16. 11. 2026: »naj se res na koncu dneva pobriše«).

Testi Večera si delajo mape z mkdtemp(prefix="vecer-…") in jih ne pobrišejo: 13. 11. 2026 jih je bilo 39 477 (19 GB).
Hook pravila-vrata.py ob »dovolj za danes« naroči zagon te skripte.

Briše samo: vnose neposredno v /tmp, katerih ime se začne z eno od PREDPON, ki so od trenutnega uporabnika
in niso bili spremenjeni vsaj --starost minut. Ne briše nič, če ravno teče kak test (unittest/pytest).
Uporaba: pospravi_teste.py [--suho] [--starost 60]
"""
import argparse
import os
import shutil
import subprocess
import time

PREDPONE = ("vecer-",)  # novo predpono dodaj tu, ko jo najdeš pri drugem agentu
KOREN = "/tmp"


def velikost(pot):
    if os.path.isfile(pot) or os.path.islink(pot):
        return os.lstat(pot).st_size
    s = 0
    for d, _, datoteke in os.walk(pot):
        for f in datoteke:
            try:
                s += os.lstat(os.path.join(d, f)).st_size
            except OSError:
                pass
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suho", action="store_true", help="samo izpiši, nič ne briši")
    ap.add_argument("--starost", type=int, default=60, help="minimalna starost v minutah")
    a = ap.parse_args()

    teste = subprocess.run(["pgrep", "-af", "--", r"-m (unittest|pytest)|/pytest "], capture_output=True, text=True).stdout.strip()
    if teste and not a.suho:
        print("NI POBRISANO: teče test, poskusi znova, ko konča:\n" + teste)
        return 1

    meja = time.time() - a.starost * 60
    uid = os.getuid()
    kandidati = []
    for ime in os.listdir(KOREN):
        if not ime.startswith(PREDPONE):
            continue
        pot = os.path.join(KOREN, ime)
        try:
            st = os.lstat(pot)
        except OSError:
            continue
        if st.st_uid == uid and st.st_mtime < meja:
            kandidati.append(pot)

    skupaj = sum(velikost(p) for p in kandidati)
    if not a.suho:
        for p in kandidati:
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                try:
                    os.remove(p)
                except OSError:
                    pass
    ostalo = sum(1 for i in os.listdir(KOREN) if i.startswith(PREDPONE))
    print(f"{'bi pobrisal' if a.suho else 'pobrisano'}: {len(kandidati)} testnih map, {skupaj / 1e9:.2f} GB; "
          f"ostalo z istimi predponami (mlajše od {a.starost} min ali tuje): {ostalo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
