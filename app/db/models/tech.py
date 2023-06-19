from sqlalchemy import Column, BIGINT, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from ..base_class import Base


class Tech(Base):
    __tablename__ = "tech"
    text = Column(VARCHAR(200), nullable=False, primary_key=True)
    company_id = Column(VARCHAR(200), ForeignKey('company.id'), nullable=False, primary_key=True)
    notice_id = Column(BIGINT, ForeignKey('notice.id'), nullable=False, primary_key=True)
    company = relationship("Company", back_populates="tech", lazy=True)
    notice = relationship("Notice", back_populates="tech", lazy=True)
