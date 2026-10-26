"""Tests for DNA validation, statistics, strands, translation and mutation classification."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import genetics as g  # noqa: E402


class TestValidation(unittest.TestCase):
    def test_valid_sequence_is_cleaned(self):
        ok, cleaned, msg = g.validate_dna(" atg c\nGT ")
        self.assertTrue(ok)
        self.assertEqual(cleaned, "ATGCGT")
        self.assertEqual(msg, "")

    def test_empty_and_none_are_invalid(self):
        for value in ("", "   \n", None):
            ok, _, msg = g.validate_dna(value)
            self.assertFalse(ok)
            self.assertIn("empty", msg)

    def test_invalid_characters_reported(self):
        ok, _, msg = g.validate_dna("ATGXZ1")
        self.assertFalse(ok)
        for bad in ("X", "Z", "1"):
            self.assertIn(bad, msg)

    def test_rna_u_gets_helpful_hint(self):
        ok, _, msg = g.validate_dna("AUGC")
        self.assertFalse(ok)
        self.assertIn("RNA", msg)


class TestCountsAndGC(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(g.count_nucleotides("AATGC"), {"A": 2, "T": 1, "C": 1, "G": 1})

    def test_counts_include_zero_bases(self):
        self.assertEqual(g.count_nucleotides("AAAA"), {"A": 4, "T": 0, "C": 0, "G": 0})

    def test_percentages_sum_to_100(self):
        self.assertAlmostEqual(sum(g.nucleotide_percentages("ATGCCGA").values()), 100.0)

    def test_gc_content_values(self):
        self.assertAlmostEqual(g.gc_content("GGCC"), 100.0)
        self.assertAlmostEqual(g.gc_content("ATAT"), 0.0)
        self.assertAlmostEqual(g.gc_content("ATGC"), 50.0)
        self.assertAlmostEqual(g.gc_content("atgc"), 50.0)

    def test_empty_and_invalid_raise(self):
        for func in (g.count_nucleotides, g.nucleotide_percentages, g.gc_content, g.complement, g.reverse_complement):
            with self.assertRaises(ValueError):
                func("")
            with self.assertRaises(ValueError):
                func("ATGX")


class TestStrands(unittest.TestCase):
    def test_complement(self):
        self.assertEqual(g.complement("ATGC"), "TACG")

    def test_reverse_complement(self):
        self.assertEqual(g.reverse_complement("ATGC"), "GCAT")
        self.assertEqual(g.reverse_complement("AAACCC"), "GGGTTT")

    def test_reverse_complement_twice_is_identity(self):
        seq = "ATGGCTAAAGAATTC"
        self.assertEqual(g.reverse_complement(g.reverse_complement(seq)), seq)

    def test_transcription_replaces_t_with_u(self):
        self.assertEqual(g.transcribe_coding_strand("ATGTTT"), "AUGUUU")

    def test_template_strand_is_complement_aligned(self):
        self.assertEqual(g.template_strand("ATGC"), "TACG")


class TestGeneticCode(unittest.TestCase):
    def test_table_complete(self):
        self.assertEqual(len(g.CODON_TABLE), 64)
        self.assertEqual(set(g.CODON_TABLE.values()) - {"*"}, set("ACDEFGHIKLMNPQRSTVWY"))

    def test_known_codons(self):
        expected = {"ATG": "M", "TGG": "W", "TAA": "*", "TAG": "*", "TGA": "*", "TTT": "F", "GAA": "E", "GAG": "E",
                    "GGG": "G", "CCC": "P", "AAA": "K", "CAT": "H", "AGA": "R", "TCA": "S", "AGC": "S", "ATA": "I"}
        for codon, amino_acid in expected.items():
            self.assertEqual(g.CODON_TABLE[codon], amino_acid, codon)

    def test_degeneracy_counts(self):
        counts = {}
        for aa in g.CODON_TABLE.values():
            counts[aa] = counts.get(aa, 0) + 1
        self.assertEqual(counts["*"], 3)
        self.assertEqual(counts["M"], 1)
        self.assertEqual(counts["W"], 1)
        self.assertEqual(counts["L"], 6)
        self.assertEqual(counts["S"], 6)
        self.assertEqual(counts["R"], 6)

    def test_translate_stops_at_stop(self):
        self.assertEqual(g.translate_coding("ATGGCTTAAGGG"), ("MA", True, 3))

    def test_translate_without_stop(self):
        protein, stop, leftover = g.translate_coding("ATGGCTAA")
        self.assertEqual((protein, stop, leftover), ("MA", False, 2))

    def test_translate_keeping_stop_symbol(self):
        self.assertEqual(g.translate_coding("ATGTAAGGG", to_stop=False)[0], "M*G")

    def test_find_start_codon(self):
        self.assertEqual(g.find_start_codon("CCATGG"), 2)
        self.assertEqual(g.find_start_codon("CCCC"), -1)

    def test_split_codons_drops_incomplete(self):
        self.assertEqual(g.split_codons("ATGGCTA"), ["ATG", "GCT"])

    def test_examples_are_in_frame_with_stop(self):
        for name, seq in g.EXAMPLE_SEQUENCES.items():
            self.assertTrue(seq.startswith("ATG"), name)
            self.assertEqual(len(seq) % 3, 0, name)
            protein, stop, _ = g.translate_coding(seq)
            self.assertTrue(stop, name)
            self.assertEqual(len(protein) * 3 + 3, len(seq), f"{name}: stop codon should be last")


class TestMutations(unittest.TestCase):
    REF = g.EXAMPLE_SEQUENCES["Fictional sequence 1 (9 codons + stop)"]  # ATG GCT AAA GAA TTC GGT CTG ACC TGG TAA

    def classify(self, kind, position, detail):
        return g.analyse_mutation(self.REF, kind, position, detail)[1]

    def test_synonymous(self):
        self.assertEqual(self.classify("substitution", 9, "G").category, "Synonymous (silent) change")  # AAA -> AAG (Lys)

    def test_missense(self):
        res = self.classify("substitution", 4, "A")  # GCT -> ACT (Ala -> Thr)
        self.assertEqual(res.category, "Missense change")
        self.assertEqual(res.mutated_protein, "MTKEFGLTW")

    def test_nonsense(self):
        res = self.classify("substitution", 10, "T")  # GAA -> TAA
        self.assertIn("Premature stop", res.category)
        self.assertEqual(res.mutated_protein, "MAK")

    def test_stop_lost(self):
        self.assertEqual(self.classify("substitution", 28, "G").category, "Stop codon lost")

    def test_start_codon_altered(self):
        self.assertEqual(self.classify("substitution", 1, "C").category, "Start codon altered")

    def test_frameshift_insertion_and_deletion(self):
        self.assertEqual(self.classify("insertion", 6, "G").category, "Frameshift")
        self.assertEqual(self.classify("deletion", 7, 1).category, "Frameshift")
        self.assertEqual(self.classify("deletion", 7, 2).category, "Frameshift")

    def test_in_frame_indels(self):
        self.assertEqual(self.classify("insertion", 6, "GGG").category, "In-frame insertion")
        res = self.classify("deletion", 7, 3)
        self.assertEqual(res.category, "In-frame deletion")
        self.assertEqual(len(res.mutated_protein), len(res.reference_protein) - 1)

    def test_in_frame_insertion_creating_stop(self):
        res = self.classify("insertion", 6, "TAA")  # ATGGCT TAA AAAGAA...
        self.assertIn("Premature stop", res.category)

    def test_no_change(self):
        self.assertEqual(self.classify("substitution", 5, "C").category, "No change")  # position 5 is already C

    def test_change_after_stop_codon_is_outside(self):
        seq = self.REF + "GGGCCC"
        _, res = g.analyse_mutation(seq, "substitution", 31, "A")
        self.assertEqual(res.category, "Outside the translated region")

    def test_reference_must_start_with_atg(self):
        with self.assertRaises(ValueError):
            g.analyse_mutation("GCTAAATAA", "substitution", 1, "A")

    def test_bad_positions_and_bases(self):
        with self.assertRaises(ValueError):
            g.apply_substitution(self.REF, 0, "A")
        with self.assertRaises(ValueError):
            g.apply_substitution(self.REF, len(self.REF) + 1, "A")
        with self.assertRaises(ValueError):
            g.apply_substitution(self.REF, 3, "U")
        with self.assertRaises(ValueError):
            g.apply_insertion(self.REF, 3, "")
        with self.assertRaises(ValueError):
            g.apply_insertion(self.REF, 0, "A")
        with self.assertRaises(ValueError):
            g.apply_deletion(self.REF, len(self.REF), 2)
        with self.assertRaises(ValueError):
            g.apply_deletion(self.REF, 3, 0)

    def test_apply_functions(self):
        self.assertEqual(g.apply_substitution("ATGC", 2, "A"), "AAGC")
        self.assertEqual(g.apply_insertion("ATGC", 2, "CC"), "ATCCGC")
        self.assertEqual(g.apply_deletion("ATGC", 2, 2), "AC")


class TestSimulatedExpression(unittest.TestCase):
    def test_shape_and_reproducibility(self):
        a = g.simulate_expression(g.FICTIONAL_GENES, replicates=3, seed=5)
        b = g.simulate_expression(g.FICTIONAL_GENES, replicates=3, seed=5)
        self.assertEqual(len(a), 5 * 4 * 3)
        self.assertTrue(a.equals(b))

    def test_non_negative(self):
        df = g.simulate_expression(g.FICTIONAL_GENES, replicates=5, noise=0.4, seed=1)
        self.assertTrue((df["expression"] >= 0).all())

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            g.simulate_expression(g.FICTIONAL_GENES, replicates=0)
        with self.assertRaises(ValueError):
            g.simulate_expression(g.FICTIONAL_GENES, noise=-1)


if __name__ == "__main__":
    unittest.main()
