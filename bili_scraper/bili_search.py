import requests
import json
import pandas as pd
from datetime import datetime
from time import sleep
import random

BILI_HEADER = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

KEYWORDS = ["明日方舟 画中人 WR-EX"]
REPETITIONS = 8  # first 3 pages
POST_URL = 'https://api.opssr.fun/api/v1/import/xximport'
# POST_URL = 'http://192.168.2.215:3005/api/dev/import/xximport'
BASE_URL = 'http://api.bilibili.com/x/web-interface/search/type?order=pubdate&duration=0&search_type=video&tids=0&'


def _daily_report(my_table, current):
    for each_key in KEYWORDS:
        for i in range(REPETITIONS):
            if i == 0: continue
            url = BASE_URL + 'keyword={}&page={}'.format(each_key, i)
            r = requests.get(url, headers=BILI_HEADER).json()
            videos = r["data"]["result"]
            sleep(random.randint(6, 8))

            for v in videos:
                pubdate = v['pubdate']
                pubdate = datetime.utcfromtimestamp(int(pubdate))
                strDate = pubdate.strftime("%m-%d-%Y %H:%M:%S")
                # duration_in_s = (current - pubdate).total_seconds()
                # diff = divmod(duration_in_s, 3600)[0]  
                diff = (current - pubdate).days
                if diff < 1:
                    bvid = v['bvid']
                    author = v['author'].replace(',','')
                    link = v['arcurl']
                    title = v['title'].strip().replace('<em class="keyword">','').replace('</em>','').replace(',',' ')
                    desc = v['description'].strip().replace(',',' ').replace('\n', '')
                    pic = v['pic'].replace('//','')
                    tag = v['tag'].replace(',',' ')
                    duration = v['duration']

                    data = {'bvid': bvid, 'author': author, 'arcurl': link,
                            'title': title, 'description': desc, 'pic': pic,
                            'tag': tag, 'pubdate': strDate, 'duration': duration}
                    my_table = my_table.append(data, ignore_index=True)

    my_table.sort_values("bvid", inplace=True)
    my_table.drop_duplicates(subset="bvid", keep=False, inplace=True)
    # print(my_table.head())
    my_dict = my_table.to_dict('r')

    # date_file = current.strftime("%m%d")
    # file_name = './bili_{}.csv'.format(date_file)
    # my_table.to_csv(file_name, header=columns, index=None, sep=',', mode='a')
    return my_dict


def _post_data(report):

    payload = json.dumps(report, ensure_ascii=False).encode('utf-8')
    headers = {
        'X-Admin': 'landuxiaotianshi',
        'Content-Type': 'application/json; charset=utf-8'
    }
    r = requests.post(POST_URL, headers=headers, data=payload)
    # print(r.text)


if __name__ == "__main__":
    columns = ['bvid', 'author', 'arcurl', 'title', 'description',
               'pic', 'tag', 'pubdate', 'duration']
    my_table = pd.DataFrame(columns=columns)
    current = datetime.utcnow()
    daily_report = _daily_report(my_table, current)
    print(daily_report)
    _post_data(daily_report)
