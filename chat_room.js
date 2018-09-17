$("#submit_post_btn").click(function () {
	chat= document.getElementById("msg_list");
	msg=	document.createElement('p');
	msg.innerHTML= document.getElementById("post").value;
	chat.appendChild(msg);
	msg.style= "text-align:right;";
	socket.send(document.getElementById("post").value);
	document.getElementById("post").value = "";
});
