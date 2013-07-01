miCoach Backup
=====

**miCoach backup** is a tool to save your workouts from [Adidas miCoach] to your computer.

Description
----

**miCoach backup** contains two things:

  - the beginning of a Python implementation of *Adidas miCoach* API 
  - a small GUI for selecting and saving you workouts

This was forked from Manual Vonthron's micoach-backup.  I ported it to python 3 and removed the use Mariano Reingar's SimpleXML library in favor of lxml.  I added writeGpx and a working version of writeTcx for export options.  The PySide based GUI has been removed for my own crude Gtk+ 3 GUI. The "xml" backup option will save the raw xml file that is delivered from the [Adidas miCoach] website.


Usage 
-----
**Requirements**
  - a computer and a *miCoach* account...

  - [Python 3+](http://www.python.org)
  - [Gtk+ 3](http://www.gtk.org/)
  - [PyGObject](https://wiki.gnome.org/PyGObject)
  - [lxml](http://lxml.de/)

**Installation**

No installation needed. Just move the program wherever you like.

**Usage**

1. Run `micoach-backup`
2. Enter your *miCoach* credentials
3. Choose any combination of backup options "xml", "gpx", or "tcx" (Choose tcx if you use Heart Rate Monitor"
4. Optional Choose the folder you want to save in. (Step 3 and 4 DO NOT need to be repeated each use)
3. Select workouts to be downloaded


Screenshot
----

![miCoach backup](http://s15.postimg.org/8wow61gi3/Screenshot_from_2013_06_27_15_49_55.png)

Licensing
---------

This program and its documentation are released under the terms of the
BSD license.

XML manipulation library (simplexml.py) by Mariano Reingar, LGPL license

----
2012, Manuel Vonthron <manuel.vonthron@acadis.org>,
2013, Patrick Walker

  [Adidas miCoach]: http://www.micoach.com/ 

