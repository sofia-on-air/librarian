import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QAbstractItemView, QTableWidgetItem

from MessageBox import show_question


class ReturnBookForm(QDialog):
    reader_id = 0

    def __init__(self, reader_id):
        super().__init__()
        uic.loadUi('ReturnBookDialog.ui', self)  # Загружаем дизайн
        # Запомним начальные значения
        self.reader_id = reader_id
        # По двойному щелчку будет редактирование
        self.booksWidget.cellDoubleClicked.connect(self.table_click)
        # Редактирование самой таблицы запретим
        self.booksWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Показываем список
        self.show_books()

    def show_books(self):
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        result = cur.execute("""
                    SELECT
                        given_books.Id,
                        books.Title,
                        books.Author
                    FROM
                        given_books JOIN books ON given_books.BookId = books.Id
                    WHERE
                        given_books.ReaderId = ? AND given_books.ReturnDate IS NULL""", (self.reader_id, )).fetchall()
        # Заполним размеры таблицы
        self.booksWidget.setColumnCount(3)
        self.booksWidget.setRowCount(0)
        # Заполним заголовки столбцов
        self.booksWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str('Номер выдачи')))
        self.booksWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str('Название')))
        self.booksWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str('Автор')))
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.booksWidget.setRowCount(
                self.booksWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.booksWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()

    def table_click(self, row, column):
        # Подтверждение выдачи
        result = show_question(self, 'Вы уверены, что хотите сдать книгу?', 'Подтверждение')
        if result == QMessageBox.Yes:
            # Достанем данные книги из таблицы
            given_id = int(self.booksWidget.item(row, 0).text())
            # Подключение к БД
            con = sqlite3.connect('librarian.sqlite')
            cur = con.cursor()
            # Выполнение запроса удаления
            cur.execute("""UPDATE given_books SET ReturnDate = date('now')
                            WHERE Id = ?""", (given_id,)).fetchall()
            con.commit()
            con.close()
            # Закрываем диалог с результатом
            self.done(QMessageBox.Ok)
