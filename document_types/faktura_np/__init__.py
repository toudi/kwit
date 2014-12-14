from core.dialogs import DIALOG_DOCUMENTS_LIST

NAZWA = 'Faktura NP'

from document_types.faktura_np.models import FakturaNP
from document_types.faktura_np.dialogs.edit import EditNPInvoice

MODEL = FakturaNP


def register(window):
    if window.WINDOW_TYPE == DIALOG_DOCUMENTS_LIST:
        window.tbCreate.clicked.connect(edit_np_invoice(window))


def edit_np_invoice(parent):
    def inner():
        return EditNPInvoice(parent=parent).exec()
    return inner
