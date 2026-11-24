#!/usr/bin/env python3
"""stej.py: šteje popravke glasovnih agentov in odpira kartice »Analiza vzroka«.

Kaj dela:
  stej.py                 po vsakem commitu (post-commit): ob vsakem novem popravku pogleda zadnjih 10 popravkov (drseče okno)
  stej.py --dnevno        popravki zadnjih 24 ur; družina >= 3 brez odprte kartice -> kartica
  stej.py --zgodovina CSV preizkus na zgodovini (nič ne zapiše, izpiše, kdaj bi se kartica odprla)

Popravek = commit z `Vrsta: popravek`, brez vrstice `Prenos-iz:` (prenos ni nova napaka).
Šteje se iz git zgodovine vseh repozitorijev, zato je ponovni zagon varen (nič se ne šteje dvakrat).
Samo stdlib. Okoljske spremenljivke za teste:
  NAPAKE_MAPA (stanje, log), NAPAKE_KANBAN (mapa 05-tasks), NAPAKE_REPOS (poti ločene z ':'),
  NAPAKE_BREZ_DB=1 (ne kliči maios_db.py), NAPAKE_DRUZINE (druzine.json).
"""
import argparse
import csv
import datetime as dt
import fcntl
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKRIPTA = Path(__file__).resolve().parent
MAPA = Path(os.environ.get("NAPAKE_MAPA") or SKRIPTA)
KANBAN = Path(os.environ.get("NAPAKE_KANBAN") or "/home/chebo/MAIOS/05-tasks")
MAIOS_DB = "/home/chebo/MAIOS/00-system/db/maios_db.py"
PROJEKTI = Path("/home/chebo/MAIOS/09-projects")
OKNO_POPRAVKOV = 10  # drseče okno: zadnjih 10 popravkov čez vse repozitorije
PRAG = 3
OKNO = dt.timedelta(hours=24)
ODPRTE_MAPE = ("backlog", "in-progress", "needs-review")

REPOZITORIJI = [
    PROJEKTI / "POC glasovni agent/megaphone-voice-poc",
    PROJEKTI / "Joze - glasovni agent",
    PROJEKTI / "Fine dining - glasovni agent",
    PROJEKTI / "Prebil - glasovni agent",
    PROJEKTI / "Večer - glasovni agenti/vecer-hetzner-poc",
    PROJEKTI / "Kratochwill - glasovni agent",
]


class Popravek:
    def __init__(self, repo, sha, cas, prva, druzina):
        self.repo, self.sha, self.cas, self.prva, self.druzina = repo, sha, cas, prva, druzina

    @property
    def kljuc(self):
        return "%s|%s" % (self.repo, self.sha)


def repozitoriji():
    env = os.environ.get("NAPAKE_REPOS")
    return [Path(p) for p in env.split(":") if p] if env else REPOZITORIJI


def druzine():
    pot = Path(os.environ.get("NAPAKE_DRUZINE") or SKRIPTA / "druzine.json")
    with open(pot, encoding="utf-8") as f:
        return {d["slug"]: d for d in json.load(f)["druzine"]}


def razberi(sporocilo):
    """Vrne (je_popravek, družina) iz celega sporočila (regex, ker git ne pozna ključa s šumnikom)."""
    v = re.search(r"(?m)^Vrsta:\s*(\S+)", sporocilo)
    if not v or v.group(1).lower() != "popravek":
        return False, ""
    if re.search(r"(?m)^Prenos-iz:", sporocilo):
        return False, ""
    d = re.search(r"(?m)^Družina:\s*(\S+)", sporocilo)
    return True, (d.group(1) if d else "")


def git_log(repo):
    okolje = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    r = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), "log", "--all", "--no-merges",
         "--date=unix", "--format=%H%x00%ad%x00%B%x01"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=okolje, timeout=60)
    return r.stdout if r.returncode == 0 else ""


