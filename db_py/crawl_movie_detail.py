from ast import AsyncFunctionDef
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
        is_running_raw = soup.select("#content > div.article > div.mv_info_area > div.mv_info > h3 > a.opening > em")
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
        
        aka_raw = soup.select("#content > div.article > div:nth-child(7) > div:nth-child(3) > div > div.aka_info > p")

        # db에 들어갈 타입으로 정리한 attrs
        movie_code = url.split("code=")[1]
        is_running = True if len(is_running_raw) !=0 else False
        title = str(title_raw[0].text) if len(title_raw) != 0 else None
        title_eng = str(title_eng_raw[0].text.split('\n')[0].strip()) if len(title_eng_raw) !=0 else None
        img_src = img_src_raw[0]["src"] if len(img_src_raw) !=0 else None
        movie_intro = []
        for em in movie_intro_raw:
            movie_intro.append(int(em['href'].split('=')[1]))
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
        aka = aka_raw[0].text.strip() if len(aka_raw) !=0 else None
        print(movie_intro)
        return movie_intro

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

def get_data_from_quotes_url(url):
    curpage = 1
    while True:
        # print(f"request on page={curpage}")
        response = requests.get(f"{url}{curpage}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            daum = soup.select(f"#pagerTagAnchor{curpage+1} > em")
            # 한 페이지 내에서 해야할 일
            quotes = soup.select("#iframeDiv > ul > li")
            for quote in quotes:
                comment_raw = quote.select("div.lines_area2>p.one_line")
                character_raw = quote.select("div.lines_area2>p.char_part>span")
                actor_raw = quote.select("div.lines_area2>p.char_part>a")
                thumbnail_raw = quote.select("p.thumb>a>img")
                comment = comment_raw[0].text if len(comment_raw) !=0  else None
                character = character_raw[0].text if len(character_raw) !=0 else None
                actor = actor_raw[0]["href"].split("code=")[1] if len(actor_raw) !=0 else None
                thumbnal = thumbnail_raw[0]["src"] if len(thumbnail_raw) !=0 else None
                print(f"{comment}\n{character}\n{actor}\n{thumbnal}")
            if len(daum) == 0:
                break
            curpage += 1

        else:
            print(f"quotes permission denied in page {curpage}")
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
        
        netizen_male_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_gender > div:nth-child(1) > div > strong.graph_point")
        netizen_female_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_gender > div:nth-child(2) > div > strong.graph_point")
        watcher_male_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_gender > div:nth-child(1) > div > strong.graph_point")
        watcher_female_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_gender > div:nth-child(2) > div > strong.graph_point")
        
        netiezen_age_10s_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_age > div.grp_box.high_percent > strong.graph_point")
        netiezen_age_20s_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(2) > strong.graph_point")
        netiezen_age_30s_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(3) > strong.graph_point")
        netiezen_age_40s_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(4) > strong.graph_point")
        netiezen_age_50s_rate_raw = soup.select("#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(5) > strong.graph_point")
        watcher_age_10s_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_age > div.grp_box.high_percent > strong.graph_point")
        watcher_age_20s_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(2) > strong.graph_point")
        watcher_age_30s_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(3) > strong.graph_point")
        watcher_age_40s_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(4) > strong.graph_point")
        watcher_age_50s_rate_raw = soup.select("#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(5) > strong.graph_point")

        netizen_point_raw_list = soup.select("#netizen_point_graph > div > div.grp_sty4 > ul > li")
        watcher_point_raw_list = soup.select("#actual_point_graph > div.grp_sty4 > ul > li")
        ll = []
        for netizen_point_raw in netizen_point_raw_list:
            ll.append({netizen_point_raw.select("strong")[0].text : netizen_point_raw.select("span.grp_score")[0].text})
        # print(ll)
        ll2 = []
        for watcher_point_raw in watcher_point_raw_list:
            ll2.append({watcher_point_raw.select("strong")[0].text : watcher_point_raw.select("span.grp_score")[0].text})
        # print(ll2)

        # 관람객 평점, 한줄평은 iframe 통해서 접근해야함..! 일단 1페이지만
        iframe_url_raw = soup.select("#pointAfterListIframe")
        print(f'https://movie.naver.com{iframe_url_raw[0]["src"]}')
        curpage = 1
        while True:
            iframe_url = f'https://movie.naver.com{iframe_url_raw[0]["src"]}&page={curpage}'
            print(iframe_url)
            iframe_response = requests.get(iframe_url)
            if iframe_response.status_code == 200:
                soup = BeautifulSoup(iframe_response.text, "lxml")
                daum = soup.select(f"#pagerTagAnchor{curpage+1} > em")

                major_watcher_review_list_raw = soup.select("body > div > div > div.score_result > ul > li")
                # print(len(major_watcher_review_list_raw))
                for review in major_watcher_review_list_raw:
                    score_raw = review.select("div.star_score > em")
                    isWatcher_raw = review.select("div.score_reple > p > span.ico_viewer")
                    if len(isWatcher_raw) == 0:
                        #관람객이 아닌 경우
                        review_content_raw = review.select("div.score_reple>p>span")
                    else:
                        #관람객인 경우
                        review_content_raw = review.select("div.score_reple>p>span:nth-child(2)")
                    reviewer_raw = review.select("div.score_reple>dl>dt>em>a>span")

                    score = score_raw[0].text if len(score_raw) !=0 else None
                    isWatcher = True if len(isWatcher_raw) !=0 else False
                    review_content = review_content_raw[0].text.strip() if len(review_content_raw) !=0 else None
                    reviewer = reviewer_raw[0].text if len(reviewer_raw) !=0 else None

                    print(f"평점 : {score} {'관람객' if isWatcher else '안본사람'} {review_content} \n by {reviewer}\n================")
                if len(daum) == 0:
                    break
                curpage += 1

            else:
                print("iframe permission denied")
        
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
            critic_code = el.select("div.reporter_line > dl.p_review > dt > a")[0]["href"].split("code=")[1]
            critic_title = el.select("div.reporter_line > dl.p_review > dd")[0].text
            critic_rate = el.select("div.re_score_grp > div.reporter_score > div.star_score > em")[0].text
            critic_content = el.select("p.tx_report")[0].text
            # print(critic_name,critic_code,critic_title, critic_rate)
            # print(critic_content)
            # print("===================")
        for el in critic_2_detail_raw:
            critic_name = el.select("div.score_reple > dl > dd")[0].text.replace("|","").strip()
            critic_title = el.select("div.score_reple > p")[0].text
            critic_rate = el.select("div.star_score > em")[0].text
            # print(critic_name,critic_title, critic_rate)
        netizen_male_rate = float(netizen_male_rate_raw[0].text) if len(netizen_male_rate_raw) !=0 else None 
        netizen_female_rate = float(netizen_female_rate_raw[0].text) if len(netizen_female_rate_raw) !=0 else None 
        watcher_male_rate = float(watcher_male_rate_raw[0].text) if len(watcher_male_rate_raw) !=0 else None
        watcher_female_rate = float(watcher_female_rate_raw[0].text) if len(watcher_female_rate_raw) !=0 else None
        netiezen_age_10s_rate = float(netiezen_age_10s_rate_raw[0].text) if len(netiezen_age_10s_rate_raw) !=0 else None
        netiezen_age_20s_rate = float(netiezen_age_20s_rate_raw[0].text) if len(netiezen_age_20s_rate_raw) !=0 else None
        netiezen_age_30s_rate = float(netiezen_age_30s_rate_raw[0].text) if len(netiezen_age_30s_rate_raw) !=0 else None
        netiezen_age_40s_rate = float(netiezen_age_40s_rate_raw[0].text) if len(netiezen_age_40s_rate_raw) !=0 else None
        netiezen_age_50s_rate = float(netiezen_age_50s_rate_raw[0].text) if len(netiezen_age_50s_rate_raw) !=0 else None
        watcher_age_10s_rate = float(watcher_age_10s_rate_raw[0].text) if len(watcher_age_10s_rate_raw) !=0 else None
        watcher_age_20s_rate = float(watcher_age_20s_rate_raw[0].text) if len(watcher_age_20s_rate_raw) !=0 else None
        watcher_age_30s_rate = float(watcher_age_30s_rate_raw[0].text) if len(watcher_age_30s_rate_raw) !=0 else None
        watcher_age_40s_rate = float(watcher_age_40s_rate_raw[0].text) if len(watcher_age_40s_rate_raw) !=0 else None
        watcher_age_50s_rate = float(watcher_age_50s_rate_raw[0].text) if len(watcher_age_50s_rate_raw) !=0 else None

        # print(watcher_age_50s_rate)
        # print(watcher_age_10s_rate)

    else:
        print("rate permission denied")
        return -1


def insertTitle(title,conn,cur) : 
    sql ="""insert into movie (title) 
        values (%s);"""
    # print(title)
    cur.execute(sql, title)
    conn.commit()
    cur.close()
    conn.close()


def get_data_from_review_url(url):
    movie_code = url.split('code=')[1]
    curpage = 1
    while True:
        # print(f"request on page={curpage}")
        response = requests.get(f"{url}&page={curpage}")
        print(f"request to url {url}&page={curpage}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            daum = soup.select(f"#pagerTagAnchor{curpage+1} > em")
            # 한 페이지 내에서 해야할 일
            review_list = soup.select("#reviewTab > div > div > ul > li")
            # print(review_list)
            for review in review_list:
                reviewer_code = review.select("a")[0]["onclick"].split("showReviewDetail(")[1][:-1]
                print(reviewer_code, movie_code)
                response = requests.get("https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={reviewer_code}&code={movie_code}&order=#tab")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "lxml")
                    review_title_raw = soup.select("#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior > strong")
                    review_title = review_title_raw[0].text if len(review_title_raw) !=0 else None
                    print(review_title)
                else:
                    print(f"reviews permission denied on url https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={reviewer_code}&code={movie_code}&order=#tab")    
            if len(daum) == 0:
                break
            curpage += 1

        else:
            print(f"reviews permission denied in page {curpage}")
            return -1


if __name__ == "__main__":
    url1 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=192608"
    url2 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=17149"
    url3 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=182016"
    urlPhoto = "https://movie.naver.com/movie/bi/mi/photoView.naver?code=192608"
    urlQuotes = "https://movie.naver.com/movie/bi/mi/script.naver?code=192608&order=best&nid=&page="    #페이지 1붙혀서 시작
    # [conn,cur] = open_db()
    # get_data_from_movie_url(url2)
    # get_data_from_photo_url(url1.replace("basic","photoView"))
    # get_data_from_video_url(url1.replace("basic","media"))
    # get_data_from_rate_url(url1.replace("basic","point"))
    get_data_from_review_url(url1.replace("basic","review"))
    # get_data_from_quotes_url(urlQuotes)
    # insertTitle(get_data_from_movie_url(url),conn,cur)

