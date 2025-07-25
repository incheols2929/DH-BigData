import datetime as dt
import time
import schedule
import os
import sys
import logging
import config.config_database as cd
import urllib3.exceptions  # 추가
import traceback  # 추가

from common.utils.logger import write_log, create_new_logfile  # 수정된 부분
from common.naver.news import NaverNews
from common.analysis.MakeModel import MakeModel
from flask import Flask
from datetime import datetime
from common.service.Service import Service

# 매일 자정(00:00)에 새로운 로그 파일 생성
schedule.every().day.at("00:00").do(create_new_logfile)

# 프로그램 시작시 로그 파일 생성
create_new_logfile()

app = Flask(__name__)

@app.route('/keyword/<keyword>', methods=['GET'])
def keyword(keyword):
    return Service.keyword(keyword)



def end_job():
    write_log("<=== Start analysis ===>")
    try:
        makeModel = MakeModel()
        makeModel.make_file()
        write_log("<=== End analysis ===>")
    except Exception as e:
        write_log(f"분석 중 에러 발생: {str(e)}")
        write_log(f"에러 상세: {traceback.format_exc()}")


def start_job():
    count = 0
    write_log("데이터 수집 시작.")
    try:
        keyword_list = cd.pgUtils.readDB("public", "wk_news_category", "news_category_nm", "use_yn='Y'")
        config_list = cd.pgUtils.readDB("public", "dhc_code", "code, code_name", "group_code='COLLECTION_CONFIG'")

        for config in config_list:
            if config[0] == 'CLIENT_ID':
                client_id = config[1]
            elif config[0] == 'CLIENT_SECRET':
                client_secret = config[1]

        for keyword in keyword_list:
            try:
                count += NaverNews.get_naver_news(client_id, client_secret, keyword[0])
            except urllib3.exceptions.HeaderParsingError as e:
                write_log(f"헤더 파싱 에러 발생 - 키워드: {keyword[0]}")
                write_log(f"헤더 파싱 에러 상세: {str(e)}")
                continue  # 다음 키워드로 진행
            except Exception as e:
                write_log(f"네이버 뉴스 수집 중 에러 발생 - 키워드: {keyword[0]}")
                write_log(f"에러 상세: {str(e)}")
                write_log(f"에러 추적: {traceback.format_exc()}")
                continue  # 다음 키워드로 진행

    except Exception as e:
        write_log(f'DB에서 네이버 키 가져올 시 에러 발생 ==> \n{str(e)}')
        write_log(f"에러 추적: {traceback.format_exc()}")
    finally:
        # 예외 발생 여부와 관계없이 end_job 실행
        end_job()


def setup_logging():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    log_dir = '{}/logs'.format(current_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('./logs/{:%Y-%m-%d}.log'.format(datetime.now()), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def run_schedule():
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            write_log(f"스케줄러 실행 중 에러: {str(e)}")
            write_log(f"에러 추적: {traceback.format_exc()}")


if __name__ == '__main__':
    try:
        # 로깅 설정
        setup_logging()

        # 스케줄러 작업 설정
        schedule.every().day.at("00:00").do(create_new_logfile)
        schedule.every().minute.at(":00").do(start_job)

        # 프로그램 시작시 로그 파일 생성
        create_new_logfile()

        # Flask 앱과 스케줄러를 별도의 스레드에서 실행
        from threading import Thread

        scheduler_thread = Thread(target=run_schedule)
        scheduler_thread.daemon = True
        scheduler_thread.start()

        # Flask 앱 실행
        app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)

    except Exception as e:
        write_log(f"메인 프로그램에서 치명적 에러 발생: {str(e)}")
        write_log(f"에러 추적: {traceback.format_exc()}")

