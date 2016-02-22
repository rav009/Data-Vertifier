__author__ = 'v-rewei'
import web
import DAO.QueryDAO
import DAO.ExecLogDAO
import DAO.DimDAO
import DAO.KPIValueDAO
import DAO.HierarchyDAO
import DAO.BatchRunSqlDAO
import DAO.BackupSQLDAO
import DAO.MiscellaneousDAO
import json

#For Https
# from web.wsgiserver import CherryPyWSGIServer
# CherryPyWSGIServer.ssl_certificate = "D:\\tmp-program\\Data Vertifier SSL\\v-rewei-pc.crt"
# CherryPyWSGIServer.ssl_private_key = "D:\\tmp-program\\Data Vertifier SSL\\private.key"

#global variables and functions
urls = (
    '/', 'Index',
    '/favicon.ico', 'icon',
    '/index', 'Index',
    '/index/', 'Index',
    '/mdxquery/', 'MDXQuery',
    '/execlog/', 'ExecLog',
    '/dim/', 'Dim',
    '/verifykpi/(.+)', 'VerifyKPI',
    '/verifykpijson/', 'VerifyKPIJson',
    '/switchdb/', 'SwitchDB',
    '/addnode/', 'AddNode',
    '/clipboard/', 'Clipboard',
    '/getfimode/', 'GetFullIncrementMode',
    '/getjobstatus/', 'GetJobStatus',
    '/batchexec/', 'BatchExec',
    '/backupsql/', 'BackupSQL'
)

remote_clipboard = []

connstr_d = 'Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_p = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-prod;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_us = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-us;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'

def GetCurrentDBName(connstr):
    import re
    p = re.search('data source=([\w-]+);', connstr)
    return p.group(1)



def createGlobalDAO():
    global batchrunSqlDAO
    batchrunSqlDAO = DAO.BatchRunSqlDAO.BatchRunSqlDAO()
    global backupSQLDAO
    backupSQLDAO = DAO.BackupSQLDAO.BackupSQLDAO(connstr_us)
    global misdao_us
    misdao_us = DAO.MiscellaneousDAO.MiscellaneousDAO(connstr_us)
    global misdao_prod
    misdao_prod = DAO.MiscellaneousDAO.MiscellaneousDAO(connstr_p)
#     global querydao
#     querydao = DAO.QueryDAO.QueryDAO(current_connstr)
#     global execlogdao
#     execlogdao = DAO.ExecLogDAO.ExecLogDAO(current_connstr)
#     global dimdao
#     dimdao = DAO.DimDAO.DimDAO(current_connstr)
#     global verifykpidao
#     verifykpidao = DAO.KPIValueDAO.KPIValueDAO(current_connstr)
#     global hierarchydao
#     hierarchydao = DAO.HierarchyDAO.HierarchyDAO(current_connstr)

def getRuntimeDAO(data, daoname):
    if 'selectdb' not in data.keys():
        current_connstr = connstr_us
    elif str(data['selectdb']).lower() == 'prod':
        current_connstr = connstr_p
    elif str(data['selectdb']).lower() == 'dev':
        current_connstr = connstr_d
    else:
        current_connstr = connstr_us
    if daoname == 'querydao':
        dao = DAO.QueryDAO.QueryDAO(current_connstr)
    elif daoname =='execlogdao':
        dao = DAO.ExecLogDAO.ExecLogDAO(current_connstr)
    elif daoname =='dimdao':
        dao = DAO.DimDAO.DimDAO(current_connstr)
    elif daoname =='verifykpidao':
        dao = DAO.KPIValueDAO.KPIValueDAO(current_connstr)
    elif daoname =='hierarchydao':
        dao = DAO.HierarchyDAO.HierarchyDAO(current_connstr)
    else:
        raise Exception('Unknown dao name!')
    return dao


def createRender():
    global render
    #render = web.template.render('templates', base='layout', globals={"connstr": GetCurrentDBName(current_connstr)})
    render = web.template.render('templates', base='layout')
    global render_plain
    render_plain = web.template.render('templates',globals={"str":str})
    #render_plain = web.template.render('templates', globals={"connstr": GetCurrentDBName(current_connstr)})


