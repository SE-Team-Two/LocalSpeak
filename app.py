from flask import Flask, render_template, url_for;

app = Flask(__name__);
app.config['SECRET_KEY'] = 'secretytypeword!';

@app.route("/")
def index() :
	return render_template("chat_room.html");

if __name__ == '__main__':
	app.run(debug=True)