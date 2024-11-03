# src/security/multi_signature.py

import logging
import hashlib
import json

class MultiSignatureWallet:
    def __init__(self, required_signatures):
        self.required_signatures = required_signatures
        self.signatures = {}
        self.transactions = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('MultiSignatureWallet')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('multi_signature.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def add_signature(self, transaction_id, signer_id, signature):
        if transaction_id not in self.signatures:
            self.signatures[transaction_id] = {}
        
        self.signatures[transaction_id][signer_id] = signature
        self.logger.info(f"Signature added for transaction {transaction_id} by signer {signer_id}.")

        if self.is_transaction_complete(transaction_id):
            self.execute_transaction(transaction_id)

    def is_transaction_complete(self, transaction_id):
        if transaction_id in self.signatures:
            return len(self.signatures[transaction_id]) >= self.required_signatures
        return False

    def execute_transaction(self, transaction_id):
        # Here you would implement the logic to execute the transaction
        self.logger.info(f"Executing transaction {transaction_id} with signatures: {self.signatures[transaction_id]}")
        self.transactions.append(transaction_id)
        del self.signatures[transaction_id]  # Clear signatures after execution

    def create_transaction(self, transaction_data):
        transaction_id = self.hash_transaction(transaction_data)
        self.logger.info(f"Transaction created with ID: {transaction_id}")
        return transaction_id

    def hash_transaction(self, transaction_data):
        return hashlib.sha256(json.dumps(transaction_data, sort_keys=True).encode()).hexdigest()

    def get_transaction_status(self, transaction_id):
        if transaction_id in self.signatures:
            return {
                'transaction_id': transaction_id,
                'signatures': self.signatures[transaction_id],
                'complete': self.is_transaction_complete(transaction_id)
            }
        else:
            return {
                'transaction_id': transaction_id,
                'signatures': {},
                'complete': False
            }

    def get_all_transactions(self):
        return self.transactions

    def clear_signatures(self, transaction_id):
        if transaction_id in self.signatures:
            del self.signatures[transaction_id]
            self.logger.info(f"Cleared signatures for transaction {transaction_id}.")
        else:
            self.logger.warning(f"No signatures found for transaction {transaction_id}.")
