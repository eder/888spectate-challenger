import os

from gino import Gino
from db.models import db  
DATABASE_URL = os.environ['DATABASE_URL'] 

def run_migrations_offline():
    # ...
    context.configure(
        url=DATABASE_URL,
        target_metadata=db,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    # ...

def run_migrations_online():
    # ...
    context.configure(
        url=DATABASE_URL,
        target_metadata=db
    )
    # ...

