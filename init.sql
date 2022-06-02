drop database moviedb;
create database moviedb;
use moviedb;

create table movie(
	mid INT AUTO_INCREMENT PRIMARY KEY,
    title varchar(50),
    title_eng varchar(50),
    film_rating varchar(50),
    film_rating_foreign varchar(50),
    summary varchar(5000),
    makingnote varchar(5000),
    aka varchar(1000),
    country varchar(50),
    releasedate datetime,
    screening bool
);

create table genre(
	genre_id INT PRIMARY KEY,
    name varchar(50)
);

create table movie_genre(
	mid int,
    genre_id int,
	primary key(mid, genre_id),
    foreign key(mid) references moviedb.movie(mid)
		on update cascade
        on delete cascade,
	foreign key(genre_id) references moviedb.genre(genre_id)
		on update cascade
        on delete cascade
);
insert into genre(genre_id, name)
values
(1,'드라마'),
(2,'판타지'),
(3,'서부'),
(4,'공포'),
(5,'멜로/로멘스'),
(6,'모험'),
(7,'스릴러'),
(8,'느와르'),
(9,'컬트'),
(10,'다큐멘터리'),
(11,'코미디'),
(12,'가족'),
(13,'미스터리'),
(14,'전쟁'),
(15,'애니메이션'),
(16,'범죄'),
(17,'뮤지컬'),
(18,'SF'),
(19,'액션'),
(20,'무협'),
(21,'에로'),
(22,'서스펜스'),
(23,'서사'),
(24,'블랙코미디'),
(25,'실험'),
(26, '공연실황');

select * from movie;