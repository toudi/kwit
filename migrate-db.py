from core.models.abstract import Base
from core import db
# inside of a "create the database" script, first create
# tables:
from core.models import *
from document_types.faktura_np.models import *
Base.metadata.create_all(db.session.bind)

# then, load the Alembic configuration and generate the
# version table, "stamping" it with the most recent rev:
from alembic.config import Config
from alembic import command
alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
