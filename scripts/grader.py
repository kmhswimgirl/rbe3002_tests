from canvasapi import Canvas
import yaml
import os
import argparse
import re

# my classes
from student import StudentLookup, Student
from xml_parsing import XMLScoring

parser = argparse.ArgumentParser(description='Rips GitHub usernames off of a Canvas quiz using the Canvas LMS API')
# parser.add_argument('-n', '--name', help='GitHub user who triggered the action')
parser.add_argument('-o', '--config', help='Autograder configuration file path', default='config/config.yaml')
# parser.add_argument('-r', '--results', help='ROS launch_pytest results.xml file path', default='results.xml')
# parser.add_argument('-l', '--lab', choices=['lab2-ind', 'lab2-grp', 'lab3-ind', 'lab3-grp', 'lab4-ind', 'lab4-grp'], 
#                     default='lab2-ind', help='Lab assignment')
# parser.add_argument('-d', '--debug', action='store_true', help='run the debug functions')
# parser.add_argument('-a', '--api', help="passing in a canvas api key secret")
args = parser.parse_args()

# load yaml config file
with open(args.config, 'r') as file:
    info = yaml.safe_load(file)

# general setup
API_URL = info['canvas']['instance_url']
API_KEY = os.getenv("CANVAS_API")
COURSE_ID = info['rbe_3002']['course_id']
QUIZ_ID = info['rbe_3002']['gh_user_quiz']
GH_ACTOR = "AdamBuier"

canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)
quiz = course.get_quiz(QUIZ_ID)

lookup = StudentLookup(course, quiz)
student = lookup.gh_username_to_student(GH_ACTOR)

# team = student.get_team()
# team_members = student.get_group_members()

# print(student.name)
# print(student.canvas_id)
# print(team.name)
# print(team.id)

# print(f"Total members: {len(list(team_members))}")

# for member in team_members:
#     print(member.name)

'''
workflow:
---------
    - figure out quiz id
    - get student using gh username canvas quiz id
    - get lab assignment ids and points possible based on arg passed in
    - calc new score + compare to current score
        - generate list of score updates
        - post list of new scores to canvas
'''

example_results = { # example XML output from lab2 
    'test_send_speed': 1, 
    'test_drive': 1, 
    'test_go_to': 1, 
    'test_correct_nodes_active': 1, 
    'test_turtlebot_topics': 1, 
    'test_path_generator_init': 1, 
    'test_convert_to_nav_msg': 1, 
    'test_generate_path_publishes': 1, 
    'test_rotate_case_1': 1, 
    'test_rotate_case_2': 1, 
    'test_controller_init': 1, 
    'test_update_odometry': 1
}

def find_username_quiz(course):
    '''
    Find the GitHub username quiz by matching common keywords
    '''
    keywords = ['gh', 'github', 'username']
    pattern = '|'.join(keywords)  # Creates: 'gh|github|username'
    
    quizzes = course.get_quizzes()
    for quiz in quizzes:
        if re.search(pattern, quiz.title, re.IGNORECASE):
            return quiz
    return None

def test_results_to_score(lab, test_results, student: Student):
    '''intake xml test results and lab name and output score based on sign off'''


    pass

quiz_function = find_username_quiz(course)
print(quiz_function.id)
print(QUIZ_ID)

# assignment_grps = course.get_assignment_groups()
# for group in assignment_grps:
#     if "Lab" in group.name:
#         print(f"Group: {group.name}")
#         print(f"ID: {group.id}")
#         assignments = course.get_assignments_for_group(group)
#         for assignment in assignments:
#             print(f'\t {assignment.name}')
#             print(f'\t {assignment.id}')

# assignment_id = 466293
# grade = student.get_grade(assignment_id)
# print(grade) 
