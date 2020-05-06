from tkinter import *
import tkinter.ttk as ttk
import os
from tkinter.messagebox import *
import change_password as ps
import Db_school_1
class Main_Windows(Tk):
    """
    主窗体的构造函数
        1. current_user,current_time的引入是为了加载logingui.py窗体中用户输入及加载登录时间记录时间的参数
        2. 同样设计主窗体下界面的布局及配置
    """
    def __init__(self,current_login_user,current_time): #current_login_user为了实现登录信息的加载（记录logingui界面中当前用户是谁）
                                                 #current_time同样是为了记录当前用户登录的系统时间
        super().__init__()
        self.title("主窗体")
        self.geometry("1200x700+1+20")  # 通过控制图像大小可以通过+号来调整窗体出现的位置
        self.resizable(0, 0)  # 固定窗体大小.不允许改动窗体大小. resizable(0,0)表示x轴为0y轴也为0
        self.iconbitmap(R"china.ico")  # 加载.ico文件到窗口小图标. 网上可以将png转成ico文件
        # 添加图片背景色
        self["bg"] = "RoyalBlue"

        #设置全局变量
        self.login_times = current_time #为了记录用户的登录时间
        self.current_stu_list = [] #存储双击行匹配到的最终数据
        self.get_number_result = [] #用户存储获取到的所有学员信息
       
        self.action_flag = 0  #设置查看/修改/添加学生信息的title值,默认为0
        self.current_user_list = current_login_user  #把login界面的list传到主界面接收

        #加载窗体
        self.Setup_UI()

        #将窗体的行为转化为方法
        self.protocol("WM_DELETE_WINDOW",self.close_windows)    #"WM_DELETE_WINDOW"为固定写法

    def Setup_UI(self):
        """
        布局主窗体的窗体并对其中的控件属性进行配置
        :return:
        """
        #设置Sytle配置控件的属性
        self.Style01 = ttk.Style()
        self.Style01.configure("left.TPanedwindow",background="RoyalBlue")
        self.Style01.configure("right.TPanedwindow", background="skyblue")
        self.Style01.configure("TButton",font = ("微软雅黑",12,"bold"))
        self.Style01.configure("TLabel", font=("微软雅黑", 10, "bold"))
        self.Style01.configure("labframe.TButton", font=("微软雅黑", 10, "bold"))
        self.Style01.configure("title1.TLabel", font=("微软雅黑", 10, "bold"),background = "lightblue")

        # 加载窗体图片
        self.login_img = PhotoImage(file=R"1.png")
        self.label_img = ttk.Label(self, image=self.login_img)
        self.label_img.pack()

        #加载当前用户和时间
        self.label_login_user = ttk.Label(self,text = "当前登录用户:" + str(self.current_user_list[0]).title() +
                                                      "\n登录时间:" + self.login_times,style = "title1.TLabel" )

        self.label_login_user.place(x=1000,y=165)

        # 左边按钮区域的布局
        self.pan_left = ttk.PanedWindow(width =200,height=500,style ="left.TPanedwindow")
        self.pan_left.pack(side = LEFT,padx=3,pady=1)

        # 添加左边区域按钮
        self.buttion_useradd = ttk.Button(self.pan_left,text = "添加学生信息",width =12,command = self.add_student)
        self.buttion_useradd.place(x = 30,y = 20)

        self.buttion_userupdate = ttk.Button(self.pan_left,text = "修改学生信息",width =12,command = self.update_student)
        self.buttion_userupdate.place(x = 30,y = 60)

        self.buttion_userdelete = ttk.Button(self.pan_left,text = "删除学生信息",width =12,command = self.delete_student)
        self.buttion_userdelete.place(x = 30,y = 100)

        #改动区***********************************************************************************************************
        
        
        self.buttion_changepassword = ttk.Button(self.pan_left,text = "更改密码",width =12,command = self.change_password_windows)
        self.buttion_changepassword.place(x = 30,y = 180)
        self.buttion_changepassword = ttk.Button(self.pan_left,text = "查看签到信息",width =12,command = self.view_student)
        self.buttion_changepassword.place(x = 30,y = 140)
        self.buttion_changepassword = ttk.Button(self.pan_left,text = "帮助",width =12,command = self.soft_help)
        self.buttion_changepassword.place(x = 30,y = 220)
        
        #右边按钮区域的布局
        self.pan_right = ttk.PanedWindow(width = 991,height = 500,style = "right.TPanedwindow" )
        self.pan_right.pack(side = LEFT)

        # 添加查询区域(属于右边区域)
        self.labelFrame_query = ttk.LabelFrame(self.pan_right,text = "学生信息",width =990,height = 60)
        self.labelFrame_query.place(x=1,y=1)

        #添加控件
        self.label_number = ttk.Label(self.labelFrame_query,text = "学号:")
        self.label_stu_no = StringVar()
        self.label_number.place(x =10,y =10)
        self.entry_number = ttk.Entry(self.labelFrame_query,textvariable = self.label_stu_no,font = ("微软雅黑",10,"bold"),width=8)
        self.entry_number.place(x =55,y =10)

        self.label_name = ttk.Label(self.labelFrame_query,text = "姓名:")
        self.get_stu_name = StringVar()
        self.label_stu_name = StringVar()
        self.label_name.place(x =130,y =10)

        self.entry_name = ttk.Entry(self.labelFrame_query,textvariable = self.get_stu_name,font = ("微软雅黑",10,"bold"),width=10)
        self.entry_name.place(x =175,y =10)

        self.label_age = ttk.Label(self.labelFrame_query,text = "年龄:")
        self.get_stu_age = StringVar()
        self.label_age.place(x =270,y =10)
        self.entry_age = ttk.Entry(self.labelFrame_query,textvariable=self.get_stu_age,font = ("微软雅黑",10,"bold"),width=5)
        self.entry_age.place(x =314,y =10)

        self.label_department = ttk.Label(self.labelFrame_query,text = "所在系:")
        self.get_stu_department = StringVar()
        self.label_department.place(x =360,y =10)
        self.entry_department = ttk.Entry(self.labelFrame_query,textvariable=self.get_stu_department,font = ("微软雅黑",10,"bold"),width=16)
        self.entry_department.place(x =415,y =10)

        self.label_class = ttk.Label(self.labelFrame_query,text = "班级:")
        self.get_stu_class = StringVar()
        self.label_class.place(x =546,y =10)
        self.entry_class = ttk.Entry(self.labelFrame_query,textvariable=self.get_stu_class,font = ("微软雅黑",10,"bold"),width=14)
        self.entry_class.place(x =594,y =10)

        self.button_search = ttk.Button(self.labelFrame_query,text = "查询",width=6,style="labframe.TButton",command = self.get_student_result)
        self.button_search.place(x=790, y=10)

        self.button_homepage = ttk.Button(self.labelFrame_query,text = "返回主页面",width=10,style="labframe.TButton",command = self.load_all_data)
        self.button_homepage.place(x=860, y=10)

    def soft_help(self):
        showinfo("使用帮助","这是一个使用帮助")
    
    def get_student_result(self):
        
        """
        获取输入的值
        """
        #清空get_number_result中的数据(因为每次查询一个stu_number就显示一条.如果不清空就会每次查询的结果都会被显示)
        self.get_number_result.clear()

        #获取输入的值
        get_input = []
        get_input.append(self.label_stu_no.get().strip())
        get_input.append(self.get_stu_name.get().strip())
        #get_input.append(self.get_stu_age.get().strip())
        get_input.append(self.get_stu_department.get().strip())
        get_input.append(self.get_stu_class.get().strip())

        
        return get_input
        #分别获得输入框中的学号，姓名，年龄，所在系，班级
    
 
    def add_student(self):

        try:
            get_input = self.get_student_result()
            list1 = ['s_id','s_name','department','class_id']
            sql1 ='insert into student('

            sql2 =') values('
            for i in range(4):
                if get_input[i]!='':
                    if(i==0):
                        sql1 = sql1 + list1[i]
                        sql2 = sql2 + get_input[i]
                    else:
                        sql1 =  sql1 +','+ list1[i]
                        sql2 =  sql2 + ',' + get_input[i]
            sql = sql1 + sql2+')'

            student  = Db_school_1.Student()
            student.insert(sql)
            print('成功')
        except Exception:
            print('失败')
                        
                
                    

        
        
        
    def update_student(self):
        try:
            #通过学生学号来查找对应的学生
            get_input = self.get_student_result()
            sql1 = 'update student set '
            list1 = ['s_id', 's_name', 'department', 'class_id']
            for i in range(1,4):
                if(get_input[i]!=''):
                    if sql1[-1]==' ':

                        sql1 =sql1 +  '%s=\' %s\''%(list1[i],get_input[i])
                    else:
                        sql1 = sql1 +','+ '%s=\' %s\'' % (list1[i], get_input[i])
            sql =sql1+ ' where s_id = \'%s\''%get_input[0]


            student = Db_school_1.Student()
            student.insert(sql)
            print('成功')
        except Exception:
            print('失败')

     

    def view_student(self):
        try:
            def get_cname(c_id):
                student = Db_school_1.Student()
                student.get('select c_name from class where c_id = \'%s\''%c_id)
                return  student.get_one()
            get_input = self.get_student_result()

            student = Db_school_1.Student()
            sql = 'select * from sign_in where s_id = \'%s\''%get_input[0]
            print(sql)
            student.get(sql)

            xinxi = student.get_all()

            sql = 'select * from student where s_id =\'%s\' '%get_input[0]
            print(sql)
            student.get(sql )
            s= student.get_one()
            print(s)
            print(xinxi)
            s_id = s['s_id']
            s_name = s['s_name']

            ffffffff=[]
            for x in xinxi:

                ffffffff.append([s_id,s_name,x['c_id'],get_cname(x['c_id'])['c_name'],str(x['date']),x['state']])
            #你来操作这个FFFFFFF
            print('成功')
            return ffffffff

        except Exception:
            print('失败')


   

    def delete_student(self):
        try:
            get_input = self.get_student_result()
            student = Db_school_1.Student()
            student.get('delete from student where s_id = \'%s\''%get_input[0])
            print('成功')
        except Exception:
            print('失败')



    
    

    def close_windows(self):
        """
        1.提醒用户关闭窗口前是否保存数据
        2.保存数居前先清空数据再保存数据
        :return:
        """
        choose = askyesno("系统关闭提醒","是否将修改的数据保存到文件？")
        if choose:
            try:
                pass
                #####保存到数据库
            except:
                showinfo("系统消息","写入文件出错！")

            #提醒
            showinfo("系统消息","文件写入成功！")

            #关闭窗体
            self.destroy()
        else:
            self.destroy()

    def change_password_windows(self):
        this_password_windows = ps.change_User_password(self.current_user_list)
        #把list绑定到change_password_windows中
    

if __name__ == "__main__":
    pass
    #this_main_window = Main_Windows()
    #this_main_window.mainloop()


