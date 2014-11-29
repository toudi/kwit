from sqlalchemy.ext.declarative import declarative_base
from core.utils.alchemical_model import AlchemicalTableModel
from core import db
Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True

    @classmethod
    def get_qmodel_class(cls):
        return AlchemicalTableModel(
            db.session,
            cls,
            cls.get_header_columns()
        )
