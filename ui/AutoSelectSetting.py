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
        AutoSelectSetting.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(AutoSelectSetting)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(AutoSelectSetting)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 20, 171, 52))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout.addWidget(self.spinBox)

        self.retranslateUi(AutoSelectSetting)
        self.buttonBox.accepted.connect(AutoSelectSetting.accept)
        self.buttonBox.rejected.connect(AutoSelectSetting.reject)
        QtCore.QMetaObject.connectSlotsByName(AutoSelectSetting)

    def retranslateUi(self, AutoSelectSetting):
        _translate = QtCore.QCoreApplication.translate
        AutoSelectSetting.setWindowTitle(_translate("AutoSelectSetting", "Dialog"))
        self.label.setText(_translate("AutoSelectSetting", "Stride"))

