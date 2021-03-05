from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
from gevent.pywsgi import WSGIServer
from selenium.webdriver import Chrome, Firefox, ActionChains

from datetime import datetime
from flask import Flask, request, Response
from time import sleep
from lxml import etree
import pandas as pd
import random

# url = "https://bbs.nga.cn/read.php?tid=18887364"

HEADERS = ['topic_id', 'uid', 'user_url', 'user_level', 'user_prestige', 'user_famous',
           'register_date', 'publish_date', 'publish_source']
CSV_COLUMNS = ['topic_id', 'topic_url', 'topic_tag', 'topic_description',
               'reply_count', 'author_id', 'author_name',
               'post_time', 'last_reply_by', 'last_reply_time',
               'page_count']
CSV = './nga_yingzhishi.csv'
# CSV = './nga_test.csv'
THREAD = 'thread'
my_table = None
BASE_URL = 'https://bbs.nga.cn/'


def get_page_source(my_t, tid, url):

    browser.get(url)
    if tid == 't_tt1_0' or tid == 't_tt1_1':
        sleep(8)
    else:
        sleep(random.randint(3, 5))
    parser = etree.HTML(browser.page_source)
    # collecting all container into a list and going through each one
    all_posts = parser.xpath('//div[@id="m_posts_c"]/table[@class="forumbox postbox"]')

    for num, table in enumerate(all_posts):
        try:
            # user id
            if table.xpath('.//a[@name="uid"]'):
                uid = table.xpath('.//a[@name="uid"]/text()')[0]
            else:
                uid = None
            #user url
            if table.xpath('.//a[@class="author b nobr"]'):
                user_url = table.xpath('.//a[@class="author b nobr"]/@href')[0]
                user_url = BASE_URL + user_url
            else:
                user_url = None

            #user level
            if table.xpath('.//span[@class="silver"]'):
                ulevel = table.xpath('.//span[@class="silver"]/text()')[0]
            else:
                ulevel = None
            # user prestige (威望)
            if table.xpath('.//span[@class="numericl silver"]/text()'):
                uprestige = table.xpath('.//span[@class="numericl silver"]/text()')[0]
            else:
                uprestige = None
            # 声望
            if table.xpath('.//span[@class="silver numericl"]/text()'):
                ufamous = table.xpath('.//span[@class="silver numericl"]/text()')[0]
            else:
                ufamous = None
            # 注册时间
            if table.xpath('.//span[@name="regdate"]'):
                ureg = table.xpath('.//span[@name="regdate"]/text()')
                if ureg:
                    uregister = ureg[0]
                else:
                    uregister = None
            else:
                uregister = None
            # publish date and source
            if table.xpath('.//div[@class="postInfo"]'):
                pubdate = table.xpath('.//div[@class="postInfo"]//span[@class=" stxt"]/text()')[0]
                source = table.xpath('.//div[@class="postInfo"]//a[@class="  inlineBlock stxt"]/@title')[0]
                sources = source.strip()
                if 'Android' in sources:
                    source = 'android'
                elif 'iOS' in sources:
                    source = "ios"
                elif '/' in sources:
                    source = 'desktop'
                else:
                    source = 'other'
            else:
                source = None
                pubdate = None


            data = {"topic_id": tid, "uid": uid, "user_url": user_url, "user_level": ulevel, "user_prestige": uprestige,
                    "user_famous": ufamous, "register_date": uregister, "publish_date": pubdate,
                    "publish_source": source
                   }
            my_t = my_t.append(data, ignore_index=True)

        except Exception as e:
            pass


    return my_t


if __name__ == "__main__":
    browser = Firefox()
    browser.implicitly_wait(10)
    browser.maximize_window()

    my_table = pd.DataFrame(columns=HEADERS)
    topic_table = pd.read_csv(CSV, names=CSV_COLUMNS)
    topic_table.dropna(subset=['topic_url'], inplace=True)
    # print(topic_table.head(5))
    for i, row in topic_table.iterrows():
        if i == 0: continue
        topic_id = row['topic_id']
        topic_url = row['topic_url']
        page_count = int(row['page_count'])

        # topic_url
        if not topic_url:
            continue
        if topic_url.find(THREAD) != -1:
            continue

        my_table = get_page_source(my_table, topic_id, topic_url)
       
    # print(my_table.head())
    my_table.to_csv(r'./yingzhishi_user.csv', header=HEADERS, index=None, sep=',', mode='a')

    # closing the browser window
    browser.close()
