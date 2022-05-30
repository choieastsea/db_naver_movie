from xml.dom.minidom import Element
import pymysql
import requests
from bs4 import BeautifulSoup

def get_url():
    url="https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")
 
    element = soup.select('#old_content > table td a')
    
    for a in element :
        link = a['href']
        print(link)
        
        


    # a =[]
    # for el in element:
    #     title = el.select('.tit > a')[0].text
    #     # print(f"{title},{el.select('.tit > span')}")
    #     movie_rate =""
    #     if len(el.select('.tit > span')) != 0 :
    #         movie_rate = el.select('.tit > span')[0].text 
    #         # print(movie_rate)
    #     else :
    #         movie_rate = None
    #     netizen_rate = float(el.select('.star_t1 .num')[0].text) if len(el.select('.star_t1 .num')) != 0 else None
    #     netizen_count = int(el.select('.star_t1 .num2 > em')[0].text.replace(",","")) if len(el.select('.star_t1 .num2 > em')) != 0 else None
        
    #     if len(el.select('.star_t1 .num')) != 1 :
    #         journalist_score = float(el.select('.star_t1 .num')[1].text) 
    #         journalist_count = int(el.select('.star_t1 .num2 > em')[1].text.replace(",",""))
    #     else : 
    #         journalist_score=None 
    #         journalist_count=None
        
    #     tmp = el.select('.info_txt1 > dd')[0].text 
    #     str = "".join(tmp.split()).split("|")
    #     scope = "".join(str[0].split()) if len("".join(str[0].split())) != 0 else None
    #     playing_time = "".join(str[1].split()) if len("".join(str[1].split())) != 0 else None
    #     opening_date = "".join(str[2].split()) if len("".join(str[2].split())) != 0 else None
    #     director = el.select('.info_txt1 .link_txt')[1].text.replace("\n","").replace("\t","").replace("\r","") if len("".join(el.select('.info_txt1 .link_txt')[1].text.split())) != 0 else None
    #     image = el.select('.thumb > a > img')[0].attrs['src'] if len(el.select('.thumb > a > img')[0].attrs['src']) != 0 else None
        
    #     a.append([title,movie_rate,netizen_rate,netizen_count,journalist_score,journalist_count,scope,playing_time,opening_date,director,image])
    # return a
       
def commit(a):
    conn = pymysql.connect(host='localhost', user='kkh',password='kkh', db='moviedb')
    curs = conn.cursor()
    sql ="""insert into movie (title, movie_rate, netizen_rate,netizen_count,journalist_score,journalist_count,scope,playing_time,opening_date,director,image) 
        values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    # print(a)
    curs.executemany(sql, a)
    conn.commit()
    curs.close()
    conn.close()

        


if __name__ == '__main__':
    get_url()


