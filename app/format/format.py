from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from .model.data import FrameWork, Language
from ..db.base import select_data_from_table, find_all_tech_by_notice_id
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

frameworkList, languageList = FrameWork.list, Language.list


def data_format():
    techList = select_data_from_table('tech')

    if techList is None:
        return {'message': '먼저 테크리스트를 업데이트 해주세요'}

    framework, language = [], []

    for v in techList:

        vText = v['text']
        vNotice = v['notice_id']

        if vText in frameworkList:
            if not isinstance(frameworkList[vText], list):
                if vText == 'Spring' or vText == 'Spring Boot':
                    framework.append(f'{frameworkList[vText]}-Spring/SpringBoot')
                elif vText == 'DRF(Django REST framework)':
                    framework.append(f'{frameworkList[vText]}-Django')
                else:
                    framework.append(f'{frameworkList[vText]}-{vText}')
            else:
                finded = find_all_tech_by_notice_id(vNotice)
                for k in frameworkList[vText]:
                    for i in finded:
                        if i.text == k:
                            if vText == 'Spring' or vText == 'Spring Boot':
                                framework.append(f'{k}-Spring/SpringBoot')
                            elif vText == 'DRF(Django REST framework)':
                                framework.append(f'{k}-Django')
                            else:
                                framework.append(f'{k}-{vText}')

        elif vText in languageList:
            language.append(vText)

    return {'frameworkCountList': dict(Counter(framework)), 'languageCountList': dict(Counter(language))}


def all_format():
    techList = select_data_from_table('tech')

    if techList is None:
        return {'message': '먼저 테크리스트를 업데이트 해주세요'}

    return {'allCountList': Counter(v['text'] for v in techList)}


def show_data_format(tag: str, typ: str):
    if (tag != 'framework' and tag != 'language') or (typ != 'pie' and typ != 'bar'):
        return {'message': 'Invalid Tag Exception'}

    df = data_format()

    if df == {'message': '먼저 테크리스트를 업데이트 해주세요'}:
        return df

    lists, value, label = df[f'{tag}CountList'], [], []

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

    create_image(value, label, f'{tag}_count_{typ}', typ)

    return f'app/format/img/{tag}_count_{typ}.png'


def create_image(value, label, file_name, typ: str):
    rainbow = ['red', 'gold', 'limegreen', 'mediumpurple', 'skyblue', 'dodgerblue', 'darkviolet']
    if typ == 'pie':
        plt.rc('font', family='Apple SD Gothic Neo', size=7)
        plt.rcParams['text.color'] = "Black"
        plt.rcParams['axes.unicode_minus'] = False
        if file_name == 'framework_count_pie':
            plt.title('Framework Count Pie Chart', fontdict={'fontsize': 20})
        else:
            plt.title('Language Count Pie Chart', fontdict={'fontsize': 20})
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
        plt.savefig(f'app/format/img/{file_name}.png', format='png', dpi=200)
    else:
        if file_name == 'framework_count_bar':
            plt.title('Framework Count Bar Graph', fontdict={'fontsize': 20})
            plt.xlabel('Language-Framework',
                       fontdict={'fontsize': 10, 'family': 'Apple SD Gothic Neo', 'color': 'black'})
        else:
            plt.title('Language Count Bar Graph', fontdict={'fontsize': 20})
            plt.xlabel('Languages', fontdict={'fontsize': 10, 'family': 'Apple SD Gothic Neo', 'color': 'black'})
        plt.rc('axes', unicode_minus=False)
        size = range(len(label))
        colors = []
        for i in size:
            colors.append(rainbow[i % 7])
        bars = plt.bar(size, value, color=colors)
        plt.legend(handles=bars, labels=label, prop={'family': 'Apple SD Gothic Neo'})
        plt.grid(True, axis='y', alpha=0.5, color='gray', linestyle='--')
        plt.xticks(size, label, fontdict={'fontsize': 4, 'family': 'Apple SD Gothic Neo', 'color': 'black'})
        plt.ylabel('Count', fontdict={'fontsize': 10, 'family': 'Apple SD Gothic Neo', 'color': 'black'})
        plt.tight_layout()
        plt.savefig(f'app/format/img/{file_name}.png', format='png', dpi=200)
    plt.cla()
    plt.clf()


def get_one_percentage(lists: dict):
    result = 0
    for k in lists:
        result += int(lists[k])

    return result / 50


def get_cloud_word():
    techList = select_data_from_table('tech')

    if techList is None:
        return {'message': '먼저 테크리스트를 업데이트 해주세요'}

    techList = [v['text'] for v in techList]

    bulb = np.array(Image.open('app/format/img/bulb.png'))

    stopwords = set(STOPWORDS)
    stopwords.add("bulb")
    stopwords.add("tech")

    wc = WordCloud(background_color="white", max_words=2000, mask=bulb, width=5000, height=5000,
                   stopwords=stopwords, contour_width=1, contour_color='steelblue')

    tech_str = ''

    for t in techList:
        tech_str = tech_str + ' ' + t

    wc.generate(tech_str)

    plt.imshow(wc, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout
    plt.savefig('app/format/img/cloudword.png', format='png', dpi=200)

    return 'app/format/img/cloudword.png'
