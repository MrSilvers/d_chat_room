//document.querySelector('.chat[data-chat=admin]').classList.add('active-chat');
//document.querySelector('.person[data-chat=admin]').classList.add('active');
$("div.chat:first").addClass('active-chat');
$("li.person:first").addClass('active');
$("#receiver").text($("li.person:first").attr("data-chat"));

var friends = {
  list: document.querySelector('ul.people'),
  all: document.querySelectorAll('.left .person'),
  name: '' },

chat = {
  container: document.querySelector('.container .right'),
  current: null,
  person: null,
  name: document.querySelector('.container .right .top .name') };


friends.all.forEach(function (f) {
  f.addEventListener('mousedown', function () {
    f.classList.contains('active') || setAciveChat(f);
  });
});

function setAciveChat(f) {
  friends.list.querySelector('.active').classList.remove('active');
  f.classList.add('active');
  chat.current = chat.container.querySelector('.active-chat');
  chat.person = f.getAttribute('data-chat');
  chat.current.classList.remove('active-chat');
  chat.container.querySelector('[data-chat="' + chat.person + '"]').classList.add('active-chat');
  friends.name = f.querySelector('.name').innerText;
  chat.name.innerHTML = friends.name;
}

var chatSocket = new WebSocket('ws://127.0.0.1:8000/chat/chat');
var user_id = $("#user_id").val();
chatSocket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  var from = data['user_id'];
  console.log(data);
  var message = '<li><div class="bubble you">' + data['message'] + '</div></li>';
  if($("#"+from+"_records").length>0){
    $("#"+from+"_records").append(message);
  }else{
    var new_temp_chat = "<div class=\"chat\" data-chat=" + from + " id=" + from + ">" +
        "<ul id="+ from + "_records style=\"height:458px;overflow-x: hidden;overflow-y:auto\"></ul></div>";
    $("div.write").before(new_temp_chat);
    var new_temp_friend = "<li class=\"person\" data-chat="+from+">" +
        "<img src=\"img/thomas.jpg\" alt=\"\" />" +
        "<span class=\"name\">"+from+"</span>" +
        "<span class=\"time\">now</span>" +
        "<span class=\"preview\"></span>" +
        "</li>";
    $("#"+from+"_records").append(message);
    $("ul.people").append(new_temp_friend);
    $("div.chat:first").addClass('active-chat');
    $("li.person:first").addClass('active');
    $("#receiver").text($("li.person:first").attr("data-chat"));
  }
};

chatSocket.onopen = function () {
  // Web Socket 已连接上，使用 send() 方法发送数据
  init_message = {"user_id":user_id,"message":"connected","receiver":user_id};
  chatSocket.send(JSON.stringify(init_message));
  console.log("init: send message")
};
chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

function send_message(){
  var message = $("#message_input").val();
  var receiver = $("#receiver").text();
  //var receiver = friends.name;
  console.log(message);
  data = {
      'message': message,
      'receiver': receiver,
      'user_id': user_id
  };
  chatSocket.send(JSON.stringify(data));
  var message = data["user_id"] + " : " + data["message"];
  //document.querySelector('#chat-log').value += (message + '\n');
  var chat_log = $("#chat-log").val();
  console.log(message)
  // $("#chat-log").text(chat_log + "\n" + message);
  var message = '<li><div class="bubble me">' + data['message'] + '</div></li>';
  $("#"+receiver+"_records").append(message);
}

function logout() {
  chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
  };
  location.href="../auth/logout";
}