import requests
from urlparse import urljoin
from pprint import pprint
from lxml import html
import csv
from normality import slugify

import dataset

URL = 'https://portal.mvp.bafin.de/database/DealingsInfo/sucheForm.do'
QUERY = {
    'emittentIsin': '',
    'emittentName': '',
    'meldepflichtigerName': '',
    'meldepflichtigerButton': 'Suche Meldepflichtiger',
    'zeitraum': 2,
    'zeitraumVon': '',
    'zeitraumBis': ''
}

engine = dataset.connect('sqlite:///data.sqlite')
dealings = engine.get_table('data')


def scrape():
    session = requests.Session()
    res = session.post(URL, data=QUERY, verify=False)
    a = html.fromstring(res.content).find('.//div[@class="exportlinks"]//a')
    res = session.get(urljoin(URL, a.get('href')), verify=False)
    for row in csv.DictReader(res.iter_lines(), delimiter=';'):
        data = {}
        for k, v in row.items():
            if k is None:
                continue
            if 'DOCTYPE' in k:
                return
            k = k.decode('latin-1')
            k = slugify(k, sep='_')
            data[k] = v.decode('latin-1')
        dealings.upsert(data, ['bafin_id', 'meldungsnr'])

if __name__ == '__main__':
    scrape()
