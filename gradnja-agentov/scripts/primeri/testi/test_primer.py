"""Primer testov, ki se sklicujejo na zahteve iz CL (komentar `# CL: ID`)."""
import unittest


class TestObseg(unittest.TestCase):
    def test_vsaka_tezava(self):          # CL: SZ-OB-01
        pass

    def test_ekolo_zavrnjeno(self):       # CL: SZ-OB-02
        pass


class TestPovzetek(unittest.TestCase):
    def test_povzetek_iz_kode(self):      # CL: SZ-PO-01
        pass

    def test_enkratna_oddaja(self):       # CL: SZ-PO-02
        pass

    def test_hm_ni_potrditev(self):       # CL: SZ-PO-03
        pass

    def test_sz_bs_02(self):              # CL: SZ-BS-02
        pass
