from PyQt4 import QtCore

class JournalTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, journal=[[]], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__journal = journal
        self.__headers = ['Workout ID', 'Name', 'Date', 'Time', 'Activity', 'Duration', 'Distance', 'Pace', 'Heart Rate', 'Calories']
        self.__checks = {}
    
    def rowCount(self, parent):
        return len(self.__journal)
    
    def columnCount(self, parent):
        return len(self.__journal[0])
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
    
    def checkState(self, index):
        if index in self.__checks:
            return self.__checks[index]
        else:
            return QtCore.Qt.Unchecked
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        
        row = index.row()
        column = index.column()
        
        if role == QtCore.Qt.DisplayRole:
            value = self.__journal[row][column]
            return value
        
        if role == QtCore.Qt.CheckStateRole:
            if column == 0:
                return self.checkState(index)
    
    def setData(self, index, value, role):
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            self.__checks[index] = value
            self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return QtCore.QAbstractTableModel.setData(self, index, value, role)
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
    
    def checkedItems(self):
        return [self.data(item) for item in self.__checks if self.__checks[item] == 2]
        
