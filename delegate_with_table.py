from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QAbstractItemView

class Delegate(QtWidgets.QItemDelegate):
    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices
    
    def createEditor(self, parent, option, index):

        
        self.editor = QtWidgets.QComboBox(parent)
        self.editor.addItems(self.items)
        if index.column() == 1:
            self.editor.currentIndexChanged.connect(self.parent().onIndexChanged1)
        elif index.column() == 2:
            self.editor.currentIndexChanged.connect(self.parent().onIndexChanged2)


        return self.editor
    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect

        #print(opt.text,opt.text)
        style.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.blockSignals(True)
        editor.setCurrentIndex(num)
        editor.blockSignals(False)
        #if index.column() == 1: #just to be sure that we have a QCombobox
            #editor.showPopup()
    




    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, QtCore.Qt.DisplayRole, QtCore.QVariant(value))
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class Model(QtCore.QAbstractTableModel):
    def __init__(self, table):
        super().__init__()
        self.table = table
    def rowCount(self, parent):
        return len(self.table)
    def columnCount(self, parent):
        return len(self.table[0])
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.table[index.row()][index.column()]
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self.table[index.row()][index.column()] = value
        return True

class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # set combo box choices:
        choices = ['apple', 'orange', 'banana']
        choices2 = ['hi', 'there', 'all']
        # create table data:
        table   = []
        table.append(['A', choices[0],choices2[0]])
        table.append(['B', choices[1],choices2[2]])
        table.append(['C', choices[0],choices2[1]])
        table .append(['D', choices[2],choices2[1]])
        # create table view:
        self.model     = Model(table)
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.model)

        



        #self.tableView.setEditTriggers(QAbstractItemView.CurrentChanged) # this is the one that fits best to your request
        self.tableView.setItemDelegateForColumn(1, Delegate(self,choices))
        self.tableView.setItemDelegateForColumn(2, Delegate(self,choices2))
        # make combo boxes editable with a single-click:
        for row in range( len(table) ):
            self.tableView.openPersistentEditor(self.model.index(row, 1))
            self.tableView.openPersistentEditor(self.model.index(row, 2))
         #initialize
        self.setCentralWidget(self.tableView)
        self.setWindowTitle('Delegate Test')
        self.show()
    
    def onIndexChanged1(self):
        print('selection col 1 changed')
    def onIndexChanged2(self):
        print('selection col 2 changed')


    #def __init__(self, parent=None):
        #super(Main, self).__init__(parent)
        #self.model = Model()
        #self.table = QtWidgets.QTableView()
        #self.table.setModel(self.model)
        #self.table.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged) # this is the one that fits best to your request
        #self.table.setItemDelegateForColumn(1, Delegate(self, ["apple", "orange", "banana"]))
        #self.setCentralWidget(self.table)
        #self.setWindowTitle('Delegate Test')
        #self.show()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    app.exec_()