from core.dialogs.abstract import AbstractWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from os.path import dirname
from plugins.nbp import NBPCurrency
from decimal import Decimal
from slownie import *

form_class = uic.loadUiType("%s/np_edit.ui" % dirname(__file__))[0]
print(form_class)


class EditNPInvoice(QDialog, form_class):
    def __init__(self, *args, **kwargs):
        self.value_total = Decimal('10000.23')
        super(EditNPInvoice, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.nbp = NBPCurrency()

        self.cbCurrency.currentIndexChanged.connect(self.calculate_currency)
        self.cbCurrency.currentIndexChanged.emit(0)
        self.deIssued.dateChanged.connect(self.calculate_currency)
        self.bb.rejected.connect(self.reject)

    def calculate_currency(self):
        info = self.nbp.get_currency_info(
            self.cbCurrency.currentText(),
            self.deIssued.date()
        )
        self.lWaluta.setText('Razem (%s)' % self.cbCurrency.currentText())
        self.lKurs.setText(str(info.rate))
        self.lTabela.setText(info.codename)

        reszta_waluta = self.value_total * 100 % 100
        self.lSlownieWaluta.setText(
            '%s, %d/100' % (
                slownie(self.value_total),
                int(reszta_waluta)
            )
        )
        pln = self.value_total * info.rate
        groszy = pln * 100 % 100
        self.lSlowniePLN.setText(
            '%s, %s' % (
                slownie(pln, unit=UNIT_ZLOTY),
                slownie(int(groszy), unit=UNIT_GROSZ)
            )

        )
