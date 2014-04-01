miCoach Backup
=====

**miCoach backup** is a tool to save your workouts from [Adidas miCoach] to your computer.

Description
----

**miCoach backup** contains two things:

  - the beginning of a Python implementation of *Adidas miCoach* API 
  - a small GUI for selecting and saving you workouts

This was forked from Manual Vonthron's micoach-backup.  I ported it to python 3 and removed the use Mariano Reingar's SimpleXML library in favor of lxml.  I added writeGpx and a working version of writeTcx for export options. This program uses the Google Maps api to replace miCoaches rounded elevations with more accurate information.

I have completely rewritten this using the requests library and json instead of the xml.  I have also rewritten the gui using Qt4 Designer. 


Usage 
-----
**Requirements**
  - a computer and a *miCoach* account...

  - [Python 3+](http://www.python.org)
  - [PyQt4](http://www.riverbankcomputing.com/software/pyqt/intro)
  - [Python Requests](https://github.com/kennethreitz/requests)
  - [lxml](http://lxml.de/)

**Installation**

No installation needed. Just move the program wherever you like.

**Usage**

1. Run `micoach-backup.py`
2. Enter your *miCoach* credentials
3. Choose any combination of backup options "json", "gpx", or "tcx"
4. Optional Choose the folder you want to save in. (Step 3 and 4 DO NOT need to be repeated each use)
3. Select workouts to be downloaded


Screenshot
----

![miCoach backup](http://s21.postimg.org/ar5i9vucn/Screenshot_from_2014_03_31_21_15_49.png)

Licensing
---------

This program and its documentation are released under the terms of the
BSD license.

XML manipulation library (simplexml.py) by Mariano Reingar, LGPL license

----
2012, Manuel Vonthron <manuel.vonthron@acadis.org>,
2013, Patrick Walker

  [Adidas miCoach]: http://www.micoach.com/ 

