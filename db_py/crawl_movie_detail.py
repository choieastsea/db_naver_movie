from ast import AsyncFunctionDef
import pymysql
import requests
import re
from bs4 import BeautifulSoup
from init_db import open_db

NETIZEN = 1
VIEWER = 2
CRITIC = 3


def get_viewing_trend_data(code):
    url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # male_ratio_raw = soup.select("#actualGenderGraph_wide") -> 안가져와짐
        age_10s_ratio_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(1) > strong.graph_percent")
        age_20s_ratio_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(2) > strong.graph_percent")
        age_30s_ratio_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(3) > strong.graph_percent")
        age_40s_ratio_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(4) > strong.graph_percent")
        age_50s_ratio_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.viewing_graph > div > div.bar_graph > div:nth-child(5) > strong.graph_percent")

        # male_ratio = int(male_ratio_raw[0].text.strip().replace("%","")) if len(male_ratio_raw) != 0 else None
        # 성별 관람 추이는 크롤링 안됨...
        # 10대 비율
        age_10s_ratio = int(age_10s_ratio_raw[0].text.replace(
            "%", "")) if len(age_10s_ratio_raw) != 0 else None
        # 20대 비율
        age_20s_ratio = int(age_20s_ratio_raw[0].text.replace(
            "%", "")) if len(age_20s_ratio_raw) != 0 else None
        # 30대 비율
        age_30s_ratio = int(age_30s_ratio_raw[0].text.replace(
            "%", "")) if len(age_30s_ratio_raw) != 0 else None
        # 40대 비율
        age_40s_ratio = int(age_40s_ratio_raw[0].text.replace(
            "%", "")) if len(age_40s_ratio_raw) != 0 else None
        # 50대 비율
        age_50s_ratio = int(age_50s_ratio_raw[0].text.replace(
            "%", "")) if len(age_50s_ratio_raw) != 0 else None
    else:
        # print(f"access denied on get_viewing_trend_data, url : {url}")
        return None
    return [age_10s_ratio, age_20s_ratio, age_30s_ratio, age_40s_ratio, age_50s_ratio]


def get_moie_data(code):
    """
    naver movie url에서 데이터를 크롤링한다.
    """
    url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        is_running_raw = soup.select(
            "#content > div.article > div.mv_info_area > div.mv_info > h3 > a.opening > em")
        title_raw = soup.select(
            "#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)")
        title_eng_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > h3 > strong")
        img_src_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.poster > a > img")
        movie_intro_raw = soup.select(
            "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a")
        movie_country_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(2) > a")
        running_time_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(3)")
        opening_date_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(4)>a")
        domestic_age_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(5)>a:nth-child(1)")
        foreign_age_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > p > span:nth-child(5) > a:nth-child(2)")
        cumulative_audience_raw = soup.select(
            "#content > div.article > div.wide_info_area > div.mv_info > p > span.count")

        aka_raw = soup.select(
            "#content > div.article > div:nth-child(7) > div:nth-child(3) > div > div.aka_info > p")

        # 영화 코드
        movie_code = url.split("code=")[1]
        # 상영중 여부
        is_running = True if len(is_running_raw) != 0 else False
        # 한국어 제목
        title = str(title_raw[0].text) if len(title_raw) != 0 else None
        print(title)
        # 영어 제목
        title_eng = str(title_eng_raw[0].text.split(
            '\n')[0].strip()) if len(title_eng_raw) != 0 else None
        # 영화 포스터 이미지 url
        img_src = img_src_raw[0]["src"] if len(img_src_raw) != 0 else None
        # 영화 장르 (문자열 배열)
        movie_intro = []
        for em in movie_intro_raw:
            movie_intro.append(em.text.strip())
        movie_intro = movie_intro if len(movie_intro) != 0 else None
        # 제작 국가
        movie_country = movie_country_raw[0].text if len(
            movie_country_raw) != 0 else None
        # 영화 시간
        running_time = 0
        if len(running_time_raw)>0:
            running_time = int(re.sub(r'[^0-9]', '', running_time_raw[0].text.strip()[:-1])) if len(re.sub(r'[^0-9]', '', running_time_raw[0].text.strip()[:-1])) != 0 else None
        # 영화 개봉일 -> 아마 이대로 db 저장해도 될듯?
        opening_date = ''
        for em in opening_date_raw:
            opening_date += em.text
        opening_date = opening_date if len(opening_date) != 0 else None
        # 국내 등급
        domestic_age = domestic_age_raw[0].text if len(
            domestic_age_raw) != 0 else None
        # 해외 등급
        foreign_age = foreign_age_raw[0].text if len(
            foreign_age_raw) != 0 else None
        # 누적관객수
        cumulative_audience = int(cumulative_audience_raw[0].text.replace(
            ",", "").split("명")[0]) if len(cumulative_audience_raw) != 0 else None

        # aka
        aka = aka_raw[0].text.strip() if len(aka_raw) != 0 else None
        # print(movie_intro)
        return [movie_code, is_running, title, title_eng, img_src, movie_intro, movie_country, running_time, opening_date, domestic_age, foreign_age, cumulative_audience, aka]

    else:
        # print("access denied")
        return None


