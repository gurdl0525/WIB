from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.crawler.programmers import crawl_programmers
from app.crawler.wanted import wanted
from app.db.base import Base
from app.db.session import db_engine
from app.dto import RequestCrawl, RequestShow, RequestCloudwords
from app.format.format import show_data_format, get_cloud_word


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


app = get_application()


@app.put("/crawl", status_code=201)
def crawl_joblist(request: RequestCrawl):
    if request.typ == 'programmers':
        crawl_programmers(request.occ)
    elif request.typ == 'wanted':
        print('wanted')
    else:
        raise HTTPException(status_code=400)

    return {'message': 'updated now'}


@app.get('/show/cloudwords', status_code=200)
def show_all_cloud_word(request: RequestCloudwords):
    return FileResponse(get_cloud_word(request.occ))


@app.get('/show', status_code=200)
def show_tech_format(request: RequestShow):
    return FileResponse(show_data_format(request.typ, request.tag, request.occ))


@app.get('/wanted/{n_id}')
def wanted_api(n_id: str):
    return wanted(n_id)
