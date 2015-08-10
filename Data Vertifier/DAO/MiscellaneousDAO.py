__author__ = 'v-rewei'


import DAO.SqlServerDAO

class MiscellaneousDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(MiscellaneousDAO, self).__init__(connstr)
        self.syncjobname = 'Sync'
        self.jobstatus_struct = {
            'current_execution_status': 25,
            'current_execution_step': 26,
            'last_run_date': 19,
            'last_run_time': 20,
            'last_run_outcome': 21
        }

    def LoadFullIncrementMode(self):
        rs = None
        _conn = self.returnconn(self.connstr)
        cursor = _conn.cursor()
        cursor.execute('select * from dashboard.helper_KPIValue_Increment_Full')
        try:
            row = cursor.fetchone()
            if row is not None:
                rs = ((row[0], row[1]))
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            _conn.close()
            return rs

    def LoadSyncJobStatus(self):
        sql = ('EXEC msdb.dbo.sp_help_job @Job_name = \'{0}\',@job_aspect = N\'JOB\' ;').format(self.syncjobname)
        rs = None
        _conn = self.returnconn(self.connstr)
        cursor = _conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            if row is not None:
                rs = {}
                for k in self.jobstatus_struct.keys():
                    rs[k] = row[self.jobstatus_struct[k]]
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            _conn.close()
            return rs