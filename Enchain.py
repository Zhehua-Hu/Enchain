# coding=utf-8
"""
 Copyright {2017} {Zhehua-Hu}
Version: v1.0.0
"""

# TODO[BUG]:
# open img folder&exit will cause error
# video_show format bug

"""
# read labelImg use drawing!
# img check: check in/out
    read_folder
        img & xml
        draw rect on img
        show img
    ok->done
    wrong->error-select
        ->(TODO)redraw
        rewrite xml

# img_delete will reorder img

# 标准化
#add icon,tip,shortcut
#show status
# unicode

# 可用第一版
git tag & version1
cross-platform run
	## windows[ok]
	## Ubuntu[skip]

# TODO
# dataset manage & stat

可有可无
# auto-check img adding to folder
# video_select( video player)
"""

# std libs
import sys
import os
import shutil
import numpy as np

"""
Global Macros
"""
# import platform
# if "Windows" in platform.system():
# 	PRO_DIR = os.environ.get("ENCHAINPATH")
# else:
# 	PRO_DIR = os.environ.get("ENCHAINPATH")
PRO_DIR = os.environ.get("ENCHAINPATH")
print PRO_DIR
Debug = True
gSupported_img_suffix = ["BMP", "GIF", "JPG", "JPEG", "PNG", "TIFF", "PBM", "PGM", "PPM", "XBM", "XPM"]

projectLink = "https://github.com/Zhehua-Hu/Enchain"
onlineHelpLink = "https://github.com/Zhehua-Hu/Enchain/wiki"
author_blog = "http://zhehua.info"

# OpenCV
import cv2
# PyQt
from PyQt5.QtWidgets import QApplication, qApp,\
	QMainWindow, QWidget, QFileDialog, QGraphicsScene,\
	QGraphicsPixmapItem, QMessageBox, QAction


from PyQt5.QtGui import QPixmap, QImage, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
# from PyQt5.QtWebKit import QWebView


file_path = os.path.join(PRO_DIR, "ui")
# sys.path.append(file_path)
icon_path = os.path.join(PRO_DIR, "icons")

