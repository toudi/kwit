import urllib.request
from lxml import etree
from datetime import datetime
from decimal import Decimal
from io import StringIO

EXCHANGE_RATES = 'http://www.nbp.pl/kursy/xml'


class CurrencyInfo(object):
    codename = None
    rate = None
    date = None


class NBPCurrency(object):
    def __init__(self):
        self.dirfile = None

    def get_currency_info(self, currency, date):
        table, date = self.get_exchange_table(date)
        # with urllib.request.urlopen(table) as xml:
        tree = etree.parse(table)
        root = tree.getroot()

        info = CurrencyInfo()
        info.date = date
        info.codename = root.find('./numer_tabeli').text
        info.rate = self.get_rate(root, currency)

        return info

    def get_exchange_table(self, date):
        if not self.dirfile:
            self.dirfile = StringIO(urllib.request.urlopen(
                '%s/dir.txt' % EXCHANGE_RATES).read().decode())
        self.dirfile.seek(0)
        for line in reversed(list(self.dirfile)):
            if line.strip().startswith('a'):
                _date = datetime.strptime(
                    line.strip()[5:], '%y%m%d').date()
                if _date < date:
                    return '%s/%s.xml' % (
                        EXCHANGE_RATES, line.strip()), _date

    def get_rate(self, root, currency):
        item = root.xpath(
            './pozycja/kod_waluty[text()="%s"]' % currency.upper())[0]
        return Decimal(
            item.getparent().find('./kurs_sredni').text.replace(',', '.'))
