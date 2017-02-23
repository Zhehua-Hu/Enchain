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
        self.graphicsView.setGeometry(QtCore.QRect(10, 30, 720, 480))
        self.graphicsView.setObjectName("graphicsView")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(470, 540, 231, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(60, 540, 381, 27))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 25))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTool = QtWidgets.QMenu(self.menubar)
        self.menuTool.setObjectName("menuTool")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuPipeline = QtWidgets.QMenu(self.menubar)
        self.menuPipeline.setObjectName("menuPipeline")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAuthor_Info = QtWidgets.QAction(MainWindow)
        self.actionAuthor_Info.setObjectName("actionAuthor_Info")
        self.actionAbout_Enchain = QtWidgets.QAction(MainWindow)
        self.actionAbout_Enchain.setObjectName("actionAbout_Enchain")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOnline_Help = QtWidgets.QAction(MainWindow)
        self.actionOnline_Help.setObjectName("actionOnline_Help")
        self.actionCheck_Update = QtWidgets.QAction(MainWindow)
        self.actionCheck_Update.setObjectName("actionCheck_Update")
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.actionRename = QtWidgets.QAction(MainWindow)
        self.actionRename.setObjectName("actionRename")
        self.actionOpenFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenFolder.setObjectName("actionOpenFolder")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpenVideo = QtWidgets.QAction(MainWindow)
        self.actionOpenVideo.setObjectName("actionOpenVideo")
        self.actionOpenImage = QtWidgets.QAction(MainWindow)
        self.actionOpenImage.setObjectName("actionOpenImage")
        self.actionSaveImage = QtWidgets.QAction(MainWindow)
        self.actionSaveImage.setObjectName("actionSaveImage")
        self.actionCutImage = QtWidgets.QAction(MainWindow)
        self.actionCutImage.setObjectName("actionCutImage")
        self.actionDatasetInput = QtWidgets.QAction(MainWindow)
        self.actionDatasetInput.setObjectName("actionDatasetInput")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSetUserInfo = QtWidgets.QAction(MainWindow)
        self.actionSetUserInfo.setObjectName("actionSetUserInfo")
        self.menuHelp.addAction(self.actionOnline_Help)
        self.menuHelp.addAction(self.actionAuthor_Info)
        self.menuHelp.addAction(self.actionCheck_Update)
        self.menuHelp.addAction(self.actionInfo)
        self.menuTool.addAction(self.actionRename)
        self.menuTool.addAction(self.actionCutImage)
        self.menuFile.addAction(self.actionOpenFolder)
        self.menuFile.addAction(self.actionOpenVideo)
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addAction(self.actionSaveImage)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionQuit)
        self.menuPipeline.addAction(self.actionSetUserInfo)
        self.menuPipeline.addAction(self.actionDatasetInput)
        self.menubar.addAction(self.menuPipeline.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Enchain"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTool.setTitle(_translate("MainWindow", "Tools"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuPipeline.setTitle(_translate("MainWindow", "Pipeline"))
        self.actionAuthor_Info.setText(_translate("MainWindow", "Author Info"))
        self.actionAbout_Enchain.setText(_translate("MainWindow", "About Enchain"))
        self.actionOpen.setText(_translate("MainWindow", "OpenFolder"))
        self.actionExit.setText(_translate("MainWindow", "Quit"))
        self.actionOnline_Help.setText(_translate("MainWindow", "Online Help"))
        self.actionCheck_Update.setText(_translate("MainWindow", "Check Update"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
        self.actionRename.setText(_translate("MainWindow", "Rename"))
        self.actionOpenFolder.setText(_translate("MainWindow", "OpenFolder"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionOpenVideo.setText(_translate("MainWindow", "OpenVideo"))
        self.actionOpenImage.setText(_translate("MainWindow", "OpenImage"))
        self.actionSaveImage.setText(_translate("MainWindow", "SaveImage"))
        self.actionCutImage.setText(_translate("MainWindow", "CutImage"))
        self.actionDatasetInput.setText(_translate("MainWindow", "DatasetInput"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionSetUserInfo.setText(_translate("MainWindow", "SetUserInfo"))