def zberi_popravke():
    izid = []
    for repo in repozitoriji():
        for zapis in git_log(repo).split("\x01"):
            zapis = zapis.strip("\n")
            deli = zapis.split("\x00", 2)
            if len(deli) < 3:
                continue
            sha, ts, sporocilo = deli
            je, dr = razberi(sporocilo)
            if not je:
                continue
            prva = next((v.strip() for v in sporocilo.splitlines() if v.strip()), "")
            izid.append(Popravek(repo.name, sha[:10], dt.datetime.fromtimestamp(int(ts)), prva, dr))
    izid.sort(key=lambda p: (p.cas, p.kljuc))
    return izid


def zadetki(popravki, znane):
    """Družine z >= PRAG popravki. Neznane slugove (hook je v načinu opozori) preskoči."""
    po = {}
    for p in popravki:
        if p.druzina in znane:
            po.setdefault(p.druzina, []).append(p)
    return {s: l for s, l in po.items() if len(l) >= PRAG}


def odprta_kartica(slug):
    for mapa in ODPRTE_MAPE:
        if list((KANBAN / mapa).glob("*-analiza-vzroka-%s.md" % slug)):
            return True
    return False


def datum_sl(d):
    return "%d. %d. %d" % (d.day, d.month, d.year)


def zapisi_log(vrstica):
    try:
        with open(MAPA / "opozorila.log", "a", encoding="utf-8") as f:
            f.write("%s | %s\n" % (dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), vrstica))
    except OSError:
        pass


def odpri_kartico(slug, druzina, popravki, razlog, zdaj):
    """Ustvari datoteko v backlog/ in vrstico v DB. Vrne id ali None, če kartica že obstaja."""
    if odprta_kartica(slug):
        return None
    id_ = "%s-analiza-vzroka-%s" % (zdaj.strftime("%Y-%m-%d"), slug)
    pot = KANBAN / "backlog" / (id_ + ".md")
    ime = druzina["ime"] if druzina else slug
    naslov = "Glasovni agenti — analiza vzroka: %s (%s)" % (ime, datum_sl(zdaj))
    kje = "v zadnjih 10 popravkih" if razlog == "okno" else "ob dnevni preverbi (zadnjih 24 ur)"
    seznam = "\n".join("- %s / %s — %s" % (p.repo, p.sha, p.prva) for p in popravki)
    definicija = (druzina or {}).get("definicija", "")
    telo = (
        "---\ntitle: \"%s\"\nstatus: backlog\nowner: claude-code\ntype: research\n---\n\n"
        "Raziskava (ca. 1 ura). Družina »%s« se je %s pojavila %d-krat. Primer: isti vzrok je bil zakrpan "
        "že večkrat in vsaka zakrpa je pustila novo luknjo. Če nadaljujemo s popravki po enega, se krog vrti naprej. "
        "Naloga: poišči skupni vzrok teh popravkov in predlagaj en trajen popravek v jedru, ne še ene zakrpe. "
        "Odvisno od: nič. Blokira: nadaljnje popravke v tej družini.\n\n"
        "Kaj družina pomeni: %s\n\n## Commiti (repozitorij / SHA / prva vrstica)\n%s\n\n"
        "Vir: samodejno iz stej.py (družine v 00-system/napake/druzine.json).\n"
    ) % (naslov.replace('"', "'"), ime, kje, len(popravki), definicija, seznam)
    pot.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(pot, "x", encoding="utf-8") as f:  # 'x' = ne prepiši, če je med tem nastala
            f.write(telo)
    except FileExistsError:
        return None
    if not os.environ.get("NAPAKE_BREZ_DB"):
        try:
            subprocess.run(
                [sys.executable, MAIOS_DB, "upsert", "--task", id_, "--spec", str(pot),
                 "--type", "research", "--owner", "claude-code", "--status", "backlog"],
                capture_output=True, text=True, timeout=60)
        except Exception as e:
            zapisi_log("DB upsert ni uspel za %s: %s" % (id_, e))
    return id_


