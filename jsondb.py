#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import sqlite3


class DB:
    def __init__(self, file_path=None):
        if file_path is not None:
            self.file_path = file_path

    def open(self, file_path=None):
        if file_path is not None:
            self.file_path = file_path
        self.connection = sqlite3.connect(self.file_path, isolation_level="DEFERRED")
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetch(self, sql):
        for row in self.cursor.execute(sql):
            yield row

    def query(self, sql):
        self.cursor.execute(sql)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self.close()


class JsonDB(DB):
    # def __query_string(self, sql, tablename, where, condition, column):
    #     if len(where) > 0:
    #         wstr = []
    #         for key in where.keys():
    #             if str(where[key]).find("%") != -1:
    #                 wstr.append(f"json_extract({column},'$.{key}') like '{where[key]}'")
    #             else:
    #                 if type(where[key]) == int:
    #                     wstr.append(f"json_extract({column},'$.{key}') = {where[key]}")
    #                 else:
    #                     wstr.append(
    #                         f"json_extract({column},'$.{key}') = '{where[key]}'"
    #                     )
    #         wstr = f" {condition} ".join(wstr)
    #         sql = " where ".join((sql, wstr))

    #     return sql

    def set(self, table_name, data_id, json_text):
        sql = f"""replace into {table_name} values({data_id}, '{json_text}')"""
        self.query(sql)

    def get(self, table_name, data_id):
        ret = None
        sql = f"select * from {table_name} where id={data_id}"
        for row in self.fetch(sql):
            ret = json.loads(row[1])
            break
        return ret

    # def find(self, tablename, where={}, condition="and", column="jsondata"):
    #     sql = f"select * from {tablename}"
    #     sql = self.__query_string(sql, tablename, where, condition, column)
    #     for row in self.fetch(sql):
    #         yield {"id": row[0], "data": json.loads(row[1])}

    # def count(self, tablename, where={}, condition="and", column="jsondata"):
    #     sql = f"select count(*) from {tablename}"
    #     sql = self.__query_string(sql, tablename, where, condition, column)
    #     row = self.fetch(sql)
    #     return row.__next__()[0]

    def create_table(self, tablename):
        sql = f"""create table if not exists "{tablename}" """
        sql += """("id" INTEGER, "jsondata" TEXT, PRIMARY KEY("id"))"""
        self.query(sql)
        self.commit()
