__author__ = 'v-rewei'

import DAO.SqlServerDAO

class BackupSQLDAO:
    def __init__(self, connstr):
        self.connstr = connstr

    def GetDB_id(self, dbname):
        sql = "select DB_ID('" + dbname +"')"
        dao = DAO.SqlServerDAO.SqlServerDAO(self.connstr)
        rs = dao.getone(sql)
        return int(rs)

