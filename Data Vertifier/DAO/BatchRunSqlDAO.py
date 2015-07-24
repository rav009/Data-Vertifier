__author__ = 'v-rewei'

import DAO.SqlServerDAO
import datetime

class BatchRunSqlDAO:
    def RunBatch(self, slist, sql, who):
        if not sql or not slist or len(slist) == 0 or str(sql).strip == '':
            return "Parameters Null Exception"
        else:
            sql = str(sql).strip()
            self.LogBatchStart(who, sql)
            extmsg = 'Success'
            for s in slist:
                self.LogSqlStart(s)
                dao = DAO.SqlServerDAO.SqlServerDAO(s)
                dao.connect()
                try:
                    c = dao.conn.cursor()
                    c.execute(sql)
                    dao.conn.commit()
                except Exception as ext:
                    extmsg = s + '\n Exception Message:' + ext.message
                    self.LogException(ext.message)
                    break
                finally:
                    c.close()
                    dao.closeconnect()
            self.LogBatchEnd()
            return extmsg

    def LogBatchStart(self, who, sql):
        with open("batchlog.log", mode='a+') as f:
            f.write('\n')
            s = self.FormatSplteline()
            f.write(s)
            f.write('\n')
            f.write('Batch Start')
            f.write('\n')
            f.write('Alias: ' + who)
            f.write('\n')
            f.write(str(sql))

    def LogSqlStart(self, connstr):
        with open("batchlog.log", mode='a+') as f:
            f.write('\n');
            f.write(connstr)

    def LogException(self, message):
        with open("batchlog.log", mode='a+') as f:
            f.write('\n');
            f.write('Exception: \n');
            f.write(message)

    def LogBatchEnd(self):
        with open("batchlog.log", mode='a+') as f:
            f.write('\n');
            f.write('Batch End')
            f.write('\n')
            s = self.FormatSplteline()
            f.write(s)
            f.write('\n')
            f.write('\n')
            f.write('\n')

    def FormatSplteline(self):
        s = ''.join(['=']*40)
        s += datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        s += ''.join(['=']*40)
        return s
