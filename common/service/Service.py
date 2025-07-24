import json
from gensim.models import word2vec
from config.config import MODEL_PATH

class Service:
    news_file_json = {}
    category_file_json = {}
    all_file_json = {}
    client = None

    def keyword(keyword):
        # w2v_model = word2vec.Word2Vec.load("/user/daeho/data/word2vec.model")
        # w2v_model = word2vec.Word2Vec.load("/home/daeho/naver_news_analyze/datas/word2vec.model")
        #w2v_model = word2vec.Word2Vec.load("D:/pythonWorkspace/DH-BigData-Module/naver_news_analyze/datas/word2vec.model")
        w2v_model = word2vec.Word2Vec.load(MODEL_PATH)

        position = [['' for j in range(10)] for i in range(10)]
        w2v = {}
        word_dic = {
            "name": keyword,
            "children": []
        }
        try:
            # 키워드에 대한 연관어
            wordlist = w2v_model.wv.most_similar(keyword)
            for i in range(len(wordlist)):
                children = {
                    "name": wordlist[i][0],
                    "value": wordlist[i][1],
                    "children": [],
                    "link": []
                }
                word_dic["children"].append(children)

                # 연관어에 대한 연관어
                wordlist2 = w2v_model.wv.most_similar(wordlist[i][0])
                for j in range(len(wordlist2)):
                    # 링크를 위한 포지셔닝
                    position[i][j] = wordlist2[j][0]
                    # 키워드, 키워드에 대한 연관어면 안넣음
                    if keyword == wordlist2[j][0] or wordlist2[j][0] in list(zip(*wordlist))[0]:
                        continue

                    # 연관어 체크 중 다른 노드에 이미 나온 단어면 링크
                    check = 0
                    if i > 0:
                        for x in range(i):
                            if wordlist2[j][0] in position[x]:
                                word_dic["children"][i]["link"].append(wordlist2[j][0])
                                check = 1
                                break

                    if check == 0:
                        children2 = {
                            "name": wordlist2[j][0],
                            "value": wordlist2[j][1]
                        }
                        word_dic["children"][i]["children"].append(children2)

        except Exception as e:
            print(e)
        w2v['result'] = [word_dic]
        return w2v
