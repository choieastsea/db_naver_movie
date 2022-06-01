import pymysql
import requests
from bs4 import BeautifulSoup
from init_db import open_db

def get_data_from_movie_url(url):
    """
    naver movie url에서 데이터를 크롤링한다.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        title_raw = soup.select("#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)")
        title_eng_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > h3 > strong")
        img_src_raw = soup.select("#content > div.article > div.wide_info_area > div.poster > a > img")
        movie_intro_raw = soup.select("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1)>a")
        movie_country_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(2) > a")
        running_time_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(3)")
        opening_date_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(4)>a")
        domestic_age_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(5)>a:nth-child(1)")
        foreign_age_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(5) > a:nth-child(2)")
        cumulative_audience_raw = soup.select("#content > div.article > div.wide_info_area > div.mv_info > p > span.count")
        # male_ratio_raw = soup.select("#actualGenderGraph_wide") -> 안가져와짐
        age_10s_ratio_raw = soup.select("#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(1) > strong.graph_percent")
        age_20s_ratio_raw = soup.select("#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(2) > strong.graph_percent")
        age_30s_ratio_raw = soup.select("#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(3) > strong.graph_percent")
        age_40s_ratio_raw = soup.select("#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(4) > strong.graph_percent")
        age_50s_ratio_raw = soup.select("#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(5) > strong.graph_percent")
        

        title = str(title_raw[0].text) if len(title_raw) != 0 else None
        title_eng = str(title_eng_raw[0].text.split('\n')[0].strip()) if len(title_eng_raw) !=0 else None
        img_src = img_src_raw[0]["src"] if len(img_src_raw) !=0 else None
        movie_intro = []
        for em in movie_intro_raw:
            movie_intro.append(em.text)
        movie_intro = movie_intro if len(movie_intro) != 0 else None
        movie_country = movie_country_raw[0].text if len(movie_country_raw) !=0 else None
        running_time = int(running_time_raw[0].text.strip()[:-1]) if len(running_time_raw) !=0 else None
        opening_date = ''
        for em in opening_date_raw:
            opening_date += em.text
        opening_date = opening_date if len(opening_date) !=0 else None
        domestic_age = domestic_age_raw[0].text if len(domestic_age_raw) !=0 else None
        foreign_age = foreign_age_raw[0].text if len(foreign_age_raw) !=0 else None
        cumulative_audience = int(cumulative_audience_raw[0].text.replace(",","").split("명")[0]) if len(cumulative_audience_raw) !=0 else None
        # male_ratio = int(male_ratio_raw[0].text.strip().replace("%","")) if len(male_ratio_raw) != 0 else None
        age_10s_ratio = int(age_10s_ratio_raw[0].text.replace("%","")) if len(age_10s_ratio_raw) !=0 else None
        age_20s_ratio = int(age_20s_ratio_raw[0].text.replace("%","")) if len(age_20s_ratio_raw) !=0 else None
        age_30s_ratio = int(age_30s_ratio_raw[0].text.replace("%","")) if len(age_30s_ratio_raw) !=0 else None
        age_40s_ratio = int(age_40s_ratio_raw[0].text.replace("%","")) if len(age_40s_ratio_raw) !=0 else None
        age_50s_ratio = int(age_50s_ratio_raw[0].text.replace("%","")) if len(age_50s_ratio_raw) !=0 else None
        
        print(age_10s_ratio)
        return title

    else:
        print("access denied")
        return -1

def get_data_from_photo_url(url):
    """
    naver movie photo url에서 데이터를 크롤링한다.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        photo_url_list = []
        photo_list = soup.select("#photo_area > div > div.list_area._list_area > div > ul > li")
        for photo in photo_list:
            photo_url_list.append(photo.select("a > img")[0]["src"])
    else:
        print("access denied")
        return -1
    print(photo_url_list)

