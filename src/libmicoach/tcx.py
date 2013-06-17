from datetime import datetime, timedelta
from dateutil.parser import parse
import dateutil.tz 
import libmicoach.xmlassist as xa
from lxml import etree

def writeTcx(filename, content):
    """Convert miCoach xml to TCX format"""
	
    #parse xml content with lxml
    xml = content
	
    utc = xa.search(xml, 'StartDateTimeUTC')

    local = xa.search(xml, 'StartDateTime')

    #Set UTC start time for workout
    start = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S")	

    #Use computer's local timezone to correct UTC for daylight if needed
    delta = datetime.strptime(local, "%Y-%m-%dT%H:%M:%S") - datetime.now()
    datetz = dateutil.tz.tzlocal().tzname(datetime.now() + delta)
    
    if parse(local + datetz).timetuple().tm_isdst != 0:
        start = start - timedelta(hours=1)

    gps_active = xa.search(xml, 'GPSActive')
    hr_active = int(xa.findvalue(xml, 'AvgHR'))

    #create tcx container
    xmlns = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    xsd = 'http:/www.w3.org/2001Schema'
    NSMAP = {None: xmlns, 'xsi': xsi, 'xsd': xsd}

    tcx = etree.Element('TrainingCenterDatabase', nsmap=NSMAP) 
	
    activities = etree.SubElement(tcx, 'Activities')
    activity = etree.SubElement(activities, 'Activity')
    etree.SubElement(activity, 'Sport').text = xa.search(xml, 'ActivityType')
    etree.SubElement(activity, 'Id').text = str(start)
	
    lap = etree.SubElement(activity, 'Lap')
    lap.set('StartTime', str(start))
    etree.SubElement(lap, 'TotalTimeSeconds').text = xa.search(xml,'TotalTime')
    etree.SubElement(lap, 'DistanceMeters').text = xa.findvalue(xml, 'TotalDistance') 
    etree.SubElement(lap, 'Calories').text = xa.findvalue(xml, 'TotalCalories')
    if hr_active != 0:
        avghrbpm = etree.SubElement(lap, 'AverageHeartRateBpm')
        etree.SubElement(avghrbpm, 'Value').text = xa.findvalue(xml, 'AvgHR')
        maxhrbpm = etree.SubElement(lap, 'MaximumHeartRateBpm')
        etree.SubElement(maxhrbpm, 'Value').text = xa.findvalue(xml, 'PeakHR')
    
    #Setup basic Track	
    track = etree.SubElement(lap,'Track')

    #Add GPS and/or HRM data points
    for point in xml.iter(xa.nodestring(xml, 'CompletedWorkoutDataPoint')):
        delta = timedelta(0, float(point.find(xa.findstring(xml, 'TimeFromStart')).text))
        trackpoint = etree.SubElement(track, 'Trackpoint')
        etree.SubElement(trackpoint, 'Time').text  = (start + delta).isoformat()
        if gps_active == "true":			
            position = etree.SubElement(trackpoint, 'Position')
            etree.SubElement(position, 'LatitudeDegrees').text = point.find(xa.findstring(xml, 'Latitude')).text
            etree.SubElement(position, 'LongitudeDegrees').text = point.find(xa.findstring(xml, 'Longitude')).text
            etree.SubElement(trackpoint, 'AltitudeMeters').text = point.find(xa.findstring(xml, 'Altitude')).text
            etree.SubElement(trackpoint, 'DistanceMeters').text = point.find(xa.findstring(xml, 'Distance')).text
        if hr_active != 0:
            hrbpm = etree.SubElement(trackpoint, 'HeartRateBpm', attrib={'{'+xsi+'}type': 'HeartRateInBeatsPerMinute_t'})
            # hrbpm.set('HeartRateInBeatsPerMinute_t')
            etree.SubElement(hrbpm, 'Value').text = point.find(xa.findstring(xml, 'HeartRate')).text

    #Write Completed tcx file
    etree.ElementTree(tcx).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)
