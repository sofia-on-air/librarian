import sqlite3, datetime

from PyQt5 import uic
from PyQt5.QtCore import QDate  # Импортируем uic
from PyQt5.QtWidgets import QMessageBox, QDialog

from MessageBox import show_error, show_question


class ReaderForm(QDialog):
    reader_id = 0
    name = ''
    surname = ''
    patronymic_name = ''
    birth_date = ''
    home_address = 0
    phone_number = ''

    def __init__(self, reader_id, name='', surname='', patronymic_name='', birth_date='', home_address='', phone_number=''):
        super().__init__()
        uic.loadUi('ReaderDialog.ui', self)  # Загружаем дизайн
        self.deleteButton.clicked.connect(self.delete_click)
        self.okButton.clicked.connect(self.ok_click)
        self.cancelButton.clicked.connect(self.cancel_click)
        # self.giveButton.clicked.connect(self.give_click)
        # self.returnButton.clicked.connect(self.return_click)
        # Исправим формат отображения даты
        self.dateEdit.setDisplayFormat('yyyy-MM-dd')
        # Запомним начальные значения
        self.reader_id = reader_id
        self.name = name
        self.surname = surname
        self.patronymic_name = patronymic_name
        self.birth_date = birth_date
        self.home_address = home_address
        self.phone_number = phone_number
        # Если это новая книга, отключим кнопку удаления
        if self.reader_id == 0:
            self.deleteButton.setEnabled(False)
            self.setWindowTitle('Новый читатель')
        else:
            # Если это редактирование книги, заполним поля
            self.deleteButton.setEnabled(True)
            self.deleteButton.setStyleSheet("background-color: pink")
            self.setWindowTitle('Редактирование читателя')
            self.nameEdit.setText(name)
            self.surnameEdit.setText(surname)
            self.patronymicEdit.setText(patronymic_name)
            self.dateEdit.setDate(QDate.fromString(birth_date, 'yyyy-MM-dd'))
            self.addressEdit.setText(home_address)
            self.phoneEdit.setText(phone_number)

    def delete_click(self):
        # Подтверждение удаления
        result = show_question(self, 'Вы уверены, что хотите удалить читателя?', 'Удалить?')
        if result == QMessageBox.Yes:
            # Подключение к БД
            con = sqlite3.connect('librarian.sqlite')
            cur = con.cursor()
            # Выполнение запроса удаления
            cur.execute("""DELETE FROM readers WHERE Id = ?""", (self.reader_id,)).fetchall()
            con.commit()
            con.close()
            # Закрываем диалог с результатом
            self.done(QMessageBox.Ok)

    def cancel_click(self):
        # Закрываем диалог с результатом
        self.done(QMessageBox.Cancel)

    def ok_click(self):
        result = False
        if self.reader_id == 0:
            result = self.create_reader()
        else:
            result = self.update_reader()
        # Закрываем диалог с результатом
        if result:
            self.done(QMessageBox.Ok)

    # Проверка заполненности полей формы
    def is_reader_ok(self):
        if self.nameEdit.text() == '':
            show_error(self, 'Имя читателя отсутствует')
            return False
        if self.surnameEdit.text() == '':
            show_error(self, 'Фамилия читателя отсутствует')
            return False
        if self.patronymicEdit.text() == '':
            show_error(self, 'Отчество читателя отсутствует')
            return False
        if self.addressEdit.text() == '':
            show_error(self, 'Адрес читателя не указан')
            return False
        if self.phoneEdit.text() == '':
            show_error(self, 'Телефон читателя не указан')
            return False
        return True

    def create_reader(self):
        if not self.is_reader_ok():
            return False
        # Заберём новые значения
        self.name = self.nameEdit.text()
        self.surname = self.surnameEdit.text()
        self.patronymic_name = self.patronymicEdit.text()
        self.birth_date = self.dateEdit.date().toString('yyyy-MM-dd')
        self.home_address = self.addressEdit.text()
        self.phone_number = self.phoneEdit.text()
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        # Добавляем книгу
        cur.execute("""INSERT INTO readers
            (Name, Surname, PatronymicName, BirthDate, HomeAddress, PhoneNumber)
            VALUES (?, ?, ?, ?, ?, ?)""", (self.name, self.surname, self.patronymic_name, self.birth_date, self.home_address, self.phone_number)).fetchall()
        con.commit()
        con.close()
        return True

    def update_reader(self):
        if not self.is_reader_ok():
            return False
        # Обновляем данные о читателе, если они изменились
        if self.name != self.nameEdit.text() \
                or self.surname != self.surnameEdit.text() \
                or self.patronymic_name != self.patronymicEdit.text() \
                or self.birth_date != self.dateEdit.date().toString('yyyy-MM-dd') \
                or self.phone_number != self.phoneEdit.text() \
                or self.home_address != self.addressEdit.text():
            # Заберём новые значения
            self.name = self.nameEdit.text()
            self.surname = self.surnameEdit.text()
            self.patronymic_name = self.patronymicEdit.text()
            self.birth_date = self.dateEdit.date().toString('yyyy-MM-dd')
            self.home_address = self.addressEdit.text()
            self.phone_number = self.phoneEdit.text()
            # Подключение к БД
            con = sqlite3.connect('librarian.sqlite')
            cur = con.cursor()
            # Выполнение запроса обновления
            cur.execute("""UPDATE readers
                SET Name = ?,
                    Surname = ?,
                    PatronymicName = ?,
                    BirthDate = ?,
                    HomeAddress = ?,
                    PhoneNumber = ?
                WHERE Id = ?""", (self.name, self.surname, self.patronymic_name, self.birth_date, self.home_address, self.phone_number, self.reader_id)).fetchall()
            con.commit()
            con.close()
        return True
