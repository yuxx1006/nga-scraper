from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os

from selenium.webdriver import Chrome, Firefox, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

from datetime import datetime
from time import sleep
from lxml import etree
import pandas as pd
import random

url = "https://bbs.nga.cn/thread.php?fid=-362960"
browser = Firefox()
browser.implicitly_wait(10)
browser.maximize_window()
sleep(2)

headers = ['topic_id', 'topic_url', 'topic_tag', 'topic_description',
           'reply_count', 'author_id', 'author_name',
           'post_time', 'last_reply_by', 'last_reply_time',
           'page_count']
my_table = pd.DataFrame(columns=headers)
REPETITIONS = 126
for i in range(REPETITIONS):
    if i == 0:
        continue
    browser.get(url + "&page={}".format(i))
    if i == 1 or i == 2:
        sleep(8)
    else:
        sleep(random.randint(3, 6))
    parser = etree.HTML(browser.page_source)
    # result = etree.tostring(parser)
    # print(result.decode('utf-8'))

    # collecting all container into a list and going through each one
    all_posts = parser.xpath('//div[@id="m_threads"]//table[@class="forumbox "]/tbody')
    print("page {} has {} posts".format(i, str(len(all_posts))))
    ti = 0
    for table in all_posts:
        topic_tags = []
        try:
            # topic tags
            if table.xpath('.//a[@class="topic"]//span[@class="silver"]'):
                tag_length = table.xpath('.//a[@class="topic"]//span[@class="silver"]')
                if len(tag_length) == 1:
                    topic_tags.append(table.xpath('.//a[@class="topic"]//span[@class="silver"]/text()')[0][1:-1])
                elif len(tag_length) > 1:
                    for each in tag_length:
                        topic_tags.append(each.xpath('.//text()')[0][1:-1].replace(',', ''))

            # topic description
            if table.xpath('.//a[@class="topic"]'):
                topic_tag_name = "topic"
            elif table.xpath('.//a[@class="topic b "]'):
                topic_tag_name = "topic b "
            elif table.xpath('.//a[@class="topic blue "]'):
                topic_tag_name = "topic blue "
            elif table.xpath('.//a[@class="topic blue b "]'):
                topic_tag_name = "topic blue b "
            elif table.xpath('.//a[@class="topic red "]'):
                topic_tag_name = "topic red "
            elif table.xpath('.//a[@class="topic red b "]'):
                topic_tag_name = "topic red b "
            elif table.xpath('.//a[@class="topic green "]'):
                topic_tag_name = "topic green "
            elif table.xpath('.//a[@class="topic green b "]'):
                topic_tag_name = "topic green b "
            elif table.xpath('.//a[@class="topic orange "]'):
                topic_tag_name = "topic orange "
            elif table.xpath('.//a[@class="topic orange b "]'):
                topic_tag_name = "topic orange b "
            elif table.xpath('.//a[@class="topic AgFxB68"]'):
                topic_tag_name = "topic AgFxB68"
            elif table.xpath('.//a[@class="topic AgE3rN4"]'):
                topic_tag_name = "topic AgE3rN4"
            elif table.xpath('.//a[@class="topic AgCfP9Q"]'):
                topic_tag_name = "topic AgCfP9Q"
            else:
                topic_tag_name = None

            if topic_tag_name:
                topic_des = table.xpath('.//a[@class="{}"]/text()'.format(topic_tag_name))[0]
                t_url = table.xpath('.//a[@class="{}"]/@href'.format(topic_tag_name))[0]
                if table.xpath('.//a[@class="{}"]//span[@class="silver"]'.format(topic_tag_name)):
                    tag_length = table.xpath('.//a[@class="{}"]//span[@class="silver"]'.format(topic_tag_name))
                    if len(tag_length) == 1:
                        topic_tags.append(
                            table.xpath('.//a[@class="{}"]//span[@class="silver"]/text()'.format(topic_tag_name))[0][
                            1:-1])
                    elif len(tag_length) > 1:
                        for each in tag_length:
                            topic_tags.append(each.xpath('.//text()')[0][1:-1].replace(',', ''))
            else:
                topic_des = None
                t_url = None

            # number of page in topic
            if table.xpath('.//span[@class=" pager"]'):
                pages = table.xpath('.//span[@class=" pager"]//a[@class=" silver"]')
                page_count = len(pages)
            else:
                page_count = 0

            # track topic id
            topic_id = 't_tt{}_{}'.format(i, ti)
            ti = ti + 1

            # number of reply
            if table.xpath('.//a[@class="replies"]/text()'):
                reply_count = table.xpath('.//a[@class="replies"]/text()')[0]
            else:
                reply_count = None

            # author info
            if table.xpath('.//a[@class="author"]/@title'):
                author_id = table.xpath('.//a[@class="author"]/@title')[0]
                author_id = author_id.replace('用户ID ', '')
                author_name = []
                author_name.append(table.xpath('.//a[@class="author"]/b[@class="block_txt"]/text()')[0])
                author_name.append(table.xpath('.//a[@class="author"]/text()')[0])
                author_name = ''.join(author_name)
                post_time = table.xpath('.//span[@class="silver postdate"]/@title')[0]
            else:
                author_id = None
                author_name = None
                post_time = None

            # last reply
            if table.xpath('.//a[@class="silver replydate"]/@title'):
                last_reply_time = table.xpath('.//a[@class="silver replydate"]/@title')[0]
                last_reply_by = []
                last_reply_by.append(table.xpath('.//span[@class="replyer"]/b[@class="block_txt"]/text()')[0])
                last_reply_by.append(table.xpath('.//span[@class="replyer"]/text()')[0])
                last_reply_by = ''.join(last_reply_by)
            else:
                last_reply_time = None
                last_reply_by = None
        except Exception as e:
            pass

        data = {
            "topic_id": topic_id, "topic_url": t_url, "topic_tag": topic_tags,
            "topic_description": topic_des, "reply_count": reply_count,
            "author_id": author_id, "author_name": author_name, "post_time": post_time,
            "last_reply_by": last_reply_by, "last_reply_time": last_reply_time,
            "page_count": page_count
        }
        my_table = my_table.append(data, ignore_index=True)

# closing the browser window
browser.close()
print(my_table.head())

my_table.to_csv(r'./nga_fflogs.csv', header=headers, index=None, sep=',', mode='a')
