import tkinter as tk
import random
import time

class FruitSlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("水果老虎机")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # 水果列表
        self.fruits = ["🍎", "🍌", "🍒", "🍇", "🍉", "🍓"]
        
        # 得分
        self.score = 0
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg="#ffffff", width=450, height=350)
        self.main_frame.place(x=25, y=25)
        
        # 添加标题
        self.add_title()
        
        # 添加滚轮区域
        self.add_reels()
        
        # 添加得分显示
        self.add_score_display()
        
        # 添加开始按钮
        self.add_start_button()
    
    def add_title(self):
        title_label = tk.Label(self.main_frame, text="水果老虎机", font=("Arial", 24, "bold"), fg="#ff6600", bg="#ffffff")
        title_label.place(x=150, y=20)
    
    def add_reels(self):
        # 滚轮框架
        self.reels_frame = tk.Frame(self.main_frame, bg="#ffffff", width=400, height=150)
        self.reels_frame.place(x=25, y=80)
        
        # 三个滚轮
        self.reel1 = tk.Label(self.reels_frame, text="🍎", font=("Arial", 48), bg="#ffffff", width=3, height=2, relief="groove")
        self.reel1.place(x=50, y=20)
        
        self.reel2 = tk.Label(self.reels_frame, text="🍌", font=("Arial", 48), bg="#ffffff", width=3, height=2, relief="groove")
        self.reel2.place(x=175, y=20)
        
        self.reel3 = tk.Label(self.reels_frame, text="🍒", font=("Arial", 48), bg="#ffffff", width=3, height=2, relief="groove")
        self.reel3.place(x=300, y=20)
    
    def add_score_display(self):
        score_frame = tk.Frame(self.main_frame, bg="#ffffff", width=400, height=50)
        score_frame.place(x=25, y=250)
        
        score_label = tk.Label(score_frame, text="得分:", font=("Arial", 16), bg="#ffffff")
        score_label.place(x=50, y=10)
        
        self.score_var = tk.StringVar()
        self.score_var.set(f"{self.score}")
        score_value = tk.Label(score_frame, textvariable=self.score_var, font=("Arial", 16, "bold"), fg="#ff6600", bg="#ffffff")
        score_value.place(x=120, y=10)
    
    def add_start_button(self):
        start_button = tk.Button(self.main_frame, text="开始游戏", font=("Arial", 16, "bold"), 
                               bg="#ff6600", fg="#ffffff", bd=0, width=15, height=2,
                               command=self.start_game)
        start_button.place(x=150, y=300)
    
    def start_game(self):
        # 模拟滚轮转动动画
        for _ in range(10):
            # 随机更新每个滚轮的水果
            self.reel1.config(text=random.choice(self.fruits))
            self.reel2.config(text=random.choice(self.fruits))
            self.reel3.config(text=random.choice(self.fruits))
            # 更新界面
            self.root.update()
            # 暂停一段时间
            time.sleep(0.1)
        
        # 最终结果
        result1 = random.choice(self.fruits)
        result2 = random.choice(self.fruits)
        result3 = random.choice(self.fruits)
        
        # 更新滚轮显示最终结果
        self.reel1.config(text=result1)
        self.reel2.config(text=result2)
        self.reel3.config(text=result3)
        
        # 判断中奖情况
        self.check_win(result1, result2, result3)
    
    def check_win(self, r1, r2, r3):
        # 三个相同
        if r1 == r2 == r3:
            self.score += 100
            self.show_message("恭喜中奖！获得100分！")
        # 两个相同
        elif r1 == r2 or r1 == r3 or r2 == r3:
            self.score += 10
            self.show_message("小奖！获得10分！")
        else:
            self.show_message("未中奖，再接再厉！")
        
        # 更新得分显示
        self.score_var.set(f"{self.score}")
    
    def show_message(self, message):
        # 创建消息窗口
        msg_window = tk.Toplevel(self.root)
        msg_window.title("游戏结果")
        msg_window.geometry("300x150")
        msg_window.resizable(False, False)
        
        msg_label = tk.Label(msg_window, text=message, font=("Arial", 14), pady=30)
        msg_label.pack()
        
        ok_button = tk.Button(msg_window, text="确定", font=("Arial", 12), width=10, 
                             command=msg_window.destroy)
        ok_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = FruitSlotMachine(root)
    root.mainloop()
import tkinter as tk
import random
import time
import socket
import threading
import socket
import threading
import socket
import threading

class FruitSlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("水果老虎机")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # 水果列表
        self.fruits = ["🍎", "🍌", "🍒", "🍇", "🍉", "🍓"]
        
        # 得分
        self.score = 0
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg="#ffffff", width=450, height=350)
        self.main_frame.place(x=25, y=25)
        
        # 添加标题
        self.add_title()
        
        # 添加滚轮区域
        self.add_reels()
        
        # 添加得分显示
        self.add_score_display()
        
        # 添加开始按钮
        self.add_start_button()
        
        # 启动网络服务器
        self.start_server()
        
        # 启动网络服务器
        self.start_server()
        
        # 启动网络服务器
        self.start_server()
    
    def add_title(self):
        title_label = tk.Label(self.main_frame, text="水果老虎机", font=("Arial", 24, "bold"), fg="#ff6600", bg="#ffffff")
        title_label.place(x=150, y=20)
    
    def add_reels(self):
        # 滚轮框架
        self.reels_frame = tk.Frame(self.main_frame, bg="#ffffff", width=400, height=150)
        self.reels_frame.place(x=25, y=80)
        
        # 三个滚轮
        self.reel1 = tk.Label(self.reels_frame, text="🍎", font=("Arial", 48), bg="#ffffff", width=3, height=2, relief="groove")
        self.reel1.place(x=50, y=20)
        
        self.reel2 = tk.Label(self.reels_frame, text="🍌", font=("Arial", 48), bg="#ffffff", width=3, height=2, relief="groove")
        self.reel2.place(x=175, y=20)
        
        self.reel3 = tk.Label(self.reels_frame, text="🍒", font=("Arial", 48), bg="#ffffff", width=3, height=2, relief="groove")
        self.reel3.place(x=300, y=20)
    
    def add_score_display(self):
        score_frame = tk.Frame(self.main_frame, bg="#ffffff", width=400, height=50)
        score_frame.place(x=25, y=250)
        
        score_label = tk.Label(score_frame, text="得分:", font=("Arial", 16), bg="#ffffff")
        score_label.place(x=50, y=10)
        
        self.score_var = tk.StringVar()
        self.score_var.set(f"{self.score}")
        score_value = tk.Label(score_frame, textvariable=self.score_var, font=("Arial", 16, "bold"), fg="#ff6600", bg="#ffffff")
        score_value.place(x=120, y=10)
    
    def add_start_button(self):
        start_button = tk.Button(self.main_frame, text="开始游戏", font=("Arial", 16, "bold"), 
                               bg="#ff6600", fg="#ffffff", bd=0, width=15, height=2,
                               command=self.start_game)
        start_button.place(x=150, y=300)
    
    def start_game(self):
        # 模拟滚轮转动动画
        for _ in range(10):
            # 随机更新每个滚轮的水果
            self.reel1.config(text=random.choice(self.fruits))
            self.reel2.config(text=random.choice(self.fruits))
            self.reel3.config(text=random.choice(self.fruits))
            # 更新界面
            self.root.update()
            # 暂停一段时间
            time.sleep(0.1)
        
        # 最终结果
        result1 = random.choice(self.fruits)
        result2 = random.choice(self.fruits)
        result3 = random.choice(self.fruits)
        
        # 更新滚轮显示最终结果
        self.reel1.config(text=result1)
        self.reel2.config(text=result2)
        self.reel3.config(text=result3)
        
        # 判断中奖情况
        self.check_win(result1, result2, result3)
    
    def check_win(self, r1, r2, r3):
        # 三个相同
        if r1 == r2 == r3:
            self.score += 100
            self.show_message("恭喜中奖！获得100分！")
        # 两个相同
        elif r1 == r2 or r1 == r3 or r2 == r3:
            self.score += 10
            self.show_message("小奖！获得10分！")
        else:
            self.show_message("未中奖，再接再厉！")
        
        # 更新得分显示
        self.score_var.set(f"{self.score}")
    
    def show_message(self, message):
        # 创建消息窗口
        msg_window = tk.Toplevel(self.root)
        msg_window.title("游戏结果")
        msg_window.geometry("300x150")
        msg_window.resizable(False, False)
        
        msg_label = tk.Label(msg_window, text=message, font=("Arial", 14), pady=30)
        msg_label.pack()
        
        ok_button = tk.Button(msg_window, text="确定", font=("Arial", 12), width=10, 
                             command=msg_window.destroy)
        ok_button.pack()
    
    def start_server(self):
        # 创建服务器套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 8888))
        self.server_socket.listen(5)
        
        # 启动服务器线程
        server_thread = threading.Thread(target=self.server_listen, daemon=True)
        server_thread.start()
        
        # 显示服务器状态
        self.server_label = tk.Label(self.main_frame, text="服务器已启动: localhost:8888", 
                                   font=("Arial", 10), fg="#009900", bg="#ffffff")
        self.server_label.place(x=150, y=5)
    
    def server_listen(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"客户端连接: {addr}")
                # 处理客户端请求
                client_thread = threading.Thread(target=self.handle_client, 
                                              args=(client_socket,), daemon=True)
                client_thread.start()
            except Exception as e:
                print(f"服务器错误: {e}")
                break
    
    def handle_client(self, client_socket):
        while True:
            try:
                # 接收客户端指令
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"收到指令: {data}")
                
                # 处理指令
                if data == "start":
                    # 在主线程中执行游戏开始
                    self.root.after(0, self.start_game)
                    client_socket.send("游戏已开始".encode('utf-8'))
                elif data == "reset":
                    # 重置得分
                    self.score = 0
                    self.score_var.set(f"{self.score}")
                    client_socket.send("得分已重置".encode('utf-8'))
                elif data == "score":
                    # 返回当前得分
                    client_socket.send(f"当前得分: {self.score}".encode('utf-8'))
                else:
                    client_socket.send("未知指令".encode('utf-8'))
            except Exception as e:
                print(f"客户端处理错误: {e}")
                break
        client_socket.close()
    
    def start_server(self):
        # 创建服务器套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 8888))
        self.server_socket.listen(5)
        
        # 启动服务器线程
        server_thread = threading.Thread(target=self.server_listen, daemon=True)
        server_thread.start()
        
        # 显示服务器状态
        self.server_label = tk.Label(self.main_frame, text="服务器已启动: localhost:8888", 
                                   font=("Arial", 10), fg="#009900", bg="#ffffff")
        self.server_label.place(x=150, y=5)
    
    def server_listen(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"客户端连接: {addr}")
                # 处理客户端请求
                client_thread = threading.Thread(target=self.handle_client, 
                                              args=(client_socket,), daemon=True)
                client_thread.start()
            except Exception as e:
                print(f"服务器错误: {e}")
                break
    
    def handle_client(self, client_socket):
        while True:
            try:
                # 接收客户端指令
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"收到指令: {data}")
                
                # 处理指令
                if data == "start":
                    # 在主线程中执行游戏开始
                    self.root.after(0, self.start_game)
                    client_socket.send("游戏已开始".encode('utf-8'))
                elif data == "reset":
                    # 重置得分
                    self.score = 0
                    self.score_var.set(f"{self.score}")
                    client_socket.send("得分已重置".encode('utf-8'))
                elif data == "score":
                    # 返回当前得分
                    client_socket.send(f"当前得分: {self.score}".encode('utf-8'))
                else:
                    client_socket.send("未知指令".encode('utf-8'))
            except Exception as e:
                print(f"客户端处理错误: {e}")
                break
        client_socket.close()
    
    def start_server(self):
        # 创建服务器套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 8888))
        self.server_socket.listen(5)
        
        # 启动服务器线程
        server_thread = threading.Thread(target=self.server_listen, daemon=True)
        server_thread.start()
        
        # 显示服务器状态
        self.server_label = tk.Label(self.main_frame, text="服务器已启动: localhost:8888", 
                                   font=("Arial", 10), fg="#009900", bg="#ffffff")
        self.server_label.place(x=150, y=5)
    
    def server_listen(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"客户端连接: {addr}")
                # 处理客户端请求
                client_thread = threading.Thread(target=self.handle_client, 
                                              args=(client_socket,), daemon=True)
                client_thread.start()
            except Exception as e:
                print(f"服务器错误: {e}")
                break
    
    def handle_client(self, client_socket):
        while True:
            try:
                # 接收客户端指令
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"收到指令: {data}")
                
                # 处理指令
                if data == "start":
                    # 在主线程中执行游戏开始
                    self.root.after(0, self.start_game)
                    client_socket.send("游戏已开始".encode('utf-8'))
                elif data == "reset":
                    # 重置得分
                    self.score = 0
                    self.score_var.set(f"{self.score}")
                    client_socket.send("得分已重置".encode('utf-8'))
                elif data == "score":
                    # 返回当前得分
                    client_socket.send(f"当前得分: {self.score}".encode('utf-8'))
                else:
                    client_socket.send("未知指令".encode('utf-8'))
            except Exception as e:
                print(f"客户端处理错误: {e}")
                break
        client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FruitSlotMachine(root)
    root.mainloop()