import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QSpinBox

from MessageBox import show_error


class BookForm(QDialog):
    book_id = 0
    author = ''
    title = ''
    count = 0
    place = ''

    def __init__(self, book_id, author='', title='', count=0, place=''):
        super().__init__()
        uic.loadUi('BookDialog.ui', self)  # Загружаем дизайн
        self.deleteButton.clicked.connect(self.delete_click)
        self.okButton.clicked.connect(self.ok_click)
        self.cancelButton.clicked.connect(self.cancel_click)
        # Запомним начальные значения
        self.book_id = book_id
        self.author = author
        self.title = title
        self.count = count
        self.place = place
        # Если это новая книга, отключим кнопку удаления
        if self.book_id == 0:
            self.deleteButton.setEnabled(False)
            self.setWindowTitle('Новая книга')
        else:
            # Если это редактирование книги, заполним поля
            self.deleteButton.setEnabled(True)
            self.setWindowTitle('Редактирование книги')
            self.authorEdit.setText(author)
            self.titleEdit.setText(title)
            self.countEdit.setValue(count)
            self.placeEdit.setText(place)

    def delete_click(self):
        # Подтверждение удаления
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Удалить?")
        dlg.setText("Вы уверены, что хотите удалить книгу?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        result = dlg.exec()
        if result == QMessageBox.Yes:
            # Подключение к БД
            con = sqlite3.connect('librarian.sqlite')
            cur = con.cursor()
            # Выполнение запроса удаления
            cur.execute("""DELETE FROM books WHERE Id = ?""", (self.book_id,)).fetchall()
            con.commit()
            con.close()
            # Закрываем диалог с результатом
            self.done(QMessageBox.Ok)

    def cancel_click(self):
        # Закрываем диалог с результатом
        self.done(QMessageBox.Cancel)

    def ok_click(self):
        result = False
        if self.book_id == 0:
            result = self.create_book()
        else:
            result = self.update_book()
        # Закрываем диалог с результатом
        if result:
            self.done(QMessageBox.Ok)

    def is_book_ok(self):
        if self.titleEdit.text() == '':
            show_error(self, 'Название книги отсутствует')
            return False
        if self.authorEdit.text() == '':
            show_error(self, 'Автор книги отсутствует')
            return False
        if self.placeEdit.text() == '':
            show_error(self, 'Расположение книги отсутствует')
            return False
        if self.countEdit.value() == 0:
            show_error(self, 'Количество книги не указано')
            return False
        return True

    def create_book(self):
        if not self.is_book_ok():
            return False
        # Заберём новые значения
        self.title = self.titleEdit.text()
        self.author = self.authorEdit.text()
        self.count = self.countEdit.value()
        self.place = self.placeEdit.text()
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        # Добавляем книгу
        cur.execute("""INSERT INTO books
            (Author, Title, Count, Place)
            VALUES (?, ?, ?, ?)""", (self.author, self.title, self.count, self.place)).fetchall()
        con.commit()
        con.close()
        return True

    def update_book(self):
        if not self.is_book_ok():
            return False
        # Обновляем данные о книге, если они изменились
        if self.title != self.titleEdit.text() \
                or self.author != self.authorEdit.text() \
                or self.count != self.countEdit.value() \
                or self.place != self.placeEdit.text():
            # Заберём новые значения
            self.title = self.titleEdit.text()
            self.author = self.authorEdit.text()
            self.count = self.countEdit.value()
            self.place = self.placeEdit.text()
            # Подключение к БД
            con = sqlite3.connect('librarian.sqlite')
            cur = con.cursor()
            # Выполнение запроса обновления
            cur.execute("""UPDATE books
                SET Author = ?, Title = ?, Count = ?, Place = ?
                WHERE Id = ?""", (self.author, self.title, self.count, self.place, self.book_id)).fetchall()
            con.commit()
            con.close()
        return True
