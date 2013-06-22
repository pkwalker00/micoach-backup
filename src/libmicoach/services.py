import urllib, http.client
from lxml import etree
import libmicoach.xmlassist as xa

class miCoachService(object):

    isconnected = False
    auth_cookie = ''
    
    def __init__(self, service, email=None, password=None):
        self.location = ('/Services/%s') % (service)
        self.http = http.client.HTTPConnection('micoach.adidas.com')

        if miCoachService.isconnected == False:
            if email == None or password == None:
                return

            print("Not yet connected. Connecting...")
            self.connect(email, password)

    def __getattr__(self, attr): 
        return lambda self=self, *args, **kwargs: self.call(attr, *args, **kwargs)

    def call(self, method, *args, **kwargs):
        if miCoachService.isconnected:
            data = self.GET(method, **kwargs)
            return  etree.fromstring(data)

    def GET(self, action, *args, **kwargs) :
        params = urllib.parse.urlencode(kwargs)
        #print('GET %s/%s?%s' % (self.location, action, params))
        self.http.request('GET', ('%s/%s?%s') % (self.location, action, params), headers = {'cookie': self.auth_cookie})
        data = self.http.getresponse().read()
        return data

    def connect(self, email, password):

        params = urllib.parse.urlencode({'email': email})+'&'+urllib.parse.urlencode({'password': password})+'&isRememberMeSelected=False&TimeZoneInfo='
        headers = {
                    'Content-Type': 'x-www-form-urlencoded',
                    'Connection': 'keep-alive',
                    'Accept': 'text/html'
                    }
        https = http.client.HTTPSConnection('micoach.adidas.com', 443)
        https.request('POST', '/Login.aspx', params, headers)
        https_authcookie = https.getresponse().getheader('set-cookie')

        self.http = http.client.HTTPConnection('micoach.adidas.com')
        self.http.request('GET', '/Services/UserProfileWS.asmx/miCoachLogin?'+ params, headers = {'cookie': https_authcookie})
        response = self.http.getresponse()
        xml = etree.fromstring(response.read())
        status = xa.search(xml, 'ResultStatusMessage')

        if status == 'SUCCESS':
            miCoachService.auth_cookie = response.getheader('set-cookie') 
            miCoachService.isconnected = True

class CompletedWorkout(miCoachService):
    def __init__(self, email=None, password=None):
        miCoachService.__init__(self, 'CompletedWorkoutWS.asmx', email, password)

class UserProfile(miCoachService):
    def __init__(self, email=None, password=None):
        miCoachService.__init__(self, 'UserProfileWS.asmx', email, password)

class Calendar(miCoachService):
    def __init__(self, email=None, password=None):
        miCoachService.__init__(self, 'CalendarWS.asmx', email, password)

class SyncAPI(miCoachService):
    def __init__(self, email=None, password=None):
        miCoachService.__init__(self, 'SyncAPIWS.asmx', email, password)

class Route(miCoachService):
    def __init__(self, email=None, password=None):
        miCoachService.__init__(self, 'RouteWS.asmx', email, password)

class Activity(miCoachService):
    def __init__(self, email=None, password=None):
        miCoachService.__init__(self, 'ActivityWS.asmx', email, password)
