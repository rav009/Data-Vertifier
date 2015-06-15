__author__ = 'v-rewei'

import DAO.SqlServerDAO

class HierarchyDAO(DAO.SqlServerDAO.SqlServerDAO):
    def __init__(self, connstr):
        super(HierarchyDAO, self).__init__(connstr)

    def getnewid(self, root, nodepath):
        ns = [n for n in nodepath.split('/') if n != '']
        if len(ns) == 0:
            raise Exception('Given nodepath has no nodes:'+ nodepath)
        rs = [(self.getnodenamebyid(root), root, 0)]
        return self.getnodeid(root, ns, 0, rs)

    def getnodenamebyid(self, hid):
        sql = u'SELECT [NodeValue] FROM [GBS_StagingDB].[selfboard].[Hierarchy] where' \
             ' [Hierarchyid] = hierarchyid::Parse(\'{0}\')'.format(hid)
        #print sql
        rs = self.getone(sql)
        if not rs:
            raise Exception('The hierarchyid can\'t be found in the Hierarchy table:' + hid)
        return rs

    def getnodeid(self, root, ns, i, nodefamily):
        if len(ns) == i:
            return nodefamily
        else:
            n = ns[i]
            i += 1
            newroot = self.getnodebyfatherandname(root, n)
            nodefamily.append((n, newroot[0],newroot[1]))
            return self.getnodeid(newroot[0], ns, i, nodefamily)

    def getnodebyfatherandname(self, fathernodeid, name):
        sql= ('SELECT [HierarchyId].ToString() FROM [GBS_StagingDB].[selfboard].[Hierarchy] where '
             'Nodevalue like \'{0}\' and '
             '[HierarchyId].IsDescendantOf(hierarchyid::Parse(\'{1}\'))=1 and '
             '[HierarchyId].GetLevel()-hierarchyid::Parse(\'{1}\').GetLevel()=1').format(name, fathernodeid)
        hid = self.getone(sql)
        if hid:
            return hid, 0
        else:
            sql= ('select '
                  '[selfboard].[GetAvaiableHierarchyID](hierarchyid::Parse(\'{0}\')).ToString()').format(fathernodeid)
            hid = self.getone(sql)
            sql = ('insert into [selfboard].[Hierarchy] '
                  'select hierarchyid::Parse(\'{0}\'),\'{1}\',0').format(hid, name)
            self.execsql(sql)
            return hid, sql
