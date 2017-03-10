#!/usr/bin/python
# -*- coding: utf-8 -*-
from channels.generic.websockets import WebsocketConsumer
from channels.generic import BaseConsumer
from channels.sessions import channel_session
import json
import time
from workflow.controllers import task_log

#message.reply_channel    一个客户端通道的对象
#message.reply_channel.send(chunk)  用来唯一返回这个客户端

#一个管道大概会持续30s
#当连接上时，发回去一个connect字符串
@channel_session
def ws_connect(message):
    message.reply_channel.send({'text': json.dumps({"accept": True, "data": "Successfully"})})


#将发来的信息原样返回
@channel_session
def ws_message(message):
    print message
    # text = json.loads(message.content['text'])
    # method_name = eval(text['invoke_method'])
    # dict = json.dumps(method_name(text))
    # message.reply_channel.send({'text': dict})
    message.reply_channel.send({'text': 'send message'})


#断开连接时发送一个disconnect字符串，当然，他已经收不到了
def ws_disconnect(message):
    message.reply_channel.send({"disconnect": 'disconnect'})


class DeployStatus(WebsocketConsumer):
    def connect(self, message, **kwargs):
        print "connect"
        self.message.reply_channel.send({'text': json.dumps({"accept": True, "connect": "Successfully"})})

    def receive(self, text=None, bytes=None, **kwargs):
        data = json.loads(text)
        content = task_log.ws_get_deploy_result(data['tid'], data['task_log_id'])
        self.send(text=content, bytes=bytes)

    def disconnect(self, message, **kwargs):
        pass



        # class Terminal(WebsocketConsumer):
#     def connect(self, message, **kwargs):
#         print "connect"
#         url = message.content['path']
#         host_ip, username, password, port = url.split('/')[2:]
#         try:
#             Terminal.client = MySSH(username, password, host_ip, port)
#         except Exception, e:
#             print e
#             return
#
#         try:
#             while True:
#                 data = Terminal.client.chan.recv(1024)
#                 # data = Terminal.client.chan.recv(Terminal.client.bufsize)
#                 if not len(data):
#                     return
#                 message.reply_channel.send({'text': json.dumps({"data": data})})
#         finally:
#             Terminal.client.ssh.close()
#
#
#     def receive(self, text=None, bytes=None, **kwargs):
#         try:
#             Terminal.client.chan.send(json.loads(text)['data'])
#         except Exception, e:
#             print e
#             print text
#             self.send(text=json.loads(text)['data'], bytes=bytes)
#         # self.send(text=json.loads(text)['data'], bytes=bytes)
#
#
#     def disconnect(self, message, **kwargs):
#         pass
#
# class MyConsumer(BaseConsumer):
#
#     method_mapping = {
#         "channel.name.here": "method_name",
#     }
#
#     def method_name(self, message, **kwargs):
#         print "test method_name"
#         pass