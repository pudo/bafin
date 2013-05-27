from datastringer import DataStringer
from common import dealings
import urllib


def submit_all():
    stringer = DataStringer(host='http://localhost:5000', service='foerderkatalog', event='project')
    for row in list(dealings.find(datawire_submitted=False)):
        if 'datawire_submitted' in row:
            del row['datawire_submitted']
        row['source_url'] = URL_BASE % urllib.quote_plus(row['fkz'])
        stringer.submit(row)
        upd = {'datawire_submitted': True, 'fkz': row['fkz']}
        dealings.update(upd, ['fkz'])


if __name__ == '__main__':
    submit_all()
