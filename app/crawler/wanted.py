import datetime
import json
import logging

import requests
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.config import OccupationalW
from app.db.base import create_tech


def crawl_wanted(occ: str):

    for o in OccupationalW:
        if o.name == occ:
            occ = o
            break

    logging.info(f'Crawling {occ.name} in wanted')

    if isinstance(occ, str):
        raise HTTPException(status_code=400, detail={'message': '잘못된 분야'})

    n_id_list, offset = [], 0

    while True:

        req = requests.get(
            fr'https://www.wanted.co.kr/api/v4/jobs?{int(datetime.datetime.now().timestamp())}&country=kr&tag_type_ids={occ.value}&job_sort=company.response_rate_order&locations=all&years=-1&limit=100&offset={offset}')

        try:
            n_id_list += [i['id'] for i in json.loads(req.text)['data']]

        except TypeError:
            break

        offset += 100

    for n_id in set(n_id_list):

        request = requests.get(fr'https://www.wanted.co.kr/api/v4/jobs/{n_id}?{int(datetime.datetime.now().timestamp())}')

        try:
            for tag in json.loads(request.text)['job']['skill_tags']:
                create_tech(n_id, tag['title'], "WANTED", occ.name)
        except IntegrityError:
            continue

    logging.info(f'Complete crawling {occ.name} in wanted')
