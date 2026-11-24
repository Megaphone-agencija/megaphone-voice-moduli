#!/usr/bin/env python3
"""»Pripravljeno za Cheba«: ali je veja glasovnega agenta zrela? Izpiše ZRELO ali NI ZRELO + razlogi.

Uporaba:
  pripravljeno.py <repo> [--veja HEAD] [--osnova main] [--python POT] [--pythonpath "tests:.:govor"] [-j N]
                  [--cl POT] [--porocilo POT] [--skrite POT.py] [--model sonnet-high] [--izjema SHA ...] [--brez-testov]

Izhodna koda: 0 = ZRELO, 1 = NI ZRELO, 2 = napaka uporabe.

Preverbe (vsaka izpiše [OK], [NE] ali [OPOZORILO]):
  1. cela zbirka testov (vzporedni_testi.py)        5. skrite oblike (--skrite) v začasnem worktreeju
  2. preveri_cl.py --testi tests/                   6. pravi model 3x: <podatki>/<sha12>-pravi-model.json
  3. reprodukcija pred/po za vsak commit s          7. Codex: <podatki>/<sha12>-codex.txt
     »Reprodukcija:« (test pade s PREVERBO pred
     popravkom, gre skozi po njem, ima # klic:)
  4. poročilo (--porocilo): »Ne pokrije:« + ## Oblike >= 10 (od tega >= 3 »nasprotna«) + ## Klicni list;
     ob ZRELO se Klicni list izpiše za IZID

Podatkovna mapa: PODATKI/<ime mape repozitorija>/ (okoljska spremenljivka PRIPRAVLJENO_MAPA zamenja PODATKI).
Vrstice skritih oblik gredo v SKRITE_CSV (okoljska spremenljivka PRIPRAVLJENO_SKRITE_CSV).
Začasni worktreeji se vedno pobrišejo. Samo standardna knjižnica + git.
"""
import argparse
import ast
import contextlib
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import date

PODATKI = "/home/chebo/MAIOS/00-system/pripravljeno"
SKRITE_CSV = "/home/chebo/MAIOS/00-system/napake/skrite-oblike.csv"
SKRIPTE = os.path.dirname(os.path.abspath(__file__))
SKRITA_DATOTEKA = "tests/test_skrite_oblike_zacasno.py"
SKRITI_MODUL = "tests.test_skrite_oblike_zacasno"
MIN_OBLIK = 10
MIN_NASPROTNIH = 3
MAX_KLICNI_LIST = 8
MIN_TEKOV = 3
CAS_TESTA = 600

# Izvajalnik enega testa (ali modula): požene ga ciljni python v worktreeju (python -c IZVAJALNIK ime).
IZVAJALNIK = r'''
import contextlib, io, json, os, sys, traceback, unittest
sys.path.insert(0, os.getcwd())
ime = sys.argv[1]
tek = unittest.TestResult()
nalagalnik = unittest.TestLoader()
dodatne = []
sum_ = io.StringIO()
try:
    with contextlib.redirect_stdout(sum_), contextlib.redirect_stderr(sum_):
        nalagalnik.loadTestsFromName(ime).run(tek)
except BaseException:
    dodatne.append(traceback.format_exc())
napake = [tb for _, tb in tek.errors] + dodatne
if not tek.errors and not dodatne:
    napake += list(getattr(nalagalnik, "errors", []))
fail = [tb for _, tb in tek.failures]
padla = []
for t, _ in tek.failures + tek.errors + tek.skipped:
    padla.append(t.id().split(" ")[0].split(".")[-1])
izpis = (fail + napake + [r for _, r in tek.skipped] + [""])[0]
sys.__stdout__.write(json.dumps({"tekov": tek.testsRun, "failures": len(fail), "errors": len(napake),
    "skipped": len(tek.skipped), "izpis": izpis,
    "nalaganje": any(type(t).__name__ == "_FailedTest" for t, _ in tek.errors) or bool(dodatne), "napaka": (napake + [""])[0], "padla": padla}) + "\n")
'''


