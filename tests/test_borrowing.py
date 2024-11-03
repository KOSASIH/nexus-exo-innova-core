# tests/test_borrowing.py

import unittest
from src.borrowing import Borrowing  # Assuming you have a Borrowing class in src/borrowing.py

class TestBorrowing(unittest.TestCase):
    def setUp(self):
        self.borrowing = Borrowing()

    def test_borrow_funds(self):
        transaction_id = self.borrowing.borrow_funds(amount=500)
        self.assertIsNotNone(transaction_id)

    def test_repay_borrowing(self):
        transaction_id = self.borrowing.borrow_funds(amount=500)
        result = self.borrowing.repay_borrowing(transaction_id, amount=250)
        self.assertTrue(result)

    def test_get_borrowing_details(self):
        transaction_id = self.borrowing.borrow_funds(amount=500)
        details = self.borrowing.get_borrowing_details(transaction_id)
        self.assertEqual(details['amount'], 500)

if __name__ == '__main__':
    unittest.main()
