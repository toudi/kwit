from PyQt5 import QtGui
from PyQt5.QtCore import QModelIndex, QAbstractTableModel, QVariant, Qt, pyqtSlot
import logging  # noqa
from PyQt5.QtWidgets import *


class TableModel(QAbstractTableModel):
    def __init__(self, items=None):
        self.items = items or []
        self.columns = []
        self.model_mapping = {}
        self.cols_indexes_cache = None
        super(TableModel, self).__init__()

    def getColNum(self, colname):
        if not self.cols_indexes_cache:
            self.cols_indexes_cache = {}
            for colno, column in enumerate(self.columns):
                self.cols_indexes_cache[column[0]] = colno

        return self.cols_indexes_cache[colname]

    def getColName(self, colnum):
        return self.columns[colnum][0]

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.columns)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.columns[col][1])
        return QVariant()

    def data(self, index, role):
        # print(self.items)
        if not index.isValid():
            return QVariant()

        row = index.row()
        column = index.column()
        colname = self.getColName(column)

        value = self.items[row].get(colname, None)

        if value is not None:
            if role == Qt.DisplayRole:
                if colname in self.model_mapping:
                    MODEL = self.model_mapping[colname].get_qmodel_class()
                    return MODEL.get_by_id(value, MODEL.model.DISPLAY_COLUMN)
                return value
            elif role == Qt.EditRole:
                return value

        return QVariant()

    def setData(self, index, value, role):
        row = index.row()
        column = index.column()

        self.items[row][self.getColName(column)] = value

        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def insertRows(self, row, count, parent):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.items.append({})
        self.endInsertRows()
        return True

    def registerEditors(self, view):
        for colname, model in self.model_mapping.items():
            view.setItemDelegateForColumn(
                self.getColNum(colname),
                ComboDelegate(view, model.get_qmodel_class()))



class ComboDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent, model):

        QItemDelegate.__init__(self, parent)
        self.model = model

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.setModel(self.model)
        combo.currentIndexChanged.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(
            editor.findData(
                index.model().data(index, Qt.EditRole),
                Qt.EditRole
            )
        )
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(
            index,
            editor.itemData(editor.currentIndex(), Qt.EditRole), Qt.EditRole
        )

    # @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

class TableView(QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """
    def __init__(self, *args, **kwargs):
        QTableView.__init__(self, *args, **kwargs)

        # Set the delegate for column 0 of our table
        # self.setItemDelegateForColumn(0, ButtonDelegate(self))
        self.setItemDelegateForColumn(0, ComboDelegate(self))
