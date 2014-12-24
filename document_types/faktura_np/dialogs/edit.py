from core.dialogs.abstract import AbstractWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os.path import dirname
from plugins.nbp import NBPCurrency
from decimal import Decimal
from slownie import *
from core.models.kontrahent import Sprzedawca
from document_types.faktura_np.models import FakturaNP
from document_types.faktura_np.models import FakturaNPPozycja
from core.models.kontrahent import Klient
from core.models.usluga import Usluga
from core.utils.tablemodel import TableModel, ComboDelegate

form_class = uic.loadUiType("%s/np_edit.ui" % dirname(__file__))[0]


class NPInvoiceItemModel(TableModel):
    recalculate_prices = pyqtSignal(QModelIndex)

    def __init__(self, *args, **kwargs):
        super(NPInvoiceItemModel, self).__init__(*args, **kwargs)
        self.columns = (
            ('usluga', 'Usługa'),
            ('cena_pln', 'Cena (PLN)'),
            ('cena_waluta', 'Cena (waluta obca)'),
        )
        self.model_mapping = {
            'usluga': Usluga
        }

    def setData(self, index, value, role):
        row = index.row()
        column = index.column()

        if value is not None:
            if role == Qt.EditRole:
                if self.getColName(column) == 'usluga':
                    if self.items[row].get('cena') is None:
                        cena = Usluga.get_qmodel_class().get_by_id(value, 'cena_netto')
                        self.setData(
                            self.createIndex(row, self.getColNum('cena_pln')),
                            cena,
                            Qt.EditRole
                        )


        out = super(NPInvoiceItemModel, self).setData(index, value, role)

        if self.getColName(column) == 'cena_pln':
            self.recalculate_prices.emit(index)

class EditNPInvoice(QDialog, form_class):
    def __init__(self, *args, **kwargs):
        self.value_total = Decimal('10000.23')
        super(EditNPInvoice, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.nbp = NBPCurrency()

        self.deIssued.setDate(QDate.currentDate())
        self.cbCurrency.currentIndexChanged.connect(self.calculate_currency)
        self.cbCurrency.currentIndexChanged.emit(0)
        self.deIssued.dateChanged.connect(self.calculate_currency)
        self.bb.rejected.connect(self.reject)
        self.cbWystawca.setModel(Sprzedawca.get_qmodel_class())
        self.cbKlient.setModel(Klient.get_qmodel_class())
        self.model = NPInvoiceItemModel()
        self.model.recalculate_prices.connect(self.recalculate_prices)
        self.model.registerEditors(self.tvFakturaNPPozycje)
        # self.tvFakturaNPPozycje = TableView(self)
        self.tvFakturaNPPozycje.setModel(self.model)
        self.pbDodaj.clicked.connect(self.dodajPozycje)

    def dodajPozycje(self):
        self.model.insertRows(0, 1, QModelIndex())

    def calculate_currency(self):
        info = self.nbp.get_currency_info(
            self.cbCurrency.currentText(),
            self.deIssued.date()
        )
        self.info = info
        self.lWaluta.setText('Razem (%s)' % self.cbCurrency.currentText())
        self.lKurs.setText(str(info.rate))
        self.lTabela.setText(info.codename)

        self.update_prices()

    def update_prices(self):
        self.value_total = Decimal(0)

        for rownum in range(self.model.rowCount(None)):
            self.value_total += Decimal(
                self.model.data(
                    self.model.createIndex(
                        rownum, self.model.getColNum('cena_waluta')
                    ),
                    Qt.EditRole
                )
            )

        reszta_waluta = self.value_total * 100 % 100
        self.lSlownieWaluta.setText(
            '%s, %d/100' % (
                slownie(self.value_total),
                int(reszta_waluta)
            )
        )
        pln = self.value_total * self.info.rate
        groszy = pln * 100 % 100
        self.lSlowniePLN.setText(
            '%s, %s' % (
                slownie(pln, unit=UNIT_ZLOTY),
                slownie(int(groszy), unit=UNIT_GROSZ)
            )

        )

    def recalculate_prices(self, index):
        cena = self.model.data(index, Qt.EditRole)
        cena_waluta = Decimal(cena) / Decimal(self.info.rate)
        cena_waluta = cena_waluta.quantize(Decimal('0.01'))
        cena_waluta_idx = self.model.createIndex(
            index.row(),
            self.model.getColNum('cena_waluta')
        )
        self.model.setData(cena_waluta_idx, str(cena_waluta), Qt.EditRole)

        self.update_prices()