from ui.mainwindow import Ui_MainWindow
from libs.videoSlice import videoSlice, showVideoInfo
from libs.create_VOC_dirs import create_VOC_dirs

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
		imgs_name = []
		imgs_path = []
		ret_cnt = 0
		for root, dirs, filenames in os.walk(folder):
			if type == "Recursive":
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if filename.split(".")[-1].upper() in gSupported_img_suffix:
							imgs_name.append(filename)
							ret_cnt += 1
			else:
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if filename.split(".")[-1].upper() in gSupported_img_suffix:
							imgs_name.append(filename)
				ret_cnt = len(imgs_name)
				break

		imgs_name.sort()  # from 000001 to increase
		for item in imgs_name:
			imgs_path.append(os.path.join(self.img_dirname, item))
		return imgs_path, ret_cnt


	def FirstImg(self):
		return self.imgs_path[0]

	def nextImg(self):
		self.cur_idx += 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return self.imgs_path[self.cur_idx]

	def previousImg(self):
		self.cur_idx -= 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return self.imgs_path[self.cur_idx]
	
	def getImgPath(self):
		return self.imgs_path[self.cur_idx]

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
backend image process: gCVimg using OpenCV
"""
	def __init__(self, parent=None):
		super(QMainWindow, self).__init__()
		QMainWindow.__init__(self, parent)
		self.setupUi(self)

		self.setWindowIcon(QIcon(icon_path + u"/EnchainLogoLittle.png"))
		self.gFileDialog = QFileDialog()
		self.gMesssage = QMessageBox()
		self.graphicsscene = QGraphicsScene()
		self.graphicsView.setScene(self.graphicsscene)

		self.gCVimg = None
		self.gQpixmap = None
		self.gQimg = None
		self.gVideo = None
		self.gVidDesFolder = None
		self.gSelectSourceFolder = None
		self.gSelectSource_exist = False
		self.gImgList = None
		self.gImgList_exist = False

		self.gSelectDestinationFolder = None
		self.gSelectDestination_exist = False



		self.setupMenubar()
		self.setupToolbar()
		self.setupButtons()
		self.setupStatusbar()

	def setupMenubar(self):
		self.menubar.setNativeMenuBar(False)  # better for cross-platform

		self.actionCreateVOCFolder.triggered.connect(self.createVOCFolder)

		self.actionQuit.setIcon(QIcon(icon_path + u"/exit-to-app.svg"))
		self.actionQuit.setShortcut(u"Ctrl+Q")
		self.actionQuit.setStatusTip(u"Quit Software")
		self.actionQuit.triggered.connect(qApp.quit)

		self.actionClose.setIcon(QIcon(icon_path + u"/close-circle.svg"))
		self.actionClose.setStatusTip(u"Close File")
		self.actionClose.triggered.connect(self.clearView)

		self.actionOpenImage.setIcon(QIcon(icon_path + u"/image-area.svg"))
		self.actionOpenImage.setStatusTip(u"Open Single Image")
		self.actionOpenImage.triggered.connect(self.openImage)

		self.actionSaveImage.setStatusTip(u"Save Image")
		self.actionSaveImage.triggered.connect(self.saveImageFromBackendCVimg)

		self.actionOpenFolder.setIcon(QIcon(icon_path + u"/folder-open.svg"))
		self.actionOpenFolder.setStatusTip(u"Open Folder Contains Images")
		self.actionOpenFolder.triggered.connect(self.setSelectSourceFolder)

		self.actionOpenVideo.setIcon(QIcon(icon_path + u"/video.svg"))
		self.actionOpenVideo.setStatusTip(u"Open Folder Contains Images")
		self.actionOpenVideo.triggered.connect(self.setVideo)

		self.actionVideoSlice.setIcon(QIcon(icon_path + u"/animation.svg"))
		self.actionVideoSlice.setStatusTip(u"Slice Video TO Images")
		self.actionVideoSlice.triggered.connect(self.videoSliceToFolder)

		self.actionSelectSource.setIcon(QIcon(icon_path + u"/folder-open.svg"))
		self.actionSelectSource.setStatusTip(u"Open Folder Contains Source Images")
		self.actionSelectSource.triggered.connect(self.setSelectSourceFolder)

		self.actionSelectDestination.setIcon(QIcon(icon_path + u"/folder-open.svg"))
		self.actionSelectDestination.setStatusTip(u"Open Folder To Save Selected Images")
		self.actionSelectDestination.triggered.connect(self.setSelectDestinationFolder)


		self.actionDataCleansing.triggered.connect(self.todoInfo)

		self.actionOnline_Help.triggered.connect(self.onlineHelp)
		self.actionAbout_Enchain.triggered.connect(self.about_Enchain)
		self.actionAbout_Qt.triggered.connect(self.aboutQt)




	def setupToolbar(self):
		self.toolbar = self.addToolBar(u"maintoolbar")

		actionPrevious = QAction(QIcon(icon_path + u"/arrow-left-bold-circle.svg"), u"Previous", self)
		actionPrevious.setShortcut(u"Left")
		actionPrevious.triggered.connect(self.showPreviousImg)
		self.toolbar.addAction(actionPrevious)
		
		actionNext = QAction(QIcon(icon_path + u"/arrow-right-bold-circle.svg"), u"Next", self)
		actionNext.setShortcut(u"Right")
		actionNext.triggered.connect(self.showNextImg)
		self.toolbar.addAction(actionNext)
		
		actionSelect = QAction(QIcon(icon_path + u"/check-circle.svg"), u"Select", self)
		actionSelect.setShortcut(u"Ctrl+Return")
		actionSelect.triggered.connect(self.selectImg)
		self.toolbar.addAction(actionSelect)

		actionDelete = QAction(QIcon(icon_path + u"/delete-circle.svg"), u"Delete", self)
		actionDelete.setShortcut(u"Ctrl+Delete")
		actionDelete.triggered.connect(self.deleteImg)
		self.toolbar.addAction(actionDelete)

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

		choosed_path = self.gFileDialog.getOpenFileName(self, u"Open File", openImage_path)
		if choosed_path[0]:
			self.showImgFromPath(choosed_path[0])
			self.printToStatus("Open Image in " + choosed_path[0])

	def showImgFromPath(self, img_path):
		if Debug:
			print("showImgFromPath")
			print(img_path)

		pixmap = QPixmap(img_path)
		self.updateView(pixmap)

	def showImgFromCvimg(self, CVimg):
		if Debug:
			print("showImgFromCvimg")
		self.updateView(self.convert_CVimgToQpixmap(CVimg))

	def getPixmapFromPath(self, img_path):
		if Debug:
			print("getPixmapFromPath")
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

	def setSelectSourceFolder(self):
		if Debug:
			print("setSelectSourceFolder")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		if self.gSelectSource_exist:
			print("Select Source Has Set!")
			
		choosed_folder = self.gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		
		if Debug:
			print(choosed_folder)
			print(choosed_folder[0])
			
		if choosed_folder is not None:
			self.gSelectSourceFolder = choosed_folder

		self.gImgList = ImgList(self.gSelectSourceFolder)
		self.gSelectSource_exist = True
		self.gImgList_exist = True
		if self.gImgList_exist:
			self.showImgFromPath(self.gImgList.FirstImg())

	def showNextImg(self):
		if Debug:
			print("showNextImg")
		if self.gImgList_exist:
			self.showImgFromPath(self.gImgList.nextImg())

	def showPreviousImg(self):
		if Debug:
			print("showPreviousImg")
		if self.gImgList_exist:
			self.showImgFromPath(self.gImgList.previousImg())

	def setVideo(self):
		if Debug:
			print("setVideo")
			openVideo_path = os.path.join(PRO_DIR, u"test/video_folder")
		else:
			openVideo_path = os.path.expanduser(u"~")

		choosed_path = self.gFileDialog.getOpenFileName(self, u"Open File", openVideo_path)

		if choosed_path[0] is not None:
			self.gVideo = choosed_path[0]
			vhandle, fps, size, firstframe = showVideoInfo(choosed_path[0])
			self.showImgFromCvimg(firstframe)

	def videoSliceToFolder(self):
		if Debug:
			print("videoSlice")
			videoSlice_path = os.path.join(PRO_DIR, u"test/")
		else:
			videoSlice_path = os.path.expanduser(u"~")

		choosed_folder = self.gFileDialog.getExistingDirectory(self, u"Open Folder", videoSlice_path)
		if choosed_folder is not None:
			self.gVidDesFolder = choosed_folder

		videoSlice(self.gVideo, self.gVidDesFolder, "png")

	def setSelectDestinationFolder(self):
		if Debug:
			print("setSelectDestinationFolder")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		choosed_folder = self.gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		if choosed_folder[0] is not None:
			self.gSelectDestinationFolder = choosed_folder
			self.gSelectDestination_exist = True
		# TODO: pop info if img folder has opened

	def selectImg(self):
		if Debug:
			print("selectImg")
		if self.gSelectDestination_exist:
			img_src = self.gImgList.getImgPath()
			img_des = self.gSelectDestinationFolder
			# print img_src, img_des
			shutil.copy(img_src, self.gSelectDestinationFolder)
		else:
			print("Did not set Select Destination!")

	def deleteImg(self):
		if Debug:
			print("deleteImg")
		if self.gSelectDestination_exist:
			print(self.gImgList.cur_idx)
		else:
			print("Did not set Select Destination!")

	def convert_CVimgToQpixmap(self, CVimg):
		height, width, dim = CVimg.shape
		bytesPerLine = dim * width
		qimg = QImage(CVimg.data, width, height, bytesPerLine, QImage.Format_RGB888)
		return QPixmap.fromImage(qimg)

	def convert_CVimgToQimg(self, CVimg):
		height, width, dim = CVimg.shape
		bytesPerLine = dim * width
		qimg = QImage(CVimg.data, width, height, bytesPerLine, QImage.Format_RGB888)
		return qimg

	def saveImageFromBackendCVimg(self):
		default_name = "test.jpg"
		try:
			if self.gCVimg is not None:
				choosed_path = self.gFileDialog.getSaveFileName(self, "Save file", os.path.expanduser("~") + "/" + default_name)
				if choosed_path[0]:
					cv2.imwrite(choosed_path[0], self.gCVimg)
			else:
				print("Empty!")
		except:
			print("No Image!")

	def saveImageFromCVimg(self, CVimg):
		default_name = "test.jpg"
		try:
			if self.gCVimg is not None:
				choosed_path = self.gFileDialog.getSaveFileName(self, "Save file", os.path.expanduser("~") + "/" + default_name)
				if choosed_path[0]:
					cv2.imwrite(choosed_path[0], CVimg)
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

	# Project Zone
	def createVOCFolder(self):
		if Debug:
			print("createVOCFolder")
			videoSlice_path = os.path.join(PRO_DIR, u"test/")
		else:
			videoSlice_path = os.path.expanduser(u"~")

		choosed_folder = self.gFileDialog.getExistingDirectory(self, u"Open Folder", videoSlice_path)
		if choosed_folder is not None:
			create_VOC_dirs(choosed_folder)
			self.printToStatus("create VOC Folder in " + choosed_folder)

	def todoInfo(self):
		if Debug:
			print("todoInfo")
		reply = QMessageBox.about(self.gMesssage, "Todo Info", "This function will be active in future version.")


	def onlineHelp(self):
		if Debug:
			print("about_Enchain")
		QDesktopServices.openUrl(QUrl(onlineHelpLink))

	def about_Enchain(self):
		if Debug:
			print("about_Enchain")
		reply = QMessageBox.about(self.gMesssage, "About Enchain", "Please visit project homepage")
		QDesktopServices.openUrl(QUrl(projectLink))

	def aboutQt(self):
		if Debug:
			print("aboutQt")
		reply = self.gMesssage.aboutQt(self)

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
