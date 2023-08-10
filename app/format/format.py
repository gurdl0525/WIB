from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from fastapi import HTTPException
from wordcloud import WordCloud, STOPWORDS

from .model.data import FrameWork, Language
from ..db.base import find_all_tech_by_occ

frameworkList, languageList = FrameWork.list, Language.list


def data_format_p(tag: str, occ: str):
    techList = find_all_tech_by_occ(occ)

    if techList is None:
        raise HTTPException(status_code=400, detail={'message': '먼저 테크리스트를 업데이트 해주세요'})

    result = []

    if tag == 'language':

        for v in techList:

            if v.text in languageList:
                result.append(v.text)

    elif tag == 'framework':

        for v in techList:

            if v.text in frameworkList:

                result.append(v.text if v.text != 'DRF(Django REST framework)' else 'Django')

    elif tag == 'compound':

        l, n = [], 0

        for v in techList:

            if n != v.id:
                n = v.id
                l.clear()

            txt = v.text

            if txt in frameworkList:

                if isinstance(frameworkList[txt], list):
                    for lang in list(set(l).intersection(frameworkList[txt])):
                        result.append(lang + '-' + txt if txt != 'DRF(Django REST framework)' else 'Django')
                else:
                    result.append(frameworkList[txt] + '-' + txt if txt != 'DRF(Django REST framework)' else 'Django')

            elif txt in languageList:
                l.append(txt)
    else:
        raise HTTPException(status_code=400, detail={'message': 'Invalid Tag Exception'})

    return dict(Counter(result))


def show_data_format(typ: str, tag: str, occ: str):

    if typ != 'pie' and typ != 'bar':
        raise HTTPException(status_code=400, detail={'message': 'Invalid Type Exception'})

    df = data_format_p(tag, occ)

    lists, value, label = df, [], []

    onePercentage, etc = get_one_percentage(lists), 0

    for k in lists:
        if lists[k] >= onePercentage:
            label.append(k)
            value.append(lists[k])
        else:
            etc += lists[k]

    if etc != 0:
        label.append('기타')
        value.append(etc)

    create_image(value, label, f'{tag}_count_{typ}', typ, occ)

    return f'app/format/img/{occ}/{tag}_count_{typ}.png'


def create_image(value: list, label: list, file_name: str, typ: str, occ :str):
    rainbow = ['red', 'gold', 'limegreen', 'mediumpurple', 'skyblue', 'dodgerblue', 'darkviolet']
    if typ == 'pie':
        plt.rc('font', family='Apple SD Gothic Neo', size=7)
        plt.rcParams['text.color'] = "Black"
        plt.rcParams['axes.unicode_minus'] = False
        plt.title(file_name.title().replace('_', ' ') + ' Chart', fontdict={'fontsize': 20})
        size = len(label)
        colors = []
        for i in range(size):
            colors.append(rainbow[i % 7])
        plt.pie(
            value,
            labels=label,
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.03] * size,
            wedgeprops={'width': 0.7},
            colors=colors
        )
        plt.tight_layout()
        plt.savefig(f'app/format/img/{occ}/{file_name}.png', format='png', dpi=200)
    else:
        plt.title(file_name.title().replace('_', ' ') + ' Bar Graph', fontdict={'fontsize': 20})
        plt.xlabel(
            xlabel='languages' if file_name == 'language_count_bar' else 'Frameworks' if file_name == 'framework_count_bar' else 'Compounds',
            fontdict={
                'fontsize': 10,
                'family': 'Apple SD Gothic Neo',
                'color': 'black'
            }
        )
        plt.rc('axes', unicode_minus=False)
        size = range(len(label))
        colors = []
        for i in size:
            colors.append(rainbow[i % 7])
        bars = plt.bar(size, value, color=colors, width=0.5)
        plt.legend(handles=bars, labels=label, prop={'family': 'Apple SD Gothic Neo'})
        plt.grid(True, axis='y', alpha=0.5, color='gray', linestyle='--')
        plt.xticks(size, label, fontdict={'fontsize': 4, 'family': 'Apple SD Gothic Neo', 'color': 'black'})
        plt.ylabel('Count', fontdict={'fontsize': 10, 'family': 'Apple SD Gothic Neo', 'color': 'black'})
        plt.tight_layout()
        plt.savefig(f'app/format/img/{occ}/{file_name}.png', format='png', dpi=200)
    plt.cla()
    plt.clf()


def get_one_percentage(lists: dict):
    result = 0
    for k in lists:
        result += int(lists[k])

    return result / 50


def get_cloud_word(occ: str):
    techList = find_all_tech_by_occ(occ)

    if techList is None:
        raise HTTPException(status_code=400, detail={'message': '먼저 테크리스트를 업데이트 해주세요'})

    techList = [v.text for v in techList]

    bulb = np.array(Image.open('app/format/img/bulb.png'))

    stopwords = set(STOPWORDS)
    stopwords.add("bulb")
    stopwords.add("tech")

    wc = WordCloud(
        background_color="white",
        max_words=2000,
        mask=bulb,
        width=5000,
        height=5000,
        stopwords=stopwords,
        contour_width=1,
        contour_color='steelblue'
    )

    tech_str = ''

    for t in techList:
        tech_str = tech_str + ' ' + t

    wc.generate(tech_str)

    plt.imshow(wc, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f'app/format/img/{occ}/cloudword.png', format='png', dpi=300)

    return f'app/format/img/{occ}/cloudword.png'