def preglej(popravki, razlog, zdaj, znane):
    odprte = []
    for slug, l in sorted(zadetki(popravki, znane).items()):
        id_ = odpri_kartico(slug, znane.get(slug), l, razlog, zdaj)
        if id_:
            odprte.append(id_)
            zapisi_log("%s | družina %s x%d | kartica odprta: %s" % (razlog, slug, len(l), id_))
        elif razlog == "dnevno":  # pri oknu ob vsakem commitu bi to samo zasulo log
            zapisi_log("%s | družina %s x%d | kartica že odprta" % (razlog, slug, len(l)))
    return odprte


def stanje_preberi():
    try:
        return json.loads((MAPA / "stanje-stetja.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"videni": []}


def stanje_zapisi(s):
    pot = MAPA / "stanje-stetja.json"
    tmp = pot.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, pot)


def zgodovina(pot_csv):
    """Suh preizkus: drseče okno 10 popravkov in dnevne preverbe ob 20:00 čez zgodovino. Nič ne zapiše."""
    znane = druzine()
    p = []
    with open(pot_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["vrsta"] == "popravek" and r["prenos"] != "da":
                cas = dt.datetime.strptime(r["datum"], "%Y-%m-%d %H:%M")
                p.append(Popravek(r["repo"], r["sha"], cas, r.get("napaka", ""), r["druzina"]))
    p.sort(key=lambda x: (x.cas, x.sha))
    dogodki = []
    for i in range(len(p)):
        dogodki.append((p[i].cas, 0, "okno ob %s/%s" % (p[i].repo, p[i].sha), p[max(0, i - OKNO_POPRAVKOV + 1):i + 1]))
    dan = p[0].cas.replace(hour=20, minute=0)
    while dan <= p[-1].cas + dt.timedelta(days=1):
        okno = [x for x in p if dan - OKNO <= x.cas <= dan]
        dogodki.append((dan, 1, "dnevno", okno))
        dan += dt.timedelta(days=1)
    dogodki.sort(key=lambda d: (d[0], d[1]))
    odprte = {}
    print("popravkov (brez prenosa): %d; drseče okno zadnjih %d popravkov" % (len(p), OKNO_POPRAVKOV))
    for cas, _, kaj, sez in dogodki:
        for slug, l in sorted(zadetki(sez, znane).items()):
            if slug in odprte:
                continue  # v zgodovini ne vemo, kdaj bi Chebo kartico zaprl: prvič odprta ostane odprta
            odprte[slug] = cas
            print("%s  %-34s  KARTICA %s (x%d v oknu)" % (cas.strftime("%Y-%m-%d %H:%M"), kaj, slug, len(l)))
    print("--- povzetek: prva kartica po družini")
    for slug, cas in sorted(odprte.items(), key=lambda x: x[1]):
        print("%s  %s" % (cas.strftime("%Y-%m-%d %H:%M"), slug))
    return odprte


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dnevno", action="store_true")
    ap.add_argument("--zgodovina", metavar="CSV")
    a = ap.parse_args(argv)
    if a.zgodovina:
        zgodovina(a.zgodovina)
        return 0
    MAPA.mkdir(parents=True, exist_ok=True)
    with open(MAPA / ".stej.lock", "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return 0  # teče drug zagon; štetje je iz gita, naslednji zagon ujame vse
        znane = druzine()
        zdaj = dt.datetime.now()
        popravki = zberi_popravke()
        if a.dnevno:
            okno = [p for p in popravki if zdaj - OKNO <= p.cas <= zdaj]
            preglej(okno, "dnevno", zdaj, znane)
            return 0
        s = stanje_preberi()
        videni = set(s.get("videni", []))
        novi = [p for p in popravki if p.kljuc not in videni]
        indeks = {p.kljuc: i for i, p in enumerate(popravki)}
        for p in novi:  # ob vsakem novem popravku pogledamo zadnjih 10 do njega
            i = indeks[p.kljuc]
            preglej(popravki[max(0, i - OKNO_POPRAVKOV + 1):i + 1], "okno", zdaj, znane)
            videni.add(p.kljuc)
        s["videni"] = sorted(videni)
        s["zadnji_zagon"] = zdaj.isoformat(timespec="seconds")
        stanje_zapisi(s)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        zapisi_log("NAPAKA stej.py: %r" % (e,))
        sys.exit(1)
