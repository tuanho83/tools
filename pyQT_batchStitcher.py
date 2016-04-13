import sys
from PyQt4 import QtCore, QtGui
from functools import partial

class QCustomDelegate (QtGui.QItemDelegate):
	def createEditor (self, parentQWidget, optionQStyleOptionViewItem, indexQModelIndex):
		column = indexQModelIndex.column()
		if column == 1:
			editorQWidget = QtGui.QSpinBox(parentQWidget)
			editorQWidget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			editorQWidget.setMinimum(0)
			editorQWidget.setMaximum(100)
			return editorQWidget
		elif column == 2:
			editorQWidget = QtGui.QLineEdit(parentQWidget)
			editorQWidget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			return editorQWidget
		elif column == 3:
			editorQWidget = QtGui.QPushButton(parentQWidget)
			return editorQWidget            
		else:
			return QtGui.QItemDelegate.createEditor(self, parentQWidget, optionQStyleOptionViewItem, indexQModelIndex)

	def setEditorData (self, editorQWidget, indexQModelIndex):
		column = indexQModelIndex.column()
		if column == 1:
			value, _ = indexQModelIndex.model().data(indexQModelIndex, QtCore.Qt.EditRole).toInt()
			editorQWidget.setValue(value)
		elif column == 2:
			textQString = indexQModelIndex.model().data(indexQModelIndex, QtCore.Qt.EditRole).toString()
			editorQWidget.setText(textQString)
		elif column == 3:
			textQString = indexQModelIndex.model().data(indexQModelIndex, QtCore.Qt.EditRole).toString()
			self.connect(editorQWidget, QtCore.SIGNAL('released()'), partial(self.requestNewPath, indexQModelIndex))
			editorQWidget.setText(textQString)
		else:
			QtGui.QItemDelegate.setEditorData(self, editorQWidget, indexQModelIndex)

	def setModelData (self, editorQWidget, modelQAbstractItemModel, indexQModelIndex):
		column = indexQModelIndex.column()
		if column == 1:
			value = editorQWidget.value()
			modelQAbstractItemModel.setData(indexQModelIndex, value, QtCore.Qt.EditRole)
		elif column == 2:
			textQString = editorQWidget.text()
			modelQAbstractItemModel.setData(indexQModelIndex, textQString, QtCore.Qt.EditRole)
		elif column == 3:
			textQString = editorQWidget.text()
			modelQAbstractItemModel.setData(indexQModelIndex, textQString, QtCore.Qt.EditRole)
		else:
			QtGui.QItemDelegate.setModelData(self, editorQWidget, modelQAbstractItemModel, indexQModelIndex)

	def updateEditorGeometry(self, editorQWidget, optionQStyleOptionViewItem, indexQModelIndex):
		column = indexQModelIndex.column()
		if column == 1:
			editorQWidget.setGeometry(optionQStyleOptionViewItem.rect)
		elif column == 2:
			editorQWidget.setGeometry(optionQStyleOptionViewItem.rect)
		elif column == 3:
			editorQWidget.setGeometry(optionQStyleOptionViewItem.rect)
		else:
			QtGui.QItemDelegate.updateEditorGeometry(self, editorQWidget, optionQStyleOptionViewItem, indexQModelIndex)

	def requestNewPath (self, indexQModelIndex):
		self.emit(QtCore.SIGNAL('requestNewPath'), indexQModelIndex)

	def paint (self, painterQPainter, optionQStyleOptionViewItem, indexQModelIndex):
		column = indexQModelIndex.column()
		if column == 1:
			value, _ = indexQModelIndex.model().data(indexQModelIndex, QtCore.Qt.EditRole).toInt()
			textQStyleOptionViewItem = optionQStyleOptionViewItem
			textQStyleOptionViewItem.displayAlignment = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
			currentQRect = QtCore.QRect(optionQStyleOptionViewItem.rect)
			currentQRect.setWidth(currentQRect.width() - 22)
			self.drawDisplay(painterQPainter, textQStyleOptionViewItem, currentQRect, QtCore.QString(str(value)));
			spinBoxQStyleOptionSpinBox = QtGui.QStyleOptionSpinBox()
			spinBoxQStyleOptionSpinBox.rect = QtCore.QRect(optionQStyleOptionViewItem.rect)
			QtGui.QApplication.style().drawComplexControl(QtGui.QStyle.CC_SpinBox, spinBoxQStyleOptionSpinBox, painterQPainter)
		elif column == 2:
			textQStyleOptionViewItem = optionQStyleOptionViewItem
			textQStyleOptionViewItem.displayAlignment = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
			QtGui.QItemDelegate.paint(self, painterQPainter, textQStyleOptionViewItem, indexQModelIndex)
		elif column == 3:
			textQString = indexQModelIndex.model().data(indexQModelIndex, QtCore.Qt.EditRole).toString()
			buttonQStyleOptionButton = QtGui.QStyleOptionButton()
			buttonQStyleOptionButton.rect = QtCore.QRect(optionQStyleOptionViewItem.rect)
			buttonQStyleOptionButton.text = textQString
			buttonQStyleOptionButton.state = QtGui.QStyle.State_Active
			QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_PushButton, buttonQStyleOptionButton, painterQPainter)
		else:
			QtGui.QItemDelegate.paint(self, painterQPainter, optionQStyleOptionViewItem, indexQModelIndex)

