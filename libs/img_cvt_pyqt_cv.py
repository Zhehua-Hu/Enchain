#!/usr/bin/python
# coding=utf-8
"""

C++ Version See
https://asmaloney.com/2013/11/code/converting-between-cvmat-and-qimage-or-qpixmap/
http://qtandopencv.blogspot.com/2013/08/how-to-convert-between-cvmat-and-qimage.html
"""

from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

def convert_CVmatToQpixmap(CVmat):
	# COLOR_BGR2RGB
	CVmat = cv2.cvtColor(CVmat, cv2.COLOR_BGR2RGB)

	# CVmat to Qimage
	height, width, dim = CVmat.shape
	bytesPerLine = dim * width
	qimg = QImage(CVmat.data, width, height, bytesPerLine, QImage.Format_RGB888)
	return QPixmap.fromImage(qimg)

def convert_CVmatToQimg(CVmat):
	# COLOR_BGR2RGB
	CVmat = cv2.cvtColor(CVmat, cv2.COLOR_BGR2RGB)

	# CVmat to Qimage
	height, width, dim = CVmat.shape
	bytesPerLine = dim * width
	qimg = QImage(CVmat.data, width, height, bytesPerLine, QImage.Format_RGB888)
	return qimg

def convertQimgToQpixmap(Qimg):
	return QPixmap.fromImage(Qimg)

def convertQpixmapToQimg(qpixmap):
	return QPixmap.toImage(qpixmap)


# not work
# def convertQimgToCVmat(Qimg):
# 	Qimg = Qimg.convertToFormat(4)
# 	width = Qimg.width()
# 	height = Qimg.height()
# 	ptr = Qimg.bits()
# 	ptr.setsize(Qimg.byteCount())
# 	arr = np.array(ptr).reshape(height, width, 4)
# 	return cv2.cvtColor(arr, cv2.CV_BGR2RGB)

# not work
# def convertQimgToCVmat(img):

# Test Code in Enchain
# QPixmap
# pixmap = QPixmap(img_path)
# self.updateView(pixmap)

# QPixmap <-> Qimage
# convertQimgToQpixmap convertQpixmapToQimg
# pixmap = QPixmap(img_path)
# self.updateView(convertQimgToQpixmap(convertQpixmapToQimg(pixmap)))

# CVMat
# convert_CVmatToQpixmap
# CVmat = cv2.imread(img_path)
# self.updateView(convertQimgToQpixmap(convertQpixmapToQimg(convert_CVmatToQpixmap(CVmat))))

# CVMat -> Qimage
# convert_CVmatToQimg
# CVmat = cv2.imread(img_path)
# self.updateView(convertQimgToQpixmap(convert_CVmatToQimg(CVmat)))
