from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import *

class Detail_Windows(Toplevel): # 这里要用Toplevel不能用Tk因为tkinter只支持一个主窗体存在.要想再跳出一个窗体必须选Toplevel
    def __init__(self,action_flag:int,current_stu:list,all_stu_list:list):
        super().__init__()
        self.title("学生信息窗体")
        self.geometry("700x600+300+100")  # 通过控制图像大小可以通过+号来调整窗体出现的位置
        self.resizable(0, 0)  # 固定窗体大小.不允许改动窗体大小. resizable(0,0)表示x轴为0y轴也为0
        #self.iconbitmap(R"C:\Users\Administrator\python_图库\china.ico")  # 加载.ico文件
        self["bg"] = "RoyalBlue"

        #设置全局变量
        self.flag = action_flag  #接收构造函数中action_flag中的值.（为了判断传进来的是添加,修改还是删除等状态值）
        self.current_student_list = current_stu # 接收构造函数中current_stu传进来的值（为了接收选中行中的值）
        # self.all_stu_list = all_stu_list接收构造函数中all_stu_list传进来的值(强调主窗体中all_list中的值最终跟我们子窗体中all_stu_list中的值相同.因为传的是地址)

        # 加载窗体
        self.Setup_UI()
        self.load_windows_flag()
    def Setup_UI(self):
        # 通过style设置属性
        self.Style01 = ttk.Style()
        self.Style01.configure("titel2.TLabel", font=("微软眼黑", 24, "bold"), foreground="darkred")
        self.Style01.configure("TPanedwindow", background="lightcyan")#RoyalBlue
        self.Style01.configure("TButton", font=("微软眼黑", 11), background="RoyalBlue", foreground="black")
        self.Style01.configure("TLabel",font=("微软眼黑", 14, "bold"), foreground="black",background="lightcyan")
        self.Style01.configure("TRadiobutton",font=("微软眼黑", 14, "bold"), foreground="black",background="lightcyan")

        #加载窗体图片
        self.login_img = PhotoImage(file = R"beijingtu.png")
        self.label_img = ttk.Label(self,image = self.login_img)
        self.label_img.pack()

        #添加Titile框体
        self.var_titel = StringVar()
        self.title_label = ttk.Label(self,textvariable=self.var_titel,style = "titel2.TLabel")
        self.title_label.place(x = 20,y = 30)

        #添加一个Panewindows
        self.pane = ttk.PanedWindow(self,width=696, height=450, style="TPanedwindow")
        self.pane.place(x=2,y=98)

        #添加学员信息属性

        self.label_number = ttk.Label(self.pane,text = "学号",style="stu_number.TLabel")
        self.var_stunumber=StringVar()
        self.label_number.place(x=30, y=20)
        self.entry_number = ttk.Entry(self.pane,textvariable = self.var_stunumber,font=("微软眼黑",12, "bold"),width=8)
        self.entry_number.place(x=80, y=20)

        self.label_name = ttk.Label(self.pane,text = "姓名",style="TLabel")
        self.var_stuname = StringVar()
        self.label_name.place(x=170, y=20)
        self.entry_name = ttk.Entry(self.pane,textvariable=self.var_stuname,font=("微软眼黑",12, "bold"),width=11)
        self.entry_name.place(x=220, y=20)

        self.label_age = ttk.Label(self.pane,text = "年龄",style="TLabel")
        self.var_age = StringVar()
        self.label_age.place(x=323, y=20)
        self.entry_age = ttk.Entry(self.pane,textvariable=self.var_age,font=("微软眼黑",12, "bold"),width=5)
        self.entry_age.place(x=370, y=20)

        self.label_department = ttk.Label(self.pane, text="所在系：")
        self.label_department.place(x=440, y=20)
        self.var_genter = StringVar()
        self.entry_department = ttk.Entry(self.labelFrame_query,textvariable=self.get_stu_department,font = ("微软雅黑",10,"bold"),width=16)
        self.entry_department.place(x =490,y =20)
        
        self.label_class = ttk.Label(self.pane,text = "班级",style="TLabel")
        self.var_class = StringVar()
        self.label_class.place(x=30, y=70)
        self.entry_class = ttk.Entry(self.pane,textvariable=self.var_brithday,font=("微软眼黑",12, "bold"),width=15)
        self.entry_class.place(x=120, y=70)



        #添加保存,关闭按钮
        self.save_buttion = ttk.Button(self, text="保存", width=10,command = self.submit)
        self.save_buttion.place(x=480, y=560)
        self.exit_buttion = ttk.Button(self, text="退出", width=10,command = self.close_windows)
        self.exit_buttion.place(x=580, y=560)



    def close_windows(self):
        """
        关闭窗口
        :return:
        """
        self.comp_info = 0
        self.destroy()



if __name__ == "__main__":
    this_windows = Detail_Windows()
    this_windows.mainloop()

