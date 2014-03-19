from datetime import datetime, timedelta
from dateutil.parser import parse
import dateutil.tz
from lxml import etree

def writeGpx(filename, workout):
    """Convert miCoach json to GPX format"""
    
    #Find what sensors were used
    if 'GPSActive' in workout['WorkoutInfo']:
        gps_active = workout['WorkoutInfo']['GPSActive']
    else:
        gps_active = False
    hrm_active = 'Value' in workout['WorkoutInfo']['AvgHR']
    footpod_active = 'Value' in workout['WorkoutInfo']['AvgStrideRate']
    
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
    xmlns = 'http://www.topografix.com/GPX/1/1'
    gpxtpx = 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'
    NSMAP = {None: xmlns, 'gpxtpx': gpxtpx}
    gpx = etree.Element('gpx', creator='micoach-backup', version='1.1', nsmap=NSMAP)

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
    etree.SubElement(trk, 'name').text = workout['WorkoutInfo']['WorkoutName']
    cmt = etree.SubElement(trk, 'cmt')
    if 'UserNote' in workout['WorkoutInfo']:
        cmt.text = workout['WorkoutInfo']['UserNote']

    etree.SubElement(trk, 'src').text = 'Adidas miCoach' + u' \u00a9' 
    etree.SubElement(trk, 'link').set('href', 'https://micoach.adidas.com/us/Track/TrackWorkout?paramworkoutid='+str(workout['WorkoutInfo']['CompletedWorkoutID'])+'#Pace')

    #Determine ActivityType from code
    activityType = workout['WorkoutInfo']['ActivityType']
    if activityType == 1:
        activity = 'Running'
    if activityType == 2:
        activity = 'Walking'
    if activityType == 3:
        activity = 'Cycling'
    if activityType == 14:
        activity = 'Nordic Skiing'
    if activityType == 999:
        activity = 'Other'
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
        else:
            trkpt.set('lat', '0.000000')
            trkpt.set('lon', '0.000000')
        etree.SubElement(trkpt, 'time').text = (start + delta).strftime("%Y-%m-%dT%H:%M:%SZ")
        if hrm_active or footpod_active:
            extensions = etree.SubElement(trkpt, 'extensions')
            gpxtpx = etree.SubElement(extensions, '{%s}TrackPointExtension' % NSMAP['gpxtpx'], nsmap=NSMAP)
        if hrm_active:
            #etree.SubElement(extensions, 'heartrate').text = str(point['HeartRate'])
            etree.SubElement(gpxtpx, '{%s}hr' % NSMAP['gpxtpx'], nsmap = NSMAP).text = str(point['HeartRate'])
        if footpod_active:
            etree.SubElement(extensions, 'cadence').text = str(point['StrideRate'])
            etree.SubElement(gpxtpx, '{%s}cad' % NSMAP['gpxtpx'], nsmap = NSMAP).text = str(point['StrideRate'])
    
    #write completed xml to file
    etree.ElementTree(gpx).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)

