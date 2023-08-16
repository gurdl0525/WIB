import json
import logging

import requests
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.config import OccupationalP
from app.db.base import create_tech


def crawl_programmers(occ: str):

    for o in OccupationalP:
        if o.name == occ:
            occ = o
            break

    logging.info(f'Crawling {occ.name} in programmers')

    if isinstance(occ, str):
        raise HTTPException(status_code=400, detail={'message': '잘못된 분야'})

    totalPage = int(dict(json.loads(requests.get(
        url=rf'https://career.programmers.co.kr/api/job_positions?order=recent&page=1&job_category_ids[]={occ.value}'
    ).text))['totalPages'])

    for i in range(totalPage + 1)[1::]:

        response = dict(json.loads(requests.get(
            url=rf'https://career.programmers.co.kr/api/job_positions?order=recent&page={i}&job_category_ids[]={occ.value}'
        ).text))

        for n in response['jobPositions']:

            n_id = int(n['id'])

            response = requests.get(url=f'https://career.programmers.co.kr/api/job_positions/{n_id}')

            if response.status_code == 401:
                continue

            try:
                response = dict(json.loads(response.text))['jobPosition']
            except KeyError:
                continue

            try:
                for j in response['technicalTags']:
                    create_tech(n_id, j['name'], "PROGRAMMERS", occ.name)

            except IntegrityError:
                continue

    logging.info(f'Complete crawling {occ.name} in programmers')
