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

class FakturaNPPozycja(AbstractModel):
    __tablename__ = 'kwit_faktury_np_pozycje'

    id = Column(Integer, primary_key=True)
    faktura_np = Column(Integer, ForeignKey('kwit_faktury_np.id'))
    usluga = Column(Integer, ForeignKey('kwit_uslugi.id'))
    cena_pln = Column(String)
    cena_waluta = Column(String)

    @staticmethod
    def get_header_columns():
        return [
            ('ID', FakturaNPPozycja.id, 'id', {}),
            ('Usluga', FakturaNPPozycja.usluga, 'usluga', {}),
            ('Cena (PLN)', FakturaNPPozycja.cena_pln, 'cena_pln', {}),
            ('Cena (waluta obca)', FakturaNPPozycja.cena_waluta, 'cena_waluta', {})
        ]
