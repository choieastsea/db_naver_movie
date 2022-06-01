import pymysql
import requests
from bs4 import BeautifulSoup

def get_url():
    url="https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")
 
    element = soup.select('#old_content > table td a')
    # print(element)
    addr=[]

    flag = 0
    link=""
    i=0
    while i <len(element):
        print(i)
        
        if flag==0:
            link ="https://movie.naver.com/movie/sdb/browsing/"
            link += element[i]['href']
        print(link)    
        
        resp = requests.get(link)
        soup = BeautifulSoup(resp.text,"lxml")
        element2 = soup.select('#old_content > ul > li > a')
        element3 = soup.select('#old_content > div.pagenavigation > table td.next > a')
        # print(element2)
        for at in element2:
            # print(at['href'])
            addr.append(at['href'])
        print("다음 있음?",len(element3))
        if len(element3)>0 :
            flag = 1
            # print(element[i].index,"::",flag)
            link ="https://movie.naver.com"
            link += element3[0]['href']
            pass
            
        elif len(element3)>0 and flag == 1 :
            flag = 1
            # print(element[i].index,"::",flag)
            link ="https://movie.naver.com"
            link += element3[0]['href']
            pass
            
        else:
            flag = 0
            i = i+1
        

    print(len(addr))
    # for a in element :
    #     element3 = soup.select('#old_content > div.pagenavigation > table td.next > a')
    #     if flag==0:
    #         link ="https://movie.naver.com/movie/sdb/browsing/"
    #         link += a['href']
            
    #     resp = requests.get(link)
    #     soup = BeautifulSoup(resp.text,"lxml")
    #     element2 = soup.select('#old_content > ul > li > a')

    #     for at in element2:
    #         addr.append(at['href'])

    #     if(len(element3)>0) :
    #         flag = 1
    #         print(a.index,"::",flag)
    #         link ="https://movie.naver.com/movie/sdb/browsing/"
    #         link += element3[0]['href']
    #         continue
    #     else:
    #         flag = 0
   
    
        
        


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


