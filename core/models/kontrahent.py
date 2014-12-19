from core.utils.qvariantalchemy import String, Integer, Boolean
from sqlalchemy import Column
from core.models.abstract import AbstractModel


class Kontrahent(AbstractModel):
    __tablename__ = 'kwit_kontrahenci'

    DISPLAY_COLUMN = 'nazwa'

    id    = Column(Integer, primary_key=True)
    nazwa = Column(String)
    nip   = Column(String)
    adres = Column(String)
    sprzedawca = Column(Boolean, default=False)

    @staticmethod
    def get_header_columns():
        return [
            ('ID', Kontrahent.id, 'id', {'editable': False}),
            ('Nazwa kontrahenta', Kontrahent.nazwa, 'nazwa', {'editable': True}),
            ('NIP', Kontrahent.nip, 'nip', {}),
            ('Adres', Kontrahent.adres, 'adres', {}),
        ]

class Klient(Kontrahent):
    @classmethod
    def _query(cls, basequery):
        return basequery.filter(Kontrahent.sprzedawca == False)

class Sprzedawca(Kontrahent):
    @classmethod
    def _query(cls, basequery):
        return basequery.filter(Kontrahent.sprzedawca == True)
