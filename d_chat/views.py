#coding:utf-8
from django.shortcuts import render,HttpResponse
from dwebsocket.decorators import accept_websocket
import time
import json
from user_mgmt.views import login_required
from .models import *

# Create your views here.
send_flag = 0

@accept_websocket
def chat(request):
    if request.is_websocket:
        # while True:
        #     time.sleep(5)
        #     if send_flag == 1:
        #         message = ChatRecordTbl.objects.filter()
        #     request.websocket.send(json.dumps({'info':'server info:hhhhh...'}))
        try:
            while True:
                message = request.websocket.wait()  # 接受前段发送来的数据
                if message:
                    message = bytes.decode(message)
                    if message != '886':
                        try:
                            receive_data = message
                            if receive_data:
                                request.websocket.send(receive_data.encode())  # 发送给前段的数据
                                time.sleep(1)

                        except Exception as e:
                            request.websocket.close()
                            return
                    else:
                        print('socket请求关闭！！！')
                        request.websocket.close()
                        return
        except Exception as e:
            try:
                request.websocket.close()
                return
            except:
                return

@login_required
def chat_panel(request):
    if request.method == "GET":
        return render(request, "d_chat/index.html")
    elif request.method == "POST":
        username = request.session['user_id']
        receiver = request.POST.get('receiver')




