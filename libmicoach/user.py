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
        try:   
            url1 = 'https://cp.adidas.com/idp/startSSO.ping'
            url2 = 'https://cp.adidas.com/sp/ACS.saml2'
            url3 = 'https://micoach.adidas.com/us/Login'
            
            params1 = {
                                'FirstName':'',
                                'InErrorResource':'https://micoach.adidas.com/us/Login/OpenToken', 
                                'LastName':'', 
                                'PartnerSpId':'sp:micoach', 
                                'TargetResource':'https://micoach.adidas.com/us/Login/OpenToken?popupName=login-popup',
                                'loginUrl':'https://micoach.adidas.com/us/Login/OpenToken?popupName=login-popup', 
                                'password':user_password, 
                                'username':user_email, 
                                'validator_id':'micoach'
                                }
            request1 = requests.post(url1, data=params1, timeout=60)

            SAMLResponse = BeautifulSoup(request1.text).find_all('input')[0]['value']
            RelayState = BeautifulSoup(request1.text).find_all('input')[1]['value']

            params2 = {
                                'RelayState':RelayState, 
                                'SAMLResponse':SAMLResponse
                                }
            request2 = requests.post(url2,  data=params2, timeout=60)

            ot = BeautifulSoup(request2.text).find_all('input')[0]['value']
            params3 = {
                                'ot':ot,
                                'popupName':'login-popup', 
                                'error':'',
                                'rememberMe':'False'
                                }
            request3 = requests.post(url3, data = params3,  timeout=60)
            self.cookies = {
                                    'micoach_authtoken':request3.cookies['micoach_authtoken'],
                                    'user_data':request3.cookies['user_data']
                                    }
            print(self.cookies)
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
