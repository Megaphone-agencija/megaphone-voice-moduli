#!/usr/bin/env python3
"""Determinističen preverjalnik poslovnega checklista (CL) glasovnega agenta.

Uporaba:
  preveri_cl.py POT_DO_CL.md [--stolpci id,zahteva,nosilec,merilo,test] [--dovoli-odprto] [--testi MAPA]

Izhodna koda: 0 = CL je v redu, 1 = CL ima napake (seznam na izhodu), 2 = napačna uporaba / datoteke ni.

Kaj preveri (format je določen v references/predloga-checklista.md):
  * Tabela je tabela zahtev, če ima stolpec ID (ali »Oznaka«) in stolpec z zahtevo
    (»Zahteva«, »Pričakovano vedenje«, »Pravilo«, »Kaj«). Druge tabele se preskočijo.
  * ID: izpolnjen, oblika PREDPONA-SKLOP-ŠT (npr. P-ZA-01), brez podvojitev v celotni datoteki.
  * Nosilec: natanko en glavni nosilec: Koda | LLM | Glasovni sloj | Vsebina
    (podpora je lahko v oklepaju: »Koda (podpora: LLM)«).
  * Merilo: izpolnjeno (ne prazno, ne »?«, ne »TODO«, ne »<…>«).
  * Test: test ali scenarij je naveden (ne prazno, ne »?«, ne »TODO«, ne »<…>«).
  * Status »ODPRTO« je napaka (CL ni zaprt), razen z --dovoli-odprto (osnutek).
    Status »ne velja« + razlog izvzame vrstico iz preverjanja nosilca, merila in testa.
  * --testi MAPA (faza 04): vsak ID mora nastopati v kakšni .py/.yaml/.json/.js/.sh datoteki
    v MAPI (v testih piši komentar `# CL: ID`). Brez te možnosti se testi ne iščejo.
  * --stolpci omeji preverjanje na naštete stolpce (npr. za stare CL brez nosilca: id,zahteva).

Samo standardna knjižnica.
"""
import argparse
import os
import re
import sys
import unicodedata

ID_OBLIKA = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+$")
ID_ZETON = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+")
NOSILCI = {"koda": "Koda", "llm": "LLM", "glasovni sloj": "Glasovni sloj", "vsebina": "Vsebina"}
PRAZNO = {"", "-", "--", "—", "–", "?", "??", "tbd", "todo", "n/a", "...", "…", "nic", "ni", "/"}
VSI_STOLPCI = ("id", "zahteva", "nosilec", "merilo", "test")
KONCNICE_TESTOV = (".py", ".yaml", ".yml", ".json", ".js", ".sh", ".ts")
PRESKOCI_MAPE = {".git", ".venv", "venv", "__pycache__", "node_modules"}


