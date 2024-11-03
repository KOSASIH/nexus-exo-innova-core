# src/security/biometric_auth.py

import logging
import base64
import hashlib
import os
import json

class BiometricAuth:
    def __init__(self):
        self.users = {}
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('BiometricAuth')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('biometric_auth.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def register_user(self, user_id, biometric_data):
        # Hash the biometric data for storage
        hashed_data = self.hash_biometric_data(biometric_data)
        self.users[user_id] = hashed_data
        self.logger.info(f"User  {user_id} registered successfully.")

    def hash_biometric_data(self, biometric_data):
        # Hash the biometric data using SHA-256
        return hashlib.sha256(biometric_data.encode()).hexdigest()

    def authenticate_user(self, user_id, biometric_data):
        if user_id not in self.users:
            self.logger.error(f"User  {user_id} not found.")
            return False
        
        hashed_data = self.hash_biometric_data(biometric_data)
        if self.users[user_id] == hashed_data:
            self.logger.info(f"User  {user_id} authenticated successfully.")
            return True
        else:
            self.logger.warning(f"Authentication failed for user {user_id}.")
            return False

    def save_users(self, filename='users.json'):
        with open(filename, 'w') as f:
            json.dump(self.users, f)
        self.logger.info("User  data saved successfully.")

    def load_users(self, filename='users.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.users = json.load(f)
            self.logger.info("User  data loaded successfully.")
        else:
            self.logger.warning("User  data file not found.")
