from libmicoach.journal import *
from bs4 import BeautifulSoup
import threading

class miCoachUser(object):
    
    def __init__(self):
        self.cookies = ''
        self.loggedin = False
        self.username = ''
        self.journal =''
    
    def __repr__(self):
        if self.loggedin == False:
            return 'miCoach user not logged in'
        else:
            return 'Logged in as %s' % (self.username)
    
    def login(self, user_email, user_password):
        url = 'https://micoach.adidas.com/us/services/login/loginuser'
        creds = {'email':user_email,'password':user_password,'errors':{}}
        login_request = requests.post(url, data=creds)
        if login_request.status_code == 200:
            authtoken = login_request.cookies['micoach_authtoken']
            self.cookies=dict(micoach_authtoken=authtoken)
            self.loggedin = True
            threading.Thread(target = self.getJournal).start()
            self.getUserID()
    
    def logout(self):
        self.cookies = ''
        self.loggedin = False
        self.username = ''
        self.journal =''
    
    def getUserID(self):
        url = 'https://micoach.adidas.com/us/UI/Settings/General.aspx'
        request = requests.get(url, cookies=self.cookies)
        html = BeautifulSoup(request.text)
        self.username = html.find_all(id='loggedAsUserName')[0].text

    def getJournal(self):
        self.journal = Journal(self.cookies)

    def getWorkout(self, workoutId):
        return self.journal.getWorkout(workoutId)
    
    def getLatestWorkout(self):
        return self.journal.getLatestWorkout()
