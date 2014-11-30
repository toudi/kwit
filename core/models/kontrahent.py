from core.utils.qvariantalchemy import String, Integer
from sqlalchemy import Column
from core.models.abstract import AbstractModel


class Kontrahent(AbstractModel):
    __tablename__ = 'kwit_kontrahenci'

    id    = Column(Integer, primary_key=True)
    nazwa = Column(String)
    nip   = Column(String)
    adres = Column(String)

    @staticmethod
    def get_header_columns():
        return [
            ('ID', Kontrahent.id, 'id', {'editable': False}),
            ('Nazwa kontrahenta', Kontrahent.nazwa, 'nazwa', {'editable': True}),
            ('NIP', Kontrahent.nip, 'nip', {}),
            ('Adres', Kontrahent.adres, 'adres', {}),
        ]
