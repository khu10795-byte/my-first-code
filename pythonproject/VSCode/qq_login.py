import tkinter as tk
from tkinter import ttk
import os

class QQLoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("QQ登录")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        
        # 设置背景色
        self.root.configure(bg="#f0f0f0")
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg="#ffffff", width=360, height=400)
        self.main_frame.place(x=20, y=25)
        
        # 添加QQ标志
        self.add_qq_logo()
        
        # 添加账号密码输入框
        self.add_account_input()
        
        # 添加登录按钮
        self.add_login_button()
        
        # 添加其他选项
        self.add_options()
    
    def add_qq_logo(self):
        # QQ标志文字
        logo_label = tk.Label(self.main_frame, text="QQ", font=("Arial", 36, "bold"), fg="#1296db", bg="#ffffff")
        logo_label.place(x=150, y=40)
        
        # 登录提示
        login_label = tk.Label(self.main_frame, text="账号密码登录", font=("Arial", 14), fg="#333333", bg="#ffffff")
        login_label.place(x=120, y=100)
    
    def add_account_input(self):
        # 账号输入框
        account_frame = tk.Frame(self.main_frame, bg="#ffffff", width=280, height=40, relief="groove", bd=1)
        account_frame.place(x=40, y=140)
        
        account_icon = tk.Label(account_frame, text="Q", font=("Arial", 16), fg="#1296db", bg="#ffffff")
        account_icon.place(x=10, y=8)
        
        self.account_var = tk.StringVar()
        account_entry = tk.Entry(account_frame, textvariable=self.account_var, font=("Arial", 14), bd=0, bg="#ffffff")
        account_entry.place(x=40, y=8, width=230)
        
        # 密码输入框
        password_frame = tk.Frame(self.main_frame, bg="#ffffff", width=280, height=40, relief="groove", bd=1)
        password_frame.place(x=40, y=200)
        
        password_icon = tk.Label(password_frame, text="🔒", font=("Arial", 16), fg="#1296db", bg="#ffffff")
        password_icon.place(x=10, y=8)
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, textvariable=self.password_var, font=("Arial", 14), bd=0, bg="#ffffff", show="*")
        password_entry.place(x=40, y=8, width=230)
    
    def add_login_button(self):
        login_button = tk.Button(self.main_frame, text="登录", font=("Arial", 14, "bold"), 
                               bg="#1296db", fg="#ffffff", bd=0, width=28, height=2,
                               command=self.login)
        login_button.place(x=40, y=260)
    
    def add_options(self):
        # 记住密码和自动登录选项
        remember_var = tk.IntVar()
        auto_login_var = tk.IntVar()
        
        remember_check = tk.Checkbutton(self.main_frame, text="记住密码", variable=remember_var, 
                                       bg="#ffffff", font=("Arial", 12), fg="#666666")
        remember_check.place(x=40, y=320)
        
        auto_login_check = tk.Checkbutton(self.main_frame, text="自动登录", variable=auto_login_var, 
                                         bg="#ffffff", font=("Arial", 12), fg="#666666")
        auto_login_check.place(x=150, y=320)
        
        # 注册账号和找回密码链接
        register_link = tk.Label(self.main_frame, text="注册账号", font=("Arial", 12), 
                               fg="#1296db", bg="#ffffff", cursor="hand2")
        register_link.place(x=40, y=360)
        register_link.bind("<Button-1>", self.register)
        
        forgot_link = tk.Label(self.main_frame, text="找回密码", font=("Arial", 12), 
                              fg="#1296db", bg="#ffffff", cursor="hand2")
        forgot_link.place(x=240, y=360)
        forgot_link.bind("<Button-1>", self.forgot_password)
    
    def login(self):
        account = self.account_var.get()
        password = self.password_var.get()
        print(f"登录账号: {account}, 密码: {password}")
        # 这里可以添加实际的登录逻辑
    
    def register(self, event):
        print("注册账号")
        # 这里可以添加注册账号的逻辑
    
    def forgot_password(self, event):
        print("找回密码")
        # 这里可以添加找回密码的逻辑

if __name__ == "__main__":
    root = tk.Tk()
    app = QQLoginWindow(root)
    root.mainloop()