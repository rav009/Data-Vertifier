__author__ = 'v-rewei'


class MDXQuery:
    def __init__(self, kpiid, query, datasourceid, part):
        self.kpiid = kpiid
        if not query.lower().strip().startswith('with') and self.kpiid:
            self.query = 'with \n' + query
        else:
            self.query = query
        self.datasourceid = datasourceid
        self.part = part