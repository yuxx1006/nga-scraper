from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os

from selenium.webdriver import Chrome, Firefox, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pdb

from datetime import datetime
from time import sleep
from lxml import etree
import pandas as pd


url = "https://bbs.nga.cn/thread.php?fid=592"
# url = 'https://www.macys.com/shop/handbags-accessories/designer-handbags?id=69603&cm_sp=c2_1111INT_catsplash_handbags-%26-accessories-_-row2-_-imagemap_designer-handbags'

browser = Firefox()
browser.implicitly_wait(10)
browser.maximize_window()
sleep(2)


headers = ['topic', 'topic_description', 'reply_count', 'author_id',
			'author_name','post_time', 'last_reply_by', 'last_reply_time']

my_table = pd.DataFrame(columns=headers)

REPETITIONS = 20
for i in range(REPETITIONS):
	if i == 0: 
		continue

	# browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	browser.get(url+"&page={}".format(i))
	
	if i == 1 or i == 2:
		sleep(10)
	else:
		sleep(3)

	parser = etree.HTML(browser.page_source)
	# result = etree.tostring(parser)
	# print(result.decode('utf-8'))

	#collecting all container into a list and going through each one
	# all_products_listed =  parser.xpath('//div[@class="cell"]//ul[@class="items grid-x small-up-2 medium-up-3 large-up-3"]/li[@class="cell productThumbnailItem"]')
	all_posts = parser.xpath('//div[@id="m_threads"]//table[@class="forumbox "]/tbody')

	for table in all_posts:
		# print(table.xpath('.//a[@class="topic"]/span[@class="silver"]/text()'))
		top = table.xpath('.//a[@class="topic"]//span[@class="silver"]')

		topics = []

		if len(top) == 1:
			topics.append(table.xpath('.//a[@class="topic"]//span[@class="silver"]/text()')[0][1:-1])
		elif len(top) > 1:
			for each in top:
				topics.append(each.xpath('.//text()')[0][1:-1].replace(',',''))
		try: 
			if table.xpath('.//a[@class="topic"]'):		
				topic_des =  table.xpath('.//a[@class="topic"]/text()')[0]
			elif table.xpath('.//a[@class="topic AgEywho"]'): 	
				topic_des =  table.xpath('.//a[@class="topic AgEywho"]/text()')[0]
			else:
				None
		except:
			pass

		reply_count = table.xpath('.//a[@class="replies"]/text()')[0]

		author_id = table.xpath('.//a[@class="author"]/@title')[0]
		author_id = author_id.replace('用户ID ','')

		author_name = table.xpath('.//a[@class="author"]/text()')[0]

		post_time = table.xpath('.//span[@class="silver postdate"]/@title')[0]

		last_reply_time = table.xpath('.//a[@class="silver replydate"]/@title')[0]
		last_reply_by = table.xpath('.//span[@class="replyer"]/text()')[0]


		data = {
			"topic":topics, "topic_description": topic_des, "reply_count": reply_count, "author_id": author_id,
			"author_name": author_name, "post_time": post_time,"last_reply_by": last_reply_by, 
			"last_reply_time": last_reply_time
			 }
		my_table = my_table.append(data, ignore_index=True)

       


#closing the browser window
browser.close()
print(my_table.head())
# print(my_table.info())


my_table.to_csv(r'./nga_thread.csv', header=headers, index=None, sep=',', mode='a')





