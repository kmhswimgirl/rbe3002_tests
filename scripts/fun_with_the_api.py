from canvasapi import Canvas
import os
import re

API_URL = "https://canvas.wpi.edu"
API_KEY = os.getenv("CANVAS_API")
COURSE_ID = 82620

canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

assignments = course.get_assignments()
labs = {}

for assignment in assignments:
    name = assignment.name
    
    match = re.match(r'(Lab\d+)\s*-\s*(INDV|IND|GRP\.?|GROUP)\s*-\s*(.*?)(?:\s*\(.*\))?$', name, re.IGNORECASE)
    
    if match:
        lab = match.group(1)
        assignment_type = match.group(2).upper()
        task = match.group(3).strip()
        
        if assignment_type in ['IND', 'INDV']:
            assignment_type = 'INDV'
        else:  
            assignment_type = 'GROUP'
        
        if lab not in labs:
            labs[lab] = {'INDV': [], 'GROUP': []}
        
        labs[lab][assignment_type].append({
            'id': assignment.id,
            'task': task,
            'name': name,
            'points': assignment.points_possible,
            'due': assignment.due_at
        })

for lab in sorted(labs.keys()):
    print(f"\n{lab}:")
    for atype in ['INDV', 'GROUP']:
        if labs[lab][atype]:
            print(f"  {atype}:")
            for task in labs[lab][atype]:
                print(f"    - {task['task']} ({task['points']} pts)")
                print(f"      ID: {task['id']}, Due: {task['due']}")