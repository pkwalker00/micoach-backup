from datetime import datetime, timedelta
from dateutil.parser import parse
import dateutil.tz
from lxml import etree

def writeGpx(filename, workout):
    """Convert miCoach json to GPX format"""
    
    gps_active = workout['WorkoutInfo']['GPSActive']
    utc = workout['WorkoutInfo']['StartDateTimeUTC'][:-1]

    local = workout['WorkoutInfo']['StartDateTime'][:-1]

    #Set UTC start time for workout
    start = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S")	

    #Use computer's local timezone to correct UTC for daylight if needed
    delta = datetime.strptime(local, "%Y-%m-%dT%H:%M:%S") - datetime.now()
    datetz = dateutil.tz.tzlocal().tzname(datetime.now() + delta)

    if parse(local + datetz).timetuple().tm_isdst != 0:
        start = start - timedelta(hours=1)
    
    #create gpx container
    gpx = etree.Element('gpx', version='1.1')
    gpx.set("creator","micoach-backup")
    gpx.set("schemaLocation","http://www.topografix.com/GPX/1/1/")

    #Add metadata to gpx
    metadata = etree.SubElement(gpx, 'metadata')
    etree.SubElement(metadata, 'name').text = workout['WorkoutInfo']['WorkoutName']
    etree.SubElement(metadata, 'time').text = str(start)
    
    if gps_active:
        bounds = etree.SubElement(metadata, 'bounds')

        lat = []
        lon = []
        for point in workout['CompletedWorkoutDataPoints']:
            lat.append(point['Latitude'])
            lon.append(point['Longitude'])

        bounds.set("minlat", str(min(lat)))
        bounds.set("minlon", str(min(lon)))
        bounds.set("maxlat", str(max(lat)))
        bounds.set("maxlon", str(max(lon)))
    
    #Setup basic Track	
    trk = etree.SubElement(gpx, 'trk')
    cmt = etree.SubElement(trk, 'cmt')
    if 'UserNote' in workout['WorkoutInfo']:
        cmt.text = workout['WorkoutInfo']['UserNote']

    etree.SubElement(trk, 'src').text = 'Adidas miCoach' + u' \u00a9' 
    etree.SubElement(trk, 'link').set('href', 'https://micoach.adidas.com/us/Track/TrackWorkout?paramworkoutid='+str(workout['WorkoutInfo']['CompletedWorkoutID'])+'#Pace')
    #Need to find other activity type codes
    if workout['WorkoutInfo']['ActivityType'] == 1:
        activity = 'Running'
    etree.SubElement(trk, 'type').text = activity

    #add track points from from source
    trkseg = etree.SubElement(trk, 'trkseg')
    
    #Add GPS data points
    
    for point in workout['CompletedWorkoutDataPoints']:
        delta = timedelta(0, point['TimeFromStart'])
        trkpt = etree.SubElement(trkseg, 'trkpt')
        if gps_active:
            trkpt.set('lat', str(point['Latitude']))
            trkpt.set('lon', str(point['Longitude']))
            etree.SubElement(trkpt, 'ele').text = str(point['Altitude'])
        etree.SubElement(trkpt, 'time').text = (start + delta).isoformat()
    
    #write completed xml to file
    etree.ElementTree(gpx).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)

