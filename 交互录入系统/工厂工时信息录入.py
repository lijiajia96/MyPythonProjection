#导入包
import pymysql
import sys
import xlwt
import uuid
import os
import datetime ,time
#import NLP2 as nlp
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from PyQt5.Qt import QWidget
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame,QApplication,QDialog, QDialogButtonBox,
        QMessageBox,QVBoxLayout, QLineEdit,QTableWidgetItem,QTableWidget,QHBoxLayout,QComboBox,QGridLayout,
                             QLabel,QTextEdit)

#pyinstaller -w -F 本项目.py -p D:\zhaopro\venv\Lib\site-pack.py


#建立界面类
class creat_view(QDialog):
    def __init__(self,parent = None):
        super(creat_view,self).__init__(parent)

        #设置界面大小、名称、背景
        self.resize(1200,900)
        self.setWindowTitle('故障诊断专家系统')
        self.setStyleSheet("background-image:url(tubiao_meitu.jpg)")

        #窗体属性
        self.setWindowFlags(Qt.Widget)

        #连接数据库

        db = pymysql.connect("localhost", "root", "12345678q", "jisuanxitong",charset='utf8')

        #获取游标、数据
        cur = db.cursor()
        cur.execute("SELECT 序号,开始日期,车牌号,工单号（事件）,施工项目,技师姓名,施工开始时间,施工结束时间,状态,备注 FROM employee")
        data = cur.fetchall()


        #数据列名
        col_lst = [tup[0] for tup in cur.description]

        #数据的大小t
        row = len(data)
        vol = len(data[0])


        #插入表格
        self.MyTable = QTableWidget(row,vol)
        font = QtGui.QFont('微软雅黑',10)

        #设置字体、表头
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(col_lst)
        #self.MyTable.resizeColumnsToContents()
        #设置竖直方向表头不可见
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.Panel)
        self.MyTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.MyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MyTable.resizeColumnsToContents()
        self.MyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
#设置表格颜色 self.MyTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')

        #构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)
        #输入框
        self.qle = QLineEdit()
        self.qle.setFixedSize(1200,50)
        buttonBox = QDialogButtonBox()
        #增删查改四个按钮
        self.addButton= buttonBox.addButton("&录入数据",QDialogButtonBox.ActionRole)
        inquireButton = buttonBox.addButton("&查询",QDialogButtonBox.ActionRole)
        daochuanniu= buttonBox.addButton("&导出数据", QDialogButtonBox.ActionRole)

        #设置按钮内字体样式
        self.addButton.setFont(font)
        daochuanniu.setFont(font)
        # okButton.setFont(font)
        # deleteButton.setFont(font)
        inquireButton.setFont(font)

        #垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.qle)
        layout.addWidget(buttonBox)
        layout.addWidget(self.MyTable)
        self.setLayout(layout)

        inquireButton.clicked.connect(partial(self.inq_data,db))#查询实现
        daochuanniu.clicked.connect(self.daochushuju)

    #打开录入界面
    def add_data(self,cur,db):
        neww=lvru_window
        neww.show()

    def daochushuju(self):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name ='Times New Roman'
        style.font = font

        uuid_str = uuid.uuid1().hex  # 构成完整文件存储路径
        tmp_file_name = 'D:/downloaddata/data_%s.xls' % uuid_str[:7]
        #print(tmp_file_name)

        work_book = xlwt.Workbook()
        sheet = work_book.add_sheet('sheet1')
        rows = self.MyTable.rowCount()
        for i in range(rows):
            mainList=[]    #tablewidget一共有10列
            for j in range(10):
                try:
                    data = self.MyTable.item(i, j).text()
                    mainList.append(data)
                except:
                    data=''
                    mainList.append(data)
                sheet.write(i, j, mainList[j],style)#保存
                print("写入",mainList[j])
        work_book.save(tmp_file_name)

    #查询
    def inq_data(self,db):
        cur = db.cursor()
        #txt=self.qle.text()
        txt = self.qle.text()

        # keywordlist=nlp.abkeyword(text1)
        # txt="".join(keywordlist)
        #模糊查询 
        if len(txt) != 0:
            try:
                cur.execute("SELECT 序号,开始日期,车牌号,工单号（事件）,施工项目,技师姓名,施工开始时间,施工结束时间,状态,备注 FROM EMPLOYEE WHERE 开始日期 LIKE '%"+txt+"%' or 车牌号 LIKE '%"+txt+"%' or 施工项目 LIKE '%"+txt+"%' or 技师姓名 LIKE '%"+txt+"%' or 备注 LIKE '%"+txt+"%'")
                data_x = cur.fetchall()
                self.MyTable.clearContents()

                row_4 = len(data_x)
                vol_1 = len(cur.description)

                # 查询到的更新带表格当中
                for i_x in range(row_4):
                    for j_y in range(vol_1):
                        temp_data_1 = data_x[i_x][j_y]  # 临时记录，不能直接插入表格
                        data_1 = QTableWidgetItem(str(temp_data_1))  # 转换后可插入表格
                        self.MyTable.setItem(i_x, j_y, data_1)
            except pymysql.connector.Error as e:
                print('query error!{}'.format(e))
        #空输入返回原先数据表格
        else:
            self.MyTable.clearContents()
            cur.execute("SELECT 序号,开始日期,车牌号,工单号（事件）,施工项目,技师姓名,施工开始时间,施工结束时间,状态,备注 FROM EMPLOYEE")
            data_y = cur.fetchall()
            row_5 = len(data_y)
            vol_1 = len(cur.description)
            for i_x_1 in range(row_5):
                for j_y_1 in range(vol_1):
                    temp_data_2 = data_y[i_x_1][j_y_1]  # 临时记录，不能直接插入表格
                    data_2 = QTableWidgetItem(str(temp_data_2))  # 转换后可插入表格
                    self.MyTable.setItem(i_x_1, j_y_1, data_2)

    def messageDialog(self,QCloseEvent):
        msg_box = QMessageBox.warning(self, '警告', '文件出现异常',QMessageBox.Yes  )
        if msg_box == QtWidgets.QMessageBox.Yes:
            QCloseEvent.accept()

