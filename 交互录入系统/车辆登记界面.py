import pymysql
import sys
import xlwt
import uuid
import os
import shutil
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
        self.setWindowTitle('车辆信息查询')
        self.setStyleSheet("background-image:url(tubiao_meitu.jpg)")
        self.setWindowFlags(Qt.Widget)

        #连接数据库

        db = pymysql.connect("localhost", "root", "12345678q", "carmanage",charset='utf8')
        cur = db.cursor()
        cur.execute("SELECT id,车架号,车辆颜色,车辆型号,车机版本,拖运时间,拖运出发地,拖运目的地,拖车时状态,是否有拖车邮件,备注 FROM carinfo")
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
        self.MyTable.doubleClicked.connect(self.sync_table_double_clicked)
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

    def sync_table_double_clicked(self, index):
        table_column = index.column()
        table_row = index.row()
        a1 = self.MyTable.item(table_row, 1).text()
        c1=self.MyTable.item(table_row, 3).text()
        e1=self.MyTable.item(table_row, 5).text()
        f1=self.MyTable.item(table_row, 6).text()
        g1=self.MyTable.item(table_row, 7).text()
        print(a1,c1,e1,f1,g1)
        wenjianjia = a1 + c1 + e1 + f1 + "_" + g1
        wenjianjia = wenjianjia.replace("/", "-")
        pathnew=os.path.join("D:/carinformation/",wenjianjia)
        print(pathnew)
        if os.path.exists(pathnew):
            os.startfile(pathnew)
        else:
            print(1)


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
        txt = self.qle.text()
        if len(txt) != 0:
            try:
                sql="SELECT id,车架号,车辆颜色,车辆型号,车机版本,拖运时间,拖运出发地,拖运目的地,拖车时状态,是否有拖车邮件,备注 FROM CARINFO WHERE CONCAT(IFNULL(车架号,''),IFNULL(车辆型号,''),IFNULL(车机版本,''),IFNULL(拖运时间,''),IFNULL(备注,''),IFNULL(拖运出发地,''),IFNULL(拖运目的地,'')) LIKE '%"+txt+"%'"
                cur.execute(sql)
                #cur.execute("SELECT 车架号,车辆颜色,车辆型号,车机版本,拖运时间,拖运出发地,拖运目的地,拖车时状态,是否有拖车邮件,备注 FROM CARINFO WHERE 车架号 LIKE '%"+txt+"%' or 车辆型号 LIKE '%"+txt+"%' or 车机版本 LIKE '%"+txt+"%' or 拖运时间 LIKE '%"+txt+"%' or 备注 LIKE '%"+txt+"%'or 出发地 LIKE '%"+txt+"%' or 目的地 LIKE '%"+txt+"%'")
                print(sql)

                data_x = cur.fetchall()
                self.MyTable.clearContents()
                row_4 = len(data_x)
                vol_1 = len(cur.description)
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
            cur.execute("SELECT id,车架号,车辆颜色,车辆型号,车机版本,拖运时间,拖运出发地,拖运目的地,拖车时状态,是否有拖车邮件,备注 FROM CARINFO")
            data_y = cur.fetchall()
            row_5 = len(data_y)
            vol_1 = len(cur.description)
            for i_x_1 in range(row_5):
                for j_y_1 in range(vol_1):
                    temp_data_2 = data_y[i_x_1][j_y_1]  # 临时记录，不能直接插入表格
                    data_2 = QTableWidgetItem(str(temp_data_2))  # 转换后可插入表格
                    self.MyTable.setItem(i_x_1, j_y_1, data_2)
            print("已刷新")
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

        self.setWindowTitle('车辆拖运信息录入')
        self.setWindowFlags(Qt.Widget)

        # kekeke=["MT", "ST", "DT","BAT", "BST", "BDT","PMT", "PST", "PDT"]
        # self.course= QComboBox(self)
        # self.course.addItems(kekeke)
        # self.course.currentIndexChanged.connect(self.kemugengxin)
        # self.course.setFixedSize(200,30)

        self.cjh= QLineEdit(self)
        self.cjh.setFixedSize(200,30)

        self.clys= QLineEdit(self)
        self.clys.setFixedSize(200,30)

        self.clxh= QLineEdit(self)
        self.clxh.setFixedSize(200,30)

        self.cjbb= QLineEdit(self)
        self.cjbb.setFixedSize(200,30)

        self.tyrq = QDateEdit(QDate.currentDate(), self)
        self.tyrq.setDisplayFormat('yyyy/MM/dd')
        self.tyrq.setCalendarPopup(True)
        self.tyrq.setFixedSize(200, 30)

        self.cfd= QLineEdit(self)
        self.cfd.setFixedSize(200,30)

        self.mdd= QLineEdit(self)
        self.mdd.setFixedSize(200,30)

        self.zt= QLineEdit(self)
        self.zt.setFixedSize(200,30)

        xuanxiang= ["有", "无"]
        self.email = QComboBox(self)
        self.email.addItems(xuanxiang)
        self.email.setFixedSize(200, 30)

        self.bz = QLineEdit(self)
        self.bz.setFixedSize(200, 30)

        self.label16 = QLabel(self)
        self.label16.setText("故障图片")
        self.label16.setFixedSize(250, 150)
        self.label16.setHidden(True)
        pic1 = QPushButton(self)
        pic1.setText("上传照片1")
        pic1.setFixedSize(100,30)
        pic1.clicked.connect(self.openimage1)

        self.label17 = QLabel(self)
        self.label17.setText("故障图片")
        self.label17.setFixedSize(250, 150)
        self.label17.setHidden(True)
        pic2 = QPushButton(self)
        pic2.setText("上传照片2")
        pic2.setFixedSize(100, 30)
        pic2.clicked.connect(self.openimage2)

        self.label18 = QLabel(self)
        self.label18.setText("故障图片")
        self.label18.setFixedSize(250, 150)
        self.label18.setHidden(True)
        pic3 = QPushButton(self)
        pic3.setText("上传照片3")
        pic3.setFixedSize(100, 30)
        pic3.clicked.connect(self.openimage3)

        self.label19 = QLabel(self)
        self.label19.setText("   ")
        self.label19.setHidden(True)
        fujian= QPushButton(self)
        fujian.setText("上传附件")
        fujian.setFixedSize(100, 30)
        fujian.clicked.connect(self.uploadfj)

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
        # horizonal1 = QHBoxLayout()
        # horizonal1.addWidget(self.tyrq)
        # horizonal1.addWidget(title5)
        # horizonal1.addWidget(self.enddate)

        qfl= QFormLayout()
        qfl.setContentsMargins(20,20,20,20)
        qfl.setSpacing(20)
        qfl.addRow("车架号",self.cjh)
        qfl.addRow("车辆颜色", self.clys)
        qfl.addRow("车辆型号", self.clxh)
        qfl.addRow("车机版本",self.cjbb)
        qfl.addRow("拖运日期", self.tyrq)
        qfl.addRow("出发地",self.cfd)
        qfl.addRow("目的地", self.mdd)
        qfl.addRow("拖车时状态", self.zt)
        qfl.addRow("拖车邮件", self.email)
        qfl.addRow("备注",self.bz)

        qf2=QFormLayout()
        qf2.setContentsMargins(20,20,20,20)
        qf2.setSpacing(20)

        qf2.addRow("", pic1)
        qf2.addRow("", self.label16)
        qf2.addRow("", pic2)
        qf2.addRow("", self.label17)
        qf2.addRow("", pic3)
        qf2.addRow("", self.label18)
        qf2.addRow("", fujian)
        qf2.addRow("", self.label19)

        hbj = QHBoxLayout()
        hbj.addWidget(self.btn1)
        hbj.addWidget(self.btn2)

        hbj1 = QHBoxLayout()
        hbj1.addLayout(qfl)
        hbj1.addLayout(qf2)

        self.vbj.addLayout(hbj1)
        self.vbj.addLayout(hbj)
        self.setLayout(self.vbj)

        self.imgName1=[]
        self.imgName2=[]
        self.imgName3=[]
        self.fujianName=[]

    def openimage1(self):
        self.imgName1, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png")
        jpg = QtGui.QPixmap(self.imgName1).scaled(self.label16.width(), self.label16.height())
        self.label16.setPixmap(jpg)
        if(len(self.imgName1)!=0):
            self.label16.setHidden(False)

    def openimage2(self):
        self.imgName2, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.imgName2).scaled(self.label16.width(), self.label16.height())
        self.label17.setPixmap(jpg)
        if(len(self.imgName2)!=0):
            self.label17.setHidden(False)

    def openimage3(self):
        self.imgName3, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.imgName3).scaled(self.label16.width(), self.label16.height())
        self.label18.setPixmap(jpg)
        if(len(self.imgName3)!=0):
            self.label18.setHidden(False)

    def uploadfj(self):
        self.fujianName, imgType = QFileDialog.getOpenFileNames(self, "选择附件", "", "All Files(*)")

        self.label19.setText("选择了“{}”等{}个附件".format(str(self.fujianName[0]),len(self.fujianName)))

        if(len(self.fujianName)!=0):
            self.label19.setHidden(False)

    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self, '消息', '是否关闭录入窗口？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            QCloseEvent.accept()
            self.cjh.clear()
            self.clys.clear()
            self.clxh.clear()
            self.cjbb.clear()
            self.cfd.clear()
            self.mdd.clear()
            self.zt.clear()
            self.bz.clear()
            self.label16.clear()
            self.label17.clear()
            self.label18.clear()
            self.label19.clear()
        else:
            QCloseEvent.ignore()

    def lurutanchu(self):
        if not self.isVisible():
            self.show()

    def lurushujuku(self):
        newname1=[]
        newname2=[]
        newname3=[]
        res = QMessageBox.question(self, '提示', '确认录入？', QMessageBox.Yes | QMessageBox.No,QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            a = self.cjh.text()
            b = self.clys.text()
            c = self.clxh.text()
            d = self.cjbb.text()
            e = self.tyrq.text()
            f = self.cfd.text()
            g = self.mdd.text()
            h = self.zt.text()
            i = self.email.currentText()
            j=self.bz.text()

            wenjianjia=a+c+e+f+"_"+g
            wenjianjia=wenjianjia.replace("/","-")
            pathnew="D:/carinformation/"+wenjianjia    #为每一次提交建立文件夹

            isExists = os.path.exists(pathnew)
            if not isExists:
                os.makedirs(pathnew)
            if len(self.imgName1)!=0:
                fpath1, fname1 = os.path.split(self.imgName1)
                newname1 = pathnew+"/"+fname1
                #os.system('copy %s %s' % (self.imgName1, newname))
                shutil.copy(self.imgName1, newname1)
                if os.path.isfile(newname1):
                    print('copy file success')
                else:
                    print(0)
            if len(self.imgName2) != 0:
                fpath2, fname2 = os.path.split(self.imgName2)
                newname2 = pathnew+"/"+fname2
                #os.system('copy %s %s' % (self.imgName1, newname))
                shutil.copy(self.imgName2, newname2)
                if os.path.isfile(newname2):
                    print('copy file success')
                else:
                    print(0)
            if len(self.imgName3) != 0:
                fpath3, fname3 = os.path.split(self.imgName3)
                newname3 = pathnew+"/"+fname3
                #os.system('copy %s %s' % (self.imgName1, newname))
                shutil.copy(self.imgName3, newname3)
                if os.path.isfile(newname3):
                    print('copy file success')
                else:
                    print(0)
            if len(self.fujianName) != 0:
                for filef in self.fujianName:
                    fpath4, fname4 = os.path.split(filef)
                    newname4 = pathnew + "/" + fname4
                    # os.system('copy %s %s' % (self.imgName1, newname))
                    shutil.copy(filef, newname4)

            print(a, b, c, d, e, f, g, h, i,j)
            conn = pymysql.connect("localhost", "root", "12345678q", "carmanage", charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            sql = """INSERT INTO CARINFO(车架号,车辆颜色,车辆型号,车机版本,拖运时间,拖运出发地,拖运目的地,拖车时状态,是否有拖车邮件,备注,照片1,照片2,照片3,附件)
                             VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s','%s','%s','%s','%s','%s')""" % (a, b, c, d, e, f, g, h, i,j,newname1, newname2, newname3, pathnew)
            #newname1, newname2, newname3, pathnew
            # sql1="""INSERT INTO CARINFO(照片1,照片2,照片3,附件)
            #                  VALUES ('%s','%s','%s','%s')""" % (newname1, newname2, newname3, pathnew)
            try:
                cursor.execute(sql)
                conn.commit()
                self.cjh.clear()
                self.clys.clear()
                self.clxh.clear()
                self.cjbb.clear()
                self.cfd.clear()
                self.mdd.clear()
                self.zt.clear()
                self.bz.clear()
                self.label16.clear()
                self.label16.setHidden(True)
                self.label17.clear()
                self.label17.setHidden(True)
                self.label18.clear()
                self.label17.setHidden(True)
                self.label19.clear()

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
        msg_box=QMessageBox().information(None, "提示", "无法连接数据库！", QMessageBox.Yes)
        if msg_box == QtWidgets.QMessageBox.Yes:
            exit()
    d = lvru_window()
    c.addButton.clicked.connect(d.lurutanchu)
    c.show()

    sys.exit(app.exec_())

main()