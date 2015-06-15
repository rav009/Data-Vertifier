__author__ = 'v-rewei'

import DAO.SqlServerDAO
import MODEL.ExecLog

class ExecLogDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(ExecLogDAO, self).__init__(connstr)

    def loadlogs(self, top, ifalllog):
        rs = []
        if ifalllog:
            sql = ('SELECT TOP {0} '
                    'e.[KPIID]'
                    ',[Querypart]'
	                ',n.DataSourceID'
                    ',[ExecStatus]'
                    ',[FiscalYear]'
                    ',[FiscalMonthOfYear]'
                    ',[ExecDate]'
                    ',remark'
                    ' FROM [dashboard].[KPIQuery_ExecLog] e left join [dashboard].[KPIQuery_Specific] n '
                    'on e.KPIID=n.KPIID and e.Querypart=n.Part'
                    ' {1} '
                    'order by execdate desc').format(str(top), '')
        else:
            sql = ('SELECT TOP {0} '
                    'e.[KPIID]'
                    ',[Querypart]'
	                ',n.DataSourceID'
                    ',[ExecStatus]'
                    ',[FiscalYear]'
                    ',[FiscalMonthOfYear]'
                    ',[ExecDate]'
                    ',remark'
                    ' FROM [dashboard].[KPIQuery_ExecLog] e left join [dashboard].[KPIQuery_Specific] n '
                    ' on e.KPIID=n.KPIID and e.Querypart=n.Part '
                    ' {1} '
                    'order by execdate desc').format(str(top), 'where ExecStatus like \'Failed\'')
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                m = MODEL.ExecLog.ExecLog(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                rs.append(m)
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            self.closeconnect()
            return rs


