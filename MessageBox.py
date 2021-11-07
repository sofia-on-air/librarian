from PyQt5.QtWidgets import QMessageBox


def show_error(parent, text):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle("Ошибка")
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setIcon(QMessageBox.Critical)
    dlg.exec()


def show_warning(parent, text):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle("Упс..")
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setIcon(QMessageBox.Warning)
    dlg.exec()


def show_question(parent, text, title):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dlg.setIcon(QMessageBox.Question)
    result = dlg.exec()
    return result


def show_info(parent, text, title):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setIcon(QMessageBox.Information)
    dlg.exec()
