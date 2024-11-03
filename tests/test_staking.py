# tests/test_staking.py

import unittest
from src.staking import Staking  # Assuming you have a Staking class in src/staking.py

class TestStaking(unittest.TestCase):
    def setUp(self):
        self.staking = Staking()

    def test_stake_tokens(self):
        stake_id = self.staking.stake_tokens(user_id="user_001", amount=100)
        self.assertIsNotNone(stake_id)

    def test_unstake_tokens(self):
        stake_id = self.staking.stake_tokens(user_id="user_001", amount=100)
        result = self.staking.unstake_tokens(stake_id)
        self.assertTrue(result)

    def test_get_staking_details(self):
        stake_id = self.staking.stake_tokens(user_id="user_001", amount=100)
        details = self.staking.get_staking_details(stake_id)
        self.assertEqual(details['amount'], 100)

if __name__ == '__main__':
    unittest.main()
