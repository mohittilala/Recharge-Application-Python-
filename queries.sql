#drop database mydb2;
CREATE DATABASE mydb3;

USE mydb3;

CREATE TABLE useracc (username VARCHAR(10) PRIMARY KEY, passwd VARCHAR(10));

CREATE TABLE plan (plan_id int primary key, amount int, data varchar(20), validity varchar(15), details varchar(100), facility varchar(100));

CREATE TABLE adminacc (admin_id VARCHAR(20) PRIMARY KEY, passwd VARCHAR(50));

CREATE TABLE userplan (plan_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(10), plan INT, time DATETIME);

CREATE TABLE recharge (reg_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(10), amount FLOAT, time DATETIME);

CREATE TABLE history (h_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(10), time DATETIME, type varchar(1));

INSERT INTO adminacc (admin_id, passwd) VALUES ("admin", "admin@123");

INSERT INTO plan (plan_id, amount, data, validity, details, facility) VALUES 
("1", "399", "1.5 GB/day", "84 days", "Unlimited calls + 100 sms/day", "Music premium(84 days) + MyCinema(84 days)"),
("2", "149", "1.5 GB/day", "28 days", "Unlimited calls + 100 sms/day", "Music premium(28 days)"),
("3", "99", "3 GB", "28 days", "Unlimited calls + 50 sms/day", "Music premium(28 days)");