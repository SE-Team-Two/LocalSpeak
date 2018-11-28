DROP DATABASE speakeasy;
REVOKE ALL ON speakeasy.* FROM 'my_daemon'@localhost;

CREATE DATABASE speakeasy;

USE speakeasy;

CREATE TABLE users (
user_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(32) NOT NULL UNIQUE,
password VARCHAR(32) NOT NULL,
distance SMALLINT(2) NOT NULL DEFAULT 25
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
creator VARCHAR(32) NOT NULL
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
(default,'User1','password1',default),
(default,'User2','password2',default),
(default,'User3','password3',default),
(default,'User4','password4',default),
(default,'User5','password5',default),
(default,'User6','password6',default),
(default,'User7','password7',default),
(default,'User8','password8',default),
(default,'User9','password9',default);

-- CREATE USER 'my_daemon'@'localhost' IDENTIFIED BY 'daemondothething!';

GRANT
SELECT, UPDATE, DELETE, INSERT
ON speakeasy.*
TO 'my_daemon'@'localhost';
