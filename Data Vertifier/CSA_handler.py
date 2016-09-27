__author__ = 'v-rewei'
import web
import main
import DAO.DimDAO

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
        deliverysites = dimdao.LoadDimDeliverySite()
        supporttype = dimdao.LoadSupportType()
        costallocation = dimdao.LoadCSSCostAllocation()
        return main.render_plain.csadim(measures, geos, products, customeraudience, cloudfilter, lifecycle, targetversion, datasource, deliverysites, supporttype, costallocation)