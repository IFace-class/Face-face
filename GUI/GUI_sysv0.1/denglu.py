from tkinter import *
import tkinter.ttk as ttk
import os
from tkinter.messagebox import *
from datetime import datetime
# import maingui as man

class Login_Windows(Tk):
    def __init__(self):
        """
        主构造函数
            1. 初始化登录界面窗体
            2. 布局登录窗体并配置各个按键的属性
            3. 实现用户验证功能
        """
        super().__init__()  #初始化框口
        self.title("登录界面")
        self.geometry("640x420+300+200") #通过控制图像大小可以通过+号来调整窗体出现的位置
        self.resizable(0,0) #固定窗体大小.不允许改动窗体大小. resizable(0,0)表示x轴为0y轴也为0
        self.iconbitmap(R"china.ico")
        #添加图片背景色
        self["bg"] = "RoyalBlue" #传统tkinter中配置颜色方法

        #加载窗体
        self.SetUp_UI()

        #设置全局变量
        self.file_path = R"loginuser_info.txt"
        self.user_list = [] #用户存储读取文件中所有的元素
        self.misspasswd_counter = 0 #记录password错误的次数
        self.input_user = "" #记录当前用户
        self.input_password = "" #记录当前用户密码
        self.current_login_list = [] #存储登录的账号和密码

        #自动执行文件中文件的加载
        self.load_localfile_info()
        #showinfo(message=self.user_list) #通过该提示可以直接看文件是否被读取成功！

    #设置GUI页面窗体及控件的布局
    def SetUp_UI(self):
        #通过style设置属性
        self.Style01 = ttk.Style()
        self.Style01.configure("TLabel",font=("微软眼黑",18,"bold"),background = "RoyalBlue",foreground = "white")
        self.Style01.configure("TButton", font=("微软眼黑", 11), background="RoyalBlue", foreground="black")

        #加载窗体图片
        self.login_img = PhotoImage(file =R"school_demo.png")
        self.label_img = ttk.Label(self,image = self.login_img)
        self.label_img.pack(padx = 10,pady = 10)

        #创建Label + Entry ----用户名
        self.username = ttk.Label(self,text = "用户名")
        self.var_user = StringVar() #为了获取键盘输入
        self.username.pack(side = LEFT,padx = 10, pady = 10)
        self.user_entry = ttk.Entry(self,width = 10,textvariable =self.var_user,font=("微软眼黑",13,"bold"))# bold代表字体粗体
        self.user_entry.pack(side = LEFT,padx = 10, pady = 10)

        #创建Label + Entry ----密码
        self.password = ttk.Label(self,text = "密码")
        self.var_password = StringVar()#为了获取键盘输入
        self.password.pack(side = LEFT,padx = 10, pady = 10)
        self.password_entry = ttk.Entry(self,show = "*",width = 10,textvariable=self.var_password,font=("微软眼黑",13,"bold")) #密码密文
        self.password_entry.pack(side = LEFT,padx = 10, pady = 10)

        #创建Button ---- 登录
        self.button_login = ttk.Button(self,text = "登录",command = self.login)
        self.button_login.pack(side = LEFT,padx = 10, pady = 10)
         
        #创建Buttton —— 登录方式****************************************************************************
        self.button_loginway = ttk.Button(self,text = "登录方式",command = self.loginway)     #登录方式（人脸识别）未实现
        self.button_loginway.pack(side = RIGHT,padx = 10, pady = 10)
        
    def load_localfile_info(self):
        """
        加载本地文件:
        :return:
        """
        if not os.path.exists(self.file_path):
            showinfo("系统提示","文件不存在.请确认后重新加载!!")
        else:
            try:
                with open(self.file_path,mode = "r") as fd:
                    current_list = fd.readline() #一次读一行
                    while current_list: #表示直到current_list中所有元素被读完，循环结束
                        temp_list = current_list.split(",")     #按照逗号把每个list中的元素分割出来
                        self.user_list.append(temp_list)    #把分割后的每个元素重新添加到user_list列表中
                        current_list = fd.readline()    #因为我们一次只读一行。读完后如果不加这一句那么循环会一直只读第一行。

            except:
                showinfo("系统信息","文件读取出现异常.请联系管理员！！")
    
    def loginway(self):
        pass         
    def login(self):
        """
        用户身份验证功能的实现
            1. 获取到文件中的用户名，密码,状态(是否被锁定)
            2. 判断用户是否被锁定及是否是规定用户以外的非法用户登录(如果是拒绝登录)
            3. 用户正确判断密码是否匹配，密码不匹配3次被锁定并写入到文件
        :return:
        """
        # 获取输入的用户名及密码
        self.input_user = self.var_user.get()
        self.input_password = self.var_password.get()
        #showinfo("提示信息","用户名：" + input_user + "\n" + "密码：" + input_password)

        #实现身份验证
        for index in range(len(self.user_list)): #这里的user_list 为之前从文件中读取重新存入list列表中的数据
            #先判断用户名是否存在
            if self.input_user.strip().lower() == str(self.user_list[index][0]).strip().lower():
                #如果用户名存在,再判断用户名是否被锁定。1为锁定,0为active.
                if "1" in str(self.user_list[index][2]):
                    showinfo("系统提示", "该用户被锁定.请联系管理员解锁后再登录。")
                    break
                else:
                    #如果用户存在并且是active的状态再判断密码是否正确
                    if self.input_password != str(self.user_list[index][1]):
                        self.misspasswd_counter +=1 #初始值设置为0.如果上述条件不成立则循环加1次
                        if self.misspasswd_counter >=3: #设置密码错误次数最大不能超过3次
                            showinfo("系统提示","密码输入错误3次账号被锁定！")

                            #改变锁定账户的状态(如果错误3次则改变文件中账户的状态把第3个元素变为1代表用户被锁定)
                            self.user_list[index][2] = "1\n" #这里需要加一个空格

                            #写入文件
                            self.write_file()  #调用下列write_file()方法
                        else:
                            showinfo("系统提示", "密码错误，请重新输入")

                        break

                    else:
                        self.misspasswd_counter = 0 #如果输入的password正确那么这里的错误次数还是为0
                        self.current_login_list = self.user_list[index]
                        #用户密码输入都正确则加载主窗体()
                        self.upload_main()
                        break
            #这句话的意思是：循环到最后如果没有找到相同的用户名则用户判定为不存在！！！(这句话为重点,也是因为这句话才循环时用索引)
            if index == len(self.user_list)-1:
                showinfo("系统提示","输入的用户名不存在！")

    def write_file(self):
        """
        写入文件":1.分2次写入第一次先清空原文件，第2次再逐一写入
                 2. 写入的是用户登录后反应的最新的状态信息
        :return:
        """
        try:
            #[1] 先清空原文件（不放心可以先备份原文件再执行代码,不然数据会丢失）
            with open(self.file_path,mode="w") as fd:
                fd.write("") #不写任何东西代表清空

            #[2] 再逐一把user_list中的数据写入到文件."a"代表追加写入
            with open(self.file_path,mode = "a") as fd:
                for item in self.user_list:
                    fd.write(",".join(item)) #通过.join()方法指定写入时按照什么进行分割写入文件。这里指定的是按照逗号分割写入
        except:
            showinfo("系统信息","写入数据失败.")

#     def upload_main(self):
#         """
#         加载主窗体函数: 1. 用户验证通过后自动关闭当前窗体
#                        2. 用户验证通过后自动加载主窗体
#         :return:
#         """
#         #关闭当前窗体
#         self.destroy()

#         #加载主窗体
#         self.main_window = man.Main_Windows(self.current_login_list,self.get_login_time())
#         #man.Main_Windows()中self.current_login_list及self.get_login_time()为加载登录主窗体后实现当前用户及登录时间显示的功能

    def get_login_time(self):
        """
        实现用户登录后自动加载登录时间功能
            #通过import datetime这个模块中datetime.today()方法来实现.
        :return:
        """
        today = datetime.today()
        return ("%04d/%02d/%02d %02d:%02d:%02d" % (
        today.year, today.month, today.day, today.hour, today.minute, today.second))


if __name__ == "__main__":
    this_login = Login_Windows()
    this_login.mainloop()

