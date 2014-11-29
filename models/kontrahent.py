from peewee import *


class Kontrahent(Model):
    nazwa = CharField()
    adres = CharField()
    nip = CharField()
    regon = CharField()