class QCustomTreeWidget (QtGui.QTreeWidget):
	def __init__(self, parent = None):
		super(QCustomTreeWidget, self).__init__(parent)
		# self.setDragEnabled(False)
		# self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		self.setColumnCount(5)
		self.setHeaderLabels(("Order", "Frame Padding", "Frame Offset", "Image Extension", "Image Location" ))
		myQCustomDelegate = QCustomDelegate()
		self.setItemDelegate(myQCustomDelegate)
		self.connect(myQCustomDelegate, QtCore.SIGNAL('requestNewPath'), self.getNewPath)

	def addMenu (self, title, value, text, path, parentQTreeWidgetItem = None):
		if parentQTreeWidgetItem == None:
			parentQTreeWidgetItem = self.invisibleRootItem()
		currentQTreeWidgetItem = QtGui.QTreeWidgetItem(parentQTreeWidgetItem)
		currentQTreeWidgetItem.setData(0, QtCore.Qt.EditRole, title)
		currentQTreeWidgetItem.setData(1, QtCore.Qt.EditRole, value)
		currentQTreeWidgetItem.setData(2, QtCore.Qt.EditRole, text)
		currentQTreeWidgetItem.setData(3, QtCore.Qt.EditRole, path)
		currentQTreeWidgetItem.setFlags(currentQTreeWidgetItem.flags() | QtCore.Qt.ItemIsEditable)
		for i in range(self.columnCount()):
			currentQSize = currentQTreeWidgetItem.sizeHint(i)
			currentQTreeWidgetItem.setSizeHint(i, QtCore.QSize(currentQSize.width(), currentQSize.height() + 40))

	def getNewPath (self, indexQModelIndex):
		currentQTreeWidgetItem = self.itemFromIndex(indexQModelIndex)
		pathQStringList = QtGui.QFileDialog.getOpenFileNames()
		if pathQStringList.count() > 0:
			textQString = pathQStringList.first()
			currentQTreeWidgetItem.setData(indexQModelIndex.column(), QtCore.Qt.EditRole, textQString)

class QCustomQWidget (QtGui.QWidget):
	def __init__ (self, parent = None):
		super(QCustomQWidget, self).__init__(parent)
		self.myQCustomTreeWidget = QCustomTreeWidget(self)
		self.allQHBoxLayout = QtGui.QHBoxLayout()
		self.allQHBoxLayout.addWidget(self.myQCustomTreeWidget)
		self.setLayout(self.allQHBoxLayout)
		self.myQCustomTreeWidget.addMenu('1', 4, 'A', 'home/Meyoko/Desktop')
		self.myQCustomTreeWidget.addMenu('2', 4, 'B', 'home/Kitsune/Desktop')
		self.myQCustomTreeWidget.addMenu('3', 4, 'C', 'c:/temp')

app = QtGui.QApplication([])
myQCustomQWidget = QCustomQWidget()
myQCustomQWidget.show()
sys.exit(app.exec_())