$(document).ready(function () {
   var socket = io.connect('https://' + document.domain + ":" + location.port);
   
   function sendFromTextBox() {
      chat = document.getElementById("msg_list");
      msg = document.createElement('p');
      msg.innerHTML = document.getElementById("post").value;
      chat.appendChild(msg);
      msg.style = "text-align:right;";
      socket.send(document.getElementById("post").value);
      document.getElementById("post").value = "";
      chat.scrollTop = chat.scrollHeight;
   }

   $("#submit_post_btn").click(function () {
      sendFromTextBox();
   });

   $("#post").on('keydown', function(event) {
      if(event.key == "Enter") {
         event.preventDefault();

         sendFromTextBox();
      }
   });

   $("#send_location").click(function () {
      navigator.geolocation.getCurrentPosition(function(position) { 
         socket.emit('location', {
            'lat' : position.coords.latitude,
            'lon' : position.coords.longitude,
            'radius' : 5
         });
      });

   });

   socket.on('connect', function() {
      navigator.geolocation.getCurrentPosition(function(position) { 
         socket.emit('location', {
            'lat' : position.coords.latitude,
            'lon' : position.coords.longitude,
            'radius' : 5 
         });
      });
   });

   socket.on('message', function(msg) {
      chat = document.getElementById("msg_list");
      displayedMessage = document.createElement('p');
      displayedMessage.innerHTML= msg;
      chat.appendChild(displayedMessage);
   });

   $(window).on('beforeunload',function(){
      socket.disconnect();
   });
});
