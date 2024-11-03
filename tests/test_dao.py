# tests/test_dao.py

import unittest
from src.dao import DAO  # Assuming you have a DAO class in src/dao.py

class TestDAO(unittest.TestCase):
    def setUp(self):
        self.dao = DAO()

    def test_create_proposal(self):
        proposal_id = self.dao.create_proposal(title="New Proposal", description="Proposal details")
        self.assertIsNotNone(proposal_id)

    def test_vote_on_proposal(self):
        proposal_id = self.dao.create_proposal(title="New Proposal", description="Proposal details")
        result = self.dao.vote_on_proposal(proposal_id, user_id="user_001", vote="yes")
        self.assertTrue(result)

    def test_get_proposal_details(self):
        proposal_id = self.dao.create_proposal(title="New Proposal", description="Proposal details")
        details = self.dao.get_proposal_details(proposal_id)
        self.assertEqual(details['title'], "New Proposal")

if __name__ == '__main__':
    unittest.main()
