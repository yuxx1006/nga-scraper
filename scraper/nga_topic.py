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

HEADERS = ['topic_id', 'uid', 'user_level', 'user_prestige', 'user_famous',
           'register_date', 'publish_date', 'publish_source', 'content',
           'quote_author', 'quote_post_time', 'quote', 'image_url', 'is_master']
CSV_COLUMNS = ['topic_id', 'topic_url', 'topic_tag', 'topic_description',
               'reply_count', 'author_id', 'author_name',
               'post_time', 'last_reply_by', 'last_reply_time',
               'page_count']
CSV = './nga_arknights_2.csv'
# CSV = './nga_test.csv'
THREAD = 'thread'
my_table = None


def get_page_source(my_t, tid, url, index):
    if index > 1:
        browser.get(url + "&page={}".format(j))
    else:
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
            if num == 0 and index == 1:
                is_master = True
            else:
                is_master = False
            # user id
            if table.xpath('.//a[@name="uid"]'):
                uid = table.xpath('.//a[@name="uid"]/text()')[0]
            else:
                uid = None
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

            # content not the first one
            if table.xpath('.//span[@class="postcontent ubbcode"]'):
                content = table.xpath('.//span[@class="postcontent ubbcode"]/text()')
                content = ''.join(content).strip().replace(',', ' ')
                # content - quote
                if table.xpath('.//span[@class="postcontent ubbcode"]//div[@class="quote"]'):
                    quote_author = []
                    # check if the quote has author
                    if table.xpath(
                            './/span[@class="postcontent ubbcode"]//div[@class="quote"]//a[@class="b"]/text()'):
                        quote_author.append(
                            table.xpath(
                                './/span[@class="postcontent ubbcode"]//div[@class="quote"]//b[@class="block_txt"]/text()')[0]
                        )
                        quote_author.append(
                            table.xpath(
                                './/span[@class="postcontent ubbcode"]//div[@class="quote"]//a[@class="b"]/text()')[1]
                        )
                        quote_author = ''.join(quote_author).replace(']', '')

                        quote_post_time = \
                            table.xpath('.//span[@class="postcontent ubbcode"]//div[@class="quote"]//span[@class="xtxt silver"]/text()')[0]
                        quote_post_time = quote_post_time[1:-1]
                    else:
                        quote_author = None
                        quote_post_time = None

                    quote = table.xpath('.//span[@class="postcontent ubbcode"]//div[@class="quote"]/text()')
                    quote = ''.join(quote).strip().replace(',', '')
                else:
                    quote_author = None
                    quote_post_time = None
                    quote = None
                # images in content
                imgs = table.xpath('.//span[@class="postcontent ubbcode"]//img')
                if imgs:
                    images = []
                    for img in imgs:
                        img_url = img.xpath('./@src')[0]
                        if img_url != 'about:blank':
                            images.append(img_url)
                else:
                    images = None
            # 版主 the first content
            elif table.xpath('.//p[@class="postcontent ubbcode"]'):
                content = table.xpath('.//p[@class="postcontent ubbcode"]/text()')
                content = ''.join(content).strip().replace(',', '')
                # quote
                has_quote = table.xpath('.//p[@class="postcontent ubbcode"]//div[@class="quote"]')
                if has_quote:
                    quote = []
                    for each in has_quote:
                        if each.xpath('.//h4[@class="subtitle"]'):
                            quote_h4 = each.xpath('.//h4[@class="subtitle"]/text()')[0]
                            quote.append(quote_h4)
                        each_quote = each.xpath('./text()')
                        each_quote = ''.join(each_quote).strip().replace(',', '')
                        quote.append(each_quote)
                    quote = ''.join(quote).strip().replace(',', '')
                else:
                    quote = None
                quote_author = None
                quote_post_time = None
                # all images
                imgs = table.xpath('.//p[@class="postcontent ubbcode"]//img')
                if imgs:
                    images = []
                    for img in imgs:
                        img_url = img.xpath('./@src')[0]
                        if img_url != 'about:blank':
                            images.append(img_url)
                else:
                    images = None
            else:
                content = None
                quote_author = None
                quote_post_time = None
                quote = None
                images = None

            data = {"topic_id": tid, "uid": uid, "user_level": ulevel, "user_prestige": uprestige,
                    "user_famous": ufamous, "register_date": uregister, "publish_date": pubdate,
                    "publish_source": source, "content": content, "quote_author": quote_author,
                    "quote_post_time": quote_post_time, "quote": quote, "image_url": images,
                    "is_master": is_master}
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
        if not page_count:
            page_count = 0
        if page_count == 0:
            my_table = get_page_source(my_table, topic_id, topic_url, index=1)
        else:
            for j in range(1, page_count + 1):
                my_table = get_page_source(my_table, topic_id, topic_url, index=j)

    # print(my_table.head())
    my_table.to_csv(r'./arknights_topics.csv', header=HEADERS, index=None, sep=',', mode='a')

    # closing the browser window
    browser.close()
