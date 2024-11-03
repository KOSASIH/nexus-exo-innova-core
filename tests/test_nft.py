# tests/test_nft.py

import unittest
from src.nft import NFTMarketplace  # Assuming you have an NFTMarketplace class in src/nft.py

class TestNFTMarketplace(unittest.TestCase):
    def setUp(self):
        self.nft_marketplace = NFTMarketplace()

    def test_create_nft(self):
        nft_id = self.nft_marketplace.create_nft(owner_id="user_001", metadata={"name": "Art Piece", "description": "A beautiful art piece."})
        self.assertIsNotNone(nft_id)

    def test_buy_nft(self):
        nft_id = self.nft_marketplace.create_nft(owner_id="user_001", metadata={"name": "Art Piece", "description": "A beautiful art piece."})
        result = self.nft_marketplace.buy_nft(nft_id, buyer_id="user_002", price=100)
        self.assertTrue(result)

    def test_get_nft_details(self):
        nft_id = self.nft_marketplace.create_nft(owner_id="user_001", metadata={"name": "Art Piece", "description": "A beautiful art piece."})
        details = self.nft_marketplace.get_nft_details(nft_id)
        self.assertEqual(details['metadata']['name'], "Art Piece")

if __name__ == '__main__':
    unittest.main()
