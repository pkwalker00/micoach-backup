# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'micoach.ui'
#
# Created: Tue Mar 25 18:41:03 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1072, 458)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        Form.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.emailEdit = QtGui.QLineEdit(self.splitter)
        self.emailEdit.setObjectName(_fromUtf8("emailEdit"))
        self.passwordEdit = QtGui.QLineEdit(self.splitter)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.loginButton = QtGui.QPushButton(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setAutoDefault(True)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.jsonButton = QtGui.QToolButton(self.splitter)
        self.jsonButton.setEnabled(False)
        self.jsonButton.setCheckable(True)
        self.jsonButton.setObjectName(_fromUtf8("jsonButton"))
        self.gpxButton = QtGui.QToolButton(self.splitter)
        self.gpxButton.setEnabled(False)
        self.gpxButton.setCheckable(True)
        self.gpxButton.setObjectName(_fromUtf8("gpxButton"))
        self.tcxButton = QtGui.QToolButton(self.splitter)
        self.tcxButton.setEnabled(False)
        self.tcxButton.setCheckable(True)
        self.tcxButton.setObjectName(_fromUtf8("tcxButton"))
        self.fileButton = QtGui.QToolButton(self.splitter)
        self.fileButton.setEnabled(False)
        self.fileButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        self.fileButton.setIcon(icon)
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.backupButton = QtGui.QPushButton(self.splitter)
        self.backupButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backupButton.sizePolicy().hasHeightForWidth())
        self.backupButton.setSizePolicy(sizePolicy)
        self.backupButton.setObjectName(_fromUtf8("backupButton"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(Form)
        self.cancelButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 2, 1, 1, 1)
        self.journalTable = QtGui.QTableView(Form)
        self.journalTable.setStyleSheet(_fromUtf8("alternate-background-color: rgb(170, 255, 255);"))
        self.journalTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.journalTable.setTabKeyNavigation(False)
        self.journalTable.setProperty("showDropIndicator", False)
        self.journalTable.setDragDropOverwriteMode(False)
        self.journalTable.setAlternatingRowColors(True)
        self.journalTable.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.journalTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.journalTable.setShowGrid(False)
        self.journalTable.setWordWrap(False)
        self.journalTable.setObjectName(_fromUtf8("journalTable"))
        self.journalTable.horizontalHeader().setStretchLastSection(True)
        self.journalTable.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.journalTable, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.emailEdit, self.passwordEdit)
        Form.setTabOrder(self.passwordEdit, self.loginButton)
        Form.setTabOrder(self.loginButton, self.jsonButton)
        Form.setTabOrder(self.jsonButton, self.gpxButton)
        Form.setTabOrder(self.gpxButton, self.tcxButton)
        Form.setTabOrder(self.tcxButton, self.fileButton)
        Form.setTabOrder(self.fileButton, self.backupButton)
        Form.setTabOrder(self.backupButton, self.journalTable)
        Form.setTabOrder(self.journalTable, self.cancelButton)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "micoach-backup", None))
        self.emailEdit.setPlaceholderText(_translate("Form", "email", None))
        self.passwordEdit.setPlaceholderText(_translate("Form", "password", None))
        self.loginButton.setText(_translate("Form", "Login", None))
        self.jsonButton.setText(_translate("Form", "JSON", None))
        self.gpxButton.setText(_translate("Form", "GPX", None))
        self.tcxButton.setText(_translate("Form", "TCX", None))
        self.backupButton.setText(_translate("Form", "Backup", None))
        self.cancelButton.setText(_translate("Form", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

