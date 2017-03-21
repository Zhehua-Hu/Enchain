#!/usr/bin/env python
# coding=utf-8
"""
Copyright {2017} {Zhehua-Hu}
Version: v0.0.2
"""


# std libs
import sys
import os
import shutil
import numpy as np
import pprint

"""
Global Config
"""
Debug = True
USE_QRC = True


# USE PRO_DIR FOR DEBUG
if Debug:
	import platform
	if "Windows" in platform.system():
		PRO_DIR = os.environ.get("ENCHAINPATH")
	else:
		PRO_DIR = os.path.dirname(__file__)
	print("PRO_DIR: %s" % PRO_DIR)

if USE_QRC:
	icon_path = ":/"
else:
	icon_path = os.path.join(PRO_DIR, "icons")

gProgressBarFull = 100
gProgressBarEmpty = 0
gSupported_img_suffix = ["BMP", "GIF", "JPG", "JPEG", "PNG", "TIFF", "PBM", "PGM", "PPM", "XBM", "XPM"]
gSupported_video_suffix = ["AVI", "MP4"]
__appname__ = "Enchain"
projectLink = "https://github.com/Zhehua-Hu/Enchain"
onlineHelpLink = "https://github.com/Zhehua-Hu/Enchain/wiki"
author_blog = "http://zhehua.info"

# OpenCV
import cv2
# PyQt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import resources
from ui.mainwindow import Ui_MainWindow
from ui.AutoSelectSetting import Ui_AutoSelectSetting

from libs.videoSlice import videoSlice, showVideoInfo
from libs.create_VOC_dirs import create_VOC_dirs
from libs.img_cvt_pyqt_cv import *

class FileList():
	"""
	class: provide file(eg.images,videos) list management
	"""

	cur_idx = 0
	file_cnt = 0

	def __init__(self, folder, supported_file_suffix, search_type="NotRecursive"):
		self.file_dirname = folder
		self.file_suffix = supported_file_suffix
		self.files_path, self.file_cnt = self.getContainedfiles(folder, type=search_type)


	def isEmpty(self):
		if self.file_cnt > 0:
			return False
		else:
			return True

	def getContainedfiles(self, folder, type="NotRecursive"):
		"""
		get Contained files
		:param folder: searched folder
		:param type: determine if search sub-folder
		:return: full path list, list length
		"""
		files_name = []
		files_path = []
		ret_cnt = 0
		for root, dirs, filenames in os.walk(folder):
			if type == "Recursive":
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if filename.split(".")[-1].upper() in self.file_suffix:
							files_name.append(filename)
							ret_cnt += 1
			else:
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if filename.split(".")[-1].upper() in self.file_suffix:
							files_name.append(filename)
				ret_cnt = len(files_name)
				break

		files_name.sort()  # from 000001 to increase
		for item in files_name:
			files_path.append(os.path.join(self.file_dirname, item))
		return files_path, ret_cnt

	def getFilesPathList(self):
		return self.files_path

	def firstFile(self):
		return self.files_path[0]

	def nextFile(self):
		self.cur_idx += 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return self.files_path[self.cur_idx]

	def previousFile(self):
		self.cur_idx -= 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return self.files_path[self.cur_idx]
	
	def getCurFilePath(self):
		return self.files_path[self.cur_idx]

	def safeLimit(self, idx):
		if idx > self.file_cnt-1:
			return self.file_cnt-1
		elif idx < 0:
			return 0
		else:
			return idx

	def __repr__(self):
		for item in self.__dict__.items():
			print("%s : %s" % item)

class AutoSelectSettingClass(QDialog, Ui_AutoSelectSetting):
	def __init__(self, parent=None):
		super(QDialog, self).__init__()
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.dialog = QInputDialog()

class MainWindow(QMainWindow, Ui_MainWindow):
	"""
Main Window in Enchain.
backend image process: gCVmat using OpenCV
"""
	def __init__(self, parent=None):
		super(QMainWindow, self).__init__()
		QMainWindow.__init__(self, parent)
		self.setupUi(self)

		self._gFileDialog = QFileDialog()
		self._gMesssage = QMessageBox()
		self._graphicsscene = QGraphicsScene()
		# DO NOT RENAME "graphicsView"
		self.graphicsView.setScene(self._graphicsscene)

		# global variables
		self._gCVmat = None
		self._gQpixmap = None
		self._gQimg = None
		self._gVideo = None
		self._gVidDesFolder = None
		self._gVidoesFolder = None
		self._gVidoesList = None

		self._gSelectSourceFolder = None
		self._gSelectSource_exist = False
		self._gImgList = None
		self._gImgList_exist = False


		self.gSelectDestinationFolder = None
		self.gSelectDestination_exist = False



		self.progressBar.step = gProgressBarEmpty
		self.progressBar.setValue(self.progressBar.step)

		self.dockWidgetRight.setObjectName("listView")

		self.setupMenubar()
		self.setupToolbar()
		self.setupButtons()
		self.setupStatusbar()

