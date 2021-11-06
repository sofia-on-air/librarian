import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QAbstractItemView, QTableWidgetItem

from MessageBox import show_question, show_warning


class GiveBookForm(QDialog):
    reader_id = 0

    def __init__(self, reader_id):
        super().__init__()
        uic.loadUi('GiveBookDialog.ui', self)  # Загружаем дизайн
        self.searchButton.clicked.connect(self.show_books)
        # Запомним начальные значения
        self.reader_id = reader_id
        # По двойному щелчку будет редактирование
        self.booksWidget.cellDoubleClicked.connect(self.table_click)
        # Редактирование самой таблицы запретим
        self.booksWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Показываем список
        self.show_books()

    def table_click(self, row, column):
        # Подтверждение выдачи
        result = show_question(self, 'Вы уверены, что хотите выдать книгу?', 'Подтверждение')
        if result == QMessageBox.Yes:
            # Достанем данные книги из таблицы
            book_id = int(self.booksWidget.item(row, 0).text())
            # Подключение к БД
            con = sqlite3.connect('librarian.sqlite')
            cur = con.cursor()
            # Выполнение запроса удаления
            cur.execute("""INSERT INTO given_books (BookId, ReaderId, GivenDate, ExpirationDate)
                            VALUES (?, ?, date('now'), date('now','+14 days'))""", (book_id, self.reader_id)).fetchall()
            con.commit()
            con.close()
            # Закрываем диалог с результатом
            self.done(QMessageBox.Ok)

    def show_books(self):
        # Параметры поиска
        title = '%' + self.searchEdit.text() + '%'
        author = '%' + self.searchEdit.text() + '%'
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        result = cur.execute("""
                    SELECT
                        books.Id,
                        books.Title,
                        books.Author,
                        books.Place,
                        (SELECT COUNT(given_books.Id) FROM given_books
                            WHERE given_books.BookId = books.Id AND given_books.ReturnDate IS NULL) AS Given
                    FROM
                        books
                    WHERE
                        books.Count > Given
                        AND (books.Title LIKE ? OR books.Author LIKE ?)""", (title, author)).fetchall()
        # Заполним размеры таблицы
        self.booksWidget.setColumnCount(4)
        self.booksWidget.setRowCount(0)
        # Заполним заголовки столбцов
        self.booksWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str('Номер')))
        self.booksWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str('Название')))
        self.booksWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str('Автор')))
        self.booksWidget.setHorizontalHeaderItem(3, QTableWidgetItem(str('Расположение')))
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.booksWidget.setRowCount(
                self.booksWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.booksWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        # Если не нашли ни одной книги, показываем ошибку
        if len(result) == 0:
            show_warning(self, 'Книг по вашему критерию не найдено.\nПопробуйте исправить критерии поиска.')
        con.close()