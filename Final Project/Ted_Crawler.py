import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from enum import Enum
import os
import json
import words

class Endpoints:

    def __init__(self):

        # 預設為所有種類影片、6-12分鐘、熱門演講
        self.default_list = "/talks?sort=popular&duration=6-12"

        # 用戶選擇影片種類
        self.with_topics = "&topics%5B%5D="

        # 逐字稿
        self.transcript = "/transcript.json?language=en"

class Topics(Enum):

    # 可供選擇影片種類
    All = ""
    Technology = "Technology"
    Entertainment = "Entertainment"
    Design = "Design"
    Business = "Business"
    Science = "Science"
    Global_Issues = "Global+issues"

    @classmethod
    def getTopics(cls):
        """取得影片種類的list，elements皆是enum型別"""

        topics_list = [
            cls.All,
            cls.Technology,
            cls.Entertainment,
            cls.Business,
            cls.Design,
            cls.Science,
            cls.Global_Issues,
            ]

        return topics_list

class TedCrawler:

    # 生成爬蟲物件，同時定義base_url, headers
    def __init__(self):
        self.base_url = "https://www.ted.com"
        self.headers = {
            'user-agent': 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
            }

    def playlists_request(self, topic):
        """取得影片清單

        Parameters:
            topic: str, 用戶選擇影片種類
        """

        request_url = self.base_url + Endpoints().default_list

        if topic != "":
            request_url += Endpoints().with_topics
            request_url += topic

        #print("playlists_request: " + request_url)

        try:
            playlsits_page = requests.get(request_url, headers = self.headers).content
        except Exception as e:
            print("encounter error when request to playlsits page")
            print(e)

        soup = BeautifulSoup(playlsits_page, "html.parser")

        # 搜尋後可能會有多頁結果，這裏僅將第一頁的所有演講記錄下來
        content = soup.findAll(attrs = {"data-ga-context":"talks"})

        # lists為字典型別: key為演講主題，value為endoint參數，供接下來進入影片頁面使用
        lists = {}
        for i in range(len(content)):
            if i%2 != 0:
                uri = content[i]["href"]
                name = content[i].text.strip()
                lists[name] = uri
        return lists

    def vedio_page_request(self, vedio_endpoint):
        """進入影片頁面

        Parameters:
            vedio_endpoint: str, 用戶選擇的影片endpoint
        """

        request_url = self.base_url + vedio_endpoint
        #print("vedio_page_request: " + request_url)

        try:
            video_page = requests.get(request_url, headers = self.headers)
        except Exception as e:
            print("encounter error when request to video page")
            print(e)

        vedio_cont = video_page.content
        vedio_soup = BeautifulSoup(vedio_cont, "html.parser")

        # 我們所需資訊在第十個script位置，若網站更新可能會有所改變
        scripts = vedio_soup.findAll("script")
        info_script = scripts[9]

        # 取得音檔下載地址及talk_id
        links_tuple = self.extract_links(info_script)
        audio_link = links_tuple[0]
        talk_id = links_tuple[1]

        # 下載音檔，先判斷是否有下載網址，如果有再執行音檔和逐字稿下載
        if audio_link == "":
            print("Audio download link is not available.")
            return (False, "", "", [])
        else:
            # 取得音檔
            # print("NOTE: 不想下載音檔，請將下面一行註解起來")
            print("=====正在載入音檔，請稍候=====")
            self.download_audio(audio_link, talk_id)
            # 取得逐字稿
            transcript_with_answer = self.transcript_request(talk_id)
            transcript = transcript_with_answer[0]
            answer_list = transcript_with_answer[1]
            return (True, talk_id, transcript, answer_list)

    def extract_links(self, script):
        """從script中萃取 (1)adioDownload的網址 (2)talk_id

        Parameters:
            script: str, 影片頁面特定script

        Returns:
            audioDownload_url: adioDownload網址
            talk_id: talk_id
        """

        info_str = script.text

        #使用正規表示法，取得audioDownload_url
        pattern_audio = re.compile('audioDownload":"http.*?mp3.apikey=.*?"')
        audio_path = pattern_audio.findall(info_str)

        audioDownload_url = ""
        if len(audio_path) > 0:
            split_path = audio_path[0].split("\":\"")
            audioDownload_url = split_path[1][:-1]
        #print("audioDownload_url: " + audioDownload_url)

        #取得id
        pattern_id = re.compile('talk_id":\d+')
        id_path = pattern_id.findall(info_str)
        split_id = id_path[0].split("\":")
        talk_id = split_id[1]

        return (audioDownload_url, talk_id)

    def download_audio(self, link, talk_id):
        """下載音檔至根目錄，並以id當作檔案名稱

        Parameters:
            link: str, 下載網址
            talk_id: str, 演講id
        """

        fullfilename = os.path.join("./talks/", "{}.mp3".format(talk_id))
        try:
            urllib.request.urlretrieve(link, fullfilename, reporthook = None)
        except Exception as e:
            print("encounter error when download audio file")
            print(e)

    def transcript_request(self, talk_id):
        """取得逐字稿，並存成json格式

        Parameters:
            talk_id: str, 演講id
        """

        transcript_url = (self.base_url) + "/talks/" + talk_id + Endpoints().transcript
        #print("transcript_url: " + transcript_url)

        try:
            transcript_page = requests.get(transcript_url, headers = self.headers)
        except Exception as e:
            print("encounter error when request to transcript")
            print(e)

        transcript_cont = transcript_page.content
        transcript_soup = BeautifulSoup(transcript_cont, "html.parser")
        transcript_text = transcript_soup.text
        transcript_json = json.loads(transcript_text)

        text_converter = words.Text_converter(transcript_json)
        return text_converter.parse_text()