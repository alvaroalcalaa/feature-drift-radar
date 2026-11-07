import unittest
from radar import analyse, js_distance, proportions

class RadarTests(unittest.TestCase):
    def test_categorical_shift_is_detected(self):
        reference = [{"plan": "free"}] * 90 + [{"plan": "pro"}] * 10
        current = [{"plan": "free"}] * 40 + [{"plan": "pro"}] * 60
        item = analyse(reference, current)[0]
        self.assertEqual(item["type"], "categorical")
        self.assertEqual(item["status"], "drift")

    def test_identical_distribution_is_stable(self):
        rows = [{"region": "ES"}, {"region": "FR"}, {"region": "ES"}]
        item = analyse(rows, rows)[0]
        self.assertEqual(item["status"], "stable")

if __name__ == "__main__":
    unittest.main()
