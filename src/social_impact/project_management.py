# src/social_impact/project_management.py

import logging
from datetime import datetime

class ProjectManagement:
    def __init__(self):
        self.projects = {}
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('ProjectManagement')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('project_management.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def create_project(self, project_id, title, description, target_amount):
        self.logger.info(f"Creating project: {title} (ID: {project_id})")
        self.projects[project_id] = {
            'title': title,
            'description': description,
            'target_amount': target_amount,
            'current_amount': 0,
            'donors': [],
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.logger.info(f"Project created successfully: {self.projects[project_id]}")

    def update_project(self, project_id, title=None, description=None, target_amount=None):
        if project_id not in self.projects:
            self.logger.error(f"Project ID {project_id} not found.")
            raise Exception("Project not found.")
        
        if title:
            self.projects[project_id]['title'] = title
        if description:
            self.projects[project_id]['description'] = description
        if target_amount is not None:
            self.projects[project_id]['target_amount'] = target_amount
        
        self.projects[project_id]['updated_at'] = datetime.now().isoformat()
        self.logger.info(f"Project updated: {self.projects[project_id]}")

    def delete_project(self, project_id):
        if project_id in self.projects:
            del self.projects[project_id]
            self.logger.info(f"Project ID {project_id} deleted.")
        else:
            self.logger.error(f"Project ID {project_id} not found.")
            raise Exception("Project not found.")

    def add_donation(self, project_id, donor_id, amount):
        if project_id not in self.projects:
            self.logger.error(f"Project ID {project_id} not found.")
            raise Exception("Project not found.")
        
        self.projects[project_id]['current_amount'] += amount
        self.projects[project_id]['donors'].append({'donor_id': donor_id, 'amount': amount})
        self.logger.info(f"Donation of ${amount:.2f} added to project {project_id} from donor {donor_id}.")

    def get_project_info(self, project_id):
        if project_id in self.projects:
            return self.projects[project_id]
        else:
            self.logger.error(f"Project ID {project_id} not found.")
            raise Exception("Project not found.")
