__author__ = 'v-rewei'

import DAO.SqlServerDAO
import MODEL.KPIValue


class KPIValueDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(KPIValueDAO, self).__init__(connstr)

    def t5loadkpivalues(self, dashboardid, fiscaltimeid, geoid, productid, deliverysiteid, teamid):
        rs = []
        sql = (
                'exec [dashboard].[procGetT5KPIValues]'
                ' {0},{1},{2},{3},{4},{5}'
        ).format(dashboardid, fiscaltimeid, geoid, productid, deliverysiteid, teamid)
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                m = MODEL.KPIValue.KPIValue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                rs.append(m)
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            self.closeconnect()
            return rs

    def t4loadkpivalues(self, dashboardid, fiscaltimeid, geoid, productid, deliverysiteid, pubsectorid):
        rs = []
        sql = (
                'exec [dashboard].[procGetT4KPIValues]'
                ' {0},{1},{2},{3},{4},{5}'
        ).format(dashboardid, fiscaltimeid, geoid, productid, deliverysiteid, pubsectorid)
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                m = MODEL.KPIValue.KPIValue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                rs.append(m)
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            self.closeconnect()
            return rs
