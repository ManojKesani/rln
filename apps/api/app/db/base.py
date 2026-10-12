"""SQLAlchemy declarative base. Every table model inherits from Base, which lets
Alembic (alembic/env.py) see all tables through Base.metadata."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
