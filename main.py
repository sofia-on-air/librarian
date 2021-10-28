import sys
import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget

from MessageBox import show_error
from mainForm import MainFormWidget


class LoginWidget(QWidget):
    logged = False
    main_window = None

    def __init__(self):
        super().__init__()
        uic.loadUi('LoginForm.ui', self)  # Загружаем дизайн
        # Отключаем кнопки минимизации и разворачивания
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
        self.loginButton.clicked.connect(self.login_click)

    def login_click(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()
        # Проверка на наличие логина и пароля
        if login == '' or password == '':
            show_error(self, 'Логин и пароль должны быть введены!')
            return
        # Проверка наличия пользователя в базе
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT id
            FROM users
            WHERE login = ? AND password = ?""", (login, password)).fetchall()
        if len(result) > 0:
            self.logged = True
        else:
            self.logged = False
        con.close()
        if self.logged:
            # Если пользователь есть, открыть основное окно
            self.hide()
            self.main_window = MainFormWidget()
            self.main_window.show()
            return
        else:
            # Если пользователя нет, показываем ошибку
            show_error(self, 'Пользователь с таким логином и паролем не найден!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWidget()
    login_window.show()
    sys.exit(app.exec_())