class Izpis:
    def __init__(self):
        self.razlogi = 0

    def vr(self, oznaka, besedilo, *vrinjene):
        if oznaka == "NE":
            self.razlogi += 1
        print(f"[{oznaka}] {besedilo}", flush=True)
        for v in vrinjene:
            print("      " + v, flush=True)


def napaka_uporabe(sporocilo):
    print(f"napaka: {sporocilo}", file=sys.stderr)
    sys.exit(2)


def okolje(pythonpath):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"  # testi v repozitoriju ne smejo puščati __pycache__
    env["GIT_TERMINAL_PROMPT"] = "0"
    if pythonpath:
        env["PYTHONPATH"] = pythonpath
    return env


def git(repo, *arg, bajti=False):
    return subprocess.run(["git", "-C", repo, *arg], capture_output=True, text=not bajti,
                          env=okolje(None))


def git_ali_napaka(repo, *arg):
    p = git(repo, *arg)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(arg)}: {p.stderr.strip() or p.stdout.strip()}")
    return p.stdout


@contextlib.contextmanager
def worktree(repo, sha):
    """Začasni worktree (detached) na sha; vedno pobrisan."""
    tmp = tempfile.mkdtemp(prefix="pripravljeno-")
    wt = os.path.join(tmp, "wt")
    try:
        git_ali_napaka(repo, "worktree", "add", "--detach", "--quiet", wt, sha)
        yield wt
    finally:
        git(repo, "worktree", "remove", "--force", wt)
        shutil.rmtree(tmp, ignore_errors=True)
        git(repo, "worktree", "prune")


def mnozina(n, ena, dve, tri, pet):
    if n % 100 == 1:
        return ena
    if n % 100 == 2:
        return dve
    if n % 100 in (3, 4):
        return tri
    return pet


def zadnja_vrstica(tb):
    vr = [v for v in (tb or "").splitlines() if v.strip()]
    return vr[-1].strip() if vr else "(brez izpisa)"


def simptom(tb, n=15):
    """Izpis padca brez okvirjev sklada: izjema in sporočilo (prvih n vrstic)."""
    vr = (tb or "").rstrip().splitlines()
    kje = max((i for i, v in enumerate(vr) if v.startswith("AssertionError")), default=None)
    if kje is not None:  # vrstica z AssertionError je vedno prva izpisana
        return vr[kje:kje + n]
    zadnji = max((i for i, v in enumerate(vr) if v.startswith('  File "')), default=None)
    if zadnji is None:
        return vr[:n]
    i = zadnji + 1
    while i < len(vr) and vr[i].startswith("    "):
        i += 1
    ostanek = vr[i:] or vr[-n:]
    return ostanek[:n]


def poganjaj_test(python, wt, ime, pythonpath):
    try:
        p = subprocess.run([python, "-c", IZVAJALNIK, ime], cwd=wt, env=okolje(pythonpath),
                           capture_output=True, text=True, timeout=CAS_TESTA)
    except subprocess.TimeoutExpired:
        return {"tekov": 0, "failures": 0, "errors": 1, "skipped": 0, "padla": [],
                "izpis": f"TimeoutError: test traja dlje kot {CAS_TESTA} s", "napaka": f"TimeoutError: več kot {CAS_TESTA} s"}
    vr = [v for v in p.stdout.splitlines() if v.strip()]
    try:
        return json.loads(vr[-1])
    except (IndexError, ValueError):
        sporocilo = "izvajalnik testov se je sesul: " + zadnja_vrstica(p.stderr or p.stdout)
        return {"tekov": 0, "failures": 0, "errors": 1, "skipped": 0, "padla": [], "izpis": sporocilo, "napaka": sporocilo}


