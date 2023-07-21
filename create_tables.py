import logging
from app.database.base import create_tables, drop_tables

logging.basicConfig(level=logging.INFO)

drop_tables()
create_tables()
