# TEST
import os
from datetime import datetime, timedelta
import config.config_database as con
import traceback

from common.analysis.Word2VecLearning import Word2VecLearning
from common.analysis.LogisticLearning import LogisticLearning
from nltk.corpus import stopwords
from common.utils import write_log
from common.naver.news import NaverNews


class MakeModel():
    def make_file(self):
        today = datetime.now()
        before_one_week = today - timedelta(weeks=24)

        today_str = str(today.strftime('%Y%m%d'))
        before_one_week_str = str(before_one_week.strftime('%Y%m%d'))

        try:
            # DB 연결 시 변수 추가
            category_list = con.pgUtils.readDB("public", "wk_news_category", "news_category_nm", "use_yn='Y'")
            # 모든기사
            self.make_model("", today_str, None, 0)

        except Exception as e:
            write_log(f"Error in make_file: {str(e)}")
            pass

    def make_model(self, keyword, today_str, cvf, cnt):
        path = keyword + "/" + today_str
        if cnt == 5:
            write_log(path + ' ==> 오류')
            return False
        try:
            tokenized_sentence_list = []
            logistic_list = {'x_data': [], 'y_data': []}

            # 오늘 날짜의 데이터만 가져오도록 수정
            news_data = con.pgUtils.readDB(
                "public",
                "wk_news_category",
                "news_category_nm",
                "use_yn='Y'"
            )

            processed_count = 0

            if news_data:
                total_count = len(news_data)
                write_log(f'전체 뉴스 데이터 수: {total_count}')

                for idx, news in enumerate(news_data, 1):
                    if news[0]:  # 뉴스 내용이 있는 경우에만 처리
                        try:
                            write_log(f'토큰화 처리 시작: {news[0][:50]}...')
                            tokenized_text, sentiment = NaverNews.get_tokenizer(news[0])
                            if tokenized_text:
                                tokens = tokenized_text if isinstance(tokenized_text, list) else tokenized_text.split()
                                if len(tokens) > 0:
                                    tokenized_sentence_list.append(tokens)
                                    processed_count += 1
                                    # 로깅 추가
                                    write_log(f'토큰화 성공 - 토큰 수: {len(tokens)}')

                        except Exception as e:
                            write_log(f'토큰화 처리 실패: {str(e)}')
                            continue

            write_log(f'전체 처리된 문서 수: {processed_count}')
            write_log(f'유효한 토큰화 문장 수: {len(tokenized_sentence_list)}')
            if len(tokenized_sentence_list) > 0:
                if cvf is None:
                    try:
                        self.scheduler_record('Word2Vec', 'start')
                        word2VecLearning = Word2VecLearning()
                        write_log(f'Word2Vec 학습 시작 - 입력 데이터 크기: {len(tokenized_sentence_list)}')
                        word2VecLearning.makeModel(tokenized_sentence_list, path="")
                        self.scheduler_record('Word2Vec', 'end')
                    except Exception as e:
                        write_log(f"Word2Vec 학습 중 오류 발생: {str(e)}")
                        raise

        except Exception as e:
            write_log(f'모델 생성 중 오류 발생: {str(e)}')
            write_log(traceback.format_exc())
            if cnt < 5:  # 재시도 횟수 제한
                self.make_model(keyword, today_str, cvf, cnt + 1)

    def scheduler_record(self, name, type):
        x = datetime.now()
        f = open('scheduler.txt', "a")
        f.write(type + ' ==> ' + name + ' : ' + str(x.strftime('%Y-%m-%d %H:%M:%S')) + '\n')
        f.close()
