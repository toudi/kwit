from sqlalchemy.orm import sessionmaker
from core import settings
from sqlalchemy import create_engine


Session = sessionmaker()


Session.configure(
    bind=create_engine(
        settings.get('SQLALCHEMY_URI', 'sqlite:///~/.kwit/kwit.sqlite3')
    )
)

session = Session()
