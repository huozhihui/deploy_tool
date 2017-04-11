#!/usr/bin/python
# -*- coding: utf-8 -*-
from channels.generic.websockets import WebsocketConsumer
from channels.generic import BaseConsumer
from channels.sessions import channel_session
import json
import time
import datetime
from workflow.controllers import task_log
from common.redis_api import Rs


class DeployStatus(WebsocketConsumer):
    def connect(self, message, **kwargs):
        print "connect websocket successfully"
        self.message.reply_channel.send({'text': json.dumps({"accept": True, "connect": "Successfully"})})

    def receive(self, text=None, bytes=None, **kwargs):
        receive_data = json.loads(text)
        task_log_id = receive_data['task_log_id']
        ip = receive_data['ip']
        send_data = task_log.ws_get_deploy_result(self, task_log_id, ip)


        # redis_key_info = "{tid}-{ip}-info".format(tid=task_log_id, ip=ip)
        # while True:
        #     status = Rs.hget(redis_key_info, 'status')
        #     print status
        #     if int(status) < 2:
        #         send_data = task_log.ws_get_deploy_result(task_log_id, ip)
        #         self.send(text=json.dumps(send_data), bytes=bytes)
        #         time.sleep(3)
        #     else:
        #         # self.send(text=json.dumps(send_data), bytes=bytes)
        #         break


def disconnect(self, message, **kwargs):
    pass
