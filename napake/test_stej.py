#!/usr/bin/env python3
"""Testi za commit-msg hook in stej.py (unittest, stdlib, začasni git repozitoriji).

Zagon: python3 -m unittest -v test_stej   (v mapi 00-system/napake)
"""
import datetime as dt
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MAPA = Path(__file__).resolve().parent
HOOK = MAPA / "git-hooks" / "commit-msg"
STEJ = MAPA / "stej.py"
CSV = Path("/home/chebo/.config/Claude/side-session-notes/local_0cfa2963-85a7-4e00-887a-81cfca7853e9/ontologija-vse.csv")
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]


def okolje(**dodatno):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and not k.startswith("NAPAKE_")}
    e.update(dodatno)
    return e


class HookTest(unittest.TestCase):
    def poganjaj(self, sporocilo, nacin):
        with tempfile.NamedTemporaryFile("w", suffix=".msg", delete=False, encoding="utf-8") as f:
            f.write(sporocilo)
        try:
            return subprocess.run([sys.executable, str(HOOK), f.name], capture_output=True, text=True,
                                  env=okolje(NAPAKE_NACIN=nacin))
        finally:
            os.unlink(f.name)

    def test_veljavna_sporocila_gredo_v_obeh_nacinih(self):
        for sp in ("Popravi jed\n\nVrsta: popravek\nDružina: jed-dvakrat-na-listku\n",
                   "Nova funkcija\n\nVrsta: ni-popravek\nPodvrsta: funkcija\n",
                   "Prenos\n\nVrsta: popravek\nDružina: drugo\nPrenos-iz: jana\n"):
            for n in ("opozori", "zavrni"):
                r = self.poganjaj(sp, n)
                self.assertEqual((r.returncode, r.stderr), (0, ""), (sp, n))

    def test_krsitve_opozori_izhod_0_zavrni_izhod_1(self):
        slabi = {
            "brez vrste": "Nekaj\n",
            "popravek brez družine": "Nekaj\n\nVrsta: popravek\n",
            "popravek z neznano družino": "Nekaj\n\nVrsta: popravek\nDružina: izmisljena\n",
            "prej v prvi vrstici": "Gost reče X (prej: Y)\n\nVrsta: ni-popravek\nPodvrsta: test\n",
            "neznana vrsta": "Nekaj\n\nVrsta: nekaj\n",
        }
        for ime, sp in slabi.items():
            r = self.poganjaj(sp, "opozori")
            self.assertEqual(r.returncode, 0, ime)
            self.assertIn("OPOZORILO", r.stderr, ime)
            r = self.poganjaj(sp, "zavrni")
            self.assertEqual(r.returncode, 1, ime)
            self.assertIn("ZAVRNJENO", r.stderr, ime)

    def test_merge_in_fixup_izvzeta(self):
        for sp in ("Merge pull request #6 from x/y\n", "fixup! Nekaj\n", "squash! Nekaj\n"):
            self.assertEqual(self.poganjaj(sp, "zavrni").returncode, 0, sp)

    def test_komentarji_git_se_ignorirajo(self):
        sp = "Nekaj\n\nVrsta: popravek\nDružina: drugo\n# Vrsta: ni-popravek\n"
        self.assertEqual(self.poganjaj(sp, "zavrni").returncode, 0)

    def test_prav_commit_prek_gita_z_hooksPath(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True, env=okolje())
            subprocess.run(["git", "-C", d, "config", "core.hooksPath", str(MAPA / "git-hooks")], check=True)
            r = subprocess.run(GIT + ["-C", d, "commit", "--allow-empty", "-q", "-m", "brez vrste"],
                               capture_output=True, text=True, env=okolje(NAPAKE_NACIN="zavrni"))
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("ZAVRNJENO", r.stderr)
            r = subprocess.run(GIT + ["-C", d, "commit", "--allow-empty", "-q", "-m", "brez vrste"],
                               capture_output=True, text=True, env=okolje(NAPAKE_NACIN="opozori", NAPAKE_MAPA=d, NAPAKE_BREZ_DB="1"))
            self.assertEqual(r.returncode, 0)
            self.assertIn("OPOZORILO", r.stderr)


class StejTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.repo = t / "repo-a"
        self.repo2 = t / "repo-b"
        for r in (self.repo, self.repo2):
            subprocess.run(["git", "init", "-q", str(r)], check=True, env=okolje())
        self.mapa = t / "napake"
        self.kanban = t / "05-tasks"
        for m in ("backlog", "in-progress", "needs-review", "done"):
            (self.kanban / m).mkdir(parents=True)
        self.env = okolje(NAPAKE_MAPA=str(self.mapa), NAPAKE_KANBAN=str(self.kanban),
                          NAPAKE_REPOS="%s:%s" % (self.repo, self.repo2), NAPAKE_BREZ_DB="1")
        self.n = 0

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, druzina, vrsta="popravek", repo=None, ure_nazaj=0.0, extra=""):
        self.n += 1
        cas = (dt.datetime.now() - dt.timedelta(hours=ure_nazaj, seconds=100 - self.n)).strftime("%Y-%m-%dT%H:%M:%S")
        sp = "Commit %d\n\nVrsta: %s\n" % (self.n, vrsta)
        if druzina:
            sp += "Družina: %s\n" % druzina
        sp += extra
        subprocess.run(GIT + ["-C", str(repo or self.repo), "commit", "--allow-empty", "-q", "-m", sp],
                       check=True, env=okolje(GIT_AUTHOR_DATE=cas, GIT_COMMITTER_DATE=cas))

    def stej(self, *args):
        r = subprocess.run([sys.executable, str(STEJ), *args], capture_output=True, text=True, env=self.env)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def kartice(self, mapa="backlog"):
        return sorted(p.name for p in (self.kanban / mapa).glob("*-analiza-vzroka-*.md"))

    def test_tretji_popravek_v_oknu_10_sprozi_kartico(self):
        self.commit("jed-dvakrat-na-listku")
        self.commit("jed-dvakrat-na-listku", repo=self.repo2)  # čez repozitorije
        self.stej()
        self.assertEqual(self.kartice(), [])
        for f in ("drugo", "zunanji-ponudnik", "vprasanje-v-zanki", "oddaja-odloci-model"):
            self.commit(f)
        self.commit("jed-dvakrat-na-listku")  # 7. popravek, tretji te družine
        self.stej()
        self.assertEqual(len(self.kartice()), 1)

    def test_tretji_popravek_zunaj_okna_ne_sprozi(self):
        self.commit("jed-dvakrat-na-listku")
        self.commit("jed-dvakrat-na-listku")
        for i in range(9):  # 9 drugih, vsak drugačen: v oknu 10 je tretji že na 12. mestu
            self.commit(["drugo", "zunanji-ponudnik", "vprasanje-v-zanki", "oddaja-odloci-model",
                         "novo-prepise-staro", "obrat-brez-govorca", "slisanost-napacen-dokaz",
                         "priloga-ze-v-jedi", "prepis-brez-prilagoditve"][i])
        self.commit("jed-dvakrat-na-listku")  # prvi je pravkar izpadel iz okna zadnjih 10
        self.stej()
        self.assertEqual(self.kartice(), [])

    def test_okno_ob_vsakem_commitu_tudi_pri_vec_novih_naenkrat_in_po_enega(self):
        self.commit("drugo")
        self.stej()
        self.commit("drugo")
        self.stej()
        self.assertEqual(self.kartice(), [])
        self.commit("drugo")
        self.stej()
        self.assertEqual(len(self.kartice()), 1)

    def test_prenos_in_ni_popravek_se_ne_stejeta(self):
        for _ in range(5):
            self.commit("jed-dvakrat-na-listku", extra="Prenos-iz: jana\n")
        for _ in range(5):
            self.commit(None, vrsta="ni-popravek", extra="Podvrsta: test\n")
        self.stej()
        self.assertEqual(self.kartice(), [])
        self.assertEqual(self.stanje()["videni"], [])

    def stanje(self):
        import json
        return json.loads((self.mapa / "stanje-stetja.json").read_text(encoding="utf-8"))

    def test_kartica_vsebina_in_brez_podvojene(self):
        for _ in range(10):
            self.commit("jed-dvakrat-na-listku")
        self.stej()
        k = self.kartice()
        self.assertEqual(len(k), 1)
        self.assertTrue(k[0].endswith("-analiza-vzroka-jed-dvakrat-na-listku.md"))
        t = (self.kanban / "backlog" / k[0]).read_text(encoding="utf-8")
        self.assertIn("status: backlog", t)
        self.assertIn("owner: claude-code", t)
        self.assertIn("type: research", t)
        self.assertIn("title: \"Glasovni agenti — analiza vzroka: Jed dvakrat na listku (", t)
        self.assertEqual(t.count("- repo-a / "), 3)
        # nov paket iste družine: kartica je odprta, nove ne sme biti
        for _ in range(10):
            self.commit("jed-dvakrat-na-listku")
        self.stej()
        self.assertEqual(len(self.kartice()), 1)
        # tudi kartica v in-progress in needs-review šteje za odprto
        (self.kanban / "backlog" / k[0]).rename(self.kanban / "in-progress" / k[0])
        for _ in range(10):
            self.commit("jed-dvakrat-na-listku")
        self.stej()
        self.assertEqual(self.kartice(), [])
        self.assertEqual(len(self.kartice("in-progress")), 1)
        (self.kanban / "in-progress" / k[0]).rename(self.kanban / "needs-review" / k[0])
        for _ in range(10):
            self.commit("jed-dvakrat-na-listku")
        self.stej()
        self.assertEqual(self.kartice(), [])
        # zaprta (done) kartica ni odprta: nova se sme odpreti
        (self.kanban / "needs-review" / k[0]).rename(self.kanban / "done" / k[0])
        for _ in range(10):
            self.commit("jed-dvakrat-na-listku")
        self.stej()
        self.assertEqual(len(self.kartice()), 1)

    def test_ponoven_zagon_ne_steje_dvakrat(self):
        for _ in range(10):
            self.commit("drugo")
        self.stej()
        self.stej()
        self.assertEqual(len(self.stanje()["videni"]), 10)
        self.assertEqual(len(self.kartice()), 1)
        self.assertEqual(len((self.mapa / "opozorila.log").read_text(encoding="utf-8").splitlines()), 1)

    def test_dnevno_samo_zadnjih_24_ur(self):
        for _ in range(3):
            self.commit("zunanji-ponudnik", ure_nazaj=30)
        self.stej("--dnevno")
        self.assertEqual(self.kartice(), [])
        for _ in range(3):
            self.commit("vprasanje-v-zanki", ure_nazaj=2)
        self.stej("--dnevno")
        self.assertEqual(len(self.kartice()), 1)
        self.assertIn("vprasanje-v-zanki", self.kartice()[0])
        self.assertIn("kartica odprta", (self.mapa / "opozorila.log").read_text(encoding="utf-8"))

    def test_kartica_zapise_vrstico_v_db(self):
        db = Path(self.tmp.name) / "test.db"
        ok = okolje(MAIOS_DB=str(db))
        self.assertEqual(subprocess.run([sys.executable, "/home/chebo/MAIOS/00-system/db/maios_db.py", "init"],
                                        capture_output=True, text=True, env=ok).returncode, 0)
        self.env = dict(self.env, MAIOS_DB=str(db))
        del self.env["NAPAKE_BREZ_DB"]
        for _ in range(10):
            self.commit("oddaja-odloci-model")
        self.stej()
        r = subprocess.run([sys.executable, "/home/chebo/MAIOS/00-system/db/maios_db.py", "tasks", "--status", "backlog"],
                           capture_output=True, text=True, env=ok)
        self.assertIn("analiza-vzroka-oddaja-odloci-model", r.stdout)


@unittest.skipUnless(CSV.exists(), "zgodovinski CSV ni na voljo")
class ZgodovinaTest(unittest.TestCase):
    def test_jed_dvakrat_se_pokaze_17_11_popoldne(self):
        r = subprocess.run([sys.executable, str(STEJ), "--zgodovina", str(CSV)], capture_output=True, text=True,
                           env=okolje())
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("popravkov (brez prenosa): 473", r.stdout)
        vrstica = [v for v in r.stdout.splitlines() if "KARTICA jed-dvakrat-na-listku" in v]
        self.assertEqual(len(vrstica), 1)
        self.assertTrue(vrstica[0].startswith("2026-11-17 15:"), vrstica[0])


if __name__ == "__main__":
    unittest.main()
