# scripts/deploy_contracts.py

import json
from web3 import Web3
from solcx import compile_source
import os

# Connect to Ethereum network (e.g., Ganache, Infura, etc.)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Change to your provider
w3.eth.defaultAccount = w3.eth.accounts[0]  # Set default account

# Load Solidity contract source code
def load_contract_source(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Compile Solidity contract
def compile_contract(source_code):
    compiled_sol = compile_source(source_code)
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_id, contract_interface

# Deploy contract
def deploy_contract(contract_interface):
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt.contractAddress

if __name__ == "__main__":
    contract_source = load_contract_source('path/to/YourContract.sol')  # Update with your contract path
    contract_id, contract_interface = compile_contract(contract_source)
    contract_address = deploy_contract(contract_interface)
    print(f"Contract deployed at address: {contract_address}")
