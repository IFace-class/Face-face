from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import *
import os

class change_User_password(Toplevel): # 这里要用Toplevel不能用Tk因为tkinter只支持一个主窗体存在.要想再跳出一个窗体必须选Toplevel
    def __init__(self,current_user_list):
        super().__init__()
        self.title("修改密码")
        self.geometry("600x500+300+100")  # 通过控制图像大小可以通过+号来调整窗体出现的位置
        self.resizable(0, 0)  # 固定窗体大小.不允许改动窗体大小. resizable(0,0)表示x轴为0y轴也为0
        #self.iconbitmap(R"C:\Users\Administrator\python_图库\china.ico")  # 加载.ico文件
        self["bg"] = "RoyalBlue"

        #定义全局变量
        self.current_user_list = current_user_list  #同样在change_User_password窗口中接收list的地址
        self.file_path = R"loginuser_info.txt"
        self.get_all_userlist = []  #获取所有的账号密码

        #加载setup_UI
        self.Setup_UI()

        #初始化
        self.var_loginuser.set(self.current_user_list[0]) #初始化登录的账号

        #自动加载
        self.get_all_loginuser()

    def Setup_UI(self):
        # 通过style设置属性
        self.Style01 = ttk.Style()
        self.Style01.configure("titel3.TLabel", font=("微软眼黑", 20, "bold"), foreground="darkred")
        self.Style01.configure("TPanedwindow", background="lightcyan")#RoyalBlue
        self.Style01.configure("TButton", font=("微软眼黑", 11), background="RoyalBlue", foreground="black")
        self.Style01.configure("TLabel",font=("微软眼黑", 14, "bold"), foreground="black",background="lightcyan")
        self.Style01.configure("TRadiobutton",font=("微软眼黑", 14, "bold"), foreground="black",background="lightcyan")

        #加载窗体图片
        self.login_img = PhotoImage(file = R"beijingtu.png")
        self.label_img = ttk.Label(self,image = self.login_img)
        self.label_img.pack()

        #添加Titile框体
        self.title_label = ttk.Label(self,text="== 更改密码 ==",style = "titel3.TLabel")
        self.title_label.place(x = 20,y = 30)

        #添加一个Panewindows
        self.pane = ttk.PanedWindow(self,width=596, height=360, style="TPanedwindow")
        self.pane.place(x=2,y=98)

        self.label_login_user = ttk.Label(self.pane,text = "登录账号",style="stu_number.TLabel")
        self.var_loginuser=StringVar()
        self.label_login_user.place(x=170, y=60)
        self.entry_login_user = ttk.Entry(self.pane,state = DISABLED,textvariable = self.var_loginuser,font=("微软眼黑",14, "bold"),width=16)
        self.entry_login_user.place(x=270, y=60)

        self.label_old_password = ttk.Label(self.pane,text = "旧密码",style="stu_number.TLabel")
        self.var_old_password=StringVar()
        self.label_old_password.place(x=170, y=120)
        self.entry_old_password = ttk.Entry(self.pane,show = "*",textvariable = self.var_old_password,font=("微软眼黑",14, "bold"),width=16)
        self.entry_old_password.place(x=270, y=120)

        self.label_new_password = ttk.Label(self.pane,text = "新密码",style="stu_number.TLabel")
        self.var_new_password=StringVar()
        self.label_new_password.place(x=170, y=180)
        self.entry_new_password = ttk.Entry(self.pane,show = "*",textvariable = self.var_new_password,font=("微软眼黑",14, "bold"),width=16)
        self.entry_new_password.place(x=270, y=180)

        self.label_reinput_password = ttk.Label(self.pane,text = "重新输入新密码",style="stu_number.TLabel")
        self.var_reinput_password=StringVar()
        self.label_reinput_password.place(x=120, y=240)
        self.entry_reinput_password = ttk.Entry(self.pane,show = "*",textvariable = self.var_reinput_password,font=("微软眼黑",14, "bold"),width=16)
        self.entry_reinput_password.place(x=270, y=240)

        #添加保存,关闭按钮
        self.save_buttion = ttk.Button(self, text="保存", width=10,command = self.save_pass_windows)
        self.save_buttion.place(x=380, y=470)
        self.exit_buttion = ttk.Button(self, text="退出", width=10,command = self.close_pass_windows)
        self.exit_buttion.place(x=480, y=470)

    def close_pass_windows(self):
        self.destroy()

    def save_pass_windows(self):
        # 获取登录账号相关的值
        old_password = self.var_old_password.get()
        new_password = self.var_new_password.get()
        second_password = self.var_reinput_password.get()

        #判断旧密码是否真确
        if old_password != self.current_user_list[1]:
            showinfo("系统消息","输入的旧密码不正确！")
            return
        #判断新密码跟旧密码是否相同

        if new_password == old_password:
            showinfo("系统消息", "新密码不能跟旧密码相同！")
            return

        #判断输入的新密码不能为空
        if len(new_password.strip()) == 0:
            showinfo("系统消息", "新密码不能为空！")
            return

        #两次密码输入是否相同
        if new_password != second_password:
            showinfo("系统消息", "两次密码输入不一致！")
            return

        #修改密码
        for index in range(len(self.get_all_userlist)):
            if self.get_all_userlist[index][0] == self.current_user_list[0]:
                self.get_all_userlist[index][1] = new_password

        # 完成更改(写入文件)
        try:
            with open(self.file_path,mode="w") as fd:
                fd.write("")
            with open(self.file_path,mode="a") as fd:
                for item in self.get_all_userlist:
                    temp = ",".join(item)
                    temp = temp.replace("\n","") + "\n"
                    fd.write(temp)

        except:
            showinfo("系统消息","写入文件出错.请联系管理员")

        #提示
        showinfo("系统消息", "密码修改成功！")

        #关闭窗口
        self.destroy()

    def get_all_loginuser(self):
        """
        读取文件获取所有的账号信息保存到get_all
        :return:
        """
        if not os.path.exists(self.file_path):
            showinfo("系统提示","文件不存在.请确认后重新加载!!")
        else:
            try:
                with open(self.file_path,mode = "r") as fd:
                    current_list = fd.readline() #一次读一行
                    while current_list:#表示直到current_list中所有元素被读完，循环结束
                        temp_list = current_list.split(",") #按照逗号把每个list中的元素分割出来
                        self.get_all_userlist.append(temp_list) #把分割后的每个元素重新添加到all_list列表中
                        current_list = fd.readline() #因为我们一次只读一行。读完后如果不加这一句那么循环会一直只读第一行。

            except:
                showinfo("系统信息","文件读取出现异常.请联系管理员！！")

if __name__ == "__main__":
    this_windows = change_User_password()
    this_windows.mainloop()


