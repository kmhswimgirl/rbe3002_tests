# makes a dictionary using student ID vs answer to the GH username quiz on canvas
from canvasapi import Canvas
import yaml

# get quiz ID from config file (config/assignments.yaml)

# general setup
API_URL = "https://<your-canvas-domain>.instructure.com"
API_KEY = "<your-access-token>"
COURSE_ID = 12345
QUIZ_ID = 67890

canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)
quiz = course.get_quiz(QUIZ_ID)

for submission in quiz.get_submissions():
    user = course.get_user(submission.user_id)
    print(f"{user.name} ({user.login_id}): {submission.score}")
    for q in submission.get_submission_questions():
        print(q)
    print("--" * 20)