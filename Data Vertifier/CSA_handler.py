__author__ = 'v-rewei'
import web
import main
import DAO.DimDAO

class CSADim:
    def GET(self):
        dimdao = DAO.DimDAO.CSA_DimDAO(main.connstr_csa)
        measures = dimdao.LoadMeasure()
        return main.render_plain.csadim(measures)