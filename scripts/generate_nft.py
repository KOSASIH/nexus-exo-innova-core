# scripts/generate_nft.py

import json
import requests
from web3 import Web3

# Connect to Ethereum network
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Change to your provider
nft_contract_address = '0xYourNFTContractAddress'  # Replace with your NFT contract address
nft_contract_abi = json.loads('[]')  # Replace with your NFT contract ABI

nft_contract = w3.eth.contract(address=nft_contract_address, abi=nft_contract_abi)

def mint_nft(to_address, token_id, metadata_uri):
    tx_hash = nft_contract.functions.mint(to_address, token_id, metadata_uri).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

def generate_metadata(name, description, image_url):
    metadata = {
        "name": name,
        "description": description,
        "image": image_url
    }
    return metadata

if __name__ == "__main__":
    # Example NFT data
    to_address = '0xRecipientAddress'  # Replace with recipient address
    token_id = 1
    metadata = generate_metadata("Art Piece", "A beautiful art piece.", "http://example.com/image.png")
    
    # Upload metadata to IPFS or a similar service (optional)
    # response = requests.post('https://api.pinata.cloud/pinning/pinJSONToIPFS', json=metadata)
    # metadata_uri = response.json()['IpfsHash']

    # For demonstration, using a placeholder URI
    metadata_uri = "http://example.com/metadata.json"

    receipt = mint_nft(to_address, token_id, metadata_uri)
    print(f"NFT minted with transaction receipt: {receipt}")
