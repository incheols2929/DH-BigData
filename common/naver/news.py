#!/usr/bin/python
# -*- coding: utf-8 -*-
import uuid
import json
import config.config_nlp as nlpCon
import config.config_database as cd
import config as config
import urllib.request
import requests
from common.utils import write_log
from urllib.parse import urlparse
from datetime import datetime
from newspaper import Article
from bs4 import BeautifulSoup

from db.interfaces import DatabaseInterface

from nlp.MorphologicalAnalyzer import MorphologicalAnalyzer
from nlp.SyntaxAnalyzer import SyntaxAnalyzer
from nlp.Processing import Processing


"""
    @author : incheols
    @date : 2023. 1. 4. 오전 09:52:52
    @content : 네이버 뉴스 데이터 수집
"""

ma = MorphologicalAnalyzer()
sa = SyntaxAnalyzer()
pro = Processing()

with open('common/SentiWord_info.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)


class NaverNews:
    @classmethod
    def get_detail_crawling(cls, posts, text):
        # LOGGER.debug(' Start collecting Naver News detailed post information...')
        resultList = []
        for post in posts:

            url = post['originallink']
            # date = str(datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900').strftime('%Y%m%d'))
            date = int(datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900').strftime('%Y%m%d'))

            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                if r.encoding == 'ISO-8859-1':
                    soup = BeautifulSoup(r.content.decode('utf-8-sig', 'replace'), 'html.parser')
                else:
                    soup = BeautifulSoup(r.content, 'html.parser')

                propertys = ['og:site_name', 'article:section']
                names = ['twitter:creator', 'Copyright']

                newsPress = ''

                for property in propertys:
                    siteName = soup.select_one('meta[property="' + property + '"]')
                    if siteName != None:
                        newsPress = siteName["content"]
                        break
                if newsPress == '':
                    for name in names:
                        siteName = soup.select_one('meta[name="' + name + '"]')
                        if siteName != None:
                            newsPress = siteName["content"]
                            break

                # 언론사를 특정할 수 없어, 하드코딩
                keys = config.news_press.keys()
                for key in keys:
                    if key in url:
                        newsPress = config.news_press[key]

                if newsPress != '':
                    article = Article(url)
                    article.download()
                    article.html
                    article.parse()
                    article.nlp()

                    if article.text != '':
                        token, pn = cls.get_tokenizer(article.text)
                        rowUuid = str(uuid.uuid4())
                        resultList.append(
                            {'row': rowUuid, 'data':
                                {
                                    "news:collection_title": str(article.title)
                                    , "news:collection_press": str(newsPress)
                                    , "news:collection_date": str(date)
                                    , "news:collection_content": str(article.text)
                                    , "news:collection_category": str(text)
                                    , "news:collection_url": str(url)
                                    , "news:collection_etc": ""
                                    , "news:collection_keyword": str(article.keywords)
                                    , "news:collection_summary": str(article.summary)
                                    , "news:collection_token": str(token)
                                    , "news:collection_pn": str(pn)
                                }
                             }
                        )

                        # Postgres 변수
                        colums = ['news_press', 'news_title', 'news_explan', 'reg_date', 'news_url', 'news_keyword',
                                  'news_summary', 'news_pn', 'news_category']
                        datas = [newsPress, article.title.replace("'", "''"), article.text.replace("'", "''"),
                                 str(date), url, ','.join(article.keywords), article.summary.replace("'", "''"), pn,
                                 text]
                        cd.pgUtils.updatInserteDB("public", "wk_news", colums, datas, "news_url, news_category")
                        cls.count += 1
            except Exception as e:  # work on python 3.x
                # import nltk
                # nltk.download()
                write_log(e)
                pass

        # LOGGER.debug(' Success in collecting Naver News detailed post information...')
        #write_log('Hbase에 저장할 데이터 ==>', resultList)
        #count = DatabaseInterface.insert_data(resultList, 'news')
        #cls.count += count

    @classmethod
    def get_tokenizer(cls, content):
        tokenized_sentence_list = []
        total_point = 0

        for word in nlpCon.SKIP_WORD_LIST:
            content = content.replace(word, "")

        sentence_list = pro.sentence_splitter(content)
        for sentence in sentence_list:
            word_list = sentence.split()
            for data in json_data:
                point = data['polarity']
                cnt = word_list.count(data['word'])
                if cnt > 0:
                    total_point += cnt * int(point)

            tagged_word_list = ma.parse(sentence)
            for tagged_word in tagged_word_list:
                # if tagged_word[1] in nlpCon.TAG_CLASSES and tokenizer.isHangul(tagged_word[0]):
                if tagged_word[1] in nlpCon.TAG_CLASSES:
                    tokenized_sentence_list.append(tagged_word[0])

        if total_point > 0:
            total_point = '1'
        elif total_point < 0:
            total_point = '-1'
        else:
            total_point = '0'

        return ' '.join(tokenized_sentence_list), total_point

    # [CODE 1]
    def getRequestUrl(cls, url):
        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", cls.client_id)
        req.add_header("X-Naver-Client-Secret", cls.client_secret)

        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                write_log("[%s] Url Request Success" % datetime.now())
                return response.read().decode('utf-8')
        except Exception as e:
            write_log(e)
            write_log("[%s] Error for URL : %s" % (datetime.now(), url))
            return None

    # [CODE 2]
    def getNaverSearch(cls, srcText, display, sort):
        base = "https://openapi.naver.com/v1/search/news.json"
        parameters = "?query=%s&display=%s&sort=%s" % (urllib.parse.quote(srcText), display, sort)

        url = base + parameters
        responseDecode = cls.getRequestUrl(cls, url)  # [CODE 1]

        if (responseDecode == None):
            return None
        else:
            return json.loads(responseDecode)

    # [CODE 0]
    @classmethod
    def get_naver_news(cls, client_id, client_secret, keyword):
        # LOGGER.info('<=== Start collecting Naver News data ===>')
        write_log("<=== Start collecting Naver News data ===>")
        cls.count = 0
        cls.client_id = client_id
        cls.client_secret = client_secret
        cls.today = str(datetime.today().strftime("%Y%m%d"))

        jsonResponse = cls.getNaverSearch(cls, keyword, '100', 'date')  # [CODE 2]
        #write_log('Naver API Response  ==> \n', jsonResponse['items'])
        #write_log('Naver API Response  ==> \n',jsonResponse['items'])
        cls.get_detail_crawling(jsonResponse['items'], keyword)
        write_log("<=== End of Naver News data collection ===>")
        # LOGGER.info('<=== End of Naver News data collection ===>')
        return cls.count
