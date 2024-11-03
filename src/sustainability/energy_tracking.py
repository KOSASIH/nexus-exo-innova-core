# src/sustainability/energy_tracking.py

import logging
from datetime import datetime
import json

class EnergyTracking:
    def __init__(self):
        self.energy_data = {}
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('EnergyTracking')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('energy_tracking.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def record_energy_generation(self, user_id, source, amount):
        timestamp = datetime.now().isoformat()
        if user_id not in self.energy_data:
            self.energy_data[user_id] = []
        
        self.energy_data[user_id].append({
            'timestamp': timestamp,
            'source': source,
            'amount': amount
        })
        self.logger.info(f"Recorded energy generation for user {user_id}: {source} - {amount} kWh")

    def get_energy_report(self, user_id):
        if user_id in self.energy_data:
            report = {
                'user_id': user_id,
                'data': self.energy_data[user_id]
            }
            self.logger.info(f"Generated energy report for user {user_id}.")
            return report
        else:
            self.logger.error(f"No energy data found for user {user_id}.")
            raise Exception("No energy data found for this user.")

    def calculate_total_generation(self, user_id):
        if user_id in self.energy_data:
            total = sum(entry['amount'] for entry in self.energy_data[user_id])
            self.logger.info(f"Total energy generation for user {user_id}: {total} kWh")
            return total
        else:
            self.logger.error(f"No energy data found for user {user_id}.")
            raise Exception("No energy data found for this user.")
