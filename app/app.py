import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.crawler.programmers import crawl_programmers
from app.crawler.wanted import crawl_wanted
from app.db.base import Base
from app.db.session import db_engine
from app.dto import RequestCrawl, RequestShow, RequestCloudwords
from app.format.format import show_data_format, get_cloud_word


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


logging.basicConfig(level='INFO')

app = get_application()

scheduler = AsyncIOScheduler(daemon=True, timezone='Asia/Seoul')


@app.put("/crawl", status_code=201)
def crawl_joblist(request: RequestCrawl):
    if request.typ == 'programmers':
        crawl_programmers(request.occ)
    elif request.typ == 'wanted':
        crawl_wanted(request.occ)
    else:
        raise HTTPException(status_code=400)

    return {'message': 'updated now'}


@app.get('/show/cloudwords', status_code=200)
def show_all_cloud_word(request: RequestCloudwords):
    return FileResponse(get_cloud_word(request.occ))


@app.get('/show', status_code=200)
def show_tech_format(request: RequestShow):
    return FileResponse(show_data_format(request.typ, request.tag, request.occ))


scheduler.add_job(func=crawl_programmers, trigger='cron', day=1, id='crawl_p_b', args=['BACKEND'])
scheduler.add_job(func=crawl_wanted, trigger='cron', day=1, id='crawl_w_b', args=['BACKEND'])
scheduler.add_job(func=crawl_programmers, trigger='cron', day=1, id='crawl_p_f', args=['FRONTEND'])
scheduler.add_job(func=crawl_wanted, trigger='cron', day=1, id='crawl_w_f', args=['FRONTEND'])
scheduler.start()
