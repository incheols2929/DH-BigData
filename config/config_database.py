#!/usr/bin/python
# -*- coding: utf-8 -*-
from db.pg_utils import PgUtils

"""
    @packageName : source.common.config
    @fileName : config_database.py
    @author : incheols
    @date : 2023. 1. 4. 오전 09:52:52
    @content : 기본 설정 정보
"""


"""
     HBASE 설정 정보
"""
#HBASE_HOST = '192.168.0.101'
#HBASE_PORT = 9090
#HBASE_SIZE = 10

#TABLE_NAME = "bigdata_collection_list"

PG_HOST = '192.168.0.204'
PG_PORT = 31215
PG_DB = 'HN-SmartOffice_20250116'
PG_USER = 'postgres'
PG_PW = 'daeho1990!'

#hbaseUtils = HbaseUtils(host=HBASE_HOST, port=HBASE_PORT, size=HBASE_SIZE)
pgUtils = PgUtils(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PW)
