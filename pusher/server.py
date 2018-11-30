from flask import Flask, render_template, url_for, session, request, redirect, jsonify;
from flask_session import Session;
from flask_mysqldb import MySQL
from pusher import Pusher;
from datetime import datetime, timedelta
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
		session['username'] = request.form['username'];
		session['room'] = 'Global';
		return redirect(url_for("chat",username=session['username'])); 
	elif 'username' in session:
		session['room'] = 'Global';
		return redirect(url_for("chat",username=session['username'])); 
	else:
		return render_template("login.html");

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
		channels = pusher.channels_info()
		pusher.trigger(channels['channels'].keys(),'new_room',{'room':room,'username':username})
		name = request.form['name']
		delta = request.form['time']
		time = datetime.now() + timedelta(hours=int(delta))
		query= "INSERT INTO rooms VALUES (default,'"+name+"','"+str(time)+"','"+username+"');"
		cursor = mysql.connection.cursor()
		cursor.execute(query)
		mysql.connection.commit();
		return jsonify(msg='Success!')

@app.route("/save",methods=['POST'])
def save():
	session['username'] = request.form['username']
	session['SID'] = request.form['SID']
	return jsonify(msg='Success!')

@app.route("/authenticate",methods=['POST'])
def authenticate():
  auth = pusher.authenticate( channel=request.form['channel_name'],
			     socket_id=request.form['socket_id'],custom_data= {'user_id':session['username']})
  return json.dumps(auth)

@app.route("/get/<request>",methods=['POST'])
@app.route("/get/<request>/<room>",methods=['POST'])
def get(request,room=None):
	if request == "messages":
		cursor = mysql.connection.cursor()
		query = "SELECT * FROM messages WHERE room ='" + room +"' ORDER BY time DESC LIMIT 50;"
		cursor.execute(query)
		data = cursor.fetchall()
		return jsonify(data=data)
	elif request == "rooms":
		cursor = mysql.connection.cursor()
		query = "SELECT * FROM rooms;"
		cursor.execute(query)
		data = cursor.fetchall()
		return jsonify(data=data)

@app.route("/logout")
def logout():
	session.pop('username');
	session.pop('SID',None);
	return redirect(url_for('login'));

def mk_room(room):
	return 'presence-'+room

# @app.route("/testing")
# def testing():
# 	return render_template("testing.html",string=str(request.cookies['session']))

if __name__ == '__main__':
	app.run(debug=True)
