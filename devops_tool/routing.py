#!/usr/bin/python
# -*- coding: utf-8 -*-
from channels.routing import route, route_class
from devops_tool import consumers  # 导入处理函数

channel_routing = [
    # route("http.request", consumers.http_consumer), 这个表项比较特殊，他响应的是http.request，也就是说有HTTP请求时就会响应，同时urls.py里面的表单会失效
    # route('my_test', consumers.my_test, path=r'^/my_test/'),
    # route("websocket.connect", consumers.terminal_conn, path=r'^/wssh'),
    # route("websocket.receive", consumers.terminal_msg, path=r'^/wssh'),
    # route_class(consumers.Terminal, path=r"^/wssh/"),
    # route("websocket.connect", consumers.ws_connect, path=r"^/aa/$"),  # 当WebSocket请求连接上时调用consumers.ws_connect函数
    # route("websocket.receive", consumers.ws_message, path=r"^/aa/$"),  # 当WebSocket请求发来消息时。。。
    # route("websocket.disconnect", consumers.ws_disconnect, path=r"^/aa/$"),  # 当WebSocket请求断开连接时。。。
    # route("websocket.connect", consumers.ws_connect, path=r"^/deploy_status$"),
    # route("websocket.receive", consumers.ws_message, path=r"^/deploy_status$"),
    # route("websocket.disconnect", consumers.ws_disconnect, path=r"^/deploy_status$")
    # route_class(consumers.DeployStatus, path=r"^/deploy_status$"),
    consumers.DeployStatus.as_route(path=r"^/deploy_status")
]
