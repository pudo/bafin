from datastringer import DataStringer
from datetime import datetime
from common import URL, dealings
import urllib


def date(row):
    try:
        data = row.get('Veroffentlichungsdatum')
        return datetime.strptime(data, '%d.%m.%Y')
    except:
        return


def submit_all():
    stringer = DataStringer(service='bafindealings', event='notice')
    for row in list(dealings.find()):
        if 'datawire_submitted' in row:
            if row['datawire_submitted']:
                continue
            del row['datawire_submitted']
            #continue
        stringer.submit(row, source_url=URL, action_at=date(row))
        upd = {'datawire_submitted': True, 'BaFin_ID': row['BaFin_ID'], 'Meldungsnr': row['Meldungsnr']}
        dealings.update(upd, ['BaFin_ID', 'Meldungsnr'])


if __name__ == '__main__':
    submit_all()
