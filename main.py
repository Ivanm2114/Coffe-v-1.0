import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui.ui', self)
        self.resize(1000, 600)
        self.tableWidget.setRowCount(0)
        self.tableWidget.resize(980, 490)
        self.tableWidget.move(10, 50)
        self.pushButton.clicked.connect(self.add_coffe)
        self.pushButton_2.clicked.connect(self.change_coffe)
        self.showResults()

    def showResults(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""select * from coffee order by id""").fetchall()
        numRows = 0
        columns1 = ['ID', 'Name', 'Sort', 'Stage', 'Beans', 'Taste', 'Price', 'Volume']
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(columns1)
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

    def add_coffe(self):
        self.add_window = addWindow(1, self.tableWidget)
        self.add_window.show()

    def change_coffe(self):
        self.add_window = addWindow(2, self.tableWidget)
        self.add_window.show()


class addWindow(QMainWindow):
    def __init__(self, code, table):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.table = table
        self.label8 = QLabel(self)
        self.label8.move(100, 220)
        if code == 2:
            id = self.table.item(self.table.currentRow(), 0).text()
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            result = cur.execute(f"""select * from coffee where id = {id}""").fetchall()
            self.coffee = result[0]
            print(result)
            self.lineEdit.setText(self.coffee[1])
            self.lineEdit_2.setText(self.coffee[2])
            self.lineEdit_3.setText(self.coffee[3])
            self.lineEdit_4.setText(self.coffee[4])
            self.lineEdit_5.setText(self.coffee[5])
            self.lineEdit_6.setText(str(self.coffee[6]))
            self.lineEdit_7.setText(str(self.coffee[7]))
            self.pushButton.setText('Изменить')
        self.pushButton.clicked.connect(self.confirm)

    def confirm(self):
        if self.pushButton.text() == 'Добавить':
            self.addToDB()
        elif self.pushButton.text() == 'Изменить':
            self.editDB()

    def addToDB(self):
        name = self.lineEdit.text()
        sort = self.lineEdit_2.text()
        stage = self.lineEdit_3.text()
        beans = self.lineEdit_4.text()
        taste = self.lineEdit_5.text()
        price = self.lineEdit_6.text()
        vol = self.lineEdit_7.text()
        if name and sort and stage and beans and taste and price and vol:
            self.label8.setText('')
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            result = cur.execute(f"""select * from coffee""").fetchall()
            id = result[-1][0]
            cur.execute(f"""insert into coffee('id', 'name', 'sort', 'stage', 'beans', 'taste', 'price', 'volume')
values ({id+1}, '{name}', '{sort}', '{stage}', '{beans}', '{taste}', {price}, {vol})""")
            con.commit()
            con.close()
            self.close()
            ex.showResults()

        else:
            self.label8.setText('Неверный ввод')

    def editDB(self):
        name = self.lineEdit.text()
        sort = self.lineEdit_2.text()
        stage = self.lineEdit_3.text()
        beans = self.lineEdit_4.text()
        taste = self.lineEdit_5.text()
        price = self.lineEdit_6.text()
        vol = self.lineEdit_7.text()
        if name and sort and stage and beans and taste and price and vol:
            self.label8.setText('')
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            cur.execute(f'''delete from coffee where id = {self.coffee[0]}''')
            cur.execute(f"""insert into coffee('id', 'name', 'sort', 'stage', 'beans', 'taste', 'price', 'volume')
        values ({self.coffee[0]}, '{name}', '{sort}', '{stage}', '{beans}', '{taste}', {price}, {vol})""")
            con.commit()
            con.close()
            self.close()
            ex.showResults()
        else:
            self.label8.setText('Неверный ввод')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
