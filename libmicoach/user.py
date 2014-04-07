from libmicoach.journal import Journal
import requests
from bs4 import BeautifulSoup

class miCoachUser(object):
    
    def __init__(self):
        self.cookies = ''
        self.loggedin = False
        self.username = ''
        self.journal =''
        self.distanceUnit = ''
        self.heightUnit = ''
        self.weightUnit = ''
    
    def __repr__(self):
        if self.loggedin == False:
            return 'miCoach user not logged in'
        else:
            return 'Logged in as %s' % (self.username)
    
    def login(self, user_email, user_password):
        url = 'https://micoach.adidas.com/us/services/login/loginuser'
        creds = {'email':user_email,'password':user_password,'errors':{}}
        try:
            login_request = requests.post(url, data=creds, timeout=60)
            authtoken = login_request.cookies['micoach_authtoken']
            self.cookies=dict(micoach_authtoken=authtoken)
            self.loggedin = True
            self.getJournal()
            self.getUserInfo()
        except:
            return "Login failed"

    def logout(self):
        self.cookies = ''
        self.loggedin = False
        self.username = ''
        self.journal =''
        self.distanceUnit = ''
        self.heightUnit = ''
        self.weightUnit = ''
    
    def getUserInfo(self):
        url = 'https://micoach.adidas.com/us/UI/Settings/General.aspx'
        request = requests.get(url, cookies=self.cookies)
        html = BeautifulSoup(request.text)
        self.username = html.find_all(id='loggedAsUserName')[0].text
        
        if 'checked' in html.find_all(id='rbDistanceMiles')[0].input.attrs:
            self.distanceUnit = 'miles'
        else:
            self.distanceUnit = 'kilometers'
        
        if 'checked' in html.find_all(value='rbHeightWeightFeetPounds')[0].attrs:
            self.heightUnit = 'feet'
            self.weightUnit = 'pounds'
        else:
            self.heightUnit = 'centimeters'
            self.weightUnit = 'kilograms'

    def getJournal(self):
        self.journal = Journal(self.cookies)

    def getWorkout(self, workoutId):
        return self.journal.getWorkout(workoutId)
    
    def getLatestWorkout(self):
        return self.journal.getLatestWorkout()

    def journalList(self):
        return self.journal.journalAsList(self.distanceUnit)
