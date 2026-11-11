import unittest
from scoring import score_lead, score_band

class ScoringTests(unittest.TestCase):
    def test_maximum_score_is_capped_at_100(self):
        lead = {
            "budget_confirmed": True, "decision_maker": True,
            "source": "Demo Request", "timeline_days": 7,
            "employees": 100, "email": "person@example.com"
        }
        self.assertEqual(score_lead(lead), 100)

    def test_cold_lead(self):
        lead = {
            "budget_confirmed": False, "decision_maker": False,
            "source": "Cold Outreach", "timeline_days": 180,
            "employees": 2, "email": ""
        }
        self.assertEqual(score_lead(lead), 0)
        self.assertEqual(score_band(0), "Cold")

    def test_score_reasons_are_returned(self):
        lead = {"budget_confirmed": True, "email": "a@b.com"}
        score, reasons = score_lead(lead, include_reasons=True)
        self.assertEqual(score, 30)
        self.assertEqual(len(reasons), 2)

if __name__ == "__main__":
    unittest.main()
