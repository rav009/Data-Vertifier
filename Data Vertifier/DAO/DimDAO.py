__author__ = 'v-rewei'

import DAO.SqlServerDAO


class DimDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(DimDAO, self).__init__(connstr)

    def LoadData2Col(self, sql):
        rs = []
        conn = self.returnconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                rs.append((row[0], row[1]))
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            conn.close()
            return rs

    def LoadDimGeography(self):
        rs = []
        sql = 'SELECT [GeographyID],[FullName],[DisplayHierachy] FROM [GBS_StagingDB].[dashboard].[DimGeography]'
        conn = self.returnconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                rs.append((row[0], row[1], row[2]))
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            conn.close()
            return rs

    def LoadDimProduct(self):
        sql = 'SELECT [ProductID],[ProductName] FROM [GBS_StagingDB].[dashboard].[DimProduct]'
        return self.LoadData2Col(sql)

    def LoadDimDeliverySite(self):
        sql = 'SELECT [DeliverySiteID],[DeliverySiteName] FROM [GBS_StagingDB].[dashboard].[DimDeliverySite]'
        return self.LoadData2Col(sql)

    def LoadDimTeam(self):
        sql = 'SELECT [TeamID],[Name] FROM [GBS_StagingDB].[dashboard].[DimTeam]'
        return self.LoadData2Col(sql)

    def LoadDimFiscalTime(self):
        rs = []
        sql = ('SELECT [FiscalPeriodID] ,'
                '[FiscalYearName]+\'FM\'+ case when [FiscalMonth]<10 then \'0\''
                '+cast([FiscalMonth] as varchar(3)) else cast([FiscalMonth] as varchar(3)) end'
                ',[FiscalYearName]+ ' '+[FiscalMonthName]'
                'FROM [GBS_StagingDB].[dashboard].[DimFiscalPeriod]')
        conn = self.returnconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                rs.append((row[0], row[1], row[2]))
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            conn.close()
            return rs

    def LoadDimPubSector(self):
        sql = ('SELECT  [PublicSectorID],[PublicSectorName] '
               'FROM [GBS_StagingDB].[dashboard].[DimPublicSector]')
        return self.LoadData2Col(sql)

    def LoadDimFunction(self):
        sql = 'select functionid, FunctionName from dashboard.DimFunction'
        return self.LoadData2Col(sql)


    def LoadDimPCGeography(self):
        sql = 'select PCGeographyID, FullName from dashboard.DimPCGeography'
        return self.LoadData2Col(sql)
