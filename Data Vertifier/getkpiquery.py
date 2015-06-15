import DAO.QueryDAO
import win32clipboard as wincb
import win32con


connstr = 'Provider=SQLOLEDB.1;data source=v-rewei-pc;initial catalog=GBSDashboardDB_Staging;Integrated Security=SSPI;'
d = DAO.QueryDAO.QueryDAO(connstr)

def copytowin(copystr):
    if copystr is None:
        raise 'Copy str is null'
    wincb.OpenClipboard()
    wincb.EmptyClipboard()
    wincb.SetClipboardData(win32con.CF_TEXT, copystr)
    wincb.CloseClipboard()

if __name__=='__main__':
    while True:
        gid=input('Please input general id:')
        sid=input('Please input special id:')
        copystr = d.GetQuery(gid, sid)
        if copystr is None:
            print 'None KPI query found.'
            continue
        print copystr
        copytowin(copystr)
        print "Query has been copied into your Clipboard."