createGlobalDAO()
createRender()


#PageClass begin
class icon:
    def GET(self):
        raise web.seeother("/static/favicon.ico")

class Index:
    def GET(self):
        return render_plain.index()


class MDXQuery:
    def GET(self):
        data = web.input()
        querydao = getRuntimeDAO(data, 'querydao')
        if 'kpiid' in data.keys() and 'queryitem' in data.keys() and data['kpiid'] is not None\
                and data['kpiid'] != '':
            qs = querydao.getquery(data['kpiid'], data['queryitem'])
        else:
            return render.mdxquery([])
        plain_text = ""
        for q in qs:
            plain_text += "<b>KPI ID</b>:"+ str(q.kpiid) + "&nbsp&nbsp&nbsp&nbsp&nbsp<b>Part</b>:" + str(q.part) + "<br />"
            plain_text += "<textarea style='HEIGHT: 600px; WIDTH: 900px'>" + q.query + "</textarea><br />"
        return plain_text

    def POST(self):
        data = web.input()
        querydao = getRuntimeDAO(data, 'querydao')
        if 'kpiid' in data.keys() and 'queryitem' in data.keys() and data['kpiid'] is not None\
                and data['kpiid'] != '':
            qs = querydao.getquery(data['kpiid'], data['queryitem'])
        else:
            qs = []
        return render.mdxquery(qs)

class ExecLog:
    def GET(self):
        return render.execlog([])

    def POST(self):
        data = web.input()
        execlogdao = getRuntimeDAO(data, 'execlogdao')
        #print data.keys()
        if 'top' in data.keys():
            bool_ifalllog = 'ifalllog' in data.keys()
            logs = execlogdao.loadlogs(int(data['top']), bool_ifalllog)
        else:
            logs = []
        return render.execlog(logs)


class Dim:
    def GET(self):
        data = web.input()
        dimdao = getRuntimeDAO(data, 'dimdao')
        geos = dimdao.LoadDimGeography()
        products = dimdao.LoadDimProduct()
        deliverysites = dimdao.LoadDimDeliverySite()
        teams = dimdao.LoadDimTeam()
        times = dimdao.LoadDimFiscalTime()
        ps = dimdao.LoadDimPubSector()
        fun = dimdao.LoadDimFunction()
        pcg = dimdao.LoadDimPCGeography()
        return render.dim(geos, products, deliverysites, teams, times, ps, fun, pcg)


class VerifyKPI:
    def GET(self, t):
        data = web.input()
        if str(t).upper() == 'T4':
            return render.T4verifykpi([])
        elif str(t).upper() == 'DE':
            return render.DeliveryExcellence([])
        else:
            raise Exception('Unknown Parameter: ' + str(t))


class VerifyKPIJson:
    def GET(self):
        data = web.input()
        verifykpidao = getRuntimeDAO(data, 'verifykpidao')
        if str(data['type']).upper() == 'DE':
            return self.DEhandler(data, verifykpidao)
        elif str(data['type']).upper() == 'T4':
            return self.T4handler(data, verifykpidao)

    def T4handler(self, data, verifykpidao):
        if 'dashboard' in data.keys():
            dashboard = data['dashboard']
            fiscaltime = data['fiscaltime']
            geography = data['geography']
            product = data['product']
            deliverysite = data['deliverysite']
            publicsector = data['pubsector']
            kpis = verifykpidao.t4loadkpivalues(dashboard, fiscaltime, geography, product, deliverysite, publicsector)
            return json.dumps([kpi.__dict__ for kpi in kpis])

    def DEhandler(self, data, verifykpidao):
        if 'fiscaltime' in data.keys():
            fiscaltime = data['fiscaltime']
            profitcenterid = data['profitcenterid']
            deliverysite = data['deliverysite']
            function = data['function']
            usedeliverysite = int(data['usedeliverysite'])
            kpis = verifykpidao.DEloadkpivalues(fiscaltime, profitcenterid, deliverysite, function, usedeliverysite)
            return json.dumps([kpi.__dict__ for kpi in kpis])