# Event Testing
# 	def wheelEvent(self, ev):
# 		# print(ev.phase())
# 		# print(ev.x())
# 		# print(ev.y())
# 		# print(ev.pos())
# 		# print(ev.posF())
# 		# print(ev.globalX())
# 		# print(ev.globalY())
# 		# print(ev.angleDelta())
# 		# print(ev.pixelDelta())
# 		# print(ev.buttons())
#
# 		# for item in type(ev).__dict__:
# 		# 	print(item)
# 			# print(getattr(ev,item))
#
# 		def isWheelUp(ev):
# 			if ev.angleDelta().y() >=0:
# 				return True
# 			else:
# 				return False
# 		print(isWheelUp(ev))
# 		# print(ev.angleDelta().y())
#
#
# 		ev.accept()
#
# 	def keyPressEvent(self, ev):
# 		# print(ev)
# 		key = ev.key()
# 		print(key)
#
# 	def enterEvent(self, ev):
# 		print("enterEvent")
#
# 	def leaveEvent(self, ev):
# 		print("leaveEvent")
#
# 	def focusOutEvent(self, ev):
# 		print("focusOutEvent")
#
# 	def mouseMoveEvent(self, ev):
# 		print("mouseMoveEvent")
# 		print(ev.pos())
#
# 	def mousePressEvent(self, ev):
# 		print("mousePressEvent")
# 		print(ev.pos())
#
# 	def mouseReleaseEvent(self, ev):
# 		print("mouseReleaseEvent")
# 		print(ev.pos())




# Sys Setup

	def setupMenubar(self):
		self.menubar.setNativeMenuBar(False)  # better for cross-platform

		self.actionCreateVOCFolder.triggered.connect(self.createVOCFolder)

		self.actionQuit.setIcon(QIcon(icon_path + "/exit-to-app.svg"))
		self.actionQuit.setShortcut("Ctrl+Q")
		self.actionQuit.setStatusTip(u"Quit Software")
		self.actionQuit.triggered.connect(qApp.quit)

		self.actionClose.setIcon(QIcon(icon_path + "/close-circle.svg"))
		self.actionClose.setStatusTip(u"Close File")
		self.actionClose.triggered.connect(self.clearView)

		self.actionOpenImage.setIcon(QIcon(icon_path + "/image-area.svg"))
		self.actionOpenImage.setStatusTip(u"Open Single Image")
		self.actionOpenImage.triggered.connect(self.openImage)

		self.actionSaveImage.setStatusTip(u"Save Image")
		self.actionSaveImage.triggered.connect(self.saveImageFromBackendCVmat)

		self.actionOpenImageFolder.setIcon(QIcon(icon_path + "/folder-open.svg"))
		self.actionOpenImageFolder.setStatusTip(u"Open Folder Contains Images")
		self.actionOpenImageFolder.triggered.connect(self.setSelectSourceFolder)

		self.actionOpenVideo.setIcon(QIcon(icon_path + "/video.svg"))
		self.actionOpenVideo.setStatusTip(u"Open Folder Contains Video")
		self.actionOpenVideo.triggered.connect(self.setVideo)

		self.actionOpenVideoFolder.setIcon(QIcon(icon_path + "/folder-open.svg"))
		self.actionOpenVideoFolder.setStatusTip(u"Open Folder Contains Videos")
		self.actionOpenVideoFolder.triggered.connect(self.setVideosFolder)

		self.actionSaveSliceTo.setIcon(QIcon(icon_path + "/animation.svg"))
		self.actionSaveSliceTo.setStatusTip(u"Slice Video To Images")
		self.actionSaveSliceTo.triggered.connect(self.saveSliceToFolder)

		self.actionSaveSliceSetTo.setIcon(QIcon(icon_path + "/animation.svg"))
		self.actionSaveSliceSetTo.setStatusTip(u"Slice Videos To Images")
		self.actionSaveSliceSetTo.triggered.connect(self.saveSliceSetToFolder)


		self.actionSelectSource.setIcon(QIcon(icon_path + "/folder-open.svg"))
		self.actionSelectSource.setStatusTip(u"Open Folder Contains Source Images")
		self.actionSelectSource.triggered.connect(self.setSelectSourceFolder)

		self.actionSelectDestination.setIcon(QIcon(icon_path + "/folder-open.svg"))
		self.actionSelectDestination.setStatusTip(u"Open Folder To Save Selected Images")
		self.actionSelectDestination.triggered.connect(self.setSelectDestinationFolder)

		self.actionAutoSelect.setIcon(QIcon(icon_path + "/pokeball.svg"))
		self.actionAutoSelect.setStatusTip(u"Auto Select From Images")
		self.actionAutoSelect.triggered.connect(self.autoSelect)

		self.actionOnline_Help.setIcon(QIcon(icon_path + "/search-web.svg"))
		self.actionOnline_Help.triggered.connect(self.onlineHelp)

		self.actionAbout_Enchain.setIcon(QIcon(icon_path + "/EnchainLogoLittle.ico"))
		self.actionAbout_Enchain.triggered.connect(self.about_Enchain)

		self.actionAbout_Qt.setIcon(QIcon(icon_path + "/qt.png"))
		self.actionAbout_Qt.triggered.connect(self.aboutQt)

		# TODO
		self.actionConnect_Author.setIcon(QIcon(icon_path + "/account-circle.svg"))
		self.actionConnect_Author.triggered.connect(self.todoInfo)

		self.actionCheck_Update.setIcon(QIcon(icon_path + "/autorenew.svg"))
		self.actionCheck_Update.triggered.connect(self.todoInfo)

		self.actionAssignment.setIcon(QIcon(icon_path + "/account-multiple.svg"))

		self.actionCutImage.triggered.connect(self.todoInfo)
		self.actionShow_guidance.triggered.connect(self.todoInfo)
		self.actionDatasetInput.triggered.connect(self.todoInfo)
		self.actionConvertSliceToVideo.triggered.connect(self.todoInfo)

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

