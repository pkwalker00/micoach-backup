import requests, json, calendar
from libmicoach import polyencode, gpx, tcx

class Workout(object):
    
    def __init__(self, workoutId, journalItem, cookies):
        url = 'https://micoach.adidas.com/us/services/track/getChartWorkoutDetail?completedWorkoutId='
        workout_request = requests.get(url + str(workoutId), cookies=cookies)
        self.jsonFile = workout_request.json()
        self.jsonFile['details']['WorkoutInfo']['ActivityType'] = journalItem['activity']
        if 'GPSPathThumbnail' in self.jsonFile['details']['WorkoutInfo']:
            del self.jsonFile['details']['WorkoutInfo']['GPSPathThumbnail']
        if 'GPSActive' in self.jsonFile['details']['WorkoutInfo']:
            self.updateElevations()
        self.workout = self.jsonFile['details']
        
        
    
    def __repr__(self):
        return 'Workout ID: %s, Name: %s' % (self.workout['WorkoutInfo']['CompletedWorkoutID'],  self.workout['WorkoutInfo']['WorkoutName'])

    def updateElevations(self):
        elevations = []
        gpspoints = [[]]
        index = 0
        for point in self.jsonFile['details']['CompletedWorkoutDataPoints']:
            
            if len(gpspoints[index]) < 512:
                gpspoints[index].append((point['Latitude'], point['Longitude']))
            else:
                gpspoints.append([])
                index = index + 1
                gpspoints[index].append((point['Latitude'], point['Longitude']))
            
        for group in gpspoints:
            params = polyencode.encode_coords(group)
            url = 'http://maps.googleapis.com/maps/api/elevation/json?sensor=true&locations=enc:'+params
            elevation_request = requests.get(url)
            response = json.loads(elevation_request.text)['results']
            for result in response:
                elevations.append(result['elevation'])
            
        index = 0
        for point in self.jsonFile['details']['CompletedWorkoutDataPoints']:
            point['Altitude'] = round(elevations[index], 6)
            index = index + 1
    
    def year(self):
        return self.workout['WorkoutInfo']['StartDateTime'][:4]
    
    def month(self):
        return calendar.month_name[int(self.workout['WorkoutInfo']['StartDateTime'][5:-13])]
    
    def suggestFilename(self):
        return self.sanitize(self.workout['WorkoutInfo']['StartDateTime'][:19] + ' - ' + self.workout['WorkoutInfo']['WorkoutName'])
    
    def sanitize(self, filename):
        keepcharacters = (' ', '.', '_', '-', ':')
        santized = ''.join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
        return santized

    def writeGpx(self, filename):
        gpx.writeGpx(filename, self.workout)
    
    def writeTcx(self, filename):
        tcx.writeTcx(filename, self.workout)
    
    def writeJson(self, filename):
        with open(filename, 'w') as workout:
            workout.write(json.dumps(self.jsonFile, sort_keys=True, indent=4))
