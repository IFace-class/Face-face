import Db_school_1
def get(room='一号楼',date='2020-5-4'):
    student = Db_school_1.Student()
    sql = 'select classes from schedule where room=\'%s\' and date=\'%s\''%(room,date)
    student.get(sql)
    classes = student.get_one()['classes']
    
    sql = 'select c_id from schedule where room=\'%s\' and date=\'%s\''%(room,date)
    student.get(sql)
    c_id = student.get_one()['c_id']

    sql = 'select c_name from class where c_id=\'%s\''%c_id
    print(sql)
    student.get(sql)
    c_name = student.get_one()['c_name']
    

    
    Class = classes.split(',')
    list1 = []
    
    for x in Class:
        sql = 'select * from student where class_id=\'%s\'' %(x)
        student.get(sql)
        list1 = list1 + list(student.get_all())

        
    list2 = []
    for x in list1:
        list2.append([x['s_id'],x['s_name'],x['face'],x['department'],x['class_id'],c_id,c_name,date,'0'])
    print(list2)


    


def commit(list1=[['20174595', 'yzm', '[1.1213213,1.2323232]', 'cs', '1703', '0001', '生理健康', '2020-5-4', '0']]):
    #list1里是已经签到的学生？
    student = Db_school_1.Student()
    for  x in list1:
        try:
            sql = 'insert into sign_in(s_id,c_id,date,state) values (\'%s\',\'%s\',\'%s\',\'%s\')'%(x[0],x[-4],x[-2],x[-1])
            print(sql)
            student.update(sql)
        
        except Exception:
            print('呵呵')


    
commit()




    
