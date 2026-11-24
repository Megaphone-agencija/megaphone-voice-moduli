#!/usr/bin/env python3
"""Vzporedni zagon unittest zbirke: vsak testni modul v svojem procesu.

Uporaba: vzporedni_testi.py <koren repozitorija> <python> [-j N] [-o izhod.padci]
Izpiše povzetek (moduli, testi, padci, napake, čas) in zapiše urejen seznam vrstic FAIL:/ERROR: v -o.
"""
import argparse, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
ap.add_argument("koren"); ap.add_argument("python")
ap.add_argument("-j", type=int, default=max(1, (os.cpu_count() or 2) - 2))
ap.add_argument("-o", default=None)
ap.add_argument("--zacetek", default="tests")
a = ap.parse_args()

moduli = []
for d, _, datoteke in os.walk(os.path.join(a.koren, a.zacetek)):
    if "__pycache__" in d:
        continue
    for f in datoteke:
        if f.startswith("test") and f.endswith(".py"):
            rel = os.path.relpath(os.path.join(d, f), a.koren)[:-3]
            moduli.append(rel.replace(os.sep, "."))
moduli.sort()

def pozeni(m):
    t = time.time()
    p = subprocess.run([a.python, "-m", "unittest", m], cwd=a.koren, capture_output=True, text=True)
    return m, p.returncode, p.stderr + p.stdout, time.time() - t

t0 = time.time()
with ThreadPoolExecutor(a.j) as ex:
    rez = list(ex.map(pozeni, moduli))

testov = padci = 0
vrstice, pocasni = [], []
for m, rc, izhod, cas in rez:
    n = re.search(r"Ran (\d+) test", izhod)
    testov += int(n.group(1)) if n else 0
    vr = [l for l in izhod.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    vrstice += vr
    if rc != 0 and not vr:
        vrstice.append(f"ERROR: modul {m} (koda {rc}, brez vrstice FAIL/ERROR)")
    pocasni.append((cas, m))
vrstice.sort()
if a.o:
    open(a.o, "w").write("\n".join(vrstice) + ("\n" if vrstice else ""))
print(f"moduli {len(moduli)}, testov {testov}, FAIL {sum(v.startswith('FAIL') for v in vrstice)}, ERROR {sum(v.startswith('ERROR') for v in vrstice)}, čas {time.time()-t0:.0f} s, -j {a.j}")
print("najpočasnejši:", ", ".join(f"{m} {c:.0f}s" for c, m in sorted(pocasni, reverse=True)[:5]))
