import sqlite3

from PyQt5 import QtCore, uic  # Импортируем uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QTableWidget, QAbstractItemView

from MessageBox import show_warning

# from MessageBox import show_warning
# from bookForm import BookForm


class ReadersForm(QWidget):
    book_form = None

    def __init__(self):
        super().__init__()
        uic.loadUi('ReadersForm.ui', self)  # Загружаем дизайн
        # Отключаем кнопки минимизации и разворачивания
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)

        self.searchButton.clicked.connect(self.show_readers)
        self.addButton.clicked.connect(self.add_click)
        # self.readersButton.clicked.connect(self.readers_click)
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
        result = cur.execute("""SELECT Id, Name, BirthDate, HomeAddress, PhoneNumber
            FROM readers
            WHERE Name LIKE ?""", (search,)).fetchall()
        # Заполним размеры таблицы
        self.readersWidget.setColumnCount(5)
        self.readersWidget.setRowCount(0)
        # Заполним заголовки столбцов
        self.readersWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str('Номер')))
        self.readersWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str('ФИО')))
        self.readersWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str('Дата рождения')))
        self.readersWidget.setHorizontalHeaderItem(3, QTableWidgetItem(str('Адрес')))
        self.readersWidget.setHorizontalHeaderItem(4, QTableWidgetItem(str('Телефон')))
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

    def edit_reader(self):
        pass

    def add_click(self):
        pass
    