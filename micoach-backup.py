# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'micoach.ui'
#
# Created: Tue Mar 18 20:03:57 2014
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
        Form.resize(970, 458)
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
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.jsonButton = QtGui.QToolButton(self.splitter)
        self.jsonButton.setCheckable(True)
        self.jsonButton.setObjectName(_fromUtf8("jsonButton"))
        self.gpxButton = QtGui.QToolButton(self.splitter)
        self.gpxButton.setCheckable(True)
        self.gpxButton.setObjectName(_fromUtf8("gpxButton"))
        self.tcxButton = QtGui.QToolButton(self.splitter)
        self.tcxButton.setCheckable(True)
        self.tcxButton.setObjectName(_fromUtf8("tcxButton"))
        self.fileButton = QtGui.QToolButton(self.splitter)
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
        self.listView = QtGui.QListView(Form)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.gridLayout.addWidget(self.listView, 1, 0, 1, 2)
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 24)
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

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

