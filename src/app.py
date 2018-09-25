from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretytypeword!'
socketio = SocketIO(app)

@socketio.on('message')
def handleMessage(msg):
   print('Message: ' + msg)
   send(msg, broadcast=True);

@app.route("/")
def index() :
	return render_template("chat_room.html")

if __name__ == '__main__':
	app.run(debug=True)
