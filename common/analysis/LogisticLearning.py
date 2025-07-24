import pandas as pd
import json
import config.config_database as Dcon
import traceback
import os

from common.analysis.TfidfCalculator import TfidfCalculator
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
from common.handler.FileHandler import FileHandler
from hdfs import InsecureClient
from common.utils import write_log
class LogisticLearning():  
    def __init__(self):
        self.fh = FileHandler()

    def makeModel(self, x_data, y_data, keyword, today_str) :
        path = keyword + "/" + today_str
        
        tfidfCalculator = TfidfCalculator()

        vect, bow_vect = tfidfCalculator.get_count_vector(x_data)
        tf_idf_vect = tfidfCalculator.get_tfidf_vector(bow_vect)

        df = pd.DataFrame({
            'y':y_data
        })
        x_train, x_test, y_train, y_test = train_test_split(tf_idf_vect, df['y'], test_size = 0.3, random_state=1)

        # fit in training set
        lr = LogisticRegression(random_state = 0)
        lr.fit(x_train, y_train)

        # predict in test set
        y_pred = lr.predict(x_test)

        confu = confusion_matrix(y_true = y_test, y_pred = y_pred)

        coef_index = sorted(((value, index) for index, value in enumerate(lr.coef_[0])), reverse = False)
        # coef_pos_index = sorted(((value, index) for index, value in enumerate(lr.coef_[0])), reverse = False)

        invert_index_vectorizer = {v: k for k, v in vect.vocabulary_.items()}

        pos_list = []
        neg_list = []
        neu_list = []

        half = len(coef_index) // 2

        for coef in coef_index[:20]:
            pos_list.append(invert_index_vectorizer[coef[1]])

        for coef in coef_index[::-1][:20]:
            neg_list.append(invert_index_vectorizer[coef[1]])

        for coef in coef_index[half:half+20]:
            neu_list.append(invert_index_vectorizer[coef[1]])

        feeling_json = {
            '긍정어' : pos_list,
            '부정어' : neg_list,
            '중립어' : neu_list
        }

        # Postgres 변수
        colums = ['feeling_code', 'feeling_word', 'feeling_rank', 'reg_date', 'keyword']

        # 긍정어
        for i in range(len(pos_list)) :
            datas = ['01', pos_list[i], str(i+1), today_str, keyword]
            Dcon.pgUtils.updatInserteDB("public", "wk_feeling", colums, datas, "feeling_code, feeling_rank, reg_date, keyword")

        # 부정어
        for i in range(len(neg_list)) :
            datas = ['02', neg_list[i], str(i+1), today_str, keyword]
            Dcon.pgUtils.updatInserteDB("public", "wk_feeling", colums, datas, "feeling_code, feeling_rank, reg_date, keyword")

        #if not os.path.exists('/home/daeho/naver_news_analyze/datas/'+ path):
        #    os.makedirs('/home/daeho/naver_news_analyze/datas/'+ path)

        #with open('/home/daeho/naver_news_analyze/datas/' + path + '/feeling.json', 'w+', encoding='UTF-8') as f:
         #   json.dump(feeling_json, f, ensure_ascii=False)

        if not os.path.exists('C:/pythonWorkspace/DH-BigData-Module/naver_news_analyze/datas/'+ path):
           os.makedirs('C:/pythonWorkspace/DH-BigData-Module/naver_news_analyze/datas/'+ path)

        with open('C:/pythonWorkspace/DH-BigData-Module/naver_news_analyze/datas/' + path + '/feeling.json', 'w+', encoding='UTF-8') as f:
           json.dump(feeling_json, f, ensure_ascii=False)

        try :
            # HDFS 클라이언트와 연결합니다.
            client = InsecureClient(Dcon.HDFS_URL, user=Dcon.HDFS_USER)

            # HDFS의 디렉토리를 생성합니다.
            client.makedirs('data')

            # 파일을 업로드합니다.
            client.upload('data/' +  path + '/feeling.json', 'C:/pythonWorkspace/DH-BigData-Module/naver_news_analyze/datas/' +  path + '/feeling.json', overwrite=True)
            #client.upload('data/' + path + '/feeling.json', '/home/daeho/naver_news_analyze/datas/' + path + '/feeling.json', overwrite=True)
        except Exception as e:
            write_log(traceback.format_exc())