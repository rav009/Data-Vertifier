__author__ = 'v-rewei'

import DAO.SqlServerDAO
import MODEL.KPIValue


class KPIValueDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(KPIValueDAO, self).__init__(connstr)

    def t4loadkpivalues(self, dashboardid, fiscaltimeid, geoid, productid, deliverysiteid, pubsectorid):
        rs = []
        sql = (
                'exec [dashboard].[procGetT4KPIValues]'
                ' {0},{1},{2},{3},{4},{5}'
        ).format(dashboardid, fiscaltimeid, geoid, productid, deliverysiteid, pubsectorid)
        conn = self.returnconn()
        cursor = conn.cursor()
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
            conn.close()
            return rs

    def DEloadkpivalues(self, fiscaltimeid, pcid, deliverysiteid,functionid, usedeliveryid):
        rs = []
        sql = (
                'exec [dashboard].[procGetKpiValuesForDE]'
                ' {0},{1},{2},{3},{4},{5}'
        ).format(4, fiscaltimeid, pcid, functionid, deliverysiteid, usedeliveryid)
        conn = self.returnconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                m = MODEL.KPIValue.KPIValue(row[0], row[3], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
                rs.append(m)
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            conn.close()
            return rs