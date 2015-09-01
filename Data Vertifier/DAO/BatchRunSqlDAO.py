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
            extmsg = ''
            for s in slist:
                self.LogSqlStart(s)
                dao = DAO.SqlServerDAO.SqlServerDAO(s)
                c = None
                try:
                    dao.connect()
                    c = dao.conn.cursor()
                    c.execute(sql)
                    dao.conn.commit()
                    extmsg += s + " :Success\n"
                except Exception as ext:
                    extmsg += s + " :Fail\n Exception Message:" + ext.message
                    self.LogException(ext.message)
                    break
                finally:
                    if c:
                        c.close()
                    if dao:
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
            f.write(str(sql).replace('\r\n', '\n'))
            f.write('\n')

    def LogSqlStart(self, connstr):
        with open("batchlog.log", mode='a+') as f:
            f.write('\n')
            f.write(connstr)

    def LogException(self, message):
        with open("batchlog.log", mode='a+') as f:
            f.write('\n')
            f.write('Exception: \n');
            f.write(message.replace('\r\n', '\n'))

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
