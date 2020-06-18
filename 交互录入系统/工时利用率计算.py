import xlrd
import sys
import os
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from PyQt5.Qt import QWidget
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QFrame,QApplication,QDialog, QDialogButtonBox,
        QMessageBox,QVBoxLayout, QLineEdit,QTableWidgetItem,QTableWidget,QHBoxLayout,QComboBox,QGridLayout,
                             QLabel,QTextEdit)


class Chaxun(QDialog):
    def __init__(self,parent = None):
        super(Chaxun,self).__init__(parent)

        #设置界面大小、名称、背景
        self.setWindowTitle('工时利用率')
        self.setStyleSheet("background-image:url(tubiao_meitu.jpg)")
        #self.setWindowOpacity(0.9)  # 设置窗口透明度
        #窗体属性
        self.setWindowFlags(Qt.Widget)
        QApplication.setStyle("Fusion")
        font = QtGui.QFont('微软雅黑', 13)
        #self.setWindowFlags(Qt.FramelessWindowHint)#无边框

        #self.exceldata1=self.readexcel

        self.feathdata=[]
        data = xlrd.open_workbook(r'C:\Users\miaojia.li\Desktop\安晓路早会记录跟踪表(1).xlsx')
        table = data.sheet_by_name('晨会记录表')
        for rows in range(1,table.nrows):
            array={'data':'','actualtime':''}
            if table.cell(rows,0).ctype==3:
                guodu=xlrd.xldate_as_datetime(table.cell_value(rows,0),0)
                cell =guodu.strftime('%Y/%m/%d')
            array['data']=cell
            array['actualtime']=table.cell_value(rows,5)
            self.feathdata.append(array)



        lable1=QLabel("输入日期:格式****/*/*")
        self.cfd= QLineEdit(self)
        self.cfd.setFixedSize(200,30)


        self.btn1 = QPushButton("查询")
        self.btn1.setFixedSize(70, 40)
        self.btn1.clicked.connect(lambda :self.inquire(self.feathdata))

        lable2 = QLabel("计算结果")
        self.mdd= QLineEdit(self)
        self.mdd.setFixedSize(200,30)

        hbj = QHBoxLayout()
        hbj1 = QHBoxLayout()
        vbj=QVBoxLayout()

        hbj.addWidget(lable1)
        hbj.addWidget(self.cfd)
        hbj1.addWidget(lable2)
        hbj1.addWidget(self.mdd)
        vbj.addLayout(hbj)
        vbj.addWidget(self.btn1)
        vbj.addLayout(hbj1)

        self.setLayout(vbj)

    def readexcel(self):
        feathdata=[]
        data = xlrd.open_workbook(r'C:\Users\miaojia.li\Desktop\安晓路早会记录跟踪表(1).xlsx')
        table = data.sheet_by_name('晨会记录表')
        for rows in range(1,table.nrows):
            array={'data':'','actualtime':''}
            if table.cell(rows,0).ctype==3:
                guodu=xlrd.xldate_as_datetime(table.cell_value(rows,0),0)
                cell =guodu.strftime('%Y/%m/%d')
            array['data']=cell
            array['actualtime']=table.cell_value(rows,5)
            feathdata.append(array)
        return feathdata

    def inquire(self,exceldata):
        print(exceldata)
        print(type(exceldata))
        inputdata=self.cfd.text()
        output=0
        print("aaa")
        for i in range(len(exceldata)):
            if exceldata[i]['data']==inputdata:
                output+=exceldata[i]['actualtime']
        print(output)
        self.mdd.setText(str(output))



def main():
    #显示
    app = QApplication(sys.argv)
    c = Chaxun()
    bbb=c.readexcel()
    print(bbb)
    print(type(bbb))
    c.btn1.clicked.connect(lambda :c.inquire(bbb))

    c.show()
    sys.exit(app.exec_())

main()