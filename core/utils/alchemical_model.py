#!/usr/bin/env python2
#-*- coding=utf-8 -*-
# © 2013 Mark Harviston, BSD License
from __future__ import absolute_import, unicode_literals, print_function
"""
Qt data models that bind to SQLAlchemy queries
"""
from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
import logging  # noqa


class AlchemicalTableModel(QAbstractTableModel):
	"""
	A Qt Table Model that binds to a SQL Alchemy query

	Example:
	>>> model = AlchemicalTableModel(Session, [('Name', Entity.name)])
	>>> table = QTableView(parent)
	>>> table.setModel(model)
	"""

	def __init__(self, session, model, columns):
		super(AlchemicalTableModel, self).__init__()
		#TODO self.sort_data = None
		self.session = session
		self.fields = columns
		self.query = session.query(model)

		self.results = None
		self.count = None
		self.sort = None
		self.filter = None

		self.cols_indexes = {col[2]: i for i, col in enumerate(columns)}

		self.refresh()

	def getId(self, index, colname='id'):
		return self.data(
			self.createIndex(
				index.row(),
				self.cols_indexes[colname]
			), Qt.EditRole
		)

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.fields[col][0])
		return QVariant()

	def setFilter(self, filter):
		"""Sets or clears the filter, clear the filter by setting to None"""
		self.filter = filter
		self.refresh()

	def refresh(self):
		"""Recalculates, self.results and self.count"""

		self.layoutAboutToBeChanged.emit()

		q = self.query
		if self.sort is not None:
			order, col = self.sort
			col = self.fields[col][1]
			if order == Qt.DescendingOrder:
				col = col.desc()
		else:
			col = None

		if self.filter is not None:
			q = q.filter(self.filter)

		q = q.order_by(col)

		self.results = q.all()
		self.count = q.count()
		self.layoutChanged.emit()

		# start = self.createIndex(0, self.columnCount(None) - 1)
		# end = self.createIndex(self.count, self.columnCount(None) - 1)

		# self.dataChanged.emit(start, end)

	def flags(self, index):
		_flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

		if self.sort is not None:
			order, col = self.sort

			if self.fields[col][3].get('dnd', False) and index.column() == col:

				_flags |= Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

		if self.fields[index.column()][3].get('editable', False):
			_flags |= Qt.ItemIsEditable

		return _flags

	def supportedDropActions(self):
		return Qt.MoveAction

	def dropMimeData(self, data, action, row, col, parent):
		if action != Qt.MoveAction:
			return

		return False

	def rowCount(self, parent):
		return self.count or 0

	def columnCount(self, parent):
		return len(self.fields)

	def data(self, index, role):
		if not index.isValid():
			return QVariant()

		elif role not in (Qt.DisplayRole, Qt.EditRole):
			return QVariant()

		row = self.results[index.row()]
		name = self.fields[index.column()][2]

		return str(getattr(row, name))

	def setData(self, index, value, role=None):
		row = self.results[index.row()]
		name = self.fields[index.column()][2]

		try:
			setattr(row, name, value.toString())
			self.session.commit()
		except Exception as ex:
			QtGui.QMessageBox.critical(None, 'SQL Error', unicode(ex))
			return False
		else:
			self.dataChanged.emit(index, index)
			return True

	def sort(self, col, order):
		"""Sort table by given column number."""
		self.sort = order, col
		self.refresh()
