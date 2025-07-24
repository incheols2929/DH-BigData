import os
import json
import pandas as pd
import warnings
import config.config_database as Dcon
import config.config as con
import traceback

from datetime import datetime
from common.handler.FileHandler import FileHandler
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from hdfs import InsecureClient
from common.utils import write_log

warnings.filterwarnings(action='ignore')

class CountCalculator():  
    def __init__(self):
        self.fh = FileHandler()
    
    def calculation_count(self, news_list, date=str(datetime.today().strftime("%Y%m%d"))):
        self.all_dict = {}
        for press in news_list :
            news_path = '/' + press
            # TF Vector
            self.vectorizer = CountVectorizer(token_pattern='\S+')
            self.matrix = self.vectorizer.fit_transform(news_list[press]).todense()
            self.matrix = pd.DataFrame(self.matrix, columns=self.vectorizer.get_feature_names_out())
            self.dict = {}
            for tokenized_sentence in tqdm(news_list[press]):
                word_list = tokenized_sentence.split(" ")
                for word in word_list:
                    word = word.lower()
                    if word not in self.__get_stopwords():
                        if word in self.dict.keys():
                            self.dict[word] += 1
                        else :
                            self.dict[word] = 1
                            
                        if word in self.all_dict.keys():
                            self.all_dict[word] += 1
                        else :
                            self.all_dict[word] = 1

                            
            if not os.path.exists('datas/' + date + news_path):
                os.makedirs('datas/' + date + news_path)

            with open('datas/' + date + news_path + '/count.json', 'w+', encoding='UTF-8') as f:
                json.dump(self.dict, f, ensure_ascii=False)


            try :
                # HDFS 클라이언트와 연결합니다.
                client = InsecureClient(Dcon.HDFS_URL, user=Dcon.HDFS_USER)

                # HDFS의 디렉토리를 생성합니다.
                client.makedirs('data')

                # 파일을 업로드합니다.
                client.upload('data/' +  date + news_path + '/count.json', 'datas/' +  date + news_path + '/count.json', overwrite=True)
            except Exception as e:
                write_log(traceback.format_exc())
                
        if not os.path.exists('datas/' + date):
            os.makedirs('datas/' + date )

        with open('datas/' + date + '/count.json', 'w+', encoding='UTF-8') as f:
            json.dump(self.all_dict, f, ensure_ascii=False)

        try :
            # HDFS 클라이언트와 연결합니다.
            client = InsecureClient(Dcon.HDFS_URL, user=Dcon.HDFS_USER)

            # HDFS의 디렉토리를 생성합니다.
            client.makedirs('data')

            # 파일을 업로드합니다.
            client.upload('data/' + date + '/count.json', 'datas/' + date + '/count.json', overwrite=True)
        except Exception as e:
            write_log(traceback.format_exc())
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list