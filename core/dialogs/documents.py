from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from core.dialogs.abstract import AbstractWindow
from core import settings
from importlib import import_module


class DocumentsList(AbstractWindow, QDialog):

    def setupUI(self):
        # cache modulow
        self.document_types = {}

        mainLayout = QVBoxLayout()

        self.lwDocumentType = QListWidget()
        self.tvDocuments = QTableView()

        self.lwDocumentType.setMaximumWidth(200)

        self.cbMonth = QComboBox()
        self.sbYear = QSpinBox()

        monthPickLayout = QHBoxLayout()
        monthPickLayout.addWidget(self.cbMonth)
        monthPickLayout.addWidget(self.sbYear)
        monthPickLayout.addSpacerItem(
            QSpacerItem(
                0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
            )
        )

        documentsListLayout = QVBoxLayout()
        documentsListLayout.addLayout(monthPickLayout)
        documentsListLayout.addWidget(self.tvDocuments)

        self.gbBatchActions = QGroupBox("Zaznaczone")

        self.tbPrint = QToolButton()
        self.tbPrint.setText("Wydrukuj")
        self.tbPrint.setIcon(QIcon("static/img/print.svg"))
        self.tbPrint.setIconSize(QSize(25, 25))
        self.tbPrint.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tbPDF = QToolButton()
        self.tbPDF.setText("PDF")
        self.tbPDF.setIcon(QIcon("static/img/pdf.svg"))
        self.tbPDF.setIconSize(QSize(25, 25))
        self.tbPDF.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        batchActionsLayout = QHBoxLayout()
        batchActionsLayout.addWidget(self.tbPrint)
        batchActionsLayout.addWidget(self.tbPDF)
        self.gbBatchActions.setLayout(batchActionsLayout)

        actionsLayout = QHBoxLayout()
        actionsLayout.addWidget(self.gbBatchActions)

        documentsListLayout.addLayout(actionsLayout)

        container = QHBoxLayout()
        container.addWidget(self.lwDocumentType)
        container.addLayout(documentsListLayout)

        mainLayout.addLayout(container)

        self.bb = QDialogButtonBox(QDialogButtonBox.Close)
        mainLayout.addWidget(self.bb)
        self.setLayout(mainLayout)

        self.bb.rejected.connect(self.reject)

        self.sbYear.setMaximum(QDate.currentDate().year())
        self.sbYear.setValue(QDate.currentDate().year())

        for month in range(12):
            self.cbMonth.addItem(
                QDate.longMonthName(
                    month + 1, QDate.StandaloneFormat
                )
            )

        self.cbMonth.setCurrentIndex(
            QDate.currentDate().month() - 1
        )

        self.lwDocumentType.itemSelectionChanged.connect(
            self.document_type_selected)

        # ladowanie typow dokumentow
        for doctype in settings.get_array(
            'DOCUMENT_TYPES', ['document_types.faktura_np', 'document_types.faktura_vat']
        ):
            doc_module = import_module(doctype)
            self.document_types[doctype] = doc_module
            doc_module_item = QListWidgetItem(getattr(doc_module, 'NAZWA', doctype))
            doc_module_item.setData(Qt.UserRole, doctype)

            self.lwDocumentType.addItem(
                doc_module_item
            )

    def document_type_selected(self):
        doctype = self.lwDocumentType.currentItem().data(Qt.UserRole)
        
        model = self.document_types[doctype].MODEL.get_qmodel_class()
        self.tvDocuments.setModel(model)
