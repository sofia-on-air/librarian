import sys
import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QWidget


class MainFormWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainForm.ui', self)  # Загружаем дизайн
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
        # self.loginButton.clicked.connect(self.login_click)
        self.showBooks()

    def showBooks(self):
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT Id, Title, Author, Count, Place
            FROM books""").fetchall()
        # Заполним размеры таблицы
        self.booksWidget.setColumnCount(5)
        self.booksWidget.setRowCount(0)
        self.booksWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str('Номер')))
        self.booksWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str('Название')))
        self.booksWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str('Автор')))
        self.booksWidget.setHorizontalHeaderItem(3, QTableWidgetItem(str('Количество')))
        self.booksWidget.setHorizontalHeaderItem(4, QTableWidgetItem(str('Расположение')))
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.booksWidget.setRowCount(
                self.booksWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.booksWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()

    # def login_click(self):
    #     login = self.loginEdit.text()
    #     password = self.passwordEdit.text()
    #     if login == '' or password == '':
    #         dlg = QMessageBox(self)
    #         dlg.setWindowTitle("Ошибка")
    #         dlg.setText("Логин и пароль должны быть введены!")
    #         dlg.setStandardButtons(QMessageBox.Ok)
    #         dlg.setIcon(QMessageBox.Critical)
    #         dlg.exec()
    #         return

    #     # Подключение к БД
    #     con = sqlite3.connect('librarian.sqlite')
    #     # Создание курсора
    #     cur = con.cursor()
    #     # Выполнение запроса и получение всех результатов
    #     result = cur.execute("""SELECT id
    #         FROM users
    #         WHERE login = ? AND password = ?""", (login, password)).fetchall()
    #     if len(result) > 0:
    #         self.logged = True
    #     else:
    #         self.logged = False
    #     con.close()
    #     if self.logged:
    #         self.close()
    #         return
    #     else:
    #         dlg = QMessageBox(self)
    #         dlg.setWindowTitle("Ошибка")
    #         dlg.setText("Пользователь с таким логином и паролем не найден!")
    #         dlg.setStandardButtons(QMessageBox.Ok)
    #         dlg.setIcon(QMessageBox.Critical)
    #         dlg.exec()
