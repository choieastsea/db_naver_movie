from shutil import which
from tokenize import Double
import pymysql
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from init_db import open_db
from enum import Enum
from enter import get_url
from crawl_movie_basic import get_basic
from crawl_movie_basic import get_actor
from crawl_movie_basic import get_director
from crawl_movie_basic import get_producer
from crawl_movie_basic import get_company
from crawl_movie_basic import get_relate
from crawl_movie_detail import get_comment_data
from crawl_movie_detail import get_data_from_review_url
from crawl_movie_detail import get_enjoy_point_data
from crawl_movie_detail import get_moie_data
from crawl_movie_detail import get_quotes_data
from crawl_movie_detail import get_photo_data
from crawl_movie_detail import get_satisfying_netizen_data
from crawl_movie_detail import get_satisfying_viewer_data
from crawl_movie_detail import get_score_data
from crawl_movie_detail import get_viewing_trend_data
from crawl_movie_detail import get_video_data

NETIZEN = 1
VIEWER = 2
CRITIC = 3

def insert_movie():
    # a=[]
    # genre=[]
    # movie_index = 1
    # [story,makingnote] = get_basic(0)
    # genre = get_data_from_movie_url("https://movie.naver.com/movie/bi/mi/basic.naver?code=192608")

    # # 장르 이름을 받아올 때
    # a.append(["범죄도시",None,None,None,story,makingnote,None,None,None,None])

    # 한영화의 loop안에서 다 해결가능할 듯 함 
    # 예를들어 
    # 1. 범죄도시 들어오면 범죄도시의 code를 변수로 저장한다
    # 2. 영화인의 1씩 증가하는 영화인id를 만들어서 내부에 for loop로 영화 내의 영화인들을 넣는 loop를 만든다
    # 3. 영화인들을 넣을 때 code가 있는 애들은 해당 코드를 select 하여서 해당 code를 검색하는 select문 작성 후 그 것이 not exist하면 그 테이블에 넣는 식으로한다.https://ayoteralab.tistory.com/entry/MySQL-INSERT-WHERE-NOT-EXISTS
    # 4. 해당 영화에 해당하는 영화인들을 모두 넣고 
    # 5. 영화 출연(appearance) 테이블을 만든다 영화 출연 테이블의 id도 우리가 직접 관리한다. 그리고 영화인의 id도 가지고 있으니 출연(apperance)테이블은 생성 가능하다
    # 6. 영화인의 명대사(quotes)와 배역(casting)을 넣어야하는데 이미 우리는 영화인의 id를 가지고 있고, 출연(appearance)의 id도 가지고 있다. 
    # 7. 따라서  명대사 내용 추천수등을 넣어서 테이블 생성가능하고
    # 8. 배역이름을 넣어서 배역(casting)테이블도 생성 가능하다.
    # 9. 이렇게해서 영화와 영화인은 모두 넣었다. 나머지 것들도 한 영화 loop안에서 다 넣을 수 있다.

    # 요지는 autoincrement id들을 우리가 직접 관리하면 된다는 것임.(전역변수든 뭐든 해서)
    # 이론은 이렇다 대충 코드 적어보겠음. 

    # 크롤링할 떄 무비 코드를 얻어온다. 얻어온 무비코드를 변수에 저장하고 그것을 다른 테이블요소를 채울 때 사용해야 한다. 
    # 추천수:300으로 통일, 비추천수 28로 통일

    # todo. sql에서 autoincrement 빼야될 애들 빼줘야됨

    # ####################################################################################################################################################################################
    [conn,curs] = open_db()

    addr = get_url() # addr은 영화 코드 배열
    # addr = [192608]
    mpeople_index=int(147483647)
    for movie_code2 in addr:
        movie_code = int(movie_code2)
        [story,makingnote] = get_basic(movie_code)
        movie_data= get_moie_data(movie_code)
        
        # movie =  [code,한국영화등급 , "해외영화등급", "스토리 ~~~~", "메이킹 노트","A.K.A", "영화이름(국내)", "영화이름(해외) ","2020-10-10", "상영중 여부",img ,runningtime ,누적관객수]
    
        [story,makingnote] = get_basic(movie_code)

        # 영화 기본 정보 배열
        movie=[movie_code,movie_data[9], movie_data[10], story, makingnote ,movie_data[12], movie_data[2], movie_data[3] ,movie_data[8], movie_data[1], movie_data[4], movie_data[7],movie_data[11],movie_data[6]]
        commitq(conn,curs,SQL.movie, movie)
        [actor,subactor] = get_actor(movie_code)
        director_arr = get_director(movie_code)
        producer_arr = get_producer(movie_code)
        
        #  영화인 - 배우
        if actor!=None:
            for act in actor : 
                # act[0] : tumbnail act[1]:영화인code act[2]:이름 act[3]: 영어이름 act[4] :주연/조연 act[5] : ...역

                if act[1]==None:
                    subpeople = [mpeople_index,movie_code ,act[2],  act[5]]
                    mpeople_index +=1
                    commitq(conn,curs,SQL.mpeople_sub,subpeople)
                else:
                    mpeople = [int(act[1]),act[0] ,act[2],  act[3]]
                    commitq(conn,curs,SQL.people,mpeople)

                movie_appearance = [int(act[1]),movie_code,act[5]]
                commitq(conn,curs,SQL.movie_appearance,movie_appearance)
                casting = [int(act[1]),movie_code,act[4]]
                commitq(conn,curs,SQL.casting,casting)

        # 영화인 - 서브배우
        if subactor!=None:
            for act in subactor : 
                # act[0] :이름, act[1]:영화인code, act[2]:...역
                if act[1]==None:
                    subpeople = [mpeople_index,movie_code ,act[0],  act[2]]
                    mpeople_index +=1
                    commitq(conn,curs,SQL.mpeople_sub,subpeople)
                else:
                    mpeople = [int(act[1]),None ,act[0],  None]
                    commitq(conn,curs,SQL.people,mpeople)


                movie_appearance = [int(act[1]),movie_code,act[2]]
                commitq(conn,curs,SQL.movie_appearance,movie_appearance)

                casting = [int(act[1]),movie_code,None]
                commitq(conn,curs,SQL.casting,casting)

        
        # 영화인 - 감독
        if director_arr!=None:
            for act in director_arr : 
                # act[0] : tumbnail act[1]:영화인code act[2]:이름 act[3]: 영어이름 
                if act[1]==None:
                    subpeople = [mpeople_index,movie_code ,act[2],  "감독"]
                    mpeople_index +=1
                    commitq(conn,curs,SQL.mpeople_sub,subpeople)

                else:
                    mpeople = [int(act[1]),act[0] ,act[2],  act[3]]
                    commitq(conn,curs,SQL.people,mpeople)


                movie_appearance = [int(act[1]),movie_code,None]
                commitq(conn,curs,SQL.movie_appearance,movie_appearance)

                # 명대사 quotes get 함수 & for문
                # quotes = [act[1],movie_code,"명대사 1 ", "추천수 (int)"]

                casting = [int(act[1]),movie_code,"감독"]
                commitq(conn,curs,SQL.casting,casting)

        
        # 영화인 - 제작진
        if producer_arr!=None:
            for act in producer_arr : 
                #  act[0]:영화인code act[2] :part  act[3]:이름 act[1]: 영어이름
                if act[0]==None:
                    subpeople = [mpeople_index,movie_code ,act[3],  act[2]]
                    commitq(conn,curs,SQL.mpeople_sub,subpeople)
                    mpeople_index +=1
                else:
                    mpeople = [mpeople_index,None ,act[3],  act[1]]
                    commitq(conn,curs,SQL.people,mpeople)
                    movie_appearance = [int(act[0]),movie_code,None]
                    commitq(conn,curs,SQL.movie_appearance,movie_appearance)
                    casting = [int(act[0]),movie_code, act[2]]
                    commitq(conn,curs,SQL.casting,casting)


        # 명대사
        quotes_arr = get_quotes_data(movie_code)
        if quotes_arr !=None:
            for quote in quotes_arr:
                # quote[1] : people code  quote[2] = comment , quote[5]: 추천수 , quote[6] : user id
                if quote[1] == None: quote[1]=0
                if quote[5] == None: quote[5]=0

                quotes = [int(quote[1]),movie_code, quote[2],int(quote[5]),quote[6]]
                commitq(conn,curs,SQL.quotes,quotes)

        
        # 연관영화
        relates = get_relate(movie_code)
        if relates !=None:
            for relate_movie in relates:
                insert_value = [movie_code, int(relate_movie), int(relate_movie)]
                commitq(conn,curs,SQL.relate_movie,insert_value)


        # 한줄평
        comments = get_comment_data(movie_code)
        if comments !=None:
            for comment in comments:
                insert_value = [movie_code, int(comment[1]),comment[2],comment[3]]
                commitq(conn,curs,SQL.comment,insert_value)


        # 리뷰
        review_data_list = get_data_from_review_url(movie_code)
        if review_data_list !=None:
            for review in review_data_list :
                if review[1]==None: review[1]=0
                if review[4]==None: review[4]=0
                if review[5]==None: review[5]=0

                insert_value = [movie_code, review[0],int(review[4]),int(review[5]),review[2],review[3],review[6],int(review[1])]
                commitq(conn,curs,SQL.review,insert_value)


        # 평점 (score)
        scores = get_score_data(movie_code)
        if scores !=None:
            for score1 in scores : 
                if score1[1] == None:
                    insert_value = [movie_code, score1[2], None, int(score1[3])]
                    commitq(conn,curs,SQL.score,insert_value)


                elif score1[3] == None:
                    insert_value = [movie_code, score1[2],  int(score1[1]), None]
                    commitq(conn,curs,SQL.score,insert_value)

                
                elif score1[3] == None and score1[1] == None:
                    insert_value = [movie_code, score1[2], None, None]
                    commitq(conn,curs,SQL.score,insert_value)
                else:
                    insert_value = [movie_code, score1[2], int(score1[1]), int(score1[3])]
                    commitq(conn,curs,SQL.score,insert_value)

        # 장르
        genres = movie_data[5]
        if genres !=None:
            for genre in genres:
                insert_value = [genre,movie_code]
                commitq(conn,curs,SQL.genre,insert_value)


        # 회사
        companies = get_company(movie_code)
        if companies !=None:
            for company in companies:
                insert_value = [movie_code, company[1],company[0]]
                commitq(conn,curs,SQL.company,insert_value)


        # 사진
        photoes  = get_photo_data(movie_code)
        if photoes !=None:
            for photo in photoes:
                insert_value = [movie_code, photo[1]]
                commitq(conn,curs,SQL.photo,insert_value)

        # 동영상
        videos = get_video_data(movie_code)
        if videos !=None:
            for video in videos:
                insert_value = [movie_code, video[3], video[2],video[1]]
                commitq(conn,curs,SQL.video,insert_value)


        # enjoy_point
        [eps,eps2] = get_enjoy_point_data(movie_code)
        if eps!=None and len(eps) > 2 :
            insert_value = [movie_code,eps[1],eps[2],eps[3],eps[4],eps[5],int(eps[0])]
            commitq(conn,curs,SQL.enjoy_point,insert_value)


        if eps2!=None and len(eps2) > 2 :
            insert_value = [movie_code,eps2[1],eps2[2],eps2[3],eps2[4],eps2[5],int(eps2[0])]
            commitq(conn,curs,SQL.enjoy_point,insert_value)


        # satifying_netizen
        sns = get_satisfying_netizen_data(movie_code)
        if sns!=None:
            insert_value = [movie_code, sns[0],sns[1],sns[2],sns[3],sns[4],sns[5],sns[6]]
            commitq(conn,curs,SQL.satisfying_netizen,insert_value)

        else:
            insert_value = [movie_code, None,None,None,None,None,None,None]
            commitq(conn,curs,SQL.satisfying_netizen,insert_value)


        # satifying_viewer
        svs = get_satisfying_viewer_data(movie_code)
        if svs!=None:
            insert_value = [movie_code, svs[0],svs[1],svs[2],svs[3],svs[4],svs[5],svs[6]]
            commitq(conn,curs,SQL.satisfying_viewer,insert_value)

        else:
            insert_value = [movie_code, None,None,None,None,None,None,None]
            commitq(conn,curs,SQL.satisfying_viewer,insert_value)


        # viewing trend
        vts = get_viewing_trend_data(movie_code)
        if vts != None:
            insert_value = [movie_code, vts[0],vts[1],vts[2],vts[3],vts[4]]
            commitq(conn,curs,SQL.viewing_trend,insert_value)

        else:
            insert_value = [movie_code, None,None,None,None,None]
            commitq(conn,curs,SQL.viewing_trend,insert_value)

    curs.close()
    conn.close()



    