# class SwitchDB:
#     def GET(self):
#         global current_connstr
#         return GetCurrentDBName(current_connstr)
#
#     def POST(self):
#         '''
#         servername = web.ctx.env['HTTP_USER_AGENT']
#         '''
#         global current_connstr
#         data = web.input()
#         if 'db' in data:
#             if data['db'].lower() == 'prod':
#                 current_connstr = connstr_p
#             elif data['db'].lower() == 'dev':
#                 current_connstr = connstr_d
#             elif data['db'].lower() == 'us':
#                 current_connstr = connstr_us
#             createDAO()
#             createRender()
#             return 'Switch to ' + GetCurrentDBName(current_connstr)
#         return 'Argument Error.'


class AddNode:
    def GET(self):
        return render.addnode("", "", [])

    def POST(self):
        data = web.input()
        hierarchydao = getRuntimeDAO(data, 'hierarchydao')
        if not data['action']:
            return
        if data['action'].lower() == 'getnewid':
            r = str(data['root']).strip()
            n = str(data['nodepath']).strip()
            nodefamily = hierarchydao.getnewid(r, n)
            return render.addnode(r, n, nodefamily)


class Clipboard:
    def GET(self):
        return render.clipboard(remote_clipboard)

    def POST(self):
        data = web.input()
        if data['content']:
            remote_clipboard.append(data['content'].encode('utf-8'))
        return render.clipboard(remote_clipboard)


class GetFullIncrementMode:
    def GET(self):
        t = misdao_us.LoadFullIncrementMode()
        if t:
            return 'T4 Package Current Mode is ' + t[0] + ', updated on ' + t[1]
        else:
            return 'No mode info!'


class GetJobStatus:
    def GET(self):
        joblists = ['CDP_BootStrap',
                    'Sync',
                    'Cosmos_KPIValue_CTS_GPS_Daily',
                    'Cosmos_CommonTables_CTSLabor_Daily_CDP',
                    'Cosmos_CommonTables_CTSMSVoice_Daily_CDP',
                    'Cosmos_CommonTables_CTSDim_Daily_CDP',
                    'Cosmos_CommonTables_CTSServiceRequest_Daily_CDP',
                    'Cosmos_CommonTables_PFE_Daily_CDP']
        ts = misdao_us.LoadJobStatus(joblists)
        rs = []
        for t in ts:
            rs.append(self.jobqueryhandler(t))
        ts = misdao_prod.LoadJobStatus(['__DigIt_BootStrap_Daily'])
        for t in ts:
            rs.append(self.jobqueryhandler(t))
        #print json.dumps(rs)
        return json.dumps(rs)

    def jobqueryhandler(self, t):
        map_status={
            0: 'Returns only those jobs that are not idle or suspended.',
            1: 'Executing.',
            2: 'Waiting for thread.',
            3: 'Between retries.',
            4: 'Idle.',
            5: 'Suspended.',
            7: 'Performing completion a ctions.'
        }
        map_outcome ={
            0: 'Failed',
            1: 'Succeeded',
            3: 'Canceled',
            5: 'Unknown'
        }
        rs = {}
        if t:
            date = ''
            hms = ''
            for k in t.keys():
                kr = str(k).replace("_", " ")
                if k == 'current_execution_status':
                    rs[kr] = map_status[t[k]]
                elif k == 'last_run_outcome':
                    rs[kr] = map_outcome[t[k]]
                elif k == 'last_run_date':
                    date = str(t[k])[0:4] + "/" + str(t[k])[4:6] + "/" + str(t[k])[6:8]
                elif k == 'last_run_time':
                    if len(str(t[k])) == 6:
                        hms = str(t[k])[0:2] + ":" + str(t[k])[2:4] + ":" + str(t[k])[4:6]
                    else:
                        hms = str(t[k])[0:1] + ":" + str(t[k])[1:3] + ":" + str(t[k])[3:5]
                else:
                    rs[kr] = t[k]
            rs['last run datetime'] = date + " " + hms
        return rs


