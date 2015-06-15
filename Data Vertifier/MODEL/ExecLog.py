__author__ = 'v-rewei'


class ExecLog:
    def __init__(self, kpiid, querypart, datasourceid, execstatus, fiscalyear, fiscalmonth, execdate, remark):
        self.kpiid = kpiid
        self.querypart = querypart
        self.datasourceid = datasourceid
        self.execstatus = execstatus
        self.fiscalyear = fiscalyear
        self.fiscalmonth = fiscalmonth
        self.execdate = execdate
        self.execdate_str= str(self.execdate)[0 :19]
        self.remark = remark