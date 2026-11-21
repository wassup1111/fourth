import sys
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QMainWindow
from PyQt6 import uic
import sqlite3

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.fill_db()

    def fill_db(self):
        with sqlite3.connect("coffee.sqlite") as con:
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
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())