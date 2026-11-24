#!/usr/bin/env python3
"""Izpiše pravila za glasovne agente ŽIVO iz Obsidiana (edini vir resnice).

Kaj izpiše:
  privzeto (--projekt splosno, jana, joze, fine-dining, prebil):
      splošni FILTER 1-3, FILTER velja tudi za Codexove najdbe, »Ne izumljaj tople vode« z moduli,
      šest mehanizmov, kakovost, preverjanje
  --projekt vecer: dodatno Večerov vratar 0-6 in mehanizmi M1-M8
  --pregled:       dodatno »Pregled pred gradnjo« (PRAVILA.md)

Izluščanje je PREPISANO iz ~/.claude/hooks/pravila-vrata.py (funkcije _berilo, _razdelek,
_odstavki, _brez, _podrazdelek, filter_in_vecer); hooka ne spreminjamo. Če se struktura
Obsidianovih datotek spremeni in razdelka ni mogoče najti, skripta pade (izhodna koda 2)
z imenom razdelka: takrat preberi Agent-Shared/PRAVILA.md in glasovni-agenti-nacela.md ročno.
Svoje kopije pravil skripta nima.
"""
import argparse
import re
import sys

PRAVILA = "/home/chebo/Documents/Obsidian Vault/Agent-Shared/PRAVILA.md"
NACELA = "/home/chebo/Documents/Obsidian Vault/Agent-Shared/glasovni-agenti-nacela.md"
META = ("*Kaj se zgodi brez tega:*", "*Od ")


# --- od tu naprej prepis iz pravila-vrata.py ---------------------------------------------

def _berilo(pot):
    with open(pot, encoding="utf-8") as f:
        return f.read().split("\n")


def _razdelek(vrstice, zacetek, konec):
    """Vrstice od prve, ki se začne z `zacetek`, do vrstice (izključno), za katero konec(vrstica) velja."""
    for i, v in enumerate(vrstice):
        if v.startswith(zacetek):
            out = [v]
            for w in vrstice[i + 1:]:
                if konec(w):
                    break
                out.append(w)
            return out
    raise LookupError("razdelek »%s« ni najden" % zacetek)


def _odstavki(vrstice):
    odst, tek = [], []
    for v in vrstice:
        if v.strip() == "":
            if tek:
                odst.append("\n".join(tek))
                tek = []
        else:
            tek.append(v)
    if tek:
        odst.append("\n".join(tek))
    return odst


def _brez(odst, predpone):
    return [o for o in odst if not any(o.startswith(p) for p in predpone)]


def _podrazdelek(vrstice, naslov):
    """Podrazdelek `### naslov…` do naslednjega naslova ali ---."""
    return _razdelek(vrstice, naslov, lambda w: w.startswith("#") or w.strip() == "---")


def filter_in_vecer():
    """Vrne (splošno, vecer) kot besedili; dvigne izjemo, če česa ni mogoče najti."""
    pr = _berilo(PRAVILA)
    na = _berilo(NACELA)
    fl = _razdelek(pr, "## FILTER", lambda w: w.strip() == "---")
    pr_vecer = _podrazdelek(fl, "### FILTER — Večer")
    i0 = next(i for i, v in enumerate(fl) if v.startswith("### FILTER — Večer"))
    fl_splosno = fl[:i0] + fl[i0 + len(pr_vecer):]
    topla = _razdelek(pr, "### Ne izumljaj", lambda w: w.startswith("#") and not w.startswith("### Ne izumljaj"))
    topla_odst = _odstavki(topla[1:])
    topla_txt = topla[0] + "\n" + (topla_odst[0] if topla_odst else "")
    deli, citat = [], []
    for n in ("## 1.", "## 2.", "## 3.", "## 4."):
        sek = _razdelek(na, n, lambda w: w.startswith("## "))
        odst = _odstavki(sek)
        citat += [o for o in odst if o.startswith("> **Večer")]
        if n != "## 1.":  # ## 1. ponavlja FILTER iz PRAVILA.md (Chebo 9. 11. 2026)
            deli.append("\n\n".join(o for o in odst if not o.startswith("> **Večer")))
    nv = _razdelek(na, "## Večer", lambda w: w.startswith("## "))
    if not citat:
        raise LookupError("citatni blok »> **Večer« ni najden")
    splosno = "\n\n".join(_brez(_odstavki(fl_splosno), META) + [topla_txt] + deli)
    vecer = "\n\n".join(_brez(_odstavki(pr_vecer), META) + _odstavki(nv) + citat)
    return re.sub(r"\n{3,}", "\n\n", splosno).strip(), re.sub(r"\n{3,}", "\n\n", vecer).strip()

# --- konec prepisa ------------------------------------------------------------------------


def pregled():
    """»Pregled pred gradnjo — glasovni agenti« iz PRAVILA.md (v hooku je to trda kopija, tu je živo)."""
    pr = _berilo(PRAVILA)
    sek = _razdelek(pr, "## Pregled pred gradnjo", lambda w: w.strip() == "---")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(sek)).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--projekt", default="splosno",
                    choices=["splosno", "jana", "joze", "fine-dining", "prebil", "vecer"],
                    help="vecer doda vratar 0-6 in M1-M8; vsi ostali dobijo splošni FILTER in šest mehanizmov")
    ap.add_argument("--pregled", action="store_true", help="dodaj »Pregled pred gradnjo«")
    a = ap.parse_args()
    try:
        splosno, vecer = filter_in_vecer()
        izpis = ["== FILTER, MEHANIZMI, KAKOVOST, PREVERJANJE (živo iz Obsidiana: Agent-Shared/PRAVILA.md + glasovni-agenti-nacela.md) ==\n\n" + splosno]
        if a.projekt == "vecer":
            izpis.append("== VEČER: vratar 0-6 in M1-M8 ==\n\n" + vecer)
        if a.pregled:
            izpis.append("== PREGLED PRED GRADNJO ==\n\n" + pregled())
    except (LookupError, OSError, StopIteration) as e:
        print("NAPAKA: pravil ni mogoče izluščiti (%s). Preberi ročno: %s in %s" % (e, PRAVILA, NACELA), file=sys.stderr)
        return 2
    print("\n\n".join(izpis))
    return 0


if __name__ == "__main__":
    sys.exit(main())
