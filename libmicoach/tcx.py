from datetime import datetime, timedelta
from dateutil.parser import parse
import dateutil.tz
from lxml import etree

def writeTcx(filename, workout):
    """Convert miCoach xml to TCX format"""

    utc = workout['WorkoutInfo']['StartDateTimeUTC'][:-1]

    local = workout['WorkoutInfo']['StartDateTime'][:-1]

    #Set UTC start time for workout
    start = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S")	

    #Use computer's local timezone to correct UTC for daylight if needed
    delta = datetime.strptime(local, "%Y-%m-%dT%H:%M:%S") - datetime.now()
    datetz = dateutil.tz.tzlocal().tzname(datetime.now() + delta)
    
    if parse(local + datetz).timetuple().tm_isdst != 0:
        start = start - timedelta(hours=1)

    #Find what sensors were used
    if 'GPSActive' in workout['WorkoutInfo']:
        gps_active = workout['WorkoutInfo']['GPSActive']
    else:
        gps_active = False
    hrm_active = 'Value' in workout['WorkoutInfo']['AvgHR']
    footpod_active = 'Value' in workout['WorkoutInfo']['AvgStrideRate']

    #create tcx container
    xmlns = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    xsd = 'http:/www.w3.org/2001Schema'
    NSMAP = {None: xmlns, 'xsi': xsi, 'xsd': xsd}

    tcx = etree.Element('TrainingCenterDatabase', nsmap=NSMAP) 

    activities = etree.SubElement(tcx, 'Activities')
    activity = etree.SubElement(activities, 'Activity',  Sport=workout['WorkoutInfo']['ActivityType'])
    etree.SubElement(activity, 'WorkoutName').text = workout['WorkoutInfo']['WorkoutName']
    etree.SubElement(activity, 'Id').text = str(start)

    lap = etree.SubElement(activity, 'Lap')
    lap.set('StartTime', str(start))
    etree.SubElement(lap, 'TotalTimeSeconds').text = str(workout['WorkoutInfo']['TotalTime'])
    if 'Value' in workout['WorkoutInfo']['TotalDistance']:
        etree.SubElement(lap, 'DistanceMeters').text = str(workout['WorkoutInfo']['TotalDistance']['Value'])
    else:
        etree.SubElement(lap, 'DistanceMeters').text = '0'
    if 'Value' in workout['WorkoutInfo']['TotalCalories']:
        etree.SubElement(lap, 'Calories').text = str(workout['WorkoutInfo']['TotalCalories']['Value'])
    else:
        etree.SubElement(lap, 'Calories').text = '0'
    
    if hrm_active:
        avghrbpm = etree.SubElement(lap, 'AverageHeartRateBpm')
        etree.SubElement(avghrbpm, 'Value').text = str(workout['WorkoutInfo']['AvgHR']['Value'])
        maxhrbpm = etree.SubElement(lap, 'MaximumHeartRateBpm')
        etree.SubElement(maxhrbpm, 'Value').text = str(workout['WorkoutInfo']['PeakHR']['Value'])

    if footpod_active:
        avgcadence = etree.SubElement(lap,  'AverageCadence')
        etree.SubElement(avgcadence, 'Value').text = str(workout['WorkoutInfo']['AvgStrideRate']['Value'])
    
    #Setup basic Track	
    track = etree.SubElement(lap,'Track')

    #Add GPS and/or HRM data points
    for point in workout['CompletedWorkoutDataPoints']:
        if 'TimeFromStart' in point:
            delta = timedelta(0, point['TimeFromStart'])
        else:
            delta = timedelta(0, 0)
        trackpoint = etree.SubElement(track, 'Trackpoint')
        etree.SubElement(trackpoint, 'Time').text  = (start + delta).strftime("%Y-%m-%dT%H:%M:%SZ")
        if gps_active:			        
            position = etree.SubElement(trackpoint, 'Position')
            etree.SubElement(position, 'LatitudeDegrees').text = str(point['Latitude'])
            etree.SubElement(position, 'LongitudeDegrees').text = str(point['Longitude'])
            etree.SubElement(trackpoint, 'AltitudeMeters').text = str(point['Altitude'])
        if footpod_active:
            etree.SubElement(trackpoint, 'DistanceMeters').text = str(point['Distance'])
            etree.SubElement(trackpoint, 'Cadence').text = str(point['StrideRate'])
        if hrm_active:
            hrbpm = etree.SubElement(trackpoint, 'HeartRateBpm', attrib={'{'+xsi+'}type': 'HeartRateInBeatsPerMinute_t'})
            etree.SubElement(hrbpm, 'Value').text = str(point['HeartRate'])

    #Write Completed tcx file
    etree.ElementTree(tcx).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)
