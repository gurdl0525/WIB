from sqlalchemy import Column, BIGINT
from sqlalchemy.orm import relationship

from ..base_class import Base


class Notice(Base):
    __tablename__ = "notice"
    id = Column(BIGINT, primary_key=True, autoincrement=False)
    tech = relationship("Tech", lazy=True)
