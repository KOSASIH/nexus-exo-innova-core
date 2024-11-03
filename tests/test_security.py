# tests/test_security.py

import unittest
from src.security.biometric_auth import BiometricAuth
from src.security.multi_signature import MultiSignatureWallet

class TestBiometricAuth(unittest.TestCase):
    def setUp(self):
        self.biometric_auth = BiometricAuth()

    def test_register_user(self):
        self.biometric_auth.register_user(user_id="user_001", biometric_data="fingerprint_data_001")
        self.assertIn("user_001", self.biometric_auth.users)

    def test_authenticate_user_success(self):
        self.biometric_auth.register_user(user_id="user_001", biometric_data="fingerprint_data_001")
        result = self.biometric_auth.authenticate_user(user_id="user_001", biometric_data="fingerprint_data_001")
        self.assertTrue(result)

    def test_authenticate_user_failure(self):
        self.biometric_auth.register_user(user_id="user_001", biometric_data="fingerprint_data_001")
        result = self.biometric_auth.authenticate_user(user_id="user_001", biometric_data="wrong_data")
        self.assertFalse(result)

class TestMultiSignatureWallet(unittest.TestCase):
    def setUp(self):
        self.multi_sig_wallet = MultiSignatureWallet(required_signatures=2)

    def test_create_transaction(self):
        transaction_data = {"amount": 100, "to": "recipient_address"}
        transaction_id = self.multi_sig_wallet.create_transaction(transaction_data)
        self.assertIsNotNone(transaction_id)

    def test_add_signature(self):
        transaction_data = {"amount": 100, "to": "recipient_address"}
        transaction_id = self.multi_sig_wallet.create_transaction(transaction_data)
        self.multi_sig_wallet.add_signature(transaction_id, signer_id="signer_001", signature="signature_001")
        self.assertIn("signer_001", self.multi_sig_wallet.signatures[transaction_id])

    def test_execute_transaction(self):
        transaction_data = {"amount": 100, "to": "recipient_address"}
        transaction_id = self.multi_sig_wallet.create_transaction(transaction_data)
        self.multi_sig_wallet.add_signature(transaction_id, signer_id="signer_001", signature="signature_001")
        self.multi_sig_wallet.add_signature(transaction_id, signer_id="signer_002", signature="signature_002")
        self.assertIn(transaction_id, self.multi_sig_wallet.transactions)

if __name__ == '__main__':
    unittest.main()
