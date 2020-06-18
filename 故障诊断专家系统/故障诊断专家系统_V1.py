#导入包
import pymysql
import sys
import os
#import NLP2 as nlp
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


#建立界面类
class Chaxun(QDialog):
    def __init__(self,parent = None):
        super(Chaxun,self).__init__(parent)

        #设置界面大小、名称、背景
        self.setWindowTitle('故障诊断专家系统')
        self.setStyleSheet("background-image:url(tubiao_meitu.jpg)")
        #self.setWindowOpacity(0.9)  # 设置窗口透明度
        #窗体属性
        self.setWindowFlags(Qt.Widget)
        QApplication.setStyle("Fusion")
        font = QtGui.QFont('微软雅黑', 13)
        #self.setWindowFlags(Qt.FramelessWindowHint)#无边框


        #连接数据库
        db = pymysql.connect("localhost", "root", "123456", "expertsy",charset='utf8')
        # #获取游标、数据
        # cur = db.cursor()
        # cur.execute("SELECT 问题描3述,短期措施,长期措施,根本原因 FROM employee")
        # data = cur.fetchall()



        #编辑按钮
        self.qle = QLineEdit()
        self.qle.setFixedSize(800,40)
        self.qle.setStyleSheet('''QLineEdit
        {
        border:1px solid gray;
        width:100px;
        border-radius:10px;
        padding:2px 4px;
        }''')

        buttonBox = QDialogButtonBox()

        self.inquireButton = buttonBox.addButton("&查询",QDialogButtonBox.ActionRole)
        self.inquireButton.setFont(font)
        self.inquireButton.clicked.connect(partial(self.inq_data,db))  # 查询实现


        hron = QHBoxLayout()
        hron.setSpacing(15)  # 创建标签之间的空间
        hron.addWidget(self.qle)
        hron.addWidget(self.inquireButton)
        self.setLayout(hron)


    def inq_data(self,db):
        cur = db.cursor()
        list=[]
        #cur = db.cursor(cursor=pymysql.cursors.DictCursor) #取出字典
        text1 = self.qle.text()
        if len(text1) != 0:
            try:
                #sql="INSERT INTO 查询表 (常见失效,排查序号) VALUES (爱你，123)"
                sql='SELECT 排查序号 FROM 查询表 WHERE 常见失效="%s"' % text1
                cur.execute(sql)
                string = cur.fetchone()
                string0=string[0]
                print(string[0])
                print(type(string0))
                print(string0)
                print(type(string0.split("，")))
                print(string0.split("，"))
                newlist=string0.split("，")
                print(newlist[0])
                for i in newlist:
                    print(i)
                    sql1='SELECT 问题 FROM 问题关联 WHERE 序号="%s"' % i
                    cur.execute(sql1)
                    reslist=cur.fetchone()
                    print(reslist)
                    list.append(reslist[0])
                i = 0
                self.w2 = Weijiejue(list, i)
                self.w2.show()
            except mysql.Error as e:
                print('query error!{}'.format(e))
        else:
            print("请输入")
        print(list)



class Jiejue(QDialog):
    def __init__(self, parent=None):
        super(Jiejue, self).__init__(parent)

        # 设置界面大小、名称
        self.setWindowTitle('专家系统——成功解决')
        self.setWindowFlags(Qt.Widget)
        QApplication.setStyle("Fusion")

        hbox1=QHBoxLayout()
        hbox1.setSpacing(20)
        hbox2 = QHBoxLayout()
        vbox=QVBoxLayout()
        vbox.setSpacing(15)


        zuizhongjielun = QLabel("最终结论" )
        zuizhongjielun.setAlignment(Qt.AlignCenter)
        self.jielun = QLineEdit()
        self.jielun.setFixedSize(800,40)
        self.jielun.setStyleSheet('''QLineEdit
        {
        border:1px solid gray;
        width:300px;
        border-radius:10px;
        padding:2px 4px;
        }''')


        tijiao = QPushButton("提交")
        guanbi = QPushButton("关闭")

        guanbi.clicked.connect(QCoreApplication.instance().quit)
        tijiao.clicked.connect(self.tijiaocom)

        hbox1.addWidget(zuizhongjielun)
        hbox1.addWidget(self.jielun)
        hbox2.addStretch(1)
        hbox2.addWidget(tijiao)
        hbox2.addStretch(2)
        hbox2.addWidget(guanbi)
        hbox2.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)



    def tijiaocom(self):
        res = QMessageBox.question(self, '消息', '是否需要更新相关设备规范/标准模板？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)  # 两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            pass
        else:
            pass
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label16.width(), self.label16.height())
        self.label16.setPixmap(jpg)

