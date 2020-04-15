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
request_dict = {}

@accept_websocket
@login_required
def chat(request):
    user_id = request.session.get("user_id")
    print(user_id)
    if request.is_websocket:
        if not request_dict.get(user_id):
            request_dict[user_id] = request
        print(request_dict,request_dict.values())
        while True:
            time.sleep(1)
            try:
                data = request.websocket.wait()  # 接受前端发送来的数据
                if data:
                    print(data)
                    data = json.loads(str(data, encoding = "utf-8"))
                    print(data)
                    receiver = data.get("receiver")
                    if receiver == "public":
                        print(1111111111)
                        receiver_list = request_dict.values()
                        print(receiver_list)
                    else:
                        receiver_list = [request_dict.get(receiver)]
                    if data.get("message") == "886":
                        data = {"user_id": user_id, "message": "connect closed."}
                        receiver_list = request_dict.values()
                        send_message(data, receiver_list)
                        request.websocket.close()
                        # remove current request in request_dict
                        request_dict.pop(user_id)
                    else:
                        print(22222)
                        send_message(data,receiver_list)

            except Exception as e:
                print(e)
                request.websocket.close()
                print('socket请求关闭！！！')

@login_required
def chat_panel(request):
    if request.method == "GET":
        return render(request, "d_chat/index.html")
    elif request.method == "POST":
        username = request.session['user_id']
        receiver = request.POST.get('receiver')

def send_message(data,send_to_list):
    for item in send_to_list:
        item.websocket.send(json.dumps(data))  # 发送给前端的数据




