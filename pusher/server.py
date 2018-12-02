from flask import Flask, render_template, url_for, session, request, redirect, jsonify;
from flask_session import Session;
from flask_mysqldb import MySQL
from pusher import Pusher;
from datetime import datetime, timedelta
from geopy import distance
import json

app = Flask(__name__);
SECRET_KEY = 'secretytypeword!';
SESSION_TYPE = 'filesystem';
MYSQL_USER = 'my_daemon';
MYSQL_PASSWORD = 'daemondothething!';
MYSQL_DB = 'speakeasy';
app.config.from_object(__name__)

Session(app);
mysql = MySQL(app)

pusher = Pusher(
  app_id='655434',
  key = "8d8668079552b2207a73",
  secret = "6a78990c43960ac1fec2",
  cluster='us2',
  ssl=True
);

@app.route("/",methods=['POST','GET'])
def login():
	if request.method == "POST":
		username = request.form['username'];
		password = request.form['password'];
		cursor = mysql.connection.cursor()
		query = "SELECT * FROM users WHERE username ='" + username +"';"
		cursor.execute(query)
		data = cursor.fetchall()
		if data:
			if data[0][2] == password:
				session['username'] = username;
				session['distance'] = data[0][3];
				return redirect(url_for("chat",username=session['username']));
		else:
			return render_template("login.html",error=1);
	elif 'username' in session:
		return redirect(url_for("chat",username=session['username'])); 
	else:
		return render_template("login.html",error=0);

@app.route("/chat/<username>")
def chat(username):
	if 'username' in session and session['username'] == username:
		return render_template("chat_room.html",curr_usr=username);
	else:
		return render_template("login.html");

@app.route("/settings/<username>")
def settings(username):
	if 'username' in session and session['username'] == username:
		return render_template("settings.html",curr_usr=username);
	else:
		return render_template("login.html");

@app.route("/message/<room>",methods=['POST'])
def message(room):
	username = request.form['username']
	if 'username' in session and session['username'] == username:
		msg = request.form['msg']
		pusher.trigger(mk_room(room),'message',{'msg':msg,'username':username})
		query = "INSERT INTO messages VALUES (default,'"+username+"','"+room+"','"+msg+"',default);"
		cursor = mysql.connection.cursor()
		cursor.execute(query)
		mysql.connection.commit();
		return jsonify(username=username,msg=msg)
	else:
		return jsonify(username=username,msg='Message Failed!')

@app.route("/create/<room>",methods=['POST'])
def create(room):
	username = request.form['username']
	if 'username' in session and session['username'] == username:
		name = request.form['name']
		delta = request.form['time']
		time = datetime.now() + timedelta(hours=int(delta))
		query= "INSERT INTO rooms VALUES (default,'"+name+"','"+str(time)+"','"+username+"',"+session['lat']+","+session['long']+");"
		cursor = mysql.connection.cursor()
		cursor.execute(query)
		mysql.connection.commit();
		query = "SELECT * FROM users;"
		cursor.execute(query)
		response = cursor.fetchall()
		data = list()
		r_position = (session['lat'],session['long'])
		for user in response:
			u_position = (user[4],user[5])
			u_distance = user[3]
			if distance.distance(r_position,u_position).miles <= u_distance:
				data.append(user[1]);
		for user in data:
			pusher.trigger('private-'+user,'new_room',{'room':room,'username':username})
		return jsonify(msg='Success!')

@app.route("/save/<call>",methods=['POST'])
def save(call):
	if call == "user":
		session['username'] = request.form['username']
		session['lat'] = request.form['lat']
		session['long'] = request.form['long']
		query = "UPDATE users SET latitude = "+request.form['lat']+", longitude ="+request.form['long']+" WHERE username = '"+request.form['username']+"';"
		cursor = mysql.connection.cursor()
		cursor.execute(query)
		mysql.connection.commit();
		return jsonify(msg='Success!')
	if call == "distance":
		session['distance'] = request.form['distance']
		query = "UPDATE users SET distance = "+request.form['distance']+" WHERE username = '"+request.form['username']+"';"
		cursor = mysql.connection.cursor()
		cursor.execute(query)
		mysql.connection.commit();
		return jsonify(msg='Success!')

@app.route("/authenticate",methods=['POST'])
def authenticate():
  auth = pusher.authenticate( channel=request.form['channel_name'],
  														socket_id=request.form['socket_id'],
  														custom_data= {'user_id':session['username']})
  return json.dumps(auth)

@app.route("/get/<call>",methods=['POST'])
@app.route("/get/<call>/<room>",methods=['POST'])
def get(call,room=None):
	username = request.form['username']
	if 'username' in session and session['username'] == username: 
		if call == "messages":
			cursor = mysql.connection.cursor()
			query = "SELECT * FROM messages WHERE room ='" + room +"' ORDER BY time DESC LIMIT 50;"
			cursor.execute(query)
			data = cursor.fetchall()
			return jsonify(data=data)
		elif call == "rooms":
			cursor = mysql.connection.cursor()
			query = "SELECT * FROM rooms;"
			cursor.execute(query)
			response = cursor.fetchall()
			data = list()
			u_position = (request.form['lat'],request.form['long'])
			for room in response:
				r_position = (room[4],room[5])
				if distance.distance(r_position,u_position).miles <= int(session['distance']):
					data.append(room);
			return jsonify(data=data)
		elif call == "distance":
			cursor = mysql.connection.cursor()
			query = "SELECT distance FROM users where username='"+username+"';"
			cursor.execute(query)
			data = cursor.fetchall()
			return jsonify(data=data)

@app.route("/logout")
def logout():
	session.pop('username');
	session.pop('lat');
	session.pop('long');
	return redirect(url_for('login'));

def mk_room(room):
	return 'presence-'+room

if __name__ == '__main__':
	app.run(debug=True)
