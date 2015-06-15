__author__ = 'wei'

import adodbapi

def testconnstr(connstr):
    try:
        conn = adodbapi.connect(connstr)
    except Exception as ext:
        return False
    conn.close()
    return True

def sqlparamhandler(sqlparam):
    if sqlparam is None:
        return 'NULL'
    elif type(sqlparam) is str:
        sqlparam=sqlparam.replace('\'', '')
        return '\''+sqlparam+'\''
    else:
        return str(sqlparam)