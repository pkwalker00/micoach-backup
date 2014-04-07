#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore
from micoachUI import Ui_Form
from journalModel import JournalTableModel
import libmicoach.user, configparser, os, platform

class miCoachWindow(QtGui.QWidget, Ui_Form):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.journalData = [[]]
        self.user = libmicoach.user.miCoachUser()
        self.setTableModel()
        self.loginButton.clicked.connect(self.login)
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.worker.loginComplete.connect(self.loggedIn)
        self.worker.loginFailed.connect(self.loginFail)
        self.worker.progress.connect(self.onProgress)
        self.worker.backupComplete.connect(self.backupComplete)
        self.jsonButton.clicked.connect(self.configUpdate)
        self.gpxButton.clicked.connect(self.configUpdate)
        self.tcxButton.clicked.connect(self.configUpdate)
        self.fileButton.clicked.connect(self.folderChooser)
        self.backupButton.clicked.connect(self.backup)
        self.cancelButton.clicked.connect(self.onCancel)

    def setTableModel(self):
        self.model = JournalTableModel(self.journalData)
        self.journalTable.setModel(self.model)
        self.journalTable.setColumnWidth(1, 250)
        self.journalTable.setColumnWidth(3, 70)
        self.journalTable.setColumnWidth(4, 125)
        self.journalTable.setColumnWidth(5, 65)
        self.journalTable.setColumnWidth(6, 65)
        self.journalTable.setColumnWidth(8, 75)
        self.journalTable.setColumnWidth(9, 60)
    
    def initializeConfig(self):
        self.config = configparser.ConfigParser()
        self.backupConfig = os.path.join(os.path.expanduser('~'), 'miCoach', self.user.username, 'backup.cfg')
        if not os.path.exists(os.path.join(os.path.expanduser('~'), 'miCoach', self.user.username)):
            try:
                os.makedirs(os.path.join(os.path.expanduser('~'), 'miCoach', self.user.username))
            except:
                pass
        try:
            with open(self.backupConfig): pass
        except IOError:
            self.config['General'] = {}
            self.saveConfig()
        self.config.read(self.backupConfig)
        self.json = self.config['General'].getboolean('json', False)
        self.gpx = self.config['General'].getboolean('gpx', True)
        self.tcx = self.config['General'].getboolean('tcx', True)
        self.folder = self.config['General'].get('folder',  os.path.join(os.path.expanduser('~'), 'miCoach'))
        self.jsonButton.setChecked(self.json)
        self.gpxButton.setChecked(self.gpx)
        self.tcxButton.setChecked(self.tcx)
        self.configUpdate()

    def configUpdate(self):
        if self.sender() == self.jsonButton:
            self.json = self.sender().isChecked()
        if self.sender() == self.gpxButton:
            self.gpx = self.sender().isChecked()
        if self.sender() == self.tcxButton:
            self.tcx = self.sender().isChecked()
        
        if not self.json and not self.gpx and not self.tcx:
            QtGui.QMessageBox.warning(self, "Invalid Configuration", "You must choose at least one backup option")
            self.sender().setChecked(not self.sender().isChecked())
            self.configUpdate()
            return

        self.config.set('General', 'json', str(self.json))
        self.config.set('General', 'gpx', str(self.gpx))
        self.config.set('General', 'tcx', str(self.tcx))
        self.config.set('General',  'folder', self.folder)
        self.saveConfig()

    def saveConfig(self):
        with open(self.backupConfig, 'w') as configfile:
            self.config.write(configfile)

    def login(self):
        if self.user.loggedin:
            self.logout()
        else:
            if self.emailEdit.text() == '':
                QtGui.QMessageBox.warning(self, "No Email Address", "You must enter an email address")
                self.emailEdit.setFocus()
                return
            if self.passwordEdit.text() == '':
                QtGui.QMessageBox.warning(self, "No Password", "You must enter a password")
                self.passwordEdit.setFocus()
                return
            self.emailEdit.setEnabled(False)
            self.passwordEdit.setEnabled(False)
            self.loginButton.setEnabled(False)
            self.thread.start()
            self.progressBar.setRange(0, 0)
            QtCore.QMetaObject.invokeMethod(self.worker, 'login', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(libmicoach.user.miCoachUser, self.user), 
                                                                        QtCore.Q_ARG(str, self.emailEdit.text()), QtCore.Q_ARG(str, self.passwordEdit.text()))
        
    def loginFail(self):
        self.progressBar.setRange(0, 1)
        self.emailEdit.setEnabled(True)
        self.passwordEdit.setEnabled(True)
        self.loginButton.setEnabled(True)
        QtGui.QMessageBox.warning(self, "Login Failed", "Login Failed:Please try again")
        self.emailEdit.setText('')
        self.emailEdit.setFocus()
        self.passwordEdit.setText('')
        self.user.logout()
        self.thread.quit()

    def loggedIn(self):
        self.progressBar.setRange(0, 1)
        self.loginButton.setText("Logout")
        self.initializeConfig()
        self.loginButton.setEnabled(True)
        self.journalData = self.user.journalList()
        self.setTableModel()
        self.jsonButton.setEnabled(True)
        self.gpxButton.setEnabled(True)
        self.tcxButton.setEnabled(True)
        self.fileButton.setEnabled(True)
        self.backupButton.setEnabled(True)
        self.thread.quit()
    
    def logout(self):
        self.user.logout()
        self.journalData = [[]]
        self.setTableModel()
        self.emailEdit.setEnabled(True)
        self.emailEdit.setText('')
        self.emailEdit.setFocus()
        self.passwordEdit.setEnabled(True)
        self.passwordEdit.setText('')
        self.loginButton.setText('Login')
        self.jsonButton.setEnabled(False)
        self.gpxButton.setEnabled(False)
        self.tcxButton.setEnabled(False)
        self.fileButton.setEnabled(False)
        self.backupButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        self.jsonButton.setChecked(False)
        self.gpxButton.setChecked(False)
        self.tcxButton.setChecked(False)
    
    def folderChooser(self):
        self.folder = os.path.join(QtGui.QFileDialog.getExistingDirectory(self, 'Choose a folder', os.path.expanduser('~'), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks), 'miCoach')
        self.config.set('General', 'folder', self.folder)
        self.saveConfig()

    def backup(self):
        if len(self.model.checkedItems()) == 0:
            QtGui.QMessageBox.warning(self, "No Workout Selected", "You must choose at least one workout to backup.")
            return
        self.backupButton.setEnabled(False)
        self.cancelButton.setEnabled(True)
        self.loginButton.setEnabled(False)
        self.gpxButton.setEnabled(False)
        self.jsonButton.setEnabled(False)
        self.tcxButton.setEnabled(False)
        self.fileButton.setEnabled(False)
        count = 0
        for workout in self.model.checkedItems():
            count = count + 1
            if self.json:
                count = count + 1
            if self.gpx:
                count = count + 1
            if self.tcx:
                count = count + 1
        self.progressBar.setRange(0, count)
        options = {'json':self.json, 'gpx':self.gpx, 'tcx':self.tcx, 'folder':self.folder}
        selectedWorkouts = self.model.checkedItems()
        self.thread.start()
        QtCore.QMetaObject.invokeMethod(self.worker, 'backupWorkouts', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(libmicoach.user.miCoachUser, 
                                                                self.user), QtCore.Q_ARG(list, selectedWorkouts), QtCore.Q_ARG(dict, options))
    
    def backupComplete(self):
        self.thread.quit()
        self.cancelButton.setEnabled(False)
        self.backupButton.setEnabled(True)
        self.loginButton.setEnabled(True)
        self.jsonButton.setEnabled(True)
        self.gpxButton.setEnabled(True)
        self.tcxButton.setEnabled(True)
        self.fileButton.setEnabled(True)
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(0)
    
    def onProgress(self):
        newValue = self.progressBar.value() + 1
        self.progressBar.setValue(newValue)
    
    def onCancel(self):
        self.worker.stop()

