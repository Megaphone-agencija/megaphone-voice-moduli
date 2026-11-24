#!/usr/bin/env python3
"""Testi za pripravljeno.py. Zagon: cd scripts && python3 -m unittest test_pripravljeno -v

Vsak test dela v začasnem git repozitoriju; podatkovna mapa in CSV skritih oblik sta začasna
(PRIPRAVLJENO_MAPA, PRIPRAVLJENO_SKRITE_CSV), prave datoteke v MAIOS se ne dotaknejo.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SKRIPTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pripravljeno.py")
GIT = ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false"]

AGENT_STARI = 'def pecenost():\n    return "Pečenost?"\n'
AGENT_NOVI = 'def pecenost():\n    return "Kako pečen naj bo?"\n\n\ndef nova():\n    return 1\n'
TEST_OSNOVA = '''import unittest
import agent


class TestAgent(unittest.TestCase):
    def test_osnova(self):
        self.assertTrue(agent.pecenost())
'''
TEST_REPRO = TEST_OSNOVA + '''
    def test_pecenost(self):
        # klic: scenarij-12 (gost reče "srednje")
        # CL: T-PE-01
        self.assertEqual(agent.pecenost(), "Kako pečen naj bo?")
'''
CL_PRIMER = "# CL\n\n| ID | Zahteva | Nosilec | Merilo | Test | Status |\n|---|---|---|---|---|---|\n" \
            "| T-PE-01 | Agent vpraša, kako pečen naj bo. | Koda | Vprašanje je dobesedno enako | tests/test_agent.py::TestAgent::test_pecenost | potrjeno |\n"
SPOROCILO = "Popravek pečenosti\n\nDružina: pomen po seznamu besed\nReprodukcija: tests/test_agent.py::TestAgent::test_pecenost\n"
TEST_ID = "tests/test_agent.py::TestAgent::test_pecenost"


def sporocilo(repro=TEST_ID, druzina=True):
    s = "Popravek pečenosti\n\n"
    if druzina:
        s += "Družina: pomen po seznamu besed\n"
    if repro is not None:
        s += f"Reprodukcija: {repro}\n"
    return s


def zazeni(*ukaz, cwd=None):
    p = subprocess.run(ukaz, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{ukaz}: {p.stderr}")
    return p.stdout.strip()


def zgradi_repo(koren, popravki, ime="repo-test"):
    """main: agent.py + tests/test_agent.py; veja popravek: seznam (datoteke, sporočilo). Na koncu je izvlečen popravek."""
    repo = os.path.join(koren, ime)
    os.makedirs(os.path.join(repo, "tests"))
    zazeni("git", "init", "-q", "-b", "main", repo)

    def zapisi(datoteke):
        for pot, vsebina in datoteke.items():
            os.makedirs(os.path.dirname(os.path.join(repo, pot)), exist_ok=True)
            with open(os.path.join(repo, pot), "w", encoding="utf-8") as f:
                f.write(vsebina)

    def commit(sporocilo_):
        zazeni(*GIT, "-C", repo, "add", "-A")
        zazeni(*GIT, "-C", repo, "commit", "-q", "-m", sporocilo_)

    zapisi({"agent.py": AGENT_STARI, "tests/test_agent.py": TEST_OSNOVA})
    commit("Začetek")
    zazeni("git", "-C", repo, "checkout", "-q", "-b", "popravek")
    for datoteke, sp in popravki:
        zapisi(datoteke)
        commit(sp)
    return repo


def standardni_popravki():
    return [({"agent.py": AGENT_NOVI, "tests/test_agent.py": TEST_REPRO}, SPOROCILO),
            ({"README.md": "opis\n"}, "Drobno čiščenje")]


KLICNI_LIST = "## Klicni list\n1. Gost: »Ja, lahko daš.« → agent odda naročilo.\n2. Nasprotno: »V redu, hvala, nasvidenje.« → agent ne odda.\n3. Ne pokrije: nič znanega.\n"
POROCILO_OK = ("## Povzetek\nbla\n\n**Ne pokrije:** nič znanega\n\n## Oblike\n"
               + "".join(f"- oblika {i}\n" for i in range(1, 8))
               + "".join(f"- {i} nasprotna: oblika {i}\n" for i in range(8, 11))
               + "\n" + KLICNI_LIST + "\n## Naprej\n- ni oblika\n")
SKRITE_OK = '''import unittest
import agent


class TestSkrite(unittest.TestCase):
    def test_oblika_1(self):
        self.assertTrue(agent.pecenost())

    def test_oblika_2(self):
        self.assertIn("pečen", agent.pecenost())

    def test_oblika_3(self):
        self.assertTrue(agent.nova())
'''
SKRITE_RDECE = SKRITE_OK.replace('self.assertIn("pečen", agent.pecenost())', 'self.assertEqual(agent.pecenost(), "nekaj tretjega")')


class Osnova(unittest.TestCase):
    def setUp(self):
        self.koren = tempfile.mkdtemp(prefix="test-pripravljeno-")
        self.addCleanup(shutil.rmtree, self.koren, True)
        self.podatki = os.path.join(self.koren, "podatki")
        self.csv = os.path.join(self.koren, "napake", "skrite-oblike.csv")
        self.env = dict(os.environ, PRIPRAVLJENO_MAPA=self.podatki, PRIPRAVLJENO_SKRITE_CSV=self.csv)

    @staticmethod
    def citaj(pot):
        with open(pot, encoding="utf-8") as f:
            return f.read().splitlines()

    def mapa_repoja(self, repo):
        m = os.path.join(self.podatki, os.path.basename(repo))
        os.makedirs(m, exist_ok=True)
        return m

    def zagon(self, repo, *args, preveri_cisto=True):
        p = subprocess.run([sys.executable, SKRIPTA, repo, "--osnova", "main", "--python", sys.executable, *args],
                           capture_output=True, text=True, env=self.env)
        if preveri_cisto:
            self.preveri_cisto(repo)
        return p.returncode, p.stdout + p.stderr

    def preveri_cisto(self, repo):
        wt = zazeni("git", "-C", repo, "worktree", "list")
        self.assertEqual(len(wt.splitlines()), 1, f"ostal je worktree:\n{wt}")
        self.assertEqual(zazeni("git", "-C", repo, "status", "--porcelain"), "", "repozitorij ni čist")

    def vrstica(self, izhod, vsebuje):
        v = [x for x in izhod.splitlines() if vsebuje in x]
        self.assertTrue(v, f"ni vrstice z »{vsebuje}« v:\n{izhod}")
        return v[0]


class Reprodukcija(Osnova):
    def zgradi(self, popravki):
        return zgradi_repo(self.koren, popravki)

    def test_1_ok(self):
        repo = self.zgradi(standardni_popravki())
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[OK]"), izhod)
        self.assertIn("pade pred popravkom (preverba)", v)
        self.assertIn("pred: AssertionError", izhod)  # simptom padca je v izpisu
        self.assertIn("1 commit brez oznake popravka", izhod)
        self.assertTrue(os.path.exists(os.path.join(self.mapa_repoja(repo), zazeni("git", "-C", repo, "rev-list", "--reverse", "main..popravek").splitlines()[0][:12] + "-reprodukcija-pred.txt")))

    def test_1b_ok_ko_je_izvlecena_main(self):
        repo = self.zgradi(standardni_popravki())
        zazeni("git", "-C", repo, "checkout", "-q", "main")
        rc, izhod = self.zagon(repo, "--veja", "popravek", "--brez-testov")
        self.assertTrue(self.vrstica(izhod, "reprodukcija ").startswith("[OK]"), izhod)

    def test_2_sesutje_ni_dokaz(self):
        test = TEST_OSNOVA + '\n    def test_pecenost(self):\n        # klic: x\n        self.assertEqual(agent.nova(), 1)\n'
        repo = self.zgradi([({"agent.py": AGENT_NOVI, "tests/test_agent.py": test}, SPOROCILO)])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]"), izhod)
        self.assertIn("sesuje", v)
        self.assertIn("AttributeError", v)
        self.assertIn("ni dokaz", v)

    def test_2b_sesutje_zaradi_uvoza(self):
        test = "import unittest\nimport agent\nfrom agent import nova_stvar\n\n\nclass TestAgent(unittest.TestCase):\n    def test_pecenost(self):\n        # klic: x\n        self.assertTrue(nova_stvar)\n"
        agent = AGENT_STARI + "\nnova_stvar = 1\n"
        repo = self.zgradi([({"agent.py": agent, "tests/test_agent.py": test}, SPOROCILO)])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]") and "sesuje" in v and "ImportError" in v, izhod)

    def test_3_test_ne_ujame_napake(self):
        test = TEST_OSNOVA + '\n    def test_pecenost(self):\n        # klic: x\n        self.assertTrue(agent.pecenost())\n'
        repo = self.zgradi([({"agent.py": AGENT_NOVI, "tests/test_agent.py": test}, SPOROCILO)])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]") and "ne ujame napake" in v, izhod)

    def test_3b_po_popravku_ne_gre_skozi(self):
        test = TEST_OSNOVA + '\n    def test_pecenost(self):\n        # klic: x\n        self.assertEqual(agent.pecenost(), "nekaj tretjega")\n'
        repo = self.zgradi([({"agent.py": AGENT_NOVI, "tests/test_agent.py": test}, SPOROCILO)])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]") and "po popravku" in v, izhod)
        self.assertIn("pred: AssertionError: 'Pečenost?' != 'nekaj tretjega'", izhod)  # simptom tudi pri NE

    def test_4_brez_klic(self):
        test = TEST_REPRO.replace('        # klic: scenarij-12 (gost reče "srednje")\n', "")
        repo = self.zgradi([({"agent.py": AGENT_NOVI, "tests/test_agent.py": test}, SPOROCILO)])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]") and "# klic:" in v, izhod)
        self.assertIn("pred: AssertionError", izhod)

    def test_4b_klic_tri_vrstice_nad_def(self):
        test = TEST_REPRO.replace('        # klic: scenarij-12 (gost reče "srednje")\n', "").replace(
            "    def test_pecenost", "    # klic: scenarij-12\n    def test_pecenost")
        repo = self.zgradi([({"agent.py": AGENT_NOVI, "tests/test_agent.py": test}, SPOROCILO)])
        rc, izhod = self.zagon(repo, "--brez-testov")
        self.assertTrue(self.vrstica(izhod, "reprodukcija ").startswith("[OK]"), izhod)

    def test_4c_pikcasta_oblika(self):
        repo = self.zgradi([({"agent.py": AGENT_NOVI, "tests/test_agent.py": TEST_REPRO},
                             sporocilo("tests.test_agent.TestAgent.test_pecenost"))])
        rc, izhod = self.zagon(repo, "--brez-testov")
        self.assertTrue(self.vrstica(izhod, "reprodukcija ").startswith("[OK]"), izhod)

    def test_5_druzina_brez_reprodukcije_in_izjema(self):
        repo = self.zgradi([({"agent.py": AGENT_NOVI}, sporocilo(repro=None))])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]") and "Reprodukcija" in v, izhod)
        sha = zazeni("git", "-C", repo, "rev-parse", "popravek")
        rc, izhod = self.zagon(repo, "--brez-testov", "--izjema", sha[:10])
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[OK]") and "izjema (ročno)" in v, izhod)

    def test_5b_reprodukcija_ni(self):
        repo = self.zgradi([({"agent.py": AGENT_NOVI}, sporocilo(repro="ni — popravek besedila vprašanja"))])
        rc, izhod = self.zagon(repo, "--brez-testov")
        v = self.vrstica(izhod, "reprodukcija ")
        self.assertTrue(v.startswith("[NE]") and "popravek besedila vprašanja" in v, izhod)
        sha = zazeni("git", "-C", repo, "rev-parse", "popravek")
        rc, izhod = self.zagon(repo, "--brez-testov", "--izjema", sha[:7])
        self.assertTrue(self.vrstica(izhod, "reprodukcija ").startswith("[OK]"), izhod)

    def test_5c_commit_brez_oznak_se_samo_steje(self):
        repo = self.zgradi([({"README.md": "a\n"}, "Eno"), ({"README.md": "b\n"}, "Dva")])
        rc, izhod = self.zagon(repo, "--brez-testov")
        self.assertIn("2 commita brez oznake popravka", izhod)
        self.assertNotIn("[NE] reprodukcija", izhod)


class Standardni(Osnova):
    """Osnova za teste na standardnem repozitoriju (popravek + čiščenje)."""

    def setUp(self):
        super().setUp()
        self.repo = zgradi_repo(self.koren, standardni_popravki())
        self.tip = zazeni("git", "-C", self.repo, "rev-parse", "popravek")
        self.mapa = self.mapa_repoja(self.repo)

    def zapisi(self, pot, vsebina):
        with open(pot, "w", encoding="utf-8") as f:
            f.write(vsebina)
        return pot


class Simptom(unittest.TestCase):
    def test_assertionerror_je_vedno_med_izpisanimi(self):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import pripravljeno
        tb = ('Traceback (most recent call last):\n  File "t.py", line 3, in test\n    self.assertEqual(a, b)\n'
              'AssertionError: \'a\' != \'b\'\n  File "v sporočilu", line 1\n    nekaj\n' + "".join(f"- vrstica {i}\n" for i in range(30)))
        izpis = pripravljeno.simptom(tb)
        self.assertTrue(izpis[0].startswith("AssertionError"), izpis)
        self.assertLessEqual(len(izpis), 15)
        # brez AssertionError (druga izjema): ostane izjema za zadnjim okvirjem
        self.assertEqual(pripravljeno.simptom('Traceback\n  File "t.py", line 3, in t\n    x()\nKeyError: 1\n'), ["KeyError: 1"])


class DatotekePogojev(Standardni):
    """Poročilo, skrite oblike, pravi model, Codex."""

    # 6. pravi model
    def pravi_model(self, d):
        self.zapisi(os.path.join(self.mapa, f"{self.tip[:12]}-pravi-model.json"), json.dumps(d))
        return self.vrstica(self.zagon(self.repo, "--brez-testov")[1], "pravi model")

    def test_6_pravi_model(self):
        self.assertTrue(self.pravi_model({"sha": self.tip, "teki": 3, "padci": 0, "scenarij": "pečenost"}).startswith("[OK]"))
        self.assertTrue(self.pravi_model({"sha": self.tip[:12], "teki": 5, "padci": 0, "scenarij": "x"}).startswith("[OK]"))
        v = self.pravi_model({"sha": "0" * 40, "teki": 3, "padci": 0, "scenarij": "x"})
        self.assertTrue(v.startswith("[NE]") and "ni vrh veje" in v, v)
        v = self.pravi_model({"sha": self.tip, "teki": 2, "padci": 0, "scenarij": "x"})
        self.assertTrue(v.startswith("[NE]") and "teki 2" in v, v)
        v = self.pravi_model({"sha": self.tip, "teki": 3, "padci": 1, "scenarij": "x"})
        self.assertTrue(v.startswith("[NE]") and "padci 1" in v, v)

    def test_6b_pravi_model_manjka(self):
        v = self.vrstica(self.zagon(self.repo, "--brez-testov")[1], "pravi model")
        self.assertTrue(v.startswith("[NE]") and f"ni datoteke {self.tip[:12]}-pravi-model.json" in v, v)

    # 7. Codex
    def codex(self, vsebina):
        if vsebina is not None:
            self.zapisi(os.path.join(self.mapa, f"{self.tip[:12]}-codex.txt"), vsebina)
        return self.vrstica(self.zagon(self.repo, "--brez-testov")[1], "codex")

    def test_7_codex(self):
        self.assertTrue(self.codex("\n  Brez Blokatorja \n").startswith("[OK]"))
        self.assertTrue(self.codex("Blokator: Jana pade.\n").startswith("[NE]"))
        izhod = self.zagon(self.repo, "--brez-testov")[1]
        self.assertIn("Blokator: Jana pade.", izhod)

    def test_7b_codex_manjka(self):
        v = self.codex(None)
        self.assertTrue(v.startswith("[NE]") and "ni datoteke" in v, v)

    # 4. poročilo
    def porocilo(self, besedilo):
        pot = self.zapisi(os.path.join(self.koren, "porocilo.md"), besedilo)
        return self.vrstica(self.zagon(self.repo, "--brez-testov", "--porocilo", pot)[1], "poročilo")

    def test_8_porocilo(self):
        v = self.porocilo(POROCILO_OK)
        self.assertTrue(v.startswith("[OK]") and "Oblike 10" in v, v)
        v = self.porocilo(POROCILO_OK.replace("- 10 nasprotna: oblika 10\n", ""))
        self.assertTrue(v.startswith("[NE]") and "9 oblik" in v, v)
        v = self.porocilo(POROCILO_OK.replace("**Ne pokrije:** nič znanega", "nekaj drugega"))
        self.assertTrue(v.startswith("[NE]") and "Ne pokrije" in v, v)

    def test_8a_nasprotne_oblike_in_klicni_list(self):
        v = self.porocilo(POROCILO_OK)
        self.assertTrue(v.startswith("[OK]") and "nasprotnih 3" in v and "Klicni list" in v, v)
        # velike črke ne štejejo
        v = self.porocilo(POROCILO_OK.replace("nasprotna", "NASPROTNA"))
        self.assertTrue(v.startswith("[OK]"), v)
        # 2 ali 1 nasprotna (skupaj še vedno 10 oblik) -> NE
        v = self.porocilo(POROCILO_OK.replace("- 10 nasprotna: oblika 10", "- 10 oblika 10"))
        self.assertTrue(v.startswith("[NE]") and "je 2 nasprotnih oblik, treba jih je vsaj 3" in v, v)
        v = self.porocilo(POROCILO_OK.replace("- 10 nasprotna: oblika 10", "- 10 oblika 10").replace("- 9 nasprotna: oblika 9", "- 9 oblika 9"))
        self.assertTrue(v.startswith("[NE]") and "je 1 nasprotnih oblik, treba jih je vsaj 3" in v, v)
        # brez Klicnega lista -> NE; naslov brez vrstic -> NE
        v = self.porocilo(POROCILO_OK.replace(KLICNI_LIST, ""))
        self.assertTrue(v.startswith("[NE]") and "manjka Klicni list" in v, v)
        v = self.porocilo(POROCILO_OK.replace(KLICNI_LIST, "## Klicni list\n\n"))
        self.assertTrue(v.startswith("[NE]") and "manjka Klicni list" in v, v)

    def test_8b_porocilo_tabela_in_obvezno(self):
        tabela = ("ne pokrije: nič\n\n## Oblike\n| št | oblika | skupina nasprotna |\n|---|---|---|\n"
                  + "".join(f"| {i} | x |\n" for i in range(7)) + "".join(f"| {i} | x | nasprotna |\n" for i in range(3))
                  + "\n" + KLICNI_LIST)
        self.assertTrue(self.porocilo(tabela).startswith("[OK]"))
        izhod = self.zagon(self.repo, "--brez-testov")[1]  # brez --porocilo, a je Družina
        self.assertTrue(self.vrstica(izhod, "poročilo").startswith("[NE]"), izhod)

    # 5. skrite oblike
    def skrite(self, vsebina, *dodatno):
        pot = self.zapisi(os.path.join(self.koren, "skrite.py"), vsebina)
        return self.zagon(self.repo, "--brez-testov", "--skrite", pot, *dodatno)[1]

    def test_9_skrite_zelene_in_csv(self):
        izhod = self.skrite(SKRITE_OK, "--model", "sonnet-high")
        self.assertTrue(self.vrstica(izhod, "skrite oblike").startswith("[OK]"), izhod)
        self.assertIn("3 od 3 zelenih", izhod)
        vr = self.citaj(self.csv)
        self.assertEqual(vr[0], "datum,repo,veja,sha,model,vseh,padlo")
        self.assertEqual(len(vr), 2)
        self.assertTrue(vr[1].endswith(f"repo-test,popravek,{self.tip[:12]},sonnet-high,3,0"), vr[1])
        self.skrite(SKRITE_RDECE, "--model", "sonnet-high")  # ponovni zagon istega SHA zamenja vrstico (zadnji velja)
        vr = self.citaj(self.csv)
        self.assertEqual(len(vr), 2)
        self.assertTrue(vr[1].endswith("sonnet-high,3,1"), vr)

    def test_9b_skrita_rdeca(self):
        izhod = self.skrite(SKRITE_RDECE)
        v = self.vrstica(izhod, "skrite oblike")
        self.assertTrue(v.startswith("[NE]") and "2 od 3 zelenih (test_oblika_2)" in v, izhod)
        vr = self.citaj(self.csv)
        self.assertTrue(vr[1].endswith("neznano,3,1"), vr)

    def test_9c_skrite_z_napako_uvoza(self):
        izhod = self.skrite("import ne_obstaja\n")
        self.assertTrue(self.vrstica(izhod, "skrite oblike").startswith("[NE]"), izhod)
        self.assertIn("ne naložijo", izhod)
        self.assertFalse(os.path.exists(self.csv), "pokvarjena datoteka ni meritev, vrstice ne sme biti")

    def test_9d_skrite_manjkajo(self):
        izhod = self.zagon(self.repo, "--brez-testov")[1]
        v = self.vrstica(izhod, "skrite oblike")
        self.assertTrue(v.startswith("[NE]") and "ni skritih oblik" in v, izhod)
        self.assertFalse(os.path.exists(self.csv))


class Celota(Standardni):
    def pogoji(self):
        self.zapisi(os.path.join(self.mapa, f"{self.tip[:12]}-pravi-model.json"),
                    json.dumps({"sha": self.tip, "teki": 3, "padci": 0, "scenarij": "pečenost"}))
        self.zapisi(os.path.join(self.mapa, f"{self.tip[:12]}-codex.txt"), "brez blokatorja\n")
        return ["--porocilo", self.zapisi(os.path.join(self.koren, "porocilo.md"), POROCILO_OK),
                "--skrite", self.zapisi(os.path.join(self.koren, "skrite.py"), SKRITE_OK)]

    def test_11_brez_testov_ni_zrelo(self):
        rc, izhod = self.zagon(self.repo, "--brez-testov", *self.pogoji())
        self.assertEqual(rc, 1, izhod)
        self.assertIn("NI PREVERJENO", izhod)
        self.assertIn("IZID: NI ZRELO (1 razlog)", izhod)

    def test_11b_zrelo_v_delovni_mapi(self):
        rc, izhod = self.zagon(self.repo, *self.pogoji())
        self.assertEqual(rc, 0, izhod)
        self.assertIn("IZID: ZRELO", izhod)
        self.assertTrue(self.vrstica(izhod, "testi:").startswith("[OK]"), izhod)
        self.assertIn("[OPOZORILO] CL ni najden", izhod)

    def test_11a_klicni_list_se_izpise_ob_zrelo(self):
        rc, izhod = self.zagon(self.repo, *self.pogoji())
        self.assertEqual(rc, 0, izhod)
        po_izidu = izhod.split("IZID: ZRELO\n", 1)[1].splitlines()
        self.assertEqual(po_izidu[0], "KLICNI LIST:", izhod)
        self.assertEqual(po_izidu[1:], KLICNI_LIST.splitlines()[1:], izhod)  # kot zapisano, brez naslova
        # NI ZRELO: klicnega lista ni
        rc, izhod = self.zagon(self.repo, "--brez-testov", *self.pogoji())
        self.assertEqual(rc, 1, izhod)
        self.assertNotIn("KLICNI LIST", izhod)
        # več kot 8 vrstic: izpiše prvih 8 in označi ostanek
        dolg = POROCILO_OK.replace(KLICNI_LIST, "## Klicni list\n" + "".join(f"vrstica {i}\n" for i in range(1, 11)))
        pogoji = self.pogoji()
        self.zapisi(pogoji[1], dolg)
        rc, izhod = self.zagon(self.repo, *pogoji)
        self.assertEqual(rc, 0, izhod)
        self.assertIn("vrstica 8\n", izhod)
        self.assertNotIn("vrstica 9", izhod)
        self.assertIn("… še 2", izhod)

    def test_11c_zrelo_na_worktreeju(self):
        zazeni("git", "-C", self.repo, "checkout", "-q", "main")
        rc, izhod = self.zagon(self.repo, "--veja", "popravek", *self.pogoji())
        self.assertEqual(rc, 0, izhod)
        self.assertIn("začasnem worktreeju", izhod)

    def test_11d_cl_najden_sam_in_preverjen(self):
        os.makedirs(os.path.join(self.repo, "docs"))
        self.zapisi(os.path.join(self.repo, "docs", "checklist-agent.md"), CL_PRIMER)
        zazeni(*GIT, "-C", self.repo, "add", "-A")
        zazeni(*GIT, "-C", self.repo, "commit", "-q", "-m", "CL")
        self.tip = zazeni("git", "-C", self.repo, "rev-parse", "popravek")
        self.mapa = self.mapa_repoja(self.repo)
        rc, izhod = self.zagon(self.repo, *self.pogoji())
        self.assertEqual(rc, 0, izhod)
        self.assertIn("[OK] CL: checklist-agent.md", izhod)
        # CL brez testa v tests/ → NE
        self.zapisi(os.path.join(self.repo, "docs", "checklist-agent.md"), CL_PRIMER.replace("T-PE-01", "T-PE-77"))
        zazeni(*GIT, "-C", self.repo, "add", "-A")
        zazeni(*GIT, "-C", self.repo, "commit", "-q", "-m", "CL pokvarjen")
        self.tip = zazeni("git", "-C", self.repo, "rev-parse", "popravek")
        rc, izhod = self.zagon(self.repo, "--brez-testov", *self.pogoji())
        self.assertIn("[NE] CL:", izhod)

    def test_12_napake_uporabe(self):
        rc, izhod = self.zagon(self.koren, preveri_cisto=False)
        self.assertEqual(rc, 2, izhod)
        rc, izhod = self.zagon(self.repo, "--veja", "ne-obstaja")
        self.assertEqual(rc, 2, izhod)
        rc, izhod = self.zagon(self.repo, "--cl", "/ni/te/datoteke.md")
        self.assertEqual(rc, 2, izhod)

    def test_12b_worktree_odpove_zunaj_reprodukcije(self):
        """git worktree add odpove: [NE] za testi, skrite oblike in reprodukcijo, izhod 1, IZID vseeno izpisan."""
        pravi = shutil.which("git")
        bin_ = os.path.join(self.koren, "bin")
        os.makedirs(bin_)
        with open(os.path.join(bin_, "git"), "w") as f:
            f.write(f'#!/bin/sh\nfor a in "$@"; do [ "$a" = worktree ] && [ "$2" != x ] && for b in "$@"; do [ "$b" = add ] && echo boom >&2 && exit 1; done; done\nexec {pravi} "$@"\n')
        os.chmod(os.path.join(bin_, "git"), 0o755)
        zazeni("git", "-C", self.repo, "checkout", "-q", "main")
        self.env["PATH"] = bin_ + os.pathsep + os.environ["PATH"]
        skrite = self.zapisi(os.path.join(self.koren, "skrite.py"), SKRITE_OK)
        rc, izhod = self.zagon(self.repo, "--veja", "popravek", "--skrite", skrite)
        self.assertEqual(rc, 1, izhod)
        self.assertIn("[NE] testi: napaka pri pripravi worktreeja", izhod)
        self.assertIn("[NE] skrite oblike: napaka pri pripravi worktreeja", izhod)
        self.assertIn("[NE] reprodukcija", izhod)
        self.assertIn("IZID: NI ZRELO", izhod)
        self.assertNotIn("Traceback", izhod)

    def test_13_pythonpath_gre_v_teste(self):
        tema = "import os, unittest\n\n\nclass TestPP(unittest.TestCase):\n    def test_pp(self):\n        self.assertEqual(os.environ.get('PYTHONPATH'), 'tests:.')\n"
        repo = zgradi_repo(self.koren, [({"tests/test_pp.py": tema}, "Dodan test")], ime="repo-pp")
        rc, izhod = self.zagon(repo, "--brez-testov")
        rc, izhod = self.zagon(repo, "--pythonpath", "tests:.")
        self.assertTrue(self.vrstica(izhod, "testi:").startswith("[OK]"), izhod)
        rc, izhod = self.zagon(repo)
        self.assertTrue(self.vrstica(izhod, "testi:").startswith("[NE]"), izhod)

    def test_13b_pythonpath_v_izvajalniku_in_skritih(self):
        """Kot Jože (tests:.:govor): modul v govor/ se uvozi samo prek PYTHONPATH — v reprodukciji (pred/po) in v skritih oblikah."""
        agent = "import pomoc\n\n\ndef odgovor():\n    return pomoc.vrednost()\n"
        test = ("import unittest\nimport agent\n\n\nclass TestPP(unittest.TestCase):\n    def test_odg(self):\n"
                "        # klic: x\n        self.assertEqual(agent.odgovor(), 'novo')\n")
        repo = os.path.join(self.koren, "repo-govor")
        os.makedirs(os.path.join(repo, "govor"))
        zazeni("git", "init", "-q", "-b", "main", repo)
        self.zapisi(os.path.join(repo, "govor", "pomoc.py"), "def vrednost():\n    return 'staro'\n")
        self.zapisi(os.path.join(repo, "agent.py"), agent)
        zazeni(*GIT, "-C", repo, "add", "-A")
        zazeni(*GIT, "-C", repo, "commit", "-q", "-m", "Začetek")
        zazeni("git", "-C", repo, "checkout", "-q", "-b", "popravek")
        os.makedirs(os.path.join(repo, "tests"))
        self.zapisi(os.path.join(repo, "govor", "pomoc.py"), "def vrednost():\n    return 'novo'\n")
        self.zapisi(os.path.join(repo, "tests", "test_pp.py"), test)
        zazeni(*GIT, "-C", repo, "add", "-A")
        zazeni(*GIT, "-C", repo, "commit", "-q", "-m",
               "Popravek\n\nDružina: x\nReprodukcija: tests/test_pp.py::TestPP::test_odg\n")
        skrite = self.zapisi(os.path.join(self.koren, "skrite_pp.py"),
                             "import unittest\nimport pomoc\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.assertEqual(pomoc.vrednost(), 'novo')\n")
        rc, izhod = self.zagon(repo, "--brez-testov", "--skrite", skrite, "--pythonpath", "tests:.:govor")
        self.assertTrue(self.vrstica(izhod, "reprodukcija ").startswith("[OK]"), izhod)
        self.assertIn("pred: AssertionError: 'staro' != 'novo'", izhod)
        self.assertIn("[OK] skrite oblike: 1 od 1 zelenih", izhod)
        rc, izhod = self.zagon(repo, "--brez-testov", "--skrite", skrite)  # brez govor/ na poti
        self.assertIn("sesuje", self.vrstica(izhod, "reprodukcija "))
        self.assertIn("ne naložijo", izhod)


if __name__ == "__main__":
    unittest.main()
