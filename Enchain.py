# coding=utf-8
"""
 Copyright {2017} {Zhehua-Hu}
Version: v1.0.0
"""

# TODO:
# cross-platform run
# setSavefolder
# video_slice(name format)
# img_select
# img_delete



# img check: check in/out
"""
    read_folder
        img & xml
        draw rect on img
        show img
    ok->done
    wrong->error-select
        ->(TODO)redraw
        rewrite xml
"""

# tag & version1
# read labelImg

# video_select
# reorderImgs()
# auto-check img adding to folder
# dataset manage & stat

# std libs
import sys
import os
import numpy as np

"""
Global Macros
"""
import platform
if "Windows" in platform.system():
	# Set it if need
	# PRO_DIR = r"H:\Clouds\pythonPro\A_Github\Enchain"
	PRO_DIR = os.environ.get("ENCHAINPATH")
else:
	# PRO_DIR = r"/home/zhehua/pythonPro/A_Github/Enchain"
	# PRO_DIR = os.environ.get("ENCHAINPATH")
	PRO_DIR = os.path.dirname(__file__)
print PRO_DIR
Debug = True
gSupported_img_suffix = ["BMP", "GIF", "JPG", "JPEG", "PNG", "TIFF", "PBM", "PGM", "PPM", "XBM", "XPM"]



# OpenCV
import cv2
# PyQt
from PyQt5.QtWidgets import QApplication, qApp,\
	QMainWindow, QWidget, QFileDialog, QGraphicsScene,\
	QGraphicsPixmapItem, QMessageBox, QAction

from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt


file_path = os.path.join(PRO_DIR, "ui")
sys.path.append(file_path)
icon_path = os.path.join(PRO_DIR, "icons")

from ui.mainwindow import Ui_MainWindow




class ImgList():
	"""
class: provide image list management
"""

	cur_idx = 0
	img_cnt = 0

	def __init__(self, folder):
		self.img_dirname = folder
		self.imgs_path, self.img_cnt = self.getContainedImgs(folder, type="Recursive")

	def getContainedImgs(self, folder, type="NotRecursive"):
		imgs_path = []
		ret_cnt = 0
		for root, dirs, filenames in os.walk(folder):
			if type == "Recursive":
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if filename.split(".")[-1].upper() in gSupported_img_suffix:
							imgs_path.append(os.path.join(root, filename))
							ret_cnt += 1
			else:
				for item in filenames:
					if not item.startswith('.'): # not hiden file
						if item.split(".")[-1].upper() in gSupported_img_suffix:
							imgs_path.append(os.path.join(root, item))
				ret_cnt = len(imgs_path)
				break
		return imgs_path, ret_cnt


	def FirstImg(self):
		return os.path.join(self.imgs_path[0])

	def nextImg(self):
		self.cur_idx += 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return os.path.join(self.imgs_path[self.cur_idx])

	def previousImg(self):
		self.cur_idx -= 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return os.path.join(self.imgs_path[self.cur_idx])

	def safeLimit(self, idx):
		if idx > self.img_cnt-1:
			return self.img_cnt-1
		elif idx < 0:
			return 0
		else:
			return idx

	def __repr__(self):
		for item in self.__dict__.items():
			print("%s : %s" % item)


class MainWindow(QMainWindow, Ui_MainWindow):
	"""
Main Window in Enchain.
"""
	def __init__(self, parent=None):
		super(QMainWindow, self).__init__()
		QMainWindow.__init__(self, parent)
		self.setupUi(self)

		self.setWindowIcon(QIcon(icon_path + u"/EnchainLogoLittle.png"))
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


		self.actionQuit.setIcon(QIcon(icon_path + u"/close-circle.svg"))
		self.actionQuit.setShortcut(u"Ctrl+Q")
		self.actionQuit.setStatusTip(u"Quit Software")
		self.actionQuit.triggered.connect(qApp.quit)

		self.actionClose.setStatusTip(u"Close File")
		self.actionClose.triggered.connect(self.clearView)

		self.actionOpenImage.setStatusTip(u"Open Single Image")
		self.actionOpenImage.triggered.connect(self.openImage)

		self.actionSaveImage.setStatusTip(u"Save Image")
		self.actionSaveImage.triggered.connect(self.SaveImage)

		self.actionSaveImage.setStatusTip(u"Open Folder Contains Images")
		self.actionOpenFolder.triggered.connect(self.setWorkspace)

	def setupToolbar(self):
		self.toolbar = self.addToolBar(u"maintoolbar")

		actionPrevious = QAction(QIcon(icon_path + u"/arrow-left-bold-circle.svg"), u"Previous", self)
		actionPrevious.setShortcut(u"Ctrl+LeftArrow")
		actionPrevious.triggered.connect(self.showPreviousImg)
		self.toolbar.addAction(actionPrevious)
		
		actionNext = QAction(QIcon(icon_path + u"/arrow-right-bold-circle.svg"), u"Next", self)
		actionNext.setShortcut(u"Ctrl+N")
		actionNext.triggered.connect(self.showNextImg)
		self.toolbar.addAction(actionNext)
		
		actionSelect = QAction(QIcon(icon_path + u"/check-circle.svg"), u"Select", self)
		actionSelect.setShortcut(u"Ctrl+Enter")
		actionSelect.triggered.connect(self.selectImg)
		self.toolbar.addAction(actionSelect)

	def setupButtons(self):
			pass

	def setupStatusbar(self):
		self.statusBar().showMessage("Ready")


	def printToStatus(self, message):
		self.statusBar().showMessage(message)

	def openImage(self):
		if Debug:
			openImage_path = os.path.join(PRO_DIR, u"test/img_folder")
		else:
			openImage_path = os.path.expanduser(u"~")

		img_path = self.gFileDialog.getOpenFileName(self, u"Open File", openImage_path)
		if img_path[0]:
			self.showImg(img_path[0])

	def showImg(self, img_path):
		print(img_path)
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
			setWorkspace_path = os.path.join(PRO_DIR, u"test/")
		else:
			setWorkspace_path = os.path.expanduser(u"~")

		folder_path = self.gFileDialog.getExistingDirectory(self, u"Open Folder", setWorkspace_path)
		if folder_path is not None:
			self.gWorkspace = folder_path

		self.gimg_list = ImgList(self.gWorkspace)
		self.showImg(self.gimg_list.FirstImg())

	def showNextImg(self):
		print("showNextImg")
		self.showImg(self.gimg_list.nextImg())


	def showPreviousImg(self):
		print("showPreviousImg")
		self.showImg(self.gimg_list.previousImg())

	def selectImg(self):
		print("selectImg")


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

	def getContainedFiles(self, folder, type="NotRecursive"):
		file_names = []
		ret_cnt = 0
		for root, dirs, filenames in os.walk(folder):
			if type == "Recursive":
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						file_names.append(os.path.join(root, filename))
						ret_cnt += 1
			else:
				for item in filenames:
					if not item.startswith('.'): # not hiden file
						file_names.append(os.path.join(root, item))
				ret_cnt = len(file_names)
				break
		return file_names, ret_cnt

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
