drop database moviedb;
create database moviedb;
use moviedb;

create table movie(
	mid INT AUTO_INCREMENT PRIMARY KEY,
    title varchar(50)
);

select * from movie;