def get_data_from_video_url(url):
    """
    naver movie video url에서 데이터를 크롤링한다.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        video_data_list = []
        video_section_list = soup.select("#content > div.article > div.obj_section2.noline > div > div.ifr_module > div")
        for video_section in video_section_list:
            video_list = video_section.select("ul.video_thumb>li")
            for video in video_list:
                link = f'movie.naver.com/{video.select("a")[0]["href"]}'
                thumbnail_img_src = video.select("img")[0]["src"]
                title = video.select("img")[0]["alt"]
                video_date = video.select("p.video_date")[0].text
                print(f'{title}\n{thumbnail_img_src}\n{link}\n{video_date}\n===================')
                # video_data_list.append(video)
    else:
        print("permission denied")
        return -1


def get_data_from_rate_url(url):
    """
    naver movie 평점 url에서 데이터를 크롤링한다.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        netizen_rate_raw = soup.select("#netizen_point_tab_inner>em")
        netizen_cnt_raw = soup.select("#graph_area > div.grade_netizen > div.title_area.grade_tit > div.sc_area > span > em")
        watcher_rate_raw = soup.select("#actual_point_tab_inner > div > em")
        watcher_cnt_raw = soup.select("#actual_point_tab_inner > span > em")
        critic_rate_raw = soup.select("#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.title_area > div > em")
        critic_cnt_raw = soup.select("#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.title_area > span > em")
        
        critic_detail_raw = soup.select("#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.reporter > ul > li")
        critic_2_detail_raw = soup.select("#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.score140 > div > ul > li")
        print(len(critic_2_detail_raw))
        
        male_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_gender > div:nth-child(1) > div > strong.graph_point")
        female_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_gender > div:nth-child(2) > div > strong.graph_point")
        
        
        netizen_rate = ""
        for em in netizen_rate_raw:
            netizen_rate += em.text
        netizen_rate = float(netizen_rate) if len(netizen_rate) != 0 else None
        netizen_cnt = int(netizen_cnt_raw[0].text.replace(",","")) if len(netizen_cnt_raw) !=0 else None
        watcher_rate = ""
        for em in watcher_rate_raw:
            watcher_rate += em.text
        watcher_rate = float(watcher_rate) if len(watcher_rate) != 0 else None
        watcher_cnt = int(watcher_cnt_raw[0].text.replace(",","")) if len(watcher_cnt_raw) !=0 else None
        critic_rate = ""
        for em in critic_rate_raw:
            critic_rate += em.text
        critic_rate = float(critic_rate) if len(critic_rate) != 0 else None
        critic_cnt = int(critic_cnt_raw[0].text.replace(",","")) if len(critic_cnt_raw) !=0 else None

        critic_detail = []
        for el in critic_detail_raw:
            critic_name = el.select("div.reporter_line > dl.p_review > dt > a")[0].text
            critic_title = el.select("div.reporter_line > dl.p_review > dd")[0].text
            critic_rate = el.select("div.re_score_grp > div.reporter_score > div.star_score > em")[0].text
            critic_content = el.select("p.tx_report")[0].text
            # print(critic_name,critic_title, critic_rate)
            # print(critic_content)
            # print("===================")
        for el in critic_2_detail_raw:
            critic_name = el.select("div.score_reple > dl > dd")[0].text.replace("|","").strip()
            critic_title = el.select("div.score_reple > p")[0].text
            critic_rate = el.select("div.star_score > em")[0].text
            print(critic_name,critic_title, critic_rate)
        male_rate = float(male_rate_raw[0].text) if len(male_rate_raw) !=0 else None 
        female_rate = float(female_rate_raw[0].text) if len(female_rate_raw) !=0 else None 


    else:
        print("permission denied")
        return -1


def insertTitle(title,conn,cur) : 
    sql ="""insert into movie (title) 
        values (%s);"""
    # print(title)
    cur.execute(sql, title)
    conn.commit()
    cur.close()
    conn.close()



if __name__ == "__main__":
    url1 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=192608"
    url2 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=17149"
    urlPhoto = "https://movie.naver.com/movie/bi/mi/photoView.naver?code=192608"
    [conn,cur] = open_db()
    # get_data_from_movie_url(url2)
    # get_data_from_photo_url(url1.replace("basic","photoView"))
    # get_data_from_video_url(url1.replace("basic","media"))
    # get_data_from_rate_url(url1.replace("basic","point"))
    # insertTitle(get_data_from_movie_url(url),conn,cur)

