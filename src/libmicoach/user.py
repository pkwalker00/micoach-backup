from libmicoach import services, schedule
import libmicoach.xmlassist as xa
from lxml import etree

class miCoachUser(object):
    
    def __init__(self, email=None, password=None):
        if email != None and password != None:
             self.login(email, password)

    def login(self, email, password):
       self.profile = services.UserProfile(email, password)
       self.schedule = schedule.Schedule()
       self.getProfile()

    def getProfile(self):

        profile = self.profile.GetUserGeneralSettings()
        self.screenname = xa.search(profile, 'ScreenName')
        self.email = xa.search(profile, 'Email')
        self.firstname = xa.search(profile, 'FirstName')
        self.lastname = xa.search(profile, 'LastName')
        self.unitofdistance = int(xa.search(profile, 'UserUnitOfDistancePreference'))
        self.unitofweight = int(xa.search(profile, 'UserUnitOfWeightPreference'))
        self.unitofheight = int(xa.search(profile, 'UserUnitOfHeightPreference'))
        if int(xa.findvalue(profile, 'Gender')) == 1:
            self.gender = 'Male'
        else:
            self.gender = 'Female'
        self.country = xa.search(profile, 'CountryCode')

    def getSchedule(self):
        return self.schedule
