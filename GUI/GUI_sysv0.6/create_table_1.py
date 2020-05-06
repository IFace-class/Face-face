import pymysql

if __name__=='__main__':
    conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd="yzm115287",
            db="db_school",
            charset="utf8"
        )
    cursor = conn.cursor()
    
    
    student = 'create table student( \
s_id char(8),\
s_name varchar(20) not null,\
face varchar(3000),\
department varchar(20) not null,\
class_id char(4),\
primary key(s_id))'
    cursor.execute(student)

    
    Class ='create table class(\
c_id char(4),\
c_name varchar(20) not null,\
primary key(c_id))'
    cursor.execute(Class)
    
    teacher = 'create table teacher(\
t_id char(4),\
t_name varchar(20) not null,\
department varchar(20),\
face varchar(3000),\
primary key(t_id)\
)'
    cursor.execute(teacher)

    
    student_class = 'create table student_class(\
s_id char(8),\
c_id char(4),\
score char(3),\
term varchar(20),\
number int,\
primary key(s_id,c_id),\
FOREIGN KEY ( s_id  ) REFERENCES student( s_id ),\
foreign key (c_id) references class(c_id))'
    cursor.execute(student_class)

    
    teacher_class =  'create table teacher_class(\
t_id char(4),\
c_id char(4),\
classes varchar(40),\
term varchar(20),\
primary key(t_id,c_id),\
foreign key (t_id) references teacher(t_id),\
foreign key (c_id) references class(c_id))'
    cursor.execute(teacher_class)

    schedule = 'create table schedule (\
c_id char(4) ,\
date date ,\
classes varchar(40),\
room varchar(20),\
primary key (c_id,date),\
foreign key (c_id) references class(c_id))'
    cursor.execute(schedule)

    cursor.execute('CREATE INDEX date_ ON schedule(date)');
               
    sign_in = 'create table sign_in (\
s_id char(8),\
c_id char(4),\
date date,\
state char(3),\
primary key(s_id,c_id,date),\
foreign  key (s_id) references student(s_id),\
foreign  key (c_id) references schedule(c_id),\
foreign  key (date) references schedule(date))'
    cursor.execute(sign_in)
    
    
    
    audit = 'create table audit(\
s_id char(8),\
c_id char(8),\
date date,\
t_id  char(4),\
primary key(s_id,c_id),\
foreign key (s_id) references student(s_id),\
foreign  key (c_id) references schedule(c_id),\
foreign  key (date) references schedule(date))'
    cursor.execute(audit)

    conn.commit()




