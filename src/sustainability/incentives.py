# src/sustainability/incentives.py

import logging

class IncentiveDistribution:
    def __init__(self, energy_tracker):
        self.energy_tracker = energy_tracker
        self.incentives = {}
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('IncentiveDistribution')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('incentives.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def calculate_incentive(self, user_id):
        total_generation = self.energy_tracker.calculate_total_generation(user_id)
        incentive = total_generation * 0.1  # Example: $0.10 per kWh generated
        self.incentives[user_id] = incentive
        self.logger.info(f"Calculated incentive for user {user_id}: ${incentive:.2f}")
        return incentive

    def distribute_incentives(self):
        for user_id in self.incentives:
            self.logger.info(f"Distributing incentive of ${self.incentives[user_id]:.2f} to user {user_id}.")
            # Here you would implement the logic to transfer the incentive to the user (e.g., via a payment API)

    def get_incentive_report(self, user_id):
        if user_id in self.incentives:
            report = {
                'user_id': user_id,
                'incentive': self.incentives[user_id]
            }
            self.logger.info(f"Generated incentive report for user {user_id}.")
            return report
        else:
            self.logger.error(f"No incentive data found for user {user_id}.")
            raise Exception("No incentive data found for this user.")