# Callback function
	def printToStatus(self, message):
		self.statusBar().showMessage(message)

	def openImage(self):
		"""
		Open and Show single imagesaveSliceSetToFolder
		:return:
		"""
		if Debug:
			openImage_path = os.path.join(PRO_DIR, u"test/img_folder")
		else:
			openImage_path = os.path.expanduser(u"~")

		choosed_path = self._gFileDialog.getOpenFileName(self, u"Open File", openImage_path)
		if choosed_path[0]:
			self.showImgFromPath(choosed_path[0])
			self.printToStatus("Open Image in " + choosed_path[0])

	def showImgFromPath(self, img_path):
		if Debug:
			print("showImgFromPath")
			print(img_path)
		pixmap = QPixmap(img_path)
		self.updateView(pixmap)

	def showImgFromCVmat(self, CVmat):
		if Debug:
			print("showImgFromCVmat")
		self.updateView(convert_CVmatToQpixmap(CVmat))

	def getPixmapFromPath(self, img_path):
		if Debug:
			print("getPixmapFromPath")
		pixmap = QPixmap(img_path)
		return pixmap

	def updateView(self, qpixmap):
		self.clearView()
		viewWidth = self.graphicsView.frameGeometry().width()
		viewHeight = self.graphicsView.frameGeometry().height()

		# fix window
		pixRatioMap = qpixmap.scaled(viewWidth, viewHeight, Qt.KeepAspectRatio)
		pixItem = QGraphicsPixmapItem(pixRatioMap)
		self._graphicsscene.addItem(pixItem)
		self._graphicsscene.update()

	def clearView(self):
		items = self._graphicsscene.items()
		for item in items:
			self._graphicsscene.removeItem(item)

	def showNextImg(self):
		if Debug:
			print("showNextImg")
		if self._gImgList_exist:
			self.showImgFromPath(self._gImgList.nextFile())

	def showPreviousImg(self):
		if Debug:
			print("showPreviousImg")
		if self._gImgList_exist:
			self.showImgFromPath(self._gImgList.previousFile())

