from canvasapi import Canvas
import yaml
import os
import argparse
import re

# my classes
from student import StudentLookup, Student
from xml_parsing import XMLScoring

parser = argparse.ArgumentParser(description='Rips GitHub usernames off of a Canvas quiz using the Canvas LMS API')
parser.add_argument('-o', '--config', help='Autograder configuration file path', default='config/config.yaml')
args = parser.parse_args()

# load yaml config file
with open(args.config, 'r') as file:
    info = yaml.safe_load(file)

# general setup
API_URL = info['canvas']['instance_url']
API_KEY = os.getenv("CANVAS_API")
COURSE_ID = info['rbe_3002']['course_id']
PUB_COURSE_ID = info['canvas']['course_id']
GH_ACTOR = "AdamBuier"

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

xml = XMLScoring(xml_file='results/results.xml')
example_results = xml.get_test_results()
print(example_results)

def find_username_quiz(course):
    '''
    Find the GitHub username quiz by matching common keywords
    '''
    keywords = ['gh', 'github', 'username']
    pattern = '|'.join(keywords) 
    
    quizzes = course.get_quizzes()
    for quiz in quizzes:
        if re.search(pattern, quiz.title, re.IGNORECASE):
            return quiz
    return None

def test_results_to_score(lab, test_results, student: Student):
    '''intake xml test results and lab name and output score based on sign off'''


    pass

canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

quiz = find_username_quiz(course)

print(quiz.id)

lookup = StudentLookup(course, quiz.id)
student = lookup.gh_username_to_student(GH_ACTOR)

print(student.name)
print(student.canvas_id)

