from core.utils.qvariantalchemy import String, Integer, Boolean, DateTime
from sqlalchemy import Column, ForeignKey
from core.models.abstract import AbstractModel


class FakturaNP(AbstractModel):
    __tablename__ = 'kwit_faktury_np'

    id    = Column(Integer, primary_key=True)
    sprzedawca = Column(Integer, ForeignKey('kwit_kontrahenci.id'))
    nabywca = Column(Integer, ForeignKey('kwit_kontrahenci.id'))
    numer = Column(String)
    wystawiona = Column(DateTime)
    termin_platnosci = Column(DateTime)
    zaplacona = Column(Boolean)

    @staticmethod
    def get_header_columns():
        return [
            ('ID', FakturaNP.id, 'id', {'editable': False}),
            ('Numer', FakturaNP.numer, 'numer', {}),
            ('Nabywca', FakturaNP.nabywca, 'nabywca', {}),
            ('Data wystawienia', FakturaNP.wystawiona, 'wystawiona', {}),
            ('Termin płatności', FakturaNP.termin_platnosci, 'termin_platnosci', {}),
            ('Zapłacona', FakturaNP.zaplacona, 'zaplacona', {}),
        ]
