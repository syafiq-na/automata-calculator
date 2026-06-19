import unittest

from common import DEAD_STATE, EPSILON
from dfa import DFA
from equivalence import check_equivalence
from nfa import NFA
from thompson import build_nfa_from_postfix, regex_to_postfix, tokenize_regex


def compile_regex(regex):
    return build_nfa_from_postfix(regex_to_postfix(tokenize_regex(regex)))


class TransitionContractTests(unittest.TestCase):
    def test_tuple_keys_allow_old_delimiter_inside_state_names(self):
        dfa = DFA(
            ["q|||0", "q1"],
            ["a"],
            "q|||0",
            ["q1"],
            {("q|||0", "a"): "q1", ("q1", "a"): "q1"},
        )
        self.assertTrue(dfa.test_string("a")[0])

    def test_json_transition_records_are_normalized_to_tuple_keys(self):
        dfa = DFA(
            ["q0"],
            ["a"],
            "q0",
            ["q0"],
            [{"state": "q0", "symbol": "a", "target": "q0"}],
        )
        self.assertEqual(dfa.transitions, {("q0", "a"): "q0"})

    def test_reserved_dead_state_cannot_be_supplied_by_user(self):
        with self.assertRaises(ValueError):
            DFA([DEAD_STATE], ["a"], DEAD_STATE, [], [])


class InputConsistencyTests(unittest.TestCase):
    def test_dfa_and_nfa_use_same_whitespace_tokenization(self):
        transitions = [
            {"state": "q0", "symbol": "ab", "target": "q1"},
            {"state": "q1", "symbol": "cd", "target": "q2"},
        ]
        dfa = DFA(["q0", "q1", "q2"], ["ab", "cd"], "q0", ["q2"], transitions)
        nfa = NFA(["q0", "q1", "q2"], ["ab", "cd"], "q0", ["q2"], transitions)
        self.assertTrue(dfa.test_string("  ab   cd  ")[0])
        self.assertTrue(nfa.test_string("  ab   cd  ")[0])


class ThompsonTests(unittest.TestCase):
    def test_slash_is_literal_not_union(self):
        result = compile_regex("a/b")
        self.assertEqual(result["alpha"], ["/", "a", "b"])
        nfa = NFA(
            result["states"], result["alpha"], result["start"],
            result["finals"], result["trans"],
        )
        self.assertTrue(nfa.test_string("a/b")[0])
        self.assertFalse(nfa.test_string("a")[0])

    def test_optional_operator_accepts_zero_or_one_occurrence(self):
        result = compile_regex("a?")
        nfa = NFA(
            result["states"], result["alpha"], result["start"],
            result["finals"], result["trans"],
        )
        self.assertTrue(nfa.test_string("")[0])
        self.assertTrue(nfa.test_string("a")[0])
        self.assertFalse(nfa.test_string("aa")[0])

    def test_epsilon_is_standardized_to_E(self):
        result = compile_regex("E")
        self.assertEqual(result["alpha"], [])
        self.assertTrue(any(symbol == EPSILON for _, symbol in result["trans"]))

    def test_invalid_parentheses_are_rejected(self):
        with self.assertRaises(ValueError):
            regex_to_postfix(tokenize_regex("(ab"))


class MinimizerTests(unittest.TestCase):
    def test_partial_dfa_adds_reachable_dead_state(self):
        dfa = DFA(
            ["q0", "q1", "unreachable"],
            ["a", "b"],
            "q0",
            ["q1"],
            {("q0", "a"): "q1", ("q1", "a"): "q1"},
        )
        minimized = dfa.minimize()
        self.assertTrue(minimized["added_dead_state"])
        self.assertTrue(any(
            DEAD_STATE in mapping["group"] for mapping in minimized["mapping"]
        ))
        for state in minimized["states"]:
            for symbol in minimized["alpha"]:
                self.assertIn((state, symbol), minimized["trans"])


class EquivalenceTests(unittest.TestCase):
    def test_missing_transitions_use_internal_dead_state(self):
        left = DFA(["a"], ["0"], "a", [], {})
        right = DFA(["b"], ["0"], "b", [], {})
        self.assertEqual(check_equivalence(left, right), (True, None))

    def test_shortest_counterexample_is_preserved(self):
        left = DFA(
            ["l0", "l1"], ["a", "b"], "l0", ["l1"],
            {("l0", "a"): "l1", ("l0", "b"): "l0",
             ("l1", "a"): "l1", ("l1", "b"): "l1"},
        )
        right = DFA(
            ["r0"], ["a", "b"], "r0", [],
            {("r0", "a"): "r0", ("r0", "b"): "r0"},
        )
        self.assertEqual(check_equivalence(left, right), (False, "a"))

    def test_state_names_with_commas_do_not_create_ghost_pairs(self):
        left = DFA(["x,y"], ["a"], "x,y", ["x,y"], {("x,y", "a"): "x,y"})
        right = DFA(["z"], ["a"], "z", ["z"], {("z", "a"): "z"})
        self.assertEqual(check_equivalence(left, right), (True, None))


if __name__ == "__main__":
    unittest.main()
