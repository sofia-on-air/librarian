import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QAbstractItemView

from MessageBox import show_warning
from bookForm import BookForm
from readersForm import ReadersForm


class MainForm(QWidget):
    book_form = None
    readers_form = None

    def __init__(self):
        super().__init__()
        uic.loadUi('MainForm.ui', self)  # Загружаем дизайн
        # Отключаем кнопки минимизации и разворачивания
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)

        self.searchButton.clicked.connect(self.show_books)
        self.addButton.clicked.connect(self.add_click)
        self.readersButton.clicked.connect(self.readers_click)
        # По двойному щелчку будет редактирование
        self.booksWidget.cellDoubleClicked.connect(self.edit_book)
        # Редактирование самой таблицы запретим
        self.booksWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Показываем список
        self.show_books()

    def show_books(self):
        # Параметры поиска
        title = '%' + self.titleEdit.text() + '%'
        author = '%' + self.authorEdit.text() + '%'
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT Id, Title, Author, Count, Place
            FROM books
            WHERE Title LIKE ? AND Author LIKE ?""", (title, author)).fetchall()
        # Заполним размеры таблицы
        self.booksWidget.setColumnCount(5)
        self.booksWidget.setRowCount(0)
        # Заполним заголовки столбцов
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
        # Если не нашли ни одной книги, показываем ошибку
        if len(result) == 0:
            show_warning(self, 'Книг по вашему критерию не найдено.\nПопробуйте исправить критерии поиска.')
        con.close()

    def add_click(self):
        self.book_form = BookForm(0)
        result = self.book_form.exec()
        # Если что-то сделали, нужно перезагрузить список книг
        if result == QMessageBox.Ok:
            self.show_books()

    def edit_book(self, row, column):
        # Достанем данные книги из таблицы
        book_id = int(self.booksWidget.item(row, 0).text())
        title = self.booksWidget.item(row, 1).text()
        author = self.booksWidget.item(row, 2).text()
        count = int(self.booksWidget.item(row, 3).text())
        place = self.booksWidget.item(row, 4).text()
        self.book_form = BookForm(book_id, author, title, count, place)
        result = self.book_form.exec()
        # Если что-то сделали, нужно перезагрузить список книг
        if result == QMessageBox.Ok:
            self.show_books()

    def readers_click(self):
        self.readers_form = ReadersForm()
        self.readers_form.show()
