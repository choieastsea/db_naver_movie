from dataclasses import dataclass
import pymysql
import requests
from bs4 import BeautifulSoup

# 주요정보 탭
def get_basic(basic_url):
    url="https://movie.naver.com/movie/bi/mi/basic.naver?code=192608"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    # 줄거리
    story = "" 
    element = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > h5')
    story += element[0].text
    story += "\n"
    element = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
    story += element[0].text
    print(story)
    
    # 제작노트
    makingnote=""
    element = soup.select('#makingnotePhase')
    makingnote +=element[0].text
    print(makingnote)

# 배우/제작진 탭
def get_actor(actor_url) :
    url="https://movie.naver.com/movie/bi/mi/detail.naver?code=192608"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    #배우
    actor = []
    
    element = soup.select('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')
    # print(element)
    for act in element:
        #배우 사진
        ele_thumnail = act.select('.p_thumb > a > img')
        thumbnail = ele_thumnail[0]['src']
        print(thumbnail)

        #배우 상세정보url
        ele_infourl = act.select('.p_thumb > a')
        infourl = ele_infourl[0]['href']
        print(infourl)

        # 배우 이름
        ele_name = act.select('.p_info > a')
        name = ele_name[0].text
        print(name)

        #배우 영어이름
        ele_ename = act.select('.p_info > em.e_name')
        if(len(ele_ename[0].text)>0):
            ename = ele_ename[0].text
        else:
            ename = None
        print(ename)

        #배우 조연/주연
        ele_part = act.select('.p_info > .part em.p_part')
        if(len(ele_part[0].text)>0):
            part = ele_part[0].text
        else:
            part = None
        print(part)

        #배역 (...역)
        ele_part2 = act.select('.p_info > .part p.pe_cmt > span')
        if(len(ele_part2[0].text)>0):
            part2 = ele_part2[0].text
        else:
            part2 = None
        print(part2)

        #출연 영화
        ele_movie = act.select('.mv_product > li > a')
        if(len(ele_movie[0].text)>0):
            movie = ele_movie[0].text
        else:
            movie = None
        print(movie)

        #출연 영화
        ele_year = act.select('.mv_product > li > span')
        if(len(ele_year[0].text)>0):
            year = ele_year[0].text
        else:
            year = None
        print(year)




@dataclass
class Actor:
    """Class for keeping track of an item in inventory."""
    info_url: str
    name: str
    name_eng: str
    actor_pic: str
    part : str # 주연/조연
    casting: str # ...역
    movie : str # 출연영화


if __name__ == '__main__':
    get_actor(0)
