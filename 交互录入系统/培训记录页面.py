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

#编译成exe
#pyinstaller -w -F 本项目.py -p D:\zhaopro\venv\Lib\site-pack.py


#建立界面类
class creat_view(QDialog):
    def __init__(self,parent = None):
        super(creat_view,self).__init__(parent)

        #设置界面大小、名称、背景
        self.resize(1200,900)
        self.setWindowTitle('故障诊断专家系统')
        self.setStyleSheet("background-image:url(tubiao_meitu.jpg)")
        self.setWindowFlags(Qt.Widget)

        #连接数据库

        db = pymysql.connect("localhost", "root", "12345678q", "jisuanxitong",charset='utf8')
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
        msg_box = QMessageBox.warning(self, '警告', '文件出现异常',QMessageBox.Yes)
        if msg_box == QtWidgets.QMessageBox.Yes:
            QCloseEvent.accept()

class lvru_window(QDialog):
    def __init__(self, parent=None):
        super(lvru_window, self).__init__(parent)

        self.bigdict={"MT":['健康与安全','健康与安全1','健康与安全'],
                      "ST":['健康1安全','健康1安全1','健康1安全',"asd"]}
        # 设置界面大小、名称

        self.setWindowTitle('培训记录录入')
        self.setWindowFlags(Qt.Widget)

        fm=QFrame()
        fm.setFrameShape(QFrame.StyledPanel)

        kekeke=["MT", "ST", "DT","BAT", "BST", "BDT","PMT", "PST", "PDT"]
        self.course= QComboBox(self)
        self.course.addItems(kekeke)
        self.course.currentIndexChanged.connect(self.kemugengxin)
        self.course.setFixedSize(200,30)

        self.address= QLineEdit(self)
        self.address.setFixedSize(200,30)

        self.teachername= QLineEdit(self)
        self.teachername.setFixedSize(200,30)

        self.startdate = QDateEdit(QDate.currentDate(), self)
        self.startdate.setDisplayFormat('yyyy/MM/dd')
        self.startdate.setCalendarPopup(True)
        self.startdate.setFixedSize(120,30)
        title5 = QLabel("至")
        title5.setFixedSize(15,30)
        title5.setAlignment(Qt.AlignCenter)
        self.enddate = QDateEdit(QDate.currentDate(), self)
        self.enddate.setDisplayFormat('yyyy/MM/dd')
        self.enddate.setCalendarPopup(True)
        self.enddate.setFixedSize(120,30)

        fuwuzhongxinmingchen = ["竣工", "结算", "暂停"]
        self.fuwuzx = QComboBox(self)
        self.fuwuzx.addItems(fuwuzhongxinmingchen)
        self.fuwuzx.setFixedSize(200,30)

        self.studentname= QLineEdit(self)
        self.studentname.setFixedSize(200,30)


        sex= ["男", "女"]
        self.sexy = QComboBox(self)
        self.sexy.addItems(sex)
        self.sexy.setFixedSize(200,30)

        zhiwu = ["男", "女"]
        self.zhiwu = QComboBox(self)
        self.zhiwu.addItems(zhiwu)
        self.zhiwu.setFixedSize(200,30)

        ornot = ["是", "否"]
        self.diangongzhen = QComboBox(self)
        self.diangongzhen.addItems(ornot)
        self.diangongzhen.setFixedSize(200,30)


        self.sfid= QLineEdit(self)
        self.sfid.setFixedSize(200,30)

        self.youxiang= QLineEdit(self)
        self.youxiang.setFixedSize(200,30)

        self.phone= QLineEdit(self)
        self.phone.setFixedSize(200,30)
        self.phone.setFrame(True)

        title24 = QLabel("科目和成绩")
        title24.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont('微软雅黑', 20)
        title24.setFont(font)

        self.MyTable1 = QTableWidget(1, 4)
        font1 = QtGui.QFont('微软雅黑', 15)
        self.MyTable1.setRowCount(1)
        self.MyTable1.horizontalHeader().setFont(font1)
        #self.MyTable.setHorizontalHeaderLabels(["序号", "根本原因", "概率"])
        self.MyTable1.verticalHeader().setVisible(False)
        self.MyTable1.setFrameShape(QFrame.Box)
        #self.MyTable1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.MyTable1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MyTable1.resizeColumnsToContents()
        self.MyTable1.setFixedSize(600, 100)
        #for i in range(self.MyTable1.columnCount()):
        #self.MyTable1.item(0,1).setTextAlignment(Qt.AlignCenter)


        self.MyTable1.setRowHeight(0,60)

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

        self.vbj = QVBoxLayout()
        self.vbj.setContentsMargins(10,10,10,10)
        horizonal1 = QHBoxLayout()
        horizonal1.addWidget(self.startdate)
        horizonal1.addWidget(title5)
        horizonal1.addWidget(self.enddate)

        qfl= QFormLayout()
        qfl.setContentsMargins(20,20,20,20)
        qfl.setSpacing(20)
        qfl.addRow("培训课程",self.course)
        qfl.addRow("培训地点", self.address)
        qfl.addRow("讲师", self.teachername)
        qfl.addRow("培训日期",horizonal1)
        qfl.addRow("服务中心名称", self.fuwuzx)
        qfl.addRow("学员姓名",self.studentname)
        qfl.addRow("性别", self.sexy)
        qfl.addRow("职务", self.zhiwu)
        qfl.addRow("是否有电工证", self.diangongzhen)
        qfl.addRow("身份证号码", self.sfid)
        qfl.addRow("联系人邮箱", self.youxiang)
        qfl.addRow("电话", self.phone)

        hbj = QHBoxLayout()
        hbj.addWidget(self.btn1)
        hbj.addWidget(self.btn2)

        hbj2=QHBoxLayout()
        hbj2.addWidget(self.MyTable1)


        self.vbj.addLayout(qfl)
        self.vbj.addWidget(title24)
        self.vbj.addLayout(hbj2)
        #self.vbj.addWidget(self.MyTable1)
        self.vbj.addLayout(hbj)

        self.setLayout(self.vbj)

    def kemugengxin(self):
        tag=self.course.currentText()
        self.MyTable1.setColumnCount(len(self.bigdict[tag]))
        self.MyTable1.setHorizontalHeaderLabels(self.bigdict[tag])

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