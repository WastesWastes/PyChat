"""
服务器主程序
第一先实现信息的发送，接收
多线程的第一步

对于每个客户新建socket对象单独链接tcp
如果有用户链接，应显示用户上线
用户储存的格式应为{client_address:{"socket":client_socket,"user":"name"}}
有线程进行接听，接听完信息信息格式应为{“user_from”:"user1","user_to":"user2","content":"text"}
链接的第一次会发送一次用户信息{“user_from”:"user1","user_to":"none","content":"__first__"}
接听完进行将信息发送给目标用户，

"""

import socket
import threading
import time
import json
from class_server import Server
from queue import Queue

if __name__ == "__main__":
    round_client = 0
    #新建用户储存
    user_dict = {}
    data_stream = Queue()
    #新建服务器
    local_server = Server()

    while True:
        #监听端口
        print('等待用户连接......')
        client_socket, client_address = local_server.server.accept()
        round_client += 1
        print(f"{client_address}:连接成功[{round_client}]")
        #创建用户
        user_dict[client_address] = {"socket":client_socket, "user":"user"}
        #创建接收线程
        client_thread = threading.Thread(target=local_server.receive,
                                         args=(client_socket, client_address,user_dict,data_stream),
                                         daemon=True)
        client_thread.start()
        #创建发送线程
        time.sleep(0.3)#线程间时间间隔
        send_thread = threading.Thread(target=local_server.send,
                                       args=(user_dict,data_stream),
                                       daemon= True)
        send_thread.start()
        time.sleep(0.3)#线程间时间间隔











