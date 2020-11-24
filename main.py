import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui.ui', self)
        self.resize(1000, 600)
        self.tableWidget.setRowCount(0)
        self.tableWidget.resize(980, 490)
        self.tableWidget.move(10, 100)

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""select * from coffee""").fetchall()
        numRows = 0
        self.columns1 = ['ID', 'Name', 'Sort', 'Stage', 'Beans', 'Taste', 'Price', 'Volume']
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(self.columns1)
        for el in result:
            self.tableWidget.insertRow(numRows)
            self.tableWidget.setItem(numRows, 0, QTableWidgetItem(str(el[0])))
            self.tableWidget.setItem(numRows, 1, QTableWidgetItem(str(el[1])))
            self.tableWidget.setItem(numRows, 2, QTableWidgetItem(str(el[2])))
            self.tableWidget.setItem(numRows, 3, QTableWidgetItem(str(el[3])))
            self.tableWidget.setItem(numRows, 4, QTableWidgetItem(str(el[4])))
            self.tableWidget.setItem(numRows, 5, QTableWidgetItem(str(el[5])))
            self.tableWidget.setItem(numRows, 6, QTableWidgetItem(str(el[6])))
            self.tableWidget.setItem(numRows, 7, QTableWidgetItem(str(el[7])))

            numRows += 1

        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
