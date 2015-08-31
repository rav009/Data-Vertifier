# -*- coding: utf-8 -*-
__author__ = 'wei'

import adodbapi
import logging

class SqlServerDAO(object):
    def __init__(self, connstr):
        self.connstr = connstr
        self.conn = None

    def __del__(self):
        pass

    def connect(self):
        self.conn = adodbapi.connect(self.connstr)

    def returnconn(self, _connstr = None):
        if not _connstr:
            return adodbapi.connect(self.connstr)
        else:
            return adodbapi.connect(_connstr)

    def closeconnect(self):
        self.conn.close()

    def execsql(self, sql):
        """
        执行sql语句
        """
        self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as ext:
            logging.error(ext)
            cursor.close()
            self.closeconnect()

    def fielddict(self, cursor):
        """
        get id-colname map in the cursor
        """
        dict = {}
        i = 0
        for field in cursor.description:
            dict[field[0]] = i
            i += 1
        return dict

    def getone(self, sql):
        """
        根据查询获取一行第一个
        """
        self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            row = cursor.fetchone()
            if row is None:
                return None
            return row[0]
        except Exception as ext:
            logging.error(ext)
            cursor.close()
            self.closeconnect()
            return None

# s=SqlServerDAO('Provider=SQLOLEDB.1;Data Source=192.168.62.192;Initial Catalog=RadioDataWarehouse;Persist Security Info=True;User ID=sa;Password=P@ssw0rd')
# print(s.getone('INSERT INTO DimGeography (CountryName, ProvinceName, CityName) VALUES     (\'加拿大22324\', \'新南2\', \'teeee\')'))