# Video
	def setVideo(self):
		"""
		Set single video to slice
		:return:
		"""
		if Debug:
			print("setVideo")
			openVideo_path = os.path.join(PRO_DIR, "test/video_folder")
		else:
			openVideo_path = os.path.expanduser("~")

		choosed_path = self._gFileDialog.getOpenFileName(self, u"Open File", openVideo_path)

		if choosed_path[0] == u'' or choosed_path[0] == '':
			return # avoid bug: open filedialog but not choose anything
		if choosed_path[0] is not None:
			self._gVideo = choosed_path[0]
			print("path->: ", self._gVideo)
			print(type(self._gVideo))
			vhandle, fps, size, firstframe = showVideoInfo(choosed_path[0])
			self.showImgFromCVmat(firstframe)

		self.printToStatus("Please Choose Folder To Save Video Slice")
		self.setProgressBar(gProgressBarEmpty)

	def saveSliceToFolder(self):
		"""
		Slice single video
		:return:
		"""
		if Debug:
			print("videoSlice")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		choosed_folder = self._gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		if choosed_folder == u'' or choosed_folder == '':
			return # avoid bug: open filedialog but not choose anything
		if choosed_folder is not None:
			self._gVidDesFolder = choosed_folder

		videoSlice(self._gVideo, self._gVidDesFolder, progressbarsetter=self.setProgressBar, save_type="png")
		self.setProgressBar(gProgressBarFull)

	def setVideosFolder(self):
		if Debug:
			print("setVideosFolder")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		choosed_folder = self._gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		print(choosed_folder)

		if choosed_folder == u'' or choosed_folder == '':
			return # avoid bug: open filedialog but not choose anything
		if choosed_folder is not None:
			self._gVidoesFolder = choosed_folder

		self._gVidoesList = FileList(self._gVidoesFolder, gSupported_video_suffix)
		if self._gVidoesList.isEmpty():
			print("List is EMPTY")
			self.printToStatus("Contained nothing under condition")
		else:
			self.printToStatus(self._gVidoesList.firstFile())

	def saveSliceSetToFolder(self):
		"""
		Set a folder to contain slice set
		:return:
		"""
		if Debug:
			print("saveSliceSetToFolder")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		choosed_folder = self._gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		if choosed_folder == u'' or choosed_folder == '':
			return # avoid bug: open filedialog but not choose anything
		if choosed_folder is not None:
			self._gVidDesFolder = choosed_folder

		idx = 1
		for video in self._gVidoesList.getFilesPathList():
			self.setProgressBar(gProgressBarEmpty)
			self.printToStatus("Process \"%s\", Please Wait." % video)
			processed_cnt = videoSlice(video, self._gVidDesFolder, \
			                           progressbarsetter=self.setProgressBar, \
			                           save_type="png", img_comp=9, start_idx=idx)
			idx += processed_cnt

