"""Tests for statistics helpers, dataset handling, model chooser and quiz answer checking."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import model_systems as ms  # noqa: E402
from modules import quiz  # noqa: E402
from modules import stats_utils as st_  # noqa: E402
from modules import virtual_lab as lab  # noqa: E402


class TestStats(unittest.TestCase):
    def test_mean_and_sd(self):
        self.assertEqual(st_.mean([1, 2, 3]), 2)
        self.assertAlmostEqual(st_.sample_sd([2, 4, 4, 4, 5, 5, 7, 9]), 2.13809, places=4)

    def test_empty_and_too_small_inputs(self):
        with self.assertRaises(ValueError):
            st_.mean([])
        with self.assertRaises(ValueError):
            st_.sample_sd([1])
        with self.assertRaises(ValueError):
            st_.permutation_test_independent([1], [1, 2])
        with self.assertRaises(ValueError):
            st_.paired_sign_flip_test([1, 2], [1])

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            st_.mean([1.0, float("nan")])

    def test_identical_groups_not_significant(self):
        result = st_.permutation_test_independent([1, 2, 3, 4], [1, 2, 3, 4], seed=1)
        self.assertGreater(result["p_value"], 0.9)

    def test_clearly_different_groups_small_p(self):
        result = st_.permutation_test_independent([1, 2, 3, 4, 5, 6], [21, 22, 23, 24, 25, 26], seed=1)
        self.assertLess(result["p_value"], 0.01)
        self.assertLess(result["observed_difference"], 0)

    def test_p_value_never_zero_and_reproducible(self):
        a = st_.permutation_test_independent([1, 2, 3], [100, 101, 102], seed=3)
        b = st_.permutation_test_independent([1, 2, 3], [100, 101, 102], seed=3)
        self.assertGreater(a["p_value"], 0)
        self.assertEqual(a["p_value"], b["p_value"])

    def test_paired_test(self):
        result = st_.paired_sign_flip_test([1, 2, 3, 4, 5, 6, 7, 8], [11, 12, 13, 14, 15, 16, 17, 18], seed=1)
        self.assertAlmostEqual(result["observed_difference"], 10)
        self.assertLess(result["p_value"], 0.05)
        self.assertEqual(result["n_pairs"], 8)

    def test_cohens_d(self):
        self.assertEqual(st_.cohens_d([1, 2, 3], [1, 2, 3]), 0.0)
        self.assertLess(st_.cohens_d([1, 2, 3], [11, 12, 13]), -5)


class TestDatasets(unittest.TestCase):
    def setUp(self):
        self.df = lab.load_datasets()

    def test_expected_scenarios_present(self):
        self.assertTrue(set(lab.SCENARIOS) <= set(self.df["scenario"]))
        self.assertIn("zebrafish_case", set(self.df["scenario"]))

    def test_values_numeric_and_positive(self):
        self.assertTrue((self.df["value"] > 0).all())

    def test_group_sizes(self):
        sub = lab.get_scenario_data(self.df, "tissue_size")
        self.assertEqual(len(lab.group_values(sub, "Control")), 12)

    def test_unknown_scenario(self):
        with self.assertRaises(ValueError):
            lab.get_scenario_data(self.df, "nope")

    def test_paired_values_align(self):
        sub = lab.get_scenario_data(self.df, "paired_feature")
        early, late = lab.paired_values(sub, "24 h", "48 h")
        self.assertEqual(len(early), 10)
        self.assertEqual(len(early), len(late))

    def test_analyse_each_scenario(self):
        for key, scenario in lab.SCENARIOS.items():
            result = lab.analyse_scenario(lab.get_scenario_data(self.df, key), scenario["design"])
            self.assertTrue(0 < result["p_value"] <= 1)
            self.assertTrue(lab.interpret_result(result, scenario["design"]))

    def test_analyse_rejects_bad_design(self):
        with self.assertRaises(ValueError):
            lab.analyse_scenario(lab.get_scenario_data(self.df, "tissue_size"), "weird")

    def test_summary_rows(self):
        rows = lab.summarise(lab.get_scenario_data(self.df, "cell_growth"))
        self.assertEqual({r["Group"] for r in rows}, {"Condition A", "Condition B"})
        self.assertTrue(all(r["n"] == 8 for r in rows))

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            lab.load_datasets("/no/such/file.csv")

    def test_bad_columns_and_values(self):
        with tempfile.TemporaryDirectory() as folder:
            bad_cols = os.path.join(folder, "a.csv")
            with open(bad_cols, "w") as f:
                f.write("scenario,group,value\nx,y,1\n")
            with self.assertRaises(ValueError):
                lab.load_datasets(bad_cols)
            bad_vals = os.path.join(folder, "b.csv")
            with open(bad_vals, "w") as f:
                f.write("scenario,group,subject_id,value\nx,y,s1,abc\n")
            with self.assertRaises(ValueError):
                lab.load_datasets(bad_vals)


class TestModelChooser(unittest.TestCase):
    def test_all_questions_and_priorities_work(self):
        for q in ms.CHOOSER_QUESTIONS:
            for p in ms.PRIORITY_SCORES:
                ranked = ms.rank_models(q, p)
                self.assertTrue(ranked)
                self.assertTrue(all(r["fit"] > 0 for r in ranked))

    def test_expected_top_choices(self):
        self.assertEqual(ms.rank_models("Studying basic cell-cycle mechanisms", "Speed and low cost")[0]["model"], "Yeast")
        self.assertEqual(ms.rank_models("Investigating mammalian physiology", "Closeness to human biology")[0]["model"], "Mouse")
        self.assertEqual(ms.rank_models("Observing vertebrate embryo development", "Live imaging")[0]["model"], "Zebrafish")

    def test_priority_can_change_order(self):
        q = "Investigating a developmental gene"
        self.assertEqual(ms.rank_models(q, "Whole-organism context")[0]["model"], "Zebrafish")
        self.assertEqual(ms.rank_models(q, "Speed and low cost")[0]["model"], "Fruit fly")

    def test_unknown_inputs(self):
        with self.assertRaises(ValueError):
            ms.rank_models("???", "Live imaging")
        with self.assertRaises(ValueError):
            ms.rank_models("Investigating a developmental gene", "???")

    def test_model_data_consistent(self):
        self.assertEqual(set(ms.MODELS), set(ms.MODEL_ORDER))
        self.assertEqual(set(ms.COMPARISON), set(ms.MODEL_ORDER))
        for field in ("what", "questions", "advantages", "limitations", "measure", "human_relevance", "ethics"):
            for name, info in ms.MODELS.items():
                self.assertTrue(info[field], f"{name}.{field}")

    def test_comparison_table(self):
        self.assertEqual(ms.comparison_table(["Zebrafish", "Mouse"]).shape[1], 2)
        with self.assertRaises(ValueError):
            ms.comparison_table([])
        with self.assertRaises(ValueError):
            ms.comparison_table(["Dragon"])


class TestQuiz(unittest.TestCase):
    def test_at_least_15_questions_and_valid(self):
        self.assertGreaterEqual(len(quiz.QUESTIONS), 15)
        self.assertEqual(quiz.validate_questions(quiz.QUESTIONS), [])

    def test_correct_answers_not_all_in_same_position(self):
        positions = {q["answer"] for q in quiz.QUESTIONS}
        self.assertGreaterEqual(len(positions), 3)

    def test_check_answer(self):
        q = quiz.QUESTIONS[0]
        self.assertTrue(quiz.check_answer(q, q["answer"]))
        self.assertFalse(quiz.check_answer(q, (q["answer"] + 1) % len(q["options"])))
        self.assertFalse(quiz.check_answer(q, None))

    def test_score_perfect_zero_and_partial(self):
        perfect = [q["answer"] for q in quiz.QUESTIONS]
        self.assertEqual(quiz.score_quiz(quiz.QUESTIONS, perfect), (len(quiz.QUESTIONS), len(quiz.QUESTIONS)))
        self.assertEqual(quiz.score_quiz(quiz.QUESTIONS, [None] * len(quiz.QUESTIONS))[0], 0)
        partial = perfect[:]
        partial[0] = None
        self.assertEqual(quiz.score_quiz(quiz.QUESTIONS, partial)[0], len(quiz.QUESTIONS) - 1)

    def test_score_wrong_length(self):
        with self.assertRaises(ValueError):
            quiz.score_quiz(quiz.QUESTIONS, [0])

    def test_validator_catches_problems(self):
        bad = [{"topic": "x", "question": "q", "options": ["a", "a"], "answer": 5, "explanation": "e"}]
        problems = quiz.validate_questions(bad)
        self.assertTrue(any("duplicate" in p for p in problems))
        self.assertTrue(any("out of range" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
