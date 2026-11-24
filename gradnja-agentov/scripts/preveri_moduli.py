#!/usr/bin/env python3
"""Preveri, da vsaka pot v references/moduli.md res obstaja.

Poti so v obliki `OZNAKA:pot` (v obratnih narekovajih). Oznake korenov so spodaj.
Izhodna koda: 0 = vse poti obstajajo, 1 = kakšna manjka (izpiše jih).
Poženi po vsaki spremembi moduli.md in pred uporabo zemljevida (agenti se spreminjajo).
"""
import os
import re
import sys

KORENI = {
    "J": "POC glasovni agent/megaphone-voice-poc",
    "JO": "Joze - glasovni agent",
    "FD": "Fine dining - glasovni agent",
    "PR": "Prebil - glasovni agent",
    "VE": "Večer - glasovni agenti/vecer-hetzner-poc",
    "V7": "Večer - glasovni agenti/vecer-hetzner-poc-faza7",
}
OSNOVA = "/home/chebo/MAIOS/09-projects"
MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "moduli.md")


def main():
    besedilo = open(MD, encoding="utf-8").read()
    zetoni = sorted(set(re.findall(r"`(J|JO|FD|PR|VE|V7):([^`]+)`", besedilo)))
    manjka = []
    for oznaka, pot in zetoni:
        polna = os.path.join(OSNOVA, KORENI[oznaka], pot.split(" ")[0])
        if not os.path.exists(polna):
            manjka.append("%s:%s" % (oznaka, pot))
    # nepoznane oznake (npr. tipkarska napaka) bi sicer ostale neopažene
    nepoznane = sorted(set(re.findall(r"`([A-Z0-9]{1,3}):[^`\s]+/[^`]*`", besedilo)) - set(KORENI))
    print("Preverjenih poti: %d, manjka: %d" % (len(zetoni), len(manjka)))
    for m in manjka:
        print("  MANJKA: " + m)
    for n in nepoznane:
        print("  NEPOZNANA OZNAKA KORENA: " + n)
    return 1 if (manjka or nepoznane) else 0


if __name__ == "__main__":
    sys.exit(main())
