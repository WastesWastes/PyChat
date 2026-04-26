"""
此为客户端的主进程
应有主线程，进行发送，和第二个接收线程
第一次连接时应该发送身份信息
{“user_from”:"user1",
"user_to":"none",
"content":"__first__"}
应该使用一个变量保存对话
面对不同的人应该有独立的历史记录，使用json保存
理应保存格式为
[{“role”:"user_from","content":"text"
{"role":"user","content":"text"}]
"""
import socket
import threading
from queue import Queue
import time
from class_client import Client
import json

if __name__ == "__main__":
    print("""=================================
    
    欢迎来到v0.01聊天服务器
    
=================================""")
    user = str(input("请输入用户名："))
    #新建客户端对象
    client = Client (user)
    data = []

    #发送身份信息
    client.send("__first__")
    #启动接收线程
    receive_thread = threading.Thread(target=client.receive,daemon= True,args=(data,))
    receive_thread.start()
    time.sleep(0.3)#线程间时间间隔
    #设置接收者
    client.user_to = str(input("请输入接收用户名："))
    #发送循环
    while True:
        message = str(input("输入信息："))
        #加入指令
        if message[0] == "/":
            match message:
                case "/help":
                    print("/help    帮助"
                          "/exit    退出"
                          "/history 历史"
                          "/save    保存")
                case "/exit":
                    print("退出")
                    client.client.close()
                    exit()
                case "/history":
                    print(data)
                case "/save":
                    with open("history.json","w",encoding="utf-8") as f:
                        json.dump(data,f,ensure_ascii= False,indent=4)
                case _:
                    print("未知指令")
            pass
        else:
            client.send(message)
            #添加数据
            data.append({"role":client.user,"content":message})


