__author__ = 'v-rewei'

import DAO.SqlServerDAO

class BackupSQLDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(BackupSQLDAO, self).__init__(connstr)

    def GetDB_id(self, dbname):
        sql = "select DB_ID('" + dbname +"')"
        rs = self.getone(sql)
        return int(rs)

