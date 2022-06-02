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
	genre_id INT AUTO_INCREMENT PRIMARY KEY,
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

select * from movie;