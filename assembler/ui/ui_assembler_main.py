# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\projects\master\CS553\dev\assembler\ui\ui_assembler_main.ui'
#
# Created: Wed Nov 24 12:41:15 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Assembler(object):
    def setupUi(self, Assembler):
        Assembler.setObjectName("Assembler")
        Assembler.resize(810, 708)
        self.centralwidget = QtGui.QWidget(Assembler)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabPages = QtGui.QTableView(self.groupBox)
        self.tabPages.setObjectName("tabPages")
        self.verticalLayout.addWidget(self.tabPages)
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.btnDownVersion = QtGui.QPushButton(self.splitter)
        self.btnDownVersion.setObjectName("btnDownVersion")
        self.btnUpVersion = QtGui.QPushButton(self.splitter)
        self.btnUpVersion.setObjectName("btnUpVersion")
        self.verticalLayout.addWidget(self.splitter)
        self.btnPublish = QtGui.QPushButton(self.groupBox)
        self.btnPublish.setObjectName("btnPublish")
        self.verticalLayout.addWidget(self.btnPublish)
        self.btnReload = QtGui.QPushButton(self.groupBox)
        self.btnReload.setObjectName("btnReload")
        self.verticalLayout.addWidget(self.btnReload)
        self.splitter_2 = QtGui.QSplitter(self.groupBox)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.chbSelected = QtGui.QCheckBox(self.splitter_2)
        self.chbSelected.setMaximumSize(QtCore.QSize(100, 16777215))
        self.chbSelected.setChecked(True)
        self.chbSelected.setObjectName("chbSelected")
        self.btnSendPublished = QtGui.QPushButton(self.splitter_2)
        self.btnSendPublished.setObjectName("btnSendPublished")
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter_3 = QtGui.QSplitter(self.groupBox)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.linPDFVersion = QtGui.QLineEdit(self.splitter_3)
        self.linPDFVersion.setMaximumSize(QtCore.QSize(75, 16777215))
        self.linPDFVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.linPDFVersion.setObjectName("linPDFVersion")
        self.btnGeneratePDF = QtGui.QPushButton(self.splitter_3)
        self.btnGeneratePDF.setObjectName("btnGeneratePDF")
        self.verticalLayout.addWidget(self.splitter_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.grp_images = QtGui.QGroupBox(self.centralwidget)
        self.grp_images.setObjectName("grp_images")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grp_images)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labPage = QtGui.QLabel(self.grp_images)
        self.labPage.setText("")
        self.labPage.setObjectName("labPage")
        self.verticalLayout_2.addWidget(self.labPage)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.grp_images)
        Assembler.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Assembler)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        Assembler.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Assembler)
        self.statusbar.setObjectName("statusbar")
        Assembler.setStatusBar(self.statusbar)
        self.actionDocumentation = QtGui.QAction(Assembler)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionSettings = QtGui.QAction(Assembler)
        self.actionSettings.setObjectName("actionSettings")
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuEdit.addAction(self.actionSettings)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Assembler)
        QtCore.QMetaObject.connectSlotsByName(Assembler)

    def retranslateUi(self, Assembler):
        Assembler.setWindowTitle(QtGui.QApplication.translate("Assembler", "Book Assembler", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Assembler", "Pages", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDownVersion.setText(QtGui.QApplication.translate("Assembler", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpVersion.setText(QtGui.QApplication.translate("Assembler", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPublish.setText(QtGui.QApplication.translate("Assembler", "Publish Current Version", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReload.setText(QtGui.QApplication.translate("Assembler", "Reload Pages", None, QtGui.QApplication.UnicodeUTF8))
        self.chbSelected.setText(QtGui.QApplication.translate("Assembler", "SEL", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSendPublished.setText(QtGui.QApplication.translate("Assembler", "Send Published Versions", None, QtGui.QApplication.UnicodeUTF8))
        self.linPDFVersion.setText(QtGui.QApplication.translate("Assembler", "01", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGeneratePDF.setText(QtGui.QApplication.translate("Assembler", "Generate PDF file", None, QtGui.QApplication.UnicodeUTF8))
        self.grp_images.setTitle(QtGui.QApplication.translate("Assembler", "Page Prewiew", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("Assembler", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("Assembler", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDocumentation.setText(QtGui.QApplication.translate("Assembler", "Documentation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("Assembler", "Modify Settings", None, QtGui.QApplication.UnicodeUTF8))

