from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, send
from coordinate import Coordinate
from userdata import UserData
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretytypeword!'
socketio = SocketIO(app)

connections = dict()

@socketio.on('message')
def handleMessage(msg):
   print('Message: ' + msg)

   for key, value in connections.items():
      if(key != request.sid):
         if(value.position.distanceInMeters(connections[request.sid].position) < value.radius):
            send(msg, room=key)

@socketio.on('location')
def recievedLocation(data):
   print("Recieved location data from: " + request.sid + "\n")
   
   coord = Coordinate()
   coord.setLatitude(data['lat'])
   coord.setLongitude(data['lon'])

   userData = UserData()
   userData.setPosition(coord)
   userData.setRadius(data['radius'])

   connections[request.sid] = userData

@socketio.on('disconnect')
def userDisconnected():
   print("UserID disconnected: " + request.sid + "\n")
   connections.pop(request.sid, None)

@app.route("/")
def index():
	return render_template("chat_room.html")

if __name__ == '__main__':
	app.run(debug=True)
