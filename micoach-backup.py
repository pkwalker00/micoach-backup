#!/usr/bin/env python3

from gi.repository import Gtk, GObject
from libmicoach.user import *
from math import floor
from datetime import datetime
import configparser, os,  calendar

class BackupWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Adidas miCoach" + u" \u00a9" + " Backup")
        self.connect("delete_event", Gtk.main_quit)
        self.set_border_width(10)
        self.set_default_size(1200, 600)
    
        self.config = configparser.ConfigParser()
        self.config.read('backup.cfg')
        
        self.user = miCoachUser()
        
        self.xml = self.config["General"].getboolean("xml", False)
        self.tcx = self.config["General"].getboolean("tcx",  True)
        self.gpx = self.config["General"].getboolean("gpx",  True)
        self.folder = self.config["General"].get("folder",  os.path.expanduser("~") +"/miCoach")
        
        self.to_convert = []
        
        self.grid = Gtk.Grid()
        self.add(self.grid)
        
        self.create_login_bar()
        self.create_backup_options()
        self.create_progress_bar()
        self.create_workout_list()
        self.option_enable_toggle()
        self.show_all()

    def create_backup_options(self):
        box = Gtk.Box()
        
        label_convert = Gtk.Label("Backup Formats & Location:")
        
        self.button_xml = Gtk.ToggleButton(label = "XML")
        self.button_xml.set_active(self.xml)
        self.button_xml.connect("toggled", self.on_xml_toggled)
        self.button_xml.set_tooltip_text("Save raw xml sent from miCoach")
        
        self.button_gpx = Gtk.ToggleButton(label = "GPX")
        self.button_gpx.set_active(self.gpx)
        self.button_gpx.connect("toggled", self.on_gpx_toggled)
        self.button_gpx.set_tooltip_text("Creates the smallest file. Ideal for GPS only workouts")
        
        self.button_tcx = Gtk.ToggleButton(label = "TCX")
        self.button_tcx.set_active(self.tcx)
        self.button_tcx.connect("toggled", self.on_tcx_toggled)
        self.button_tcx.set_tooltip_text("Use this if your workout has Heart Rate info")
        
        self.button_files = Gtk.Button(label = None, image = Gtk.Image(stock = Gtk.STOCK_OPEN))
        self.button_files.connect("clicked", self.on_files_clicked)
        self.button_files.set_tooltip_text("Change the default folder to save workout data")
        
        box.pack_start(label_convert, True, True, 0)
        box.pack_start(self.button_xml, True, True, 5)
        box.pack_start(self.button_gpx, True, True, 5)
        box.pack_start(self.button_tcx, True, True, 5)
        box.pack_start(self.button_files, True, True, 5)
        
        self.grid.attach(box, 1, 0, 1, 1)
        
        box2 = Gtk.Box()
        self.button_backup = Gtk.Button("  Backup  ")
        self.button_backup.connect("clicked", self.on_backup_clicked)
        box2.pack_start(self.button_backup, True, True, 5)
        box2.set_hexpand(True)
        self.button_backup.set_sensitive(False)
        self.grid.attach(box2, 2, 0, 1, 1)

    def create_login_bar(self):
        box = Gtk.Box()
        
        label_email = Gtk.Label("E-mail:")
        self.entry_email = Gtk.Entry()
        label_pass = Gtk.Label("Password:")
        self.entry_pass = Gtk.Entry(visibility = False)
        self.button_login = Gtk.Button("  Login  ")
        self.button_login.connect("clicked", self.on_login_clicked)
        
        box.pack_start(label_email, True, True, 0)
        box.pack_start(self.entry_email, True, True, 5)
        box.pack_start(label_pass, True, True, 0)
        box.pack_start(self.entry_pass, True, True, 5)
        box.pack_start(self.button_login, True, True, 5)
        self.grid.attach(box, 0, 0, 1, 1)
    
    def create_workout_list(self):
        box = Gtk.Box()
        scrollbox = Gtk.ScrolledWindow()
        scrollbox.set_vexpand(True)
        scrollbox.set_hexpand(True)
        box.pack_start(scrollbox, True, True, 5)
        
        self.listmodel = Gtk.ListStore(bool, int, str, str, str, str, str, str, str, str, str, str)
        self.view = Gtk.TreeView(model = self.listmodel)
        self.button_checkall = Gtk.CheckButton()
        self.button_checkall.show()
        columns = ['Workout ID', 'Name', 'Date', 'Time', 'Activity', 'Type', 'Duration', 'Distance', 'Pace', 'Heart Rate']
        toggle_cell = Gtk.CellRendererToggle()
        toggle_cell.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn(None, toggle_cell, active=0)
        column_toggle.set_widget(self.button_checkall)
        column_toggle.set_clickable(True)
        column_toggle.connect("clicked", self.on_column_clicked)
        self.view.append_column(column_toggle)
        for item in columns:
            cell = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(item, cell, text = columns.index(item)+1, background=11)
            self.view.append_column(col)
        
        scrollbox.add(self.view)
        box.set_vexpand(True)
        #box.set_hexpand(True)
        self.grid.attach(box, 0, 1, 10, 1)

    def create_progress_bar(self):
        box = Gtk.Box()
        self.progressbar = Gtk.ProgressBar()
        box.pack_start(self.progressbar, True, True, 5)
        self.progressbar.set_hexpand(True)
        self.button_cancel = Gtk.Button("Cancel")
        self.button_cancel.connect("clicked",  self.on_cancel_clicked)
        self.button_cancel.set_sensitive(False)
        box.pack_start(self.button_cancel, False, True, 5)
        self.grid.attach(box, 0, 2, 10, 1)

    def on_files_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Choose a folder", self, Gtk.FileChooserAction.SELECT_FOLDER, 
                                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.folder = dialog.get_filename()
            self.config.set("General", "folder", self.folder)
            self.save_config()
            print(self.folder)
        
        dialog.destroy()

    def on_backup_clicked(self, button):
        if len(self.to_convert) == 0:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No workout selected")
            dialog.format_secondary_text("You must have at least one workout selected.")
            dialog.run()
            dialog.destroy()
            return
        self.button_cancel.set_sensitive(True)
        increment = self.find_progress_increment()
        self.backup = self.backup_workouts(self.to_convert, increment)
        self.id = GObject.idle_add(self.backup.__next__)

    def on_login_clicked(self, button):
        if not self.user.logged_in:
            email = self.entry_email.get_text()
            password = self.entry_pass.get_text()
            if email == "" or password == "":
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Missing Credentials")
                dialog.format_secondary_text("You must enter both your e-mail and password")
                dialog.run()
                dialog.destroy()
                return
            self.user.login(email, password)
            if self.user.logged_in:
                self.button_backup.set_sensitive(True)
                self.entry_email.set_sensitive(False)
                self.entry_pass.set_sensitive(False)
                button.set_label("  Logout  ")
                self.option_enable_toggle()
                self.populate_workouts()
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Login Failed")
                dialog.format_secondary_text("Did you type the correct e-mail and password?")
                dialog.run()
                dialog.destroy()
        else:
            self.user.logout()
            self.user = miCoachUser()
            self.entry_email.set_text("")
            self.entry_email.set_sensitive(True)
            self.entry_pass.set_text("")
            self.entry_pass.set_sensitive(True)
            button.set_label("  Login  ")
            self.button_backup.set_sensitive(False)
            self.option_enable_toggle()
            self.listmodel.clear()
    
    def populate_workouts(self):
        self.workout_list = self.prepare_content(self.user.workouts.get_Content())
        for item in self.workout_list:
                self.listmodel.append(item)
        self.view = Gtk.TreeView(model = self.listmodel)
    
    def on_column_clicked(self, widget):
        if self.user.logged_in:
            if self.button_checkall.get_active():
                path = 0
                for item in self.listmodel:
                    item[0] = True
                    self.on_cell_toggled(item[0], path)
                    path = path + 1
                self.button_checkall.set_active(False)
            else:
                path = 0
                for item in self.listmodel:
                    item[0] = False
                    self.on_cell_toggled(item[0], path)
                    path = path + 1
                self.button_checkall.set_active(True)

    def on_cell_toggled(self, widget, path):
        self.listmodel[path][0] = not self.listmodel[path][0]
        if self.listmodel[path][0]:
            self.to_convert.append({"id": str(self.listmodel[path][1]), "name": self.listmodel[path][2], 
                                                    "date": self.listmodel[path][3], "time": self.listmodel[path][4]})
        else:
            self.to_convert = [x for x in self.to_convert if str(self.listmodel[path][1]) not in x["id"]]
    
    def on_xml_toggled(self, button):
        if self.xml:
            if not self.gpx and not self.tcx:
                self.xml =  not self.xml
                button.set_active(True)
                self.choose_backup_dialog()
                return
        self.xml =  not self.xml
        self.config.set("General", "xml", str(self.xml))
        self.save_config()
    
    def on_gpx_toggled(self,  button):
        if self.gpx:
            if not self.xml and not self.tcx:
                self.gpx =  not self.gpx
                button.set_active(True)
                self.choose_backup_dialog()
                return
        self.gpx = not self.gpx
        self.config.set("General", "gpx", str(self.gpx))
        self.save_config()

    def on_tcx_toggled(self, button):
        if self.tcx:
            if not self.gpx and not self.xml:
                self.tcx =  not self.tcx
                button.set_active(True)
                self.choose_backup_dialog()
                return
        self.tcx = not self.tcx
        self.config.set("General", "tcx", str(self.tcx))
        self.save_config()

    def prepare_content(self, dict):
        prepared_list = []
        row_color = False
        for item in dict:
            new_item = []
            new_item.append(False)
            new_item.append(item['id'])
            new_item.append(item['name'])
            new_item.append(item['start'].strftime('%Y-%m-%d'))
            new_item.append(item['start'].strftime('%I:%M %p'))
            new_item.append(item['activity'])
            new_item.append(item['type'])
            new_item.append(str(item['duration']))
            d = item['distance']
            
            mpk = item['pace']/60
            if self.user.unitofdistance == 1:
                if d > 1000:
                    new_item.append('{0:.2f} km'.format(round(d/1000,2)))
                else:
                    new_item.append('{:d} m'.format(d))
                min = floor(mpk)
                sec = int((mpk-min)*60)
                new_item.append('{:d}:{:02d} min/km'.format(min, sec))
            else:
                if d > 1610:
                    new_item.append('{0:.2f} mi'.format(round(d/1609.34,2)))
                else:
                    new_item.append('{0:.2f} yd'.format(round(d*1.09361, 0)))
                mpm = mpk * 1.609344
                min = floor(mpm)
                sec = int((mpm -  min) * 60)
                new_item.append('{:d}:{:02d} min/mi'.format(min, sec))
            new_item.append('{0:d}'.format(item['hr']))
            prepared_list.append(new_item)
            if row_color:
                new_item.append("#DAF4F7")
                row_color = not row_color
            else:
                new_item.append("#FFFFFF")
                row_color = not row_color
        return prepared_list
    
    def save_config(self):
        with open("backup.cfg", "w") as configfile:
            self.config.write(configfile)

    def choose_backup_dialog(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Invalid Selection")
        dialog.format_secondary_text("You must have at least one backup option selected.")
        dialog.run()
        dialog.destroy()
    
    def find_progress_increment(self):
        count = 0
        for item in self.to_convert:
            count = count + 1
            if self.xml:
                count = count + 1
            if self.gpx:
                count = count + 1
            if self.tcx:
                count = count + 1
        
        return 1/count

    def backup_workouts(self, selection, increment):
        for workout in selection:
            year = workout["date"][:4]
            month = calendar.month_name[int(workout["date"][5:-3])]
            time = datetime.strptime(workout["time"], "%I:%M %p").strftime("%H:%M")
            filename = workout["date"] + "T" + time  +"-" + workout["name"]
            workout_convert = self.user.schedule.getWorkout(workout["id"])
            self.update_progress(increment)
            yield True
            if self.xml:
                save_to_folder = self.folder + "/"  + self.user.screenname + "/xml/" + year + "/" + workout["date"][5:-3]+"-"+ month
                if not os.path.exists(save_to_folder):
                    try:
                        os.makedirs(save_to_folder)
                    except:
                        pass
                workout_convert.writeXml(save_to_folder+"/"+filename+".xml")
                self.update_progress(increment)
                yield True
            if self.gpx:
                save_to_folder = self.folder + "/"  + self.user.screenname + "/gpx/" + year + "/" + workout["date"][5:-3]+"-"+ month
                if not os.path.exists(save_to_folder):
                    try:
                        os.makedirs(save_to_folder)
                    except:
                        pass
                workout_convert.writeGpx(save_to_folder+"/"+filename+".gpx")
                self.update_progress(increment)
                yield True
            if self.tcx:
                save_to_folder = self.folder + "/"  + self.user.screenname + "/tcx/" + year + "/" + workout["date"][5:-3]+"-"+ month
                if not os.path.exists(save_to_folder):
                    try:
                        os.makedirs(save_to_folder)
                    except:
                        pass
                workout_convert.writeTcx(save_to_folder+"/"+filename+".tcx")
                self.update_progress(increment)
                yield True

        if self.button_checkall.get_active():
            self.button_checkall.set_active(False)
        path = 0
        for item in self.listmodel:
            item[0] = True
            self.on_cell_toggled(item[0], path)
            path = path + 1

        GObject.source_remove(self.id)
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Backup Complete!")
        dialog.format_secondary_text("Saved to: "+ self.folder+"/"+self.user.screenname+"/")
        dialog.run()
        dialog.destroy()
        self.button_cancel.set_sensitive(False)
        self.progressbar.set_fraction(0)
        yield False
    
    def update_progress(self, increment):
        self.progressbar.set_fraction(self.progressbar.get_fraction() + increment)
    
    def on_cancel_clicked(self, button):
        GObject.source_remove(self.id)
        self.progressbar.set_fraction(0)
        button.set_sensitive(False)

    def option_enable_toggle(self):
        self.button_xml.set_sensitive(not self.button_xml.get_sensitive())
        self.button_gpx.set_sensitive(not self.button_gpx.get_sensitive())
        self.button_tcx.set_sensitive(not self.button_tcx.get_sensitive())
        self.button_files.set_sensitive(not self.button_files.get_sensitive())
        
win = BackupWindow()
Gtk.main()
