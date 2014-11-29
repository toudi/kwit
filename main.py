from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from dialogs.main_window import MainWindow


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = MainWindow()
    screen.show()

    sys.exit(app.exec_())