# Image
	def setSelectSourceFolder(self):
		if Debug:
			print("setSelectSourceFolder")
			tmp_path = os.path.join(PRO_DIR, "test/")
		else:
			tmp_path = os.path.expanduser("~")

		if self._gSelectSource_exist:
			print("Select Source Has Set!")

		choosed_folder = self._gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		if choosed_folder == u'' or choosed_folder == '':
			return # avoid bug: open filedialog but not choose anything
		if choosed_folder is not None:
			self._gSelectSourceFolder = choosed_folder

		self._gImgList = FileList(self._gSelectSourceFolder, gSupported_img_suffix)
		if self._gImgList.isEmpty():
			print("List is EMPTY")
			self.printToStatus("Contained nothing under condition")
		else:
			self._gSelectSource_exist = True
			self._gImgList_exist = True
		if self._gImgList_exist:
			self.showImgFromPath(self._gImgList.firstFile())

	def setSelectDestinationFolder(self):
		if Debug:
			print("setSelectDestinationFolder")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		choosed_folder = self._gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		if choosed_folder == u'' or choosed_folder == '':
			return # avoid bug: open filedialog but not choose anything
		if choosed_folder[0] is not None:
			self.gSelectDestinationFolder = choosed_folder
			self.gSelectDestination_exist = True
		# TODO: pop info if img folder has opened

	def selectImg(self):
		"""
		Choose image and save it to SelectDestinationFolder
		:return:
		"""
		if Debug:
			print("selectImg")
		if self.gSelectDestination_exist:
			img_src = self._gImgList.getCurFilePath()
			# img_des = self.gSelectDestinationFolder
			# print img_src, img_des
			shutil.copy(img_src, self.gSelectDestinationFolder)
			self.printToStatus("Select \"%s\"" % img_src)
		else:
			print("Did not set Select Destination!")

	def deleteImg(self):
		"""
		Delete image from source
		:return:
		"""
		if Debug:
			print("deleteImg")
		if self.gSelectDestination_exist:
			print(self._gImgList.cur_idx)
		else:
			print("Did not set Select Destination!")

	def autoSelect(self):
		if Debug:
			print("autoSelect")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		tmp_idx = 1
		if self._gImgList_exist and self.gSelectDestination_exist:
			for img_src in self._gImgList.getFilesPathList():
				if tmp_idx % 50 == 0:
					shutil.copy(img_src, self.gSelectDestinationFolder)
					self.printToStatus("Select \"%s\"" % img_src)
				tmp_idx += 1
		else:
			print("ImgList or SelectDestination Not Exist!")
		self.printToStatus("AutoSelect Finish")
        # intNum, is_ok = QInputDialog.getInt(self, "QInputDialog.getInteger()","Percentage:", 25, 0, 100, 1)
        # if is_ok:
        #     self.label_integer.setText(str(intNum))

	def saveImageFromBackendCVmat(self):
		default_name = "test.jpg"
		try:
			if self._gCVmat is not None:
				choosed_path = self._gFileDialog.getSaveFileName(self, "Save file", os.path.expanduser("~") + "/" + default_name)
				if choosed_path[0] == u'' or choosed_path[0] == '':
					return # avoid bug: open filedialog but not choose anything
				if choosed_path[0] is not None:
					cv2.imwrite(choosed_path[0], self._gCVmat)
			else:
				print("Empty!")
		except:
			print("No Image!")

	def saveImageFromCVmat(self, CVmat):
		default_name = "test.jpg"
		try:
			if self._gCVmat is not None:
				choosed_path = self._gFileDialog.getSaveFileName(self, "Save file", os.path.expanduser("~") + "/" + default_name)
				if choosed_path[0]:
					cv2.imwrite(choosed_path[0], CVmat)
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

	# handler

	def setProgressBar(self, num):
		if num <= 0:
			self.progressBar.setValue(0)
		elif num >= 100:
			self.progressBar.setValue(100)
		else:
			self.progressBar.setValue(num)



	# Project Zone
	def createVOCFolder(self):
		if Debug:
			print("createVOCFolder")
			tmp_path = os.path.join(PRO_DIR, u"test/")
		else:
			tmp_path = os.path.expanduser(u"~")

		choosed_folder = self._gFileDialog.getExistingDirectory(self, u"Open Folder", tmp_path)
		if choosed_folder is not None:
			create_VOC_dirs(choosed_folder)
			self.printToStatus("create VOC Folder in " + choosed_folder)

	def todoInfo(self):
		"""
		Info that this function is not finished yet!
		:return:
		"""
		if Debug:
			print("todoInfo")
		reply = QMessageBox.about(self._gMesssage, "Todo Info", "This function will be active in future version.")


	# Common Component
	def onlineHelp(self):
		if Debug:
			print("about_Enchain")
		QDesktopServices.openUrl(QUrl(onlineHelpLink))

	def about_Enchain(self):
		if Debug:
			print("about_Enchain")
		reply = QMessageBox.about(self._gMesssage, "About Enchain", "Please visit project homepage")
		QDesktopServices.openUrl(QUrl(projectLink))

	def aboutQt(self):
		if Debug:
			print("aboutQt")
		reply = self._gMesssage.aboutQt(self)

	def closeEvent(self, event):
		"""
		Event: query when exit app
		:param event:
		:return:
		"""
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



def run_main(argv=[]):
	"""
Standard boilerplate Qt/PyQt application code.
We can test the application in one thread.
This function can be called by as below:
app, mwin = run_main(argv)
"""
	app = QApplication(argv)
	app.setApplicationName(__appname__)
	app.setWindowIcon(QIcon(icon_path + "/EnchainLogoLittle.png"))

	mwin = MainWindow(argv[1] if len(argv) == 2 else None)
	mwin.show()
	return app, mwin

def main(argv):
	"""
Call run_main to start app
unittest in folder "utest"
"""
	app, mwin = run_main(argv)
	return app.exec_() # enter Event-Loop

if __name__ == '__main__':
	sys.exit(main(sys.argv))
