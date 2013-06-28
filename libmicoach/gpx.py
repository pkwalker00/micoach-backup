from datetime import datetime, timedelta
from dateutil.parser import parse
import dateutil.tz
import libmicoach.xmlassist as xa
from lxml import etree

def writeGpx(filename, content):
    """Convert miCoach xml to GPX format"""
    
    xml = content 
    gps_active = xa.search(xml, 'GPSActive')
    utc = xa.search(xml, 'StartDateTimeUTC')

    local = xa.search(xml, 'StartDateTime')

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
    etree.SubElement(metadata, 'name').text = xa.search(xml, 'WorkoutName')
    etree.SubElement(metadata, 'time').text = str(start)
    
    if gps_active == 'true':
        bounds = etree.SubElement(metadata, 'bounds')

        lat = []
        lon = []
        for point in xml.iter(xa.nodestring(xml, 'CompletedWorkoutDataPoint')):
            lat.append(float(point.find(xa.findstring(xml, 'Latitude')).text))
            lon.append(float(point.find(xa.findstring(xml, 'Longitude')).text))

        bounds.set("minlat", str(min(lat)))
        bounds.set("minlon", str(min(lon)))
        bounds.set("maxlat", str(max(lat)))
        bounds.set("maxlon", str(max(lon)))
    
    #Setup basic Track	
    trk = etree.SubElement(gpx, 'trk')
    cmt = etree.SubElement(trk, 'cmt')
    cmt.text = xa.search(xml, 'UserNote')

    etree.SubElement(trk, 'src').text = 'Adidas miCoach' + u' \u00a9' 
    etree.SubElement(trk, 'link').set('href', 'https://micoach.adidas.com/us/Track/TrackWorkout?paramworkoutid='+xa.search(xml, 'CompletedWorkoutID')+'#Pace')
    etree.SubElement(trk, 'type').text = xa.search(xml,'ActivityType')

    #add track points from from source
    trkseg = etree.SubElement(trk, 'trkseg')
    
    #Add GPS data points
    
    for point in xml.iter(xa.nodestring(xml, 'CompletedWorkoutDataPoint')):
        delta = timedelta(0, float(point.find(xa.findstring(xml, 'TimeFromStart')).text))
        trkpt = etree.SubElement(trkseg, 'trkpt')
        if gps_active == 'true':
            trkpt.set('lat', point.find(xa.findstring(xml, 'Latitude')).text)
            trkpt.set('lon', point.find(xa.findstring(xml, 'Longitude')).text)
            etree.SubElement(trkpt, 'ele').text = point.find(xa.findstring(xml, 'Altitude')).text
        etree.SubElement(trkpt, 'time').text = (start + delta).isoformat()
    
    #write completed xml to file
    etree.ElementTree(gpx).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)

