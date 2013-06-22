from datetime import datetime
from lxml import etree
import libmicoach.xmlassist as xa
from libmicoach import gpx, tcx

class Workout(object):
    def __init__(self, content):
        self.xml = content
        self.id = xa.search(self.xml, 'CompletedWorkoutID')
        self.date = datetime.strptime(xa.search(self.xml, 'StartDateTime'), '%Y-%m-%dT%H:%M:%S')
        self.name = xa.search(self.xml, 'WorkoutName')

    def writeXml(self, filename):
        etree.ElementTree(self.xml).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)

    def writeTcx(self, filename):
        tcx.writeTcx(filename, self.xml)

    def writeGpx(self, filename):
        gpx.writeGpx(filename, self.xml)

class WorkoutList(object):
    
    def __init__(self, data):
        self.content = []
        self.log = []
        for w in data.iter(xa.nodestring(data, 'WorkoutLog')):
            start = datetime.strptime(w.find(xa.findstring(data, 'StartDate')).text[:19], '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(w.find(xa.findstring(data, 'StopDate')).text[:19], '%Y-%m-%dT%H:%M:%S')
        
            d = int(w.find(xa.findstring(data, 'Distance')).find(xa.findstring(data, 'Value')).text)
            if d > 1000:
                distance = '%.1f km' % (d/1000.)
            else:
                distance = '%d m' % (d)
            id = int(w.find(xa.findstring(data, 'WorkoutId')).text)
            name = w.find(xa.findstring(data, 'Name')).text
            activity = w.find(xa.findstring(data, 'ActivityType')).text
            type = w.find(xa.findstring(data, 'CompletedWorkoutType')).text
            time = str(end-start)
            hr = int(w.find(xa.findstring(data, 'AvgHR')).find(xa.findstring(data, 'Value')).text)
            pace = float(w.find(xa.findstring(data, 'AvgPace')).find(xa.findstring(data, 'Value')).text)
            
            self.log.append([id, name, str(start)[:10], str(start)[-8:][:5],  activity, type, time, distance, hr, str('{0:.2f}'.format(round(pace, 2)))])
            
            self.content.append({'id': id,
                                 'name': name,
                                 'date': str(start),
                                 'activity': activity,
                                 'type': type,
                                 'time': time,
                                 'distance': distance,
                                 'hr': hr,
                                 'pace': pace
                                })

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        for line in self.content:
            yield line

    def __repr__(self):
        return 'WorkoutList: contains (%d) workouts' % (len(self.content))

    def display(self):
        for w in self.content:
            print('{:d}\t{:s}\t{:s}\{:s}\{:s}\t{:s}\t{:s}\t{:d}\t{:n}'.format(w['id'],w['name'],w['date'],w['activity'],w['type'],w['time'],w['distance'],w['hr'],w['pace']))
