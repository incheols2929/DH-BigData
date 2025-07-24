#!/usr/bin/python
# -*- coding: utf-8 -*-

import config.config_database as cd
#from config.config_log import LOGGER

"""
    @packageName : source.common.db.facebook
    @fileName : facebook.py
    @author : juhee
    @date : 2023. 1. 9. 오전 10:08:02
    @content : 페이스북 Happy hbase 인터페이스 정보
"""

class DatabaseInterface:

    @classmethod
    def insert_data(cls, list, family):
        if len(list) != 0:
            count = cd.hbaseUtils.insert_batch('bigdata_collection_list', list, family + ':collection_url')
            # LOGGER.info('DB ENTIRE DATA SAVE ====> SUCCESS ')
        else:
            count = 0
            # LOGGER.info('DB ENTIRE DATA Count====> FAILED ')
        return count

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
        # else:
            # LOGGER.info(' The saved data is already stored in the database.')

        # LOGGER.info(' Saved list check complete...')