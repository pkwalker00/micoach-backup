import requests, json
from libmicoach import polyencode, gpx, tcx

class Workout(object):
    
    def __init__(self, workoutId, journalItem, cookies):
        url = 'https://micoach.adidas.com/us/services/track/getChartWorkoutDetail?completedWorkoutId='
        workout_request = requests.get(url + str(workoutId), cookies=cookies)
        self.workout = json.loads(workout_request.text)['details']
        if 'GPSPathThumbnail' in self.workout['WorkoutInfo']:
            del self.workout['WorkoutInfo']['GPSPathThumbnail']
        if 'GPSActive' in self.workout['WorkoutInfo']:
            self.updateElevations()
        self.journalItem = journalItem
    
    def __repr__(self):
        return 'Workout ID: %s, Name: %s' % (self.workout['WorkoutInfo']['CompletedWorkoutID'],  self.workout['WorkoutInfo']['WorkoutName'])

    def updateElevations(self):
        elevations = []
        gpspoints = [[]]
        index = 0
        for point in self.workout['CompletedWorkoutDataPoints']:
            
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
        for point in self.workout['CompletedWorkoutDataPoints']:
            point['Altitude'] = elevations[index]
            index = index + 1

    def writeGpx(self, filename):
        gpx.writeGpx(filename, self.workout)
    
    def writeTcx(self, filename):
        tcx.writeTcx(filename, self.workout)
    
    def writeJson(self, filename):
        with open(filename, 'w') as workout:
            workout.write(json.dumps(self.workout, sort_keys=True, indent=4))
