# coding=utf-8
"""
 Copyright {2017} {Zhehua-Hu}
Version: v1.0.0
"""

# TODO:
# img_cnt bug
# updateGit comment


# reorderImgs()
# img_select

# img check: check in/out
# auto-check img adding to folder
# tag & version1

# read labelImg

# Debug
Debug = True
if Debug:
	pass
else:
	pass

# opencv
import cv2
# qt
from PyQt5.QtWidgets import QApplication, qApp,\
	QMainWindow, QWidget, QFileDialog, QGraphicsScene,\
	QGraphicsPixmapItem, QMessageBox, QAction

from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
# Misc
import sys
import os
import numpy as np
import platform
if "Windows" in platform.system():
	# Set it if need
	PRO_DIR = ur"H:\Clouds\pythonPro\A_Github\Enchain"
else:
	PRO_DIR = os.path.dirname(__file__)

file_path = os.path.join(PRO_DIR, "ui")
sys.path.append(file_path)
icon_path = os.path.join(PRO_DIR, "icons")

from mainwindow import Ui_MainWindow


class ImgList():
	"""
class: provide image list management
"""

	cur_idx = 0
	img_cnt = 0

	def __init__(self, folder):
		self.img_dirname = folder
		self.img_names = self.getContainedImgs(folder)
		print '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

	def getContainedImgs(self, folder):
		supported_img_suffix = ["BMP", "GIF", "JPG", "JPEG", "PNG", "TIFF", "PBM", "PGM", "PPM", "XBM", "XPM"]
		file_names = []
		for root, dirs, filenames in os.walk(folder):
			for filename in filenames:
				if not filename.startswith('.'): # not hiden file
					if filename.split(".")[-1].upper() in supported_img_suffix:
						file_names.append(filename)
						self.img_cnt += 1
		return file_names

	def FirstImg(self):
		return os.path.join(self.img_dirname, self.img_names[0])

	def nextImg(self):
		self.cur_idx += 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return os.path.join(self.img_dirname, self.img_names[self.cur_idx])

	def previousImg(self):
		self.cur_idx -= 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return os.path.join(self.img_dirname, self.img_names[self.cur_idx])

	def safeLimit(self, idx):
		if idx > self.img_cnt-1:
			return self.img_cnt-1
		elif idx < 0:
			return 0
		else:
			return idx

	def __repr__(self):
		print '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

