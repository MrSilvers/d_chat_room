#coding:utf-8
from django.shortcuts import render, HttpResponse, redirect
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
    print(user_id + ": request the server")
    if request.is_websocket:
        if not request_dict.get(user_id):
            request_dict[user_id] = request
        while True:
            time.sleep(1)
            try:
                data = request.websocket.wait()  # 接受前端发送来的数据
                if data:
                    data = json.loads(str(data, encoding = "utf-8"))
                    print(user_id + " send:" + json.dumps(data) + "to the server")
                    receiver = data.get("receiver")
                    if receiver == "public":
                        print("to public")
                        receiver_list = request_dict.values()
                        print(receiver_list)
                    else:
                        print("to " + receiver)
                        receiver_list = []
                        to = request_dict.get(receiver)
                        if to:
                            receiver_list.append(to)
                    if data.get("message") == "886":
                        # data = {"user_id": user_id, "message": "connect closed."}
                        # receiver_list = request_dict.values()
                        # send_message_and_save(data, receiver_list)
                        request.websocket.close()
                        # remove current request in request_dict
                        request_dict.pop(user_id)
                    else:
                        print(22222)
                        send_message_and_save(data,receiver_list)

            except Exception as e:
                print('error: socket请求关闭！！！')
                print(e)
                request_dict.pop(user_id)
                request.websocket.close()
                break

@login_required
def chat_panel(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        print(user_id)
        friend_obj_list = get_friend_obj_list(user_id)
        print("1111111111111111111111111111111111",friend_obj_list)
        user_recent_records = []
        if friend_obj_list:
            user_recent_records = get_user_recent_chat_records(user_id,friend_obj_list)
        context = {"friends":friend_obj_list,"user_recent_records":user_recent_records}
        return render(request,"d_chat/index.html",context)
        # return render(request, "d_chat/chat_panel.html")

    elif request.method == "POST":
        username = request.session['user_id']
        receiver = request.POST.get('receiver')

def send_message_and_save(data,send_to_list):
    is_read_flag = False
    if send_to_list:
        is_read_flag = True
        print("send_to_list:")
        print(send_to_list)
        for item in send_to_list:
            print("send data:")
            print(data)
            print(item.session.get("user_id"))
            item.websocket.send(json.dumps(data))  # 发送给前端的数据
    save_data(data,is_read_flag)

def get_friend_obj_list(user_id):
    user = UserTbl.objects.filter(username=user_id)
    if user.exists():
        friend_obj_list = UserFriendsTbl.objects.filter(user=user.first())
        if friend_obj_list.exists():
            return friend_obj_list
        else:
            return []
    else:
        return redirect("user_mgmt:auth_login")

def get_user_recent_chat_records(user_id,friend_obj_list):
    record = {"message":"","from_flag":True}
    temp_friend_list = []
    for friend in friend_obj_list:
        records = []
        temp_friend = {}
        print("22222222222222222",friend.friend)
        print("333333333333333333",user_id)
        chat_records = ChatRecordTbl.objects.filter(user__username=user_id)
        if chat_records.exists():
            chat_records = chat_records.first()
            chat_records_detail = ChatRecordDetailTbl.objects.filter(chat_record=chat_records).filter(peer_user=friend.friend).order_by("record_time")
            if chat_records_detail.exists():
                print("chat_records: ")
                print(chat_records_detail)
                records = [{"message":item.message,"from_flag":item.from_flag,"record_time":item.record_time} for item in chat_records_detail[:10]]
        temp_friend['records'] = records
        temp_friend['username'] = friend.friend.username
        temp_friend_list.append(temp_friend)
    print("44444444444444444",temp_friend_list)
    return temp_friend_list


def pack_user_and_record():
    pass

def save_data(data,is_read_flag):
    print("save data.........")
    username = data.get('user_id')
    receiver = data.get("receiver")
    message = data.get("message")
    receivers = GroupTbl.objects.filter(group_name=receiver)
    try:
        if receivers.exists():
            pass
        else:
            user_obj = UserTbl.objects.filter(username=username)
            peer_user_obj = UserTbl.objects.filter(username=receiver)
            if user_obj.exists() and peer_user_obj.exists():
                user_chat_obj,status = ChatRecordTbl.objects.get_or_create(user=user_obj.first())
                print("user_chat_obj_status: ",status,user_chat_obj)
                peer_user_chat_obj,status = ChatRecordTbl.objects.get_or_create(user=peer_user_obj.first())
                print("peer_user_chat_obj_status: ",status,peer_user_chat_obj)
                obj = ChatRecordDetailTbl(chat_record=user_chat_obj,peer_user=peer_user_obj.first())
                obj.message = message
                obj.is_read_flag = True
                obj.from_flag = True
                obj.save()
                obj = ChatRecordDetailTbl(chat_record=peer_user_chat_obj,peer_user=user_obj.first())
                obj.message = message
                obj.is_read_flag = is_read_flag
                obj.from_flag = False
                obj.save()
    except Exception as e:
        print(e)
