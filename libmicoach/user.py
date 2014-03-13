from libmicoach.journal import *

class miCoachUser(object):
    
    def __init__(self):
        self.url = 'https://micoach.adidas.com'
        self.cookies = ''
        self.loggedin = False
    
    def login(self, user_email, user_password):
        url = 'https://micoach.adidas.com/us/services/login/loginuser'
        creds = {'email':user_email,'password':user_password,'errors':{}}
        login_request = requests.post(url, data=creds)
        if login_request.status_code == 200:
            authtoken = login_request.cookies['micoach_authtoken']
            self.cookies=dict(micoach_authtoken=authtoken)
            self.loggedin = True
            self.journal = Journal(self.cookies)

    def refreshJournal(self):
        self.journal = Journal(self.cookies)

    def getWorkout(self, workoutId):
        return self.journal.getWorkout(workoutId)
    
    def getLatestWorkout(self):
        return self.journal.getLatestWorkout()
