# makes a dictionary using student ID vs answer to the GH username quiz on canvas
from canvasapi import Canvas
import yaml
import os
import json
import requests
from io import StringIO
import csv

with open('config/config.yaml', 'r') as file:
    info = yaml.safe_load(file)

# general setup
API_URL = info['canvas']['instance_url']
API_KEY = os.getenv("CANVAS_API")
COURSE_ID = info['rbe_3002']['course_id']
QUIZ_ID = info['rbe_3002']['gh_user_quiz']

canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)
quiz = course.get_quiz(QUIZ_ID)

# get the csv file 
reports = quiz.get_all_quiz_reports()

csv_data = None

for report in reports:
    if report.report_type == 'student_analysis':
        if hasattr(report, 'file') and report.file:
            csv_url = report.file['url']
            
            response = requests.get(csv_url)
            csv_data = response.text
            
            print(f"Retrieved {report.file['display_name']}")
        break

# read csv data
if csv_data:
    students_dict = {}
    csv_reader = csv.reader(StringIO(csv_data))
    
    # do not want column titles
    next(csv_reader, None)
    
    for row in csv_reader:
        if len(row) >= 6:
            col1 = row[0]
            col2 = row[1]
            col6 = row[5]
            
            students_dict[col6] = { # make this global later
                'name': col1,
                'student_id': int(col2)
            }
    
    
    # save file (remove this later)
    with open('results/students_parsed.json', 'w') as f:
        json.dump(students_dict, f, indent=2)


