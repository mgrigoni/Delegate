
import numpy as np
import pandas as pd

#from PyQt5 import uic, QtCore, #, QtGui

from PyQt5 import uic, QtCore,QtGui,QtWidgets

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
        
        if (index.column() == 3):
           return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        

    def data(self, index, role):

        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignLeft |QtCore.Qt.AlignVCenter
            
     

    def setData(self, index, value, role):

        if role == QtCore.Qt.EditRole:
            # execute change in value and fire datachanged signal only if 
            # arriving new value is different
            if self._data.iloc[index.row(), index.column()]!=value:
                self._data.iloc[index.row(), index.column()] = value
                if index.column()==4:
                    self._data.iloc[index.row(), 1] = value
                    self.layoutChanged.emit() 
                self.dataChanged.emit(index, index) #, (QtCore.Qt.DisplayRole,))
                return True
            else:
                return False
        else:
            return False


class ComboBoxDelegate(QtWidgets.QItemDelegate):

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

class CheckBoxDelegate(QtWidgets.QItemDelegate):

    def __init__(self, owner):
        super().__init__(owner)
    
    def createEditor(self, parent, option, index):
        ## we do not want to create an editor, therefore we return none
        return None

    def paint(self, painter, option, index):
        
        checked = self.str_to_bool(index.data())

        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionButton()
        opt.state |=QtWidgets.QStyle.State_Enabled

        if checked:
            opt.state |= QtWidgets.QStyle.State_On
        else:
            opt.state |= QtWidgets.QStyle.State_Off

        opt.rect = self.getCheckBoxRect(option)

        style.drawControl(QtWidgets.QStyle.CE_CheckBox, opt, painter)

        #self.drawCheck(painter, option, option.rect, checked)
        #self.drawFocus(painter, option, option.rect)
    
    def getCheckBoxRect(self, option):
        check_box_style_option = QtWidgets.QStyleOptionButton()
        check_box_rect = QtWidgets.QApplication.style().subElementRect(QtWidgets.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QtCore.QPoint (option.rect.x() +
                             option.rect.width() / 2 -
                             check_box_rect.width() / 2,
                             option.rect.y() +
                             option.rect.height() / 2 -
                             check_box_rect.height() / 2)
        return QtCore.QRect(check_box_point, check_box_rect.size())

  
    def setEditorData(self, editor, index):
        pass

    def editorEvent(self, event, model, option, index):
    
        # Change the checkbox-state
         # Do not change the checkbox-state
        if event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() != QtCore.Qt.LeftButton:
                return False
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Select:
                return False
        else:
            return False

        self.setModelData(None, model, index)
        return True
 
    def setModelData(self, editor, model, index):

        checked = not self.str_to_bool(index.data())
        
        if checked:
            self.newValue='True'
        else:
            self.newValue='False'

        model.setData(index, self.newValue, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def str_to_bool(self,s):

        if s == 'True':
            return True
        elif s == 'False':
            return False

class ColorBoxDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, owner):
        super().__init__(owner)

    def paint(self, painter, option, index):

        txt= index.data()

        painter.setBrush(QtGui.QColor(txt))
        painter.setPen(QtGui.QColor(txt))

        
        dy=option.rect.height()/2
        dx=dy

        x=option.rect.x()+dx
        y=int(option.rect.y()+dy/2)

        painter.drawRect(x,y,dx,dy)

        rct = QRect(x+dx, y, 100, 50);


        #painter.drawText(x+dx,y+dy,txt)
        painter.drawText(rct,Qt.AlignVCenter,txt)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        uic.loadUi("tableView.ui", self)    

        tags=['Tag 1','Tag 2','Tag 3','Tag 4','Tag 5',]
        axes=['Left','Right 1','Right 2']
        colors=['red','green','blue','magenta','orange']

        self.df = pd.DataFrame()
        file="C:\\Users\\grigonim\\Documents\\Apps\\Delegate\\data_checkbox.csv"
        self.df = pd.read_csv(file)

        self.model= PandasModel(self.df)
        
        self.viewTable.setModel(self.model)

        self.model.dataChanged.connect(self.onPandasDataChanged)

        self.viewTable.setColumnWidth(0,50)
        self.viewTable.setColumnWidth(1,100)
        

        self.viewTable.setItemDelegateForColumn(0, CheckBoxDelegate(self))
        self.viewTable.setItemDelegateForColumn(1, ColorBoxDelegate(self))
        self.viewTable.setItemDelegateForColumn(2, ComboBoxDelegate(self,tags))
        self.viewTable.setItemDelegateForColumn(3, ComboBoxDelegate(self,axes))
        self.viewTable.setItemDelegateForColumn(4, ComboBoxDelegate(self,colors))

        for row in range(self.df.shape[0]):
            
            self.viewTable.openPersistentEditor(self.model.index(row, 2))
            self.viewTable.openPersistentEditor(self.model.index(row, 3))
            self.viewTable.openPersistentEditor(self.model.index(row, 4))


        self.show()

    def onPandasDataChanged(self):
        
        print(' ')
        print(self.df)


    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
