#coding:utf-8
from django.shortcuts import render,HttpResponse
from dwebsocket.decorators import accept_websocket
import time
import json
from user_mgmt.views import login_required
from .models import *

# Create your views here.
send_flag = 0
request_list = []
user_id_list = []

@accept_websocket
@login_required
def chat(request):
    if request.is_websocket:
        if request.session.get('user_id') in user_id_list:
            pass
        else:
            request_list.append(request)
        while True:
            time.sleep(1)
            try:
                data = request.websocket.wait()  # 接受前端发送来的数据
                if data:
                    print(data)
                    if data != '886':
                        receive_data = data
                        if receive_data:
                            for item in request_list:
                                item.websocket.send(receive_data)  # 发送给前端的数据
                    else:
                        message = {"user_id":"root","message":"connect close."}
                        request.websocket.send(json.dumps(message))
                        request.websocket.close()
                        # remove current in user_id_list and requests_list

            except Exception as e:
                request.websocket.close()
                print('socket请求关闭！！！')

@login_required
def chat_panel(request):
    if request.method == "GET":
        return render(request, "d_chat/index.html")
    elif request.method == "POST":
        username = request.session['user_id']
        receiver = request.POST.get('receiver')




