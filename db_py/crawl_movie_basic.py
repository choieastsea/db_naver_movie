from dataclasses import dataclass
from unicodedata import name
import pymysql
import requests
from bs4 import BeautifulSoup

# 주요정보 탭
def get_basic(code):
    url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code='+str(code)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    # 줄거리
    story = "" 
    element = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > h5')
    if(len(element)!=0):
        story += element[0].text
        story += "\n"
    element = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
    if(len(element)!=0):
        story += element[0].text
    # print(story)
    
    # 제작노트
    makingnote=""
    element = soup.select('#makingnotePhase')
    if(len(element)!=0):
        makingnote +=element[0].text
    # print(makingnote)

    return [story,makingnote]

# 배우
def get_actor(code) :
    url = 'https://movie.naver.com/movie/bi/mi/detail.naver?code='+str(code)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    actor_arr = []
    subactor_arr = []
    #배우
    element = soup.select('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')
    # # print(element)
    for act in element:
        actor = []

        #배우 사진
        ele_thumnail = act.select('.p_thumb > a > img')
        if(len(ele_thumnail[0]['src'])>0):
            thumbnail = ele_thumnail[0]['src']
        else:
            thumbnail = None
        actor.append(thumbnail)
        # print(thumbnail)

        #배우 code
        ele_infourl = act.select('.p_thumb > a')
        if(len(ele_infourl[0].text)>0):
            infourl = ele_infourl[0]['href'].split('=')[1]
        else:
            infourl = None
        actor.append(infourl)
        # print(infourl)

        # 배우 이름
        ele_name = act.select('.p_info > a')
        if(len(ele_name[0].text)>0):
            name = ele_name[0].text
        else:
            name = None
        actor.append(name)

        # print(name)

        #배우 영어이름
        ele_ename = act.select('.p_info > em.e_name')
        if(len(ele_ename[0].text)>0):
            ename = ele_ename[0].text
        else:
            ename = None
        actor.append(ename)
        
        # print(ename)

        #배우 조연/주연
        ele_part = act.select('.p_info > .part em.p_part')
        if(len(ele_part[0].text)>0):
            part = ele_part[0].text
        else:
            part = None
        actor.append(part)

        # print(part)

        #배역 (...역)
        ele_part2 = act.select('.p_info > .part p.pe_cmt > span')
        if(len(ele_part2)>0):
            part2 = ele_part2[0].text
        else:
            part2 = None
        actor.append(part2)

        # print(part2)
        career_arr =[]
        ele_movie = act.select('.mv_product > li > a')
        for i in range(len(ele_movie)):
            #출연 영화
            if(len(ele_movie[i].text)>0):
                movie = ele_movie[i].text
            else:
                movie = None
            # print(movie)

            #출연 영화 개붕년도
            ele_year = act.select('.mv_product > li > span')
            if(len(ele_year[i].text)>0):
                year = ele_year[i].text
            else:
                year = None
            # print(year)

            career = [movie,year]
            career_arr.append(career)
        actor.append(career_arr)

        actor_arr.append(actor)

    # 단역
    sub_actor = soup.select('#subActorList span')
    for sub in sub_actor:
        subactor = []

        #단역들 이름
        e_name = sub.select('a')

        if(len(e_name[0].text)>0):
            e_namea = e_name[0].text
            e_namecode = e_name[0]['href'].split('=')[1] #단역들 코드
        else:
            e_namea = None
            e_namecode = None
        # print(e_namea)
        # print(e_namecode)
        subactor.append(e_namea)
        subactor.append(e_namecode)


        # 단역들 배역 이름
        em_name = sub.select('em')
        if(len(em_name[0].text)>0):
            e_nameb = em_name[0].text
        else:
            e_nameb = None
        # print(e_nameb)
        subactor.append(e_nameb)

        subactor_arr.append(subactor)

    return [actor_arr,subactor_arr]
        