def get_photo_data(code):
    """
    naver movie photo url에서 데이터를 크롤링한다.(일부만...)
    """
    # 영화 코드
    url = f"https://movie.naver.com/movie/bi/mi/photoView.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # 영화 사진 url 배열
        photo_url_list = []
        photo_list = soup.select(
            "#photo_area > div > div.list_area._list_area > div > ul > li")
        for photo in photo_list:
            photo_url_list.append(
                [code, photo.select("a > img")[0]["src"]])
    else:
        # print("access denied")
        return None
    return photo_url_list


def get_video_data(code):
    """
    naver movie video url에서 데이터를 크롤링한다.
    """
    url = f"https://movie.naver.com/movie/bi/mi/media.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # video 데이터 배열(비디오 링크, 썸네일, 제목, 업로드 날짜로 구성)
        video_data_list = []
        video_section_list = soup.select(
            "#content > div.article > div.obj_section2.noline > div > div.ifr_module > div")
        for video_section in video_section_list:
            video_list = video_section.select("ul.video_thumb>li")
            for video in video_list:
                # 비디오 링크
                link = f'movie.naver.com/{video.select("a")[0]["href"]}'
                # 비디오 썸네일 사진 링크
                thumbnail_img_src = video.select("img")[0]["src"]
                # 비디오 제목
                title = video.select("img")[0]["alt"]
                # 비디오 업로드 날짜
                video_date = video.select("p.video_date")[0].text
                # # print(f'{title}\n{thumbnail_img_src}\n{link}\n{video_date}\n===================')
                video_data_list.append(
                    [code, title, thumbnail_img_src, link, video_date])
    else:
        # print("permission denied")
        return None
    return video_data_list


