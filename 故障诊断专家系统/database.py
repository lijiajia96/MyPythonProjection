import pymysql

def initdb():
   conn = pymysql.connect(
       host='localhost',
       port=3306,
       user='root',
       password='12345678q',
       db='jisuanxitong',
       charset='utf8',
       )
   cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
   cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
   sql = """CREATE TABLE EMPLOYEE(
         序号 INT NOT NULL AUTO_INCREMENT primary key,
         开始日期 CHAR(50),
         车牌号 CHAR(50),
         工单号（事件） CHAR(50),
         施工项目 CHAR(255),
         技师姓名 CHAR(50),
         施工开始时间 CHAR(255),
         施工结束时间 CHAR(255),
         状态 CHAR(30),
         备注 CHAR(255))"""
   cursor.execute(sql)
   cursor.close()
   conn.close()
initdb()

def insertdb(a,b,c,d,e,g,h,i,j,l,k,r,state,date13,date14,date15,m,n,o,p):
   conn = pymysql.connect(
       host='localhost',
       port=3306,
       user='root',
       password='123456',
       db='expertsy',
       charset='utf8',
       ) 
   cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
   sql =""" INSERT INTO EMPLOYEE (PT,项目名称,阶段,生产线,工位,问题来源,工艺划分,问题属性,潜在影响,问题等级,提出者,基地,问题照片,问题状态,提出日期,计划关闭日期,实际关闭日期,问题描述,短期措施,长期措施,根本原因)
           VALUES (%d, %d, %d, %d, %d, %d,%d, %d, %d, %d, %d, %d,%d, %d, %d, %d, %d, %d,%d,%d,%d)""" % (a,b,c,d,f,e,g,h,i,j,l,k,r,state,date13,date14,date15,m,n,o,p)
   try:  
       cursor.execute(sql)
       conn.commit()
   except Exception as e:
       print('新增条目失败')
       print(e)
       conn.rollback()

   cursor.close()
   conn.close()


def searchdb(keyword):
   conn = pymysql.connect(
       host='localhost',
       port=3306,
       user='root',
       password='123456',
       db='expertsy',
       charset='utf8',
       ) 
   cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
   sql = "SELECT * FROM EMPLOYEE \
          WHERE 工艺问题 like '%%%%%s%%%%' order by 先验概率 desc" % (keyword)
   try:  
      cursor.execute(sql)
      res = cursor.fetchall()
      conn.commit()
      return res 
   except:
      print('读取数据库失败')
     
   cursor.close()
   conn.close()
   

def updatadb(qianzaijili,realrate):
   conn = pymysql.connect(
       host='localhost',
       port=3306,
       user='root',
       password='123456',
       db='expertsy',
       charset='utf8',
       )
   cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
   sql = "update EMPLOYEE set 实际概率=%d where 潜在机理=%s" % (realrate,qianzaijili)

   try:  
      cursor.execute(sql)
      conn.commit()
   except:
      print('更新失败')
      conn.rollback()

   cursor.close()
   conn.close()

def deletadb(buxuyao):
   conn = pymysql.connect(
       host='localhost',
       port=3306,
       user='root',
       password='123456',
       db='expertsy',
       charset='utf8',
       ) 
   cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
   sql = "delete from EMPLOYEE where 潜在机理=%s" % (buxuyao) 
   try:  
      cursor.execute(sql)
      conn.commit()
   except:
      conn.rollback()

   cursor.close()
   conn.close()

#initdb()

#a=searchdb('螺栓')
#print(a)

#insertdb('"螺栓断裂"','"结合工件表面带油光滑"', 60 , 10 ,'"1.表面油液擦拭......"' , '"加工改变工艺顺序......"')
#qianzaijili='"结合工件加工孔有飞边"'
#realrate=60
#updatadb(qianzaijili,realrate)
#deletadb('"结合工件加工孔有飞边"')
