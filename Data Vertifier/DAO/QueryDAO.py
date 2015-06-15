__author__ = 'v-rewei'

import DAO.SqlServerDAO
import MODEL.MDXQuery

class QueryDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(QueryDAO, self).__init__(connstr)

    def getquery(self, kpiid, queryitem):
        rs = []
        sql = ('SELECT\n'
               '                [KPIID],\n'
               '                cast([QueryMemberMeasure] as varchar(1000)) [QueryMemberMeasure],\n'
               '                cast(B.[QueryMemberProduct] as varchar(8000)) [QueryMemberProduct],\n'
               '                cast([QueryMemberGeoNAOthers] as varchar(4000)) [QueryMemberGeoNAOthers],\n'
               '                cast([QueryMemberGeoLatamOthers] as varchar(4000)) [QueryMemberGeoLatamOthers],\n'
               '                cast([QueryMemberGeoCEEOthers] as varchar(4000)) [QueryMemberGeoCEEOthers],\n'
               '                cast([QueryMemberGeoFranceOthers] as varchar(4000)) [QueryMemberGeoFranceOthers],\n'
               '                cast([QueryMemberGeoGermanyOthers] as varchar(4000)) [QueryMemberGeoGermanyOthers],\n'
               '                cast([QueryMemberGeoMEAOthers] as varchar(4000)) [QueryMemberGeoMEAOthers],\n'
               '                cast([QueryMemberGeoUKOthers] as varchar(4000)) [QueryMemberGeoUKOthers],\n'
               '                cast([QueryMemberGeoWEOthers] as varchar(4000)) [QueryMemberGeoWEOthers],\n'
               '                cast([QueryMemberGeoAPACOthers] as varchar(4000)) [QueryMemberGeoAPACOthers],\n'
               '                cast([QueryMemberGeoGCROthers] as varchar(4000)) [QueryMemberGeoGCROthers],\n'
               '                cast([QueryMemberGeoIndiaOthers] as varchar(4000)) [QueryMemberGeoIndiaOthers],\n'
               '                cast([QueryMemberGeoJapanOthers] as varchar(4000)) [QueryMemberGeoJapanOthers],\n'
               '                cast([QueryMemberAllCountry] as varchar(8000)) [QueryMemberAllCountry],\n'
               '                cast(Isnull([QueryMemberDeliverySite],\' \') as varchar(4000)) [QueryMemberDeliverySite],\n'
               '                cast(isnull([QueryMemberQueue],\' \') as varchar(8000)) [QueryMemberQueue],\n'
               '                cast(isnull([QueryMemberTeam],\' \') as varchar(4000)) as [QueryMemberTeam],\n'
               '                cast(isnull([QueryPubSector], \'\') as varchar(6000)) as [QueryPubSector],\n'
               '                cast([QuerySelect] as varchar(6000)) [QuerySelect],\n'
               '                cast([QueryFrom] as varchar(200)) [QueryFrom],\n'
               '                cast(\'\'+[QueryWhere]+\'\' as varchar(4000)) [QueryWhere],\n'
               '                cast(B.[QueryWhereTime_MTD] as varchar(4000)) [QueryWhereTime_MTD],\n'
               '                cast(Isnull(B.[QueryWhereTime_YTD],\'\') as varchar(4000)) [QueryWhereTime_YTD],\n'
               '                cast(Isnull(B.[QueryWhereTime_Baseline],\'\') as varchar(4000)) [QueryWhereTime_Baseline],\n'
               '                A.DatasourceID,\n'
               '                B.[Part] [Part]\n'
               '                FROM [dashboard].[KPIQuery_General] A\n'
               '                JOIN [dashboard].[KPIQuery_Specific] B ON A.DatasourceID=B.DatasourceID\n'
               '                WHERE B.KPIID={0} ORDER BY [KPIID]'
        ).format(str(kpiid))
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        try:
            row = cursor.fetchone()
            while row is not None:
                tmp = []
                if str(queryitem).upper() == 'MTD':
                    for i in range(1, 24):
                        if row[i] is not None:
                            tmp.append(row[i].encode('utf-8').strip())
                elif str(queryitem).upper() == 'YTD':
                    for i in range(1, 23):
                        if row[i] is not None:
                            tmp.append(row[i].encode('utf-8').strip())
                    tmp.append(row[24].encode('utf-8').strip())
                else:
                    for i in range(1, 23):
                        if row[i] is not None:
                            tmp.append(row[i].encode('utf-8').strip())
                    tmp.append(row[25].encode('utf-8').strip())
                m = MODEL.MDXQuery.MDXQuery(int(row[0]), '\n'.join(tmp), int(row[26]), int(row[27]))
                rs.append(m)
                row = cursor.fetchone()
            #print len(rs)
        except Exception as ext:
            print ext.message
        finally:
            cursor.close()
            self.closeconnect()
            if not rs:
                m = MODEL.MDXQuery.MDXQuery(None, 'This KPI is not get by mdx', None, None)
                rs.append(m)
            return rs