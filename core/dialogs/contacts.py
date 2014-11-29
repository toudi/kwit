from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from core.dialogs.abstract import AbstractWindow
from core.models.kontrahent import Kontrahent


class ContactsList(QDialog, AbstractWindow):

    def setupUI(self):
        layout = QVBoxLayout()

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(QLabel("Filtrowanie"))
        self.leFilter = QLineEdit()
        searchLayout.addWidget(self.leFilter)

        centralLayout = QHBoxLayout()
        self.tvContacts = QTableView()
        self.tvContacts.setModel(Kontrahent.get_qmodel_class())
        self.tvContacts.resizeColumnsToContents()

        self.tbAdd = QToolButton()
        self.tbEdit = QToolButton()
        self.tbAdd.setText("Dodaj")
        self.tbAdd.setIcon(QIcon('static/img/add-contact.svg'))
        self.tbAdd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbEdit.setText("Edytuj")
        self.tbEdit.setIcon(QIcon('static/img/edit-contact.svg'))
        self.tbEdit.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        actionsLayout = QVBoxLayout()
        actionsLayout.addWidget(self.tbAdd)
        actionsLayout.addWidget(self.tbEdit)
        actionsLayout.addSpacerItem(
            QSpacerItem(
                0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding
            )
        )
        centralLayout.addWidget(self.tvContacts)
        centralLayout.addLayout(actionsLayout)

        self.bb = QDialogButtonBox(QDialogButtonBox.Close)
        layout.addLayout(searchLayout)
        layout.addLayout(centralLayout)
        layout.addWidget(self.bb)

        self.setMinimumSize(QSize(512, 294))

        self.bb.rejected.connect(self.reject)
        self.setLayout(layout)
