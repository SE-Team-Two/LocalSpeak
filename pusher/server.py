from flask import Flask, render_template, url_for, session, request, redirect, jsonify;
from flask_session import Session;
from flask_mysqldb import MySQL
from pusher import Pusher;
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
  key='da7281b2ef6e49a7428b',
  secret='60e10372b2a2c9c22519',
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

@app.route("/save",methods=['POST'])
def save():
	session['username'] = request.form['username']
	session['SID'] = request.form['SID']
	return jsonify(msg='Success!')

@app.route("/authenticate",methods=['POST'])
def authenticate():
  auth = pusher.authenticate( channel=request.form['channel_name'],
  														socket_id=request.form['socket_id'],
  														custom_data= {'user_id':session['username']})
  return json.dumps(auth)

@app.route("/get/<request>/<room>",methods=['POST'])
def get(request,room):
	if request == "messages":
		cursor = mysql.connection.cursor()
		query = "SELECT * FROM messages WHERE room ='" + room +"' ORDER BY time DESC LIMIT 10;"
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