class BatchExec:
    def __init__(self):
        self.connstrlist = [
            ['v-rewei-pc(backend package dev environment,NO QUERYDB,NO TEMP)','Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=master;Integrated Security=SSPI;'],
            ['shlab-ossbi(frontend UI dev environment,NO StagingDB,NO TEMP)','Provider=SQLOLEDB.1;data source=shlab-ossbi;initial catalog=master;Integrated Security=SSPI;'],
            ['AZMSSGBSPDB02(staging environment,NO TEMP)','Provider=SQLOLEDB.1;data source=AZMSSGBSPDB02;initial catalog=master;Integrated Security=SSPI;'],
            ['gbs-cosmos-us(product)','Provider=SQLOLEDB.1;data source=gbs-cosmos-us;initial catalog=master;Integrated Security=SSPI;'],
            ['gbs-cosmos-prod(internal product,NO StagingDB)','Provider=SQLOLEDB.1;data source=gbs-cosmos-prod;initial catalog=master;Integrated Security=SSPI;']
        ]

    def GET(self):
        return render_plain.BatchExec(self.connstrlist, "", web.ctx.ip)

    def POST(self):
        data = web.input()
        if 'who' not in data.keys() or not data['who'] or str(data['who']).strip == '' or str(data['script']).strip == '':
            return render_plain.BatchExec(self.connstrlist, "Please fill the blank.", web.ctx.ip)
        else:
            slist = [str(data[k]).replace("master", str(data["dbsel"])) for k in data.keys() if k != 'who' and k!= 'script' and k != "dbsel"]
            rs = batchrunSqlDAO.RunBatch(slist, str(data['script']), data['who'])
            return render_plain.BatchExec(self.connstrlist, rs, web.ctx.ip)


class BackupSQL:
    def __init__(self):
        self.dblist = [
            "GBS_QueryDB", "GBS_QueryDB_Temp", "CDP_CommonDB", "CDP_CommonDB_Temp"
        ]
        self.mirrorpath = "\\\\gbs-cosmos-prod\\E$\\BACKUP\\FullBackUp"
        self.bkpath = "E:\\BACKUP\\FullBackUp"
        self.backuptpl = "BACKUP DATABASE {0} \n"\
                         "TO disk = '{1}' \n"\
                         "MIRROR TO disk = '{2}' \n"\
                         "WITH compression, init ,format"\

    def GET(self):
        rs = []
        for db in self.dblist:
            r = []
            id = backupSQLDAO.GetDB_id(db)
            r.append(id)
            r.append(db)
            r.append(self.FormatBackupSQL(db, id))
            rs.append(r)
        return render_plain.BackupSQL(self.bkpath, self.mirrorpath, rs)

    def GetDB_backup_name(self, dbname, dbid):
        if("query" in str(dbname).lower()):
            if (dbid == 8):
                return "GBS_DB_ID_6_full.bak"
            elif(dbid == 9):
                return "GBS_DB_ID_8_full.bak"
            else:
                raise ValueError("Unknown dbid: "+str(dbid))
        if ("common" in str(dbname).lower()):
            return "Cdp_CommonDB_Fullbackup_" + str(dbid) + ".bak"

    def FormatBackupSQL(self, dbname, dbid):
        bkname = self.GetDB_backup_name(dbname, dbid)
        bkfullname = ""
        mfullname = ""
        if(self.bkpath.endswith('\\')):
            bkfullname = self.bkpath + bkname
        else:
            bkfullname = self.bkpath + "\\" + bkname
        if(self.mirrorpath.endswith('\\')):
            mfullname = self.mirrorpath+ bkname
        else:
            mfullname = self.mirrorpath + "\\" + bkname
        return self.backuptpl.format(dbname, bkfullname, mfullname)


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()