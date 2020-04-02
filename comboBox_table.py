
import numpy as np
import pandas as pd

#from PyQt5 import uic, QtCore, #, QtGui

from PyQt5 import uic, QtCore,QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import sys
import os

class Model(QtCore.QAbstractTableModel):
    def __init__(self, table):
        super().__init__()
        self._table = table

    def rowCount(self, parent):
        return len(self._table)

    def columnCount(self, parent):
        return len(self._table[0])

    def flags(self, index):

        if (index.column() == 1):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:          
            return self._table[index.row()][index.column()]

    def setData(self, index, value, role):

        if role == QtCore.Qt.EditRole:
            # execute change in value and fire datachanged signal only if 
            # arriving new value is different
            if self._table[index.row()][index.column()]!=value:
                self._table[index.row()][index.column()] = value    
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
        pass
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
        editor.currentIndexChanged.connect(self.commitEditor)

        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.blockSignals(True)
        editor.setCurrentIndex(num)
        editor.blockSignals(False)
 
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value,QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        uic.loadUi("tableView.ui", self)    

        #self.cmbTag1 = self.findChild(QComboBox, "cmbTag1")
        #self.cmbTag1.currentIndexChanged.connect(self.onTagChange1)

        #self.viewTable=self.findChild(QTableView,'viewTable')
        #self.viewTable.itemChanged.connect(self.onViewTableOptionsChanged)

        
        tags=['Tag 1','Tag 2','Tag 3','Tag 4','Tag 5',]
        axes=['Left','Right 1','Right 2']
        colors=['Red','Green','Blue','Magenta','Orange']

        self.table   = []
        self.table.append(['Series 1', tags[0], axes[0], colors[0] ] )
        self.table.append(['Series 2', tags[1],axes[1],colors[1]])
        self.table.append(['Series 3', tags[2],axes[2],colors[2]])
       
        # create table view:
        model     = Model(self.table)
        self.viewTable.setModel(model)

        model.dataChanged.connect(self.onTableDataChanged)

        

        self.viewTable.setItemDelegateForColumn(1, Delegate(self,tags))
        #self.viewTable.setItemDelegateForColumn(2, Delegate(self,axes))
        #self.viewTable.setItemDelegateForColumn(3, Delegate(self,colors))

        for row in range(len(self.table)):

            self.viewTable.openPersistentEditor(model.index(row, 1))
            #self.viewTable.openPersistentEditor(model.index(row, 2))
            #self.viewTable.openPersistentEditor(model.index(row, 3))


        self.show()

    def onTableDataChanged(self):
        #pass
        print('received signal')
        print(self.table)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
