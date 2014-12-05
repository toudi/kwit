from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from version import version
from core.dialogs.contacts import ContactsList
from core.dialogs.documents import DocumentsList


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("kwit v. %s" % version)
        self.setupUI()

    def setupUI(self):
        display = QWidget()
        buttonsLayout = QHBoxLayout()

        self.pbDocuments = QToolButton()
        self.pbDocuments.setText("Dokumenty")
        self.pbDocuments.setIcon(QIcon("static/img/documents.svg"))
        self.pbDocuments.setIconSize(QSize(65, 65))
        self.pbDocuments.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.pbContacts = QToolButton()
        self.pbContacts.setText("Kontrahenci")
        self.pbContacts.setIcon(QIcon("static/img/contacts.svg"))
        self.pbContacts.setIconSize(QSize(65, 65))
        self.pbContacts.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.pbSettings = QToolButton()
        self.pbSettings.setText("Ustawienia")
        self.pbSettings.setIcon(QIcon("static/img/settings.svg"))
        self.pbSettings.setIconSize(QSize(65, 65))
        self.pbSettings.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.pbExit = QToolButton()
        self.pbExit.setText("Wyjście")
        self.pbExit.setIcon(QIcon("static/img/exit.svg"))
        self.pbExit.setIconSize(QSize(65, 65))
        self.pbExit.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        buttonsLayout.addWidget(self.pbDocuments)
        buttonsLayout.addWidget(self.pbContacts)
        buttonsLayout.addWidget(self.pbSettings)
        buttonsLayout.addWidget(self.pbExit)

        display.setLayout(buttonsLayout)
        self.setCentralWidget(display)

        self.pbExit.clicked.connect(self.close)
        self.pbContacts.clicked.connect(self.showContactsList)
        self.pbDocuments.clicked.connect(self.showDocumentsList)

    def showContactsList(self):
        ContactsList(parent=self).exec()

    def showDocumentsList(self):
        DocumentsList(parent=self).exec()