from sqlalchemy.exc import NoResultFound

from .base_class import Base
from .models.tech import Tech
from .session import SessionLocal

Session = SessionLocal


def toFactor(factor):
    if factor == 'NodeJS':
        return 'Node.js'
    elif factor == 'Embedded C':
        return 'C'
    elif factor == '.NET Core':
        return '.NET'
    elif factor == 'Vue.JS' or factor == 'VueJS':
        return 'Vue.js'
    elif factor == 'React':
        return 'ReactJS'
    elif factor == 'iOS 개발' or factor == 'iOS':
        return 'Swift'
    elif factor == 'iBatis':
        return 'ibatis'
    elif factor == 'C / C++':
        return 'C++'
    elif factor == 'ASP .NET':
        return 'ASP.NET'
    elif factor == 'Spring Framework':
        return 'Spring'
    else:
        return factor


def create_tech(notice_id: int, txt: str, typ: str, occ: str):

    txt = toFactor(txt)

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