class Worker(QtCore.QObject):
    loginComplete = QtCore.pyqtSignal()
    loginFailed = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal()
    backupComplete = QtCore.pyqtSignal()
    
    @QtCore.pyqtSlot(libmicoach.user.miCoachUser, str, str)
    def login(self, user, email, password):
        user.login(email, password)
        if user.loggedin:
            self.loginComplete.emit()
        else:
            self.loginFailed.emit()
    
    @QtCore.pyqtSlot(libmicoach.user.miCoachUser, list, dict)
    def backupWorkouts(self, user, list, options):
        self._isRunning = True
        for workoutID in list:
            if not self._isRunning:
                self.backupComplete.emit()
                return
            QtGui.QApplication.processEvents()
            try:
                workout = user.getWorkout(workoutID)
                filename = workout.suggestFilename()
                if platform.system() == 'Windows':
                    filename = filename.replace(':', '-')
            except:
                print('Problem retrieving workout ID: %s'% workoutID)
                self._isRunning = False
            self.progress.emit()
            if options['json'] and self._isRunning:
                jsonPath = os.path.join(options['folder'], user.username, 'json', workout.year(), workout.month())
                if not os.path.exists(jsonPath):
                    try:
                        os.makedirs(jsonPath)
                    except:
                        pass
                workout.writeJson(os.path.join(jsonPath, filename + '.json'))
                self.progress.emit()
                
            if options['gpx'] and self._isRunning:
                gpxPath = os.path.join(options['folder'], user.username, 'gpx', workout.year(), workout.month())
                if not os.path.exists(gpxPath):
                    try:
                        os.makedirs(gpxPath)
                    except:
                        pass
                workout.writeGpx(os.path.join(gpxPath, filename + '.gpx'))
                self.progress.emit()
            if options['tcx'] and self._isRunning:
                tcxPath = os.path.join(options['folder'], user.username, 'tcx', workout.year(), workout.month())
                if not os.path.exists(tcxPath):
                    try:
                        os.makedirs(tcxPath)
                    except:
                        pass
                workout.writeTcx(os.path.join(tcxPath, filename + '.tcx'))
                self.progress.emit()
        self.backupComplete.emit()

    def stop(self):
        self._isRunning = False
    
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = miCoachWindow()
    ui.show()
    sys.exit(app.exec_())
