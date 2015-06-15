__author__ = 'v-rewei'


class KPIValue:
    def __init__(self, kpiid, kpiname, displaytype, baselinetype, statustype, baseline, mtdtarget, mtd, mtdstatus, ytdtarget, ytd, ytdstatus):
        self.kpiid = kpiid
        self.kpiname = kpiname
        self.displaytype = displaytype
        self.baselinetype = baselinetype
        self.statustype = statustype
        self.baseline = baseline
        self.mtdtarget = mtdtarget
        self.mtd = mtd
        self.mtdstatus = mtdstatus
        self.ytdtarget = ytdtarget
        self.ytd = ytd
        self.ytdstatus = ytdstatus

