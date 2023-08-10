from sqlalchemy.exc import NoResultFound

from .base_class import Base
from .models.tech import Tech
from .session import SessionLocal

Session = SessionLocal


def create_tech(notice_id: int, txt: str, typ: str, occ: str):
    if not exist_tech_by_ids(notice_id=notice_id, txt=txt, typ=typ, occ=occ):
        return

    db = SessionLocal()
    tech = Tech(id=notice_id, text=txt, type=typ, occupational=occ)
    db.add(tech)
    db.commit()
    db.refresh(tech)


def find_all_tech_by_occ(occ: str):
    session = Session()

    try:
        record = session.query(Tech).filter_by(occupational=occ).all()
    except NoResultFound:
        return None

    return list(record) if record != [] else None


def exist_tech_by_ids(notice_id: int, txt: str, typ: str, occ: str):
    session = Session()

    try:
        session.query(Tech).filter_by(id=notice_id, text=txt, type=typ, occupational=occ).first()
    except NoResultFound:
        return False
    return True
