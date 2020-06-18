#导入包
import pymysql
import sys
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

#建立界面类
class creat_view(QDialog):
    def __init__(self,parent = None):
        super(creat_view,self).__init__(parent)

        #设置界面大小、名称、背景
        self.resize(1000,900)
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

        #数据的大小
        row = len(data)
        vol = len(data[0])


        #插入表格
        self.MyTable = QTableWidget(row,vol)
        font = QtGui.QFont('微软雅黑',10)

        #设置字体、表头
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(col_lst)
        #设置竖直方向表头不可见
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)
        self.MyTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.MyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
#设置表格颜色             self.MyTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')

        #构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)


        #编辑按钮
        self.qle = QLineEdit()
        self.qle.setFixedSize(1000,50)
        buttonBox = QDialogButtonBox()
        #增删查改四个按钮
        self.addButton= buttonBox.addButton("&录入新数据",QDialogButtonBox.ActionRole)
        # okButton = buttonBox.addButton("&OK",QDialogButtonBox.ActionRole)
        # deleteButton = buttonBox.addButton("&DELETE",QDialogButtonBox.ActionRole)
        inquireButton = buttonBox.addButton("&查询",QDialogButtonBox.ActionRole)

        #设置按钮内字体样式
        self.addButton.setFont(font)
        # okButton.setFont(font)
        # deleteButton.setFont(font)
        inquireButton.setFont(font)

        #垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.qle)
        layout.addWidget(buttonBox)
        layout.addWidget(self.MyTable)
        self.setLayout(layout)

        #addButton.clicked.connect(partial(self.add_data,cur,db))#插入实现
        #okButton.clicked.connect(partial(self.up_data, cur, db,col_lst))#插入实现
        #deleteButton.clicked.connect(partial(self.del_data,cur,db))#删除实现
        inquireButton.clicked.connect(partial(self.inq_data,db))#查询实现



    #打开录入界面
    def add_data(self,cur,db):
        neww=lvru_window
        neww.show()


    #插入数据
    # def up_data(self,cur,db,col_lst):
    #     row_1 = self.MyTable.rowCount()
    #
    #     value_lst = []
    #     for i in range(len(col_lst)):
    #         if(len(self.MyTable.item(row_1-1,i).text())==0):
    #             value_lst.append(None)
    #         else:
    #             value_lst.append(self.MyTable.item(row_1-1,i).text())
    #
    #     tup_va_lst = []
    #     for cl,va in zip(col_lst,value_lst):
    #         tup_va_lst.append((cl,va))
    #
    #     #插入语句
    #     cur.execute(
    #         "INSERT INTO pm_25 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",value_lst)



    #删除
    # def del_data(self,cur,db):
    #     #是否删除的对话框
    #     reply = QMessageBox.question(self, 'Message', 'Are you sure to delete it ?', QMessageBox.Yes | QMessageBox.No,
    #                                  QMessageBox.No)
    #     if reply ==  QMessageBox.Yes:
    #         #当前行
    #         row_2 = self.MyTable.currentRow()
    #         del_d = self.MyTable.item(row_2, 0).text()
    #
    #         #在数据库删除数据
    #         cur.execute("DELETE FROM pm_25 WHERE f_id = '"+del_d+"'")
    #         db.commit()
    #
    #         #删除表格
    #         self.MyTable.removeRow(row_2)

    #查询
    def inq_data(self,db):
        cur = db.cursor()
        #txt=self.qle.text()
        text1 = self.qle.text()

        # keywordlist=nlp.abkeyword(text1)
        # txt="".join(keywordlist)
        #模糊查询 
        if len(text1) != 0:
            try:
                print("asiidhsai")
                cur.execute("SELECT 问题描述,短期措施,长期措施,根本原因 FROM EMPLOYEE WHERE 问题描述 LIKE '%"+txt+"%' or 根本原因 LIKE '%"+txt+"%'")# CONCAT('f_id','f_area','f_place','f_AQI','f_AQItype','f_PM25per1h'),concat(concat('%','#txt'),'%')
                print("asiidhsai1")
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
            except mysql.connector.Error as e:
                print('query error!{}'.format(e))
        #空输入返回原先数据表格
        else:
            self.MyTable.clearContents()
            cur.execute("SELECT 问题描述,短期措施,长期措施,根本原因 FROM EMPLOYEE")
            data_y = cur.fetchall()
            row_5 = len(data_y)
            vol_1 = len(cur.description)
            for i_x_1 in range(row_5):
                for j_y_1 in range(vol_1):
                    temp_data_2 = data_y[i_x_1][j_y_1]  # 临时记录，不能直接插入表格
                    data_2 = QTableWidgetItem(str(temp_data_2))  # 转换后可插入表格
                    self.MyTable.setItem(i_x_1, j_y_1, data_2)


