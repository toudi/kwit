from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from core.dialogs.abstract import AbstractWindow
from core.models.kontrahent import Kontrahent
from core import db

model = Kontrahent.get_qmodel_class()

class ContactsList(QDialog, AbstractWindow):

    def setupUI(self):
        layout = QVBoxLayout()

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(QLabel("Filtrowanie"))
        self.leFilter = QLineEdit()
        searchLayout.addWidget(self.leFilter)

        centralLayout = QHBoxLayout()
        self.tvContacts = QTableView()
        self.tvContacts.setModel(model)
        self.tvContacts.resizeColumnsToContents()
        self.tvContacts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tvContacts.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tvContacts.setColumnHidden(model.cols_indexes["id"], True)
        self.tvContacts.setColumnHidden(model.cols_indexes["adres"], True)

        self.tbAdd = QToolButton()
        self.tbEdit = QToolButton()
        self.tbDelete = QToolButton()
        self.tbAdd.setText("Dodaj")
        self.tbAdd.setIcon(QIcon('static/img/add-contact.svg'))
        self.tbAdd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbEdit.setText("Edytuj")
        self.tbEdit.setIcon(QIcon('static/img/edit-contact.svg'))
        self.tbEdit.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbDelete.setText("Usuń")
        self.tbDelete.setIcon(QIcon('static/img/delete.svg'))
        self.tbDelete.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        actionsLayout = QVBoxLayout()
        actionsLayout.addWidget(self.tbAdd)
        actionsLayout.addWidget(self.tbEdit)
        actionsLayout.addWidget(self.tbDelete)
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

        self.tbEdit.clicked.connect(self.editContact)
        self.tbAdd.clicked.connect(self.addContact)
        self.tbDelete.clicked.connect(self.deleteContact)

    def editContact(self):
        index = self.tvContacts.currentIndex()
        if index.isValid():
            return EditContact(parent=self, index=index).exec()

    def addContact(self):
        return EditContact(parent=self).exec()

    def deleteContact(self):
        index = self.tvContacts.currentIndex()
        if index.isValid():
            confirmation = QMessageBox.question(
                self,
                "Potwierdź usunięcie",
                "Czy napewno usunąć rekord?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                model.query.filter(Kontrahent.id == model.getId(index)).delete()
                model.refresh()


class EditContact(QDialog, AbstractWindow):
    def __init__(self, parent, index = None, *args, **kwargs):
        self.index = index
        self.kontrahent = Kontrahent()
        # load data from db
        if self.index:
            pk = model.data(
                model.createIndex(
                    self.index.row(), 
                    model.cols_indexes["id"]
                ), Qt.EditRole)
            self.kontrahent = model.query.get(pk)

        return super(EditContact, self).__init__(parent=parent, *args, **kwargs)

    def setupUI(self):
        editLayout = QFormLayout()
        mainLayout = QVBoxLayout()

        self.leNazwa = QLineEdit(self.kontrahent.nazwa)
        self.pteAdres = QPlainTextEdit(self.kontrahent.adres)
        self.leNIP = QLineEdit(self.kontrahent.nip)
        self.bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)


        editLayout.addRow(QLabel("Nazwa"), self.leNazwa)
        editLayout.addRow(QLabel("Adres"), self.pteAdres)
        editLayout.addRow(QLabel("NIP"), self.leNIP)

        mainLayout.addLayout(editLayout)
        mainLayout.addWidget(self.bb)

        self.setLayout(mainLayout)

        self.bb.rejected.connect(self.reject)
        self.bb.accepted.connect(self.accept)


    def accept(self):
        if len(self.leNazwa.text()):

            self.kontrahent.nazwa = str(self.leNazwa.text())
            self.kontrahent.adres = self.pteAdres.toPlainText()
            self.kontrahent.nip = self.leNIP.text()

            db.session.add(self.kontrahent)
            db.session.commit()

            model.refresh()

            return super(EditContact, self).accept()
