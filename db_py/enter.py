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
            # print('code is '+at['href'].split('=')[1] + '\n')
            addr.append(at['href'].split('=')[1])

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
            i = 4+i


    return addr




if __name__ == '__main__':
    get_url()


