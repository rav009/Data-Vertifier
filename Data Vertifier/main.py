__author__ = 'v-rewei'
import web
import DAO.QueryDAO
import DAO.ExecLogDAO
import DAO.DimDAO
import DAO.KPIValueDAO
import DAO.HierarchyDAO
import DAO.BatchRunSqlDAO
import json

#global variables and functions
urls = (
    '/', 'Index',
    '/index', 'Index',
    '/index/', 'Index',
    '/mdxquery/(.*)', 'MDXQuery',
    '/execlog/', 'ExecLog',
    '/dim/', 'Dim',
    '/verifykpi/(.+)', 'VerifyKPI',
    '/verifykpijson/', 'VerifyKPIJson',
    '/switchdb/', 'SwitchDB',
    '/addnode/', 'AddNode',
    '/clipboard/', 'Clipboard',
    '/getfimode/', 'GetFullIncrementMode',
    '/batchexec/', 'BatchExec'
)

remote_clipboard = []

connstr_d = 'Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_p = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-prod;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_us = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-us;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
current_connstr = connstr_us

def GetCurrentDBName(connstr):
    import re
    p = re.search('data source=([\w-]+);', connstr)
    return p.group(1)


def createDAO():
    global querydao
    querydao = DAO.QueryDAO.QueryDAO(current_connstr)
    global execlogdao
    execlogdao = DAO.ExecLogDAO.ExecLogDAO(current_connstr)
    global dimdao
    dimdao = DAO.DimDAO.DimDAO(current_connstr)
    global verifykpidao
    verifykpidao = DAO.KPIValueDAO.KPIValueDAO(current_connstr)
    global hierarchydao
    hierarchydao = DAO.HierarchyDAO.HierarchyDAO(current_connstr)
    global batchrunSqlDAO
    batchrunSqlDAO = DAO.BatchRunSqlDAO.BatchRunSqlDAO()


def createRender():
    global render
    render = web.template.render('templates', base='layout', globals={"connstr": GetCurrentDBName(current_connstr)})
    global render_plain
    render_plain = web.template.render('templates', globals={"connstr": GetCurrentDBName(current_connstr)})


createDAO()
createRender()

#PageClass begin
class Index:
    def GET(self):
        return render_plain.index()


class MDXQuery:
    def GET(self, d):
        data = web.input()
        if 'kpiid' in data.keys() and 'queryitem' in data.keys() and data['kpiid'] is not None\
                and data['kpiid'] != '':
            qs = querydao.getquery(data['kpiid'], data['queryitem'])
        else:
            qs = []
        return render.mdxquery(qs)

    def POST(self, d):
        data = web.input()
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
        #print data.keys()
        if 'top' in data.keys():
            bool_ifalllog = 'ifalllog' in data.keys()
            logs = execlogdao.loadlogs(int(data['top']), bool_ifalllog)
        else:
            logs = []
        return render.execlog(logs)


class Dim:
    def GET(self):
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
        if str(t).upper() == 'T4':
            return render.T4verifykpi([])
        else:
            return render.T5verifykpi([])

    def POST(self, t):
        data = web.input()
        if str(t).upper() == 'T5':
            return self.T5handler(data)
        else:
            return self.T4handler(data)

    #def T5handler(self, data):
    #    if 'dashboard' in data.keys():
    #        dashboard = data['dashboard']
    #        fiscaltime = data['fiscaltime']
    #        geography = data['geography']
    #        product = data['product']
    #        deliverysite = data['deliverysite']
    #        team = data['team']
    #        kpis = verifykpidao.t5loadkpivalues(dashboard, fiscaltime, geography, product, deliverysite, team)
    #    else:
    #        kpis = []
    #    return render.T5verifykpi(kpis)

    def T4handler(self, data):
        if 'dashboard' in data.keys():
            dashboard = data['dashboard']
            fiscaltime = data['fiscaltime']
            geography = data['geography']
            product = data['product']
            deliverysite = data['deliverysite']
            publicsector = data['pubsector']
            kpis = verifykpidao.t4loadkpivalues(dashboard, fiscaltime, geography, product, deliverysite, publicsector)
        else:
            kpis = []
        return render.T4verifykpi(kpis)


class VerifyKPIJson:
    def GET(self):
        data = web.input()
        if str(data['type']).upper() == 'T5':
            return self.T5handler(data)
        else:
            return self.T4handler(data)

    #def T5handler(self, data):
    #    if 'dashboard' in data.keys():
    #        dashboard = data['dashboard']
    #        fiscaltime = data['fiscaltime']
    #        geography = data['geography']
    #        product = data['product']
    #        deliverysite = data['deliverysite']
    #        team = data['team']
    #        kpis = verifykpidao.t5loadkpivalues(dashboard, fiscaltime, geography, product, deliverysite, team)
    #        return json.dumps([kpi.__dict__ for kpi in kpis])

    def T4handler(self, data):
        if 'dashboard' in data.keys():
            dashboard = data['dashboard']
            fiscaltime = data['fiscaltime']
            geography = data['geography']
            product = data['product']
            deliverysite = data['deliverysite']
            publicsector = data['pubsector']
            kpis = verifykpidao.t4loadkpivalues(dashboard, fiscaltime, geography, product, deliverysite, publicsector)
            return json.dumps([kpi.__dict__ for kpi in kpis])


    def DEhandler(self, data):
        return 'Page in building.'


class SwitchDB:
    def GET(self):
        global current_connstr
        return GetCurrentDBName(current_connstr)

    def POST(self):
        '''
        servername = web.ctx.env['HTTP_USER_AGENT']
        '''
        global current_connstr
        data = web.input()
        if 'db' in data:
            if data['db'].lower() == 'prod':
                current_connstr = connstr_p
            elif data['db'].lower() == 'dev':
                current_connstr = connstr_d
            elif data['db'].lower() == 'us':
                current_connstr = connstr_us
            createDAO()
            createRender()
            return 'Switch to ' + GetCurrentDBName(current_connstr)
        return 'Argument Error.'




class AddNode:
    def GET(self):
        return render.addnode("", "", [])

    def POST(self):
        data = web.input()
        if not data['action']:
            return
        if data['action'].lower() == 'getnewid':
            r = str(data['root']).strip()
            n = str(data['nodepath']).strip()
            nodefamily = self.Getnewid(r, n)
            return render.addnode(r, n, nodefamily)

    def Getnewid(self, root, nodepath):
        return hierarchydao.getnewid(root, nodepath)


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
        t = dimdao.LoadFullIncrementMode()
        if t:
            return 'Current Mode is ' + t[0] + ', update on ' + t[1]
        else:
            return 'No mode info!'


class BatchExec:
    def __init__(self):
        self.connstrlist = [
            ['v-rewei-pc(backend package dev environment,NO QUERYDB,NO TEMP)','Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=master;Integrated Security=SSPI;'],
            ['shlab-ossbi(frontend UI dev environment,NO TEMP)','Provider=SQLOLEDB.1;data source=shlab-ossbi;initial catalog=master;Integrated Security=SSPI;'],
            ['gbs-sandbox(staging environment,NO TEMP)','Provider=SQLOLEDB.1;data source=gbs-sandbox;initial catalog=master;Integrated Security=SSPI;'],
            ['gbs-cosmos-us(product)','Provider=SQLOLEDB.1;data source=gbs-cosmos-us;initial catalog=master;Integrated Security=SSPI;'],
            ['gbs-cosmos-prod(internal product)','Provider=SQLOLEDB.1;data source=gbs-cosmos-prod;initial catalog=master;Integrated Security=SSPI;']
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


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()