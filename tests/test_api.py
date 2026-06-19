import unittest

from app import app


class ApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_regex_to_nfa_to_nfa_evaluation_flow(self):
        response = self.client.post("/api/regex/to-nfa", json={"regex": "a?"})
        self.assertEqual(response.status_code, 200)
        nfa = response.get_json()["nfa"]
        self.assertIsInstance(nfa["trans"], list)
        self.assertTrue(all(
            set(record) == {"state", "symbol", "target"}
            for record in nfa["trans"]
        ))

        nfa["input_str"] = ""
        evaluation = self.client.post("/api/nfa/test", json=nfa)
        self.assertEqual(evaluation.status_code, 200)
        self.assertTrue(evaluation.get_json()["accepted"])

    def test_minimizer_response_uses_transition_records(self):
        response = self.client.post("/api/dfa/minimize", json={
            "states": ["q0", "q1"],
            "alpha": ["a", "b"],
            "start": "q0",
            "finals": ["q1"],
            "trans": [
                {"state": "q0", "symbol": "a", "target": "q1"},
                {"state": "q1", "symbol": "a", "target": "q1"},
            ],
        })
        self.assertEqual(response.status_code, 200)
        result = response.get_json()["minimized"]
        self.assertTrue(result["added_dead_state"])
        self.assertIsInstance(result["trans"], list)


if __name__ == "__main__":
    unittest.main()
