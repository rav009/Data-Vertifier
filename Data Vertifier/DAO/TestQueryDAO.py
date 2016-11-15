__author__ = 'v-rewei'


import DAO.SqlServerDAO

class TestQueryDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(TestQueryDAO, self).__init__(connstr)

    def LoadTestQuery(self, keyword):
        sql = '''SELECT [ID]
            ,[Name]
            ,[Category]
            ,[QueryString1] +\'|\' +[ConnectString1]
            ,[QueryString2] +\'|\' +[ConnectString2]
            ,[QueryString3] +\'|\' +[ConnectString3]
            ,[QueryString4] +\'|\' +[ConnectString4]
            ,[QueryString5] +\'|\' +[ConnectString5]
            ,[QueryString6] +\'|\' +[ConnectString6]
            ,[QueryString7] +\'|\' +[ConnectString7]
            ,[QueryString8] +\'|\' +[ConnectString8]
            ,[QueryString9] +\'|\' +[ConnectString9]
            ,[QueryString10]+\'|\'+[ConnectString10]
            FROM [CSA_QA].[dbo].[AcceptenceTestCase] where ID like \'%?%\' or name like \'%?%\' or category like \'%?%\''''
        sql = sql.replace('?', keyword)
        print sql
        rs = []
        conn = self.returnconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                rs.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                           row[10], row[11], row[12]))
                row = cursor.fetchone()
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            conn.close()
            return rs
