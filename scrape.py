import logging
import requests
from urlparse import urljoin
from pprint import pprint
from lxml import html
import csv

from common import dealings, normalize_key

log = logging.getLogger(__name__)

URL = 'http://ww2.bafin.de/database/DealingsInfo/sucheForm.do'

QUERY = {
    'emittentIsin': '',
    'emittentName': '',
    'meldepflichtigerName': '',
    'meldepflichtigerButton': 'Suche Meldepflichtiger',
    'zeitraum': 2,
    'zeitraumVon': '',
    'zeitraumBis': ''
}


def scrape():
    session = requests.Session()
    res = session.post(URL, data=QUERY)
    a = html.fromstring(res.content).find('.//div[@class="exportlinks"]//a')
    res = session.get(urljoin(URL, a.get('href')))
    for row in csv.DictReader(res.iter_lines(), delimiter=';'):
        data = {}
        for k, v in row.items():
            if k is None:
                continue
            if 'DOCTYPE' in k:
                return
            data[normalize_key(k)] = v.decode('latin-1')
        dealings.upsert(data, ['BaFin_ID'])
        #stringer.submit(data)

if __name__ == '__main__':
    scrape()
