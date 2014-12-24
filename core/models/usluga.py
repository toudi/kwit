from core.utils.qvariantalchemy import String, Integer, Boolean 
from sqlalchemy import Column
from core.models.abstract import AbstractModel


class Usluga(AbstractModel):
    __tablename__ = 'kwit_uslugi'

    DISPLAY_COLUMN = 'nazwa'

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)
    jednostka = Column(String)
    cena_netto = Column(String)
    podatek = Column(String)

    @staticmethod
    def get_header_columns():
        return [
            ('ID', Usluga.id, 'id', {'editable': False}),
            ('Nazwa', Usluga.nazwa, 'nazwa', {'editable': True}),
        ]
