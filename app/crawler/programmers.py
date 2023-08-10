import json

import requests
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.db.base import create_tech
from app.db.models.tech import OccupationalP


def crawl_programmers(occ: str):
    tag: int = None

    for e in OccupationalP:
        if e.name == occ:
            tag = e.value
            break

    if tag is None:
        raise HTTPException(status_code=400, detail={'message': '잘못된 분야'})

    totalPage = int(dict(json.loads(requests.get(
        url=rf'https://career.programmers.co.kr/api/job_positions?order=recent&page=1&job_category_ids[]={tag}'
    ).text))['totalPages'])

    for i in range(totalPage + 1)[1::]:

        response = dict(json.loads(requests.get(
            url=rf'https://career.programmers.co.kr/api/job_positions?order=recent&page={i}&job_category_ids[]={tag}'
        ).text))

        for j in response['jobPositions']:
            try:
                update_tech(int(j['id']), occ)
            except IntegrityError:
                continue

    return


def update_tech(n_id: str or int, occ: str):
    response = requests.get(url=f'https://career.programmers.co.kr/api/job_positions/{n_id}')

    if response.status_code == 401:
        return

    try:
        response = dict(json.loads(response.text))['jobPosition']
    except KeyError:
        return

    for j in response['technicalTags']:
        create_tech(n_id, j['name'], "PROGRAMMERS", occ)
