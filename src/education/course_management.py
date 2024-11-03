# src/education/course_management.py

import json
import logging

class CourseManagement:
    def __init__(self):
        self.courses = {}
        self.enrollments = {}
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('CourseManagement')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('course_management.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def create_course(self, course_id, title, description, instructor):
        self.logger.info(f"Creating course: {title} (ID: {course_id})")
        self.courses[course_id] = {
            'title': title,
            'description': description,
            'instructor': instructor,
            'students': [],
            'content': []
        }
        self.logger.info(f"Course created successfully: {self.courses[course_id]}")

    def update_course(self, course_id, title=None, description=None):
        if course_id not in self.courses:
            self.logger.error(f"Course ID {course_id} not found.")
            raise Exception("Course not found.")
        
        if title:
            self.courses[course_id]['title'] = title
        if description:
            self.courses[course_id]['description'] = description
        
        self.logger.info(f"Course updated: {self.courses[course_id]}")

    def delete_course(self, course_id):
        if course_id in self.courses:
            del self.courses[course_id]
            self.logger.info(f"Course ID {course_id} deleted.")
        else:
            self.logger.error(f"Course ID {course_id} not found.")
            raise Exception("Course not found.")

    def enroll_student(self, course_id, student_id):
        if course_id not in self.courses:
            self.logger.error(f"Course ID {course_id} not found.")
            raise Exception("Course not found.")
        
        if student_id not in self.enrollments:
            self.enrollments[student_id] = []
        
        self.enrollments[student_id].append(course_id)
        self.courses[course_id]['students'].append(student_id)
        self.logger.info(f"Student {student_id} enrolled in course {course_id}.")

    def get_course_info(self, course_id):
        if course_id in self.courses:
            return self.courses[course_id]
        else:
            self.logger.error(f"Course ID {course_id} not found.")
            raise Exception("Course not found.")