class lvru_window(QDialog):
    def __init__(self, parent=None):
        super(lvru_window, self).__init__(parent)

        # 设置界面大小、名称
        self.setFixedSize(1000, 1200)
        self.setWindowTitle('故障诊断专家系统录入')
        self.setWindowFlags(Qt.Widget)

        #施工日期
        self.workdate = QDateEdit(QDate.currentDate(), self)
        self.workdate.setDisplayFormat('yyyy/MM/dd')
        self.work.date.setCalendarPopup(True)

        #施工开始时间

        self.starttime = QTimeEdit(QTime.currentTime(), self)                                # 6
        self.starttime.setDisplayFormat('HH:mm:ss')

        #施工结束时间
        self.endtime = QTimeEdit(QTime.currentTime(), self)                                # 6
        self.endtime.setDisplayFormat('HH:mm:ss')

        #状态
        state= ["竣工", "结算", "暂停"]
        title1=QLabel("状态")
        title1.setAlignment(Qt.AlignCenter)
        self.combox1 = QComboBox(self)
        self.combox1.addItems(state)

        #备注
        title21 = QLabel("备注")
        title21.setAlignment(Qt.AlignCenter)
        self.beizhu=QTextEdit()
        #self.beizhu.set



        xiangmu = ["CSS", "GF9","CVT","GFE","GM","NGC"]
        title2 = QLabel("项目名称")
        title2.setAlignment(Qt.AlignCenter)
        self.combox2 = QComboBox(self)
        self.combox2.addItems(xiangmu)


        jianduan = ["P1", "P2", "P3", "NA"]
        title3 = QLabel("阶段")
        title3.setAlignment(Qt.AlignCenter)
        self.combox3 = QComboBox(self)
        self.combox3.addItems(jianduan)


        shengchanxian = ["ASSY", "CB", "BL", "BU","HA","EA"]
        title4 = QLabel("生产线")
        title4.setAlignment(Qt.AlignCenter)
        self.combox4 = QComboBox(self)
        self.combox4.addItems(shengchanxian)


        wentilaiyuan = ["GRAT", "PPCR", "SOP", "项目实施", "内外评审", "Pre-launch"]
        title5 = QLabel("问题来源")
        title5.setAlignment(Qt.AlignCenter)
        self.combox5 = QComboBox(self)
        self.combox5.addItems(wentilaiyuan)


        title6 = QLabel("工位")
        title6.setAlignment(Qt.AlignCenter)
        self.textbox6= QLineEdit(self)
        self.textbox6.setFixedSize(200,30)

        gongyihuafen = ["压装", "取料", "安装", "润滑", "拧紧", "清洗"]
        title7 = QLabel("工艺划分")
        title7.setAlignment(Qt.AlignCenter)
        self.combox7 = QComboBox(self)
        self.combox7.addItems(gongyihuafen)


        wentishuxing = ["产品设计", "机械（设计）", "电气控制", "来料", "工艺规范", "机械（硬件调整）","工艺规范","货品拖期"]
        title8 = QLabel("问题属性")
        title8.setAlignment(Qt.AlignCenter)
        self.combox8 = QComboBox(self)
        self.combox8.addItems(wentishuxing)


        qianzaiyingxiang = ["质量", "FTA", "开动率", "安全", "人机"]
        title9 = QLabel("潜在影响")
        title9.setAlignment(Qt.AlignCenter)
        self.combox9 = QComboBox(self)
        self.combox9.addItems(qianzaiyingxiang)

        wentidengji = ["高", "中", "低"]
        title10 = QLabel("问题等级")
        title10.setAlignment(Qt.AlignCenter)
        self.combox10 = QComboBox(self)
        self.combox10.addItems(wentidengji)

        jidi = ["JQPT", "DYPT", "WHPT","NSPT","PTME"]
        title11 = QLabel("基地")
        title11.setAlignment(Qt.AlignCenter)
        self.combox11 = QComboBox(self)
        self.combox11.addItems(jidi)

        title12 = QLabel("提出者")
        title12.setAlignment(Qt.AlignCenter)
        self.textbox12= QLineEdit(self)
        self.textbox12.setFixedSize(200,30)


        # <editor-fold desc="三组日期显示，变量date13.date14.date15">
        self.btn13= QPushButton("选择提出日期")
        self.btn13.clicked.connect(self.openCalendar13)
        self.le13 = QLabel(self)
        self.le13.setAlignment(Qt.AlignCenter)
        self.cal13 = QCalendarWidget(self)
        self.cal13.setMinimumDate(QDate(2017, 1, 1))  # 设置日期最小范围
        self.cal13.setMaximumDate(QDate(2019, 12, 30))  # 设置日期最大范围
        self.cal13.setGridVisible(True)  # 是否显示日期之间的网格
        self.cal13.hide()  # 隐藏日期控件
        self.cal13.clicked[QDate].connect(self.showDate13)
        date13 = self.cal13.selectedDate()  # 获取选中日期，默认当前系统时间
        self.le13.setText(date13.toString('yyyy-MM-dd'))

        self.btn14= QPushButton("选择计划关闭日期")
        self.btn14.clicked.connect(self.openCalendar14)
        self.le14 = QLabel(self)
        self.le14.setAlignment(Qt.AlignCenter)
        self.cal14 = QCalendarWidget(self)
        self.cal14.setMinimumDate(QDate(2017, 1, 1))  # 设置日期最小范围
        self.cal14.setMaximumDate(QDate(2019, 12, 30))  # 设置日期最大范围
        self.cal14.setGridVisible(True)  # 是否显示日期之间的网格
        self.cal14.hide()  # 隐藏日期控件
        self.cal14.clicked[QDate].connect(self.showDate14)
        date14 = self.cal14.selectedDate()  # 获取选中日期，默认当前系统时间
        self.le14.setText(date14.toString('yyyy-MM-dd'))

        self.btn15= QPushButton("选择实际关闭日期")
        self.btn15.clicked.connect(self.openCalendar15)
        self.le15 = QLabel(self)
        self.le15.setAlignment(Qt.AlignCenter)
        self.cal15 = QCalendarWidget(self)
        self.cal15.setMinimumDate(QDate(2017, 1, 1))  # 设置日期最小范围
        self.cal15.setMaximumDate(QDate(2019, 12, 30))  # 设置日期最大范围
        self.cal15.setGridVisible(True)  # 是否显示日期之间的网格
        self.cal15.hide()  # 隐藏日期控件
        self.cal15.clicked[QDate].connect(self.showDate15)
        date15 = self.cal15.selectedDate()  # 获取选中日期，默认当前系统时间
        self.le15.setText(date15.toString('yyyy-MM-dd'))
        # </editor-fold>

        self.label16 = QLabel(self)
        self.label16.setText("故障图片")
        self.label16.setFixedSize(250, 150)
        self.label16.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}")
        btn16 = QPushButton(self)
        btn16.setText("上传故障图片")
        btn16.clicked.connect(self.openimage)


        label17 = QLabel("问题状态")
        label17.setAlignment(Qt.AlignCenter)
        self.btn17 = QRadioButton('1/4')
        self.btn17.setCheckable(True)
        self.btn17.clicked.connect(lambda: self.btnstate(self.btn17))
        self.btn18 = QRadioButton('1/2')
        self.btn18.setCheckable(True)
        self.btn18.clicked.connect(lambda: self.btnstate(self.btn18))
        self.btn19 = QRadioButton('3/4')
        self.btn19.setCheckable(True)
        self.btn19.clicked.connect(lambda: self.btnstate(self.btn19))
        self.btn20 = QRadioButton('1')
        self.btn20.setCheckable(True)
        self.btn20.clicked.connect(lambda: self.btnstate(self.btn20))
        self.label18 = QLabel("     ")
        self.label18.setAlignment(Qt.AlignCenter)



        title21 = QLabel("问题描述")
        title21.setAlignment(Qt.AlignCenter)
        self.textbox21=QTextEdit()


        zhanwei2122 = QLabel("   ")

        title22 = QLabel("短期措施")
        title22.setAlignment(Qt.AlignCenter)
        self.textbox22=QTextEdit()

        zhanwei2223 = QLabel("   ")

        title23 = QLabel("长期措施")
        title23.setAlignment(Qt.AlignCenter)
        self.textbox23=QTextEdit()

        zhanwei23table = QLabel("   ")

        title24 = QLabel("根本原因")
        title24.setAlignment(Qt.AlignCenter)
        self.MyTable = QTableWidget(1, 3)
        font = QtGui.QFont('微软雅黑', 8)
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(["序号","根本原因","概率"])
        self.MyTable.setColumnWidth(0, 40)
        self.MyTable.setColumnWidth(1, 530)
        self.MyTable.setColumnWidth(2, 40)
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)
        self.btn24= QPushButton("新增一条原因")
        self.btn24.clicked.connect(self.addrow)

        #q用来存放二维字典


        self.btn25 = QPushButton("提交")
        font25 = QtGui.QFont('微软雅黑', 15)
        self.btn25.setFont(font25)
        self.btn25.setFixedSize(70, 40)
        self.btn25.clicked.connect(self.lurushujuku)

        self.btn26 = QPushButton("取消")
        self.btn26.setFont(font25)
        self.btn26.setFixedSize(70, 40)
        self.btn26.clicked.connect(lambda :self.close())

        self.title27 = QLabel("内容")
        #表格布局
        grid = QGridLayout()
        grid.setSpacing(5)  # 创建标签之间的空间
        grid.addWidget(title1, 1, 0)
        grid.addWidget(self.combox1, 1, 1)
        grid.addWidget(title2, 1, 2)
        grid.addWidget(self.combox2, 1, 3)
        grid.addWidget(title3, 1, 4)
        grid.addWidget(self.combox3, 1, 5)
        grid.addWidget(title4, 2, 0)
        grid.addWidget(self.combox4, 2, 1)
        grid.addWidget(title5, 2, 2)
        grid.addWidget(self.combox5, 2, 3)
        grid.addWidget(title6, 2, 4)
        grid.addWidget(self.textbox6, 2, 5)
        grid.addWidget(title7, 3, 0)
        grid.addWidget(self.combox7, 3, 1)
        grid.addWidget(title8, 3, 2)
        grid.addWidget(self.combox8, 3, 3)
        grid.addWidget(title9, 3, 4)
        grid.addWidget(self.combox9, 3, 5)
        grid.addWidget(title10, 4, 0)
        grid.addWidget(self.combox10, 4, 1)
        grid.addWidget(title11, 4, 2)
        grid.addWidget(self.combox11, 4, 3)
        grid.addWidget(title12, 4, 4)
        grid.addWidget(self.textbox12, 4, 5)
        grid.addWidget(self.btn13, 5, 0)
        grid.addWidget(self.le13, 5, 1)
        grid.addWidget(self.cal13, 6, 0,1,2)
        grid.addWidget(self.btn14, 5, 2)
        grid.addWidget(self.le14, 5, 3)
        grid.addWidget(self.cal14, 6, 2,1,2)
        grid.addWidget(self.btn15, 5, 4)
        grid.addWidget(self.le15, 5, 5)
        grid.addWidget(self.cal15, 6, 4,1,2)
        grid.addWidget(btn16, 7, 0)
        grid.addWidget(self.label16, 7, 1,1,2)
        grid.addWidget(label17, 8, 0)
        grid.addWidget(self.label18, 8, 5)
        grid.addWidget(self.btn17, 8, 1)
        grid.addWidget(self.btn18, 8, 2)
        grid.addWidget(self.btn19, 8, 3)
        grid.addWidget(self.btn20, 8, 4)
        grid.addWidget(title21, 9, 0)
        grid.addWidget(self.textbox21, 9, 1,2,5)
        grid.addWidget(zhanwei2122, 10, 0)
        grid.addWidget(title22, 11, 0)
        grid.addWidget(self.textbox22, 11, 1,2,5)
        grid.addWidget(zhanwei2223, 12, 0)
        grid.addWidget(title23, 13, 0)
        grid.addWidget(self.textbox23, 13, 1,2,5)
        grid.addWidget(zhanwei23table, 14, 0)
        grid.addWidget(title24, 15, 0)
        grid.addWidget(self.MyTable, 15, 1, 2, 4)
        grid.addWidget(self.btn24, 15, 5)
        grid.addWidget(self.btn25, 17, 3)
        grid.addWidget(self.btn26, 17, 2)
        grid.addWidget(self.title27, 18, 2)
        self.setLayout(grid)



    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self, '消息', '是否关闭录入窗口？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
    def lurutanchu(self):
        if not self.isVisible():
            self.show()
    def showDate13(self,date13):
        self.le13.setText(date13.toString("yyyy-MM-dd"))
        self.cal13.close()  # 关闭日期控件
    def openCalendar13(self):
        self.cal13.show()  # 显示日期控件
    def showDate14(self,date14):
        self.le14.setText(date14.toString("yyyy-MM-dd"))
        self.cal14.close()  # 关闭日期控件
    def openCalendar14(self):
        self.cal14.show()  # 显示日期控件

    def showDate15(self,date15):
        self.le15.setText(date15.toString("yyyy-MM-dd"))
        self.cal15.close()  # 关闭日期控件
    def openCalendar15(self):
        self.cal15.show()  # 显示日期控件
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label16.width(), self.label16.height())
        self.label16.setPixmap(jpg)
    def btnstate(self, btn):
        if btn.text() == '1/4':
            if btn.isChecked() == True:
                self.label18.setText("已选择1/4")
        if btn.text() == "1/2":
            if btn.isChecked() == True:
                self.label18.setText("已选择1/2")
        if btn.text() == '3/4':
            if btn.isChecked() == True:
                self.label18.setText("已选择3/4")
        if btn.text() == "1":
            if btn.isChecked() == True:
                self.label18.setText("已选择1")
    def addrow(self):
        self.MyTable.setRowCount(self.MyTable.rowCount()+1)

    def lurushujuku(self):
        a = self.combox1.currentText()
        b = self.combox2.currentText()
        l = self.textbox12.text()
        k = self.combox11.currentText()
        j = self.combox10.currentText()
        i = self.combox9.currentText()
        h = self.combox8.currentText()
        g = self.combox7.currentText()
        f = self.textbox6.text()
        e = self.combox5.currentText()
        d = self.combox4.currentText()
        c = self.combox3.currentText()
        date13=self.le13.text()
        date14 = self.le14.text()
        date15 = self.le15.text()
        r = Binary(self.label16.pixmap())#输出了这样的值：PyQt5.QtGui.QPixmap object at 0x000002657B54CCF8         数据类型：PyQt5.QtGui.QPixmap
        state1=self.label18.text()
        state=state1[3:]
        o = self.textbox23.toPlainText()
        n = self.textbox22.toPlainText()
        m = self.textbox21.toPlainText()
        rowc = self.MyTable.rowCount()

        p = ""
        for ix in range(0,rowc):
            p=p+self.MyTable.item(ix,0).text()+"."+self.MyTable.item(ix, 1).text()+" "+self.MyTable.item(ix, 2).text()+"\r\n"
        #print(type(a,b,c,d,e,f,g,h,i,j,k,l,date13,r,state,o,m,n,p))
        print(type(r))
        dt_now = date.strftime('%Y-%m-%d %H:%M:%S')#记录录入时间

        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='expertsy',
            charset='utf8',
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = """ INSERT INTO EMPLOYEE (PT,项目名称,阶段,生产线,工位,问题来源,工艺划分,问题属性,潜在影响,问题等级,提出者,基地,问题照片,问题状态,提出日期,计划关闭日期,实际关闭日期,问题描述,短期措施,长期措施,根本原因)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s,%s)""" % (a, b, c, d, f, e, g, h, i, j, l, k, r,state, date13, date14, date15, m, n, o, p)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print('新增条目失败')
            print(e)
            conn.rollback()
def main():
    #显示
    app = QApplication(sys.argv)

    c = creat_view()
    d = lvru_window()
    c.addButton.clicked.connect(d.lurutanchu)
    c.show()

    sys.exit(app.exec_())

main()