def norm(s):
    """Male črke, brez šumnikov, brez oblikovanja (*, `), skrajšani presledki."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[*`_]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def celice(vrstica):
    v = vrstica.strip()
    if v.startswith("|"):
        v = v[1:]
    if v.endswith("|") and not v.endswith("\\|"):
        v = v[:-1]
    return [c.replace("\\|", "|").strip() for c in re.split(r"(?<!\\)\|", v)]


def je_loceval(vrstica):
    c = celice(vrstica)
    return bool(c) and all(re.fullmatch(r":?-{2,}:?", x.strip()) for x in c if x.strip() != "") and any(x.strip() for x in c)


def bloki_tabel(vrstice):
    """Vrne [(številka_vrstice_glave (1-based), [vrstice tabele])]."""
    out, tek, start = [], [], 0
    for i, v in enumerate(vrstice, 1):
        if v.lstrip().startswith("|"):
            if not tek:
                start = i
            tek.append(v)
        else:
            if tek:
                out.append((start, tek))
                tek = []
    if tek:
        out.append((start, tek))
    return out


def stolpci_glave(glava):
    """Preslika vloge stolpcev (id, zahteva, nosilec, merilo, test, status) na indekse."""
    idx = {}
    for i, c in enumerate(glava):
        n = norm(c)
        if "id" not in idx and (n in ("id", "oznaka") or n.startswith(("id ", "oznaka "))):
            idx["id"] = i
        elif "nosilec" not in idx and n.startswith("nosilec"):
            idx["nosilec"] = i
        elif "merilo" not in idx and n.startswith("merilo"):
            idx["merilo"] = i
        elif "test" not in idx and (n.startswith("test") or n.startswith("scenarij")):
            idx["test"] = i
        elif "status" not in idx and n.startswith("status"):
            idx["status"] = i
        elif "zahteva" not in idx and any(k in n for k in ("zahteva", "vedenje", "pravilo")) or (
                "zahteva" not in idx and n == "kaj"):
            idx["zahteva"] = i
    return idx


def prazno(vrednost):
    n = norm(vrednost)
    if n in PRAZNO:
        return True
    if re.search(r"<[^>]*>", vrednost):          # neizpolnjen označevalec iz predloge
        return True
    return n.startswith(("todo", "tbd", "se ne vemo"))


def nosilec_ok(vrednost):
    """Vrne (ok, razlog). Podpora v oklepaju je dovoljena, glavni nosilec je en sam."""
    glavni = re.sub(r"\([^)]*\)", "", vrednost)
    n = norm(glavni)
    if n in NOSILCI:
        return True, ""
    if re.search(r"[+/,;]| in | ali ", n):
        return False, "več glavnih nosilcev (»%s«); navedi enega, podporo daj v oklepaj" % vrednost.strip()
    return False, "neznan nosilec »%s« (dovoljeno: Koda, LLM, Glasovni sloj, Vsebina)" % vrednost.strip()


def preberi_cl(pot, stolpci, dovoli_odprto):
    """Vrne (zahteve, napake, povzetek). zahteve = [(id, vrstica)] za vrstice, ki jih preverjamo."""
    with open(pot, encoding="utf-8") as f:
        vrstice = f.read().split("\n")
    napake, ids, preskoceno, tabel = [], {}, 0, 0
    zahteve, n_vrstic, n_slabih, n_pom = [], 0, set(), 0

    for zacetek, blok in bloki_tabel(vrstice):
        if not (len(blok) >= 2 and je_loceval(blok[1])):
            # blok brez glave in ločevalca: prazna vrstica je prekinila tabelo; zahteve v njem bi ostale nepreverjene
            for k, v in enumerate(blok):
                oid = re.sub(r"[*`]", "", celice(v)[0]).strip()
                if ID_OBLIKA.match(oid) and not je_loceval(v):
                    napake.append("vrstica %d [%s]: vrstica tabele brez glave (prazna vrstica prekine tabelo; zahteva ni preverjena)"
                                  % (zacetek + k, oid))
                    n_slabih.add((oid, zacetek + k))
            continue
        glava = celice(blok[0])
        idx = stolpci_glave(glava)
        if "id" not in idx or "zahteva" not in idx:
            preskoceno += 1
            continue
        tabel += 1
        telo = blok[1:]
        if telo and je_loceval(telo[0]):
            telo = telo[1:]
        potrebni = [s for s in stolpci if s not in ("id", "zahteva")]
        manjkajoci = [s for s in potrebni if s not in idx]
        if manjkajoci:
            napake.append("tabela pri vrstici %d (%d zahtev): manjka stolpec %s"
                          % (zacetek, len(telo), ", ".join("»%s«" % s.capitalize() for s in manjkajoci)))
        n_pred = n_vrstic
        for k, v in enumerate(telo):
            st = zacetek + 2 + k                      # številka vrstice v datoteki (glava + ločevalec = +2)
            c = celice(v)
            c += [""] * (len(glava) - len(c))
            if not any(x.strip() for x in c):
                continue
            oid = re.sub(r"[*`]", "", c[idx["id"]]).strip()
            n_vrstic += 1
            if not oid:
                napake.append("vrstica %d: zahteva brez identifikatorja" % st)
                n_slabih.add(("brez-id", st))
                continue
            if not ID_OBLIKA.match(oid):
                napake.append("vrstica %d [%s]: ID ni v obliki PREDPONA-SKLOP-ŠT" % (st, oid))
                n_slabih.add((oid, st))
            ids.setdefault(oid, []).append(st)
            status = norm(c[idx["status"]]) if "status" in idx else ""
            slabo = []
            if "zahteva" in stolpci and prazno(c[idx["zahteva"]]):
                slabo.append("zahteva je prazna")
            if "odprto" in status and not dovoli_odprto:
                slabo.append("status ODPRTO (CL ni zaprt; za osnutek uporabi --dovoli-odprto)")
                preskoci = True
            elif "odprto" in status:
                preskoci = True
            elif status.startswith("ne velja"):
                razlog = re.sub(r"^ne velja[\s:\-–—,()]*", "", status)
                if len(razlog) < 5:
                    slabo.append("»ne velja« brez razloga")
                preskoci = True
            else:
                preskoci = False
            if not preskoci:
                if "nosilec" in stolpci and "nosilec" in idx:
                    ok, razlog = nosilec_ok(c[idx["nosilec"]]) if not prazno(c[idx["nosilec"]]) else (False, "manjka nosilec")
                    if not ok:
                        slabo.append(razlog)
                if "merilo" in stolpci and "merilo" in idx:
                    m = c[idx["merilo"]]
                    if prazno(m) or len(norm(m)) < 10:
                        slabo.append("manjka merilo uspeha")
                if "test" in stolpci and "test" in idx:
                    t = c[idx["test"]]
                    if prazno(t) or len(norm(t)) < 3:
                        slabo.append("manjka test ali scenarij")
                zahteve.append((oid, st))
            for s in slabo:
                napake.append("vrstica %d [%s]: %s" % (st, oid, s))
            if slabo:
                n_slabih.add((oid, st))
            # ODPRTO vrstica pri --dovoli-odprto ni preverjena, a ni napaka
        if manjkajoci:
            n_pom += n_vrstic - n_pred

    podvojeni = {i: l for i, l in ids.items() if len(l) > 1}
    for i, l in sorted(podvojeni.items()):
        napake.append("podvojen ID [%s] v vrsticah %s" % (i, ", ".join(map(str, l))))
    povzetek = dict(tabel=tabel, preskoceno=preskoceno, vrstic=n_vrstic, slabih=len(n_slabih),
                    podvojenih=len(podvojeni), ids=len(ids), v_pomanjkljivih=n_pom)
    return zahteve, napake, povzetek


def poisci_id_v_testih(mapa):
    najdeni = set()
    for koren, mape, datoteke in os.walk(mapa):
        mape[:] = [m for m in mape if m not in PRESKOCI_MAPE]
        for d in datoteke:
            if d.endswith(KONCNICE_TESTOV):
                try:
                    with open(os.path.join(koren, d), encoding="utf-8", errors="ignore") as f:
                        najdeni.update(ID_ZETON.findall(f.read()))
                except OSError:
                    pass
    return najdeni


def main():
    ap = argparse.ArgumentParser(description="Preveri strukturo poslovnega checklista (glej glavo datoteke).")
    ap.add_argument("cl", help="pot do checklista (.md)")
    ap.add_argument("--stolpci", default=",".join(VSI_STOLPCI),
                    help="katere stolpce preveri (privzeto vse: %s)" % ",".join(VSI_STOLPCI))
    ap.add_argument("--dovoli-odprto", action="store_true", help="status ODPRTO ni napaka (osnutek CL)")
    ap.add_argument("--testi", metavar="MAPA", help="faza 04: vsak ID mora nastopati v datotekah v MAPI")
    a = ap.parse_args()

    if not os.path.isfile(a.cl):
        print("NAPAKA: datoteke ni: %s" % a.cl, file=sys.stderr)
        return 2
    stolpci = tuple(s.strip() for s in a.stolpci.split(",") if s.strip())
    neznani = [s for s in stolpci if s not in VSI_STOLPCI]
    if neznani or "id" not in stolpci:
        print("NAPAKA: --stolpci mora vsebovati id in samo %s" % ",".join(VSI_STOLPCI), file=sys.stderr)
        return 2
    if "zahteva" not in stolpci:
        stolpci = ("zahteva",) + stolpci

    zahteve, napake, p = preberi_cl(a.cl, stolpci, a.dovoli_odprto)

    if a.testi:
        if not os.path.isdir(a.testi):
            print("NAPAKA: mapa ni: %s" % a.testi, file=sys.stderr)
            return 2
        najdeni = poisci_id_v_testih(a.testi)
        brez = [(i, l) for i, l in zahteve if i not in najdeni]
        for i, l in brez:
            napake.append("vrstica %d [%s]: ID ni omenjen v nobeni datoteki v %s" % (l, i, a.testi))
        p["brez_testa"] = len(brez)

    print("CL: %s" % a.cl)
    print("Tabele zahtev: %d, zahtev (vrstic): %d, različnih ID: %d, preskočenih tabel brez ID/zahteve: %d"
          % (p["tabel"], p["vrstic"], p["ids"], p["preskoceno"]))
    if p["tabel"] == 0:
        napake.append("v datoteki ni nobene tabele zahtev (potrebna sta stolpca ID in Zahteva/Pričakovano vedenje)")
    if napake:
        print("NAPAKE (%d):" % len(napake))
        for n in napake:
            print("  - " + n)
    print("POVZETEK: zahtev %d (od tega %d v tabelah z manjkajočimi stolpci), vrstic z napako %d, podvojenih ID %d%s"
          % (p["vrstic"], p["v_pomanjkljivih"], p["slabih"], p["podvojenih"],
             (", brez omembe v testih %d" % p["brez_testa"]) if "brez_testa" in p else ""))
    print("IZID: %s" % ("PADE" if napake else "V REDU"))
    return 1 if napake else 0


if __name__ == "__main__":
    sys.exit(main())
