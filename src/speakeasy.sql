DROP DATABASE speakeasy;
REVOKE ALL ON speakeasy.* FROM 'my_daemon'@localhost;

CREATE DATABASE speakeasy;

USE speakeasy;

CREATE TABLE users (
user_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(32) NOT NULL UNIQUE,
password VARCHAR(32) NOT NULL,
distance SMALLINT(2) NOT NULL DEFAULT 25,
latitude FLOAT(33,30) NOT NULL,
longitude FLOAT(33,30) NOT NULL
);

CREATE TABLE messages (
message_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(32) NOT NULL,
room VARCHAR(32) NOT NULL,
message VARCHAR(256) NOT NULL,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rooms (
room_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(32) NOT NULL UNIQUE,
expire DATETIME NOT NULL,
creator VARCHAR(32) NOT NULL,
latitude FLOAT(33,30) NOT NULL,
longitude FLOAT(33,30) NOT NULL
);

ALTER TABLE messages
ADD FOREIGN KEY(username)
REFERENCES users(username)
ON DELETE CASCADE;

ALTER TABLE messages
ADD FOREIGN KEY(room)
REFERENCES rooms(name)
ON DELETE CASCADE;

ALTER TABLE rooms
ADD FOREIGN KEY(creator)
REFERENCES users(username)
ON DELETE CASCADE;

INSERT INTO users VALUES 
(default,'User1','password1',default,41.147548,-81.343118),
(default,'User2','password2',default,41.147548,-81.343118),
(default,'User3','password3',default,41.147548,-81.343118),
(default,'User4','password4',default,41.147548,-81.343118),
(default,'User5','password5',default,41.147548,-81.343118),
(default,'User6','password6',default,41.147548,-81.343118);

INSERT INTO rooms VALUES
(default,'Global','2020-01-01','User1',-72.559377,-121.568738);

INSERT INTO messages VALUES
(default,'User5','Global','These are some fake messages that are being sent for testing.','2018-11-1 12:34:56'),
(default,'User3','Global','This is also a test bro.','2018-11-2 12:34:56'),
(default,'User5','Global','Big testing type of things happening atm.','2018-11-3 12:34:56'),
(default,'User1','Global','I am a persistant chat message.','2018-11-4 12:34:56'),
(default,'User6','Global','I exist here forever and always in the global chat.','2018-11-5 12:34:56'),
(default,'User1','Global','This one is gonna be a really really long one! HA! You thought I was done lmaooooo. na b im still here. *dabs rapidly* *does flossing dance*','2018-11-6 12:34:56'),
(default,'User6','Global','ooh! killem bro! I BEEEE FLOSSSSSIIIINNNN!','2018-11-7 12:34:56'),
(default,'User2','Global','turn up!','2018-11-8 12:34:56'),
(default,'User5','Global','rain drop! drop top!','2018-11-9 12:34:56'),
(default,'User6','Global','smokin on cook in a hot-box','2018-11-10 12:34:56'),
(default,'User4','Global','*BOX!*','2018-11-11 12:34:56'),
(default,'User4','Global','still testing but ran out of things to say so now im gonna tell you about my kitty. i have many but i got this one tho thats all black and has a white spot on in belly. hes so damn cute. we go walking all the time, he thinks hes a puppy.','2018-11-12 12:34:56'),
(default,'User6','Global','wow cute','2018-11-13 12:34:56'),
(default,'User1','Global','kawaii','2018-11-14 12:34:56'),
(default,'User6','Global','swag','2018-11-15 12:34:56');

-- CREATE USER 'my_daemon'@'localhost' IDENTIFIED BY 'daemondothething!';

GRANT
SELECT, UPDATE, DELETE, INSERT
ON speakeasy.*
TO 'my_daemon'@'localhost';