# flag  1: movie 2:people 3:movie_appearance 4:quotes 5:casting 6:mpeople_sub 7:relate_movie 8:comment 9:review 10:score 11:review_comment 12:genre 13:country 14:company 15:photo 16:video 17:enjoy_point 18:satisfying_netizen 19:viewing_trend 20:satisfying_viewer
def commitq(conn,curs,flag, a):
    [conn,curs] = open_db()
    if flag== SQL.movie:
         sql = """insert IGNORE into movie (movie_code, film_rate_kor, film_rate_foreign , story, makingnote , aka , title_kor , title_foreign , release_date, current_opening, img_url , running_time, cumulate_audience,country) 
        values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    elif flag== SQL.people :
         sql = """insert IGNORE into people (people_code, thumbnail, name , eng_name) 
        values (%s, %s, %s,%s);"""
    elif flag== SQL.movie_appearance :
        sql = """insert IGNORE into movie_appearance (people_code, movie_code, role) 
        values (%s, %s, %s);"""
    elif flag== SQL.quotes :
        sql = """insert IGNORE into quotes (people_code, movie_code, quotes , good, userid) 
        values (%s, %s, %s,%s,%s);"""
    elif flag== SQL.casting :
        sql = """insert IGNORE into casting (people_code, movie_code, casting_name) 
        values (%s, %s, %s);"""
    elif flag== SQL.mpeople_sub :
        sql = """insert IGNORE into mpeople_sub (mpeople_sub_id,movie_code, name, casting) 
        values (%s,%s, %s, %s);"""
    elif flag== SQL.relate_movie :
        sql = """insert IGNORE into relate_movie (movie_code, movie_code1) 
        select %s, %s from relate_movie
        where exists (select * from movie m where m.movie_code=%s);"""
    elif flag== SQL.comment :
        sql = """insert IGNORE into comment (movie_code, score, comment , type) 
        values (%s, %s, %s,%s);"""
    elif flag== SQL.review :
        sql = """insert IGNORE into review ( movie_code, title , view_num, good , date , writer , contents ,review_score) 
        values (%s, %s,%s,%s,%s,%s,%s,%s);"""
    elif flag== SQL.score :
        sql = """insert IGNORE into score (movie_code, score, type , comment_number) 
        values (%s, %s, %s,%s);"""
    elif flag== SQL.genre :
        sql = """insert IGNORE into genre (genre_name, movie_code) 
        values (%s, %s);"""
    elif flag== SQL.company :
        sql = """insert IGNORE into company (movie_code, name, role) 
        values (%s, %s, %s);"""
    elif flag== SQL.photo :
        sql = """insert IGNORE into photo (movie_code, url) 
        values (%s, %s);"""
    elif flag== SQL.video :
        sql = """insert IGNORE into video (movie_code, video_url, thumbnail_url , title) 
        values (%s, %s, %s,%s);"""
    elif flag== SQL.enjoy_point :
        sql = """insert IGNORE into enjoy_point (movie_code, production, acting , story, recording_beauty , ost,type ) 
        values (%s, %s, %s,%s,%s,%s,%s);"""
    elif flag== SQL.satisfying_netizen :
        sql = """insert IGNORE into satisfying_netizen (movie_code, male, female , tenth, twentieth , thirtieth , fortieth , fiftieth ) 
        values (%s, %s, %s,%s,%s,%s,%s,%s);"""
    elif flag== SQL.viewing_trend :
        sql = """insert IGNORE into viewing_trend (movie_code, tenth , twentieth , thirtieth , fortieth , fiftieth) 
        values ( %s,%s,%s,%s,%s,%s);"""
    elif flag== SQL.satisfying_viewer :
        sql = """insert IGNORE into satisfying_viewer (movie_code, male, female , tenth, twentieth , thirtieth , fortieth , fiftieth ) 
        values (%s, %s, %s,%s,%s,%s,%s,%s);"""
    else : 
        print("invalid sql")

    # print(a)
    curs.execute(sql, a)
    
    conn.commit()
    

class SQL(Enum):
    movie = 1
    people = 2
    movie_appearance = 3
    quotes = 4
    casting = 5
    mpeople_sub = 6
    relate_movie = 7
    comment = 8
    review =9
    score = 10
    review_comment = 11
    genre = 12
    country = 13
    company = 14
    photo = 15
    video = 16
    enjoy_point = 17
    satisfying_netizen = 18
    viewing_trend = 19
    satisfying_viewer = 20

if __name__ == '__main__':
    insert_movie()

