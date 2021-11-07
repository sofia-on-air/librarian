import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableWidgetItem


class StatForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('StatForm.ui', self)  # Загружаем дизайн
        self.checkBox.clicked.connect(self.show_books)
        # Редактирование самой таблицы запретим
        self.booksWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Показываем список
        self.show_books()

    def show_books(self):
        result = None
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        if self.checkBox.isChecked():
            result = cur.execute("""
                                    SELECT
                                        books.Title,
                                        books.Author,
                                        readers.Surname,
                                        readers.Name,
                                        readers.PatronymicName,
                                        readers.PhoneNumber,
                                        given_books.GivenDate,
                                        given_books.ExpirationDate
                                    FROM
                                        given_books
                                        JOIN books ON given_books.BookId = books.Id
                                        JOIN readers ON given_books.ReaderId = readers.Id
                                    WHERE
                                        given_books.ReturnDate IS NULL
                                        AND given_books.ExpirationDate < date('now')""").fetchall()
        else:
            result = cur.execute("""
                        SELECT
                            books.Title,
                            books.Author,
                            readers.Surname,
                            readers.Name,
                            readers.PatronymicName,
                            readers.PhoneNumber,
                            given_books.GivenDate,
                            given_books.ExpirationDate
                        FROM
                            given_books
                            JOIN books ON given_books.BookId = books.Id
                            JOIN readers ON given_books.ReaderId = readers.Id
                        WHERE
                            given_books.ReturnDate IS NULL""").fetchall()
        # Заполним размеры таблицы
        self.booksWidget.setColumnCount(8)
        self.booksWidget.setRowCount(0)
        # Заполним заголовки столбцов
        self.booksWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str('Название')))
        self.booksWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str('Автор')))
        self.booksWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str('Фамилия')))
        self.booksWidget.setHorizontalHeaderItem(3, QTableWidgetItem(str('Имя')))
        self.booksWidget.setHorizontalHeaderItem(4, QTableWidgetItem(str('Отчество')))
        self.booksWidget.setHorizontalHeaderItem(5, QTableWidgetItem(str('Телефон')))
        self.booksWidget.setHorizontalHeaderItem(6, QTableWidgetItem(str('Дата выдачи')))
        self.booksWidget.setHorizontalHeaderItem(7, QTableWidgetItem(str('Срок сдачи')))
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.booksWidget.setRowCount(
                self.booksWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.booksWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()


