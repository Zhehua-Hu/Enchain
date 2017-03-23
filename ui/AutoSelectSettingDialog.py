#!/usr/bin/env python
# coding=utf-8
"""
Provide AutoSelectSettingDialog Class
"""


from PyQt5.QtWidgets import QDialog, QSpinBox

from AutoSelectSetting import Ui_AutoSelectSetting

class AutoSelectSettingDialog(QDialog, Ui_AutoSelectSetting):

	def __init__(self, parent=None):
		QDialog.__init__(self)
		self.setupUi(self)

		self.buttonBoxQuery.accepted.connect(self.setValue)
		self.buttonBoxQuery.rejected.connect(self.close)

		self.value = 1
		self.value_has_set = False

	def setValue(self):
		self.value_has_set = True


	def getValue(self):
		return self.value_has_set, self.spinBox.value()