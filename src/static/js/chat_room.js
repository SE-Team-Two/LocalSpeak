$(document).ready(function () {
   var socket = io.connect('http://' + document.domain + ":" + location.port);
   
   $("#submit_post_btn").click(function () {
      chat = document.getElementById("msg_list");
      msg = document.createElement('p');
      msg.innerHTML = document.getElementById("post").value;
      chat.appendChild(msg);
      msg.style = "text-align:right;";
      socket.send(document.getElementById("post").value);
      document.getElementById("post").value = "";
   });

   socket.on('connect', function() {
      navigator.geolocation.getCurrentPosition(function(position) { 
         socket.emit('location', {
            'lat' : position.coords.latitude,
            'lon' : position.coords.longitude,
            'radius' : 1000 
         });
      });
   });

   socket.on('message', function(msg) {
      chat = document.getElementById("msg_list");
      displayedMessage = document.createElement('p');
      displayedMessage.innerHTML= msg;
      chat.appendChild(displayedMessage);
   });
});
