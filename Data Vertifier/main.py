__author__ = 'v-rewei'

import sys
daolib = "D:\\tmp-program\\Data Vertifier\\Data Vertifier\\"
if not daolib in sys.path:
    sys.path.insert(0, daolib)

import web
import DAO.QueryDAO
import DAO.ExecLogDAO
import DAO.DimDAO
import DAO.KPIValueDAO
import DAO.HierarchyDAO
import DAO.BatchRunSqlDAO
import DAO.BackupSQLDAO
import DAO.MiscellaneousDAO

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
    '/mdxquery/', 'CDP_handler.MDXQuery',
    '/execlog/', 'CDP_handler.ExecLog',
    '/dim/', 'CDP_handler.Dim',
    '/verifykpi/(.+)', 'CDP_handler.VerifyKPI',
    '/verifykpijson/', 'CDP_handler.VerifyKPIJson',
    '/switchdb/', 'CDP_handler.SwitchDB',
    '/addnode/', 'CDP_handler.AddNode',
    '/clipboard/', 'CDP_handler.Clipboard',
    '/getfimode/', 'CDP_handler.GetFullIncrementMode',
    '/getjobstatus/', 'CDP_handler.GetJobStatus',
    '/batchexec/', 'CDP_handler.BatchExec',
    '/backupsql/', 'CDP_handler.BackupSQL',
    '/csadim/', 'CSA_handler.CSADim'
)

connstr_d = 'Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_p = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-prod;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_us = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-us;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_csa = 'Provider=SQLOLEDB.1;data source=mastvm03;initial catalog=CSA_DM;Integrated Security=SSPI;'

def GetCurrentDBName(connstr):
    import re
    p = re.search('data source=([\w-]+);', connstr)
    return p.group(1)

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


global render
render = web.template.render('D:\\tmp-program\\Data Vertifier\\Data Vertifier\\templates', base='layout')
global render_plain
render_plain = web.template.render('D:\\tmp-program\\Data Vertifier\\Data Vertifier\\templates', globals={"str":str})
global remote_clipboard
remote_clipboard = []
global batchrunSqlDAO
batchrunSqlDAO = DAO.BatchRunSqlDAO.BatchRunSqlDAO()
global backupSQLDAO
backupSQLDAO = DAO.BackupSQLDAO.BackupSQLDAO(connstr_us)
global misdao_us
misdao_us = DAO.MiscellaneousDAO.MiscellaneousDAO(connstr_us)
global misdao_prod
misdao_prod = DAO.MiscellaneousDAO.MiscellaneousDAO(connstr_p)

class icon:
    def GET(self):
        raise web.seeother("/static/favicon.ico")

class Index:
    def GET(self):
        return render_plain.index()


application = web.application(urls, globals()).wsgifunc()
