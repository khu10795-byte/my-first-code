import tkinter as tk
import socket

class SlotMachineController:
    def __init__(self, root):
        self.root = root
        self.root.title("水果老虎机控制器")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # 服务器信息
        self.server_ip = "localhost"
        self.server_port = 8888
        self.client_socket = None
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg="#ffffff", width=360, height=260)
        self.main_frame.place(x=20, y=20)
        
        # 添加标题
        self.add_title()
        
        # 添加连接状态
        self.add_connection_status()
        
        # 添加控制按钮
        self.add_control_buttons()
        
        # 添加消息显示
        self.add_message_display()
        
        # 尝试连接服务器
        self.connect_to_server()
    
    def add_title(self):
        title_label = tk.Label(self.main_frame, text="水果老虎机控制器", font=("Arial", 18, "bold"), fg="#ff6600", bg="#ffffff")
        title_label.place(x=80, y=20)
    
    def add_connection_status(self):
        self.status_var = tk.StringVar()
        self.status_var.set("未连接")
        status_label = tk.Label(self.main_frame, text="连接状态:", font=("Arial", 12), bg="#ffffff")
        status_label.place(x=50, y=60)
        
        self.status_display = tk.Label(self.main_frame, textvariable=self.status_var, font=("Arial", 12, "bold"), 
                                     fg="#ff0000", bg="#ffffff")
        self.status_display.place(x=150, y=60)
        
        connect_button = tk.Button(self.main_frame, text="连接服务器", font=("Arial", 10), 
                                 bg="#1296db", fg="#ffffff", bd=0, width=10, 
                                 command=self.connect_to_server)
        connect_button.place(x=250, y=55)
    
    def add_control_buttons(self):
        # 开始游戏按钮
        start_button = tk.Button(self.main_frame, text="开始游戏", font=("Arial", 14), 
                               bg="#ff6600", fg="#ffffff", bd=0, width=15, height=2,
                               command=self.start_game)
        start_button.place(x=100, y=100)
        
        # 重置得分按钮
        reset_button = tk.Button(self.main_frame, text="重置得分", font=("Arial", 12), 
                               bg="#666666", fg="#ffffff", bd=0, width=10, 
                               command=self.reset_score)
        reset_button.place(x=80, y=180)
        
        # 查询得分按钮
        score_button = tk.Button(self.main_frame, text="查询得分", font=("Arial", 12), 
                               bg="#666666", fg="#ffffff", bd=0, width=10, 
                               command=self.get_score)
        score_button.place(x=200, y=180)
    
    def add_message_display(self):
        message_frame = tk.Frame(self.main_frame, bg="#f0f0f0", width=300, height=60, relief="groove", bd=1)
        message_frame.place(x=30, y=220)
        
        self.message_var = tk.StringVar()
        self.message_var.set("等待操作...")
        message_label = tk.Label(message_frame, textvariable=self.message_var, font=("Arial", 10), 
                               bg="#f0f0f0", wraplength=280)
        message_label.place(x=10, y=5)
    
    def connect_to_server(self):
        try:
            # 创建客户端套接字
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.status_var.set("已连接")
            self.status_display.config(fg="#009900")
            self.message_var.set("成功连接到水果老虎机服务器")
            print("成功连接到服务器")
        except Exception as e:
            self.status_var.set("连接失败")
            self.status_display.config(fg="#ff0000")
            self.message_var.set(f"连接失败: {str(e)}")
            print(f"连接失败: {e}")
    
    def send_command(self, command):
        if not self.client_socket:
            self.message_var.set("未连接到服务器")
            return
        
        try:
            self.client_socket.send(command.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            self.message_var.set(f"服务器响应: {response}")
            print(f"服务器响应: {response}")
        except Exception as e:
            self.message_var.set(f"发送指令失败: {str(e)}")
            print(f"发送指令失败: {e}")
    
    def start_game(self):
        self.send_command("start")
    
    def reset_score(self):
        self.send_command("reset")
    
    def get_score(self):
        self.send_command("score")

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineController(root)
    root.mainloop()