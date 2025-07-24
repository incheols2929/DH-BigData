#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
"""
    @packageName : source.common.config
    @fileName : config_log.py
    @author : incheols
    @date : 2023. 1. 4. 오전 09:52:52
    @content : 로그 설정 정보
"""

"""
    로그 설정
"""
# # 로그 생성
# LOGGER = logging.getLogger()
# # 로그의 출력 기준 설정(INFO,DEBUG,ERROR)
# LOGGER.setLevel(logging.INFO)

# # log 출력 형식
# logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(logger_formatter)
# LOGGER.addHandler(stream_handler)


# # log를 파일에 출력
# if not os.path.exists('file/log'):
#     os.makedirs('file/log')
# timedfilehandler = logging.handlers.TimedRotatingFileHandler(filename='file/log/batch.log', when='midnight', interval=1, encoding='utf-8')
# timedfilehandler.setFormatter(logger_formatter)
# timedfilehandler.suffix = "%Y%m%d"
# LOGGER.addHandler(timedfilehandler)

# file_handler = logging.FileHandler('my.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)