def ocena(r):
    """('fail'|'error'|'pass', prva vrstica, izpis padca)."""
    if r["errors"] > 0:
        return "error", zadnja_vrstica(r.get("napaka") or r.get("izpis")), r.get("izpis", "")
    if r["skipped"] > 0:
        return "error", "test je preskočen (skip)", r.get("izpis", "")
    if r["failures"] > 0:
        return "fail", zadnja_vrstica(r.get("izpis")), r.get("izpis", "")
    if r["tekov"] == 0:
        return "error", "test ni najden (0 testov)", ""
    return "pass", "", ""


# --- commiti in oznake -------------------------------------------------------------------

def preberi_commite(repo, osnova, veja):
    izhod = git_ali_napaka(repo, "log", "--reverse", "--no-merges", "--format=%H%x1f%B%x1e", f"{osnova}..{veja}")
    out = []
    for zapis in izhod.split("\x1e"):
        if not zapis.strip():
            continue
        sha, _, telo = zapis.strip("\n").partition("\x1f")
        out.append((sha.strip(), telo))
    return out


def oznake(telo):
    druzina = bool(re.search(r"^\s*Dru[zž]ina:", telo, re.I | re.M))
    repro = []
    for m in re.finditer(r"^\s*Reprodukcija:[ \t]*(.*)$", telo, re.I | re.M):
        repro.append(m.group(1).strip().strip("`").strip())
    return druzina, repro


def razclani_test(repo, sha, vrednost):
    """Vrne (pot do .py, [Razred, test] ali [test], dotted ime za unittest) ali (None, None, razlog)."""
    ime = vrednost.split()[0].strip("`") if vrednost.split() else ""
    if "::" in ime:
        pot, *deli = ime.split("::")
        if not pot.endswith(".py") or not deli:
            return None, None, f"neprepoznana oblika »{ime}«"
        modul = pot[:-3].replace("/", ".")
        return pot, deli, ".".join([modul] + deli)
    deli = ime.split(".")
    for k in range(len(deli) - 1, 0, -1):
        pot = "/".join(deli[:k]) + ".py"
        if git(repo, "cat-file", "-e", f"{sha}:{pot}").returncode == 0:
            return pot, deli[k:], ime
    return None, None, f"testne datoteke za »{ime}« ni v commitu"


def ima_klic(izvor, deli):
    """Komentar »# klic: …« v telesu testne funkcije ali do 3 vrstice nad `def`."""
    try:
        drevo = ast.parse(izvor)
    except SyntaxError as e:
        return False, f"testna datoteka ima skladenjsko napako ({e.msg})"
    vrstice = izvor.splitlines()
    kje = drevo
    for ime in deli[:-1]:
        kje = next((n for n in ast.iter_child_nodes(kje) if isinstance(n, ast.ClassDef) and n.name == ime), None)
        if kje is None:
            return False, f"razred {ime} ni v testni datoteki"
    f = next((n for n in ast.iter_child_nodes(kje)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == deli[-1]), None)
    if f is None:
        return False, f"funkcija {deli[-1]} ni v testni datoteki"
    zacetek = min([f.lineno] + [d.lineno for d in f.decorator_list])
    odsek = vrstice[max(0, zacetek - 1 - 3):f.end_lineno]
    if any(re.search(r"#\s*klic:\s*\S", v) for v in odsek):
        return True, ""
    return False, "v testu ni komentarja »# klic: …«"


def polozi_teste(repo, sha, wt):
    """V worktree zamenja mapo tests/ s stanjem iz commita sha. Vrne napako ali None."""
    p = git(repo, "archive", "--format=tar", sha, "tests", bajti=True)
    if p.returncode != 0:
        return "commit nima mape tests/"
    shutil.rmtree(os.path.join(wt, "tests"), ignore_errors=True)
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tar:
        if hasattr(tarfile, "data_filter"):
            tar.extractall(wt, filter="data")
        else:
            tar.extractall(wt)
    return None


