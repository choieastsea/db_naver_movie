import pymysql
import requests
from bs4 import BeautifulSoup
from init_db import open_db
from crawl_movie_basic import get_basic
from crawl_movie_basic import get_actor
from crawl_movie_basic import get_director
from crawl_movie_basic import get_producer
from crawl_movie_detail import get_data_from_movie_url

def insert_movie():
    a=[]
    genre=[]
    movie_index = 1
    [story,makingnote] = get_basic(0)
    genre = get_data_from_movie_url("https://movie.naver.com/movie/bi/mi/basic.naver?code=192608")

    # 장르 이름을 받아올 때
    a.append(["범죄도시",None,None,None,story,makingnote,None,None,None,None])
    commit(a,genre,movie_index)


def commit(a,genre,movie_index):
    [conn,curs] = open_db()

    sql ="""insert into movie (title, title_eng, film_rating,film_rating_foreign,summary,makingnote,aka,country,releasedate,screening) 
        values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s);"""
    sql2 ="""insert into movie_genre (movie_index,genre_id) 
        values (%s, %s);"""
    
    # print(a)
    curs.executemany(sql, a)
    for g in genre:
        curs.executemany(sql, [movie_index,g])
    
    conn.commit()
    curs.close()
    conn.close()


if __name__ == '__main__':
    insert_movie()

