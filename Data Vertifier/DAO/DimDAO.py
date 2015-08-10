__author__ = 'v-rewei'

import DAO.SqlServerDAO


class DimDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(DimDAO, self).__init__(connstr)

    def LoadData2Col(self, sql):
        rs = []
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs

    def LoadDimGeography(self):
        rs = []
        sql = 'SELECT [GeographyID],[FullName],[DisplayHierachy] FROM [GBS_StagingDB].[dashboard].[DimGeography]'
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs

    def LoadDimProduct(self):
        rs = []
        sql = 'SELECT [ProductID],[ProductName] FROM [GBS_StagingDB].[dashboard].[DimProduct]'
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs

    def LoadDimDeliverySite(self):
        rs = []
        sql = 'SELECT [DeliverySiteID],[DeliverySiteName] FROM [GBS_StagingDB].[dashboard].[DimDeliverySite]'
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs

    def LoadDimTeam(self):
        rs = []
        sql = 'SELECT [TeamID],[Name] FROM [GBS_StagingDB].[dashboard].[DimTeam]'
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs

    def LoadDimFiscalTime(self):
        rs = []
        sql = ('SELECT [FiscalPeriodID] ,'
                '[FiscalYearName]+\'FM\'+ case when [FiscalMonth]<10 then \'0\''
                '+cast([FiscalMonth] as varchar(3)) else cast([FiscalMonth] as varchar(3)) end'
                ',[FiscalYearName]+ ' '+[FiscalMonthName]'
                'FROM [GBS_StagingDB].[dashboard].[DimFiscalPeriod]')
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs

    def LoadDimPubSector(self):
        rs = []
        sql = ('SELECT  [PublicSectorID],[PublicSectorName] '
               'FROM [GBS_StagingDB].[dashboard].[DimPublicSector]')
        self.connect()
        cursor = self.conn.cursor()
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
            self.closeconnect()
            return rs


    def LoadDimFunction(self):
        sql = 'select functionid, FunctionName from dashboard.DimFunction'
        return self.LoadData2Col(sql)


    def LoadDimPCGeography(self):
        sql = 'select PCGeographyID, FullName from dashboard.DimPCGeography'
        return self.LoadData2Col(sql)
