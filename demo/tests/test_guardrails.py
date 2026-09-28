"""Run from demo/: python -m unittest discover tests"""
import unittest

from guardrails import redact, validate_ticket

GOOD = {
    "id": "T-1",
    "title": "Split a bill",
    "user_story": "As a payer, I want to split a bill, so that friends pay me back",
    "acceptance_criteria": ["Given a completed payment when I tap split then I can add participants"],
    "priority": "P0",
    "source_requirement": "Payer can split a bill",
}


class Redaction(unittest.TestCase):
    def test_email_card_sortcode_key(self):
        text = "mail jane@example.com card 4111 1111 1111 1111 sort 12-34-56 key sk_live_abcdefghijklmnop1234"
        out, counts = redact(text)
        for raw in ("jane@example.com", "4111", "12-34-56", "sk_live"):
            self.assertNotIn(raw, out)
        self.assertEqual(set(counts), {"EMAIL", "CARD_NUMBER", "UK_SORT_CODE", "API_KEY"})

    def test_clean_text_untouched(self):
        self.assertEqual(redact("Requests expire after 30 days")[0], "Requests expire after 30 days")


class Validation(unittest.TestCase):
    def test_good_ticket_passes(self):
        self.assertEqual(validate_ticket(GOOD), [])

    def test_bad_story_and_criteria_fail(self):
        bad = {**GOOD, "user_story": "Split bills", "acceptance_criteria": ["works"], "priority": "P7"}
        problems = validate_ticket(bad)
        self.assertEqual(len(problems), 3)

    def test_leak_is_caught(self):
        leaky = {**GOOD, "title": "Ping jane@example.com"}
        self.assertTrue(any("EMAIL" in p for p in validate_ticket(leaky)))


if __name__ == "__main__":
    unittest.main()
