import pymysql
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from init_db import open_db
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
from crawl_movie_detail import get_movie_data
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
    
    addr = get_url() # addr은 영화 코드 배열
    mpeople_index=int(147483647)
    for movie_code2 in addr:
        movie_code = int(movie_code2)
        [story,makingnote] = get_basic(movie_code)
        movie_data= get_movie_data(movie_code)

        genre = movie_data[5]
        country = movie_data[6]
        # movie =  [code,한국영화등급 , "해외영화등급", "스토리 ~~~~", "메이킹 노트","A.K.A", "영화이름(국내)", "영화이름(해외) ","2020-10-10", "상영중 여부",img ,runningtime ,누적관객수]
    
        [story,makingnote] = get_basic(movie_code)

        # 영화 기본 정보 배열
        movie=[movie_code,movie_data[9], movie_data[10], story, makingnote ,movie_data[12], movie_data[2], movie_data[3] ,movie_data[8], movie_data[1], movie_data[4], movie_data[7],movie_data[11] ]

        [actor,subactor] = get_actor(movie_code)
        director_arr = get_director(movie_code)
        producer_arr = get_producer(movie_code)

        #  영화인 - 배우
        for act in actor : 
            # act[0] : tumbnail act[1]:영화인code act[2]:이름 act[3]: 영어이름 act[4] :주연/조연 act[5] : ...역

            if act[1]==None:
                subpeople = [mpeople_index,movie_code ,act[2],  act[5]]
                mpeople_index +=1
            else:
                mpeople = [int(act[1]),act[0] ,act[2],  act[3]]

            movie_appearance = [int(act[1]),movie_code,act[5]]

            casting = [int(act[1]),movie_code,act[4]]

        # 영화인 - 서브배우
        for act in subactor : 
            # act[0] :이름, act[1]:영화인code, act[2]:...역
            if act[1]==None:
                subpeople = [mpeople_index,movie_code ,act[0],  act[2]]
                mpeople_index +=1
            else:
                mpeople = [int(act[1]),None ,act[0],  None]

            movie_appearance = [int(act[1]),movie_code,act[2]]

            casting = [int(act[1]),movie_code,None]
        
        # 영화인 - 감독
        for act in director_arr : 
            # act[0] : tumbnail act[1]:영화인code act[2]:이름 act[3]: 영어이름 
            if act[1]==None:
                subpeople = [mpeople_index,movie_code ,act[2],  "감독"]
                mpeople_index +=1
            else:
                mpeople = [int(act[1]),act[0] ,act[2],  act[3]]

            movie_appearance = [int(act[1]),movie_code,None]
            # 명대사 quotes get 함수 & for문
            # quotes = [act[1],movie_code,"명대사 1 ", "추천수 (int)"]

            casting = [int(act[1]),movie_code,"감독"]
        
        # 영화인 - 제작진
        for act in producer_arr : 
            #  act[0]:영화인code act[2] :part  act[3]:이름 act[1]: 영어이름
            if act[0]==None:
                if(act[3]==None):
                    act[3]=act[1]
                subpeople = [mpeople_index,movie_code ,act[3],  act[2]]
                mpeople_index +=1
            else:
                mpeople = [int(act[0]),None ,act[3],  act[1]]

            movie_appearance = [int(act[0]),movie_code,None]

            casting = [int(act[0]),movie_code, act[2]]

        # 명대사
        quotes_arr = get_quotes_data(movie_code)
        for quote in quotes_arr:
            # quote[1] : people code  quote[2] = comment , quote[5]: 추천수 , quote[6] : user id
        
            quotes = [int(quote[1]),movie_code, quote[2],int(quote[5]),quote[6]]
        
        # 연관영화
        relates = get_relate(movie_code)
        for relate_movie in relates:
            insert_value = [movie_code, int(relate_movie)]

        # 한줄평

        # 리뷰

        # 평점 (score)
        scores = get_score_data(movie_code)

        # 장르

        # 나라(country)

        # 회사

        # 사진

        # 동영상

        # enjoy_point

        # satifying_netizen

        # satifying_viewer

        # viewing trend







# ##########################################################################################################################################
    # mpeople_sub = [movie_code,"보조영화인이름","역할 - 감독/제작진 등"]

    # # 영화인
    # mpeople_code =213123
    # # mpeople_id = 1  # 0부터 1씩 증가하는 영화인 id를 우리가 직접 넣어준다.
    # mpeople = [mpeople_code,"tumbnail url" ,"마동석", "코드30123"]
    # # 영화인 출연
    # movie_appearance = [movie_code, mpeople_code , " ~~역 (role)"] # 얘로 appearance테이블 생성
    # # 영화인 - 출연 - 명대사 
    # quote = [mpeople_code,movie_code, "명대사 내용", 300] # 300은 추천수
    # # 영화인 - 출연 - 역할 
    # casting = [mpeople_code,movie_code, "배역 이름 ex) 감독 주연 기획 제작 조연 등등"]


    # # 연관영화
    # relate_movie_code = 1112 # 연관영화의 코드를 크롤링한다.
    # relate_movie = [movie_code, relate_movie_code]

    # # 한줄평 [ autoincrement, moviecode, 평점, 코멘트내용,기자인지 관람객인지 네티즌인지, 작성시간, 추천, 비추천]
    # comment = [movie_code,5,"한줄평내용", "네티즌", "2021년12월23일 16시45분",300,28]

    # # 평점
    # score = [movie_code, 9.4, "네티즌", 328]

    # # 리뷰
    # review_id = 1 # 0부터 1씩 증가하는 리뷰id를 우리가 직접 넣어준다. 
    # # 450 = 조회수
    # review = [review_id, movie_code, "리뷰 제목", 450 , 300 , 28 , "2022년06월10일", "작성자"]
    # # 리뷰의 댓글
    # review_comment = [review_id, movie_code, "작성자", 300 , 28, "답글내용", "2022년6월12일"]


    
    # commit(a,genre,movie_index)


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

