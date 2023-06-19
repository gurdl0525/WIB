from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship
from ..base_class import Base


class Company(Base):
    __tablename__ = "company"
    id = Column(VARCHAR(200), primary_key=True)
    tech = relationship("Tech", lazy=True)
