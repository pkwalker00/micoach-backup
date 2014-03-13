import requests, json
from libmicoach import polyencode

class Workout(object):
    
    def __init__(self, workoutId, cookies):
        url = 'https://micoach.adidas.com/us/services/track/getChartWorkoutDetail?completedWorkoutId='
        workout_request = requests.get(url + str(workoutId), cookies=cookies)
        self.workout = json.loads(workout_request.text)['details']
        del self.workout['WorkoutInfo']['GPSPathThumbnail']
    
    def elevation(self):
        elevations = []
        gpspoints = []
        index = 0
        for point in self.workout['CompletedWorkoutDataPoints']:
            if len(gpspoints) == 0:
                gpspoints.append([])
            
            if len(gpspoints[index]) < 512:
                gpspoints[index].append((point['Latitude'], point['Longitude']))
            else:
                gpspoints.append([])
                index = index + 1
                gpspoints[index].append((point['Latitude'], point['Longitude']))
            
        for group in gpspoints:
            params = polyencode.encode_coords(group)
        url = 'http://maps.googleapis.com/maps/api/elevation/xml?sensor=true&locations=enc:'+params

    def __repr__(self):
        return 'Workout ID: %s, Name: %s' % (self.workout['WorkoutInfo']['CompletedWorkoutID'],  self.workout['WorkoutInfo']['WorkoutName'])

    def writeGpx(self):
        pass
    
    def writeTcx(self):
        pass
    
    def writeJson(self):
        pass
