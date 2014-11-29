from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from core.dialogs.main_window import MainWindow
from core import settings


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = MainWindow()
    screen.show()

    exitcode = app.exec_()
    settings.save()
    sys.exit(exitcode)