def get_quotes_data(code):
    """
    명대사
    """
    url = f"https://movie.naver.com/movie/bi/mi/script.naver?code={code}&order=best&nid=&page="
    curpage = 1
    quote_list = []
    while True:
        # # print(f"request on page={curpage}")
        response = requests.get(f"{url}{curpage}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            daum = soup.select(f"#pagerTagAnchor{curpage+1} > em")
            # 한 페이지 내에서 해야할 일
            quotes = soup.select("#iframeDiv > ul > li")
            for quote in quotes:
                comment_raw = quote.select("div.lines_area2>p.one_line")
                character_raw = quote.select(
                    "div.lines_area2>p.char_part>span")
                actor_raw = quote.select("div.lines_area2>p.char_part>a")
                thumbnail_raw = quote.select("p.thumb>a>img")
                recommend_raw = quote.select(
                    "div.lines_area2>p.etc_lines>span>em")
                usesr_id_raw = quote.select(
                    "div.lines_area2>p.etc_lines>span>a")
                # 명대사
                comment = comment_raw[0].text if len(
                    comment_raw) != 0 else None
                # 명대사를 한 배역
                character = character_raw[0].text if len(
                    character_raw) != 0 else None
                # 배역의 배우 (코드)
                people_code = actor_raw[0]["href"].split(
                    "code=")[1] if len(actor_raw) != 0 else None
                # 썸네일(배우 이미지)
                thumbnal = thumbnail_raw[0]["src"] if len(
                    thumbnail_raw) != 0 else None
                # 추천수
                good = recommend_raw[0].text if len(
                    recommend_raw) != 0 else None
                # 추천 유저
                user_id = usesr_id_raw[0].text if len(
                    usesr_id_raw) != 0 else None
                # # print(f"{comment}\n{character}\n{actor}\n{thumbnal}")
                quote_list.append(
                    [code, people_code, comment, character, thumbnal, good, user_id])
            if len(daum) == 0:
                break
            curpage += 1
        else:
            # print(f"quotes permission denied in page {curpage}")
            return None
    # print(len(quote_list))
    return quote_list


def get_satisfying_netizen_data(code):
    url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        netizen_male_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_gender > div:nth-child(1) > div > strong.graph_point")
        netizen_female_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_gender > div:nth-child(2) > div > strong.graph_point")
        netiezen_age_10s_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_age > div.grp_box.high_percent > strong.graph_point")
        netiezen_age_20s_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(2) > strong.graph_point")
        netiezen_age_30s_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(3) > strong.graph_point")
        netiezen_age_40s_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(4) > strong.graph_point")
        netiezen_age_50s_rate_raw = soup.select(
            "#netizen_point_graph > div > div.grp_wrap > div.grp_age > div:nth-child(5) > strong.graph_point")
        # 네티즌 남성 만족도
        netizen_male_rate = float(netizen_male_rate_raw[0].text) if len(
            netizen_male_rate_raw) != 0 else None
        # 네티즌 여성 만족도
        netizen_female_rate = float(netizen_female_rate_raw[0].text) if len(
            netizen_female_rate_raw) != 0 else None
        # 네티즌 연령대별 만족도
        netiezen_age_10s_rate = float(netiezen_age_10s_rate_raw[0].text) if len(
            netiezen_age_10s_rate_raw) != 0 else None
        netiezen_age_20s_rate = float(netiezen_age_20s_rate_raw[0].text) if len(
            netiezen_age_20s_rate_raw) != 0 else None
        netiezen_age_30s_rate = float(netiezen_age_30s_rate_raw[0].text) if len(
            netiezen_age_30s_rate_raw) != 0 else None
        netiezen_age_40s_rate = float(netiezen_age_40s_rate_raw[0].text) if len(
            netiezen_age_40s_rate_raw) != 0 else None
        netiezen_age_50s_rate = float(netiezen_age_50s_rate_raw[0].text) if len(
            netiezen_age_50s_rate_raw) != 0 else None
        return [netizen_male_rate, netizen_female_rate, netiezen_age_10s_rate, netiezen_age_20s_rate, netiezen_age_30s_rate, netiezen_age_40s_rate, netiezen_age_50s_rate]
    else:
        # print(f"satisfying netizen data permission denied on url : {url}")
        return None


def get_satisfying_viewer_data(code):
    url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        watcher_male_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_gender > div:nth-child(1) > div > strong.graph_point")
        watcher_female_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_gender > div:nth-child(2) > div > strong.graph_point")
        watcher_age_10s_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_age > div.grp_box.high_percent > strong.graph_point")
        watcher_age_20s_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(2) > strong.graph_point")
        watcher_age_30s_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(3) > strong.graph_point")
        watcher_age_40s_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(4) > strong.graph_point")
        watcher_age_50s_rate_raw = soup.select(
            "#actual_point_graph > div.grp_wrap > div.grp_age > div:nth-child(5) > strong.graph_point")
        # viewer 만족도
        watcher_male_rate = float(watcher_male_rate_raw[0].text) if len(
            watcher_male_rate_raw) != 0 else None
        watcher_female_rate = float(watcher_female_rate_raw[0].text) if len(
            watcher_female_rate_raw) != 0 else None
        watcher_age_10s_rate = float(watcher_age_10s_rate_raw[0].text) if len(
            watcher_age_10s_rate_raw) != 0 else None
        watcher_age_20s_rate = float(watcher_age_20s_rate_raw[0].text) if len(
            watcher_age_20s_rate_raw) != 0 else None
        watcher_age_30s_rate = float(watcher_age_30s_rate_raw[0].text) if len(
            watcher_age_30s_rate_raw) != 0 else None
        watcher_age_40s_rate = float(watcher_age_40s_rate_raw[0].text) if len(
            watcher_age_40s_rate_raw) != 0 else None
        watcher_age_50s_rate = float(watcher_age_50s_rate_raw[0].text) if len(
            watcher_age_50s_rate_raw) != 0 else None
        return [watcher_male_rate, watcher_female_rate, watcher_age_10s_rate, watcher_age_20s_rate, watcher_age_30s_rate, watcher_age_40s_rate, watcher_age_50s_rate]
    else:
        # print(f"satisfying viewer data permission denied on url : {url}")
        return None


def get_enjoy_point_data(code):
    url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        netizen_point_raw_list = soup.select(
            "#netizen_point_graph > div > div.grp_sty4 > ul > li")
        watcher_point_raw_list = soup.select(
            "#actual_point_graph > div.grp_sty4 > ul > li")
        # 네티즌 관람 포인트
        ll = [NETIZEN]
        for netizen_point_raw in netizen_point_raw_list:
            ll.append({netizen_point_raw.select("strong")[
                      0].text: netizen_point_raw.select("span.grp_score")[0].text})
        # # print(ll)
        # 관람객 관람 포인트
        ll2 = [VIEWER]
        for watcher_point_raw in watcher_point_raw_list:
            ll2.append({watcher_point_raw.select("strong")[
                       0].text: watcher_point_raw.select("span.grp_score")[0].text})
        # # print(ll2)
        return ll.extend(ll2)  # 두 배열 합쳐서...
    else:
        # print(f"enjoy point data permission denied on url : {url}")
        return None


def get_score_data(code):
    """
    naver movie 총 평점 평균 데이터
    """
    url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={code}"
    score_list = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        netizen_rate_raw = soup.select("#netizen_point_tab_inner>em")
        netizen_cnt_raw = soup.select(
            "#graph_area > div.grade_netizen > div.title_area.grade_tit > div.sc_area > span > em")
        watcher_rate_raw = soup.select("#actual_point_tab_inner > div > em")
        watcher_cnt_raw = soup.select("#actual_point_tab_inner > span > em")

        critic_rate_raw = soup.select(
            "#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.title_area > div > em")
        critic_cnt_raw = soup.select(
            "#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.title_area > span > em")

        netizen_rate = ""
        for em in netizen_rate_raw:
            netizen_rate += em.text
        # 네티즌 평점
        netizen_rate = float(netizen_rate) if len(netizen_rate) != 0 else None
        # 네티즌 평점 참여 인원 수
        netizen_cnt = int(netizen_cnt_raw[0].text.replace(
            ",", "")) if len(netizen_cnt_raw) != 0 else None
        score_list.append([code, NETIZEN, netizen_rate, netizen_cnt])
        watcher_rate = ""
        for em in watcher_rate_raw:
            watcher_rate += em.text
        watcher_rate = float(watcher_rate) if len(watcher_rate) != 0 else None
        watcher_cnt = int(watcher_cnt_raw[0].text.replace(
            ",", "")) if len(watcher_cnt_raw) != 0 else None
        score_list.append([code, VIEWER, watcher_rate, watcher_cnt])

        critic_rate = ""
        for em in critic_rate_raw:
            critic_rate += em.text
        critic_rate = float(critic_rate) if len(critic_rate) != 0 else None
        critic_cnt = int(critic_cnt_raw[0].text.replace(
            ",", "")) if len(critic_cnt_raw) != 0 else None
        score_list.append([code, CRITIC, critic_rate, critic_cnt])

        return score_list
    else:
        # # print("rate permission denied")
        return None


def get_comment_data(code):
    """
    관람객, 네티즌, 평론가 한줄평(with 별점)
    """
    url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={code}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        rate_list = []
        # 평론가 평점
        critic_detail_raw = soup.select(
            "#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.reporter > ul > li")
        critic_2_detail_raw = soup.select(
            "#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.score140 > div > ul > li")
        for el in critic_detail_raw:
            critic_name = el.select(
                "div.reporter_line > dl.p_review > dt > a")[0].text
            critic_code = el.select("div.reporter_line > dl.p_review > dt > a")[
                0]["href"].split("code=")[1]
            critic_title = el.select(
                "div.reporter_line > dl.p_review > dd")[0].text
            critic_rate = el.select(
                "div.re_score_grp > div.reporter_score > div.star_score > em")[0].text
            critic_content = el.select("p.tx_report")[0].text
            # # print(critic_name,critic_code,critic_title, critic_rate)
            # # print(critic_content)
            # # print("===================")
            rate_list.append([CRITIC, critic_rate, critic_title, critic_name])
        for el in critic_2_detail_raw:
            critic_name = el.select("div.score_reple > dl > dd")[
                0].text.replace("|", "").strip()
            critic_title = el.select("div.score_reple > p")[0].text
            critic_rate = el.select("div.star_score > em")[0].text
            rate_list.append([CRITIC, critic_rate, critic_title, critic_name])

            # # print(critic_name,critic_title, critic_rate)

        # 네티즌. 관람객 평점
        iframe_url_raw = soup.select("#pointAfterListIframe")
        # # print(f'https://movie.naver.com{iframe_url_raw[0]["src"]}')
        curpage = 1
        if len(iframe_url_raw) > 0:
            while True:
                iframe_url = f'https://movie.naver.com{iframe_url_raw[0]["src"]}&page={curpage}'
                # # print(iframe_url)
                iframe_response = requests.get(iframe_url)
                if iframe_response.status_code == 200:
                    soup = BeautifulSoup(iframe_response.text, "lxml")
                    daum = soup.select(f"#pagerTagAnchor{curpage+1} > em")
                    major_watcher_review_list_raw = soup.select(
                        "body > div > div > div.score_result > ul > li")
                    # # print(len(major_watcher_review_list_raw))
                    for review in major_watcher_review_list_raw:
                        score_raw = review.select("div.star_score > em")
                        isWatcher_raw = review.select(
                            "div.score_reple > p > span.ico_viewer")
                        if len(isWatcher_raw) == 0:
                            # 관람객이 아닌 경우
                            review_content_raw = review.select(
                                "div.score_reple>p>span")
                        else:
                            # 관람객인 경우
                            review_content_raw = review.select(
                                "div.score_reple>p>span:nth-child(2)")
                        reviewer_raw = review.select(
                            "div.score_reple>dl>dt>em>a>span")
                        # 평점
                        score = score_raw[0].text if len(score_raw) != 0 else None
                        # 관람객 여부(bool)
                        isWatcher = True if len(isWatcher_raw) != 0 else False
                        # 한줄평 내용
                        review_content = review_content_raw[0].text.strip() if len(
                            review_content_raw) != 0 else None
                        # 작성자
                        reviewer = reviewer_raw[0].text if len(
                            reviewer_raw) != 0 else None
                        rate_list.append(
                            [VIEWER if isWatcher else NETIZEN, score, review_content, reviewer])
                        if len(rate_list) >=100:
                            return rate_list
                        # # print(f"평점 : {score} {'관람객' if isWatcher else '안본사람'} {review_content} \n by {reviewer}\n================")
                    if len(daum) == 0:
                        break
                    curpage += 1
                else:
                    print("iframe permission denied")
            # print(len(rate_list))
            return rate_list
        return None


def get_data_from_review_url(code):
    url = f"https://movie.naver.com/movie/bi/mi/review.naver?code={code}"
    review_data_list = []
    curpage = 1
    while True:
        # # print(f"request on page={curpage}")
        response = requests.get(f"{url}&page={curpage}")
        # # print(f"request to url {url}&page={curpage}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            daum = soup.select(f"#pagerTagAnchor{curpage+1} > em")
            # 한 페이지 내에서 해야할 일
            review_list = soup.select("#reviewTab > div > div > ul > li")
            # # print(review_list)
            for review in review_list:
                reviewer_code = review.select("a")[0]["onclick"].split(
                    "showReviewDetail(")[1][:-1]
                # # print(reviewer_code, code)
                response2 = requests.get(
                    f"https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={reviewer_code}&code={code}&order=#tab")
                if response2.status_code == 200:
                    soup2 = BeautifulSoup(response2.text, "lxml")
                    review_title_raw = soup2.select(
                        "#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior> strong.h_lst_tx")
                    review_score_raw = soup2.select(
                        "#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior> div.star_score> em")
                    review_date_raw = soup2.select(
                        "#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior> span.wrt_date")
                    writer_raw = soup2.select(
                        "#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > ul > li:nth-child(2) > a > em")
                    hits_raw = soup2.select(
                        "#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > div > span:nth-child(1) > em")
                    recommend_raw = soup2.select("#goodReviewCount")
                    review_content_raw = soup2.select(
                        "#content > div.article > div.obj_section.noline.center_obj > div.review > div.user_tx_area")
                    review_comment_raw = soup2.select(
                        "#cbox_module> div > div:nth-child(3) > ul > li")
                    # print(review_comment_raw)

                    # 리뷰 제목
                    review_title = review_title_raw[0].text if len(
                        review_title_raw) != 0 else None
                    # 리뷰 점수
                    review_score = review_score_raw[0].text if len(
                        review_score_raw) != 0 else None
                    if len(review_score_raw) == 2:
                        review_score = 10
                    # 리뷰 작성일
                    review_date = review_date_raw[0].text if len(
                        review_date_raw) != 0 else None
                    # 리뷰 작성자
                    review_writer = writer_raw[0].text if len(
                        writer_raw) != 0 else None
                    # 리뷰 조회수
                    hits = hits_raw[0].text if len(hits_raw) != 0 else None
                    # 리뷰 추천수
                    recommend = recommend_raw[0].text if len(
                        recommend_raw) != 0 else None
                    # 리뷰 내용
                    review_content = review_content_raw
                    # 리뷰 댓글 -> 안불러와짐!
                    review_comment_list = []
                    # for comment in review_comment_raw:
                    #     # print(comment.select(
                    #         "div>div>div.u_cbox_text_wrap>span").text)
                    #     # review_comment_list.append()
                    review_data_list.append([review_title, review_score, review_date,
                                            review_writer, hits, recommend, review_content, review_comment_list])
                    # # print(review_content_raw)
                else:
                    print(
                        f"reviews permission denied on url https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={reviewer_code}&code={code}&order=#tab")
            if len(daum) == 0:
                break
            curpage += 1

        else:
            # print(f"reviews permission denied in page {curpage}")
            return None
        return review_data_list

def insertTitle(title, conn, cur):
    sql = """insert into movie (title) 
        values (%s);"""
    # # print(title)
    cur.execute(sql, title)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    code = 192608
    code_test = 196854
    # 영화 페이지 기본 url
    url_mold = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
    url1 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=192608"
    url2 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=17149"
    url3 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=182016"
    # [conn,cur] = open_db()
    # a = get_data_from_review_url(196854)
    # print(a)
    # # print(get_photo_data(code))
    # print(get_score_data(code))