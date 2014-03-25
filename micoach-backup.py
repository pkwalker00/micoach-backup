from PyQt4 import QtGui
from micoachUI import Ui_Form
from journalModel import JournalTableModel

class miCoachWindow(QtGui.QWidget, Ui_Form):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.journalData = [[26653305, 'Shamrock Run 2014', '2014-03-16', '08:20 AM', 'Running', '0:42:48', '5.11 mi', '08:22 min/mi', 0, 577], 
                [26653305, 'Shamrock Run 2014', '2014-03-16', '08:20 AM', 'Running', '0:42:48', '5.11 mi', '08:22 min/mi', 0, 577], 
                [26653305, 'Shamrock Run 2014', '2014-03-16', '08:20 AM', 'Running', '0:42:48', '5.11 mi', '08:22 min/mi', 0, 577], 
                [26653305, 'Shamrock Run 2014', '2014-03-16', '08:20 AM', 'Running', '0:42:48', '5.11 mi', '08:22 min/mi', 0, 577]]
        self.setTableModel()
    

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

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = miCoachWindow()
    ui.show()
    sys.exit(app.exec_())
