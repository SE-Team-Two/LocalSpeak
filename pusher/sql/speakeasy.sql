-- DROP DATABASE speakeasy;
-- REVOKE ALL ON speakeasy.* FROM 'my_daemon'@localhost;

CREATE DATABASE speakeasy;

USE speakeasy;

CREATE TABLE users (
username VARCHAR(32) PRIMARY KEY,
password VARCHAR(32) NOT NULL
);

CREATE TABLE messages (
message_id INT(6) ZEROFILL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(32) NOT NULL,
room VARCHAR(32) NOT NULL,
message VARCHAR(128) NOT NULL,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE messages
ADD FOREIGN KEY(username)
REFERENCES users(username)
ON DELETE CASCADE;

INSERT INTO users VALUES 
('User1','password1'),
('User2','password2'),
('User3','password3'),
('User4','password4'),
('User5','password5'),
('User6','password6'),
('User7','password7'),
('User8','password8'),
('User9','password9');

CREATE USER 'my_daemon'@'localhost' IDENTIFIED BY 'daemondothething!';

GRANT
SELECT, UPDATE, DELETE, INSERT
ON speakeasy.*
TO 'my_daemon'@'localhost';
