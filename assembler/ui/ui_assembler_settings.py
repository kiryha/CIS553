# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\projects\master\CS553\dev\assembler\ui\ui_assembler_settings.ui'
#
# Created: Sun Dec  5 20:05:03 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(400, 186)
        self.verticalLayout = QtGui.QVBoxLayout(Settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_5 = QtGui.QSplitter(Settings)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.btnPickProject = QtGui.QPushButton(self.splitter_5)
        self.btnPickProject.setMinimumSize(QtCore.QSize(150, 0))
        self.btnPickProject.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnPickProject.setObjectName("btnPickProject")
        self.linProjectFolder = QtGui.QLineEdit(self.splitter_5)
        self.linProjectFolder.setObjectName("linProjectFolder")
        self.verticalLayout.addWidget(self.splitter_5)
        self.splitter = QtGui.QSplitter(Settings)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtGui.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label.setObjectName("label")
        self.linVersionedPages = QtGui.QLineEdit(self.splitter)
        self.linVersionedPages.setObjectName("linVersionedPages")
        self.verticalLayout.addWidget(self.splitter)
        self.splitter_2 = QtGui.QSplitter(Settings)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_2 = QtGui.QLabel(self.splitter_2)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_2.setObjectName("label_2")
        self.linFinalPages = QtGui.QLineEdit(self.splitter_2)
        self.linFinalPages.setObjectName("linFinalPages")
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter_3 = QtGui.QSplitter(Settings)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.label_3 = QtGui.QLabel(self.splitter_3)
        self.label_3.setMinimumSize(QtCore.QSize(150, 0))
        self.label_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_3.setObjectName("label_3")
        self.linPDFfiles = QtGui.QLineEdit(self.splitter_3)
        self.linPDFfiles.setObjectName("linPDFfiles")
        self.verticalLayout.addWidget(self.splitter_3)
        self.splitter_4 = QtGui.QSplitter(Settings)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.label_4 = QtGui.QLabel(self.splitter_4)
        self.label_4.setMinimumSize(QtCore.QSize(150, 0))
        self.label_4.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_4.setObjectName("label_4")
        self.linSQLfile = QtGui.QLineEdit(self.splitter_4)
        self.linSQLfile.setObjectName("linSQLfile")
        self.verticalLayout.addWidget(self.splitter_4)
        self.btnSaveSettings = QtGui.QPushButton(Settings)
        self.btnSaveSettings.setMinimumSize(QtCore.QSize(0, 35))
        self.btnSaveSettings.setObjectName("btnSaveSettings")
        self.verticalLayout.addWidget(self.btnSaveSettings)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Edit Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPickProject.setText(QtGui.QApplication.translate("Settings", "Pick Project Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Settings", "Versioned Pages", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Settings", "Final Pages", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Settings", "PDF files", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Settings", "SQL file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveSettings.setText(QtGui.QApplication.translate("Settings", "Save Settings", None, QtGui.QApplication.UnicodeUTF8))

