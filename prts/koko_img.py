# -*- coding:utf-8 -*-
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
import re


browser = Firefox()
browser.implicitly_wait(10)
browser.maximize_window()

HEADERS = ['name', 'url']
my_table = pd.DataFrame(columns=HEADERS)
BASE_URL = 'https://kokodayo.fun/'
# WEB_BASE_URL = 'http://prts.wiki/w/'
# IMG_BASE_URL = "http://prts.wiki"


# stage_table = pd.read_csv('./prts_names.csv', names= ['name','url'])


# txt = 'background-repeat: no-repeat; display: block; width: 800px; height: 256px; background-image: url("/images/a/a3/活动预告-战地秘闻活动2.jpg"); background-size: 100%;'

# # start = re.search("background-image: url", txt)
# match = re.search(r'\(([^\)]+)\)', txt)
# match = match.group(0).replace('(','').replace(')','')

# print(match)



for i, row in stage_table.iterrows():
	try:
		if i == 0: continue
		stage_url = row['url']
		browser.get(stage_url)
		sleep(5)
		parser = etree.HTML(browser.page_source)
		# imgs = []
		print(row['name'])
		if parser.xpath('//div[@class="mw-body-content"]//div[@id="sys_container"]'):
			img = parser.xpath('//div[@id="gacha_info"]/@style')[0]
			match = re.search(r'\(([^\)]+)\)', img)
			match = IMG_BASE_URL + match.group(0).replace('(','').replace(')','')

			# for name in name_list:
			# 	name_url = name.xpath('./text()')[0]
			# 	total_url = WEB_BASE_URL + name_url

			data = {
				"name": row['name'],
				"url": row['url'],
				"img": match
			}	
				# data = {
				# 	"name": name_url,
				# 	"url": total_url
				# }
			my_table = my_table.append(data, ignore_index=True)
		else:
			print(stage)
			pass
		

	except Exception as e:
		print(e)
		pass


# data = {
# 		"name":name,
# 		"url": url 
# 		# "stage": stage, 
# 		# # "enemy": enemy, 
# 		# "image_urls": images, 
# 		# "extra_image_urls": extra_images,
# 		# "map_url": my_list
# 		# "enemy_img_url": images
# 		}
# my_table = my_table.append(data, ignore_index=True)
# 	# print(my_table.head())

browser.close()
my_table.to_csv(r'./data/prts_imgs_download.csv', header=HEADERS, index=None, sep=',', mode='a')
