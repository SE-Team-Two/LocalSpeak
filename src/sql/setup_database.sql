DROP DATABASE speakeasy;
REVOKE ALL ON speakeasy.* FROM 'my_daemon'@localhost;

CREATE DATABASE speakeasy;

-- CREATE USER 'my_daemon'@'localhost' IDENTIFIED BY 'daemondothething!';

GRANT
SELECT, UPDATE, DELETE, INSERT
ON speakeasy.*
TO 'my_daemon'@'localhost';