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

   for k, v in connections.items():
      if(k != request.sid):
         if(v.position.distanceInMeters(connections[request.sid].position) < v.radius):
            send(msg, room=k)

@socketio.on('location')
def recievedLocation(data):
   coord = Coordinate()
   coord.setLatitude(data['lat'])
   coord.setLongitude(data['lon'])

   userData = UserData()
   userData.setPosition(coord)
   userData.setRadius(data['radius'])

   connections[request.sid] = userData
   

@app.route("/")
def index():
	return render_template("chat_room.html")

if __name__ == '__main__':
	app.run(debug=True)
