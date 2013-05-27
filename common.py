import os
import dataset
import logging
import unicodedata

database_url = os.environ.get('DATABASE_URL')
engine = dataset.connect(database_url)
dealings = engine.get_table('dealings')

logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)


def normalize_key(k):
    k = k.replace('.', '')
    k = k.replace('/', '_')
    k = k.replace('-', '_')
    k = k.replace(' ', '_').decode('latin-1')
    return unicodedata.normalize('NFKD', k).encode('ASCII', 'ignore')
