# tests/test_lending.py

import unittest
from src.lending import Lending  # Assuming you have a Lending class in src/lending.py

class TestLending(unittest.TestCase):
    def setUp(self):
        self.lending = Lending()

    def test_create_loan(self):
        loan_id = self.lending.create_loan(amount=1000, interest_rate=5)
        self.assertIsNotNone(loan_id)

    def test_repay_loan(self):
        loan_id = self.lending.create_loan(amount=1000, interest_rate=5)
        result = self.lending.repay_loan(loan_id, amount=500)
        self.assertTrue(result)

    def test_get_loan_details(self):
        loan_id = self.lending.create_loan(amount=1000, interest_rate=5)
        details = self.lending.get_loan_details(loan_id)
        self.assertEqual(details['amount'], 1000)

if __name__ == '__main__':
    unittest.main()
