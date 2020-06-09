from __future__ import print_function
import pickle
import os.path
import time
import datetime
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly','https://www.googleapis.com/auth/classroom.coursework.students.readonly','https://www.googleapis.com/auth/classroom.coursework.students']
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly','https://www.googleapis.com/auth/classroom.coursework.me']

def main():
    """Shows basic usage of the Classroom API.

    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courseWork = service.courses().courseWork()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        
        for course in courses:
            courseWorkVar = courseWork.list(courseId=course['id']).execute()
            print(course['name'])
            if "courseWork" in courseWorkVar:
                for i in courseWorkVar["courseWork"]:
                    if "dueDate" in i:
                        if "Project" in i["title"] or "Summative" in i["title"] or "Assessment" in i["title"] or "test" in i["title"]:
                            if datetime.datetime.now().day <= i["dueDate"]["day"] - 1 and datetime.datetime.now().year == i["dueDate"]["year"] and datetime.datetime.now().month <= i["dueDate"]["month"] :
                                print("upcoming summatives:")
                                print("\t"+i["title"])
                                print("\t"+str(i["dueDate"]))
        for course in courses:
            courseWorkVar = courseWork.list(courseId=course['id']).execute()
            print(course['name'])
            if "courseWork" in courseWorkVar:
                for i in courseWorkVar["courseWork"]:
                    if "dueDate" in i:
                        if datetime.datetime.now().day == i["dueDate"]["day"] - 1 and datetime.datetime.now().year == i["dueDate"]["year"] and datetime.datetime.now().month == i["dueDate"]["month"] :
                            print("\t"+i["title"])
                       
              
           
if __name__ == '__main__':
    main()