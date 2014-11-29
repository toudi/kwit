from core.utils.qvariantalchemy import String, Integer
from sqlalchemy import Column
from core.models.abstract import AbstractModel


class Kontrahent(AbstractModel):
    __tablename__ = 'kwit_kontrahenci'

    id    = Column(Integer, primary_key=True)
    nazwa = Column(String)
    nip   = Column(String)

    @staticmethod
    def get_header_columns():
        return [
            ('Nazwa kontrahenta', Kontrahent.nazwa, 'nazwa', {'editable': True}),
            ('NIP', Kontrahent.nip, 'nip', {}),
        ]
