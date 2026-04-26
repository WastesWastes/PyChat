"""
客户端class
包含对socket定义
接收线程 接收的为二进制 应解码为json转化为字典对象
接听完信息信息格式应为{“user_from”:"user1","user_to":"user2","content":"text"}
发送方法
"""
import socket
import json


class Client:
    def __init__(self,user):
        self.user = user
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 8000))
        print('已连接服务器')
        self.user_to = "none"

    @staticmethod
    def text(user_from,user_to,content):
        """
        定义发送格式
        :param user_from: 发送者
        :param user_to: 接收者
        :param content: 内容
        :return:
        """
        return {"user_from":user_from,"user_to":user_to,"content":content}


    def receive(self,data):
        print('开始接收数据')
        while True:
            receive_message = self.client.recv(1024)
            if not receive_message:
                print('服务器断开')
                break
            # 将信息转化为字典对象
            receive_message_dict = json.loads(receive_message.decode('utf-8'))
            print(f'{receive_message_dict["user_from"]}:{receive_message_dict["content"]}')
            data.append({"role":receive_message_dict["user_from"],"content":receive_message_dict["content"]})
            print("已添加数据")
    def send(self,message):
        print('开始发送数据')
        send_message = self.text(self.user,self.user_to,message)
        self.client.send(json.dumps(send_message,ensure_ascii= False,indent=4).encode('utf-8'))
        print("已发送消息")










