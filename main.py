import sys
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QApplication, QMainWindow
from PyQt6 import uic
import sqlite3
from UI.main1 import Ui_MainWindow1
from UI.main2 import Ui_MainWindow2
import os
import sys

def get_db_path(filename="coffee.sqlite"):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

db_path = get_db_path("coffee.sqlite")

class MyWidget(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fill_db()
        self.btns()

    def update1(self):
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            query = """SELECT * from coffee"""
            res = cursor.execute(query).fetchall()
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
            self.tableWidget.setRowCount(len(res))
            for r, row in enumerate(res):
                for c, val in enumerate(list(row)):
                    item = QTableWidgetItem(str(val))
                    self.tableWidget.setItem(r, c, item)

    def fill_db(self):
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            query = """SELECT * from coffee"""
            res = cursor.execute(query).fetchall()
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
            self.tableWidget.setRowCount(len(res))
            for r, row in enumerate(res):
                for c, val in enumerate(list(row)):
                    item = QTableWidgetItem(str(val))
                    self.tableWidget.setItem(r, c, item)

    def btns(self):
        self.add_btn.clicked.connect(self.adding)
        self.edit_btn.clicked.connect(self.editing)

    def adding(self):
        self.form = AddEditFormCoffee(self)
        self.form.show()

    def editing(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Выберите 1 строку")
            return
        id1 = self.tableWidget.item(row, 0).text()
        self.form = AddEditFormCoffee(self, id1=id1)
        self.form.show()
        
class AddEditFormCoffee(QMainWindow, Ui_MainWindow2):
    def __init__(self, parent=None, id1=None):
        super().__init__()
        self.setupUi(self)
        self.id1 = id1
        self.parent1 = parent
        self.setupUi(self)

        if id1 is not None:
            self.load_coffee()
            self.ok_btn.clicked.connect(self.edit_row)
        else:
            self.ok_btn.clicked.connect(self.add_row)

    def edit_row(self):
        data = self.validate()
        if data is None:
            self.statusBar().showMessage("Неправильное заполнение значений")
            return
        else:
            with sqlite3.connect(db_path) as con:
                cursor = con.cursor()
                query = """UPDATE coffee
                SET name = ?, scale_of_cooked = ?, type = ?, taste = ?, price = ?, volume = ?
                WHERE id = ?"""
                cursor.execute(query, (*data, self.id1))
            self.close()
            self.parent1.update1()

    def load_coffee(self):
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            query = """SELECT * FROM coffee WHERE id = ?"""
            res = cursor.execute(query, (self.id1,)).fetchall()
        id1, name1, scale1, type1, taste1, price1, volume1 = res[0]
        self.name1.setPlainText(name1)
        self.price1.setPlainText(str(price1))
        self.scale1.setPlainText(scale1)
        self.taste1.setPlainText(taste1)
        self.volume1.setPlainText(str(volume1))
        idx = self.type1.findText(type1)
        self.type1.setCurrentIndex(idx)

    def validate(self):
        name1 = self.name1.toPlainText()
        price1 = self.price1.toPlainText()
        scale1 = self.scale1.toPlainText()
        taste1 = self.taste1.toPlainText()
        volume1 = self.volume1.toPlainText()
        type1 = self.type1.currentText()
        if (name1.strip() and 
            price1.strip().isdigit() and 
            scale1.strip() and 
            taste1.strip() and
            volume1.strip().isdigit() and
            type1.strip()):
            return name1, scale1, type1 , taste1, price1, volume1
        else:
            return None


    def add_row(self):
        data = self.validate()
        if data is None:
            self.statusBar().showMessage("Неправильное заполнение значений")
            return
        else:
            with sqlite3.connect(db_path) as con:
                cursor = con.cursor()
                query = """INSERT INTO coffee (name, scale_of_cooked, type, taste, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)"""
                cursor.execute(query, (*data,))
            self.close()
            self.parent1.update1()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())