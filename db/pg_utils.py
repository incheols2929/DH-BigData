# -*- coding: utf-8 -*-
import sys
from importlib import reload
import psycopg2
from common.utils.logger import write_log  # 추가

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# https://codeantenna.com/a/R5lMmTaBfC
class PgUtils(object):
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.db = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()

    def insertDB(self, schema, table, colum, data):
        sql = " INSERT INTO {schema}.{table}({colum}) VALUES ('{data}') ;".format(schema=schema, table=table,
                                                                                  colum=colum, data=data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            write_log(f"insert DB err: {str(e)}")

    def readDB(self, schema, table, colum, where):
        sql = " SELECT {colum} from {schema}.{table} WHERE {where}".format(colum=colum, schema=schema, table=table,
                                                                           where=where)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            write_log(f"read DB err: {str(e)}")
            result = []

        return result

    def updateDB(self, schema, table, colum, value, condition):
        sql = " UPDATE {schema}.{table} SET {colum}='{value}' WHERE {colum}='{condition}' ".format(schema=schema
                                                                                                   , table=table,
                                                                                                   colum=colum,
                                                                                                   value=value,
                                                                                                   condition=condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            write_log(f"update DB err: {str(e)}")

    def deleteDB(self, schema, table, condition):
        sql = " delete from {schema}.{table} where {condition} ; ".format(schema=schema, table=table,
                                                                          condition=condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            write_log(f"delete DB err: {str(e)}")

    def updatInserteDB(self, schema, table, colum, data, conflict):
        colums = ", ".join(colum)

        sql = " INSERT INTO {schema}.{table}({colums}) VALUES (".format(schema=schema, table=table, colums=colums)
        for i in range(len(data)):
            sql += "'" + data[i] + "'"
            if i < len(data) - 1:
                sql += ","

        sql += ") ON CONFLICT ({conflict}) DO UPDATE SET ".format(conflict=conflict)
        for i in range(len(colum)):
            sql += colum[i] + "='" + data[i] + "'"
            if i < len(colum) - 1:
                sql += ","
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            write_log(f"upsert DB err: {str(e)}")
            # 연결 재시도
            try:
                self.db = psycopg2.connect(host=self.host, port=self.port, dbname=self.dbname, user=self.user,
                                           password=self.password)
                self.cursor = self.db.cursor()
                write_log("DB 연결 재시도 성공")
            except Exception as reconnect_error:
                write_log(f"DB 연결 재시도 실패: {str(reconnect_error)}")
