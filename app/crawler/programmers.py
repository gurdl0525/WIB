import json

import requests
from sqlalchemy.exc import IntegrityError

from app.db.base import create_notice, create_company, create_tech, select_data_from_table, delete_notice_id


def update_job_list(cookie):
    totalPage = int(dict(json.loads(requests.get(
        url=r'https://career.programmers.co.kr/api/job_positions?order=recent&page=1&job_category_ids[]=1',
        cookies={'_programmers_session_production': cookie}
    ).text))['totalPages'])

    for i in range(totalPage + 1)[1::]:

        response = dict(json.loads(requests.get(
            url=f'https://career.programmers.co.kr/api/job_positions?order=recent&page={i}&job_category_ids[]=1',
            cookies={'_programmers_session_production': cookie}
        ).text))

        for j in response['jobPositions']:
            try:
                create_notice(int(j['id']))
            except IntegrityError:
                continue


def update_tech(cookie):
    jobList = select_data_from_table("notice")

    for i in jobList:

        i = i['id']

        response = requests.get(
            url=f'https://career.programmers.co.kr/api/job_positions/{i}',
            cookies={'_programmers_session_production': cookie}
        )

        if response.status_code == 401:
            continue

        try:
            response = dict(json.loads(response.text))['jobPosition']
        except KeyError:
            return

        name = response['company']['name']

        create_company(name)

        for j in response['technicalTags']:
            create_tech(j['name'], name, i)
