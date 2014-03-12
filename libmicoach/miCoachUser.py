import requests, json

class miCoachUser(object):

    cookies = ''
    loggedin = False
    
    def __init__(self):
        self.url = 'https://micoach.adidas.com'
    
    def login(self, user_email, user_password):
        login_url = '/us/services/login/loginuser'
        creds = {'email':user_email,'password':user_password,'errors':{}}
        login_request = requests.post(self.url+login_url, data=creds)
        if login_request.status_code == 200:
            authtoken = login_request.cookies['micoach_authtoken']
            miCoachUser.cookies=dict(micoach_authtoken=authtoken)
            miCoachUser.loggedin = True
            print("Login Successful")
            print("Retrieving Journal")
            self.journal = self.getJournal()
            print("Complete")

    def getJournal(self):
        journal_url = '/us//Track/JournalData'
        journal_sort = {"page":1,"start":0,"limit":1000,"sort":[{"property":"startDateTime","direction":"desc"}]}
        journal_request = requests.post(self.url+journal_url, data = journal_sort, cookies=miCoachUser.cookies)
        journal_list = json.loads(journal_request.text)
        return journal_list

    def getWorkout(self, workoutId):
        workout_url = '/us/services/track/getChartWorkoutDetail?completedWorkoutId='
        workout_request = requests.get(self.url + workout_url + str(workoutId), cookies=miCoachUser.cookies)
        workout_data = json.loads(workout_request.text)
        del workout_data['details']['WorkoutInfo']
        return workout_data
    
    def getLatestWorkout(self):
        return self.getWorkout(self.journal['items'][-1]['workoutId'])
