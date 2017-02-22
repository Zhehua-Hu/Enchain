# coding=utf-8
""" """

# opencv
import cv2
# qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import sys
import os
import numpy as np
import platform
if 'Windows' in platform.system():
	# Please set it
	PRO_DIR = r"H:\Clouds\pythonPro\A_Github\Enchain"
else:
	PRO_DIR = os.path.dirname(__file__)

file_path = os.path.join(PRO_DIR, "ui")
sys.path.append(file_path)
from mainwindow import Ui_MainWindow




class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.setup()
		self.addEvent()

	def setup(self):
		print('setup')
		self.fileDialog = QFileDialog()
		self.graphicsscene = QGraphicsScene()
		self.graphicsView.setScene(self.graphicsscene)

		self.image = None


	def addEvent(self):
		print('addEvent')
		self.pushButton_Open .clicked.connect(self.fileSelectBtnClickHandler)
		self.pushButton_Save.clicked.connect(self.saveBtnClickHandler)

	def fileSelectBtnClickHandler(self):
		print('clicked!')
		path = os.path.expanduser('~') + '/pictures/'
		print(path)
		file = self.fileDialog.getOpenFileName(self, "Open file", path)
		if file[0]:
			self.lineEdit.setText(file[0])
			self.opencPic(self.lineEdit.text())

	def opencPic(self, imgsrc):
		self.image = cv2.imread(imgsrc)
		# reset
		self.currentCvImage = None
		self.currentCvImage = self.image.copy()
		pixmap = QPixmap(imgsrc)
		self.updateImage(pixmap)

	def updateImage(self, qpixmap):
		self.deleteSceneItems()
		viewWidth = self.graphicsView.frameGeometry().width()
		viewHeight = self.graphicsView.frameGeometry().height()

		pixRatioMap = qpixmap.scaled(viewWidth, viewHeight, Qt.KeepAspectRatio)
		pixItem = QGraphicsPixmapItem(pixRatioMap)
		self.graphicsscene.addItem(pixItem)
		self.graphicsscene.update()

	def deleteSceneItems(self):
		items = self.graphicsscene.items()
		for item in items:
			self.graphicsscene.removeItem(item)


	def changeCvToQPixmap(self, cvImage):
		height, width, dim = cvImage.shape
		bytesPerLine = dim * width

		qimg = QImage(cvImage.data, width, height, bytesPerLine, QImage.Format_RGB888)

		return QPixmap.fromImage(qimg)


	def saveBtnClickHandler(self):

		try:
			if self.currentCvImage is not None:
				file = self.fileDialog.getSaveFileName(self, "Save file", os.path.expanduser('~') + '/home')
				if file[0]:
					cv2.imwrite(file[0],self.currentCvImage)
			else:
				print("Empty!")
		except:
			print("Error!")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())
