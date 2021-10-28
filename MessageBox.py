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
