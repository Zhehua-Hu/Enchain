# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 40, 551, 451))
        self.graphicsView.setObjectName("graphicsView")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(140, 550, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 510, 311, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_Open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Open.setGeometry(QtCore.QRect(380, 510, 99, 27))
        self.pushButton_Open.setObjectName("pushButton_Open")
        self.pushButton_Save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Save.setGeometry(QtCore.QRect(380, 550, 99, 27))
        self.pushButton_Save.setObjectName("pushButton_Save")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 25))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTool = QtWidgets.QMenu(self.menubar)
        self.menuTool.setObjectName("menuTool")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuManage = QtWidgets.QMenu(self.menubar)
        self.menuManage.setObjectName("menuManage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAuthor_Info = QtWidgets.QAction(MainWindow)
        self.actionAuthor_Info.setObjectName("actionAuthor_Info")
        self.actionAbout_Enchain = QtWidgets.QAction(MainWindow)
        self.actionAbout_Enchain.setObjectName("actionAbout_Enchain")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menuHelp.addAction(self.actionAuthor_Info)
        self.menuHelp.addAction(self.actionAbout_Enchain)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())
        self.menubar.addAction(self.menuManage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Open.setText(_translate("MainWindow", "Open"))
        self.pushButton_Save.setText(_translate("MainWindow", "Save"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTool.setTitle(_translate("MainWindow", "Tools"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuManage.setTitle(_translate("MainWindow", "Manage"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionAuthor_Info.setText(_translate("MainWindow", "Author Info"))
        self.actionAbout_Enchain.setText(_translate("MainWindow", "About Enchain"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))