def preveri_reprodukcijo(repo, python, pythonpath, sha, vrednost, podatki, vrh):
    """Del C za en test. Vrne (ok, besedilo, vrinjene vrstice)."""
    pot, deli, dotted = razclani_test(repo, sha, vrednost)
    if pot is None:
        return False, dotted, []
    izvor = git(repo, "show", f"{sha}:{pot}")
    if izvor.returncode != 0:
        return False, f"testna datoteka {pot} ni v commitu", []
    starsi = git(repo, "rev-parse", "--verify", "--quiet", f"{sha}^")
    if starsi.returncode != 0:
        return False, "commit nima starša (ni kaj primerjati)", []
    # a) pred popravkom
    with worktree(repo, starsi.stdout.strip()) as wt:
        napaka = polozi_teste(repo, sha, wt)
        if napaka:
            return False, napaka, []
        pred = poganjaj_test(python, wt, dotted, pythonpath)
    vrsta, prva, tb = ocena(pred)
    if vrsta == "error":
        return False, f"test se na starem stanju sesuje ({prva}) — ni dokaz", []
    if vrsta == "pass":
        return False, "test ne ujame napake (na starem stanju gre skozi)", []
    simptomi = simptom(tb)
    vr = [("pred: " if i == 0 else "      ") + v for i, v in enumerate(simptomi)]
    try:
        with open(os.path.join(podatki, f"{sha[:12]}-reprodukcija-pred.txt"), "w", encoding="utf-8") as f:
            f.write(tb)
    except OSError:
        pass
    # b) po popravku
    po = poganjaj_test(python, vrh(), dotted, pythonpath)
    vrsta2, prva2, _ = ocena(po)
    if vrsta2 != "pass":
        return False, f"po popravku test ne gre skozi ({prva2})", vr
    # c) # klic:
    ok, razlog = ima_klic(izvor.stdout, deli)
    if not ok:
        return False, razlog, vr
    return True, "pade pred popravkom (preverba), gre skozi po njem", vr


# --- poročilo, skrite oblike, pravi model, Codex ------------------------------------------

def klicni_list(vrstice):
    """Neprazne vrstice razdelka »## Klicni list« (do naslednjega naslova), kot so zapisane; None, če naslova ni."""
    blok, v_listu, imam = [], False, False
    for v in vrstice:
        if re.match(r"^#{1,6}\s", v):
            if v_listu:
                break
            v_listu = imam = bool(re.match(r"^##\s+Klicni list\b", v))
            continue
        if v_listu and v.strip():
            blok.append(v)
    return blok if imam else None


def preberi_porocilo(pot):
    with open(pot, encoding="utf-8") as f:
        return f.read().splitlines()


def preveri_porocilo(pot):
    try:
        vrstice = preberi_porocilo(pot)
    except OSError as e:
        return False, f"poročila ni mogoče prebrati ({e.strerror}): {pot}"
    ne_pokrije = any(re.match(r"ne pokrije\s*:", re.sub(r"[*_`]", "", v).lstrip(" \t>-").lower()) for v in vrstice)
    oblik, nasprotnih, v_oblikah = 0, 0, False
    blok = []
    for v in vrstice:
        if re.match(r"^#{1,6}\s", v):
            if v_oblikah:
                break
            v_oblikah = bool(re.match(r"^##\s+Oblike\b", v))
            continue
        if v_oblikah:
            blok.append(v)
    je_locilo = lambda v: v.lstrip().startswith("|") and re.fullmatch(r"[\s|:\-]+", v) is not None
    for i, v in enumerate(blok):
        je_oblika = False
        if re.match(r"^\s*([-*+]|\d+[.)])\s+\S", v):
            je_oblika = True
        elif v.lstrip().startswith("|"):
            glava = i + 1 < len(blok) and je_locilo(blok[i + 1])  # vrstica pred ločilom je glava tabele
            je_oblika = not je_locilo(v) and not glava
        if je_oblika:
            oblik += 1
            if "nasprotna" in v.lower():
                nasprotnih += 1
    imam_naslov = any(re.match(r"^##\s+Oblike\b", v) for v in vrstice)
    razlogi = []
    if not ne_pokrije:
        razlogi.append("manjka vrstica »Ne pokrije:«")
    if not imam_naslov:
        razlogi.append("manjka naslov »## Oblike«")
    elif oblik < MIN_OBLIK:
        razlogi.append(f"v »## Oblike« je {oblik} oblik, treba jih je vsaj {MIN_OBLIK}")
    if imam_naslov and nasprotnih < MIN_NASPROTNIH:
        razlogi.append(f"v »## Oblike« je {nasprotnih} nasprotnih oblik, treba jih je vsaj {MIN_NASPROTNIH}")
    if not klicni_list(vrstice):
        razlogi.append("manjka Klicni list (naslov »## Klicni list« z vsaj eno vrstico)")
    if razlogi:
        return False, "; ".join(razlogi)
    return True, f"Ne pokrije ✓, Oblike {oblik} (nasprotnih {nasprotnih}), Klicni list ✓"


