# src/nft/nft_metadata.py

import json
import logging
import requests

class NFTMetadata:
    def __init__(self, ipfs_url):
        self.ipfs_url = ipfs_url
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('NFTMetadata')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('nft_metadata.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def upload_metadata(self, metadata):
        self.logger.info("Uploading metadata to IPFS...")
        response = requests.post(f"{self.ipfs_url}/api/v0/add", files={'file': json.dumps(metadata).encode()})
        if response.status_code == 200:
            ipfs_hash = response.json()['Hash']
            self.logger.info(f"Metadata uploaded successfully! IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            self.logger.error("Failed to upload metadata to IPFS.")
            raise Exception("IPFS upload failed.")

    def retrieve_metadata(self, ipfs_hash):
        self.logger.info(f"Retrieving metadata from IPFS: {ipfs_hash}...")
        response = requests.get(f"{self.ipfs_url}/api/v0/cat?arg={ipfs_hash}")
        if response.status_code == 200:
            metadata = json.loads(response.text)
            self.logger.info("Metadata retrieved successfully.")
            return metadata
        else:
            self.logger.error("Failed to retrieve metadata from IPFS.")
            raise Exception("IPFS retrieval failed.")
