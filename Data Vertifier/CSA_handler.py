__author__ = 'v-rewei'
import web
import main
import DAO.DimDAO
import DAO.TestQueryDAO

class CSADim:
    def GET(self):
        dimdao = DAO.DimDAO.CSA_DimDAO(main.connstr_csa)
        measures = dimdao.LoadMeasure()
        geos = dimdao.LoadDimGeography()
        products= dimdao.LoadDimProduct()
        customeraudience = dimdao.LoadCustomerAudience()
        cloudfilter = dimdao.LoadCloudOnPremiseFilter()
        lifecycle = dimdao.LoadLifecycle()
        targetversion = dimdao.LoadTargetVersion()
        datasource = dimdao.LoadDataSource()
        supporttype = dimdao.LoadSupportType()
        costallocation = dimdao.LoadCSSCostAllocation()
        fingeo = dimdao.LoadFinanceGeo()
        return main.render_plain.csadim(measures, geos, products, customeraudience, cloudfilter, lifecycle,
                                        targetversion, datasource, supporttype, costallocation, fingeo)

class CSAQueryTest:
    def GET(self):
        return main.render_plain.testquery([])

    def POST(self):
        dao = DAO.TestQueryDAO.TestQueryDAO(main.connstr_csa)
        data = web.input()
        if data['keyword']:
            qs = dao.LoadTestQuery(str(data['keyword']))
            return main.render_plain.testquery(qs)
        else:
            return main.render_plain.testquery([])
