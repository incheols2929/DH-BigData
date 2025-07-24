#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
import os

# 프로젝트 디렉토리와 logs 폴더 경로 설정
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')

# logs 디렉토리가 없으면 생성
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def get_log_filename():
    # 현재 날짜로 파일명 생성 (예: log-2025-07-18.txt)
    current_date = dt.datetime.now().strftime('%Y-%m-%d')
    # logs 디렉토리와 파일명을 결합
    return os.path.join(LOGS_DIR, f'log-{current_date}.txt')

def write_log(message):
    # 현재 시간과 함께 로그 메시지 작성
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{current_time}] {message}\n'

    # 오늘 날짜의 로그 파일에 메시지 추가
    filename = get_log_filename()
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(log_message)

def create_new_logfile():
    # 새로운 로그 파일 생성
    filename = get_log_filename()
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'=== 로그 시작: {dt.datetime.now().strftime("%Y-%m-%d")} ===\n')
        write_log(f'새 로그 파일이 생성되었습니다: {filename}')