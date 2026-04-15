import csv
import requests
from io import StringIO

class StudentLookup:
    '''
    Responsible for looking up student canvas information based on GitHub Username
    
    Args:
        course: Canvas course object.
        quiz_id (int): ID of the quiz containing GitHub usernames.
    '''
    
    def __init__(self, course, quiz_id: int):
        self.course = course
        self.quiz_id = quiz_id
    
    def gh_username_to_student(self, gh_username: str) -> 'Student':
        '''
        Rip the GH usernames of students from canvas and determine who is running the script.
        '''
        quiz = self.course.get_quiz(self.quiz_id)
        reports = quiz.get_all_quiz_reports()
        csv_data = None

        # get the right type of report
        for report in reports:
            if report.report_type == 'student_analysis':
                if hasattr(report, 'file') and report.file:
                    csv_url = report.file['url']
                    response = requests.get(csv_url)
                    csv_data = response.text
                    print(f"got username quiz data")
                break

        # read csv data and search for the username
        if csv_data:
            csv_reader = csv.reader(StringIO(csv_data))
            next(csv_reader, None)  # skip headers
            
            for row in csv_reader:
                if len(row) >= 6 and row[5] == gh_username:
                    student = Student(
                        gh_username=gh_username,
                        canvas_id=int(row[1]),
                        name=row[0],
                        course=self.course
                    )
                    return student
        return None

class Student:
    '''
    Represents an individual student with course and group information

    Args:
        gh_username (str): GitHub username.
        canvas_id (int): Canvas user ID.
        name (str): Student's full name.
        course: Canvas course object.
    '''
    
    def __init__(self, gh_username: str, canvas_id: int, name: str, course):
        self.gh_username = gh_username
        self.canvas_id = canvas_id
        self.name = name
        self.course = course

    def get_team(self):
        '''Return the team this student is on'''
        groups = self.course.get_groups()
            
        for group in groups:
            users = group.get_users()
            for user in users:
                if user.id == self.canvas_id:
                    return group
        
        return None 

    def get_group_members(self):
        '''Get all members of the student's group'''
        group = self.get_team()
        
        if group:
            return group.get_users()
        
        return None
    
    def get_grade(self, assignment_id):
        '''Get current grade and submission info for an assignment'''
        try:
            assignment = self.course.get_assignment(assignment_id)
            submission = assignment.get_submission(self.canvas_id)
            return {
                'grade': submission.grade,
                'score': submission.score,
                'points_possible': assignment.points_possible,
                'submitted_at': submission.submitted_at,
                'status': submission.workflow_state
            }
        except:
            return None
