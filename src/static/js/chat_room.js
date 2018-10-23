$(document).ready(function () {
   var socket = io.connect('https://' + document.domain + ":" + location.port);
   
   var defaultRadius = 20;

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
   

   // TODO: should become sendPosition and sendRadius later
   function sendData(lat, lon, radius) {
      socket.emit('location', {
         'lat': lat,
         'lon': lon,
         'radius': radius
      });
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
         sendData(position.coords.latitude, position.coords.longitude, defaultRadius);
      });

   });

   socket.on('connect', function() {
      navigator.geolocation.getCurrentPosition(function(position) { 
         sendData(position.coords.latitude, position.coords.longitude, defaultRadius);
      });
   });

   socket.on('message', function(msg) {
      chat = document.getElementById("msg_list");
      displayedMessage = document.createElement('p');
      displayedMessage.innerHTML= msg;
      chat.appendChild(displayedMessage);
      chat.scrollTop = chat.scrollHeight;
   });

   $(window).on('beforeunload',function(){
      socket.disconnect();
   });
});
