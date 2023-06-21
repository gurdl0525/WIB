from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.core.config import get_setting
from app.crawler.programmers import update_job_list, update_tech
from app.db.base import Base, select_data_from_table
from app.db.session import db_engine
from app.format.format import data_format, all_format, show_data_format
import matplotlib.font_manager as fm

SESSION = get_setting().PROGRAMMERS_SESSION


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


app = get_application()


@app.post("/crawl/job", status_code=201)
def update_joblist_to_crawl():
    if not update_job_list(SESSION):
        return HTTPException(status_code=400, detail='세션이 만료되었습니다')
    return {'message': 'updated job_list now'}


@app.post("/crawl/tech", status_code=201)
def update_tech_to_crawl():
    update_tech(SESSION)
    return {'message': 'updated tech_list now'}


@app.get("/crawl/tech", status_code=200)
def get_tech_list():
    return select_data_from_table('tech')


@app.get("/crawl/tech/format", status_code=200)
def get_tech_list():
    return data_format()


@app.get('/crawl/all/format', status_code=200)
def get_all_list():
    return all_format()


@app.get('/show/{typ}/{tag}', status_code=200)
def show_tech_format(typ: str, tag: str):

    result = show_data_format(tag, typ)

    if result == {'message': 'Invalid Tag Exception'}:
        raise HTTPException(status_code=400, detail=result)
    elif result == {'message': '먼저 테크리스트를 업데이트 해주세요'}:
        raise HTTPException(status_code=201, detail=result)

    return FileResponse(result)

