# Deploying
This is a tutorial on how to run SpeakEasy on your own machine. 

## Prerequisites

#### Python
You must have Python installed (has been tested on 3.7, other versions may or may not work).

#### Python Packages
You must have the following Python Pip packages. 

* flask
* flask-mysql
* geopy
* pusher


To install just run `pip install ` and then the package name. 

#### MySQL Database
You must have access to either a local MySQL database or one running somewhere online. 

#### Pusher API Keys
SpeakEasy uses pusher to send messages between the server and the clients. To get the API keys create an account on https://pusher.com/ and register a web app.

## Setting up MySQL
Create a database named speakeasy, create a user, and grant it SELECT, UPDATE, DELETE, and INSERT permissions.

The sql file in src/sql/setup_database.sql may help with this. 

After that run the commands in src/sql/create_tables.sql on the database to create the tables needed for the SpeakEasy app. 

To add test data, run src/sql/create_test_data.sql.

## Setting up the Flask app
Replace the definitions at the top of app.py with the ones for your environment (i.e. the SQL username, password, etc). Also add your API keys to the pusher declaration. 

Then go into layout.html and add your client side Pusher API key to the declaration in the javascript. 

## Running the Flask app
After everything is set up, just run the command `python app.py` in the console and SpeakEasy should be being served on localhost:5000