# 감독
def get_director(code):
    url = 'https://movie.naver.com/movie/bi/mi/detail.naver?code='+str(code)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    producer = soup.select('div.dir_obj')
    director_arr = []
    
    for pr in producer:
        # 감독 썸네일
        director = []
        thumbnail = pr.select('p.thumb_dir > a > img')
        if(len(thumbnail)>0):
            img = thumbnail[0]['src']
        else:
            img = None
        # print(img)
        director.append(img)

        #감독정보 code
        url = pr.select('p.thumb_dir > a')
        
        if(len(url)>0):
            info_url = url[0]['href'].split('code=')[1]
        else:
            info_url = None
        # print(info_url)
        director.append(info_url)

        #감독 이름
        dir_name = pr.select('div.dir_product > a')
        if(len(dir_name)>0):
            name=dir_name[0].text
        else:
            name = None
        # print(name)
        director.append(name)
        #감독 영어이름
        dir_ename = pr.select('em.e_name')
        ename=dir_ename[0].text
        if len(ename)==0 :
            ename = None
        # print(ename)
        director.append(ename)
        #다른작품
        other_list = pr.select('.other_mv_group ul.other_list li')
        for other in other_list:
            #영화 이름
            o_title = other.select('.other_mv > a')
            title = o_title[0].text
            # print(title)

            #역할
            arr = []
            o_does = other.select('.other_mv > p')
            does = o_does[0].text
            does=does.replace('\t','').replace('\r','').replace('\n','')
            arr = does.split(",")
            # print(arr)

            #제작년도
            o_year = other.select('.made_since > dt')
            if(len(o_year)>0):
                year = o_year[0].text
            else:
                year = None
            # print(year)

            #제작국가
            o_country = other.select('.made_since > dd')
            if(len(o_country)>0):
                country = o_country[0].text.replace('\t','').replace('\r','').replace('\n','')
            else:
                country = None
            # print(country)

        director_arr.append(director)
    return director_arr

# 제작진
def get_producer(code):
    url = 'https://movie.naver.com/movie/bi/mi/detail.naver?code='+ str(code)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")

    staff = soup.select('div.staff tr')
    # print(staff)
    staff_arr = []
    for st in staff:
        producer_staff = []
        span = st.select('span')
        # print(st)
        for sp in span :
            #정보 code
            
            url =  sp.select('a')
            if(len(url)>0):
                str_url = url[0]['href'].split('code=')[1]
            else:
                str_url = None
            producer_staff.append(str_url)
            
            # 영어이름 , 담당
            ename = sp.select('em')
            ename_s = ename[0].text
            part_s = ename[1].text
            if(len(ename_s)==0):
                ename_s=None
            # print(ename_s)
            # print(part_s)
            producer_staff.append(ename_s)
            producer_staff.append(part_s)


            tmp=""
            if(ename_s == None) : 
                tmp = ""
            # 이름
            name = sp.select('a')
            if(len(name)>0):
                name_s = name[0].text
            else:
                name_s = sp.text.replace(tmp,'').replace(part_s,'').replace('\t','').replace('\r','').replace('\n','')
            # # print(name_s)
            producer_staff.append(name_s)
            # print(producer_staff)

            staff_arr.append([str_url,ename_s,part_s,name_s])

   # print(staff_arr)
    return staff_arr

# 제작/수입/배급사
def get_company(code):
    url = 'https://movie.naver.com/movie/bi/mi/detail.naver?code='+str(code)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml") 

    company = soup.select('#content > div.article > div:nth-child(7) > div:nth-child(2) > div > dl')
    # # print(company)
    com_arr=[]
    for com in company:
        a = com.select('dd')
        b = com.select('dt > em')
        com1 = []

        for i in range(len(a)) :
            company_role =b[i].text.strip()
            company_name = a[i].text.strip()
            # print(company_role)
            # print(company_name)
            com1.append(company_role)
            com1.append(company_name)
        com_arr.append(com1)
    return com_arr

        
def get_relate(code):
    
    url = 'https://movie.naver.com/movie/bi/mi/scriptAndRelate.naver?code='+str(code)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml") 
    ret =[]
    relate_movie = soup.select('#content > div.article > div:nth-child(7) > div > div > ul > li > h5 > a')
    for relate in relate_movie:
        ret.append(relate['href'].split('code=')[1])
    # print(ret)
    return ret

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
    url1 = 192608

    get_producer(url1)
