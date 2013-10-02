from lxml import etree
import http.client
from libmicoach import polyencode
import libmicoach.xmlassist as xa

def findelevation(workout):
    elevations = []
    gpspoints = []
    index =0
    for point in workout.iter(xa.nodestring(workout, 'CompletedWorkoutDataPoint')):
            if len(gpspoints) == 0:
                gpspoints.append([])
            
            if len(gpspoints[index]) < 512:
                gpspoints[index].append((float(point.find(xa.findstring(workout, 'Latitude')).text), float(point.find(xa.findstring(workout, 'Longitude')).text)))
            else:
                gpspoints.append([])
                index = index + 1
                gpspoints[index].append((float(point.find(xa.findstring(workout, 'Latitude')).text), float(point.find(xa.findstring(workout, 'Longitude')).text)))

    for group in gpspoints:
        params = polyencode.encode_coords(group)
        www = http.client.HTTPConnection('maps.googleapis.com')
        www.request('GET',  '/maps/api/elevation/xml?sensor=true&locations=enc:' + params)
        response = etree.fromstring(www.getresponse().read())
        for result in response.iter('result'):
            elevations.append(float(result.find('.//elevation').text))
    
    index = 0
    for point in workout.iter(xa.nodestring(workout, 'CompletedWorkoutDataPoint')):
        point.find(xa.findstring(workout, 'Altitude')).text = str(elevations[index])
        index = index + 1
    
    return workout
