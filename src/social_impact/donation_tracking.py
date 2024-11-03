# src/social_impact/donation_tracking.py

import logging

class DonationTracking:
    def __init__(self, project_management):
        self.project_management = project_management
        self.donations = {}
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('DonationTracking')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('donation_tracking.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def record_donation(self, project_id, donor_id, amount):
        if project_id not in self.project_management.projects:
            self.logger.error(f"Project ID {project_id} not found.")
            raise Exception("Project not found.")
        
        if donor_id not in self.donations:
            self.donations[donor_id] = []
        
        self.donations[donor_id].append({'project_id': project_id, 'amount': amount})
        self.logger.info(f"Recorded donation of ${amount:.2f} from donor {donor_id} to project {project_id}.")
        
        # Update the project with the new donation
        self.project_management.add_donation(project_id, donor_id, amount)

    def get_donor_report(self, donor_id):
        if donor_id in self.donations:
            report = {
                'donor_id': donor_id,
                'donations': self.donations[donor_id]
            }
            self.logger.info(f"Generated donor report for {donor_id}.")
            return report
        else:
            self.logger.error(f"No donation data found for donor {donor_id}.")
            raise Exception("No donation data found for this donor.")

    def get_project_donations(self, project_id):
        donations = []
        for donor_id, donor_donations in self.donations.items():
            for donation in donor_donations:
                if donation['project_id'] == project_id:
                    donations.append({'donor_id': donor_id, 'amount': donation['amount']})
        
        self.logger.info(f"Retrieved donations for project {project_id}.")
        return donations

    def send_donation_acknowledgment(self, donor_id, project_id, amount):
        # Simulate sending an acknowledgment (e.g., email, SMS, etc.)
        self.logger.info(f"Sending acknowledgment to donor {donor_id} for donation of ${amount:.2f} to project {project_id}.")
        # In a real application, you would integrate with an email/SMS service here
