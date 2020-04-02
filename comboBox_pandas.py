
import numpy as np
import pandas as pd

#from PyQt5 import uic, QtCore, #, QtGui

from PyQt5 import uic, QtCore,QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import sys
import os

class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, table):
        super().__init__()
        self._data = table
        

    def rowCount(self, parent):
        return self._data.shape[0]

    def columnCount(self, parent):
        return self._data.shape[1]

    def flags(self, index):

        if (index.column() == 1):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignCenter

    def setData(self, index, value, role):

        if role == QtCore.Qt.EditRole:
            # execute change in value and fire datachanged signal only if 
            # arriving new value is different
            if self._data.iloc[index.row(), index.column()]!=value:
                self._data.iat[index.row(), index.column()] = value     
                self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
                return True
            else:
                return False
        else:
            return False


class Delegate(QtWidgets.QItemDelegate):

    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices
    
    def createEditor(self, parent, option, index):

        editor = QtWidgets.QComboBox(parent)
        editor.addItems(self.items)
        
        editor.currentIndexChanged.connect(self.commitEditor)
        return editor

    def commitEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def paint(self, painter, option, index):

        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

    def setEditorData(self, editor, index):

        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.blockSignals(True)
        editor.setCurrentIndex(num)
        editor.blockSignals(False)
 
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        #print(value)
        model.setData(index, value,QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        uic.loadUi("tableView.ui", self)    

        
        tags=['Tag 1','Tag 2','Tag 3','Tag 4','Tag 5',]
        axes=['Left','Right 1','Right 2']
        colors=['Red','Green','Blue','Magenta','Orange']

        self.df = pd.DataFrame()
        file="C:\\Users\\grigonim\\Documents\\Apps\\Delegate\\data.csv"
        self.df = pd.read_csv(file)

        model= PandasModel(self.df)
        
        self.viewTable.setModel(model)

        model.dataChanged.connect(self.onPandasDataChanged)

        self.viewTable.setItemDelegateForColumn(1, Delegate(self,tags))
        self.viewTable.setItemDelegateForColumn(2, Delegate(self,axes))
        self.viewTable.setItemDelegateForColumn(3, Delegate(self,colors))

        for row in range(self.df.shape[0]):

            self.viewTable.openPersistentEditor(model.index(row, 1))
            self.viewTable.openPersistentEditor(model.index(row, 2))
            self.viewTable.openPersistentEditor(model.index(row, 3))


        self.show()

    def onIndexChanged(self):
        pass
        #print('selection changed')
        
        
        #print(self.table)
    def onPandasDataChanged(self):
        print('received signal')
        print(self.df)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
