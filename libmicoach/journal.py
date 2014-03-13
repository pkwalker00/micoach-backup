import requests,  json
from libmicoach.workout import *

class Journal(object):
    
    def __init__(self, cookies):
        self.cookies = cookies
        url = 'https://micoach.adidas.com/us//Track/JournalData'
        journal_sort = {"page":1,"start":0,"limit":3000,"sort":[{"property":"startDateTime","direction":"desc"}]}
        journal_request = requests.post(url, data = journal_sort, cookies=self.cookies)
        if journal_request.status_code == 200:
            self.list = json.loads(journal_request.text)['items']
    
    def __len__(self):
        return len(self.list)
    
    def __iter__(self):
            for line in self.list:
                yield line

    def __repr__(self):
        return 'Journal: contains (%d) workouts' % (len(self.list))

    def getWorkout(self, workoutId):
        return Workout(workoutId, self.cookies)
    
    def getLatestWorkout(self):
        return self.getWorkout(self.list[-1]['workoutId'])
