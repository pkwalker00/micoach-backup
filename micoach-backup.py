from PyQt4 import QtGui, QtCore
from micoachUI import Ui_Form
from journalModel import JournalTableModel
import libmicoach.user

class miCoachWindow(QtGui.QWidget, Ui_Form):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.journalData = [[]]
        self.user = libmicoach.user.miCoachUser()
        self.setTableModel()
        self.loginButton.clicked.connect(self.login)
        self.thread = Thread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.worker.loginComplete.connect(self.loggedIn)
        self.worker.loginFailed.connect(self.loginFail)

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

    def login(self):
        if self.emailEdit.text() == '':
            QtGui.QMessageBox.warning(self, "No Email Address", "You must enter an email address")
            self.emailEdit.setFocus()
            return
        if self.passwordEdit.text() == '':
            QtGui.QMessageBox.warning(self, "No Password", "You must enter a password")
            self.passwordEdit.setFocus()
            return
        self.progressBar.setRange(0, 0)
        QtCore.QMetaObject.invokeMethod(self.worker, 'login', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(libmicoach.user.miCoachUser, self.user), QtCore.Q_ARG(str, self.emailEdit.text()), QtCore.Q_ARG(str, self.passwordEdit.text()))

    def loginFail(self):
        self.progressBar.setRange(0, 1)
        QtGui.QMessageBox.warning(self, "Login Failed", "Login Failed:Please try again")
        self.emailEdit.setText('')
        self.emailEdit.setFocus()
        self.passwordEdit.setText('')
        self.user.logout()

    def loggedIn(self):
        self.progressBar.setRange(0, 1)
        self.journalData = self.user.journalList()
        self.setTableModel()

class Worker(QtCore.QObject):
    loginComplete = QtCore.pyqtSignal()
    loginFailed = QtCore.pyqtSignal()

    @QtCore.pyqtSlot(libmicoach.user.miCoachUser, str, str)
    def login(self, user, email, password):
        user.login(email, password)
        if user.loggedin:
            self.loginComplete.emit()
        else:
            self.loginFailed.emit()
            return
    
class Thread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def start(self):
        QtCore.QThread.start(self)
    def run(self):
        QtCore.QThread.run(self)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = miCoachWindow()
    ui.show()
    sys.exit(app.exec_())
