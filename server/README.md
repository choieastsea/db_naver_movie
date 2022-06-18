# REST API 정리 문서

거의 모든 REST Api가 MySQL과의 연동을 필요로 하므로, 정리하여 관리하도록 한다.

## 1. 영화 페이지에서 필요한 api

- api/movie/basic?code={movie_code}

  - 영화 페이지 첫 화면 구성 위한 주요정보(모든 정보 요약본) 제공

    - 윗부분 : 제목, 영어 제목, 개봉일자, 현재 상영 여부, 관람객/네티즌/평론가 평점, 장르, 국가, 러닝타임, 감독, 출연 요약, 국내등급, 해외등급, 누적관객, 성별/나이대별 관람추이
    - 아랫부분(주요정보) : 줄거리, 제작노트, 배우/제작진 (6명), 포토 1개(+슬라이드), 동영상 4개, 한줄평 공감순 5개, 명대사 3개, 관련영화 5개, aka

    ```sql
    select * from movie;
    ```

  - return 

    ```json
    {
    
    }
    ```

- api/movie/review?code={movie_code}&page={page_no}

  - 영화 페이지 리뷰 탭 정보 제공. (추천순으로 제공)

    - 총 리뷰 갯수, 페이지에 해당하는 리뷰들 (최대 10개) 요약정보(제목, 앞부분, 작성자, 작성일, 추천수)

    - https://hackerwins.github.io/2019-05-24/db-pagination 페이지네이션 sql 성능 개선...

    - offset_key = page_no*10

    - ```sql
      SELECT * FROM review WHERE rid > {offset_key} LIMIT 10;
      ```

- api/movie/review?code={movie_code}&user={user_code}

  - 영화 페이지 리뷰 페이지 제공

- api/movie/rate?code={movie_code}&page={page_no}

  - 영화 평점 탭 정보 제공, 데이터의 양이 매우 많을 수 있음...

## 2. 사람 페이지에서 필요한 api

- api/person/filmography?code={person_code}

  - 필모그래피 정보

    ```sql
    select c.역할, m.movie_name, m.movie_code, m.year, 등
    from people p, casting c, movie m 
    where p.pid = c.pid 
    and m.mid = c.mid
    and p.pid = "123456";
    ```

    

  

## 3. 인트로(검색) 페이지에서 필요한 api

- api/start

  - 영화이름, 사람이름 사용자 문자열로 시작하는 것 검색

    ```sql
    select * from movie where movie_name like "{str}%" limit 5;
    select * from mpeople where people_name like "{str}%" limit 5;
    ```

- api/search

  - 영화/사람 검색하기

## 4. 검색 결과 페이지에서 필요한 api

- api/start
- api/search
- 