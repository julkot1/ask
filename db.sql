-- Create database
CREATE DATABASE demo_db;

CREATE USER 'demo_user'@'localhost' IDENTIFIED BY 'demo_pass';

GRANT ALL PRIVILEGES ON demo_db.* TO 'demo_user'@'localhost';
FLUSH PRIVILEGES;

USE demo_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100)
);


INSERT INTO users (username, password, email) VALUES
('marek', 'qwerty', 'marek@ip.com'),
('andrzej', 'eqe', 'and.rzej@wp.pl'),
('tomasz', 'tom97.107.111', 'tomwm@ug.pl');
('mariusz', 'mario320', 'mar.iuszek@gmail.com');
('jarek', 'aqdqe', 'jaro230@onet.pl');
('pawel', 'azerty', 'pawwik@o2.pl');

