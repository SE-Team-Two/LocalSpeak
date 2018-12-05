DROP DATABASE speakeasy;
REVOKE ALL ON speakeasy.* FROM 'my_daemon'@localhost;

CREATE DATABASE speakeasy;

USE speakeasy;

CREATE TABLE users (
user_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(32) NOT NULL UNIQUE,
password VARCHAR(32) NOT NULL,
distance SMALLINT(2) NOT NULL DEFAULT 25,
latitude FLOAT(32,30) NOT NULL,
longitude FLOAT(32,30) NOT NULL
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
latitude FLOAT(32,30) NOT NULL,
longitude FLOAT(32,30) NOT NULL
);

ALTER TABLE messages
ADD FOREIGN KEY(username)
REFERENCES users(username)
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
(default,'User6','password6',default,41.147548,-81.343118),
(default,'User7','password7',default,41.147548,-81.343118),
(default,'User8','password8',default,41.147548,-81.343118),
(default,'User9','password9',default,41.147548,-81.343118);

-- CREATE USER 'my_daemon'@'localhost' IDENTIFIED BY 'daemondothething!';

GRANT
SELECT, UPDATE, DELETE, INSERT
ON speakeasy.*
TO 'my_daemon'@'localhost';
