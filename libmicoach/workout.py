import requests, json
from libmicoach import polyencode, gpx

class Workout(object):
    
    def __init__(self, workoutId, cookies):
        url = 'https://micoach.adidas.com/us/services/track/getChartWorkoutDetail?completedWorkoutId='
        workout_request = requests.get(url + str(workoutId), cookies=cookies)
        self.workout = json.loads(workout_request.text)['details']
        del self.workout['WorkoutInfo']['GPSPathThumbnail']
        self.updateElevations()
    
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


    def __repr__(self):
        return 'Workout ID: %s, Name: %s' % (self.workout['WorkoutInfo']['CompletedWorkoutID'],  self.workout['WorkoutInfo']['WorkoutName'])

    def writeGpx(self, filename):
        gpx.writeGpx(filename, self.workout)
    
    def writeTcx(self):
        pass
    
    def writeJson(self, filename):
        with open(filename, 'w') as workout:
            workout.write(json.dumps(w.workout, sort_keys=True, indent=4))
