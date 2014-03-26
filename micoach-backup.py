from PyQt4 import QtGui
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
        try:
            self.user.login(self.emailEdit.text(), self.passwordEdit.text())
            self.journalData = self.user.journalList()
            self.setTableModel()
        except:
            QtGui.QMessageBox.warning(self, "Login Failed", "Login Failed:Please try again")
            self.emailEdit.setText('')
            self.emailEdit.setFocus()
            self.passwordEdit.setText('')
            self.user.logout()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = miCoachWindow()
    ui.show()
    sys.exit(app.exec_())
