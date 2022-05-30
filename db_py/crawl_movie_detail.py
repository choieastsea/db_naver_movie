import pymysql
import requests
from bs4 import BeautifulSoup

def get_data_from_movie_url(url):
    """
    naver movie url에서 데이터를 크롤링한다.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        title_raw = soup.select("#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)")
        watcher_rate_raw = soup.select("#actualPointPersentBasic > div > span > span")
        critic_rate_raw = soup.select("#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > div > em")
        netizen_rate_raw = soup.select("#pointNetizenPersentBasic > em")
        movie_intro_raw = soup.select("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1)>a")
        print(movie_intro_raw)
        
        
        
        title = str(title_raw[0].text) if len(title_raw) != 0 else None
        
        watcher_rate = float(watcher_rate_raw[0].text.split('점')[1].strip()) if len(watcher_rate_raw) != 0 else None
        
        critic_rate = ""
        for em in critic_rate_raw:
            critic_rate += em.text
        critic_rate = float(critic_rate) if critic_rate != "" else None
        
        netizen_rate = ""
        for em in netizen_rate_raw:
            netizen_rate += em.text
        netizen_rate = float(netizen_rate) if netizen_rate != "" else None
        
        
        print(netizen_rate)

    else:
        return -1

if __name__ == "__main__":
    url = "https://movie.naver.com/movie/bi/mi/basic.naver?code=192608"
    get_data_from_movie_url(url)
