from sqlalchemy import text
from sqlalchemy.exc import ResourceClosedError, NoResultFound

from .base_class import Base
from .models.company import Company
from .models.notice import Notice
from .models.tech import Tech
from .session import SessionLocal, db_engine

Session = SessionLocal


def create_notice(notice_id: int):
    db = SessionLocal()
    notice = Notice(id=notice_id)
    db.add(notice)
    db.commit()
    db.refresh(notice)


def create_company(company_id: str):
    if find_company_by_id(company_id) is None:
        db = SessionLocal()
        company = Company(id=company_id)
        db.add(company)
        db.commit()
        db.refresh(company)


def create_tech(content: str, company_id: str, notice_id: int):
    if find_tech_by_id(content=content, company_id=company_id, notice_id=notice_id) is None:
        db = SessionLocal()
        tech = Tech(text=content, company_id=company_id, notice_id=notice_id)
        db.add(tech)
        db.commit()
        db.refresh(tech)


def select_data_from_table(table_name: str):
    with db_engine.connect() as connection:
        query = text(f"SELECT * FROM {table_name}")
        result = connection.execute(query)
        try:
            rows = result.fetchall()
        except ResourceClosedError:
            rows = []

        column_names = result.keys()
        return [dict(zip(column_names, row)) for row in rows]


def delete_notice_id(notice_id: int or str):
    with db_engine.connect() as connection:
        query = text(f"DELETE FROM notice WHERE id = {notice_id}")
        connection.execute(query)


def find_company_by_id(company_id: str):
    session = Session()

    try:
        return session.query(Company).get(company_id)
    except NoResultFound:
        return None


def find_tech_by_id(content: str, company_id: str, notice_id: int):
    session = Session()

    try:
        record = session.query(Tech).filter_by(text=content, company_id=company_id, notice_id=notice_id).first()
    except NoResultFound:
        return None
    return record


def find_all_tech_by_notice_id(notice_id: int):
    session = Session()

    try:
        record = session.query(Tech).filter_by(notice_id=notice_id).all()
    except NoResultFound:
        return None
    return list(record)
