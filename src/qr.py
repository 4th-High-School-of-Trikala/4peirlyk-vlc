import qrcode
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QrImage(qrcode.image.base.BaseImage):
	def __init__(self, border, width, box_size, qrcode_modules):
		self.border = border
		self.width = width
		self.box_size = box_size
		size = (width + border * 2) * box_size
		self._image = QImage(size, size, QImage.Format_RGB16)
		self._image.fill(Qt.white)
	
	def pixmap(self):
		return QPixmap.fromImage(self._image)
		
	def drawrect(self, row, col):
		painter = QPainter(self._image)
		painter.fillRect(
			(col + self.border) * self.box_size,
			(row + self.border) * self.box_size,
			self.box_size, self.box_size,
			QtCore.Qt.black
		)
