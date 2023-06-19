from fastapi import FastAPI

from app.core.config import get_setting
from app.crawler.programmers import update_job_list, update_tech
from app.db.base import Base, select_data_from_table
from app.db.session import db_engine

SESSION = get_setting().PROGRAMMERS_SESSION


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


app = get_application()


@app.post("/crawl", status_code=201)
def crawl():
    update_job_list(SESSION)
    print('job_list 완료')
    update_tech(SESSION)
    print('tech_list 완료')

    return {'message': 'crawling complete now'}


@app.post("/crawl/job", status_code=201)
def update_joblist_to_crawl():
    update_job_list(SESSION)
    return {'message': 'updated job_list now'}


@app.post("/crawl/tech", status_code=201)
def update_tech_to_crawl():
    update_tech(SESSION)
    return {'message': 'updated tech_list now'}


@app.get("/crawl/tech", status_code=200)
def get_tech_list():
    return select_data_from_table('tech')
