# src/ai_wallet/wallet.py

import json
import os
from web3 import Web3
from eth_account import Account
from datetime import datetime
import requests

class Wallet:
    def __init__(self, provider_url, private_key=None):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.web3.eth.account.from_key(private_key) if private_key else self.create_wallet()
        self.balance = self.get_balance()
        self.transaction_history = []

    def create_wallet(self):
        account = self.web3.eth.account.create()
        self.save_wallet(account)
        return account

    def save_wallet(self, account):
        wallet_data = {
            'address': account.address,
            'private_key': account.privateKey.hex()
        }
        os.makedirs('wallets', exist_ok=True)
        with open(f'wallets/{account.address}.json', 'w') as f:
            json.dump(wallet_data, f)

    def load_wallet(self, address):
        with open(f'wallets/{address}.json', 'r') as f:
            wallet_data = json.load(f)
            self.account = self.web3.eth.account.from_key(wallet_data['private_key'])
            self.balance = self.get_balance()

    def get_balance(self):
        return self.web3.eth.get_balance(self.account.address)

    def send_transaction(self, to_address, amount, gas_price=None):
        if gas_price is None:
            gas_price = self.estimate_gas_price()

        tx = {
            'to': to_address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
        }
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Log transaction
        self.log_transaction(tx_hash.hex(), to_address, amount, gas_price)

        return tx_hash.hex()

    def estimate_gas_price(self):
        return self.web3.eth.gas_price

    def log_transaction(self, tx_hash, to_address, amount, gas_price):
        transaction = {
            'tx_hash': tx_hash,
            'to': to_address,
            'amount': amount,
            'gas_price': gas_price,
            'timestamp': datetime.now().isoformat()
        }
        self.transaction_history.append(transaction)
        self.save_transaction_history()

    def save_transaction_history(self):
        with open(f'wallets/{self.account.address}_history.json', 'w') as f:
            json.dump(self.transaction_history, f)

    def get_wallet_info(self):
        return {
            'address': self.account.address,
            'balance': self.web3.fromWei(self.balance, 'ether'),
            'transaction_history': self.transaction_history
        }

    def enable_2fa(self, user_email):
        # Placeholder for 2FA implementation
        # This could involve sending a verification code to the user's email or phone
        print(f"2FA enabled for {user_email}. Please verify your identity.")

    def recover_wallet(self, recovery_phrase):
        # Placeholder for wallet recovery implementation
        # This could involve checking the recovery phrase against stored data
        print("Wallet recovery initiated. Please provide the recovery phrase.")

    def notify_user(self, message):
        # Placeholder for notification system
        # This could involve sending an email or push notification
        print(f"Notification: {message}")

    def get_transaction_history(self):
        return self.transaction_history