class MainWindow(QMainWindow, Ui_MainWindow):
	"""
	Main Window in Enchain.
	"""
	def __init__(self, parent=None):
		super(QMainWindow, self).__init__()
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.setup()
		self.addEvent()


	def setup(self):
		self.setWindowIcon(QIcon(icon_path + ur"/EnchainLogoLittle.png"))
		self.gFileDialog = QFileDialog()
		self.graphicsscene = QGraphicsScene()
		self.graphicsView.setScene(self.graphicsscene)

		self.gImage = None
		self.gWorkspace = None
		self.gimg_list = None

		self.setupMenubar()
		self.setupToolbar()
		self.setupButtons()
		self.setupStatusbar()



	def setupMenubar(self):
		self.menubar.setNativeMenuBar(False)  # better for cross-platform


		self.actionQuit.setIcon(QIcon(icon_path + ur"/close-circle.svg"))
		self.actionQuit.setShortcut(ur"Ctrl+Q")
		self.actionQuit.setStatusTip(ur"Quit Software")
		self.actionQuit.triggered.connect(qApp.quit)

		self.actionClose.setStatusTip(ur"Close File")
		self.actionClose.triggered.connect(self.clearView)

		self.actionOpenImage.setStatusTip(ur"Open Single Image")
		self.actionOpenImage.triggered.connect(self.openImage)

		self.actionSaveImage.setStatusTip(ur"Save Image")
		self.actionSaveImage.triggered.connect(self.SaveImage)

		self.actionSaveImage.setStatusTip(ur"Open Folder Contains Images")
		self.actionOpenFolder.triggered.connect(self.setWorkspace)

	def setupToolbar(self):
		self.toolbar = self.addToolBar(ur"maintoolbar")

		actionPrevious = QAction(QIcon(icon_path + ur"/arrow-left-bold-circle.svg"), ur"Previous", self)
		actionPrevious.setShortcut(ur"Ctrl+LeftArrow")
		actionPrevious.triggered.connect(self.showPreviousImg)
		self.toolbar.addAction(actionPrevious)
		
		actionNext = QAction(QIcon(icon_path + ur"/arrow-right-bold-circle.svg"), ur"Next", self)
		actionNext.setShortcut(ur"Ctrl+N")
		actionNext.triggered.connect(self.showNextImg)
		self.toolbar.addAction(actionNext)
		
		actionSelect = QAction(QIcon(icon_path + ur"/check-circle.svg"), ur"Select", self)
		actionSelect.setShortcut(ur"Ctrl+Enter")
		actionSelect.triggered.connect(self.selectImg)
		self.toolbar.addAction(actionSelect)


	def setupButtons(self):
			pass

	def setupStatusbar(self):
		self.statusBar().showMessage("Ready")

	def addEvent(self):
		print("addEvent")

	def printToStatus(self, message):
		self.statusBar().showMessage(message)

	def openImage(self):
		if Debug:
			openImage_path = os.path.join(PRO_DIR, ur"test/img_folder")
		else:
			openImage_path = os.path.expanduser(ur"~")

		img_path = self.gFileDialog.getOpenFileName(self, ur"Open File", openImage_path)
		if img_path[0]:
			self.showImg(img_path[0])

	def showImg(self, img_path):
		self.gImage = cv2.imread(img_path)
		self.currentCvImage = None  # reset
		self.currentCvImage = self.gImage.copy()
		pixmap = QPixmap(img_path)
		self.updateView(pixmap)

	def getPixmap(self, img_path):
		self.gImage = cv2.imread(img_path)
		self.currentCvImage = None  # reset
		self.currentCvImage = self.gImage.copy()
		pixmap = QPixmap(img_path)
		return pixmap

	def updateView(self, qpixmap):
		self.clearView()
		viewWidth = self.graphicsView.frameGeometry().width()
		viewHeight = self.graphicsView.frameGeometry().height()
		pixRatioMap = qpixmap.scaled(viewWidth, viewHeight, Qt.KeepAspectRatio)
		pixItem = QGraphicsPixmapItem(pixRatioMap)
		self.graphicsscene.addItem(pixItem)
		self.graphicsscene.update()

	def clearView(self):
		items = self.graphicsscene.items()
		for item in items:
			self.graphicsscene.removeItem(item)

	def setWorkspace(self):
		if Debug:
			setWorkspace_path = os.path.join(PRO_DIR, ur"test/")
		else:
			setWorkspace_path = os.path.expanduser(ur"~")

		folder_path = self.gFileDialog.getExistingDirectory(self, ur"Open Folder", setWorkspace_path)
		if folder_path is not None:
			self.gWorkspace = folder_path

		self.gimg_list = ImgList(self.gWorkspace)
		# print(self.gimg_list)
		self.showImg(self.gimg_list.FirstImg())


	def showNextImg(self):
		print("showNextImg")
		self.showImg(self.gimg_list.nextImg())


	def showPreviousImg(self):
		print("showPreviousImg")
		self.showImg(self.gimg_list.previousImg())

	def selectImg(self):
		print("selectImg")
		pass


	def convert_CvImgToQPixmap(self, cvImage):
		height, width, dim = cvImage.shape
		bytesPerLine = dim * width
		qimg = QImage(cvImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
		return QPixmap.fromImage(qimg)

	def convert_CvImgToQImg(self, cvImage):
		height, width, dim = cvImage.shape
		bytesPerLine = dim * width
		qimg = QImage(cvImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
		return qimg

	def SaveImage(self):
		default_name = "test.jpg"
		try:
			if self.currentCvImage is not None:
				file = self.gFileDialog.getSaveFileName(self, "Save file", os.path.expanduser("~") + "/" + default_name)
				if file[0]:
					cv2.imwrite(file[0],self.currentCvImage)
			else:
				print("Empty!")
		except:
			print("No Image!")

	def getContainedFiles(self, folder):
		file_names = []
		for root, dirs, filenames in os.walk(folder):
			for filename in filenames:
				if not filename.startswith('.'): # not hiden file
					file_names.append(filename)
		return file_names


	def closeEvent(self, event):
		if Debug:
			pass
		else:
			reply = QMessageBox.question(self, "Message",
				"Are you sure to quit?", QMessageBox.Yes |
				QMessageBox.No, QMessageBox.No)

			if reply == QMessageBox.Yes:
				event.accept()
			else:
				event.ignore()





if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())
