import pymysql

#MT,DT
def creattableMT():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='12345678q',
                                 db='peixunjilu',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:

            checksql = '''DROP TABLE IF EXISTS MT'''
            cursor.execute(checksql)
            sql = '''CREATE TABLE MT(
                         id int(10) NOT NULL AUTO_INCREMENT primary key,
                         培训地点 VarChar(255),
                         讲师 VarChar(100),
                         培训日期 VarChar(200),
                         服务中心名称 VarChar(200),
                         学员姓名 VarChar(100),
                         性别 VarChar(10),
                         职务 VarChar(200),
                         电工证 VarChar(20),
                         身份证号码 VarChar(200),
                         联系人邮箱 VarChar(200),
                         电话 VarChar(255),
                         科目1 int(10),
                         科目2 int(10),
                         科目3 int(10))'''
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
creattableMT()