kwit
====

obsługa faktur off-line w systemie linux

Wszystkie obrazki pochodzą ze strony http://www.flaticon.com/

Pierwsze uruchomienie
=====================

Przed uruchomieniem programu proszę przygotować środowisko virtualenv'a:

```
mkvirtualenv kwit
pip install -r requirements.txt
```

oraz zmigrować bazę danych:

```
python migrate-db.py
```
