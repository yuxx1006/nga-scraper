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



url = "https://bbs.nga.cn/read.php?tid=18887364"

browser = Firefox()
browser.implicitly_wait(10)
browser.maximize_window()


headers = ['uid', 'user_level', 'user_prestige', 'user_famous',
			'register_date','publish_date','publish_source', 'content']


my_table = pd.DataFrame(columns=headers)

REPETITIONS = 50
for i in range(REPETITIONS):
	if i == 0: 
		continue

	if i == 1 or i == 2:
		sleep(10)
	else:
		sleep(3)



	# browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	browser.get(url+"&page={}".format(i))
	sleep(10)

	parser = etree.HTML(browser.page_source)
	# result = etree.tostring(parser)
	# print(result.decode('utf-8'))

	#collecting all container into a list and going through each one
	all_posts = parser.xpath('//div[@id="m_posts_c"]/table[@class="forumbox postbox"]')

	for table in all_posts:
		try:
			uid = table.xpath('.//a[@name="uid"]/text()')[0]
			ulevel = table.xpath('.//span[@class="silver"]/text()')[0]
			if table.xpath('.//span[@class="numericl silver"]/text()'):
				uprestige = table.xpath('.//span[@class="numericl silver"]/text()')[0]
			else:
				uprestige = None


			if table.xpath('.//span[@class="silver numericl"]/text()'):
				ufamous = table.xpath('.//span[@class="silver numericl"]/text()')[0]
			else:
				ufamous = None
			uregister = table.xpath('.//span[@name="regdate"]/text()')[0]
			pubdate = table.xpath('.//div[@class="postInfo"]//span[@class=" stxt"]/text()')[0]
			source = table.xpath('.//div[@class="postInfo"]//a[@class="  inlineBlock stxt"]/@title')[0]
			sources = source.strip()
			if 'Android' in sources:
				source = 'android'
			elif 'iOS' in sources:
				source = "ios"
			elif '/' in sources:
				source = 'nga'
			else: 
				source = 'other'

			content = table.xpath('.//span[@class="postcontent ubbcode"]/text()')
			content = ''.join(content).strip().replace(',',' ')
		except:
			pass




		data = {"uid":uid, "user_level": ulevel, "user_prestige": uprestige, "user_famous": ufamous,
			 "register_date": uregister, "publish_date": pubdate, "publish_source": source, 
			 "content": content}
		my_table = my_table.append(data, ignore_index=True)


#closing the browser window
browser.close()
print(my_table.head())


my_table.to_csv(r'./nga_zhao.csv', header=headers, index=None, sep=',', mode='a')