class lvru_window(QDialog):
    def __init__(self, parent=None):
        super(lvru_window, self).__init__(parent)

        # 设置界面大小、名称
        #self.setFixedSize(900, 600)
        self.setWindowTitle('故障诊断专家系统录入')
        self.setWindowFlags(Qt.Widget)

        #施工日期
        title1 = QLabel("施工日期")
        title1.setAlignment(Qt.AlignCenter)
        self.workdate = QDateEdit(QDate.currentDate(), self)
        self.workdate.setDisplayFormat('yyyy/MM/dd')
        self.workdate.setCalendarPopup(True)

        #车牌号
        title2 = QLabel("车牌号")
        title2.setAlignment(Qt.AlignCenter)
        self.carnumber= QLineEdit(self)
        self.carnumber.setFixedSize(200,30)

        #工单号（事件）
        title3 = QLabel("工单号（事件）")
        title3.setAlignment(Qt.AlignCenter)
        self.worknum= QLineEdit(self)
        self.worknum.setFixedSize(200,30)

        #施工项目
        title4 = QLabel("施工项目")
        title4.setAlignment(Qt.AlignCenter)
        self.projectname= QLineEdit(self)
        self.projectname.setFixedSize(200,30)

        #技师姓名
        title5 = QLabel("技师姓名")
        title5.setAlignment(Qt.AlignCenter)
        self.teachername= QLineEdit(self)
        self.teachername.setFixedSize(200,30)

        #施工开始时间
        title6 = QLabel("施工开始时间")
        title6.setAlignment(Qt.AlignCenter)
        self.starttime = QTimeEdit(QTime.currentTime(), self)                                # 6
        self.starttime.setDisplayFormat('HH:mm:ss')

        #施工结束时间
        title7 = QLabel("施工结束时间")
        title7.setAlignment(Qt.AlignCenter)
        self.endtime = QTimeEdit(QTime.currentTime(), self)                                # 6
        self.endtime.setDisplayFormat('HH:mm:ss')

        #状态
        state11= ["竣工", "结算", "暂停"]
        title8=QLabel("状态")
        title8.setAlignment(Qt.AlignCenter)
        self.state = QComboBox(self)
        self.state.addItems(state11)

        #备注
        title9 = QLabel("备注")
        title9.setAlignment(Qt.AlignCenter)
        self.beizhu=QTextEdit()
        self.beizhu.setFixedHeight(100)

        self.btn1 = QPushButton("提交")
        font25 = QtGui.QFont('微软雅黑', 15)
        self.btn1.setFont(font25)
        self.btn1.setFixedSize(70, 40)
        self.btn1.clicked.connect(self.lurushujuku)

        self.btn2 = QPushButton("取消")
        self.btn2.setFont(font25)
        self.btn2.setFixedSize(70, 40)
        self.btn2.clicked.connect(lambda: self.close())

        #表格布局
        grid = QGridLayout()
        grid.setSpacing(5)  # 创建标签之间的空间
        grid.addWidget(title1, 1, 0)
        grid.addWidget(self.workdate, 1, 1)
        grid.addWidget(title2, 2, 0)
        grid.addWidget(self.carnumber, 2, 1)
        grid.addWidget(title3, 2, 2)
        grid.addWidget(self.worknum, 2, 3)
        grid.addWidget(title4, 3, 0)
        grid.addWidget(self.projectname, 3, 1)
        grid.addWidget(title5, 3, 2)
        grid.addWidget(self.teachername, 3, 3)
        grid.addWidget(title6, 4, 0)
        grid.addWidget(self.starttime, 4, 1)
        grid.addWidget(title7, 4, 2)
        grid.addWidget(self.endtime, 4, 3)
        grid.addWidget(title8, 5, 0)
        grid.addWidget(self.state, 5, 1)
        grid.addWidget(title9, 6, 0)
        grid.addWidget(self.beizhu,6, 1,1,3)

        grid.setVerticalSpacing(30)
        grid.setHorizontalSpacing(10)

        vbj = QVBoxLayout()
        hbj = QHBoxLayout()
        hbj.addWidget(self.btn1)
        hbj.addWidget(self.btn2)

        vbj.addLayout(grid)
        vbj.addLayout(hbj)

        self.setLayout(vbj)



    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self, '消息', '是否关闭录入窗口？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            QCloseEvent.accept()
            self.carnumber.clear()
            self.worknum.clear()
            self.projectname.clear()
            self.teachername.clear()
            self.state.clear()
            self.beizhu.clear()
        else:
            QCloseEvent.ignore()
    def lurutanchu(self):
        if not self.isVisible():
            self.show()

    def lurushujuku(self):
        res = QMessageBox.question(self, '提示', '确认录入？', QMessageBox.Yes | QMessageBox.No,QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            a = str(self.workdate.text())
            b = self.carnumber.text()
            c = self.worknum.text()
            d = self.projectname.text()
            e = self.teachername.text()
            f = self.starttime.text()
            g = self.endtime.text()
            h = self.state.currentText()
            i = self.beizhu.toPlainText()

            print(a, b, c, d, e, f, g, h, i)
            conn = pymysql.connect("localhost", "root", "12345678q", "jisuanxitong", charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            sql = """INSERT INTO EMPLOYEE(开始日期,车牌号,工单号（事件）,施工项目,技师姓名,施工开始时间,施工结束时间,状态,备注)
                             VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s')""" % (a, b, c, d, e, f, g, h, i)

            try:
                cursor.execute(sql)
                conn.commit()
                self.carnumber.clear()
                self.worknum.clear()
                self.projectname.clear()
                self.teachername.clear()
                self.beizhu.clear()

            except Exception as e:
                print('新增条目失败')
                print(e)
                conn.rollback()

        else:
            pass

def main():
    #显示
    app = QApplication(sys.argv)
    try:
        c = creat_view()
    except:
        print("sa sd ")
        msg_box=QMessageBox().information(None, "提示", "无法连接数据库！", QMessageBox.Yes)
        if msg_box == QtWidgets.QMessageBox.Yes:
            exit()
    d = lvru_window()
    c.addButton.clicked.connect(d.lurutanchu)
    c.show()

    sys.exit(app.exec_())

main()