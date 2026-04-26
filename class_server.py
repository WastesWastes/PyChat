"""
服务器的基本功能class
应包含信息的发送，接收
"""
import socket
import json
from queue import Queue

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', 8000))
        self.server.listen(5)

    """
    定义接收端，循环接收，接收的信息为bytes，
    理应解码，用json转化为字典对象
    """
    @staticmethod
    def receive(client_socket,client_address ,user_dict,data_stream):
        print('开始接收数据')
        while True:
            try:
                client_message = client_socket.recv(1024)
                if not client_message:
                    print('用户已下线')
                    del user_dict[client_address]
                    client_socket.close()
                    break
                client_message_dict = json.loads(client_message.decode('utf-8'))

                print(client_message_dict)
                print(client_message_dict["content"])
                #判断第一次信息传输
                #链接的第一次会发送一次用户信息{“user_from”:"user1","user_to":"none","content":"__first__"}
                if client_message_dict["content"] == "__first__":
                    print(f'{client_address}{client_message_dict["user_from"]}已上线')

                    #存入用户的名字
                    if user_dict[client_address]["user"] != client_message_dict["user_from"]:
                        user_dict[client_address]["user"] = client_message_dict["user_from"]
                    print("存入用户名成功")
                #否则将信息穿给内存流
                else:
                    #用户储存的格式应为{client_address:{"socket":client_socket,"user":"name"}}
                    #遍历用户字典查找目标用户
                    for value in user_dict.values():
                        if value["user"] == client_message_dict["user_to"]:
                            # 将信息放入内存流
                            data_stream.put(client_message)
                            print("信息已存入内存流")
                            break
                    else:
                        print(f'目标{client_message_dict["user_to"]}已下线')
            except ConnectionResetError as e:
                print('用户已下线')
                print(e)
                break
            except client_socket.timeout:
                print('用户已下线')
                del user_dict[client_address]
                client_socket.close()
                break
        client_socket.close()

    """
    定义发送端，循环发送，发送的信息为bytes，
    理应编码，将json转化为bytes对象
    """
    @staticmethod
    def send(user_dict,data_stream):
        print('开始发送数据')
        while True:
            # 从内存流中取出信息
            sent_message = data_stream.get()
            print("已读出内存信息")
            #将要发送信息转json为字典对象
            sent_message_dict = json.loads(sent_message.decode('utf-8'))
            for value in user_dict.values():
                if value["user"] == sent_message_dict["user_to"]:
                    print(f'{value["user"]}已找到')
                    #将信息发送给目标用户
                    try:
                        value["socket"].send(sent_message)
                        print("已发送")
                    except Exception as e:
                        print(e)
                        print("发送失败")
                    break
            else:
                print(f'{sent_message_dict["user_to"]}目标已下线')