def zapisi_csv(pot, vrstica):
    """Vrstica na (repo, sha); ponovni zagon istega SHA zamenja prejšnjo vrstico (velja zadnji zagon)."""
    glava = ["datum", "repo", "veja", "sha", "model", "vseh", "padlo"]
    vrstice = []
    if os.path.exists(pot):
        with open(pot, newline="", encoding="utf-8") as f:
            vrstice = [r for r in csv.reader(f) if r and r != glava]
    vrstice = [r for r in vrstice if not (len(r) > 3 and r[1] == vrstica[1] and r[3] == vrstica[3])]
    vrstice.append([str(x) for x in vrstica])
    os.makedirs(os.path.dirname(pot) or ".", exist_ok=True)
    with open(pot, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(glava)
        w.writerows(vrstice)


def preveri_skrite(pot, tip, python, pythonpath):
    """Vrne (ok, besedilo, vseh, padlo) — vseh None, če testov ni bilo mogoče pognati."""
    if not os.path.isfile(pot):
        return False, f"datoteke ni: {pot}", None, None
    shutil.copyfile(pot, os.path.join(tip, SKRITA_DATOTEKA))
    try:
        r = poganjaj_test(python, tip, SKRITI_MODUL, pythonpath)
    finally:
        with contextlib.suppress(OSError):
            os.remove(os.path.join(tip, SKRITA_DATOTEKA))
    padla = sorted(set(r.get("padla", [])))
    vseh = r["tekov"]
    if r.get("nalaganje") or (vseh == 0 and r["errors"] > 0):
        # modula ni bilo mogoče naložiti: to ni meritev skritih oblik, zato brez vrstice v CSV
        return False, "skrite oblike se ne naložijo: " + zadnja_vrstica(r.get("napaka")), None, None
    if vseh == 0:
        return False, "v datoteki ni testov", None, None
    n_padlo = min(len(padla) or (r["failures"] + r["errors"] + r["skipped"]), vseh)
    zelenih = vseh - n_padlo
    besedilo = f"{zelenih} od {vseh} zelenih"
    if n_padlo:
        besedilo += f" ({', '.join(padla) if padla else 'imena niso znana'})"
    return n_padlo == 0, besedilo, vseh, n_padlo


def preveri_pravi_model(mapa, sha):
    ime = f"{sha[:12]}-pravi-model.json"
    pot = os.path.join(mapa, ime)
    if not os.path.isfile(pot):
        return False, f"ni datoteke {ime} (mapa {mapa})"
    try:
        d = json.load(open(pot, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return False, f"{ime} ni veljaven JSON ({e})"
    if not isinstance(d, dict):
        return False, f"{ime}: pričakovan objekt z ključi sha, teki, padci, scenarij"
    s, teki, padci = d.get("sha"), d.get("teki"), d.get("padci")
    razlogi = []
    if not (isinstance(s, str) and len(s) >= 12 and sha.startswith(s.lower())):
        razlogi.append(f"sha {str(s)[:12]!r} ni vrh veje {sha[:12]}")
    if isinstance(teki, bool) or not isinstance(teki, int) or teki < MIN_TEKOV:
        razlogi.append(f"teki {teki!r}, treba jih je vsaj {MIN_TEKOV}")
    if isinstance(padci, bool) or not isinstance(padci, int) or padci != 0:
        razlogi.append(f"padci {padci!r}, mora biti 0")
    if razlogi:
        return False, "; ".join(razlogi)
    return True, f"teki {teki}, padci 0, scenarij: {d.get('scenarij', '(ni naveden)')}"


def preveri_codex(mapa, sha):
    ime = f"{sha[:12]}-codex.txt"
    pot = os.path.join(mapa, ime)
    if not os.path.isfile(pot):
        return False, f"ni datoteke {ime} (mapa {mapa})", []
    vsebina = open(pot, encoding="utf-8", errors="replace").read().splitlines()
    neprazne = [v for v in vsebina if v.strip()]
    if neprazne and re.sub(r"\s+", " ", neprazne[0].strip().lower()) == "brez blokatorja":
        return True, "brez blokatorja", []
    return False, "Codex ima blokator ali nejasen zapis", (neprazne or ["(datoteka je prazna)"])[:10]


# --- glavni tok ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Ali je veja glasovnega agenta zrela za Cheba?")
    ap.add_argument("repo")
    ap.add_argument("--veja", default="HEAD")
    ap.add_argument("--osnova", default="main")
    ap.add_argument("--python", default=None)
    ap.add_argument("--pythonpath", default=None)
    ap.add_argument("-j", type=int, default=None)
    ap.add_argument("--cl", default=None)
    ap.add_argument("--porocilo", default=None)
    ap.add_argument("--skrite", default=None)
    ap.add_argument("--model", default="neznano")
    ap.add_argument("--izjema", nargs="+", action="extend", default=[])
    ap.add_argument("--brez-testov", action="store_true")
    a = ap.parse_args()

    p = subprocess.run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if p.returncode != 0:
        napaka_uporabe(f"{a.repo} ni git repozitorij")
    repo = p.stdout.strip()
    tip = git(repo, "rev-parse", "--verify", "--quiet", f"{a.veja}^{{commit}}").stdout.strip()
    if not tip:
        napaka_uporabe(f"veja »{a.veja}« ne obstaja v {repo}")
    osnova_sha = git(repo, "rev-parse", "--verify", "--quiet", f"{a.osnova}^{{commit}}").stdout.strip()
    if not osnova_sha:
        napaka_uporabe(f"osnova »{a.osnova}« ne obstaja v {repo}")
    python = a.python or (os.path.join(repo, ".venv/bin/python") if os.path.exists(os.path.join(repo, ".venv/bin/python")) else sys.executable)
    python = os.path.abspath(python)  # absolutna, a brez razreševanja povezav (venv)
    if not os.access(python, os.X_OK):
        napaka_uporabe(f"python ni izvedljiv: {python}")
    if a.cl and not os.path.isfile(a.cl):
        napaka_uporabe(f"--cl: datoteke ni: {a.cl}")

    ime_repo = os.path.basename(repo)
    mapa = os.path.join(os.environ.get("PRIPRAVLJENO_MAPA") or PODATKI, ime_repo)
    os.makedirs(mapa, exist_ok=True)
    veja_ime = a.veja
    if a.veja == "HEAD":
        veja_ime = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() or "HEAD"
    izpis = Izpis()
    print(f"pripravljeno: {ime_repo} @ {veja_ime} {tip[:12]} (osnova {a.osnova})", flush=True)

    with contextlib.ExitStack() as sklad:
        predpomnilnik = []

        def vrh():
            if not predpomnilnik:
                predpomnilnik.append(sklad.enter_context(worktree(repo, tip)))
            return predpomnilnik[0]

        # na čisti delovni mapi, ki je ravno na vrhu veje, testi tečejo kar tam; sicer na worktreeju
        doma = (git(repo, "rev-parse", "HEAD").stdout.strip() == tip
                and git(repo, "status", "--porcelain", "--untracked-files=no").stdout.strip() == "")

        def koren_testov():
            return repo if doma else vrh()

        # 1. testi
        try:
            if a.brez_testov:
                izpis.vr("NE", "testi: NI PREVERJENO (--brez-testov)")
            else:
                if not doma:
                    izpis.vr("OPOZORILO", "testi tečejo na začasnem worktreeju vrha veje (delovna mapa ni na tej veji ali ima spremembe)")
                with tempfile.TemporaryDirectory(prefix="pripravljeno-padci-") as tmp:
                    padci = os.path.join(tmp, "padci.txt")
                    ukaz = [sys.executable, os.path.join(SKRIPTE, "vzporedni_testi.py"), koren_testov(), python, "-o", padci]
                    if a.j:
                        ukaz += ["-j", str(a.j)]
                    r = subprocess.run(ukaz, capture_output=True, text=True, env=okolje(a.pythonpath))
                    prva = (r.stdout.splitlines() or [""])[0]
                    vrstice = [v for v in open(padci, encoding="utf-8").read().splitlines() if v] if os.path.exists(padci) else []
                if r.returncode != 0 or not prva:
                    izpis.vr("NE", "testi: vzporedni_testi.py se je sesul", *(r.stderr.strip().splitlines()[-5:] or ["(brez izpisa)"]))
                elif prva.startswith("moduli 0,"):
                    izpis.vr("NE", f"testi: ni nobenega testnega modula ({prva})")
                elif vrstice:
                    izpis.vr("NE", f"testi: {prva}", *vrstice[:10], *([f"… še {len(vrstice) - 10}"] if len(vrstice) > 10 else []))
                else:
                    izpis.vr("OK", f"testi: {prva}")
        except RuntimeError as e:
            izpis.vr("NE", f"testi: napaka pri pripravi worktreeja: {e}")

        # 2. CL
        try:
            cl = a.cl
            if not cl:
                najdeni = []
                mapa_docs = os.path.join(koren_testov(), "docs")
                if os.path.isdir(mapa_docs):
                    najdeni = sorted(f for f in os.listdir(mapa_docs) if re.fullmatch(r"checklist-.*\.md", f))
                if len(najdeni) == 1:
                    cl = os.path.join(mapa_docs, najdeni[0])
            if cl:
                r = subprocess.run([sys.executable, os.path.join(SKRIPTE, "preveri_cl.py"), os.path.abspath(cl), "--testi", "tests/"],
                                   cwd=koren_testov(), capture_output=True, text=True, env=okolje(None))
                if r.returncode == 0:
                    izpis.vr("OK", f"CL: {os.path.basename(cl)}")
                else:
                    vr = (r.stdout + r.stderr).strip().splitlines()
                    izpis.vr("NE", f"CL: preveri_cl.py je vrnil {r.returncode} ({os.path.basename(cl)})", *vr[:8])
            else:
                izpis.vr("OPOZORILO", "CL ni najden")
        except RuntimeError as e:
            izpis.vr("NE", f"CL: napaka pri pripravi worktreeja: {e}")

        # 3. reprodukcija
        commiti = preberi_commite(repo, osnova_sha, tip)
        izjeme = [i.lower() for i in a.izjema]
        je_izjema = lambda sha: any(sha.startswith(i) for i in izjeme)
        ima_druzino = False
        brez_oznake = 0
        if not commiti:
            izpis.vr("OPOZORILO", f"veja nima commitov nad osnovo {a.osnova}")
        for sha, telo in commiti:
            druzina, repro = oznake(telo)
            ima_druzino = ima_druzino or druzina
            kratek = sha[:7]
            if not druzina and not repro:
                brez_oznake += 1
                continue
            if not repro:
                if je_izjema(sha):
                    izpis.vr("OK", f"reprodukcija {kratek}: izjema (ročno)")
                else:
                    izpis.vr("NE", f"reprodukcija {kratek}: commit ima »Družina:«, a nima vrstice »Reprodukcija:«")
                continue
            for vrednost in repro:
                oznaka_testa = f" ({vrednost.split()[0]})" if len(repro) > 1 and vrednost.split() else ""
                m = re.match(r"ni\b[\s—–:\-]*(.*)$", vrednost, re.I)
                if m:
                    if je_izjema(sha):
                        izpis.vr("OK", f"reprodukcija {kratek}: izjema (ročno)")
                    else:
                        izpis.vr("NE", f"reprodukcija {kratek}: »Reprodukcija: ni« — razlog: {m.group(1) or '(ni naveden)'}")
                    continue
                try:
                    ok, besedilo, vr = preveri_reprodukcijo(repo, python, a.pythonpath, sha, vrednost, mapa, vrh)
                except RuntimeError as e:
                    ok, besedilo, vr = False, f"napaka pri pripravi worktreeja: {e}", []
                izpis.vr("OK" if ok else "NE", f"reprodukcija {kratek}{oznaka_testa}: {besedilo}", *vr)
        if brez_oznake:
            n = brez_oznake
            izpis.vr("OK", f"reprodukcija: {n} {mnozina(n, 'commit', 'commita', 'commiti', 'commitov')} brez oznake popravka (ni preverjeno)")

        # 4. poročilo
        if a.porocilo or ima_druzino:
            if not a.porocilo:
                izpis.vr("NE", "poročilo: veja ima popravek (»Družina:«), poročila (--porocilo) pa ni")
            else:
                ok, besedilo = preveri_porocilo(a.porocilo)
                izpis.vr("OK" if ok else "NE", f"poročilo: {besedilo}")
        else:
            izpis.vr("OK", "poročilo: veja nima commita z »Družina:«, ni obvezno")

        # 5. skrite oblike
        if a.skrite or ima_druzino:
            if not a.skrite:
                izpis.vr("NE", "skrite oblike: ni skritih oblik (--skrite ni podan)")
            else:
                try:
                    ok, besedilo, vseh, padlo = preveri_skrite(a.skrite, vrh(), python, a.pythonpath)
                except RuntimeError as e:
                    ok, besedilo, vseh, padlo = False, f"napaka pri pripravi worktreeja: {e}", None, None
                izpis.vr("OK" if ok else "NE", f"skrite oblike: {besedilo}")
                if vseh:
                    csv_pot = os.environ.get("PRIPRAVLJENO_SKRITE_CSV") or SKRITE_CSV
                    zapisi_csv(csv_pot, [date.today().isoformat(), ime_repo, veja_ime, tip[:12], a.model, vseh, padlo])
        else:
            izpis.vr("OK", "skrite oblike: veja nima commita z »Družina:«, niso obvezne")

        # 6. pravi model
        ok, besedilo = preveri_pravi_model(mapa, tip)
        izpis.vr("OK" if ok else "NE", f"pravi model: {besedilo}")

        # 7. Codex
        ok, besedilo, vr = preveri_codex(mapa, tip)
        izpis.vr("OK" if ok else "NE", f"codex: {besedilo}", *vr)

    n = izpis.razlogi
    if n == 0:
        print("IZID: ZRELO")
        if a.porocilo:
            try:
                list_ = klicni_list(preberi_porocilo(a.porocilo)) or []
            except OSError:
                list_ = []
            if list_:
                print("KLICNI LIST:")
                for v in list_[:MAX_KLICNI_LIST]:
                    print(v)
                if len(list_) > MAX_KLICNI_LIST:
                    print(f"… še {len(list_) - MAX_KLICNI_LIST}")
        return 0
    print(f"IZID: NI ZRELO ({n} {mnozina(n, 'razlog', 'razloga', 'razlogi', 'razlogov')})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
