import pymysql
def getlist():
    print('此数据库有以下表格：-----')
    print('每个表格都有list函数')
    print('Student')
    print('Class')
    print('Teacher')
    print('Student_class')
    print('Teacher_class')
    print('Schedule')
    print('Sign_in')
    print('Audit')

class Db_school():
    def __init__(self):
        self.conn = self.get_conn()  # 连接对象
        self.cursor = self.get_cursor()  # 游标对象

    def get_conn(self):
        """ 获取连接对象 """
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd="yzm115287",
            db="db_school",
            charset="utf8"
        )
        return conn

    def get_cursor(self):
        """获取游标对象"""
        # cursor = None
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor

    
    def get(self , sql):
        self.cursor.execute(sql)
        '''把数据库中的数据装入内存'''
    def get_all(self):
        """
        查询全部
        :return: [{},{}]
        """
        return self.cursor.fetchall()

    def get_one(self):
        """
        查询一个
        :return: {}
        """
        return self.cursor.fetchone()

    def update(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()
    def insert(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def delete(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()
    
    def commit_data(self, sql):
        """
        提交数据
        :param sql:
        """
        self.conn.commit()
        print("表连接对象，提交成功")

    def __del__(self):
        self.cursor.close()
        self.conn.close()




class Student(Db_school):

        
    def getlist(self):
        print('s_id:Char(8)')
        print('s_name:Varchar(20)')
        print('face:VarChar(3000) 记录的是路径')
        print('department : Varchar(20)')
        print('class_id: Char(4)')
    


class Class(Db_school):
    def getlist(self):
        print('c_id:Char(4)')
        print('c_name:Varchar(20)')



        
class Teacher(Db_school):
    def getlist(self):
        print('t_id:Char(4)')
        print('t_name:Varchar(20)')
        print('department : Varchar(20)')
        print('face:VarChar(3000) 记录的是路径')
        
class Teacher_class(Db_school):
    def getlist(self):
        print('t_id:Char(4)')
        print('c_id:Char(4)')
        print('classes（所教的一或多个班级）: Varchar(40)')
        print('term:VarChar(20)')

class Schedule(Db_school):
    def getlist(self):
        print('c_id:Char(4)')
        print('date : date')
        print('classes: Varchar(40)')
        print('room :Varchar(20)')

        
class Sign_in(Db_school):
    def getlist(self):
        print('s_id : Char(8)')
        print('c_id : Char(4)')
        print('date : date')
        print('state : Char(3)')
        
class Audit(Db_school):
    def getlist(self):
        print('s_id : Char(8)')
        print('c_id : Char(4)')
        print('date : date')
        print('t_id : Char(4)')