from sqlalchemy import Column, BIGINT, VARCHAR, CHAR

from ..base_class import Base
from enum import Enum


class Tech(Base):
    __tablename__ = "tech"
    id = Column(BIGINT, primary_key=True)
    text = Column(VARCHAR(50), primary_key=True)
    type = Column(CHAR(11), primary_key=True)
    occupational = Column(VARCHAR(20), primary_key=True)


class OccupationalP(Enum):
    BACKEND = 1
    FRONTEND = 4
