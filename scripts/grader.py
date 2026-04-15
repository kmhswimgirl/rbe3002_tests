# makes a dictionary using student ID vs answer to the GH username quiz on canvas
from canvasapi import Canvas
import yaml
import os
import json
import argparse
import requests
from io import StringIO
import csv
from dataclasses import dataclass
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Rips GitHub usernames off of a Canvas quiz using the Canvas LMS API')
parser.add_argument('-n', '--name', help='GitHub user who triggered the action')
parser.add_argument('-o', '--config', help='Autograder configuration file path', default='config/config.yaml')
parser.add_argument('-r', '--results', help='ROS launch_pytest results.xml file path', default='results.xml')
parser.add_argument('-l', '--lab', choices=['lab2-ind', 'lab2-grp', 'lab3-ind', 'lab3-grp', 'lab4-ind', 'lab4-grp'], 
                    default='lab2-ind', help='Lab assignment')
parser.add_argument('-d', '--debug', action='store_true', help='run the debug functions')
parser.add_argument('-a', '--api', help="passing in a canvas api key secret")
args = parser.parse_args()

# load yaml config file
with open(args.config, 'r') as file:
    info = yaml.safe_load(file)

# general setup
API_URL = info['canvas']['instance_url']
API_KEY = args.api
COURSE_ID = info['rbe_3002']['course_id']
QUIZ_ID = info['rbe_3002']['gh_user_quiz']

canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)
quiz = course.get_quiz(QUIZ_ID)

@dataclass
class Student:
    name: str
    gh_username: str
    canvas_id: int
    team: int  

class Student:
    def __init__(self):
        self.debug = args.debug
        self.test_results = args.results
        self.course = course

    def gh_username_to_canvas_id(self, gh_username: str, course, quiz_id: int) -> Student:
        '''
        Rip the GH usernames of students from canvas and determine who is running the script.
        Also determine what group they are in if it is a group assignment.
        '''

        quiz = course.get_quiz(quiz_id)
        reports = quiz.get_all_quiz_reports()
        csv_data = None

        # get the right type of report
        for report in reports:
            if report.report_type == 'student_analysis':
                if hasattr(report, 'file') and report.file:
                    csv_url = report.file['url']
                    response = requests.get(csv_url)
                    csv_data = response.text
                    print(f"Retrieved Username Data")
                break

        # read csv data and search for the username
        if csv_data:
            csv_reader = csv.reader(StringIO(csv_data))
            next(csv_reader, None)  # Skip headers
            self.csv_data = csv_data
            
            for row in csv_reader:
                if len(row) >= 6 and row[5] == gh_username:
                    student = Student()
                    student.gh_username = gh_username
                    student.canvas_id = int(row[1])
                    student.name = row[0]
        return student

    def get_team(self, student_id: int):
        '''return the team the student is on'''

        groups = course.get_groups()
            
        for group in groups:
            users = group.get_users()
            for user in users:
                if user.id == student_id:
                    return group
        
        return None 

    def get_group_members(self, student_id: int, course):
        '''Get all members of the student's group'''

        group = self.get_student_group(student_id, self.course)
        
        if group:
            return group.get_users()
        
        return None

    def parse_test_results(self, xml_file):
        """Parse test results XML"""
        tree = ET.parse(xml_file)
        results = []
        
        for testcase in tree.getroot().findall('.//testcase'):
            test_info = {
                'name': testcase.get('name'),
                'classname': testcase.get('classname'),
                'status': 0 if testcase.find('failure') is None else 1,
                'time': float(testcase.get('time', 0))
            }
            results.append(test_info)
        
        return results

   


