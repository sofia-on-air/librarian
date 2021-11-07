import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QAbstractItemView

from MessageBox import show_warning
from readerForm import ReaderForm


class ReadersForm(QWidget):
    reader_form = None

    def __init__(self):
        super().__init__()
        uic.loadUi('ReadersForm.ui', self)  # Загружаем дизайн
        # Отключаем кнопки минимизации и разворачивания
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)

        self.searchButton.clicked.connect(self.show_readers)
        self.addButton.clicked.connect(self.add_click)
        # По двойному щелчку будет редактирование
        self.readersWidget.cellDoubleClicked.connect(self.edit_reader)
        # Редактирование самой таблицы запретим
        self.readersWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Показываем список
        self.show_readers()

    def show_readers(self):
        # Параметры поиска
        search = '%' + self.searchEdit.text() + '%'
        # Подключение к БД
        con = sqlite3.connect('librarian.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT Id, Surname, Name, PatronymicName, BirthDate, HomeAddress, PhoneNumber
            FROM readers
            WHERE Name LIKE ?""", (search,)).fetchall()
        # Заполним размеры таблицы
        self.readersWidget.setColumnCount(7)
        self.readersWidget.setRowCount(0)
        # Заполним заголовки столбцов
        self.readersWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str('Номер')))
        self.readersWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str('Фамилия')))
        self.readersWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str('Имя')))
        self.readersWidget.setHorizontalHeaderItem(3, QTableWidgetItem(str('Отчество')))
        self.readersWidget.setHorizontalHeaderItem(4, QTableWidgetItem(str('Дата рождения')))
        self.readersWidget.setHorizontalHeaderItem(5, QTableWidgetItem(str('Адрес')))
        self.readersWidget.setHorizontalHeaderItem(6, QTableWidgetItem(str('Телефон')))
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.readersWidget.setRowCount(
                self.readersWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.readersWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        con.close()
        # Если не нашли ни одного читателя, показываем ошибку
        if len(result) == 0:
            show_warning(self, 'Читаталей по вашему критерию не найдено.\nПопробуйте исправить критерии поиска.')

    def add_click(self):
        self.reader_form = ReaderForm(0)
        result = self.reader_form.exec()
        # Если что-то сделали, нужно перезагрузить список читателей
        if result == QMessageBox.Ok:
            self.show_readers()

    def edit_reader(self, row, column):
        # Достанем данные читателя из таблицы
        reader_id = int(self.readersWidget.item(row, 0).text())
        surname = self.readersWidget.item(row, 1).text()
        name = self.readersWidget.item(row, 2).text()
        patronymic_name = self.readersWidget.item(row, 3).text()
        birth_date = self.readersWidget.item(row, 4).text()
        home_address = self.readersWidget.item(row, 5).text()
        phone_number = self.readersWidget.item(row, 6).text()
        self.reader_form = ReaderForm(reader_id, name, surname, patronymic_name, birth_date, home_address, phone_number)
        result = self.reader_form.exec()
        # Если что-то сделали, нужно перезагрузить список читателей
        if result == QMessageBox.Ok:
            self.show_readers()
