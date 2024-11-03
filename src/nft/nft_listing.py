# src/nft/nft_listing.py

import json
import logging
from web3 import Web3

class NFTListing:
    def __init__(self, web3_provider, contract_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract_address = contract_address
        self.private_key = private_key
        self.logger = self.setup_logger()
        self.contract = self.load_contract()

    def setup_logger(self):
        logger = logging.getLogger('NFTListing')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('nft_listing.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_contract(self):
        with open('nft_contract_abi.json') as f:
            abi = json.load(f)
        return self.web3.eth.contract(address=self.contract_address, abi=abi)

    def list_nft(self, token_id, price):
        self.logger.info(f"Listing NFT {token_id} for {price} ETH...")
        nonce = self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount)
        txn = self.contract.functions.listNFT(token_id, self.web3.toWei(price, 'ether')).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = self.web3.eth.account.signTransaction(txn, self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.logger.info(f"NFT listed! Transaction hash: {txn_hash.hex()}")
        return txn_hash.hex()

     def buy_nft(self, token_id):
        self.logger.info(f"Buying NFT {token_id}...")
        nonce = self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount)
        txn = self.contract.functions.buyNFT(token_id).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = self.web3.eth.account.signTransaction(txn, self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.logger.info(f"NFT purchased! Transaction hash: {txn_hash.hex()}")
        return txn_hash.hex()

    def cancel_listing(self, token_id):
        self.logger.info(f"Cancelling listing for NFT {token_id}...")
        nonce = self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount)
        txn = self.contract.functions.cancelListing(token_id).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = self.web3.eth.account.signTransaction(txn, self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.logger.info(f"Listing cancelled! Transaction hash: {txn_hash.hex()}")
        return txn_hash.hex()