class Weijiejue(QDialog):

    def __init__(self,list,i,parent = None):
        super(Weijiejue,self).__init__(parent)
        #设置界面大小、名称、背景
        #self.resize(800,900)
        self.setWindowTitle('故障诊断专家系统')
        self.setStyleSheet("background-image:url(tubiao_meitu.jpg)")
        QApplication.setStyle("Fusion")
        font = QtGui.QFont('微软雅黑',20)
        font1 = QtGui.QFont('微软雅黑light', 15)
        #窗体属性


        self.i1=i
        self.list1=list

        #
        #查询self.list1[self.i1]，得到cankaoziliao字符串，转换为列表
        db = pymysql.connect("localhost", "root", "123456", "expertsy", charset='utf8')
        cur=db.cursor()



        #self.ckzl= ["手册1.pdf","图片1.jpg"]

        vbj = QVBoxLayout()
        vbj.setAlignment(Qt.AlignCenter)
        vbj.setSpacing(50)

        self.hbj1=QHBoxLayout()
        hbj2=QHBoxLayout()
        #

        self.setWindowFlags(Qt.Widget)
        self.paichatishi = QLabel(self.list1[self.i1])
        self.paichatishi.setFont(font)

        sql = 'SELECT 参考资料 FROM 问题关联 WHERE 问题="%s"' % self.list1[self.i1]
        cur.execute(sql)
        string = cur.fetchone()
        print(string)
        if len(string)!=0:
            string0 = string[0]
            self.ckzl = string0.split("，")


            for fuzu in self.ckzl:
                self.title1= QPushButton(fuzu)
                self.title1.setStyleSheet('''
                    QPushButton{
                        border:none;
                        color:blue;
                        font-size:15px;
                        height:30px;
                        padding-left:5px;
                        padding-right:5px;
                        text-align:center;
                    }
                    QPushButton:hover{
                        color:black;
                        border:1px solid #F3F3F5;
                        border-radius:10px;
                        background:LightGray;
                    }
                ''')
                file_path= fuzu
                self.title1.clicked.connect(partial(self.lianjie))
                #title1.clicked.connect(lambda :self.lianjie(file_path))
                self.hbj1.addWidget(self.title1)


        self.jiejuebut=QPushButton("解决了")
        self.jiejuebut.setFont(font1)
        self.weijiejuebut = QPushButton("未解决")
        self.weijiejuebut.setFont(font1)
        self.weijiejuebut.clicked.connect(partial(self.tonext))
        self.jiejuebut.clicked.connect(partial(self.showjiejue))

        hbj2.addStretch(1)
        hbj2.addWidget(self.weijiejuebut)
        hbj2.addStretch(2)
        hbj2.addWidget(self.jiejuebut)
        hbj2.addStretch(1)

        vbj.addStretch(1)
        vbj.addWidget(self.paichatishi)
        vbj.addStretch(2)
        vbj.addLayout(self.hbj1)
        vbj.addStretch(2)
        vbj.addLayout(hbj2)
        vbj.addStretch(1)
        self.setLayout(vbj)

    def tonext(self):

        for i in reversed (range(self.hbj1.count())):

            self.hbj1.itemAt(i).widget().close()
            self.hbj1.takeAt(i)

        changdu=len(self.list1)
        self.i1=self.i1+1
        if self.i1+1<changdu:
            self.paichatishi.setText(self.list1[self.i1])
        if self.i1+1==changdu:
            self.paichatishi.setText(self.list1[self.i1])
            self.weijiejuebut.setText("已经是最后一条")
            self.weijiejuebut.setEnabled(False)

        db = pymysql.connect("localhost", "root", "123456", "expertsy", charset='utf8')
        cur = db.cursor()
        sql = 'SELECT 参考资料 FROM 问题关联 WHERE 问题="%s"' % self.list1[self.i1]
        cur.execute(sql)
        string = cur.fetchone()
        string0 = string[0]
        if not string0 is None:
            print("assa")
            self.ckzl = string0.split("，")
            for fuzu in self.ckzl:
                self.title1= QPushButton(fuzu)
                self.title1.setStyleSheet('''
                                QPushButton{
                                    border:none;
                                    color:blue;
                                    font-size:15px;
                                    height:30px;
                                    padding-left:5px;
                                    padding-right:5px;
                                    text-align:center;
                                }
                                QPushButton:hover{
                                    color:black;
                                    border:1px solid #F3F3F5;
                                    border-radius:10px;
                                    background:LightGray;
                                }
                            ''')
                self.title1.clicked.connect(partial(self.lianjie))
                #title1.clicked.connect(lambda :self.lianjie(file_path))
                self.hbj1.addWidget(self.title1)


    def showjiejue(self):
        self.w3=Jiejue()
        self.w3.show()

    def lianjie(self):
        sender=self.sender()
        os.startfile(sender.text())
def main():
    #显示
    app = QApplication(sys.argv)

    c = Chaxun()
    c.show()

    sys.exit(app.exec_())

main()