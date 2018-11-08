$(document).ready(function () {
   var socket = io.connect('https://' + document.domain + ":" + location.port);
   
   var defaultRadius = 10000;

   function colorPicker(x){
	   switch(x){
		   case 0: return "Aqua"; break;
		   case 1: return "Beige"; break;
		   case 2: return "Brown"; break;
		   case 3: return "Coral"; break;
		   case 4: return "Crimson"; break;
		   case 5: return "DarkMagenta"; break;
		   case 6: return "DarkSlateGray"; break;
		   case 7: return "DimGray"; break;
		   case 8: return "ForestGreen"; break;
		   case 9: return "Gold"; break;
	   }
   }
   
   function sendFromTextBox() {
      chat = document.getElementById("msg_list");
      msg = document.createElement('p');
      msg.innerHTML = document.getElementById("post").value;
      chat.appendChild(msg);
      msg.style = "text-align:right;";
      socket.send(document.getElementById("post").value);
      document.getElementById("post").value = "";
	  msg.style.backgroundColor = colorPicker(Math.floor(Math.random() * Math.floor(9)));
	  msg.style.clear = "both";
	  msg.style.float = "right";
	  chat.scrollTop = chat.scrollHeight;
   }
   
   function setColor() {
	   
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