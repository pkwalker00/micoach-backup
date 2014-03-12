import requests, json
from libmicoach.journal import *

class miCoachUser(object):
    
    def __init__(self):
        self.url = 'https://micoach.adidas.com'
        self.cookies = ''
        self.loggedin = False
    
    def login(self, user_email, user_password):
        login_url = '/us/services/login/loginuser'
        creds = {'email':user_email,'password':user_password,'errors':{}}
        login_request = requests.post(self.url+login_url, data=creds)
        self.journal = ''
        if login_request.status_code == 200:
            authtoken = login_request.cookies['micoach_authtoken']
            self.cookies=dict(micoach_authtoken=authtoken)
            self.loggedin = True

    def getJournal(self):
        self.journal = Journal(self.cookies)

    def getWorkout(self, workoutId):
        workout_url = '/us/services/track/getChartWorkoutDetail?completedWorkoutId='
        workout_request = requests.get(self.url + workout_url + str(workoutId), cookies=self.cookies)
        workout_data = json.loads(workout_request.text)
        del workout_data['details']['WorkoutInfo']
        return workout_data
    
    def getLatestWorkout(self):
        return self.getWorkout(self.journal['items'][-1]['workoutId'])
