__author__ = 'v-rewei'
import web
import DAO.QueryDAO
import DAO.ExecLogDAO
import DAO.DimDAO
import DAO.KPIValueDAO
import DAO.HierarchyDAO
import json

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
    '/getfimode/', 'GetFullIncrementMode'
)

remote_clipboard = []

def GetCurrentDBName(connstr):
    import re
    p = re.search('data source=([\w-]+);', connstr)
    return p.group(1)

connstr_d = 'Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_p = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-prod;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
connstr_us = 'Provider=SQLOLEDB.1;data source=gbs-cosmos-us;initial catalog=GBS_StagingDB;Integrated Security=SSPI;'
current_connstr = connstr_d
render = web.template.render('templates', base='layout', globals={"connstr": GetCurrentDBName(current_connstr)})
render_plain = web.template.render('templates', globals={"connstr": GetCurrentDBName(current_connstr)})

querydao = DAO.QueryDAO.QueryDAO(current_connstr)
execlogdao = DAO.ExecLogDAO.ExecLogDAO(current_connstr)
dimdao = DAO.DimDAO.DimDAO(current_connstr)
verifykpidao = DAO.KPIValueDAO.KPIValueDAO(current_connstr)
hierarchydao = DAO.HierarchyDAO.HierarchyDAO(current_connstr)


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
        global querydao, execlogdao, dimdao, verifykpidao,current_connstr,render,render_plain, hierarchydao
        data = web.input()
        if 'db' in data:
            if data['db'].lower() == 'production':
                current_connstr = connstr_p
            elif data['db'].lower() == 'dev':
                current_connstr = connstr_d
            elif data['db'].lower() == 'us':
                current_connstr = connstr_us
            querydao = DAO.QueryDAO.QueryDAO(current_connstr)
            execlogdao = DAO.ExecLogDAO.ExecLogDAO(current_connstr)
            dimdao = DAO.DimDAO.DimDAO(current_connstr)
            verifykpidao = DAO.KPIValueDAO.KPIValueDAO(current_connstr)
            hierarchydao = DAO.HierarchyDAO.HierarchyDAO(current_connstr)
            render = web.template.render('templates', base='layout', globals={"connstr": GetCurrentDBName(current_connstr)})
            render_plain = web.template.render('templates', globals={"connstr": GetCurrentDBName(current_connstr)})
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


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()