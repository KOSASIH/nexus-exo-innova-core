# src/nft/nft_creation.py

import json
import logging
from web3 import Web3

class NFTCreation:
    def __init__(self, web3_provider, contract_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract_address = contract_address
        self.private_key = private_key
        self.logger = self.setup_logger()
        self.contract = self.load_contract()

    def setup_logger(self):
        logger = logging.getLogger('NFTCreation')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('nft_creation.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_contract(self):
        # Load your NFT contract ABI here
        with open('nft_contract_abi.json') as f:
            abi = json.load(f)
        return self.web3.eth.contract(address=self.contract_address, abi=abi)

    def mint_nft(self, recipient, token_uri):
        self.logger.info(f"Minting NFT for {recipient} with URI {token_uri}...")
        nonce = self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount)
        txn = self.contract.functions.mint(recipient, token_uri).buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = self.web3.eth.account.signTransaction(txn, self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.logger.info(f"NFT minted! Transaction hash: {txn_hash.hex()}")
        return txn_hash.hex()
