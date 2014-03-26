import requests
from libmicoach.workout import *
from datetime import datetime

class Journal(object):
    
    def __init__(self, cookies):
        self.cookies = cookies
        url = 'https://micoach.adidas.com/us//Track/JournalData'
        journal_sort = {"page":1,"start":0,"limit":3000,"sort":[{"property":"startDateTime","direction":"desc"}]}
        journal_request = requests.post(url, data = journal_sort, cookies=self.cookies)
        if journal_request.status_code == 200:
            self.list = journal_request.json()['items']
    
    def __len__(self):
        return len(self.list)
    
    def __iter__(self):
            for line in self.list:
                yield line

    def __repr__(self):
        return 'Journal: contains (%d) workouts' % (len(self.list))

    def getJournalItem(self, workoutId):
        for i in range(0, len(self.list)):
            if self.list[i]['workoutId'] == workoutId:
                return self.list[i]
    
    def getWorkout(self, workoutId):
        return Workout(workoutId, self.getJournalItem(workoutId), self.cookies)
    
    def getLatestWorkout(self):
        return self.getWorkout(self.list[-1]['workoutId'])
    
    def journalAsList(self,distanceType):
        workoutList = []
        if distanceType == 'miles':
            unit = ' mi'
            paceunit = ' mi/min'
        else:
            unit = ' km'
            paceunit = ' km/min'

        for workout in reversed(self.list):
            time = datetime.strptime(workout['startDateTime'][:19],'%Y-%m-%dT%H:%M:%S')
            if 'totalDistance' in workout:
                distance = workout['totalDistance'] + unit
            else:
                distance = '0' + unit
            if 'avgPace' in workout:
                pace = workout['avgPace'] + paceunit
            else:
                pace = '0' + paceunit
            workoutList.append([
                                workout['workoutId'],
                                workout['workoutName'],
                                time.strftime('%Y-%m-%d'),
                                time.strftime('%I:%M %p'),
                                workout['activity'],
                                workout['activeTime'],
                                distance,
                                pace,
                                workout['avgHR'],
                                workout['totalCalories']
                                ])
        return workoutList
