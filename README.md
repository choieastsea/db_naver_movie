# db_naver_movie
Crawling Naver Movie and Make Web Service with python, js

## 개발 환경
- python 3.x
    - virtual env 이용(/venv로 만들것!) source venv/bin/activate(mac)으로 진입하여 세팅하도록 한다.
    - db_py/init_db.py 를 만들어서 아래와 같이 해주자.
    ```python
    import pymysql

    def open_db():
        conn = pymysql.connect(
            host="localhost",
            user="user_name",
            password="password",
            db="movie_db",
            unix_socket="/tmp/mysql.sock",
        )
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cur


    def close_db(conn, cur):
        cur.close()
        conn.close()

    ```
    - libs : pymysql, requests, bs4, lxml
