import pymysql

#MT,DT
def creattableMT():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='12345678q',
                                 db='carmanage',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            checksql = '''DROP TABLE IF EXISTS CARINFO'''
            cursor.execute(checksql)
            sql = '''CREATE TABLE CARINFO(
                         id int(10) NOT NULL AUTO_INCREMENT primary key,
                         车架号 VarChar(100),
                         车辆颜色 VarChar(100),
                         车辆型号 VarChar(100),
                         车机版本 VarChar(100),
                         照片1 VarChar(100),
                         照片2 VarChar(100),
                         照片3 VarChar(100),
                         拖运时间 VarChar(100),
                         拖运出发地 VarChar(100),
                         拖运目的地 VarChar(100),
                         拖车时状态 VarChar(155),
                         是否有拖车邮件 VarChar(10),
                         备注 VarChar(255),
                         附件 VarChar(100))'''
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
creattableMT()