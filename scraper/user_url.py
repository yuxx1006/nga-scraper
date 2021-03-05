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
HEADERS = ['user_id', 'topics']
CSV_COLUMNS = ['topic_id', 'user_id', 'user_url', 'user_level', 'user_prestige', 'user_famous',
           'register_date', 'publish_date', 'publish_source']
# CSV_COLUMNS = ['topic_id', 'topic_url', 'topic_tag', 'topic_description',
#                'reply_count', 'author_id', 'author_name',
#                'post_time', 'last_reply_by', 'last_reply_time',
#                'page_count']
CSV = './yingzhishi_user.csv'
# CSV = './nga_test.csv'
THREAD = 'thread'
my_table = None
BASE_URL = 'https://bbs.nga.cn/thread.php?authorid={}&searchpost=1&fid=0'


def get_page_source(my_t, uid):
    url = BASE_URL.format(uid)

    browser.get(url)
 
    sleep(random.randint(1, 2))
    parser = etree.HTML(browser.page_source)

    # collecting all container into a list and going through each one
    all_posts = parser.xpath('//*[@id="topicrows"]/tbody/tr/td[2]')
# //*[@id="topicrows"]/tbody[6]/tr/td[2]/span[3]/a

    topics = []
    for num, table in enumerate(all_posts):
        try:
            # topics
            if table.xpath('.//a[@class="silver"]/text()'):
                topics.append(table.xpath('.//a[@class="silver"]/text()')[0])


        except Exception as e:
            pass

    tid = []
    for i in topics:
        if i not in tid:
            tid.append(i)

    print(tid)
    data = {"user_id": uid, "topics": tid }
    my_t = my_t.append(data, ignore_index=True)

    return my_t


if __name__ == "__main__":
    browser = Firefox()
    browser.implicitly_wait(10)
    browser.maximize_window()
    login_url = 'https://bbs.nga.cn/thread.php?authorid=51032&searchpost=1&fid=0'
    browser.get(login_url)
    sleep(40)

    my_table = pd.DataFrame(columns=HEADERS)
    topic_table = pd.read_csv(CSV, names=CSV_COLUMNS)
    topic_table = topic_table.drop_duplicates(subset=['user_id'], keep=False)


    for i, row in topic_table.iterrows():
        if i == 0: continue
        user_id = row['user_id']

        my_table = get_page_source(my_table, user_id)

    my_table.to_csv(r'./user_data_yingzhishi.csv', header=HEADERS, index=None, sep=',', mode='a')

    # closing the browser window
    browser.close()
