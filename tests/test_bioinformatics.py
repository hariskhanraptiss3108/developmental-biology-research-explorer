"""Tests for sequence parsing, comparison and ORF finding."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import bioinformatics as b  # noqa: E402


class TestParsing(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(b.parse_sequences(""), [])
        self.assertEqual(b.parse_sequences(None), [])
        self.assertEqual(b.parse_sequences("  \n \n"), [])

    def test_one_per_line(self):
        self.assertEqual(b.parse_sequences("atg\n\nccc"), [("Seq1", "ATG"), ("Seq2", "CCC")])

    def test_fasta_multiline(self):
        self.assertEqual(b.parse_sequences(">a\nATG\nCC\n>b\nGG"), [("a", "ATGCC"), ("b", "GG")])

    def test_summary_flags_invalid(self):
        rows = b.summarise_records([("ok", "ATGC"), ("bad", "ATGX"), ("empty", "")])
        self.assertTrue(rows[0]["Valid"])
        self.assertEqual(rows[0]["GC %"], 50.0)
        self.assertFalse(rows[1]["Valid"])
        self.assertIn("X", rows[1]["Problem"])
        self.assertFalse(rows[2]["Valid"])


class TestComparison(unittest.TestCase):
    def test_percent_identity(self):
        self.assertEqual(b.percent_identity("ATGC", "ATGC"), 100.0)
        self.assertEqual(b.percent_identity("ATGC", "ATGG"), 75.0)
        self.assertEqual(b.percent_identity("AAAA", "TTTT"), 0.0)

    def test_percent_identity_errors(self):
        with self.assertRaises(ValueError):
            b.percent_identity("ATG", "ATGC")
        with self.assertRaises(ValueError):
            b.percent_identity("", "ATG")
        with self.assertRaises(ValueError):
            b.percent_identity("ATG", "AXG")

    def test_best_ungapped_match(self):
        best = b.best_ungapped_match("ATGGCTAAA", "GCT")
        self.assertEqual(best["offset"], 3)
        self.assertEqual(best["identity_percent"], 100.0)

    def test_best_match_works_if_arguments_swapped(self):
        best = b.best_ungapped_match("GCT", "ATGGCTAAA")
        self.assertEqual(best["longer_is"], "B")
        self.assertEqual(best["offset"], 3)

    def test_kmers(self):
        self.assertEqual(b.kmer_set("ATGA", 2), {"AT", "TG", "GA"})
        self.assertEqual(b.kmer_set("AT", 3), set())
        with self.assertRaises(ValueError):
            b.kmer_set("ATG", 0)

    def test_kmer_similarity(self):
        self.assertEqual(b.kmer_similarity("ATGC", "ATGC", 2), 1.0)
        self.assertEqual(b.kmer_similarity("AAAA", "CCCC", 2), 0.0)
        self.assertEqual(b.kmer_similarity("A", "C", 3), 0.0)  # no k-mers at all


class TestOrfs(unittest.TestCase):
    def test_finds_simple_orf(self):
        orfs = b.find_orfs("CCATGGCTAAATAAGG", min_codons=2)
        self.assertEqual(len(orfs), 1)
        self.assertEqual(orfs[0]["protein"], "MAK")
        self.assertEqual((orfs[0]["start"], orfs[0]["end"]), (3, 14))

    def test_min_length_filter(self):
        self.assertEqual(b.find_orfs("ATGAAATAA", min_codons=5), [])

    def test_no_stop_codon_means_no_orf(self):
        self.assertEqual(b.find_orfs("ATGAAAGGG", min_codons=1), [])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            b.find_orfs("")
        with self.assertRaises(ValueError):
            b.find_orfs("ATGZ")


if __name__ == "__main__":
    unittest.main()
