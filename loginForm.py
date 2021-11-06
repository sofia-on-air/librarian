import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QWidget

from MessageBox import show_error
from booksForm import BooksForm
from exceptions import EmptyData, WrongCredentials


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
        # По нажатию на enter пытаемся войти
        self.loginEdit.returnPressed.connect(self.login_click)
        self.passwordEdit.returnPressed.connect(self.login_click)

    def login_click(self):
        try:
            self.login_check()
            # Если пользователь есть, открыть основное окно
            self.hide()
            self.main_window = BooksForm()
            self.main_window.show()
        except EmptyData:
            show_error(self, 'Логин и пароль должны быть введены!')
        except WrongCredentials:
            # Если пользователя нет, показываем ошибку
            show_error(self, 'Пользователь с таким логином и паролем не найден!')

    def login_check(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()
        # Проверка на наличие логина и пароля
        if login == '' or password == '':
            raise EmptyData
        # Проверка наличия пользователя в базе
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT id
            FROM users
            WHERE login = ? AND password = ?""", (login, password)).fetchall()
        if len(result) == 0:
            raise WrongCredentials
