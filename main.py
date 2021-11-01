import sys

from PyQt5.QtWidgets import QApplication
from loginForm import LoginWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWidget()
    login_window.show()
    sys.exit(app.exec_())