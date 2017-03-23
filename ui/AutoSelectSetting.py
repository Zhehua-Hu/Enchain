# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AutoSelectSetting.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AutoSelectSetting(object):
    def setupUi(self, AutoSelectSetting):
        AutoSelectSetting.setObjectName("AutoSelectSetting")
        AutoSelectSetting.resize(386, 219)
        self.buttonBoxQuery = QtWidgets.QDialogButtonBox(AutoSelectSetting)
        self.buttonBoxQuery.setGeometry(QtCore.QRect(20, 181, 341, 31))
        self.buttonBoxQuery.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxQuery.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxQuery.setObjectName("buttonBoxQuery")
        self.gridLayoutWidget = QtWidgets.QWidget(AutoSelectSetting)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 40, 160, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(AutoSelectSetting)
        self.buttonBoxQuery.accepted.connect(AutoSelectSetting.accept)
        self.buttonBoxQuery.rejected.connect(AutoSelectSetting.reject)
        QtCore.QMetaObject.connectSlotsByName(AutoSelectSetting)

    def retranslateUi(self, AutoSelectSetting):
        _translate = QtCore.QCoreApplication.translate
        AutoSelectSetting.setWindowTitle(_translate("AutoSelectSetting", "Dialog"))
        self.label.setText(_translate("AutoSelectSetting", "Stride"))

