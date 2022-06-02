from dataclasses import dataclass
from unicodedata import name
import pymysql
import requests
from bs4 import BeautifulSoup

# 주요정보 탭
def get_basic(basictab_url):
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

    return [story,makingnote]

# 배우
def get_actor(actortab_url) :
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

        


    # 단역
    sub_actor = soup.select('#subActorList span')
    for sub in sub_actor:
        #단역들 이름
        e_name = sub.select('a')

        if(len(e_name[0].text)>0):
            e_namea = e_name[0].text
        else:
            e_namea = None
        print(e_namea)

        # 단역들 배역 이름
        em_name = sub.select('em')
        if(len(em_name[0].text)>0):
            e_namea = em_name[0].text
        else:
            e_namea = None
        print(e_namea)
        
# 감독
def get_director(actortab_url):
    url="https://movie.naver.com/movie/bi/mi/detail.naver?code=204138"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    producer = soup.select('div.dir_obj')

    for pr in producer:
        # 감독 썸네일
        thumbnail = pr.select('p.thumb_dir > a > img')
        if(len(thumbnail)>0):
            img = thumbnail[0]['src']
        else:
            img = None
        print(img)

        #감독정보 url
        url = pr.select('p.thumb_dir > a')
        info_url="https://movie.naver.com"
        if(len(url)>0):
            info_url += url[0]['href']
        else:
            info_url = None
        print(info_url)

        #감독 이름
        dir_name = pr.select('div.dir_product > a')
        if(len(dir_name)>0):
            name=dir_name[0].text
        else:
            name = None
        print(name)

        #감독 영어이름
        dir_ename = pr.select('em.e_name')
        ename=dir_ename[0].text
        if len(ename)==0 :
            ename = None
        print(ename)

        #다른작품
        other_list = pr.select('.other_mv_group ul.other_list li')
        for other in other_list:
            #영화 이름
            o_title = other.select('.other_mv > a')
            title = o_title[0].text
            print(title)

            #역할
            arr = []
            o_does = other.select('.other_mv > p')
            does = o_does[0].text
            does=does.replace('\t','').replace('\r','').replace('\n','')
            arr = does.split(",")
            print(arr)

            #제작년도
            o_year = other.select('.made_since > dt')
            if(len(o_year)>0):
                year = o_year[0].text
            else:
                year = None
            print(year)

            #제작국가
            o_country = other.select('.made_since > dd')
            if(len(o_country)>0):
                country = o_country[0].text.replace('\t','').replace('\r','').replace('\n','')
            else:
                country = None
            print(country)

# 제작진
def get_producer(actortab_url):
    url="https://movie.naver.com/movie/bi/mi/detail.naver?code=204138"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    staff = soup.select('div.staff tr')

    for st in staff:
        span = st.select('span')
        for sp in span :
            #정보 url
            str_url = "https://movie.naver.com"
            url =  sp.select('a')
            if(len(url)>0):
                str_url += url[0]['href']
            else:
                str_url = None
            print(str_url)

            

            # 영어이름 , 담당
            ename = sp.select('em')
            ename_s = ename[0].text
            part_s = ename[1].text
            if(len(ename_s)==0):
                ename_s=None
            print(ename_s)
            print(part_s)


            tmp=""
            if(ename_s == None) : 
                tmp = ""
            # 이름
            name = sp.select('a')
            if(len(name)>0):
                name_s = name[0].text
            else:
                name_s = sp.text.replace(tmp,'').replace(part_s,'').replace('\t','').replace('\r','').replace('\n','')
            print(name_s)


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
    get_producer(0)
