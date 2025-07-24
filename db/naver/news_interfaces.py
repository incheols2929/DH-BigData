#!/usr/bin/python
# -*- coding: utf-8 -*-
import config.config_database as cd
from config.config_log import LOGGER

"""
    @author : incheols
    @date : 2023. 1. 4. 오전 09:52:52
    @content : 네이버 뉴스 Happy hbase 인터페이스 정보
"""

class DatabaseInterface:

    @classmethod
    def insert_data(cls, list):
        success = False

        if len(list) != 0:
            cd.hbaseUtils.insert_batch('bigdata_collection_list', list, 'naver_news:collection_url')
            # LOGGER.info('DB ENTIRE DATA SAVE ====> SUCCESS ')
            # read_count = str(hbaseUtils.read_count('bigdata_collection_list'))
            # LOGGER.info('DB ENTIRE DATA Count====> : ' + read_count)
            # cls.get_save_list(list)
            success = True
        else:
            # LOGGER.info('DB ENTIRE DATA Count====> FAILED ')
            success = False
        return success

    @classmethod
    def get_save_list(cls, list):
        # LOGGER.info(' Start checking your saved list...')
        rowKeyList = []
        for index, value in enumerate(list):
            rowKeyList.append(bytes(str(value['row']), encoding='utf-8'))

        resultRow = cd.hbaseUtils.read_rows('bigdata_collection_list', rowKeyList, include_timestamp=False,
                                         need_dict=False)
        if len(resultRow) != 0:
            json = {}
            for index, value in resultRow:
                detailJson = {}
                for k, v in value.items():
                    detailJson[k] = v.decode('utf-8')
                json[index] = detailJson
            saveJson = str(json)
            # LOGGER.debug(' Added Saved List : ' + saveJson)
        else:
            # LOGGER.info(' The saved data is already stored in the database.')
            pass

        # LOGGER.info(' Saved list check complete...')