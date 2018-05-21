import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TableModel(QAbstractTableModel):
    def __init__(self, parent, data_list, column_models, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.data_list = data_list
        self.column_models = column_models

    def rowCount(self, parent):
        return len(self.data_list)

    def columnCount(self, parent):
        return len(self.column_models)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        column_model = self.column_models[index.column()]
        object_data = self.data_list[index.row()]
        data_in_row_column = str(column_model.get_data_func(object_data))
        return data_in_row_column

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.column_models[col].name
        return None
